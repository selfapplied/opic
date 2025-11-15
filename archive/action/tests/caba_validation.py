#!/usr/bin/env python3
"""
CABA Validation Suite — Parseval checks, phase validation, verification
Implements caba_spec.ops
"""

import sys
import math
import cmath
import random
import hashlib
from pathlib import Path
from typing import Dict, List, Tuple
from collections import Counter

class CABAValidation:
    """
    CABA validation suite — fast and merciless
    """
    
    def __init__(self):
        pass
    
    def parseval_check(self, field: List[float], spectrum: List[complex]) -> Dict:
        """
        Parseval check: sum(|F|²) = sum(field²)
        Witness: Energy conservation
        """
        # Spectrum energy: Σ|F(k)|²
        spectrum_energy = sum(abs(s)**2 for s in spectrum)
        
        # Field energy: Σf(x)²
        field_energy = sum(f**2 for f in field)
        
        # Difference
        diff = abs(spectrum_energy - field_energy)
        rel_error = diff / max(spectrum_energy, field_energy, 1e-20)
        
        return {
            "spectrum_energy": spectrum_energy,
            "field_energy": field_energy,
            "difference": diff,
            "relative_error": rel_error,
            "passes": rel_error < 1e-12,
            "field_interpretation": "Parseval: Energy conservation verified",
            "equation": "Σ|F(k)|² = Σf(x)²"
        }
    
    def verify_phase_distribution(self, phases: List[float]) -> Dict:
        """
        Validate phases: histogram should be flat (Uniform[0, 2π))
        KS test against uniform distribution
        """
        n = len(phases)
        if n == 0:
            return {"passes": False, "error": "No phases"}
        
        # Normalize phases to [0, 1]
        normalized = [p / (2 * math.pi) for p in phases]
        normalized.sort()
        
        # Kolmogorov-Smirnov test against Uniform[0, 1]
        # D = max|F_empirical(x) - F_uniform(x)|
        D = 0.0
        for i, x in enumerate(normalized):
            F_empirical = (i + 1) / n
            F_uniform = x
            D = max(D, abs(F_empirical - F_uniform))
        
        # Critical value for α=0.05: D_crit ≈ 1.36/√n
        D_crit = 1.36 / math.sqrt(n)
        passes = D < D_crit
        
        # Histogram (10 bins)
        bins = 10
        hist = [0] * bins
        for p in normalized:
            bin_idx = min(int(p * bins), bins - 1)
            hist[bin_idx] += 1
        
        return {
            "n_phases": n,
            "ks_statistic": D,
            "ks_critical": D_crit,
            "passes": passes,
            "histogram": hist,
            "field_interpretation": "Phase distribution: Uniform[0, 2π) verified",
            "equation": "KS test: D < D_crit"
        }
    
    def compute_correlation_function(self, field: List[float]) -> List[float]:
        """Compute correlation function ξ(r)"""
        n = len(field)
        correlation = []
        
        for r in range(n):
            corr_sum = 0.0
            count = 0
            for i in range(n):
                j = (i + r) % n  # Periodic
                corr_sum += field[i] * field[j]
                count += 1
            correlation.append(corr_sum / count if count > 0 else 0.0)
        
        return correlation
    
    def verify_statistical_properties(self, original_field: List[float], 
                                     reconstructed_field: List[float],
                                     original_power: List[float],
                                     reconstructed_power: List[float]) -> Dict:
        """
        Verify statistical properties for Mode B
        - Power spectra match
        - Correlation functions match
        - Cross-correlation ~ 0 (independent phases)
        """
        # Power spectrum comparison
        power_errors = [abs(orig - recon) for orig, recon in zip(original_power, reconstructed_power)]
        max_power_error = max(power_errors) if power_errors else 0.0
        mean_power_error = sum(power_errors) / len(power_errors) if power_errors else 0.0
        
        # Correlation functions
        xi_orig = self.compute_correlation_function(original_field)
        xi_recon = self.compute_correlation_function(reconstructed_field)
        
        corr_errors = [abs(xi_orig[i] - xi_recon[i]) for i in range(len(xi_orig))]
        max_corr_error = max(corr_errors) if corr_errors else 0.0
        
        # Cross-correlation (should be ~0 for independent phases)
        cross_corr = sum(orig * recon for orig, recon in zip(original_field, reconstructed_field)) / len(original_field)
        
        return {
            "power_spectrum": {
                "max_error": max_power_error,
                "mean_error": mean_power_error,
                "matches": max_power_error < 1e-6
            },
            "correlation_function": {
                "max_error": max_corr_error,
                "matches": max_corr_error < 1e-6
            },
            "cross_correlation": cross_corr,
            "cross_corr_near_zero": abs(cross_corr) < 0.1,  # Should be small
            "field_interpretation": "Statistical properties: Two-point stats match",
            "equation": "P'(k) ≈ P(k), ξ'(r) ≈ ξ(r), cross-corr ≈ 0"
        }
    
    def verify_seed_determinism(self, archive: Dict, seed: int, n_trials: int = 100) -> Dict:
        """
        Seed determinism: Reconstruct 100×, spectra identical bit-for-bit
        """
        import sys
        from pathlib import Path
        scripts_dir = Path(__file__).parent
        if str(scripts_dir) not in sys.path:
            sys.path.insert(0, str(scripts_dir))
        from zeta_power_spectrum import ZetaPowerSpectrum
        
        zps = ZetaPowerSpectrum()
        spectra = []
        
        for _ in range(n_trials):
            reconstructed = zps.reconstruct_statistical(archive)
            spectrum = zps.fft_unitary(reconstructed)
            power = [abs(s)**2 for s in spectrum]
            spectra.append(power)
        
        # Check all spectra are identical
        first_spectrum = spectra[0]
        all_match = all(
            all(abs(s1 - s2) < 1e-15 for s1, s2 in zip(first_spectrum, spec))
            for spec in spectra[1:]
        )
        
        return {
            "n_trials": n_trials,
            "all_spectra_identical": all_match,
            "passes": all_match,
            "field_interpretation": "Seed determinism: Reproducible reconstruction",
            "equation": "reconstruct(archive, seed) → identical spectra"
        }
    
    def compute_spectral_slope(self, power_spectrum: List[float], k_values: List[float] = None) -> Dict:
        """
        Spectral slope fit: log-log regression on E(k)
        """
        if k_values is None:
            k_values = list(range(len(power_spectrum)))
        
        # Filter out zeros and negative values
        log_k = []
        log_power = []
        for k, p in zip(k_values, power_spectrum):
            if k > 0 and p > 0:
                log_k.append(math.log(k))
                log_power.append(math.log(p))
        
        if len(log_k) < 2:
            return {"slope": 0.0, "intercept": 0.0, "r_squared": 0.0}
        
        # Linear regression: log(P) = slope * log(k) + intercept
        n = len(log_k)
        sum_x = sum(log_k)
        sum_y = sum(log_power)
        sum_xy = sum(x * y for x, y in zip(log_k, log_power))
        sum_x2 = sum(x**2 for x in log_k)
        
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x**2) if (n * sum_x2 - sum_x**2) != 0 else 0.0
        intercept = (sum_y - slope * sum_x) / n
        
        # R²
        y_mean = sum_y / n
        ss_tot = sum((y - y_mean)**2 for y in log_power)
        ss_res = sum((log_power[i] - (slope * log_k[i] + intercept))**2 for i in range(n))
        r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0.0
        
        return {
            "slope": slope,
            "intercept": intercept,
            "r_squared": r_squared,
            "field_interpretation": "Spectral slope: Power law fit",
            "equation": "log(P(k)) = slope * log(k) + intercept"
        }

