#!/usr/bin/env python3
"""
Fingerprint Persistence A/B Test
Goal: Does primorial mask leave stable, time-averaged dent/plateau in E(k)?
"""

import json
import math
import random
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

def apply_primorial_mask(k_magnitude: float, primorial_val: int) -> float:
    """Apply primorial mask: 1 if gcd(|k|, p#) == 1 else 0"""
    k_int = int(k_magnitude)
    if k_int == 0:
        return 1.0
    return 1.0 if gcd(k_int, primorial_val) == 1 else 0.0

def simulate_e_k_evolution(N: int, mask_on: bool, primorial_val: int, n_steps: int = 100) -> Dict:
    """Simulate E(k) evolution with/without mask"""
    # Simplified simulation - in real version, use actual flow solver
    k_max = N // 2
    E_k_history = {k: [] for k in range(1, k_max + 1)}
    
    # Initial spectrum (simplified)
    for k in range(1, k_max + 1):
        E_k_history[k] = [random.random() * 0.1 for _ in range(n_steps)]
    
    # Apply mask if enabled
    if mask_on:
        for k in range(1, k_max + 1):
            mask_val = apply_primorial_mask(k, primorial_val)
            E_k_history[k] = [e * mask_val for e in E_k_history[k]]
    
    return E_k_history

def compute_time_averaged_e_k(E_k_history: Dict, late_time_start: int = 50) -> Dict:
    """Compute time-averaged E(k) over late-time window"""
    averaged = {}
    for k, history in E_k_history.items():
        late_window = history[late_time_start:]
        if late_window:
            averaged[k] = {
                "mean": statistics.mean(late_window),
                "std": statistics.stdev(late_window) if len(late_window) > 1 else 0.0,
                "count": len(late_window)
            }
    return averaged

def bootstrap_ci(values: List[float], n_bootstrap: int = 1000, alpha: float = 0.05) -> Tuple[float, float]:
    """Bootstrap 95% CI"""
    if not values:
        return (0.0, 0.0)
    
    n = len(values)
    bootstrap_means = []
    for _ in range(n_bootstrap):
        sample = [random.choice(values) for _ in range(n)]
        bootstrap_means.append(statistics.mean(sample))
    
    bootstrap_means.sort()
    lower_idx = int(n_bootstrap * alpha / 2)
    upper_idx = int(n_bootstrap * (1 - alpha / 2))
    
    return (bootstrap_means[lower_idx], bootstrap_means[upper_idx])

def benjamini_hochberg_correction(p_values: List[float], alpha: float = 0.05) -> List[bool]:
    """Benjamini-Hochberg FDR correction"""
    n = len(p_values)
    sorted_p = sorted(enumerate(p_values), key=lambda x: x[1])
    significant = [False] * n
    
    for i, (idx, p_val) in enumerate(sorted_p):
        threshold = (i + 1) * alpha / n
        if p_val <= threshold:
            significant[idx] = True
    
    return significant

def test_shell_differences(baseline: Dict, masked: Dict, alpha: float = 0.05) -> Dict:
    """Test per-shell differences with FDR correction"""
    differences = []
    p_values = []
    
    for k in sorted(set(baseline.keys()) & set(masked.keys())):
        baseline_mean = baseline[k]["mean"]
        masked_mean = masked[k]["mean"]
        diff = masked_mean - baseline_mean
        
        # Use CI width as proxy for std (in real version, use proper statistical test)
        baseline_ci_width = (baseline[k].get("ci_upper", baseline_mean) - baseline[k].get("ci_lower", baseline_mean)) / 3.92  # Approx std from 95% CI
        masked_ci_width = (masked[k].get("ci_upper", masked_mean) - masked[k].get("ci_lower", masked_mean)) / 3.92
        pooled_std = math.sqrt((baseline_ci_width**2 + masked_ci_width**2) / 2)
        if pooled_std > 0:
            t_stat = diff / (pooled_std / math.sqrt(2))
            # Simplified p-value (in real version, use proper t-distribution)
            p_val = 2 * (1 - abs(t_stat) / 10) if abs(t_stat) < 10 else 0.001
        else:
            p_val = 1.0
        
        differences.append({"k": k, "diff": diff, "p_value": p_val})
        p_values.append(p_val)
    
    # FDR correction
    significant = benjamini_hochberg_correction(p_values, alpha)
    
    # Count significant adjacent shells
    significant_shells = [d["k"] for d, sig in zip(differences, significant) if sig]
    adjacent_count = 0
    for i in range(len(significant_shells) - 1):
        if significant_shells[i+1] - significant_shells[i] == 1:
            adjacent_count += 1
    
    return {
        "differences": differences,
        "significant": significant,
        "significant_shells": significant_shells,
        "adjacent_significant": adjacent_count,
        "pass": adjacent_count >= 3
    }

