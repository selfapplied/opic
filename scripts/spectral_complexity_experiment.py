#!/usr/bin/env python3
"""
Spectral Toy + Complexity Toy: Side-by-Side Experiment
Compare RH-style spectral structure vs P vs NP computational structure
"""

import json
import math
import random
from pathlib import Path
from typing import Dict, List, Tuple
from collections import Counter

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

# ============================================================================
# Spectral Toy: Zeta-like Operator
# ============================================================================

def compute_zeta_like_spectrum(s_values: List[complex], multiplicative_func) -> Dict:
    """Compute zeta-like spectrum from multiplicative function"""
    spectrum = []
    for s in s_values:
        # Simplified: zeta-like from Euler product structure
        # Real implementation would compute proper transform
        value = multiplicative_func(s)
        spectrum.append({"s": s, "value": value, "magnitude": abs(value)})
    
    return {"spectrum": spectrum}

def find_zeros_on_critical_line(spectrum: List[Dict], threshold: float = 1e-6) -> List[float]:
    """Find zeros where Re(s) = 1/2"""
    zeros = []
    for i in range(len(spectrum) - 1):
        val1 = spectrum[i]["magnitude"]
        val2 = spectrum[i+1]["magnitude"]
        # Simple zero crossing detection
        if val1 < threshold and val2 > threshold:
            zeros.append(0.5 + 1j * (i + 0.5))  # On critical line
    return zeros

def compute_spacing_variance(zeros: List[complex]) -> float:
    """Compute spacing variance Δt of zeros"""
    if len(zeros) < 2:
        return 0.0
    
    spacings = []
    sorted_zeros = sorted(zeros, key=lambda z: z.imag)
    for i in range(len(sorted_zeros) - 1):
        spacing = sorted_zeros[i+1].imag - sorted_zeros[i].imag
        spacings.append(spacing)
    
    if not spacings:
        return 0.0
    
    mean_spacing = sum(spacings) / len(spacings)
    variance = sum((s - mean_spacing)**2 for s in spacings) / len(spacings)
    return variance

def compute_entropy_from_distribution(values: List[float]) -> float:
    """Compute entropy H = -Σ p(log p)"""
    if not values:
        return 0.0
    
    # Normalize to probabilities
    total = sum(abs(v) for v in values)
    if total == 0:
        return 0.0
    
    probs = [abs(v) / total for v in values]
    entropy = -sum(p * math.log(p + 1e-10) for p in probs if p > 0)
    return entropy

# ============================================================================
# Complexity Toy: 3-SAT Search
# ============================================================================

def generate_small_3sat(n_vars: int, n_clauses: int) -> Dict:
    """Generate small 3-SAT instance"""
    clauses = []
    for _ in range(n_clauses):
        clause = []
        for _ in range(3):
            var = random.randint(1, n_vars)
            negated = random.choice([True, False])
            clause.append({"var": var, "negated": negated})
        clauses.append(clause)
    
    return {
        "n_vars": n_vars,
        "n_clauses": n_clauses,
        "clauses": clauses
    }

def check_satisfaction(assignment: List[int], clauses: List[List[Dict]]) -> bool:
    """Check if assignment satisfies all clauses"""
    for clause in clauses:
        clause_satisfied = False
        for lit in clause:
            var_val = assignment[lit["var"] - 1]
            if lit["negated"]:
                var_val = 1 - var_val
            if var_val == 1:
                clause_satisfied = True
                break
        if not clause_satisfied:
            return False
    return True

def search_3sat(sat_instance: Dict, max_tries: int = 1000) -> Dict:
    """Search for satisfying assignment"""
    n_vars = sat_instance["n_vars"]
    clauses = sat_instance["clauses"]
    
    search_steps = []
    for attempt in range(max_tries):
        assignment = [random.choice([0, 1]) for _ in range(n_vars)]
        satisfied = check_satisfaction(assignment, clauses)
        search_steps.append({"attempt": attempt, "assignment": assignment, "satisfied": satisfied})
        if satisfied:
            return {
                "found": True,
                "assignment": assignment,
                "steps": attempt + 1,
                "search_steps": search_steps
            }
    
    return {
        "found": False,
        "steps": max_tries,
        "search_steps": search_steps
    }

def compute_search_entropy(search_steps: List[Dict]) -> float:
    """Compute entropy of search process"""
    # Entropy from assignment distribution
    assignments = [tuple(s["assignment"]) for s in search_steps]
    counts = Counter(assignments)
    probs = [count / len(assignments) for count in counts.values()]
    entropy = -sum(p * math.log(p + 1e-10) for p in probs if p > 0)
    return entropy

def compute_verification_cost(assignment: List[int], clauses: List[List[Dict]]) -> int:
    """Polynomial-time verification: check all clauses"""
    return len(clauses)  # O(m) where m = number of clauses

# ============================================================================
# Compare Metrics
# ============================================================================