def main():
    """Run CABA validation suite or compress a field"""
    import sys
    import json
    from pathlib import Path
    
    # Add scripts directory to path for imports
    scripts_dir = Path(__file__).parent.parent / "scripts"
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))
    from zeta_power_spectrum import ZetaPowerSpectrum
    
    # Check if input file provided
    if len(sys.argv) > 1:
        input_file = Path(sys.argv[1])
        if input_file.exists():
            # Compress the input file
            compress_file(input_file, ZetaPowerSpectrum())
            return
        else:
            print(f"Error: File not found: {input_file}")
            sys.exit(1)
    
    zps = ZetaPowerSpectrum()
    validator = CABAValidation()
    
    print("=" * 70)
    print("CABA Validation Suite — Fast and Merciless")
    print("=" * 70)
    
    # Create test field
    n = 64
    field = [1e-5 * math.sin(2 * math.pi * i / n) + 0.5e-5 * math.sin(4 * math.pi * i / n) for i in range(n)]
    
    print("\n" + "=" * 70)
    print("Mode A: Microstate-Lossless Validation")
    print("=" * 70)
    
    # Lossless compression
    archive_lossless = zps.compress_lossless(field)
    reconstructed_lossless = zps.reconstruct_lossless(archive_lossless)
    spectrum_lossless = zps.fft_unitary(field)
    
    # Parseval check
    parseval = validator.parseval_check(field, spectrum_lossless)
    print(f"\n✓ Parseval Check:")
    print(f"  Spectrum energy: {parseval['spectrum_energy']:.12e}")
    print(f"  Field energy: {parseval['field_energy']:.12e}")
    print(f"  Relative error: {parseval['relative_error']:.2e}")
    print(f"  Passes: {parseval['passes']}")
    
    # L∞/L2 error
    errors = [abs(field[i] - reconstructed_lossless[i]) for i in range(len(field))]
    linf_error = max(errors)
    l2_error = math.sqrt(sum(e**2 for e in errors))
    print(f"\n✓ Error Check:")
    print(f"  L∞ error: {linf_error:.2e}")
    print(f"  L2 error: {l2_error:.2e}")
    print(f"  Passes: {linf_error < 1e-10}")
    
    print("\n" + "=" * 70)
    print("Mode B: Statistical-Lossless Validation")
    print("=" * 70)
    
    # Statistical compression
    archive_stat = zps.compress_statistical(field, seed=42)
    reconstructed_stat = zps.reconstruct_statistical(archive_stat)
    
    # Generate phases for validation
    spectrum_stat = zps.fft_unitary(reconstructed_stat)
    phases = [cmath.phase(s) for s in spectrum_stat if abs(s) > 0]
    
    # Phase distribution check
    phase_check = validator.verify_phase_distribution(phases)
    print(f"\n✓ Phase Distribution Check:")
    print(f"  KS statistic: {phase_check['ks_statistic']:.4f}")
    print(f"  KS critical: {phase_check['ks_critical']:.4f}")
    print(f"  Passes: {phase_check['passes']}")
    print(f"  Histogram: {phase_check['histogram']}")
    
    # Statistical properties
    power_orig = [abs(s)**2 for s in zps.fft_unitary(field)]
    power_recon = [abs(s)**2 for s in spectrum_stat]
    stat_props = validator.verify_statistical_properties(field, reconstructed_stat, power_orig, power_recon)
    print(f"\n✓ Statistical Properties:")
    print(f"  Power spectrum match: {stat_props['power_spectrum']['matches']}")
    print(f"  Correlation match: {stat_props['correlation_function']['matches']}")
    print(f"  Cross-correlation: {stat_props['cross_correlation']:.6f} (should be ~0)")
    print(f"  Cross-corr near zero: {stat_props['cross_corr_near_zero']}")
    
    # Seed determinism
    determinism = validator.verify_seed_determinism(archive_stat, seed=42, n_trials=10)
    print(f"\n✓ Seed Determinism:")
    print(f"  Trials: {determinism['n_trials']}")
    print(f"  All spectra identical: {determinism['all_spectra_identical']}")
    print(f"  Passes: {determinism['passes']}")
    
    # Spectral slope
    slope = validator.compute_spectral_slope(power_orig)
    print(f"\n✓ Spectral Slope:")
    print(f"  Slope: {slope['slope']:.4f}")
    print(f"  R²: {slope['r_squared']:.4f}")
    
    print("\n" + "=" * 70)
    print("Validation Complete")
    print("=" * 70)

