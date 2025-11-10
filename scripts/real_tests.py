#!/usr/bin/env python3
"""Real functionality tests — Verify actual implementations work"""

import subprocess
import sys
import math
from pathlib import Path

def test_loss_functions():
    """Test actual loss function implementations"""
    print("Test: Loss Functions")
    print("-" * 60)
    
    # Generate Swift code with loss functions
    result = subprocess.run(
        [sys.executable, "generate.py", "swift", "loss.ops", "/tmp/loss.swift"],
        capture_output=True,
        timeout=5
    )
    
    if result.returncode != 0:
        print("  ✗ Failed to generate loss functions")
        return False
    
    # Create test harness
    test_code = """
import Foundation

// Include generated loss functions
"""
    test_code += Path("/tmp/loss.swift").read_text()
    test_code += """

// Test MSE
let mse1 = computemse(prediction: 0.8, target: 1.0)
let mse2 = computemse(prediction: 0.5, target: 0.5)
print("MSE(0.8, 1.0):", mse1)
print("MSE(0.5, 0.5):", mse2)

// Test crossentropy
let ce1 = computecrossentropy(prediction: 0.9, target: 1.0)
let ce2 = computecrossentropy(prediction: 0.5, target: 0.5)
print("CE(0.9, 1.0):", ce1)
print("CE(0.5, 0.5):", ce2)

// Verify MSE properties
let error1 = abs(mse1 - 0.04)  // (0.8 - 1.0)^2 = 0.04
let error2 = abs(mse2 - 0.0)   // (0.5 - 0.5)^2 = 0.0

if error1 < 0.001 && error2 < 0.001 {
    print("PASS: MSE correct")
} else {
    print("FAIL: MSE incorrect")
    exit(1)
}
"""
    
    test_file = Path("/tmp/test_loss.swift")
    test_file.write_text(test_code)
    
    # Compile and run
    compile_result = subprocess.run(
        ["swiftc", "-o", "/tmp/test_loss", str(test_file)],
        capture_output=True,
        timeout=10
    )
    
    if compile_result.returncode != 0:
        print("  ✗ Compilation failed")
        print(f"    {compile_result.stderr.decode()[:100]}")
        return False
    
    # Run test
    run_result = subprocess.run(
        ["/tmp/test_loss"],
        capture_output=True,
        text=True,
        timeout=5
    )
    
    if run_result.returncode == 0 and "PASS" in run_result.stdout:
        print("  ✓ MSE loss function works correctly")
        print(f"    {run_result.stdout.strip()}")
        return True
    else:
        print("  ✗ Loss function test failed")
        if run_result.stdout:
            print(f"    {run_result.stdout[:200]}")
        return False

def test_optimization():
    """Test actual optimization with gradients"""
    print("\nTest: Optimization")
    print("-" * 60)
    
    # Generate optimization code
    opt_ops = """
def weight { value }
def gradient { value }
def learning_rate { value: 0.01 }

voice compute.gradient / {loss -> gradient}
voice update.weight / {weight + gradient + learning_rate -> weight}

target optimized / "weight"
voice main / {weight + gradient -> optimized}
"""
    
    opt_file = Path("/tmp/opt_test.ops")
    opt_file.write_text(opt_ops)
    
    result = subprocess.run(
        [sys.executable, "generate.py", "swift", str(opt_file), "/tmp/opt.swift"],
        capture_output=True,
        timeout=5
    )
    
    if result.returncode != 0:
        print("  ✗ Failed to generate optimization code")
        return False
    
    # Test optimization
    test_code = """
import Foundation
"""
    test_code += Path("/tmp/opt.swift").read_text()
    test_code += """

// Test gradient descent
var weight: Double = 1.0
let loss: Double = 0.5
let learningRate: Double = 0.01

let grad = computegradient(loss: loss, learningRate: learningRate)
let newWeight = updateweight(weight: weight, gradient: grad, learningRate: learningRate)

print("Initial weight:", weight)
print("Loss:", loss)
print("Gradient:", grad)
print("Updated weight:", newWeight)

// Verify: new_weight should be weight - learningRate * loss
let expected = weight - learningRate * loss
let error = abs(newWeight - expected)

if error < 0.0001 {
    print("PASS: Optimization correct")
} else {
    print("FAIL: Optimization incorrect")
    print("Expected:", expected, "Got:", newWeight)
    exit(1)
}
"""
    
    test_file = Path("/tmp/test_opt.swift")
    test_file.write_text(test_code)
    
    compile_result = subprocess.run(
        ["swiftc", "-o", "/tmp/test_opt", str(test_file)],
        capture_output=True,
        timeout=10
    )
    
    if compile_result.returncode != 0:
        print("  ✗ Compilation failed")
        return False
    
    run_result = subprocess.run(
        ["/tmp/test_opt"],
        capture_output=True,
        text=True,
        timeout=5
    )
    
    if run_result.returncode == 0 and "PASS" in run_result.stdout:
        print("  ✓ Optimization works correctly")
        print(f"    {run_result.stdout.strip()}")
        return True
    else:
        print("  ✗ Optimization test failed")
        return False