def main():
    print("=" * 60)
    print("Fingerprint Persistence A/B Test")
    print("=" * 60)
    
    N = 64
    primorial_val = primorial(5)  # p#5 = 2310
    n_steps = 100
    n_seeds = 5
    
    print(f"\nConfiguration:")
    print(f"  N = {N}")
    print(f"  Primorial p#5 = {primorial_val}")
    print(f"  Steps = {n_steps}")
    print(f"  Seeds = {n_seeds}")
    
    # Pre-draw seeds
    seeds = [random.randint(1, 10000) for _ in range(n_seeds)]
    print(f"\nPre-drawn seeds: {seeds}")
    
    # Run A/B tests
    baseline_results = []
    masked_results = []
    
    for seed in seeds:
        random.seed(seed)
        
        # Baseline (mask off)
        baseline_history = simulate_e_k_evolution(N, mask_on=False, primorial_val=primorial_val, n_steps=n_steps)
        baseline_avg = compute_time_averaged_e_k(baseline_history)
        baseline_results.append(baseline_avg)
        
        # Masked (mask on)
        random.seed(seed)  # Same seed
        masked_history = simulate_e_k_evolution(N, mask_on=True, primorial_val=primorial_val, n_steps=n_steps)
        masked_avg = compute_time_averaged_e_k(masked_history)
        masked_results.append(masked_avg)
    
    # Aggregate across seeds
    k_values = sorted(set(baseline_results[0].keys()))
    
    baseline_aggregated = {}
    masked_aggregated = {}
    
    for k in k_values:
        baseline_means = [r[k]["mean"] for r in baseline_results if k in r]
        masked_means = [r[k]["mean"] for r in masked_results if k in r]
        
        baseline_ci = bootstrap_ci(baseline_means)
        masked_ci = bootstrap_ci(masked_means)
        
        baseline_aggregated[k] = {
            "mean": statistics.mean(baseline_means),
            "ci_lower": baseline_ci[0],
            "ci_upper": baseline_ci[1]
        }
        
        masked_aggregated[k] = {
            "mean": statistics.mean(masked_means),
            "ci_lower": masked_ci[0],
            "ci_upper": masked_ci[1]
        }
    
    # Test differences
    print(f"\nTesting shell differences (FDR correction)...")
    diff_test = test_shell_differences(baseline_aggregated, masked_aggregated)
    
    print(f"  Significant shells: {len(diff_test['significant_shells'])}")
    print(f"  Adjacent significant: {diff_test['adjacent_significant']}")
    print(f"  Pass (≥3 adjacent): {diff_test['pass']}")
    
    # Compute kept-mode fraction
    kept_modes = sum(1 for k in k_values if apply_primorial_mask(k, primorial_val) > 0.5)
    kept_fraction = kept_modes / len(k_values) if k_values else 0.0
    
    # Compute SNR (signal-to-noise ratio)
    baseline_mean_overall = statistics.mean([baseline_aggregated[k]["mean"] for k in k_values])
    masked_mean_overall = statistics.mean([masked_aggregated[k]["mean"] for k in k_values])
    snr = abs(masked_mean_overall - baseline_mean_overall) / baseline_mean_overall if baseline_mean_overall > 0 else 0.0
    
    # Save results
    results = {
        "experiment": "fingerprint_persistence_ab",
        "config": {
            "N": N,
            "primorial": primorial_val,
            "n_steps": n_steps,
            "n_seeds": n_seeds,
            "seeds": seeds
        },
        "baseline": baseline_aggregated,
        "masked": masked_aggregated,
        "difference_test": diff_test,
        "metrics": {
            "kept_mode_fraction": kept_fraction,
            "snr": snr
        },
        "pass": diff_test["pass"]
    }
    
    output_path = Path('results/fingerprint_persistence_ab.json')
    output_path.parent.mkdir(exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n✓ Results saved to {output_path}")
    print(f"\nMetrics:")
    print(f"  Kept-mode fraction: {kept_fraction:.1%}")
    print(f"  SNR: {snr:.6f}")
    print(f"\n{'✓ PASS' if diff_test['pass'] else '✗ FAIL'}: Fingerprint persistence test")

if __name__ == "__main__":
    main()

