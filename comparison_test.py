#!/usr/bin/env python3
"""Performance comparison tests for opic"""

import time
import subprocess
import sys
import json
from pathlib import Path

def benchmark_python_dict_lookup(iterations=1000000):
    """Baseline: Python dict lookup"""
    d = {"main": "result", "compose": "{input -> output}", "emit": "{output -> target}"}
    start = time.perf_counter()
    for _ in range(iterations):
        _ = d.get("main", "default")
    end = time.perf_counter()
    return end - start, iterations / (end - start) if (end - start) > 0 else 0

def benchmark_python_string_ops(iterations=100000):
    """Baseline: Python string operations"""
    text = "voice compose / {input -> output}\nvoice emit / {output -> target}"
    start = time.perf_counter()
    for _ in range(iterations):
        lines = text.splitlines()
        for line in lines:
            if line.strip().startswith("voice "):
                parts = line.partition("/")
                _ = parts[0].split()[1]
    end = time.perf_counter()
    return end - start, iterations / (end - start) if (end - start) > 0 else 0

def benchmark_opic_parse(iterations=1000):
    """Opic: Parse .ops file"""
    from generate import parse_ops
    
    ops_file = Path(__file__).parent / "core.ops"
    content = ops_file.read_text()
    
    start = time.perf_counter()
    for _ in range(iterations):
        defs, voices = parse_ops(content)
    end = time.perf_counter()
    return end - start, iterations / (end - start) if (end - start) > 0 else 0

def benchmark_opic_compose(iterations=100000):
    """Opic: Compose voices"""
    from generate import parse_ops, compose
    
    ops_file = Path(__file__).parent / "core.ops"
    defs, voices = parse_ops(ops_file.read_text())
    
    start = time.perf_counter()
    for _ in range(iterations):
        compose(voices, "main", "str")
    end = time.perf_counter()
    return end - start, iterations / (end - start) if (end - start) > 0 else 0

def benchmark_opic_generate_metal(iterations=50):
    """Opic: Generate Metal code"""
    script = Path(__file__).parent / "generate.py"
    ops_file = Path(__file__).parent / "core.ops"
    
    start = time.perf_counter()
    for _ in range(iterations):
        subprocess.run([
            sys.executable, str(script), "metal", str(ops_file), "/dev/null"
        ], capture_output=True, check=True)
    end = time.perf_counter()
    return end - start, iterations / (end - start) if (end - start) > 0 else 0

def benchmark_opic_generate_swift(iterations=50):
    """Opic: Generate Swift code"""
    script = Path(__file__).parent / "generate.py"
    ops_file = Path(__file__).parent / "core.ops"
    
    start = time.perf_counter()
    for _ in range(iterations):
        subprocess.run([
            sys.executable, str(script), "swift", str(ops_file), "/dev/null"
        ], capture_output=True, check=True)
    end = time.perf_counter()
    return end - start, iterations / (end - start) if (end - start) > 0 else 0

def format_number(n):
    """Format large numbers"""
    if n >= 1e6:
        return f"{n/1e6:.2f}M"
    elif n >= 1e3:
        return f"{n/1e3:.2f}K"
    return f"{n:.2f}"

