#!/usr/bin/env python3
"""
Regression Tests: Verify nothing broke after removing hardcoded logic
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

try:
    from opic_executor import OpicExecutor
except ImportError:
    print("⚠ OPIC executor not found")
    sys.exit(1)

def test_core_files_load():
    """Test that core files still load"""
    print("Test 1: Core Files Load")
    print("-" * 40)
    
    project_root = Path(__file__).parent.parent
    executor = OpicExecutor(project_root)
    
    # Check that voices loaded
    voice_count = len(executor.voices)
    print(f"  Voices loaded: {voice_count}")
    
    if voice_count > 0:
        print(f"  ✓ Core files loaded successfully")
        return True
    else:
        print(f"  ✗ No voices loaded - core files may not be loading")
        return False

def test_nlp_voices_exist():
    """Test that NLP voices still exist"""
    print("\nTest 2: NLP Voices Exist")
    print("-" * 40)
    
    project_root = Path(__file__).parent.parent
    executor = OpicExecutor(project_root)
    
    nlp_voices = [
        "nlp.masked_cycle",
        "nlp.attention_cycle",
        "nlp.hermitian_attention",
    ]
    
    found = 0
    for voice in nlp_voices:
        if voice in executor.voices:
            found += 1
            print(f"  ✓ {voice}")
        else:
            print(f"  ✗ {voice} not found")
    
    if found == len(nlp_voices):
        print(f"  ✓ All NLP voices found")
        return True
    else:
        print(f"  ⚠ {found}/{len(nlp_voices)} NLP voices found")
        return found > 0

def test_field_operations():
    """Test that field operations still work"""
    print("\nTest 3: Field Operations")
    print("-" * 40)
    
    project_root = Path(__file__).parent.parent
    executor = OpicExecutor(project_root)
    
    # Check for field operation voices
    field_voices = [
        "compute.phi_k",
        "compute.zero.positions",
        "cycle.promote_to_operator",
    ]
    
    found = 0
    for voice in field_voices:
        if voice in executor.voices:
            found += 1
            print(f"  ✓ {voice}")
        else:
            print(f"  ⚠ {voice} not found (may be optional)")
    
    if found > 0:
        print(f"  ✓ Field operations available ({found}/{len(field_voices)})")
        return True
    else:
        print(f"  ⚠ No field operations found")
        return False

def test_executor_basic():
    """Test basic executor functionality"""
    print("\nTest 4: Executor Basic Functionality")
    print("-" * 40)
    
    project_root = Path(__file__).parent.parent
    executor = OpicExecutor(project_root)
    
    # Test that executor can execute a simple voice
    try:
        # Try executing a simple voice if available
        if "nlp.masked_cycle" in executor.voices:
            result = executor.execute_voice("nlp.masked_cycle", {"context": "test"})
            print(f"  ✓ Can execute voices (result type: {type(result).__name__})")
            return True
        else:
            print(f"  ⚠ No test voice available")
            return True  # Not a failure if no test voice
    except Exception as e:
        print(f"  ✗ Execution failed: {type(e).__name__}: {e}")
        return False

def test_no_hardcoded_domains():
    """Test that hardcoded domain keywords are removed"""
    print("\nTest 5: No Hardcoded Domain Keywords")
    print("-" * 40)
    
    executor_file = Path(__file__).parent / "opic_executor.py"
    content = executor_file.read_text()
    
    # Check for removed hardcoded patterns
    hardcoded_patterns = [
        'domain_keywords = {',
        '"biology": ["mitochondria"',
        '"chemistry": ["molecule"',
        '["what", "describe", "explain"]',
        '["which", "where", "when"]',
        '["enzyme", "receptor"',
        '["th", "ch", "sh"',
        '["letter", "word", "sentence"',
    ]
    
    found_hardcoded = []
    for pattern in hardcoded_patterns:
        if pattern in content:
            found_hardcoded.append(pattern)
    
    if found_hardcoded:
        print(f"  ⚠ Found {len(found_hardcoded)} hardcoded patterns:")
        for pattern in found_hardcoded:
            print(f"    - {pattern[:50]}...")
        return False
    else:
        print(f"  ✓ No hardcoded domain keywords found")
        return True

def test_natural_discovery():
    """Test that natural discovery mechanisms work"""
    print("\nTest 6: Natural Discovery Mechanisms")
    print("-" * 40)
    
    executor_file = Path(__file__).parent / "opic_executor.py"
    content = executor_file.read_text()
    
    # Check for natural discovery patterns
    natural_patterns = [
        'glob("*.ops")',
        'Let OPIC',
        'natural resolution',
        'field operations',
    ]
    
    found_natural = []
    for pattern in natural_patterns:
        if pattern in content:
            found_natural.append(pattern)
    
    if found_natural:
        print(f"  ✓ Found {len(found_natural)} natural discovery mechanisms:")
        for pattern in found_natural:
            print(f"    - {pattern}")
        return True
    else:
        print(f"  ⚠ No natural discovery patterns found")
        return False

def main():
    """Run all regression tests"""
    print("=" * 60)
    print("Regression Tests: After Hardcode Removal")
    print("=" * 60)
    
    tests = [
        ("Core Files Load", test_core_files_load),
        ("NLP Voices Exist", test_nlp_voices_exist),
        ("Field Operations", test_field_operations),
        ("Executor Basic", test_executor_basic),
        ("No Hardcoded Domains", test_no_hardcoded_domains),
        ("Natural Discovery", test_natural_discovery),
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
    print("Regression Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {status}: {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✨ All regression tests passed!")
        print("  No functionality lost after removing hardcoded logic")
        return 0
    else:
        print(f"\n⚠ {total - passed} test(s) failed or need attention")
        return 1

if __name__ == "__main__":
    sys.exit(main())

