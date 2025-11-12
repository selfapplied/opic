#!/usr/bin/env python3
"""
Toy Decode Experiment: Parity/XOR-SAT
Test: Can supervised decoder recover truth table from observables?
"""

import json
import random
from pathlib import Path
from typing import Dict, List

def encode_parity_problem(n_bits: int = 4) -> Dict:
    """Encode parity problem: sum of bits mod 2 = 0"""
    # Generate random truth table
    truth_table = {}
    for i in range(2**n_bits):
        bits = [int(b) for b in format(i, f'0{n_bits}b')]
        parity = sum(bits) % 2
        truth_table[i] = {"bits": bits, "parity": parity}
    
    return {
        "problem": "parity",
        "n_bits": n_bits,
        "truth_table": truth_table,
        "encoding": "Map each bit to k-shell, parity to field amplitude"
    }

def encode_xor_sat_small(n_vars: int = 3) -> Dict:
    """Encode small XOR-SAT: x₁ ⊕ x₂ ⊕ x₃ = 1"""
    clauses = [{"vars": [1, 2, 3], "rhs": 1}]
    
    # Generate satisfying assignments
    satisfying = []
    for i in range(2**n_vars):
        bits = [int(b) for b in format(i, f'0{n_vars}b')]
        xor_result = bits[0] ^ bits[1] ^ bits[2]
        if xor_result == 1:
            satisfying.append({"assignment": bits, "satisfies": True})
        else:
            satisfying.append({"assignment": bits, "satisfies": False})
    
    return {
        "problem": "xor_sat",
        "n_vars": n_vars,
        "clauses": clauses,
        "satisfying": satisfying,
        "encoding": "Map variables to k-shells, clauses to field interactions"
    }

def simulate_observables(encoded_problem: Dict, noise_level: float = 0.1) -> Dict:
    """Simulate observables from field evolution (toy)"""
    # In real experiment, this would come from flow simulation
    # For now, simulate with noise
    
    observables = {
        "E_k": [random.random() for _ in range(20)],  # Simulated spectrum
        "moments": [random.random() for _ in range(5)],  # Low-order moments
        "probes": [random.random() for _ in range(10)]  # Linear probes
    }
    
    return observables

def decode_toy(observables: Dict, problem_type: str) -> Dict:
    """Attempt to decode problem from observables"""
    # Simple decoder: pattern matching on observables
    # In real experiment, use supervised learning
    
    # For now, return random guess (baseline)
    if problem_type == "parity":
        guess = random.choice([0, 1])
    else:
        guess = [random.choice([0, 1]) for _ in range(3)]
    
    return {
        "decoded": guess,
        "confidence": random.random(),
        "method": "baseline_random"
    }

def main():
    print("=" * 60)
    print("Toy Decode Experiment: Parity/XOR-SAT")
    print("=" * 60)
    
    # Test 1: Parity problem
    print("\n1. Encoding parity problem...")
    parity_problem = encode_parity_problem(n_bits=4)
    print(f"   Problem: 4-bit parity")
    print(f"   Truth table size: {len(parity_problem['truth_table'])}")
    
    # Test 2: XOR-SAT
    print("\n2. Encoding XOR-SAT problem...")
    xor_problem = encode_xor_sat_small(n_vars=3)
    satisfying_count = sum(1 for s in xor_problem['satisfying'] if s['satisfies'])
    print(f"   Problem: x₁ ⊕ x₂ ⊕ x₃ = 1")
    print(f"   Satisfying assignments: {satisfying_count}/{len(xor_problem['satisfying'])}")
    
    # Simulate observables
    print("\n3. Simulating observables...")
    parity_obs = simulate_observables(parity_problem)
    xor_obs = simulate_observables(xor_problem)
    print(f"   E(k) samples: {len(parity_obs['E_k'])}")
    print(f"   Moments: {len(parity_obs['moments'])}")
    print(f"   Probes: {len(parity_obs['probes'])}")
    
    # Attempt decode
    print("\n4. Attempting decode (baseline)...")
    parity_decode = decode_toy(parity_obs, "parity")
    xor_decode = decode_toy(xor_obs, "xor_sat")
    print(f"   Parity decode: {parity_decode['decoded']} (confidence: {parity_decode['confidence']:.2f})")
    print(f"   XOR-SAT decode: {xor_decode['decoded']} (confidence: {xor_decode['confidence']:.2f})")
    
    # Save results
    results = {
        "experiment": "toy_decode",
        "parity_problem": parity_problem,
        "xor_problem": xor_problem,
        "parity_observables": parity_obs,
        "xor_observables": xor_obs,
        "parity_decode": parity_decode,
        "xor_decode": xor_decode,
        "note": "Baseline random decoder - need supervised learning for real test"
    }
    
    output_path = Path('results/toy_decode_results.json')
    output_path.parent.mkdir(exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n✓ Results saved to {output_path}")
    print("\n" + "=" * 60)
    print("Next: Implement supervised decoder")
    print("Compare to baselines: random, linear filter, heat equation")
    print("=" * 60)

if __name__ == "__main__":
    main()

