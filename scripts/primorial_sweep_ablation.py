#!/usr/bin/env python3
"""
Primorial Sweep Ablation
Track: kept-mode fraction, fingerprint SNR, decoder accuracy
Expect U-shape: too sparse → underpowered; too dense → fingerprint washes out
"""

import json
import math
from pathlib import Path
from typing import Dict, List
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

def compute_kept_mode_fraction(N: int, primorial_val: int) -> float:
    """Compute fraction of modes kept by primorial mask"""
    k_max = N // 2
    kept = sum(1 for k in range(1, k_max + 1) if gcd(k, primorial_val) == 1)
    return kept / k_max if k_max > 0 else 0.0

def compute_fingerprint_snr(baseline_mean: float, masked_mean: float) -> float:
    """Compute signal-to-noise ratio"""
    if baseline_mean == 0:
        return 0.0
    return abs(masked_mean - baseline_mean) / baseline_mean

def simulate_decoder_accuracy(kept_fraction: float) -> float:
    """Simulate decoder accuracy (simplified - in real version, run actual decode)"""
    # U-shape: too sparse or too dense → lower accuracy
    # Optimal around 0.2-0.3
    optimal = 0.25
    distance = abs(kept_fraction - optimal)
    accuracy = max(0.5, 1.0 - distance * 2)  # Simplified model
    return accuracy

def run_primorial_sweep(N: int = 64, primorial_values: List[int] = None) -> Dict:
    """Run primorial sweep ablation"""
    if primorial_values is None:
        primorial_values = [primorial(4), primorial(5), primorial(6)]  # 210, 2310, 30030
    
    results = []
    
    # Baseline (no mask)
    baseline_mean = 0.1  # Simplified
    
    for p_val in primorial_values:
        kept_fraction = compute_kept_mode_fraction(N, p_val)
        
        # Simulate masked mean (simplified)
        masked_mean = baseline_mean * kept_fraction
        
        snr = compute_fingerprint_snr(baseline_mean, masked_mean)
        decoder_accuracy = simulate_decoder_accuracy(kept_fraction)
        
        results.append({
            "primorial": p_val,
            "kept_fraction": kept_fraction,
            "snr": snr,
            "decoder_accuracy": decoder_accuracy
        })
    
    return {
        "N": N,
        "primorial_values": primorial_values,
        "results": results
    }

def main():
    print("=" * 60)
    print("Primorial Sweep Ablation")
    print("=" * 60)
    
    N = 64
    primorial_values = [primorial(4), primorial(5), primorial(6)]
    
    print(f"\nConfiguration:")
    print(f"  N = {N}")
    print(f"  Primorials: {primorial_values}")
    
    sweep_results = run_primorial_sweep(N, primorial_values)
    
    print(f"\nResults:")
    print(f"{'Primorial':<12} {'Kept %':<10} {'SNR':<10} {'Accuracy':<10}")
    print("-" * 50)
    for r in sweep_results["results"]:
        print(f"{r['primorial']:<12} {r['kept_fraction']:<10.1%} {r['snr']:<10.6f} {r['decoder_accuracy']:<10.4f}")
    
    # Check for U-shape
    accuracies = [r["decoder_accuracy"] for r in sweep_results["results"]]
    middle_idx = len(accuracies) // 2
    u_shape = accuracies[middle_idx] > accuracies[0] and accuracies[middle_idx] > accuracies[-1]
    
    print(f"\nU-shape detected: {u_shape}")
    print(f"  (Optimal in middle: {accuracies[middle_idx]:.4f} > {accuracies[0]:.4f} and {accuracies[-1]:.4f})")
    
    # Save results
    output_path = Path('results/primorial_sweep_ablation.json')
    output_path.parent.mkdir(exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(sweep_results, f, indent=2)
    
    print(f"\n✓ Results saved to {output_path}")

if __name__ == "__main__":
    main()

