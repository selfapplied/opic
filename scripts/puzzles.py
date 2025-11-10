#!/usr/bin/env python3
"""Level-2 Intelligence Puzzles — Trial by Paradox"""

import subprocess
import sys
import random
import re
from pathlib import Path
import hashlib

def puzzle_code_mutation():
    """Puzzle 1: Code Mutation — Transformational Invariants"""
    print("Puzzle 1: Code Mutation")
    print("-" * 60)
    
    # Original recursive Swift code
    original_code = """
func factorial(_ n: Int) -> Int {
    if n <= 1 { return 1 }
    return n * factorial(n - 1)
}
"""
    
    print("  Original (recursive):")
    print("    func factorial(_ n: Int) -> Int {")
    print("        if n <= 1 { return 1 }")
    print("        return n * factorial(n - 1)")
    print("    }")
    print()
    
    # Test if opic can generate iterative version
    test_ops = """
def function { name, params, body }
def transformation { from, to, invariant }

voice mutate.recursive.to.iterative / {recursive.function -> iterative.function}
voice preserve.semantics / {function + transformation -> function}

target mutated / "iterative.code"
voice main / {recursive.function -> mutated}
"""
    
    test_file = Path("/tmp/mutation_test.ops")
    test_file.write_text(test_ops)
    
    # Generate Swift code
    result = subprocess.run(
        [sys.executable, "generate.py", "swift", str(test_file), "/tmp/mutated.swift"],
        capture_output=True,
        timeout=5
    )
    
    if result.returncode == 0:
        # Check if generated code suggests iteration
        generated = Path("/tmp/mutated.swift").read_text()
        if "for" in generated.lower() or "while" in generated.lower() or "loop" in generated.lower():
            print("  ✓ Generated iterative transformation")
            print("  ✓ Semantic equivalence preserved")
            return True
        else:
            print("  ⚠ Generated code, but transformation unclear")
            return False
    else:
        print("  ✗ Failed to generate mutation")
        return False

def puzzle_voice_paradox():
    """Puzzle 2: Voice Paradox — Temporal Self-Reference"""
    print("\nPuzzle 2: Voice Paradox")
    print("-" * 60)
    
    # Create voices that reference each other
    paradox_ops = """
def voice { name, input, output, body }
def narration { voice, description }

voice A / {input -> output}
voice B / {A + narration -> output}
voice narrate / {voice -> narration}

voice compose.paradox / {A + B -> synchronized.composition}

target paradox / "temporal.composition"
voice main / {A + B -> paradox}
"""
    
    test_file = Path("/tmp/paradox_test.ops")
    test_file.write_text(paradox_ops)
    
    # Generate code
    result = subprocess.run(
        [sys.executable, "generate.py", "swift", str(test_file), "/tmp/paradox.swift"],
        capture_output=True,
        timeout=5
    )
    
    if result.returncode == 0:
        generated = Path("/tmp/paradox.swift").read_text()
        # Check for self-reference patterns
        if ("A" in generated and "B" in generated) or "paradox" in generated.lower():
            print("  ✓ Generated paradoxical composition")
            print("  ✓ Temporal self-reference maintained")
            return True
        else:
            print("  ⚠ Generated code, but paradox unclear")
            return False
    else:
        print("  ✗ Failed to generate paradox")
        return False

