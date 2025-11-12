#!/usr/bin/env python3
"""
Run All Benchmarks
Comprehensive benchmark suite for OPIC
"""

import json
import sys
import subprocess
from pathlib import Path
from datetime import datetime

def run_benchmark(name: str, command: list, timeout: int = 300) -> dict:
    """Run a benchmark and return results"""
    print(f"\n{'='*60}")
    print(f"Running: {name}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=Path(__file__).parent.parent
        )
        
        return {
            "name": name,
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        }
    except subprocess.TimeoutExpired:
        return {
            "name": name,
            "success": False,
            "error": "Timeout",
            "timeout": timeout
        }
    except Exception as e:
        return {
            "name": name,
            "success": False,
            "error": str(e)
        }

def run_python_benchmark(name: str, script: str) -> dict:
    """Run a Python benchmark script"""
    script_path = Path(__file__).parent / script
    if not script_path.exists():
        return {
            "name": name,
            "success": False,
            "error": f"Script not found: {script}"
        }
    
    return run_benchmark(name, ["python3", str(script_path)])

def main():
    """Run all benchmarks"""
    print("=" * 60)
    print("OPIC Comprehensive Benchmark Suite")
    print("=" * 60)
    print(f"Started: {datetime.now().isoformat()}")
    
    # Use .venv/bin/python3 if available (for numpy/scipy)
    python_cmd = ".venv/bin/python3" if (Path(__file__).parent.parent / ".venv" / "bin" / "python3").exists() else "python3"
    
    benchmarks = [
        ("Zeta Intelligence Benchmark", ["python3", "scripts/zib.py"]),
        ("Benchmark Evaluation", ["python3", "scripts/benchmark.py"]),
        ("Complexity SAT Benchmark", ["python3", "scripts/complexity_sat_benchmark.py"]),
        ("Spectral Unfold Compare", [python_cmd, "scripts/spectral_unfold_compare.py"]),
        ("Field Interaction Curvature", [python_cmd, "scripts/field_interaction_curvature.py"]),
        ("Mode 7 Lab", ["python3", "scripts/run_mode7_lab.py"]),
    ]
    
    results = []
    
    for name, command in benchmarks:
        result = run_benchmark(name, command)
        results.append(result)
        
        if result.get("success"):
            print(f"  ✓ {name}: PASSED")
        else:
            print(f"  ✗ {name}: FAILED")
            if "error" in result:
                print(f"    Error: {result['error']}")
    
    # Summary
    print("\n" + "=" * 60)
    print("Benchmark Summary")
    print("=" * 60)
    
    passed = sum(1 for r in results if r.get("success"))
    total = len(results)
    
    for result in results:
        status = "✓ PASS" if result.get("success") else "✗ FAIL"
        print(f"  {status}: {result['name']}")
    
    print(f"\nTotal: {passed}/{total} benchmarks passed")
    
    # Save results
    output_path = Path('results/all_benchmarks.json')
    output_path.parent.mkdir(exist_ok=True)
    
    summary = {
        "timestamp": datetime.now().isoformat(),
        "total": total,
        "passed": passed,
        "failed": total - passed,
        "results": results
    }
    
    with open(output_path, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\n✓ Results saved to {output_path}")
    
    if passed == total:
        print("\n✨ All benchmarks passed!")
        return 0
    else:
        print(f"\n⚠ {total - passed} benchmark(s) failed or had issues")
        return 1

if __name__ == "__main__":
    sys.exit(main())

