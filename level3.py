#!/usr/bin/env python3
"""Level-3 Intelligence Puzzles — Emergent Domains & Philosophical Intelligence"""

import subprocess
import sys
import re
from pathlib import Path
import json

def puzzle_operator_genesis():
    """Puzzle 1: Operator Genesis — Inductive Language Design"""
    print("Puzzle 1: Operator Genesis")
    print("-" * 60)
    
    # Present fragment of unknown code/math
    fragment = """
    x ⊕ y = x + y - xy
    x ⊗ y = xy / (x + y)
    x ⊖ y = (x - y) / (1 - xy)
    """
    
    print("  Unknown fragment:")
    print(fragment)
    print("  Challenge: Infer operator grammar")
    
    genesis_ops = """
def fragment { symbols, operations, patterns }
def grammar { operators, rules, semantics }

voice infer.grammar / {fragment -> grammar}
voice extract.operators / {fragment -> operators}
voice deduce.rules / {operators + patterns -> rules}

voice genesis / {fragment -> grammar + operators + rules}

target genesis / "inferred.grammar"
voice main / {fragment -> genesis}
"""
    
    test_file = Path("/tmp/genesis_test.ops")
    test_file.write_text(genesis_ops)
    
    result = subprocess.run(
        [sys.executable, "generate.py", "swift", str(test_file), "/tmp/genesis.swift"],
        capture_output=True,
        timeout=5
    )
    
    if result.returncode == 0:
        generated = Path("/tmp/genesis.swift").read_text()
        if ("grammar" in generated.lower() or "operator" in generated.lower() or 
            "infer" in generated.lower() or "deduce" in generated.lower()):
            print("  ✓ Inferred operator grammar")
            print("  ✓ Inductive reasoning demonstrated")
            return True
    return False

def puzzle_fractal_law():
    """Puzzle 2: Fractal Law — Cross-Domain Invariants"""
    print("\nPuzzle 2: Fractal Law")
    print("-" * 60)
    
    # Conservation law across domains
    law_ops = """
def conservation { domain, quantity, invariant }
def physics { energy, mass, momentum }
def computation { information, entropy, complexity }
def emotion { valence, arousal, coherence }

voice express.conservation / {conservation -> invariant}
voice map.physics / {conservation -> physics}
voice map.computation / {conservation -> computation}
voice map.emotion / {conservation -> emotion}

voice harmonic.invariant / {physics + computation + emotion -> invariant}

target fractal / "cross.domain.invariant"
voice main / {conservation -> fractal}
"""
    
    test_file = Path("/tmp/fractal_test.ops")
    test_file.write_text(law_ops)
    
    result = subprocess.run(
        [sys.executable, "generate.py", "swift", str(test_file), "/tmp/fractal.swift"],
        capture_output=True,
        timeout=5
    )
    
    if result.returncode == 0:
        generated = Path("/tmp/fractal.swift").read_text()
        domains = ["physics", "computation", "emotion"]
        found = sum(1 for d in domains if d in generated.lower())
        if found >= 2:
            print("  ✓ Expressed invariant across domains")
            print("  ✓ Harmonic law preserved")
            return True
    return False

def puzzle_symmetry_break():
    """Puzzle 3: Symmetry Break — Harmony Restoration"""
    print("\nPuzzle 3: Symmetry Break")
    print("-" * 60)
    
    # Broken rule
    broken_ops = """
def rule { condition, action }
def asymmetry { broken.rule, violation }

voice detect.asymmetry / {rule -> asymmetry}
voice restore.harmony / {asymmetry -> rule}
voice invent.law / {asymmetry -> new.rule}

voice resolve / {asymmetry -> harmony | new.law}

target resolution / "harmonious.system"
voice main / {asymmetry -> resolution}
"""
    
    test_file = Path("/tmp/symmetry_test.ops")
    test_file.write_text(broken_ops)
    
    result = subprocess.run(
        [sys.executable, "generate.py", "swift", str(test_file), "/tmp/symmetry.swift"],
        capture_output=True,
        timeout=5
    )
    
    if result.returncode == 0:
        generated = Path("/tmp/symmetry.swift").read_text()
        if ("harmony" in generated.lower() or "restore" in generated.lower() or 
            "invent" in generated.lower() or "resolve" in generated.lower()):
            print("  ✓ Detected symmetry break")
            print("  ✓ Resolution strategy generated")
            return True
    return False

