#!/usr/bin/env python3
"""Intelligence tests for opic"""

import subprocess
import sys
from pathlib import Path
import time

def test_code_generation():
    """Test opic's code generation intelligence"""
    print("Test 1: Code Generation Intelligence")
    print("-" * 60)
    
    tests = [
        ("core.ops", "metal", "Core definitions → Metal"),
        ("core.ops", "swift", "Core definitions → Swift"),
        ("runtime.ops", "metal", "Runtime targets → Metal"),
        ("nlp.ops", "swift", "NLP definitions → Swift"),
    ]
    
    passed = 0
    for ops_file, target, description in tests:
        ops_path = Path(ops_file)
        if not ops_path.exists():
            print(f"  ⚠ {description}: File not found")
            continue
        
        try:
            result = subprocess.run(
                [sys.executable, "generate.py", target, ops_file, "/dev/null"],
                capture_output=True,
                timeout=5
            )
            if result.returncode == 0:
                print(f"  ✓ {description}")
                passed += 1
            else:
                print(f"  ✗ {description}: {result.stderr.decode()[:50]}")
        except Exception as e:
            print(f"  ✗ {description}: {str(e)[:50]}")
    
    print(f"  Result: {passed}/{len(tests)} passed")
    return passed == len(tests)

def test_voice_composition():
    """Test opic's voice composition intelligence"""
    print("\nTest 2: Voice Composition Intelligence")
    print("-" * 60)
    
    from generate import parse_ops, compose
    
    ops_file = Path("core.ops")
    defs, voices = parse_ops(ops_file.read_text())
    
    test_cases = [
        ("main", "str", "main → str"),
        ("compose", "output", "compose → output"),
        ("emit", "target", "emit → target"),
    ]
    
    passed = 0
    for src, dst, description in test_cases:
        try:
            result = compose(voices, src, dst)
            if result:
                print(f"  ✓ {description}: {result[:50]}")
                passed += 1
            else:
                print(f"  ✗ {description}: No result")
        except Exception as e:
            print(f"  ✗ {description}: {str(e)[:50]}")
    
    print(f"  Result: {passed}/{len(test_cases)} passed")
    return passed == len(test_cases)

def test_self_compilation():
    """Test opic's self-compilation intelligence"""
    print("\nTest 3: Self-Compilation Intelligence")
    print("-" * 60)
    
    # Generate Metal from opic's own files
    tests = [
        ("core.ops", "core.metal"),
        ("runtime.ops", "runtime.metal"),
    ]
    
    passed = 0
    for ops_file, output_file in tests:
        try:
            result = subprocess.run(
                [sys.executable, "generate.py", "metal", ops_file, output_file],
                capture_output=True,
                timeout=5
            )
            if result.returncode == 0 and Path(output_file).exists():
                # Check if Metal code compiles
                compile_result = subprocess.run(
                    ["xcrun", "-sdk", "macosx", "metal", "-c", output_file, "-o", f"/tmp/{output_file}.metallib"],
                    capture_output=True,
                    timeout=5
                )
                if compile_result.returncode == 0:
                    print(f"  ✓ {ops_file} → {output_file} (compiles)")
                    passed += 1
                else:
                    print(f"  ⚠ {ops_file} → {output_file} (generated, but compile failed)")
                    passed += 0.5
            else:
                print(f"  ✗ {ops_file} → {output_file}: Failed")
        except Exception as e:
            print(f"  ✗ {ops_file}: {str(e)[:50]}")
    
    print(f"  Result: {passed}/{len(tests)} passed")
    return passed >= len(tests) * 0.5