def compare_metrics(spectral_results: Dict, complexity_results: Dict) -> Dict:
    """Compare RH zeros spacing vs P vs NP search times"""
    
    # RH side: spacing variance of zeros
    spacing_variance = spectral_results.get("spacing_variance", 0.0)
    
    # P vs NP side: distribution of search times
    search_times = [r["steps"] for r in complexity_results.get("runs", [])]
    search_time_variance = sum((t - sum(search_times)/len(search_times))**2 for t in search_times) / len(search_times) if search_times else 0.0
    
    # Correlation question: smoother spectra ↔ easier verification?
    spectral_smoothness = 1.0 / (spacing_variance + 1e-10)  # Inverse variance
    verification_ease = 1.0 / (search_time_variance + 1e-10)
    
    return {
        "spacing_variance": spacing_variance,
        "search_time_variance": search_time_variance,
        "spectral_smoothness": spectral_smoothness,
        "verification_ease": verification_ease,
        "correlation_question": "Do smoother spectra correlate with easier verification?",
        "note": "Pure analogy, not proof"
    }

def main():
    print("=" * 60)
    print("Spectral Toy + Complexity Toy: Side-by-Side Experiment")
    print("=" * 60)
    
    # Spectral Toy
    print("\n1. Spectral Toy: Zeta-like Operator")
    print("   Computing spectrum...")
    
    # Simplified spectrum (toy)
    s_values = [0.5 + 1j * t for t in range(1, 21)]
    def multiplicative_func(s):
        # Toy: simple multiplicative structure
        return 1.0 / (s - 1.0) if abs(s - 1.0) > 0.1 else 1.0
    
    spectrum_result = compute_zeta_like_spectrum(s_values, multiplicative_func)
    zeros = find_zeros_on_critical_line(spectrum_result["spectrum"])
    spacing_variance = compute_spacing_variance(zeros)
    
    # Compute entropy from spectrum
    magnitudes = [s["magnitude"] for s in spectrum_result["spectrum"]]
    spectral_entropy = compute_entropy_from_distribution(magnitudes)
    
    print(f"   Zeros found: {len(zeros)}")
    print(f"   Spacing variance: {spacing_variance:.6f}")
    print(f"   Spectral entropy: {spectral_entropy:.6f}")
    
    # Complexity Toy
    print("\n2. Complexity Toy: 3-SAT Search")
    print("   Running small 3-SAT searches...")
    
    n_vars = 10
    n_clauses = 20
    runs = []
    
    for seed in range(5):
        random.seed(seed)
        sat_instance = generate_small_3sat(n_vars, n_clauses)
        result = search_3sat(sat_instance, max_tries=100)
        
        if result["found"]:
            search_entropy = compute_search_entropy(result["search_steps"])
            verification_cost = compute_verification_cost(result["assignment"], sat_instance["clauses"])
            runs.append({
                "found": True,
                "steps": result["steps"],
                "search_entropy": search_entropy,
                "verification_cost": verification_cost
            })
        else:
            runs.append({
                "found": False,
                "steps": result["steps"],
                "search_entropy": 0.0,
                "verification_cost": 0
            })
    
    found_count = sum(1 for r in runs if r["found"])
    avg_steps = sum(r["steps"] for r in runs) / len(runs) if runs else 0
    avg_entropy = sum(r["search_entropy"] for r in runs) / len(runs) if runs else 0
    
    print(f"   Found: {found_count}/{len(runs)}")
    print(f"   Avg steps: {avg_steps:.1f}")
    print(f"   Avg search entropy: {avg_entropy:.6f}")
    
    # Compare Metrics
    print("\n3. Compare Metrics")
    spectral_results = {
        "spacing_variance": spacing_variance,
        "spectral_entropy": spectral_entropy
    }
    complexity_results = {"runs": runs}
    
    comparison = compare_metrics(spectral_results, complexity_results)
    print(f"   RH spacing variance: {comparison['spacing_variance']:.6f}")
    print(f"   Search time variance: {comparison['search_time_variance']:.6f}")
    print(f"   Spectral smoothness: {comparison['spectral_smoothness']:.6f}")
    print(f"   Verification ease: {comparison['verification_ease']:.6f}")
    print(f"   Question: {comparison['correlation_question']}")
    
    # Save results
    results = {
        "spectral_toy": {
            "zeros_count": len(zeros),
            "spacing_variance": spacing_variance,
            "spectral_entropy": spectral_entropy
        },
        "complexity_toy": {
            "n_vars": n_vars,
            "n_clauses": n_clauses,
            "runs": runs,
            "found_count": found_count,
            "avg_steps": avg_steps,
            "avg_search_entropy": avg_entropy
        },
        "comparison": comparison
    }
    
    output_path = Path('results/spectral_complexity_experiment.json')
    output_path.parent.mkdir(exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n✓ Results saved to {output_path}")
    print("\n" + "=" * 60)
    print("Key Insight:")
    print("RH field: linear, unitary, symmetric → smooth spectra")
    print("NP field: nonlinear, dissipative, search → computational resistance")
    print("Watch where symmetry breaks → measure 'computational curvature'")
    print("=" * 60)

if __name__ == "__main__":
    main()

