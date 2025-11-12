#!/usr/bin/env python3
"""
Toy Decode: Parity/XOR-SAT
Encode parity on m bits → decode from observables
Compare: baseline, random mask, linearized flow
"""

import json
import random
import math
from pathlib import Path
from typing import Dict, List, Tuple
import statistics

def gcd(a: int, b: int) -> int:
    """Greatest common divisor"""
    while b:
        a, b = b, a % b
    return a

def primorial(n: int) -> int:
    """Compute primorial p#"""
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
    result = 1
    for i in range(min(n, len(primes))):
        result *= primes[i]
    return result

def encode_parity_problem(m_bits: int = 8, seed: int = 42) -> Dict:
    """Encode parity: map each bit to k-shell, parity = product sign"""
    random.seed(seed)
    
    # Generate random bits
    bits = [random.choice([0, 1]) for _ in range(m_bits)]
    parity = sum(bits) % 2
    
    # Map bits to k-shells (disjoint)
    k_shells = list(range(1, m_bits + 1))
    encoding = {i: {"bit": bits[i], "k_shell": k_shells[i]} for i in range(m_bits)}
    
    return {
        "m_bits": m_bits,
        "bits": bits,
        "parity": parity,
        "encoding": encoding,
        "k_shells": k_shells
    }

def simulate_observables(problem: Dict, mask_type: str, primorial_val: int, N: int = 64) -> Dict:
    """Simulate observables: E(k_s) on those shells + linear probes"""
    k_shells = problem["k_shells"]
    bits = problem["bits"]
    
    observables = {}
    
    # E(k_s) on assigned shells
    for i, k_shell in enumerate(k_shells):
        # Simulate spectrum value (in real version, from flow simulation)
        base_value = 0.1 + bits[i] * 0.05  # Bit encoded in amplitude
        
        # Apply mask
        if mask_type == "primorial":
            mask_val = 1.0 if gcd(k_shell, primorial_val) == 1 else 0.0
        elif mask_type == "random":
            # Matched-density random mask
            mask_val = random.choice([0.0, 1.0])  # Simplified
        else:  # baseline
            mask_val = 1.0
        
        observables[f"E_k_{k_shell}"] = base_value * mask_val
    
    # Linear probes (polynomial in m)
    n_probes = len(k_shells)  # Polynomial
    for i in range(n_probes):
        observables[f"probe_{i}"] = random.random() * 0.1
    
    return observables

def decode_logistic(observables: Dict, problem: Dict) -> Dict:
    """Decode using logistic regression (simplified)"""
    k_shells = problem["k_shells"]
    m_bits = problem["m_bits"]
    
    decoded_bits = []
    for i, k_shell in enumerate(k_shells):
        e_k = observables.get(f"E_k_{k_shell}", 0.0)
        # Simple threshold decoder
        decoded_bit = 1 if e_k > 0.12 else 0
        decoded_bits.append(decoded_bit)
    
    # Decode parity
    decoded_parity = sum(decoded_bits) % 2
    
    return {
        "decoded_bits": decoded_bits,
        "decoded_parity": decoded_parity,
        "true_bits": problem["bits"],
        "true_parity": problem["parity"]
    }

def compute_accuracy(decoded: Dict) -> Dict:
    """Compute balanced accuracy"""
    decoded_bits = decoded["decoded_bits"]
    true_bits = decoded["true_bits"]
    
    bit_correct = sum(1 for d, t in zip(decoded_bits, true_bits) if d == t)
    bit_accuracy = bit_correct / len(true_bits) if true_bits else 0.0
    
    parity_correct = 1 if decoded["decoded_parity"] == decoded["true_parity"] else 0
    parity_accuracy = float(parity_correct)
    
    return {
        "bit_accuracy": bit_accuracy,
        "parity_accuracy": parity_accuracy,
        "overall_accuracy": (bit_accuracy + parity_accuracy) / 2.0
    }