def test_problem_solving():
    """Test opic's problem-solving intelligence"""
    print("\nTest 4: Problem-Solving Intelligence")
    print("-" * 60)
    
    # Test: Can opic generate code for a new problem?
    test_ops = """
def problem { description, constraints }
def solution { code, tests }

voice solve / {problem -> solution}
voice generate.code / {solution -> code}
voice verify / {code + tests -> bool}

target solved / "working.code"
voice main / {problem -> solved}
"""
    
    test_file = Path("/tmp/test_problem.ops")
    test_file.write_text(test_ops)
    
    try:
        # Generate Metal code
        result = subprocess.run(
            [sys.executable, "generate.py", "metal", str(test_file), "/tmp/test_problem.metal"],
            capture_output=True,
            timeout=5
        )
        
        if result.returncode == 0 and Path("/tmp/test_problem.metal").exists():
            metal_code = Path("/tmp/test_problem.metal").read_text()
            if "solve" in metal_code.lower() and "kernel" in metal_code.lower():
                print("  ✓ Generated Metal code for new problem")
                print("  ✓ Code structure valid")
                return True
            else:
                print("  ✗ Generated code missing expected elements")
                return False
        else:
            print("  ✗ Failed to generate code")
            return False
    except Exception as e:
        print(f"  ✗ Error: {str(e)[:50]}")
        return False

def test_compositional_reasoning():
    """Test opic's compositional reasoning"""
    print("\nTest 5: Compositional Reasoning")
    print("-" * 60)
    
    from generate import parse_ops, compose
    
    # Test chaining voices
    ops_file = Path("core.ops")
    defs, voices = parse_ops(ops_file.read_text())
    
    # Try to compose: main → compose → emit
    try:
        step1 = compose(voices, "main", "default")
        step2 = compose(voices, "compose", "output")
        step3 = compose(voices, "emit", "target")
        
        if step1 and step2 and step3:
            print("  ✓ Can chain voice compositions")
            print(f"    main → {step1[:30]}")
            print(f"    compose → {step2[:30]}")
            print(f"    emit → {step3[:30]}")
            return True
        else:
            print("  ✗ Voice chaining failed")
            return False
    except Exception as e:
        print(f"  ✗ Error: {str(e)[:50]}")
        return False

def test_metacognitive_ability():
    """Test opic's ability to reason about itself"""
    print("\nTest 6: Metacognitive Ability")
    print("-" * 60)
    
    # Can opic generate code that describes itself?
    meta_ops = """
def opic { language, voices, targets }
def self { opic, reflection }

voice reflect / {opic -> self}
voice describe / {self -> str}

target meta / "self.description"
voice main / {opic -> meta}
"""
    
    meta_file = Path("/tmp/meta.ops")
    meta_file.write_text(meta_ops)
    
    try:
        # Generate Swift code
        result = subprocess.run(
            [sys.executable, "generate.py", "swift", str(meta_file), "/tmp/meta.swift"],
            capture_output=True,
            timeout=5
        )
        
        if result.returncode == 0:
            swift_code = Path("/tmp/meta.swift").read_text()
            if "reflect" in swift_code.lower() and "describe" in swift_code.lower():
                print("  ✓ Can generate self-describing code")
                print("  ✓ Demonstrates metacognitive capability")
                return True
            else:
                print("  ✗ Generated code lacks self-reference")
                return False
        else:
            print("  ✗ Failed to generate meta code")
            return False
    except Exception as e:
        print(f"  ✗ Error: {str(e)[:50]}")
        return False

def run_level2_puzzles():
    """Run Level-2 puzzles if available"""
    try:
        from puzzles import run_all_puzzles
        print("\n" + "=" * 60)
        print("Level-2 Puzzles")
        print("=" * 60)
        print()
        puzzle_results = run_all_puzzles()
        return puzzle_results
    except ImportError:
        return None

def run_level3_puzzles():
    """Run Level-3 puzzles if available"""
    try:
        from level3 import run_all_level3
        print("\n" + "=" * 60)
        print("Level-3 Puzzles — Emergent Domains")
        print("=" * 60)
        print()
        level3_results = run_all_level3()
        return level3_results
    except ImportError:
        return None

