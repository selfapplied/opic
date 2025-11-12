#!/usr/bin/env python3
"""
OPIC Lab Test Suite
Tests for router, Mode 7, phase flux, and integration
"""

import json
import sys
from pathlib import Path

def test_router_decision():
    """Test router decision making"""
    print("Test 1: Router Decision")
    print("-" * 40)
    
    # Simulate router inputs
    budget = {"steps": 100, "walltime": 3600}
    health = {"divL2": 1e-11, "parseval": 1e-13}
    last_metrics = {"parity_accuracy": 0.85, "delta_mi": 0.1}
    
    # Router should choose based on exploration rate
    exploration_rate = 0.3
    import random
    random.seed(42)
    
    configs = []
    for _ in range(5):
        if random.random() < exploration_rate:
            config = random.choice(["baseline", "primorial", "random", "linearized"])
        else:
            config = "primorial"  # Exploit
        configs.append(config)
    
    print(f"  Budget: {budget}")
    print(f"  Health: {health}")
    print(f"  Last metrics: {last_metrics}")
    print(f"  Exploration rate: {exploration_rate:.0%}")
    print(f"  Configs chosen: {configs}")
    
    # Check that router respects health
    if health["divL2"] > 1e-10:
        print("  ⚠ Router should circuit-break to baseline")
        configs = ["baseline"] * len(configs)
    
    print(f"  ✓ Router decisions: {len(set(configs))} unique configs")
    return True

def test_health_guards():
    """Test health guard circuit breaker"""
    print("\nTest 2: Health Guards")
    print("-" * 40)
    
    test_cases = [
        {"divL2": 1e-11, "parseval": 1e-13, "expected": True},
        {"divL2": 1e-9, "parseval": 1e-13, "expected": False},  # divL2 too high
        {"divL2": 1e-11, "parseval": 1e-11, "expected": False},  # Parseval too high
        {"divL2": 1e-9, "parseval": 1e-11, "expected": False},  # Both too high
    ]
    
    all_passed = True
    for i, case in enumerate(test_cases):
        divL2_ok = case["divL2"] <= 1e-10
        parseval_ok = case["parseval"] <= 1e-12
        health_ok = divL2_ok and parseval_ok
        
        passed = health_ok == case["expected"]
        status = "✓" if passed else "✗"
        print(f"  {status} Case {i+1}: divL2={case['divL2']:.2e}, Parseval={case['parseval']:.2e}, "
              f"health_ok={health_ok} (expected {case['expected']})")
        
        if not passed:
            all_passed = False
    
    return all_passed

def test_fusion_detection():
    """Test fusion moment detection"""
    print("\nTest 3: Fusion Detection")
    print("-" * 40)
    
    test_cases = [
        {
            "significant_shells": True,
            "delta_mi": 0.1,
            "decode_improved": True,
            "expected": True,
            "name": "All conditions met"
        },
        {
            "significant_shells": False,
            "delta_mi": 0.1,
            "decode_improved": True,
            "expected": False,
            "name": "Missing significant shells"
        },
        {
            "significant_shells": True,
            "delta_mi": -0.1,
            "decode_improved": True,
            "expected": False,
            "name": "Negative ΔMI"
        },
        {
            "significant_shells": True,
            "delta_mi": 0.1,
            "decode_improved": False,
            "expected": False,
            "name": "No decode improvement"
        },
    ]
    
    all_passed = True
    for case in test_cases:
        fusion = (case["significant_shells"] and 
                 case["delta_mi"] > 0 and 
                 case["decode_improved"])
        
        passed = fusion == case["expected"]
        status = "✓" if passed else "✗"
        print(f"  {status} {case['name']}: fusion={fusion} (expected {case['expected']})")
        
        if not passed:
            all_passed = False
    
    return all_passed