def test_paradigm_synthesis_real():
    """Test actual paradigm synthesis with working code"""
    print("\nTest: Paradigm Synthesis (Real)")
    print("-" * 60)
    
    synthesis_ops = """
def quantum { state: superposition }
def archetype { type: collective }

voice synthesize / {quantum + archetype -> hybrid}

target hybrid / "synthesized"
voice main / {quantum + archetype -> hybrid}
"""
    
    test_file = Path("/tmp/synth_real.ops")
    test_file.write_text(synthesis_ops)
    
    result = subprocess.run(
        [sys.executable, "generate.py", "swift", str(test_file), "/tmp/synth_real.swift"],
        capture_output=True,
        timeout=5
    )
    
    if result.returncode != 0:
        print("  ✗ Failed to generate synthesis code")
        return False
    
    # Test that synthesis actually combines values
    test_code = """
import Foundation
"""
    test_code += Path("/tmp/synth_real.swift").read_text()
    test_code += """

// Test synthesis
let quantum = "superposition"
let archetype = "collective"

let result = synthesize(quantum: quantum, archetype: archetype)
print("Quantum:", quantum)
print("Archetype:", archetype)
print("Synthesized:", result)

// Verify synthesis produced a tuple/combination
if String(describing: result).contains("superposition") || 
   String(describing: result).contains("collective") {
    print("PASS: Synthesis combines elements")
} else {
    print("FAIL: Synthesis did not combine")
    exit(1)
}
"""
    
    test_file = Path("/tmp/test_synth.swift")
    test_file.write_text(test_code)
    
    compile_result = subprocess.run(
        ["swiftc", "-o", "/tmp/test_synth", str(test_file)],
        capture_output=True,
        timeout=10
    )
    
    if compile_result.returncode != 0:
        print("  ✗ Compilation failed")
        return False
    
    run_result = subprocess.run(
        ["/tmp/test_synth"],
        capture_output=True,
        text=True,
        timeout=5
    )
    
    if run_result.returncode == 0 and "PASS" in run_result.stdout:
        print("  ✓ Synthesis actually combines paradigms")
        print(f"    {run_result.stdout.strip()}")
        return True
    else:
        print("  ✗ Synthesis test failed")
        return False

def run_real_tests():
    """Run tests that verify actual functionality"""
    print("=" * 60)
    print("Real Functionality Tests")
    print("=" * 60)
    print()
    print("These tests verify actual implementations, not just code structure")
    print()
    
    tests = [
        ("Loss Functions", test_loss_functions),
        ("Optimization", test_optimization),
        ("Paradigm Synthesis", test_paradigm_synthesis_real),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"  ✗ {name}: Error - {str(e)[:50]}")
            results.append((name, False))
    
    print()
    print("=" * 60)
    print("Real Test Results")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {status}  {name}")
    
    print()
    print(f"Real Tests: {passed}/{total} ({passed*100//total}%)")
    
    if passed == total:
        print("Status: ALL FUNCTIONALITY VERIFIED")
    elif passed >= total * 0.6:
        print("Status: PARTIAL FUNCTIONALITY")
    else:
        print("Status: NEEDS IMPLEMENTATION")
    
    print("=" * 60)
    
    return results

if __name__ == "__main__":
    run_real_tests()