def run_toy_decode_experiment(m_bits: int = 8, n_runs: int = 20, primorial_val: int = 2310) -> Dict:
    """Run toy decode experiment with all baselines"""
    results = {
        "baseline": [],
        "primorial": [],
        "random_mask": [],
        "linearized": []
    }
    
    for run in range(n_runs):
        seed = 1000 + run
        problem = encode_parity_problem(m_bits=m_bits, seed=seed)
        
        # Baseline (mask off)
        obs_baseline = simulate_observables(problem, "baseline", primorial_val)
        decoded_baseline = decode_logistic(obs_baseline, problem)
        acc_baseline = compute_accuracy(decoded_baseline)
        results["baseline"].append(acc_baseline)
        
        # Primorial mask
        obs_primorial = simulate_observables(problem, "primorial", primorial_val)
        decoded_primorial = decode_logistic(obs_primorial, problem)
        acc_primorial = compute_accuracy(decoded_primorial)
        results["primorial"].append(acc_primorial)
        
        # Random mask (matched density)
        obs_random = simulate_observables(problem, "random", primorial_val)
        decoded_random = decode_logistic(obs_random, problem)
        acc_random = compute_accuracy(decoded_random)
        results["random_mask"].append(acc_random)
        
        # Linearized flow (simplified - no nonlinearity)
        obs_linear = simulate_observables(problem, "baseline", primorial_val)  # Simplified
        decoded_linear = decode_logistic(obs_linear, problem)
        acc_linear = compute_accuracy(decoded_linear)
        results["linearized"].append(acc_linear)
    
    # Aggregate results
    aggregated = {}
    for method, accs in results.items():
        if accs:
            aggregated[method] = {
                "mean_accuracy": statistics.mean([a["overall_accuracy"] for a in accs]),
                "mean_parity_accuracy": statistics.mean([a["parity_accuracy"] for a in accs]),
                "std_accuracy": statistics.stdev([a["overall_accuracy"] for a in accs]) if len(accs) > 1 else 0.0,
                "n_runs": len(accs)
            }
    
    # Test advantage
    primorial_mean = aggregated["primorial"]["mean_accuracy"]
    baseline_mean = aggregated["baseline"]["mean_accuracy"]
    random_mean = aggregated["random_mask"]["mean_accuracy"]
    linear_mean = aggregated["linearized"]["mean_accuracy"]
    
    advantage_over_baseline = primorial_mean - baseline_mean
    advantage_over_random = primorial_mean - random_mean
    advantage_over_linear = primorial_mean - linear_mean
    
    # Pass criteria: masked flow beats all baselines with CI
    # Simplified: check if mean is higher (in real version, use proper CI test)
    pass_criteria = (
        primorial_mean > baseline_mean and
        primorial_mean > random_mean and
        primorial_mean > linear_mean and
        aggregated["primorial"]["mean_parity_accuracy"] >= 0.9
    )
    
    return {
        "results": results,
        "aggregated": aggregated,
        "advantages": {
            "over_baseline": advantage_over_baseline,
            "over_random": advantage_over_random,
            "over_linear": advantage_over_linear
        },
        "pass": pass_criteria
    }

def main():
    print("=" * 60)
    print("Toy Decode: Parity/XOR-SAT")
    print("=" * 60)
    
    m_bits = 8
    n_runs = 20
    primorial_val = primorial(5)  # p#5 = 2310
    
    print(f"\nConfiguration:")
    print(f"  Bits: {m_bits}")
    print(f"  Runs: {n_runs}")
    print(f"  Primorial p#5 = {primorial_val}")
    
    print(f"\nRunning experiments...")
    experiment_results = run_toy_decode_experiment(m_bits=m_bits, n_runs=n_runs, primorial_val=primorial_val)
    
    print(f"\nResults:")
    for method, stats in experiment_results["aggregated"].items():
        print(f"  {method}:")
        print(f"    Mean accuracy: {stats['mean_accuracy']:.4f} ± {stats['std_accuracy']:.4f}")
        print(f"    Parity accuracy: {stats['mean_parity_accuracy']:.4f}")
    
    print(f"\nAdvantages:")
    adv = experiment_results["advantages"]
    print(f"  Over baseline: {adv['over_baseline']:+.4f}")
    print(f"  Over random: {adv['over_random']:+.4f}")
    print(f"  Over linear: {adv['over_linear']:+.4f}")
    
    print(f"\n{'✓ PASS' if experiment_results['pass'] else '✗ FAIL'}: Toy decode test")
    print(f"  Parity accuracy: {experiment_results['aggregated']['primorial']['mean_parity_accuracy']:.4f} (need ≥0.9)")
    
    # Save results
    output_path = Path('results/toy_decode_parity.json')
    output_path.parent.mkdir(exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(experiment_results, f, indent=2)
    
    print(f"\n✓ Results saved to {output_path}")

if __name__ == "__main__":
    main()