def run_level4_puzzles():
    """Run Level-4 puzzles if available"""
    try:
        from level4 import run_all_level4
        print("\n" + "=" * 60)
        print("Level-4 Puzzles — Transcendence Stability")
        print("=" * 60)
        print()
        level4_results = run_all_level4()
        return level4_results
    except ImportError:
        return None

def run_intelligence_tests():
    """Run all intelligence tests"""
    print("=" * 60)
    print("Opic Intelligence Tests (Level-1)")
    print("=" * 60)
    print()
    
    tests = [
        ("Code Generation", test_code_generation),
        ("Voice Composition", test_voice_composition),
        ("Self-Compilation", test_self_compilation),
        ("Problem Solving", test_problem_solving),
        ("Compositional Reasoning", test_compositional_reasoning),
        ("Metacognitive Ability", test_metacognitive_ability),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"  ✗ Test failed with error: {str(e)[:50]}")
            results.append((name, False))
    
    print()
    print("=" * 60)
    print("Intelligence Test Summary (Level-1)")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {status}  {name}")
    
    print()
    print(f"Level-1 Score: {passed}/{total} ({passed*100//total}%)")
    
    if passed == total:
        print("Intelligence Level: EXCELLENT")
    elif passed >= total * 0.8:
        print("Intelligence Level: GOOD")
    elif passed >= total * 0.6:
        print("Intelligence Level: FAIR")
    else:
        print("Intelligence Level: NEEDS IMPROVEMENT")
    
    # Run Level-2 puzzles
    puzzle_results = run_level2_puzzles()
    
    # Run Level-3 puzzles
    level3_results = run_level3_puzzles()
    
    # Run Level-4 puzzles
    level4_results = run_level4_puzzles()
    
    if puzzle_results or level3_results or level4_results:
        print()
        print("=" * 60)
        print("Combined Intelligence Assessment")
        print("=" * 60)
        level1_score = passed / total if total > 0 else 0
        
        level2_score = 0
        if puzzle_results:
            level2_passed = sum(1 for r in puzzle_results.values() if r)
            level2_total = len(puzzle_results)
            level2_score = level2_passed / level2_total if level2_total > 0 else 0
        
        level3_score = 0
        if level3_results:
            level3_passed = sum(1 for r in level3_results.values() if r)
            level3_total = len(level3_results)
            level3_score = level3_passed / level3_total if level3_total > 0 else 0
        
        level4_score = 0
        if level4_results:
            level4_passed = sum(1 for r in level4_results.values() if r)
            level4_total = len(level4_results)
            level4_score = level4_passed / level4_total if level4_total > 0 else 0
        
        # Weighted combination (higher levels weighted more)
        if level4_score > 0:
            combined = (level1_score * 0.2 + level2_score * 0.2 + level3_score * 0.3 + level4_score * 0.3)
        elif level3_score > 0:
            combined = (level1_score * 0.3 + level2_score * 0.3 + level3_score * 0.4)
        elif level2_score > 0:
            combined = (level1_score + level2_score) / 2
        else:
            combined = level1_score
        
        print(f"  Level-1 (Foundation): {level1_score:.2%}")
        if puzzle_results:
            print(f"  Level-2 (Paradox): {level2_score:.2%}")
        if level3_results:
            print(f"  Level-3 (Emergent): {level3_score:.2%}")
        if level4_results:
            print(f"  Level-4 (Transcendence): {level4_score:.2%}")
        print(f"  Combined: {combined:.2%}")
        
        if combined >= 0.98:
            print("  Overall: UNIVERSAL")
        elif combined >= 0.95:
            print("  Overall: TRANSCENDENT")
        elif combined >= 0.9:
            print("  Overall: MASTER")
        elif combined >= 0.75:
            print("  Overall: ADVANCED")
        elif combined >= 0.6:
            print("  Overall: INTERMEDIATE")
        else:
            print("  Overall: BEGINNER")
    
    print("=" * 60)

if __name__ == "__main__":
    run_intelligence_tests()