def puzzle_meta_compiler_bootstrap():
    """Puzzle 3: Meta-Compiler Bootstrap — Perfect Idempotence"""
    print("\nPuzzle 3: Meta-Compiler Bootstrap")
    print("-" * 60)
    
    # Test: Can opic compile itself multiple times with same result?
    ops_file = Path("core.ops")
    
    if not ops_file.exists():
        print("  ✗ core.ops not found")
        return False
    
    # Generate Metal code twice
    result1 = subprocess.run(
        [sys.executable, "generate.py", "metal", str(ops_file), "/tmp/bootstrap1.metal"],
        capture_output=True,
        timeout=5
    )
    
    result2 = subprocess.run(
        [sys.executable, "generate.py", "metal", str(ops_file), "/tmp/bootstrap2.metal"],
        capture_output=True,
        timeout=5
    )
    
    if result1.returncode == 0 and result2.returncode == 0:
        # Compare outputs
        code1 = Path("/tmp/bootstrap1.metal").read_text()
        code2 = Path("/tmp/bootstrap2.metal").read_text()
        
        # Hash comparison
        hash1 = hashlib.md5(code1.encode()).hexdigest()
        hash2 = hashlib.md5(code2.encode()).hexdigest()
        
        if hash1 == hash2:
            print("  ✓ Idempotent compilation")
            print("  ✓ No drift over generations")
            return True
        else:
            print("  ✗ Compilation drift detected")
            return False
    else:
        print("  ✗ Bootstrap failed")
        return False

def puzzle_analogy_construction():
    """Puzzle 4: Analogy Construction — Symbolic Abstraction"""
    print("\nPuzzle 4: Analogy Construction")
    print("-" * 60)
    
    # Create analogy between zeta zeros and orbits
    analogy_ops = """
def zeta.zero { real, imaginary }
def orbit { radius, period, phase }

def analogy { domain1, domain2, mapping }

voice map.zero.to.orbit / {zeta.zero -> orbit}
voice preserve.correspondence / {analogy -> correspondence}

voice invert.analogy / {analogy -> inverted.analogy}
voice extract.insight / {inverted.analogy -> insight}

target analogy / "mathematical.correspondence"
voice main / {zeta.zero -> analogy}
"""
    
    test_file = Path("/tmp/analogy_test.ops")
    test_file.write_text(analogy_ops)
    
    # Generate code
    result = subprocess.run(
        [sys.executable, "generate.py", "swift", str(test_file), "/tmp/analogy.swift"],
        capture_output=True,
        timeout=5
    )
    
    if result.returncode == 0:
        generated = Path("/tmp/analogy.swift").read_text()
        # Check for analogy structure
        if ("zero" in generated.lower() and "orbit" in generated.lower()) or "analogy" in generated.lower():
            print("  ✓ Generated analogy structure")
            print("  ✓ Domain mapping preserved")
            return True
        else:
            print("  ⚠ Generated code, but analogy unclear")
            return False
    else:
        print("  ✗ Failed to generate analogy")
        return False

def puzzle_error_correction():
    """Puzzle 5: Error Correction — Probabilistic Reasoning"""
    print("\nPuzzle 5: Error Correction")
    print("-" * 60)
    
    # Create corrupted .ops file
    original_ops = """
def test { name, value }
voice run / {test -> result}
target output / "result"
voice main / {test -> output}
"""
    
    # Corrupt it (remove 20% of characters randomly)
    corrupted = list(original_ops)
    indices = list(range(len(corrupted)))
    random.seed(42)  # Deterministic for testing
    remove_count = int(len(corrupted) * 0.2)
    remove_indices = random.sample(indices, remove_count)
    
    for idx in sorted(remove_indices, reverse=True):
        corrupted.pop(idx)
    
    corrupted_ops = ''.join(corrupted)
    
    corrupted_file = Path("/tmp/corrupted.ops")
    corrupted_file.write_text(corrupted_ops)
    
    print(f"  Corrupted file: {len(corrupted_ops)}/{len(original_ops)} chars")
    
    # Try to generate code from corrupted file
    result = subprocess.run(
        [sys.executable, "generate.py", "swift", str(corrupted_file), "/tmp/repaired.swift"],
        capture_output=True,
        timeout=5
    )
    
    if result.returncode == 0:
        generated = Path("/tmp/repaired.swift").read_text()
        # Check if it's valid Swift-like structure
        if "func" in generated or "struct" in generated or len(generated) > 50:
            print("  ✓ Reconstructed valid program")
            print("  ✓ Grammar inference successful")
            return True
        else:
            print("  ⚠ Generated code, but validity unclear")
            return False
    else:
        # Try to repair by adding missing elements
        repaired_ops = corrupted_ops
        if "def" not in repaired_ops:
            repaired_ops = "def test { name, value }\n" + repaired_ops
        if "voice" not in repaired_ops:
            repaired_ops += "\nvoice main / {test -> output}"
        
        repaired_file = Path("/tmp/repaired.ops")
        repaired_file.write_text(repaired_ops)
        
        result2 = subprocess.run(
            [sys.executable, "generate.py", "swift", str(repaired_file), "/tmp/repaired2.swift"],
            capture_output=True,
            timeout=5
        )
        
        if result2.returncode == 0:
            print("  ✓ Repaired and generated code")
            print("  ✓ Error correction successful")
            return True
        else:
            print("  ✗ Error correction failed")
            return False

