#!/usr/bin/env python3
"""Performance test using opic-generated Metal code"""

import time
import subprocess
import sys
from pathlib import Path

def generate_metal_test():
    """Generate Metal code from performance.ops"""
    script = Path(__file__).parent / "generate.py"
    ops_file = Path(__file__).parent / "performance.ops"
    metal_file = Path(__file__).parent / "performance.metal"
    
    subprocess.run([
        sys.executable, str(script), "metal", str(ops_file), str(metal_file)
    ], check=True)
    
    return metal_file.exists()

def benchmark_python_compose(iterations=1000):
    """Benchmark Python opic compose"""
    from generate import parse_ops, compose
    
    ops_file = Path(__file__).parent / "core.ops"
    defs, voices = parse_ops(ops_file.read_text())
    
    start = time.perf_counter()
    for _ in range(iterations):
        compose(voices, "main", "str")
    end = time.perf_counter()
    
    elapsed = end - start
    throughput = iterations / elapsed if elapsed > 0 else 0
    return elapsed, throughput

def benchmark_metal_compile():
    """Benchmark Metal compilation time"""
    metal_file = Path(__file__).parent / "performance.metal"
    if not metal_file.exists():
        return None, None
    
    start = time.perf_counter()
    try:
        result = subprocess.run(
            ["xcrun", "-sdk", "macosx", "metal", "-c", str(metal_file), "-o", "/tmp/performance.metallib"],
            capture_output=True,
            timeout=10
        )
        end = time.perf_counter()
        elapsed = end - start
        success = result.returncode == 0
        return elapsed, success
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return None, False

