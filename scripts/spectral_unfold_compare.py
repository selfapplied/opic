#!/usr/bin/env .venv/bin/python
"""
Spectral Unfold & Compare
Unfold spectrum before spacing stats, compare to GUE/GOE/Poisson
"""

import json
import math
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple
try:
    from scipy import stats
    from scipy.special import erf
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False
    # Fallback: simple KS test implementation
    def kolmogorov_smirnov_simple(data, cdf_func):
        """Simple KS test without scipy"""
        n = len(data)
        data_sorted = sorted(data)
        d_plus = max((i+1)/n - cdf_func(x) for i, x in enumerate(data_sorted))
        d_minus = max(cdf_func(x) - i/n for i, x in enumerate(data_sorted))
        d = max(d_plus, d_minus)
        # Approximate p-value (simplified)
        p = 1.0 / (1.0 + d * math.sqrt(n))
        return d, p

def wigner_surmise(s: np.ndarray, beta: int = 1) -> np.ndarray:
    """Wigner surmise for GOE (β=1), GUE (β=2), GSE (β=4)"""
    if beta == 1:  # GOE
        return (np.pi * s / 2) * np.exp(-np.pi * s**2 / 4)
    elif beta == 2:  # GUE
        return (32 * s**2 / np.pi**2) * np.exp(-4 * s**2 / np.pi)
    else:
        raise ValueError(f"Beta {beta} not implemented")

def poisson_spacing(s: np.ndarray) -> np.ndarray:
    """Poisson spacing distribution"""
    return np.exp(-s)

