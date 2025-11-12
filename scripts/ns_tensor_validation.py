#!/usr/bin/env python3
"""
Navier-Stokes × Tensor Descent Validation Protocol v0.1
Falsifiable, unit-consistent experiments
Implements ns_tensor_validation.ops
"""

import sys
import math
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import hashlib
import random

class NSTensorValidation:
    """
    Validation protocol for NS × Tensor Descent
    No grand claims — only measurable effects
    """
    
    def __init__(self, config: Dict):
        self.config = config
        self.seed = config.get("seed", 42)
        random.seed(self.seed)
        
        # Domain
        self.dimension = config.get("dimension", 2)  # 2D torus T²
        self.N = config.get("grid_points", 64)  # Grid points per dimension
        self.L = config.get("domain_size", 2 * math.pi)  # Domain size
        
        # Physical parameters
        self.nu = config.get("viscosity", 0.01)  # ν
        self.k_f = config.get("forcing_shell", 4)  # Forcing wavenumber
        self.dt = config.get("time_step", 0.001)  # Time step
        
        # Filter parameters
        self.filter_type = config.get("filter_type", "coprime")  # coprime, von_mangoldt, prime_shell
        self.filter_params = config.get("filter_params", {})
        
        # Descent parameters
        self.eta = config.get("descent_eta", 0.0)  # η (0 = disabled)
        self.alpha = config.get("descent_alpha", 0.1)
        self.gamma = config.get("descent_gamma", 0.01)
        
        # Diagnostics storage
        self.diagnostics = []
        
        # Initialize spectral grid
        self._init_spectral_grid()
        
        # Initialize filter mask
        self._init_filter_mask()
    
    def _init_spectral_grid(self):
        """Initialize spectral grid (wave numbers)"""
        self.kx = [2 * math.pi * i / self.L for i in range(-self.N//2, self.N//2)]
        if self.dimension == 2:
            self.ky = self.kx.copy()
        elif self.dimension == 3:
            self.ky = self.kx.copy()
            self.kz = self.kx.copy()
    
    def _init_filter_mask(self):
        """Initialize primorial filter mask"""
        self.mask = {}
        
        if self.filter_type == "coprime":
            p_sharp = self.filter_params.get("primorial", 30)  # p#
            for k in self.kx:
                k_abs = abs(int(k))
                if k_abs == 0:
                    self.mask[k] = 1.0
                else:
                    # Check if gcd(|k|, p#) = 1
                    if math.gcd(k_abs, p_sharp) == 1:
                        self.mask[k] = 1.0
                    else:
                        self.mask[k] = 0.0
        
        elif self.filter_type == "von_mangoldt":
            alpha = self.filter_params.get("alpha", 0.1)
            for k in self.kx:
                k_abs = abs(int(k))
                if k_abs == 0:
                    self.mask[k] = 1.0
                else:
                    # Von Mangoldt function Λ(n)
                    lambda_n = self._von_mangoldt(k_abs)
                    self.mask[k] = 1.0 + alpha * lambda_n
        
        elif self.filter_type == "prime_shell":
            p_max = self.filter_params.get("prime_max", 20)
            beta = self.filter_params.get("beta", 0.1)
            primes = self._primes_up_to(p_max)
            for k in self.kx:
                k_abs = abs(int(k))
                if k_abs in primes:
                    self.mask[k] = 1.0
                else:
                    self.mask[k] = beta
    
    def _von_mangoldt(self, n: int) -> float:
        """Von Mangoldt function Λ(n)"""
        if n == 1:
            return 0.0
        # Check if n is a prime power
        for p in range(2, int(math.sqrt(n)) + 1):
            if n % p == 0:
                # Check if n is a power of p
                temp = n
                power = 0
                while temp % p == 0:
                    temp //= p
                    power += 1
                if temp == 1:
                    return math.log(p)
        # If n is prime
        if self._is_prime(n):
            return math.log(n)
        return 0.0
    
    def _is_prime(self, n: int) -> bool:
        """Check if n is prime"""
        if n < 2:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True
    
    def _primes_up_to(self, n: int) -> List[int]:
        """Generate primes up to n"""
        primes = []
        for i in range(2, n + 1):
            if self._is_prime(i):
                primes.append(i)
        return primes
    
    def apply_filter(self, u_hat: Dict) -> Dict:
        """Apply primorial filter mask — scope {}"""
        filtered = {}
        for k, value in u_hat.items():
            mask_value = self.mask.get(k, 1.0)
            filtered[k] = value * mask_value
        return filtered
    
    def compute_nonlinear_term(self, u_hat: Dict) -> Dict:
        """Nonlinear operator: N(u) = Π(-u·∇u) — morphism ()"""
        # Simplified: convolution in Fourier space
        # Full implementation would use FFT
        nonlinear = {}
        for k in u_hat.keys():
            # Simplified nonlinear term
            nonlinear[k] = -1j * k * u_hat.get(k, 0) * u_hat.get(k, 0)
        return nonlinear
    
    def compute_viscous_term(self, u_hat: Dict) -> Dict:
        """Viscous operator: L(u) = νΔu — morphism ()"""
        viscous = {}
        for k in u_hat.keys():
            k_squared = k * k
            viscous[k] = -self.nu * k_squared * u_hat.get(k, 0)
        return viscous
    
    def compute_forcing(self) -> Dict:
        """Forcing: f(k) on shell |k| ≈ k_f — morphism ()"""
        forcing = {}
        for k in self.kx:
            if abs(abs(k) - self.k_f) < 0.5:
                forcing[k] = 0.1 * (random.random() - 0.5)  # Random forcing
            else:
                forcing[k] = 0.0
        return forcing
    
    def compute_tensor_descent(self, u_hat: Dict) -> Dict:
        """Tensor descent term — morphism ()"""
        if self.eta == 0:
            return {k: 0.0 for k in u_hat.keys()}
        
        descent = {}
        for k in u_hat.keys():
            # Gradient of Lyapunov functional
            # T[u] = ∫(½|u|² + α|∇u|²)dx + γ·Ψ(u)
            k_squared = k * k
            descent[k] = -self.eta * (1.0 + self.alpha * k_squared) * u_hat.get(k, 0)
        return descent
    
    def navier_stokes_step(self, u_hat: Dict, apply_filter: bool = False, apply_descent: bool = False) -> Dict:
        """Time step: ∂_t u = Π(-u·∇u) + νΔu + f"""
        # Compute terms
        nonlinear = self.compute_nonlinear_term(u_hat)
        viscous = self.compute_viscous_term(u_hat)
        forcing = self.compute_forcing()
        
        # Sum terms
        du_dt = {}
        for k in u_hat.keys():
            du_dt[k] = nonlinear.get(k, 0) + viscous.get(k, 0) + forcing.get(k, 0)
        
        # Apply filter if requested
        if apply_filter:
            du_dt = self.apply_filter(du_dt)
        
        # Add descent term if requested
        if apply_descent:
            descent = self.compute_tensor_descent(u_hat)
            for k in du_dt.keys():
                du_dt[k] += descent.get(k, 0)
        
        # Euler step
        u_new = {}
        for k in u_hat.keys():
            u_new[k] = u_hat.get(k, 0) + self.dt * du_dt.get(k, 0)
        
        return u_new
    
    def compute_energy(self, u_hat: Dict) -> float:
        """Energy: E = ½∫|u|² — witness <>"""
        energy = 0.0
        for k, value in u_hat.items():
            energy += abs(value)**2
        return 0.5 * energy
    
    def compute_divergence(self, u_hat: Dict) -> float:
        """Check divergence: ||∇·u||_2 — witness <>"""
        # For 1D, divergence is just derivative
        divergence_norm = 0.0
        for k, value in u_hat.items():
            divergence_norm += abs(1j * k * value)**2
        return math.sqrt(divergence_norm)
    
    def compute_energy_spectrum(self, u_hat: Dict) -> Dict:
        """Energy spectrum E(k) — witness <>"""
        spectrum = {}
        for k in self.kx:
            k_abs = abs(k)
            spectrum[k_abs] = spectrum.get(k_abs, 0.0) + abs(u_hat.get(k, 0))**2
        return spectrum
    
    def run_simulation(self, T_max: float, apply_filter: bool = False, apply_descent: bool = False) -> Dict:
        """Run simulation and collect diagnostics"""
        # Initialize velocity (random initial condition)
        u_hat = {}
        for k in self.kx:
            u_hat[k] = 0.01 * (random.random() - 0.5) + 0.01j * (random.random() - 0.5)
        
        diagnostics = {
            "time": [],
            "energy": [],
            "divergence": [],
            "energy_spectrum": []
        }
        
        t = 0.0
        step = 0
        
        while t < T_max:
            # Time step
            u_hat = self.navier_stokes_step(u_hat, apply_filter, apply_descent)
            
            # Diagnostics — witness <>
            diagnostics["time"].append(t)
            diagnostics["energy"].append(self.compute_energy(u_hat))
            diagnostics["divergence"].append(self.compute_divergence(u_hat))
            
            if step % 10 == 0:  # Sample spectrum periodically
                spectrum = self.compute_energy_spectrum(u_hat)
                diagnostics["energy_spectrum"].append({
                    "time": t,
                    "spectrum": spectrum
                })
            
            t += self.dt
            step += 1
        
        return diagnostics
    
    def run_comparative_study(self, T_max: float = 1.0) -> Dict:
        """Run all four comparative runs"""
        print("=" * 70)
        print("Navier-Stokes × Tensor Descent Validation Protocol")
        print("=" * 70)
        print(f"\nConfiguration:")
        print(f"  Dimension: {self.dimension}D")
        print(f"  Grid: {self.N}×{self.N}")
        print(f"  Viscosity: ν = {self.nu}")
        print(f"  Filter: {self.filter_type}")
        print(f"  Descent: η = {self.eta}")
        print(f"  Seed: {self.seed}")
        
        results = {}
        
        # Run 1: Baseline
        print("\n" + "-" * 70)
        print("Run 1: Baseline NS (no filter, no descent)")
        print("-" * 70)
        results["baseline"] = self.run_simulation(T_max, apply_filter=False, apply_descent=False)
        
        # Run 2: NS + Φ_k
        print("\n" + "-" * 70)
        print("Run 2: NS + Φ_k filter")
        print("-" * 70)
        results["filter"] = self.run_simulation(T_max, apply_filter=True, apply_descent=False)
        
        # Run 3: NS + descent
        if self.eta > 0:
            print("\n" + "-" * 70)
            print("Run 3: NS + tensor descent")
            print("-" * 70)
            results["descent"] = self.run_simulation(T_max, apply_filter=False, apply_descent=True)
        
        # Run 4: NS + Φ_k + descent
        if self.eta > 0:
            print("\n" + "-" * 70)
            print("Run 4: NS + Φ_k + descent (full model)")
            print("-" * 70)
            results["full"] = self.run_simulation(T_max, apply_filter=True, apply_descent=True)
        
        # Comparative analysis
        print("\n" + "=" * 70)
        print("Comparative Analysis")
        print("=" * 70)
        
        for run_name, diag in results.items():
            final_energy = diag["energy"][-1] if diag["energy"] else 0.0
            max_divergence = max(diag["divergence"]) if diag["divergence"] else 0.0
            print(f"\n{run_name.capitalize()}:")
            print(f"  Final energy: {final_energy:.6e}")
            print(f"  Max divergence: {max_divergence:.6e}")
        
        # Log hyperparameters
        hyperparams = {
            "nu": self.nu,
            "eta": self.eta,
            "alpha": self.alpha,
            "gamma": self.gamma,
            "filter_type": self.filter_type,
            "filter_params": self.filter_params,
            "k_f": self.k_f,
            "dt": self.dt,
            "N": self.N,
            "seed": self.seed,
            "commit_hash": self._get_commit_hash()
        }
        
        results["hyperparameters"] = hyperparams
        
        return results
    
    def _get_commit_hash(self) -> str:
        """Get git commit hash for reproducibility"""
        try:
            import subprocess
            result = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                capture_output=True,
                text=True,
                cwd=Path(__file__).parent.parent
            )
            return result.stdout.strip()[:8] if result.returncode == 0 else "unknown"
        except:
            return "unknown"

def main():
    """Run validation protocol"""
    # Configuration
    config = {
        "dimension": 1,  # Start with 1D Burgers
        "grid_points": 64,
        "viscosity": 0.01,
        "forcing_shell": 4,
        "time_step": 0.001,
        "filter_type": "coprime",
        "filter_params": {"primorial": 30},
        "descent_eta": 0.1,
        "descent_alpha": 0.1,
        "descent_gamma": 0.01,
        "seed": 42
    }
    
    validator = NSTensorValidation(config)
    results = validator.run_comparative_study(T_max=1.0)
    
    # Save results
    output_file = Path(__file__).parent.parent / "results" / "ns_validation_results.json"
    output_file.parent.mkdir(exist_ok=True)
    
    # Convert complex numbers to lists for JSON
    json_results = json.dumps(results, indent=2, default=str)
    output_file.write_text(json_results)
    
    print(f"\n✓ Results saved to: {output_file}")
    print("\n" + "=" * 70)
    print("Key Insight:")
    print("=" * 70)
    print("""
This is a falsifiable experiment — no grand claims:
• Arithmetic filters are modeling choices, not theorems
• Tensor descent is a regularization term, not a proof
• Results are numerical observations, not mathematical proofs

Compare runs to see measurable effects on:
• Stability (higher Re before crash)
• Spectral structure (arithmetic fingerprints)
• Energy budget (explicit term accounting)
    """)

if __name__ == "__main__":
    main()