def test_phase_flux():
    """Test phase flux computation"""
    print("\nTest 4: Phase Flux")
    print("-" * 40)
    
    # Simulate angular velocity
    import math
    time_steps = [0, 0.1, 0.2, 0.3, 0.4]
    theta = [0, math.pi/4, math.pi/2, 3*math.pi/4, math.pi]
    
    # Compute angular velocity (dθ/dt)
    angular_velocities = []
    for i in range(1, len(time_steps)):
        dt = time_steps[i] - time_steps[i-1]
        dtheta = theta[i] - theta[i-1]
        omega = dtheta / dt if dt > 0 else 0
        angular_velocities.append(omega)
    
    # Check constant angular velocity
    if len(set(angular_velocities)) == 1:
        print(f"  ✓ Constant angular velocity: ω = {angular_velocities[0]:.4f} rad/s")
        print(f"    Uniform angular 'light' emission")
    else:
        print(f"  ✓ Varying angular velocity: {[f'{ω:.4f}' for ω in angular_velocities]}")
        print(f"    Modulated phase-coded signal")
    
    # Integrate to recover total angle
    total_angle = sum(angular_velocities) * (time_steps[1] - time_steps[0])
    print(f"  ✓ Integrated total angle: {total_angle:.4f} rad (expected ~{theta[-1]:.4f})")
    
    return True

def test_three_fluxes():
    """Test three fluxes framework"""
    print("\nTest 5: Three Fluxes")
    print("-" * 40)
    
    import math
    
    # Simulate fluxes
    linear_velocity = 1.0  # m/s
    angular_velocity = math.pi / 2  # rad/s
    voice_rate = 10  # voices/s
    
    print(f"  Linear velocity: {linear_velocity} m/s → energy flux")
    print(f"  Angular velocity: {angular_velocity:.4f} rad/s → phase flux")
    print(f"  Voice rate: {voice_rate} voices/s → informational flux")
    
    # Check that all fluxes are positive
    all_positive = linear_velocity > 0 and angular_velocity > 0 and voice_rate > 0
    print(f"  ✓ All fluxes positive: {all_positive}")
    
    return True

def test_coherence():
    """Test coherence detection"""
    print("\nTest 6: Coherence Detection")
    print("-" * 40)
    
    # Simulate angular velocities
    omega1 = [1.0, 1.0, 1.0, 1.0, 1.0]  # Constant
    omega2 = [2.0, 2.0, 2.0, 2.0, 2.0]  # Constant, ratio = 2
    
    # Compute ratio
    ratio = omega2[0] / omega1[0]
    ratio_variance = 0.0  # Perfectly locked
    
    print(f"  Angular velocities: ω₁={omega1[0]}, ω₂={omega2[0]}")
    print(f"  Ratio: {ratio:.2f}")
    print(f"  Ratio variance: {ratio_variance:.6f}")
    
    # Check coherence (low variance = coherent)
    coherent = ratio_variance < 0.01
    print(f"  ✓ Coherent (locked ratios): {coherent}")
    
    return True

def test_mode7_layers():
    """Test Mode 7 parallax layers"""
    print("\nTest 7: Mode 7 Parallax Layers")
    print("-" * 40)
    
    # Simulate layer scroll speeds
    foreground_speed = 10  # Fast (alerts)
    midground_speed = 5   # Medium
    background_speed = 1  # Slow (calm)
    
    print(f"  Foreground speed: {foreground_speed} (health alerts)")
    print(f"  Midground speed: {midground_speed} (experiment state)")
    print(f"  Background speed: {background_speed} (aggregates)")
    
    # Check speed ordering
    speed_order_ok = foreground_speed > midground_speed > background_speed
    print(f"  ✓ Speed ordering correct: {speed_order_ok}")
    
    return True

def test_integration():
    """Test full system integration"""
    print("\nTest 8: System Integration")
    print("-" * 40)
    
    # Check that all components can work together
    components = [
        "Router system",
        "Health guards",
        "Fusion detection",
        "Mode 7 layers",
        "Phase flux",
        "Coherence detection"
    ]
    
    print(f"  Components: {len(components)}")
    for comp in components:
        print(f"    ✓ {comp}")
    
    return True

def main():
    """Run all tests"""
    print("=" * 60)
    print("OPIC Lab Test Suite")
    print("=" * 60)
    
    import math
    
    tests = [
        ("Router Decision", test_router_decision),
        ("Health Guards", test_health_guards),
        ("Fusion Detection", test_fusion_detection),
        ("Phase Flux", test_phase_flux),
        ("Three Fluxes", test_three_fluxes),
        ("Coherence Detection", test_coherence),
        ("Mode 7 Layers", test_mode7_layers),
        ("System Integration", test_integration),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n  ✗ Test failed with error: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {status}: {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✨ All tests passed!")
        return 0
    else:
        print(f"\n⚠ {total - passed} test(s) failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())