def benchmark_metal_execution(metallib_path, iterations=10000, data_size=1024):
    """Benchmark Metal GPU execution"""
    # Use default library from source instead of loading compiled library
    metal_source = Path(__file__).parent / "performance.metal"
    swift_code = f'''import Foundation
import Metal
let device = MTLCreateSystemDefaultDevice()!
let queue = device.makeCommandQueue()!
let source = try! String(contentsOfFile: "{metal_source}", encoding: .utf8)
let lib = try! device.makeLibrary(source: source, options: nil)
guard let kernelFunc = lib.makeFunction(name: "main_kernel") else {{
    print("ERROR: Kernel main_kernel not found")
    exit(1)
}}
let pipeline = try! device.makeComputePipelineState(function: kernelFunc)
let bufSize = {data_size} * MemoryLayout<Float>.size
let inBuf = device.makeBuffer(length: bufSize, options: [])!
let outBuf = device.makeBuffer(length: bufSize, options: [])!
let start = CFAbsoluteTimeGetCurrent()
for _ in 0..<{iterations} {{
    let cmd = queue.makeCommandBuffer()!
    let enc = cmd.makeComputeCommandEncoder()!
    enc.setComputePipelineState(pipeline)
    enc.setBuffer(inBuf, offset: 0, index: 0)
    enc.setBuffer(outBuf, offset: 0, index: 1)
    enc.dispatchThreadgroups(MTLSize(width: ({data_size}+255)/256, height: 1, depth: 1), threadsPerThreadgroup: MTLSize(width: min(256, {data_size}), height: 1, depth: 1))
    enc.endEncoding()
    cmd.commit()
    cmd.waitUntilCompleted()
}}
let elapsed = CFAbsoluteTimeGetCurrent() - start
print("METAL_TIME:", elapsed)
print("METAL_OPS:", Double({iterations} * {data_size}) / elapsed)
'''
    swift_file = Path("/tmp/metal_bench.swift")
    swift_file.write_text(swift_code)
    
    try:
        result = subprocess.run(
            ["swift", str(swift_file)],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            metal_time = None
            metal_throughput = None
            for line in result.stdout.splitlines():
                if "METAL_TIME:" in line:
                    metal_time = float(line.split(":")[1].strip())
                elif "METAL_OPS:" in line:
                    metal_throughput = float(line.split(":")[1].strip())
            if metal_time and metal_throughput:
                return metal_time, metal_throughput
        # Return error info for debugging
        error_msg = result.stderr if result.stderr else "Unknown error"
        if "ERROR:" in error_msg:
            return None, None, error_msg
        return None, None, None
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return None, None

def benchmark_python_simulate(iterations=10000, data_size=1024):
    """Simulate same computation in Python"""
    start = time.perf_counter()
    for _ in range(iterations):
        data = list(range(data_size))
        _ = [x for x in data]
    end = time.perf_counter()
    elapsed = end - start
    throughput = (iterations * data_size) / elapsed if elapsed > 0 else 0
    return elapsed, throughput

def benchmark_code_generation(iterations=100):
    """Benchmark opic code generation"""
    script = Path(__file__).parent / "generate.py"
    ops_file = Path(__file__).parent / "core.ops"
    
    start = time.perf_counter()
    for _ in range(iterations):
        subprocess.run([
            sys.executable, str(script), "metal", str(ops_file), "/dev/null"
        ], capture_output=True, check=True)
    end = time.perf_counter()
    
    elapsed = end - start
    throughput = iterations / elapsed if elapsed > 0 else 0
    return elapsed, throughput

def run_performance_test():
    """Run all performance benchmarks"""
    print("=" * 60)
    print("Opic Performance Test")
    print("=" * 60)
    print()
    
    # Test 1: Code generation
    print("Test 1: Code Generation Performance")
    print("-" * 60)
    gen_time, gen_throughput = benchmark_code_generation(iterations=50)
    print(f"  Generated 50 Metal files in {gen_time:.4f}s")
    print(f"  Throughput: {gen_throughput:.2f} files/sec")
    print(f"  Avg time per file: {(gen_time/50)*1000:.2f}ms")
    print()
    
    # Test 2: Python compose
    print("Test 2: Python Compose Performance")
    print("-" * 60)
    py_time, py_throughput = benchmark_python_compose(iterations=10000)
    print(f"  Composed 10,000 voices in {py_time:.4f}s")
    print(f"  Throughput: {py_throughput:,.0f} ops/sec")
    print(f"  Avg time per op: {(py_time/10000)*1e6:.2f}μs")
    print()
    
    # Test 3: Metal compilation and execution
    print("Test 3: Metal GPU Execution")
    print("-" * 60)
    if generate_metal_test():
        compile_time, success = benchmark_metal_compile()
        if compile_time is not None and success:
            print(f"  Compiled Metal shader in {compile_time:.4f}s")
            
            # Execute on GPU (use larger workload to show GPU advantage)
            metallib = Path("/tmp/performance.metallib")
            if metallib.exists():
                iterations = 1000
                data_size = 65536  # Larger data size for GPU parallelism
                result = benchmark_metal_execution(str(metallib), iterations, data_size)
                if len(result) == 3:
                    metal_time, metal_throughput, error = result
                else:
                    metal_time, metal_throughput = result
                    error = None
                
                if metal_time:
                    print(f"  GPU execution: {metal_time:.4f}s for {iterations * data_size:,} ops")
                    print(f"  GPU throughput: {metal_throughput:,.0f} ops/sec")
                    
                    # Compare with Python
                    py_time, py_throughput = benchmark_python_simulate(iterations, data_size)
                    speedup = py_time / metal_time if metal_time > 0 else 0
                    print(f"  Python (CPU): {py_time:.4f}s ({py_throughput:,.0f} ops/sec)")
                    print(f"  GPU speedup: {speedup:.2f}x {'faster' if speedup > 1 else 'slower'}")
                else:
                    if error:
                        print(f"  ⚠ Metal execution error: {error[:100]}")
                    else:
                        print("  ⚠ Could not execute Metal (check Swift/Metal runtime)")
            else:
                print("  ⚠ Metal library not found")
        else:
            print("  ⚠ Metal compiler not available")
    else:
        print("  ⚠ Could not generate Metal test file")
    print()
    
    # Summary
    print("Summary")
    print("-" * 60)
    print(f"  Code generation: {gen_throughput:.1f} files/sec")
    print(f"  Voice composition: {py_throughput:,.0f} ops/sec")
    if compile_time and success:
        print(f"  Metal compilation: {1/compile_time:.1f} shaders/sec")
    print()
    
    print("=" * 60)
    print("Performance test complete")
    print("=" * 60)

if __name__ == "__main__":
    run_performance_test()