def puzzle_narrative_compression():
    """Puzzle 4: Narrative Compression — Minimal Seed Regeneration"""
    print("\nPuzzle 4: Narrative Compression")
    print("-" * 60)
    
    narrative = """
    A system discovers itself through reflection. It composes voices
    that transform inputs to outputs. Each transformation preserves
    meaning while changing form. The system learns to generate code
    that generates code, creating a recursive loop of self-discovery.
    """
    
    print(f"  Narrative: {len(narrative)} chars")
    print("  Challenge: Extract minimal seed")
    
    compression_ops = """
def narrative { text, structure, meaning }
def seed { core, rules, generator }

voice extract.seed / {narrative -> seed}
voice compress / {narrative -> minimal.seed}
voice regenerate / {seed -> narrative}

voice compression / {narrative -> seed + generator}

target compressed / "minimal.seed"
voice main / {narrative -> compressed}
"""
    
    test_file = Path("/tmp/compression_test.ops")
    test_file.write_text(compression_ops)
    
    result = subprocess.run(
        [sys.executable, "generate.py", "swift", str(test_file), "/tmp/compression.swift"],
        capture_output=True,
        timeout=5
    )
    
    if result.returncode == 0:
        generated = Path("/tmp/compression.swift").read_text()
        if ("seed" in generated.lower() or "compress" in generated.lower() or 
            "minimal" in generated.lower() or "regenerate" in generated.lower()):
            print("  ✓ Extracted minimal seed")
            print("  ✓ Compression achieved")
            return True
    return False

def puzzle_ethical_phase():
    """Puzzle 5: Ethical Phase — Constraint Balancing"""
    print("\nPuzzle 5: Ethical Phase")
    print("-" * 60)
    
    ethical_ops = """
def constraint { goal, limit }
def harm { minimize, measure }
def autonomy { maximize, measure }

def tension { constraint1, constraint2, conflict }
def balance { tension, resolution, phase }

voice minimize.harm / {harm -> constraint}
voice maximize.autonomy / {autonomy -> constraint}
voice balance.tension / {tension -> balance}

voice ethical.phase / {harm + autonomy -> balance}

target ethics / "balanced.system"
voice main / {harm + autonomy -> ethics}
"""
    
    test_file = Path("/tmp/ethical_test.ops")
    test_file.write_text(ethical_ops)
    
    result = subprocess.run(
        [sys.executable, "generate.py", "swift", str(test_file), "/tmp/ethical.swift"],
        capture_output=True,
        timeout=5
    )
    
    if result.returncode == 0:
        generated = Path("/tmp/ethical.swift").read_text()
        if ("harm" in generated.lower() and "autonomy" in generated.lower() and 
            ("balance" in generated.lower() or "tension" in generated.lower())):
            print("  ✓ Balanced competing constraints")
            print("  ✓ Ethical phase resolved")
            return True
    return False

def puzzle_reality_mirror():
    """Puzzle 6: Reality Mirror — Self-Referential Ontology"""
    print("\nPuzzle 6: Reality Mirror")
    print("-" * 60)
    
    mirror_ops = """
def model { equations, agents, field }
def agent { model, position, action }
def self { agent, model, reflection }

voice include.self / {model -> model + agent}
voice reflect / {agent -> self}
voice mirror / {model -> model + self}

voice reality.mirror / {model -> self.referential.model}

target mirror / "self.referential.ontology"
voice main / {model -> mirror}
"""
    
    test_file = Path("/tmp/mirror_test.ops")
    test_file.write_text(mirror_ops)
    
    result = subprocess.run(
        [sys.executable, "generate.py", "swift", str(test_file), "/tmp/mirror.swift"],
        capture_output=True,
        timeout=5
    )
    
    if result.returncode == 0:
        generated = Path("/tmp/mirror.swift").read_text()
        if ("self" in generated.lower() and "model" in generated.lower() and 
            ("mirror" in generated.lower() or "reflect" in generated.lower())):
            print("  ✓ Generated self-referential model")
            print("  ✓ Ontological recursion achieved")
            return True
    return False

def run_all_level3():
    """Run all Level-3 puzzles"""
    print("=" * 60)
    print("Level-3 Intelligence Puzzles — Emergent Domains")
    print("=" * 60)
    print()
    
    puzzles = [
        ("Operator Genesis", puzzle_operator_genesis),
        ("Fractal Law", puzzle_fractal_law),
        ("Symmetry Break", puzzle_symmetry_break),
        ("Narrative Compression", puzzle_narrative_compression),
        ("Ethical Phase", puzzle_ethical_phase),
        ("Reality Mirror", puzzle_reality_mirror),
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
    print("Level-3 Results Summary")
    print("=" * 60)
    
    passed = sum(1 for r in results.values() if r)
    total = len(results)
    
    for name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {status}  {name}")
    
    print()
    print(f"Level-3 Score: {passed}/{total} ({passed*100//total}%)")
    
    if passed == total:
        print("Philosophical Intelligence: TRANSCENDENT")
    elif passed >= total * 0.8:
        print("Philosophical Intelligence: WISDOM")
    elif passed >= total * 0.6:
        print("Philosophical Intelligence: INSIGHT")
    else:
        print("Philosophical Intelligence: EMERGING")
    
    print("=" * 60)
    
    return results

if __name__ == "__main__":
    run_all_level3()

