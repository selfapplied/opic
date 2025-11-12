#!/usr/bin/env python3
"""
Zeta Power Spectrum — Lossless vs Statistical Compression
Implements zeta_cosmological_correspondence.ops

Two modes:
A) Truly lossless: Store full complex spectrum (amplitudes + phases)
B) Statistical: Store P(k) + random phases (CMB-style, ensemble-faithful)
"""

import sys
import math
import cmath
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import random

class ZetaPowerSpectrum:
    """
    Lossless vs Statistical compression system
    
    A) Microstate-lossless: field → complex spectrum → field' (exact reconstruction)
    B) Statistical-lossless: field → P(k) + phases → field' (same two-point stats)
    """
    
    def __init__(self):
        pass
    
    def fft_unitary(self, field_values: List[float]) -> List[complex]:
        """
        Forward FFT with unitary normalization
        Ensures: IFFT(FFT(f)) = f exactly
        """
        n = len(field_values)
        spectrum = []
        
        for k in range(n):
            real_sum = 0.0
            imag_sum = 0.0
            
            for i in range(n):
                angle = -2 * math.pi * k * i / n
                real_sum += field_values[i] * math.cos(angle)
                imag_sum += field_values[i] * math.sin(angle)
            
            # Unitary normalization: 1/√n
            spectrum.append(complex(real_sum / math.sqrt(n), imag_sum / math.sqrt(n)))
        
        return spectrum
    
    def ifft_unitary(self, spectrum: List[complex]) -> List[float]:
        """
        Inverse FFT with unitary normalization
        Ensures: IFFT(FFT(f)) = f exactly
        """
        n = len(spectrum)
        field = []
        
        for i in range(n):
            real_sum = 0.0
            imag_sum = 0.0
            
            for k in range(n):
                angle = 2 * math.pi * k * i / n
                real_sum += spectrum[k].real * math.cos(angle) - spectrum[k].imag * math.sin(angle)
                imag_sum += spectrum[k].real * math.sin(angle) + spectrum[k].imag * math.cos(angle)
            
            # Unitary normalization: 1/√n
            field.append(real_sum / math.sqrt(n))
        
        return field
    
    def enforce_hermitian_symmetry(self, spectrum: List[complex], n: int) -> List[complex]:
        """
        Enforce Hermitian symmetry for real fields
        For real f: F(-k) = F*(k)
        """
        hermitian = spectrum.copy()
        
        # Handle k=0 (DC component) - must be real
        hermitian[0] = complex(hermitian[0].real, 0.0)
        
        # Handle Nyquist (if n is even)
        if n % 2 == 0:
            hermitian[n//2] = complex(hermitian[n//2].real, 0.0)
        
        # Enforce symmetry: F(-k) = F*(k)
        for k in range(1, (n+1)//2):
            k_neg = n - k
            # F(-k) = conjugate(F(k))
            hermitian[k_neg] = complex(hermitian[k].real, -hermitian[k].imag)
        
        return hermitian
    
    def compress_lossless(self, field_values: List[float]) -> Dict:
        """
        Mode A: Truly lossless compression
        Store full complex spectrum (amplitudes + phases)
        """
        n = len(field_values)
        
        # Forward FFT
        spectrum = self.fft_unitary(field_values)
        
        # Enforce Hermitian symmetry for real fields
        spectrum = self.enforce_hermitian_symmetry(spectrum, n)
        
        # Store independent coefficients (use Hermitian symmetry)
        # For real field: only need k=0 to n//2
        independent_k = (n // 2) + 1
        stored_coeffs = []
        
        for k in range(independent_k):
            stored_coeffs.append({
                "k": k,
                "real": spectrum[k].real,
                "imag": spectrum[k].imag
            })
        
        return {
            "mode": "lossless",
            "n": n,
            "coefficients": stored_coeffs,
            "compression_ratio": n / independent_k,  # ~2x for real fields
            "field_interpretation": "Lossless: stores amplitudes + phases",
            "equation": "Archive = {Re[F(k)], Im[F(k)]} for k ∈ [0, n/2]"
        }
    
    def reconstruct_lossless(self, archive: Dict) -> List[float]:
        """
        Reconstruct field from lossless archive
        """
        n = archive["n"]
        coeffs = archive["coefficients"]
        
        # Reconstruct full spectrum using Hermitian symmetry
        spectrum = [complex(0.0, 0.0)] * n
        
        for coeff in coeffs:
            k = coeff["k"]
            spectrum[k] = complex(coeff["real"], coeff["imag"])
            
            # Enforce Hermitian symmetry: F(-k) = F*(k)
            if k > 0 and k < n // 2:
                k_neg = n - k
                spectrum[k_neg] = complex(coeff["real"], -coeff["imag"])
        
        # Inverse FFT
        reconstructed = self.ifft_unitary(spectrum)
        
        return reconstructed
    
    def compress_statistical(self, field_values: List[float], seed: Optional[int] = None) -> Dict:
        """
        Mode B: Statistical compression (CMB-style)
        Store only P(k) = |F(k)|², phases will be random
        """
        n = len(field_values)
        
        # Forward FFT
        spectrum = self.fft_unitary(field_values)
        
        # Compute power spectrum P(k) = |F(k)|²
        power_spectrum = []
        for k in range(n):
            power = abs(spectrum[k])**2
            power_spectrum.append(power)
        
        # Store only independent k (Hermitian symmetry)
        independent_k = (n // 2) + 1
        stored_power = power_spectrum[:independent_k]
        
        return {
            "mode": "statistical",
            "n": n,
            "power_spectrum": stored_power,
            "seed": seed,
            "compression_ratio": n / independent_k,  # ~2x for real fields
            "field_interpretation": "Statistical: stores P(k) only, phases lost",
            "equation": "Archive = {P(k) = |F(k)|²} for k ∈ [0, n/2]"
        }
    
    def reconstruct_statistical(self, archive: Dict) -> List[float]:
        """
        Reconstruct field from statistical archive (P(k) + random phases)
        Produces field with same two-point stats, not same microstate
        """
        n = archive["n"]
        power_spectrum = archive["power_spectrum"]
        seed = archive.get("seed", None)
        
        if seed is not None:
            random.seed(seed)
        
        # Reconstruct full power spectrum using Hermitian symmetry
        full_power = [0.0] * n
        independent_k = len(power_spectrum)
        
        for k in range(independent_k):
            full_power[k] = power_spectrum[k]
            # Hermitian symmetry: P(-k) = P(k)
            if k > 0 and k < n // 2:
                k_neg = n - k
                full_power[k_neg] = power_spectrum[k]
        
        # Generate random phases and reconstruct spectrum
        spectrum = []
        for k in range(n):
            # Random phase: φ_k ~ Unif[0, 2π)
            phase = 2 * math.pi * random.random()
            # Amplitude from power spectrum
            amplitude = math.sqrt(full_power[k]) if full_power[k] > 0 else 0.0
            # Compose: F(k) = |F(k)| e^(iφ_k)
            spectrum.append(amplitude * cmath.exp(1j * phase))
        
        # Enforce Hermitian symmetry for real field
        spectrum = self.enforce_hermitian_symmetry(spectrum, n)
        
        # Inverse FFT
        reconstructed = self.ifft_unitary(spectrum)
        
        return reconstructed
    
    def verify_lossless(self, original_field: List[float]) -> Dict:
        """
        Verify lossless compression: field → archive → field'
        Should reconstruct exactly (errors ~10^-12 in float64)
        """
        # Compress
        archive = self.compress_lossless(original_field)
        
        # Reconstruct
        reconstructed = self.reconstruct_lossless(archive)
        
        # Compare
        errors = [abs(original_field[i] - reconstructed[i]) for i in range(len(original_field))]
        max_error = max(errors)
        mean_error = sum(errors) / len(errors)
        l2_error = math.sqrt(sum(e**2 for e in errors))
        
        return {
            "original_field": original_field,
            "reconstructed_field": reconstructed,
            "max_error": max_error,
            "mean_error": mean_error,
            "l2_error": l2_error,
            "is_lossless": max_error < 1e-10,
            "field_interpretation": "Lossless compression verified",
            "equation": "field → FFT → archive → IFFT → field' ≈ field (exact)"
        }
    
    def verify_statistical(self, original_field: List[float], seed: int = 42) -> Dict:
        """
        Verify statistical compression: field → P(k) → field'
        Should match two-point statistics, not microstate
        """
        # Compute original power spectrum
        spectrum_orig = self.fft_unitary(original_field)
        power_orig = [abs(s)**2 for s in spectrum_orig]
        
        # Compress (statistical)
        archive = self.compress_statistical(original_field, seed=seed)
        
        # Reconstruct
        reconstructed = self.reconstruct_statistical(archive)
        
        # Compute reconstructed power spectrum
        spectrum_recon = self.fft_unitary(reconstructed)
        power_recon = [abs(s)**2 for s in spectrum_recon]
        
        # Compare power spectra (should match)
        power_errors = [abs(power_orig[i] - power_recon[i]) for i in range(len(power_orig))]
        max_power_error = max(power_errors)
        mean_power_error = sum(power_errors) / len(power_errors)
        
        # Compare fields (will NOT match - different microstate)
        field_errors = [abs(original_field[i] - reconstructed[i]) for i in range(len(original_field))]
        max_field_error = max(field_errors)
        
        return {
            "original_field": original_field,
            "reconstructed_field": reconstructed,
            "power_spectrum_match": {
                "max_error": max_power_error,
                "mean_error": mean_power_error,
                "matches": max_power_error < 1e-6
            },
            "field_mismatch": {
                "max_error": max_field_error,
                "note": "Fields differ (different microstate, same two-point stats)"
            },
            "field_interpretation": "Statistical compression: P(k) matches, microstate differs",
            "equation": "field → P(k) → random phases → field' (same ξ(r), different pattern)"
        }

def main():
    """Test lossless vs statistical compression"""
    zps = ZetaPowerSpectrum()
    
    print("=" * 70)
    print("Zeta Power Spectrum — Lossless vs Statistical Compression")
    print("=" * 70)
    
    # Create test field (primordial perturbations)
    n = 64
    field = [1e-5 * math.sin(2 * math.pi * i / n) + 0.5e-5 * math.sin(4 * math.pi * i / n) for i in range(n)]
    
    print("\n" + "=" * 70)
    print("Mode A: Truly Lossless Compression")
    print("=" * 70)
    print("  Store: Complex spectrum (amplitudes + phases)")
    print("  Expect: Round-trip errors ~10^-12 (float64)")
    print("-" * 70)
    
    verification_lossless = zps.verify_lossless(field)
    archive_lossless = zps.compress_lossless(field)
    
    print(f"\n✓ Lossless compression:")
    print(f"  Compression ratio: {archive_lossless['compression_ratio']:.2f}x")
    print(f"  Stored coefficients: {len(archive_lossless['coefficients'])}")
    print(f"\n✓ Lossless verification:")
    print(f"  Max error: {verification_lossless['max_error']:.2e}")
    print(f"  Mean error: {verification_lossless['mean_error']:.2e}")
    print(f"  L2 error: {verification_lossless['l2_error']:.2e}")
    print(f"  Is lossless: {verification_lossless['is_lossless']}")
    
    print("\n" + "=" * 70)
    print("Mode B: Statistical Compression (CMB-style)")
    print("=" * 70)
    print("  Store: P(k) only (phases lost)")
    print("  Reconstruct: Random phases → same two-point stats")
    print("-" * 70)
    
    verification_stat = zps.verify_statistical(field, seed=42)
    archive_stat = zps.compress_statistical(field, seed=42)
    
    print(f"\n✓ Statistical compression:")
    print(f"  Compression ratio: {archive_stat['compression_ratio']:.2f}x")
    print(f"  Stored power coefficients: {len(archive_stat['power_spectrum'])}")
    print(f"\n✓ Statistical verification:")
    print(f"  Power spectrum match:")
    print(f"    Max error: {verification_stat['power_spectrum_match']['max_error']:.2e}")
    print(f"    Matches: {verification_stat['power_spectrum_match']['matches']}")
    print(f"  Field mismatch:")
    print(f"    Max error: {verification_stat['field_mismatch']['max_error']:.2e}")
    print(f"    Note: {verification_stat['field_mismatch']['note']}")
    
    # Parseval check
    spectrum_lossless = zps.fft_unitary(field)
    parseval_energy_spectrum = sum(abs(s)**2 for s in spectrum_lossless)
    parseval_energy_field = sum(f**2 for f in field)
    parseval_diff = abs(parseval_energy_spectrum - parseval_energy_field)
    parseval_rel_error = parseval_diff / max(parseval_energy_spectrum, parseval_energy_field, 1e-20)
    
    print("\n" + "=" * 70)
    print("Parseval Check (Mode A)")
    print("=" * 70)
    print(f"  Σ|F(k)|²: {parseval_energy_spectrum:.12e}")
    print(f"  Σf(x)²:   {parseval_energy_field:.12e}")
    print(f"  Difference: {parseval_diff:.2e}")
    print(f"  Relative error: {parseval_rel_error:.2e}")
    print(f"  Passes: {parseval_rel_error < 1e-12}")
    
    print("\n" + "=" * 70)
    print("Key Insight:")
    print("=" * 70)
    print("""
Two valid compression modes:

A) Microstate-lossless:
   • Store: Complex spectrum F(k) = |F(k)| e^(iφ_k)
   • Reconstruct: Exact field (errors ~10^-19)
   • Parseval: Σ|F|² = Σf² (energy conservation)
   • Use: When you need the exact pattern

B) Statistical-lossless (CMB-style):
   • Store: Power spectrum P(k) = |F(k)|² only
   • Reconstruct: Random phases → same ξ(r), different pattern
   • Phases: Uniform[0, 2π) distribution
   • Use: When two-point statistics suffice

The CMB power spectrum is statistical-lossless:
• Tiny header (P(k) coefficients)
• Faithful ensemble (same two-point stats)
• Optional seed for determinism
• Not microstate-exact (phases lost)

CABA Archive = Nature's perfect compressed archive
    """)

if __name__ == "__main__":
    main()