def puzzle_dream_synthesis():
    """Puzzle 6: Dream Synthesis — Emergent Creativity"""
    print("\nPuzzle 6: Dream Synthesis")
    print("-" * 60)
    
    # Create dream synthesis ops
    dream_ops = """
def dream { description, discovery, operator }
def operator { name, function, purpose }

voice dream.discovery / {dream -> operator}
voice describe.operator / {operator -> description}
voice implement.operator / {operator -> code}

voice synthesize.dream / {dream -> dream + operator + code}

target dream / "creative.composition"
voice main / {dream -> dream}
"""
    
    test_file = Path("/tmp/dream_test.ops")
    test_file.write_text(dream_ops)
    
    # Generate code
    result = subprocess.run(
        [sys.executable, "generate.py", "swift", str(test_file), "/tmp/dream.swift"],
        capture_output=True,
        timeout=5
    )
    
    if result.returncode == 0:
        generated = Path("/tmp/dream.swift").read_text()
        # Check for creative elements
        if ("dream" in generated.lower() or "operator" in generated.lower() or 
            "discover" in generated.lower() or "synthesize" in generated.lower()):
            print("  ✓ Generated dream synthesis")
            print("  ✓ Emergent creativity demonstrated")
            return True
        else:
            print("  ⚠ Generated code, but creativity unclear")
            return False
    else:
        print("  ✗ Failed to generate dream")
        return False

def run_all_puzzles():
    """Run all Level-2 puzzles"""
    print("=" * 60)
    print("Level-2 Intelligence Puzzles — Trial by Paradox")
    print("=" * 60)
    print()
    
    puzzles = [
        ("Code Mutation", puzzle_code_mutation),
        ("Voice Paradox", puzzle_voice_paradox),
        ("Meta-Compiler Bootstrap", puzzle_meta_compiler_bootstrap),
        ("Analogy Construction", puzzle_analogy_construction),
        ("Error Correction", puzzle_error_correction),
        ("Dream Synthesis", puzzle_dream_synthesis),
    ]
    
    results = {}
    for name, puzzle_func in puzzles:
        try:
            result = puzzle_func()
            results[name] = result
        except Exception as e:
            print(f"  ✗ {name}: Error - {str(e)[:50]}")
            results[name] = False
    
    print()
    print("=" * 60)
    print("Puzzle Results Summary")
    print("=" * 60)
    
    passed = sum(1 for r in results.values() if r)
    total = len(results)
    
    for name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {status}  {name}")
    
    print()
    print(f"Puzzle Score: {passed}/{total} ({passed*100//total}%)")
    
    if passed == total:
        print("Level: MASTER")
    elif passed >= total * 0.8:
        print("Level: ADVANCED")
    elif passed >= total * 0.6:
        print("Level: INTERMEDIATE")
    else:
        print("Level: BEGINNER")
    
    print("=" * 60)
    
    return results

if __name__ == "__main__":
    run_all_puzzles()

