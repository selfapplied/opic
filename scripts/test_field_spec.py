#!/usr/bin/env python3
"""
Test runner for Field Spec 0.7 and Cycle-to-Dimension Principle
Verifies that all voices are available and can be executed
"""

import sys
from pathlib import Path

# Import opic executor
sys.path.insert(0, str(Path(__file__).parent))
from opic_executor import OpicExecutor


def test_field_spec_voices(executor: OpicExecutor) -> dict:
    """Test that Field Spec 0.7 voices are available"""
    results = {}
    
    # Test Pascal operations
    pascal_voices = [
        "pascal.add", "pascal.mul", "pascal.combination",
        "pascal.shadow", "pascal.trace7_position"
    ]
    results["pascal"] = all(v in executor.voices for v in pascal_voices)
    
    # Test Trigonometric operators
    trig_voices = [
        "trig.cos_theta", "trig.sin_theta", "trig.tan_theta",
        "trig.sec_theta", "trig.cot_theta", "trig.csc_theta"
    ]
    results["trig"] = all(v in executor.voices for v in trig_voices)
    
    # Test Flow symmetry
    flow_voices = [
        "flow.equilibrium", "flow.hermitian_flow",
        "flow.standing_wave", "flow.forward_bias", "flow.reverse_bias"
    ]
    # Check if at least 3 flow voices exist
    results["flow"] = sum(v in executor.voices for v in flow_voices) >= 3
    
    # Test Cycle-to-dimension
    cycle_voices = [
        "cycle.compute_phase", "cycle.compute_charge",
        "cycle.promote_to_operator", "cycle.learning_threshold",
        "cycle.identity_to_time", "cycle.dialogue_to_rotation",
        "cycle.trace7_fundamental"
    ]
    results["cycle"] = all(v in executor.voices for v in cycle_voices)
    
    # Test NLP cycles
    nlp_cycle_voices = [
        "nlp.masked_cycle", "nlp.masked_promotion",
        "nlp.attention_cycle", "nlp.hermitian_attention",
        "nlp.attention_dialogue", "nlp.training_epoch_cycle"
    ]
    results["nlp_cycles"] = all(v in executor.voices for v in nlp_cycle_voices)
    
    # Test Dimensional expansion
    dimension_voices = [
        "dimension.symmetry_break", "dimension.witness_event",
        "dimension.trace7_intersection"
    ]
    results["dimension"] = all(v in executor.voices for v in dimension_voices)
    
    return results


def test_cycle_execution(executor: OpicExecutor) -> dict:
    """Test that cycle voices can be executed"""
    results = {}
    
    # Test cycle phase computation
    try:
        result = executor.execute_voice("cycle.compute_phase", {"cycle": "test_cycle"})
        results["cycle_phase"] = result is not None
    except:
        results["cycle_phase"] = False
    
    # Test cycle promotion
    try:
        result = executor.execute_voice("cycle.promote_to_operator", {"cycle": "test_cycle"})
        results["cycle_promotion"] = result is not None
    except:
        results["cycle_promotion"] = False
    
    # Test learning threshold
    try:
        result = executor.execute_voice("cycle.learning_threshold", {"all_cycles": "test_cycles"})
        results["learning_threshold"] = result is not None
    except:
        results["learning_threshold"] = False
    
    return results


def test_nlp_cycle_execution(executor: OpicExecutor) -> dict:
    """Test that NLP cycle voices can be executed"""
    results = {}
    
    # Test masked cycle
    try:
        result = executor.execute_voice("nlp.masked_cycle", {"context": "test_context"})
        results["masked_cycle"] = result is not None
    except:
        results["masked_cycle"] = False
    
    # Test attention cycle
    try:
        result = executor.execute_voice("nlp.attention_cycle", {
            "token_i": "token1",
            "token_j": "token2"
        })
        results["attention_cycle"] = result is not None
    except:
        results["attention_cycle"] = False
    
    # Test hermitian attention
    try:
        result = executor.execute_voice("nlp.hermitian_attention", {
            "attention_cycle": "test_cycle"
        })
        results["hermitian_attention"] = result is not None
    except:
        results["hermitian_attention"] = False
    
    return results


def main():
    """Run all Field Spec 0.7 tests"""
    project_root = Path(__file__).parent.parent
    executor = OpicExecutor(project_root)
    
    print("=" * 60)
    print("Field Spec 0.7 Tests")
    print("=" * 60)
    print(f"\nLoaded {len(executor.voices)} voices\n")
    
    # Test 1: Voice availability
    print("Test 1: Voice Availability")
    print("-" * 60)
    availability = test_field_spec_voices(executor)
    for category, passed in availability.items():
        status = "✓" if passed else "✗"
        print(f"  {status} {category}: {'PASS' if passed else 'FAIL'}")
    
    all_available = all(availability.values())
    print(f"\n  Result: {sum(availability.values())}/{len(availability)} categories available")
    
    # Test 2: Cycle execution
    print("\nTest 2: Cycle Execution")
    print("-" * 60)
    cycle_exec = test_cycle_execution(executor)
    for test_name, passed in cycle_exec.items():
        status = "✓" if passed else "✗"
        print(f"  {status} {test_name}: {'PASS' if passed else 'FAIL'}")
    
    cycle_passed = all(cycle_exec.values())
    print(f"\n  Result: {sum(cycle_exec.values())}/{len(cycle_exec)} tests passed")
    
    # Test 3: NLP cycle execution
    print("\nTest 3: NLP Cycle Execution")
    print("-" * 60)
    nlp_exec = test_nlp_cycle_execution(executor)
    for test_name, passed in nlp_exec.items():
        status = "✓" if passed else "✗"
        print(f"  {status} {test_name}: {'PASS' if passed else 'FAIL'}")
    
    nlp_passed = all(nlp_exec.values())
    print(f"\n  Result: {sum(nlp_exec.values())}/{len(nlp_exec)} tests passed")
    
    # Summary
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"  Voice Availability: {'PASS' if all_available else 'FAIL'}")
    print(f"  Cycle Execution: {'PASS' if cycle_passed else 'FAIL'}")
    print(f"  NLP Cycle Execution: {'PASS' if nlp_passed else 'FAIL'}")
    
    all_passed = all_available and cycle_passed and nlp_passed
    print(f"\n  Overall: {'PASS' if all_passed else 'FAIL'}")
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())