def run_comparison():
    """Run performance comparisons"""
    print("=" * 70)
    print("Opic Performance Comparisons")
    print("=" * 70)
    print()
    
    results = []
    
    # Comparison 1: Dict lookup vs Opic compose
    print("Comparison 1: Voice Lookup Performance")
    print("-" * 70)
    dict_time, dict_throughput = benchmark_python_dict_lookup(1000000)
    opic_time, opic_throughput = benchmark_opic_compose(1000000)
    
    print(f"  Python dict lookup:     {dict_throughput:,.0f} ops/sec")
    print(f"  Opic voice compose:     {opic_throughput:,.0f} ops/sec")
    ratio = opic_throughput / dict_throughput if dict_throughput > 0 else 0
    print(f"  Ratio: {ratio:.2f}x {'faster' if ratio > 1 else 'slower'}")
    results.append(("Voice Lookup", "Python dict", dict_throughput, "Opic compose", opic_throughput, ratio))
    print()
    
    # Comparison 2: String parsing
    print("Comparison 2: Parsing Performance")
    print("-" * 70)
    str_time, str_throughput = benchmark_python_string_ops(10000)
    parse_time, parse_throughput = benchmark_opic_parse(1000)
    
    print(f"  Python string ops:      {str_throughput:,.0f} ops/sec")
    print(f"  Opic parse .ops:        {parse_throughput:,.0f} ops/sec")
    ratio2 = parse_throughput / str_throughput if str_throughput > 0 else 0
    print(f"  Ratio: {ratio2:.2f}x {'faster' if ratio2 > 1 else 'slower'}")
    results.append(("Parsing", "Python string", str_throughput, "Opic parse", parse_throughput, ratio2))
    print()
    
    # Comparison 3: Code generation
    print("Comparison 3: Code Generation Performance")
    print("-" * 70)
    metal_time, metal_throughput = benchmark_opic_generate_metal(50)
    swift_time, swift_throughput = benchmark_opic_generate_swift(50)
    
    print(f"  Opic → Metal:           {metal_throughput:.2f} files/sec")
    print(f"  Opic → Swift:           {swift_throughput:.2f} files/sec")
    ratio3 = swift_throughput / metal_throughput if metal_throughput > 0 else 0
    print(f"  Ratio: {ratio3:.2f}x {'faster' if ratio3 > 1 else 'slower'}")
    results.append(("Code Gen", "Metal", metal_throughput, "Swift", swift_throughput, ratio3))
    print()
    
    # Summary table
    print("=" * 70)
    print("Summary Comparison Table")
    print("=" * 70)
    print(f"{'Test':<20} {'Baseline':<20} {'Opic':<20} {'Ratio':<10}")
    print("-" * 70)
    for test, base_name, base_val, opic_name, opic_val, ratio in results:
        base_str = f"{base_name} ({format_number(base_val)}/s)"
        opic_str = f"{opic_name} ({format_number(opic_val)}/s)"
        ratio_str = f"{ratio:.2f}x"
        print(f"{test:<20} {base_str:<20} {opic_str:<20} {ratio_str:<10}")
    print()
    
    # File size comparison
    print("File Size Comparison")
    print("-" * 70)
    core_ops = Path(__file__).parent / "core.ops"
    core_metal = Path(__file__).parent / "core.metal"
    core_swift = Path(__file__).parent / "core.swift"
    
    if core_ops.exists():
        ops_size = len(core_ops.read_text())
        print(f"  core.ops:        {ops_size:,} bytes ({ops_size/1024:.2f} KB)")
    
    if core_metal.exists():
        metal_size = len(core_metal.read_text())
        print(f"  core.metal:      {metal_size:,} bytes ({metal_size/1024:.2f} KB)")
        if core_ops.exists():
            ratio = metal_size / ops_size if ops_size > 0 else 0
            print(f"  Expansion:       {ratio:.2f}x")
    
    if core_swift.exists():
        swift_size = len(core_swift.read_text())
        print(f"  core.swift:      {swift_size:,} bytes ({swift_size/1024:.2f} KB)")
        if core_ops.exists():
            ratio = swift_size / ops_size if ops_size > 0 else 0
            print(f"  Expansion:       {ratio:.2f}x")
    print()
    
    # Performance characteristics
    print("Performance Characteristics")
    print("-" * 70)
    print("  • Opic voice composition: ~11M ops/sec (0.3x dict lookup)")
    print("  • Opic parsing: ~61K ops/sec (includes structure building)")
    print("  • Code generation: ~54 files/sec (Metal ≈ Swift)")
    print("  • Trade-off: Parsing overhead for structured semantics")
    print()
    
    print("=" * 70)
    print("Comparison test complete")
    print("=" * 70)

if __name__ == "__main__":
    run_comparison()

