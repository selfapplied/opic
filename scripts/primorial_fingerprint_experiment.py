#!/usr/bin/env python3
"""
Primorial Fingerprint Persistence Experiment
Test: Do arithmetic holes in E(k) persist under flow evolution?
"""

import json
import math
from pathlib import Path
from typing import Dict, List, Tuple

def gcd(a: int, b: int) -> int:
    """Greatest common divisor"""
    while b:
        a, b = b, a % b
    return a

def primorial(n: int) -> int:
    """Compute primorial p# = product of first n primes"""
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
    result = 1
    for i in range(min(n, len(primes))):
        result *= primes[i]
    return result

def compute_mask_pattern(N: int, primorial_pmax: int = 5) -> Dict:
    """Compute primorial mask pattern"""
    p = primorial(primorial_pmax)
    
    # Simulate k-space: k ∈ [1, N/2]
    k_max = N // 2
    kept_modes = []
    filtered_modes = []
    
    for k in range(1, k_max + 1):
        if gcd(k, p) == 1:
            kept_modes.append(k)
        else:
            filtered_modes.append(k)
    
    kept_fraction = len(kept_modes) / k_max if k_max > 0 else 0
    
    return {
        "primorial": p,
        "primorial_pmax": primorial_pmax,
        "kept_modes": kept_modes[:50],  # First 50
        "filtered_modes": filtered_modes[:50],
        "kept_fraction": kept_fraction,
        "total_modes": k_max,
        "kept_count": len(kept_modes)
    }

def analyze_fingerprint_structure(pattern: Dict) -> Dict:
    """Analyze arithmetic structure in mask pattern"""
    kept = set(pattern["kept_modes"])
    filtered = set(pattern["filtered_modes"])
    
    # Find gaps (consecutive filtered modes)
    gaps = []
    prev_kept = 0
    for k in sorted(kept):
        gap_size = k - prev_kept - 1
        if gap_size > 0:
            gaps.append({"start": prev_kept + 1, "end": k - 1, "size": gap_size})
        prev_kept = k
    
    # Find clusters (consecutive kept modes)
    clusters = []
    cluster_start = None
    for k in sorted(kept):
        if cluster_start is None:
            cluster_start = k
        elif k not in kept or k - 1 not in kept:
            clusters.append({"start": cluster_start, "end": k - 1})
            cluster_start = k if k in kept else None
    
    return {
        "gaps": gaps[:10],  # First 10 gaps
        "clusters": clusters[:10],
        "structure": "Arithmetic sieve creates structured gaps and clusters"
    }

def main():
    print("=" * 60)
    print("Primorial Fingerprint Persistence Experiment")
    print("=" * 60)
    
    N = 64
    primorial_pmax = 5
    
    print(f"\n1. Computing primorial mask pattern...")
    pattern = compute_mask_pattern(N, primorial_pmax)
    print(f"   Primorial p#{primorial_pmax} = {pattern['primorial']}")
    print(f"   Kept modes: {pattern['kept_count']}/{pattern['total_modes']} ({pattern['kept_fraction']:.1%})")
    
    print(f"\n2. Analyzing arithmetic structure...")
    structure = analyze_fingerprint_structure(pattern)
    print(f"   Gaps: {len(structure['gaps'])} structured gaps")
    print(f"   Clusters: {len(structure['clusters'])} mode clusters")
    
    print(f"\n3. Fingerprint characteristics:")
    print(f"   - Reproducible: Yes (deterministic gcd)")
    print(f"   - Controllable: Yes (via primorial_pmax)")
    print(f"   - Measurable: Yes (in E(k) spectrum)")
    
    # Save results
    results = {
        "experiment": "fingerprint_persistence",
        "pattern": pattern,
        "structure": structure,
        "hypothesis": "Arithmetic holes in E(k) persist under flow evolution",
        "test": "Run A/B (mask off/on) from identical seeds, compare time-averaged E(k)"
    }
    
    output_path = Path('results/primorial_fingerprints.json')
    output_path.parent.mkdir(exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n✓ Results saved to {output_path}")
    print("\n" + "=" * 60)
    print("Next: Run flow simulation with mask off/on")
    print("Compare time-averaged E(k) to verify fingerprint persistence")
    print("=" * 60)

if __name__ == "__main__":
    main()

