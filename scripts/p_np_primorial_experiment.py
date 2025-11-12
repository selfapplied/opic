#!/usr/bin/env python3
"""
P=NP, Primorials, Field Equations Experiment
Visualize how primorial masks create arithmetic structure in field spectra
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import json
import math

def compute_primorial(n):
    """Compute primorial p# = product of first n primes"""
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
    result = 1
    for i in range(min(n, len(primes))):
        result *= primes[i]
    return result

def gcd(a, b):
    """Greatest common divisor"""
    while b:
        a, b = b, a % b
    return a

def apply_coprime_mask_spectrum(N, primorial_pmax=5):
    """Apply coprime mask and visualize spectrum"""
    primorial = compute_primorial(primorial_pmax)
    print(f"Primorial p#{primorial_pmax} = {primorial}")
    
    # Create k-grid
    k = np.arange(N)
    k[k > N // 2] -= N
    kx, ky, kz = np.meshgrid(k, k, k, indexing='ij')
    k_squared = kx**2 + ky**2 + kz**2
    k_magnitude = np.sqrt(k_squared)
    
    # Create mask: 1 if gcd(|k|, p#) = 1, else 0
    mask = np.ones((N, N, N))
    kept_modes = 0
    total_modes = 0
    
    for i in range(N):
        for j in range(N):
            for k_idx in range(N):
                k_m = int(k_magnitude[i, j, k_idx])
                total_modes += 1
                if k_m > 0:
                    if gcd(k_m, primorial) == 1:
                        mask[i, j, k_idx] = 1.0
                        kept_modes += 1
                    else:
                        mask[i, j, k_idx] = 0.0
    
    kept_percent = 100 * kept_modes / total_modes if total_modes > 0 else 0
    print(f"Kept modes: {kept_modes}/{total_modes} ({kept_percent:.2f}%)")
    
    # Compute shell-averaged mask
    k_max = int(np.max(k_magnitude))
    mask_shells = np.zeros(k_max + 1)
    counts = np.zeros(k_max + 1)
    
    for i in range(N):
        for j in range(N):
            for k_idx in range(N):
                k_m = int(k_magnitude[i, j, k_idx])
                if k_m <= k_max:
                    mask_shells[k_m] += mask[i, j, k_idx]
                    counts[k_m] += 1
    
    mask_shells /= (counts + 1e-10)  # Average
    
    return mask, mask_shells, k_magnitude, primorial

def visualize_primorial_patterns():
    """Visualize arithmetic patterns created by primorial masks"""
    N = 64
    primorial_pmax = 5
    
    mask, mask_shells, k_mag, primorial = apply_coprime_mask_spectrum(N, primorial_pmax)
    
    # Plot shell-averaged mask
    plt.figure(figsize=(12, 8))
    
    plt.subplot(2, 2, 1)
    k_values = np.arange(len(mask_shells))
    plt.plot(k_values, mask_shells, 'o-', markersize=3)
    plt.xlabel('|k|')
    plt.ylabel('Mask value (fraction kept)')
    plt.title(f'Primorial p#{primorial_pmax} = {primorial} Mask Pattern')
    plt.grid(True, alpha=0.3)
    
    # Highlight arithmetic structure
    plt.subplot(2, 2, 2)
    plt.plot(k_values, mask_shells, 'o-', markersize=3, label='Mask')
    # Mark primes
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
    for p in primes:
        if p < len(mask_shells):
            plt.axvline(p, color='r', alpha=0.3, linestyle='--')
    plt.xlabel('|k|')
    plt.ylabel('Mask value')
    plt.title('Arithmetic Structure: Primes vs Coprime Shells')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # 2D slice of mask
    plt.subplot(2, 2, 3)
    mid_slice = mask[:, :, N//2]
    plt.imshow(mid_slice, cmap='viridis', origin='lower')
    plt.colorbar(label='Mask value')
    plt.title('Mask 2D Slice (z = N/2)')
    plt.xlabel('x')
    plt.ylabel('y')
    
    # Histogram of kept modes by |k|
    plt.subplot(2, 2, 4)
    kept_by_k = []
    for k_val in range(len(mask_shells)):
        if mask_shells[k_val] > 0.5:  # Mostly kept
            kept_by_k.append(k_val)
    plt.hist(kept_by_k, bins=20, edgecolor='black', alpha=0.7)
    plt.xlabel('|k|')
    plt.ylabel('Frequency')
    plt.title('Distribution of Kept Modes')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    output_path = Path('results/primorial_patterns.png')
    output_path.parent.mkdir(exist_ok=True)
    plt.savefig(output_path, dpi=150)
    print(f"✓ Saved visualization to {output_path}")
    
    return mask_shells, primorial

def encode_simple_sat():
    """Encode simple SAT: (x ∨ y) ∧ (¬x ∨ z)"""
    # Map SAT to field modes
    # This is a toy encoding - real encoding would be more sophisticated
    sat_info = {
        "clauses": ["(x ∨ y)", "(¬x ∨ z)"],
        "variables": ["x", "y", "z"],
        "encoding": "toy_encoding"
    }
    return sat_info

def main():
    print("=" * 60)
    print("P=NP, Primorials, Field Equations Experiment")
    print("=" * 60)
    
    # Visualize primorial patterns
    print("\n1. Visualizing primorial mask patterns...")
    mask_shells, primorial = visualize_primorial_patterns()
    
    # Encode simple SAT
    print("\n2. Encoding simple SAT problem...")
    sat_info = encode_simple_sat()
    print(f"   SAT: {sat_info['clauses']}")
    
    # Analyze arithmetic structure
    print("\n3. Analyzing arithmetic structure...")
    print(f"   Primorial p#5 = {primorial}")
    print(f"   Mask creates structured pattern in Fourier space")
    print(f"   Kept modes form arithmetic sieve")
    
    # Save results
    results = {
        "primorial": primorial,
        "mask_pattern": mask_shells.tolist(),
        "sat_encoding": sat_info,
        "insight": "Primorial masks create arithmetic structure that filters field modes based on number-theoretic properties. This structure might encode computational problems."
    }
    
    output_path = Path('results/p_np_primorial_results.json')
    output_path.parent.mkdir(exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n✓ Results saved to {output_path}")
    print("\n" + "=" * 60)
    print("Key Insight:")
    print("Primorial masks create arithmetic structure in field spectra.")
    print("This structure filters modes based on number theory,")
    print("potentially encoding computational problems.")
    print("=" * 60)

if __name__ == "__main__":
    main()