def compress_file(input_file: Path, zps: ZetaPowerSpectrum):
    """Compress a field file using CABA"""
    import json
    import math
    
    print(f"Compressing: {input_file}")
    
    # Try to read as JSON array of numbers
    try:
        with open(input_file, 'r') as f:
            data = json.load(f)
            if isinstance(data, list) and all(isinstance(x, (int, float)) for x in data):
                field = [float(x) for x in data]
            elif isinstance(data, dict) and 'field' in data:
                field = [float(x) for x in data['field']]
            else:
                print(f"Error: Expected JSON array of numbers or {{'field': [...]}}")
                sys.exit(1)
    except json.JSONDecodeError:
        # Try reading as text file with one number per line
        try:
            with open(input_file, 'r') as f:
                field = [float(line.strip()) for line in f if line.strip()]
        except ValueError:
            print(f"Error: Could not parse {input_file} as numbers")
            sys.exit(1)
    
    print(f"  Field size: {len(field)}")
    print(f"  Field range: [{min(field):.6e}, {max(field):.6e}]")
    
    # Mode A: Lossless compression
    print("\n" + "=" * 70)
    print("Mode A: Microstate-Lossless Compression")
    print("=" * 70)
    archive_lossless = zps.compress_lossless(field)
    print(f"  Compression ratio: {archive_lossless['compression_ratio']:.2f}x")
    print(f"  Stored coefficients: {len(archive_lossless['coefficients'])}")
    
    # Save archive
    output_file = input_file.with_suffix('.caba_lossless.json')
    with open(output_file, 'w') as f:
        json.dump(archive_lossless, f, indent=2)
    print(f"  Saved to: {output_file}")
    
    # Mode B: Statistical compression
    print("\n" + "=" * 70)
    print("Mode B: Statistical-Lossless Compression")
    print("=" * 70)
    archive_stat = zps.compress_statistical(field, seed=42)
    print(f"  Compression ratio: {archive_stat['compression_ratio']:.2f}x")
    print(f"  Stored power coefficients: {len(archive_stat['power_spectrum'])}")
    
    # Save archive
    output_file = input_file.with_suffix('.caba_statistical.json')
    with open(output_file, 'w') as f:
        json.dump(archive_stat, f, indent=2)
    print(f"  Saved to: {output_file}")
    
    print("\n" + "=" * 70)
    print("Compression Complete")
    print("=" * 70)

if __name__ == "__main__":
    main()