def unfold_spectrum(eigenvalues: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """Unfold spectrum: polynomial fit to integrated density → unit-mean spacings"""
    eigenvalues_sorted = np.sort(eigenvalues)
    n = len(eigenvalues_sorted)
    
    # Integrated density: N(E) = number of eigenvalues ≤ E
    # Fit polynomial to N(E)
    # For simplicity, use cumulative count
    cumulative = np.arange(1, n + 1)
    
    # Fit polynomial (degree 3-5 typically)
    degree = min(5, n // 4)
    if degree < 1:
        degree = 1
    
    coeffs = np.polyfit(eigenvalues_sorted, cumulative, degree)
    poly = np.poly1d(coeffs)
    
    # Unfolded eigenvalues: N_unfolded = poly(E)
    unfolded = poly(eigenvalues_sorted)
    
    # Spacings (unit-mean)
    spacings = np.diff(unfolded)
    
    return unfolded, spacings

def compute_spacing_stats(spacings: np.ndarray) -> Dict:
    """Compute spacing statistics"""
    if len(spacings) == 0:
        return {}
    
    mean_spacing = np.mean(spacings)
    variance = np.var(spacings)
    
    # Normalize to unit mean
    normalized_spacings = spacings / mean_spacing if mean_spacing > 0 else spacings
    
    return {
        "mean": mean_spacing,
        "variance": variance,
        "normalized_spacings": normalized_spacings.tolist()
    }

def kolmogorov_smirnov_test(spacings: np.ndarray, theoretical_cdf) -> Dict:
    """KS test against theoretical distribution"""
    if len(spacings) == 0:
        return {"statistic": 0.0, "p_value": 1.0}
    
    # Normalize to unit mean
    mean_spacing = np.mean(spacings)
    normalized = spacings / mean_spacing if mean_spacing > 0 else spacings
    
    # KS test
    if HAS_SCIPY:
        ks_stat, p_value = stats.kstest(normalized, theoretical_cdf)
    else:
        ks_stat, p_value = kolmogorov_smirnov_simple(normalized.tolist(), theoretical_cdf)
    
    return {
        "statistic": float(ks_stat),
        "p_value": float(p_value)
    }

def wigner_cdf(s: float, beta: int = 1) -> float:
    """CDF of Wigner surmise"""
    if beta == 1:  # GOE
        return 1 - np.exp(-np.pi * s**2 / 4)
    elif beta == 2:  # GUE
        return 1 - np.exp(-4 * s**2 / np.pi)
    else:
        return 1 - np.exp(-s)

def poisson_cdf(s: float) -> float:
    """CDF of Poisson spacing"""
    return 1 - np.exp(-s)

def number_variance(L: float, unfolded: np.ndarray) -> float:
    """Number variance Σ²(L)"""
    # Count eigenvalues in windows of length L
    n_windows = max(10, len(unfolded) // 10)
    window_size = L
    counts = []
    
    for i in range(n_windows):
        start = i * window_size
        end = start + window_size
        count = np.sum((unfolded >= start) & (unfolded < end))
        counts.append(count)
    
    if len(counts) == 0:
        return 0.0
    
    mean_count = np.mean(counts)
    variance = np.var(counts)
    return float(variance)

def spectral_rigidity(L: float, unfolded: np.ndarray) -> float:
    """Spectral rigidity Δ₃(L)"""
    # Simplified: variance of integrated density fluctuations
    n_windows = max(10, len(unfolded) // 10)
    window_size = L
    integrated_density = []
    
    for i in range(n_windows):
        end = i * window_size
        count = np.sum(unfolded < end)
        integrated_density.append(count)
    
    if len(integrated_density) == 0:
        return 0.0
    
    # Fit linear trend and compute variance
    x = np.arange(len(integrated_density))
    coeffs = np.polyfit(x, integrated_density, 1)
    trend = np.polyval(coeffs, x)
    residuals = integrated_density - trend
    rigidity = np.var(residuals)
    
    return float(rigidity)

def spectral_entropy(eigenvalues: np.ndarray, k_shells: List[int] = None) -> float:
    """Spectral entropy: entropy of normalized power over k-shells or unfolded spacings"""
    if k_shells is not None:
        # Entropy of power over k-shells
        powers = [abs(e)**2 for e in eigenvalues]
        total_power = sum(powers)
        if total_power == 0:
            return 0.0
        probs = [p / total_power for p in powers]
        entropy = -sum(p * math.log(p + 1e-10) for p in probs if p > 0)
    else:
        # Entropy of unfolded spacings
        _, spacings = unfold_spectrum(eigenvalues)
        if len(spacings) == 0:
            return 0.0
        mean_spacing = np.mean(spacings)
        normalized = spacings / mean_spacing if mean_spacing > 0 else spacings
        # Histogram and compute entropy
        hist, _ = np.histogram(normalized, bins=20)
        probs = hist / np.sum(hist) if np.sum(hist) > 0 else hist
        entropy = -sum(p * math.log(p + 1e-10) for p in probs if p > 0)
    
    return float(entropy)

def generate_laplacian_eigenmodes(N: int) -> np.ndarray:
    """Generate eigenvalues of pure Laplacian eigenmodes"""
    # Simplified: eigenvalues of -∇² on periodic domain
    k_max = N // 2
    eigenvalues = []
    for kx in range(-k_max, k_max + 1):
        for ky in range(-k_max, k_max + 1):
            for kz in range(-k_max, k_max + 1):
                k_sq = kx**2 + ky**2 + kz**2
                if k_sq > 0:
                    eigenvalues.append(k_sq)
    return np.array(sorted(eigenvalues))

def generate_random_hermitian(N: int, seed: int = 42) -> np.ndarray:
    """Generate eigenvalues of random Hermitian (GOE)"""
    np.random.seed(seed)
    # Generate random Hermitian matrix
    A = np.random.randn(N, N) + 1j * np.random.randn(N, N)
    A = (A + A.T.conj()) / 2  # Hermitian
    eigenvalues = np.real(np.linalg.eigvals(A))
    return np.sort(eigenvalues)

def generate_zeta_like_operator(N: int, seed: int = 42) -> np.ndarray:
    """Generate eigenvalues of ζ-like operator"""
    np.random.seed(seed)
    # Simplified: multiplicative structure
    eigenvalues = []
    for k in range(1, N + 1):
        # Toy zeta-like: 1/(s - 1) structure
        value = 1.0 / (k - 1.0 + 1e-6)
        eigenvalues.append(value)
    return np.array(sorted(eigenvalues))

def compare_spectra(baselines: Dict[str, np.ndarray], L_values: List[float] = None) -> Dict:
    """Compare spectra: unfold, spacing stats, KS tests, number variance, rigidity"""
    if L_values is None:
        L_values = [1.0, 2.0, 5.0, 10.0]
    
    results = {}
    
    for name, eigenvalues in baselines.items():
        # Unfold
        unfolded, spacings = unfold_spectrum(eigenvalues)
        
        # Spacing stats
        spacing_stats = compute_spacing_stats(spacings)
        
        # KS tests
        ks_goe = kolmogorov_smirnov_test(spacings, lambda s: wigner_cdf(s, beta=1))
        ks_gue = kolmogorov_smirnov_test(spacings, lambda s: wigner_cdf(s, beta=2))
        ks_poisson = kolmogorov_smirnov_test(spacings, poisson_cdf)
        
        # Number variance and rigidity
        number_vars = {L: number_variance(L, unfolded) for L in L_values}
        rigidities = {L: spectral_rigidity(L, unfolded) for L in L_values}
        
        # Spectral entropy
        entropy = spectral_entropy(eigenvalues)
        
        results[name] = {
            "spacing_stats": spacing_stats,
            "ks_tests": {
                "goe": ks_goe,
                "gue": ks_gue,
                "poisson": ks_poisson
            },
            "number_variance": number_vars,
            "spectral_rigidity": rigidities,
            "spectral_entropy": entropy,
            "n_eigenvalues": len(eigenvalues)
        }
    
    return results

def main():
    print("=" * 60)
    print("Spectral Unfold & Compare")
    print("=" * 60)
    
    N = 64
    
    # Generate baselines
    print("\nGenerating baselines...")
    baselines = {
        "laplacian": generate_laplacian_eigenmodes(N),
        "random_hermitian_goe": generate_random_hermitian(N, seed=42),
        "zeta_like": generate_zeta_like_operator(N, seed=42)
    }
    
    print(f"  Laplacian: {len(baselines['laplacian'])} eigenvalues")
    print(f"  Random Hermitian (GOE): {len(baselines['random_hermitian_goe'])} eigenvalues")
    print(f"  Zeta-like: {len(baselines['zeta_like'])} eigenvalues")
    
    # Compare
    print("\nComparing spectra...")
    results = compare_spectra(baselines)
    
    print("\nResults:")
    for name, res in results.items():
        print(f"\n{name}:")
        print(f"  Spacing variance: {res['spacing_stats'].get('variance', 0):.6f}")
        print(f"  KS vs GOE: p={res['ks_tests']['goe']['p_value']:.4f}")
        print(f"  KS vs GUE: p={res['ks_tests']['gue']['p_value']:.4f}")
        print(f"  KS vs Poisson: p={res['ks_tests']['poisson']['p_value']:.4f}")
        print(f"  Spectral entropy: {res['spectral_entropy']:.4f}")
        print(f"  Number variance Σ²(5): {res['number_variance'].get(5.0, 0):.4f}")
        print(f"  Spectral rigidity Δ₃(5): {res['spectral_rigidity'].get(5.0, 0):.4f}")
    
    # Save results
    output_path = Path('results/spectral_unfold_compare.json')
    output_path.parent.mkdir(exist_ok=True)
    
    # Convert numpy arrays to lists for JSON
    json_results = {}
    for name, res in results.items():
        json_results[name] = res.copy()
        if 'spacing_stats' in json_results[name] and 'normalized_spacings' in json_results[name]['spacing_stats']:
            pass  # Already list
    
    with open(output_path, 'w') as f:
        json.dump(json_results, f, indent=2)
    
    print(f"\n✓ Results saved to {output_path}")

if __name__ == "__main__":
    main()

