#!/usr/bin/env python3
"""
3D Periodic Flow — Clean Navier-Stokes with Arithmetic Mask & Descent
Goal: Measure spectra, invariants, stability — no grand claims
"""

import math
import cmath
import random
import json
from pathlib import Path
from typing import List, Dict, Tuple, Optional, Any
import numpy as np

class NS3DFlow:
    """
    Clean 3D periodic flow simulator
    Grid: N³ periodic, double precision
    State: Velocity u(x,t) ∈ ℝ³
    """
    
    def __init__(self, N: int = 64, nu: float = 0.01, k_f: float = 2.0, 
                 dt: Optional[float] = None, cfl: float = 0.5,
                 mask_type: Optional[str] = None, descent_enabled: bool = False,
                 alpha_grad: float = 0.01, eta_descent: float = 0.1):
        self.N = N
        self.nu = nu  # Viscosity
        self.k_f = k_f  # Forcing wavenumber
        self.cfl = cfl
        self.mask_type = mask_type  # "coprime", "von_mangoldt", "prime_shell", None
        self.descent_enabled = descent_enabled
        self.alpha_grad = alpha_grad
        self.eta_descent = eta_descent
        
        # Grid spacing
        self.dx = 2 * math.pi / N
        self.L = 2 * math.pi
        
        # Time step (CFL-limited if not provided)
        self.dt = dt if dt is not None else self._compute_cfl_dt(None)
        
        # Initialize k-space grid
        self.kx, self.ky, self.kz = self._init_k_grid()
        self.k_squared = self.kx**2 + self.ky**2 + self.kz**2
        
        # Forcing seed
        self.forcing_seed = 42
        random.seed(self.forcing_seed)
        
        # Diagnostics
        self.diagnostics = []
    
    def _init_k_grid(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Initialize k-space grid"""
        k = np.arange(self.N)
        k[k > self.N // 2] -= self.N  # Shift to [-N/2, N/2]
        
        kx = np.zeros((self.N, self.N, self.N))
        ky = np.zeros((self.N, self.N, self.N))
        kz = np.zeros((self.N, self.N, self.N))
        
        for i in range(self.N):
            for j in range(self.N):
                for k_idx in range(self.N):
                    kx[i, j, k_idx] = k[i]
                    ky[i, j, k_idx] = k[j]
                    kz[i, j, k_idx] = k[k_idx]
        
        return kx, ky, kz
    
    def _compute_cfl_dt(self, u: Optional[np.ndarray]) -> float:
        """CFL-limited time step: dt = CFL * min(Δx / max|u|)"""
        if u is None:
            return 0.01  # Default
        
        u_mag = np.sqrt(np.sum(u**2, axis=0))
        u_max = np.max(u_mag)
        
        if u_max == 0:
            return 0.01
        
        dt_cfl = self.cfl * self.dx / u_max
        return min(dt_cfl, 0.01)  # Cap at 0.01
    
    def project_helmholtz_leray(self, u_hat: np.ndarray) -> np.ndarray:
        """
        Projection: enforce incompressibility
        Π̂u(k) = û(k) - k(k·û(k))/|k|² for k≠0
        """
        u_proj = u_hat.copy()
        
        # k·û(k)
        k_dot_u = (self.kx * u_hat[0] + self.ky * u_hat[1] + self.kz * u_hat[2])
        
        # k(k·û(k))
        k_times_scalar = np.zeros_like(u_hat)
        k_times_scalar[0] = self.kx * k_dot_u
        k_times_scalar[1] = self.ky * k_dot_u
        k_times_scalar[2] = self.kz * k_dot_u
        
        # Divide by |k|² (handle k=0)
        k_sq_safe = np.where(self.k_squared > 1e-12, self.k_squared, 1.0)
        k_times_scalar /= k_sq_safe
        
        # Subtract: û - k(k·û)/|k|²
        u_proj -= k_times_scalar
        
        # Set k=0 to zero (mean flow)
        u_proj[:, self.N//2, self.N//2, self.N//2] = 0.0
        
        return u_proj
    
    def fft3d(self, u: np.ndarray) -> np.ndarray:
        """3D FFT with unitary normalization"""
        if u.ndim == 3:
            # Single 3D field: axes=(0, 1, 2)
            u_hat = np.fft.fftn(u, axes=(0, 1, 2)) / (self.N ** 1.5)
        else:
            # 4D field (3 components): axes=(1, 2, 3)
            u_hat = np.fft.fftn(u, axes=(1, 2, 3)) / (self.N ** 1.5)
        return u_hat
    
    def ifft3d(self, u_hat: np.ndarray) -> np.ndarray:
        """3D IFFT with unitary normalization"""
        if u_hat.ndim == 3:
            # Single 3D field: axes=(0, 1, 2)
            u = np.fft.ifftn(u_hat, axes=(0, 1, 2)) * (self.N ** 1.5)
        else:
            # 4D field (3 components): axes=(1, 2, 3)
            u = np.fft.ifftn(u_hat, axes=(1, 2, 3)) * (self.N ** 1.5)
        return np.real(u)
    
    def nonlinearity(self, u: np.ndarray) -> np.ndarray:
        """
        Nonlinearity: N(u) = Π(-u·∇u)
        Pseudospectral: compute in x-space, FFT back
        """
        # Compute gradient in Fourier space
        u_hat = self.fft3d(u)
        
        # ∇u components
        grad_u = np.zeros((3, 3, self.N, self.N, self.N), dtype=complex)
        grad_u[0, 0] = 1j * self.kx * u_hat[0]  # ∂u_x/∂x
        grad_u[0, 1] = 1j * self.ky * u_hat[0]  # ∂u_x/∂y
        grad_u[0, 2] = 1j * self.kz * u_hat[0]  # ∂u_x/∂z
        grad_u[1, 0] = 1j * self.kx * u_hat[1]  # ∂u_y/∂x
        grad_u[1, 1] = 1j * self.ky * u_hat[1]  # ∂u_y/∂y
        grad_u[1, 2] = 1j * self.kz * u_hat[1]  # ∂u_y/∂z
        grad_u[2, 0] = 1j * self.kx * u_hat[2]  # ∂u_z/∂x
        grad_u[2, 1] = 1j * self.ky * u_hat[2]  # ∂u_z/∂y
        grad_u[2, 2] = 1j * self.kz * u_hat[2]  # ∂u_z/∂z
        
        # Transform to x-space
        grad_u_x = np.zeros((3, 3, self.N, self.N, self.N))
        for i in range(3):
            for j in range(3):
                # grad_u[i, j] is 3D, so ifft3d will use axes=(0,1,2)
                grad_u_x[i, j] = self.ifft3d(grad_u[i, j])
        
        # u·∇u in x-space
        u_dot_grad_u = np.zeros((3, self.N, self.N, self.N))
        for i in range(3):
            for j in range(3):
                u_dot_grad_u[i] += u[j] * grad_u_x[j, i]
        
        # -u·∇u
        neg_u_dot_grad_u = -u_dot_grad_u
        
        # FFT back to k-space
        neg_u_dot_grad_u_hat = self.fft3d(neg_u_dot_grad_u)
        
        # Project to enforce incompressibility
        N_hat = self.project_helmholtz_leray(neg_u_dot_grad_u_hat)
        
        return N_hat
    
    def viscosity(self, u_hat: np.ndarray) -> np.ndarray:
        """
        Viscosity: L(u) = νΔu → in k-space multiply by -ν|k|²
        """
        L_hat = -self.nu * self.k_squared * u_hat
        return L_hat
    
    def forcing(self) -> np.ndarray:
        """
        Forcing: narrow shell |k| ≈ k_f, divergence-free, fixed seed
        """
        random.seed(self.forcing_seed)
        f_hat = np.zeros((3, self.N, self.N, self.N), dtype=complex)
        
        # Generate forcing in narrow shell
        k_mag = np.sqrt(self.k_squared)
        shell_width = 0.5
        
        for i in range(self.N):
            for j in range(self.N):
                for k_idx in range(self.N):
                    k_m = k_mag[i, j, k_idx]
                    if abs(k_m - self.k_f) < shell_width and k_m > 0:
                        # Random phase
                        phase = random.uniform(0, 2 * math.pi)
                        amp = 0.1
                        
                        # Divergence-free: f ⊥ k
                        # Random direction perpendicular to k
                        k_vec = np.array([self.kx[i, j, k_idx], 
                                         self.ky[i, j, k_idx], 
                                         self.kz[i, j, k_idx]])
                        k_norm = np.linalg.norm(k_vec)
                        
                        if k_norm > 1e-12:
                            # Random vector
                            f_vec = np.array([random.gauss(0, 1), 
                                            random.gauss(0, 1), 
                                            random.gauss(0, 1)])
                            # Project out k component
                            f_vec -= np.dot(f_vec, k_vec) / k_norm**2 * k_vec
                            f_vec /= np.linalg.norm(f_vec) + 1e-12
                            
                            f_hat[:, i, j, k_idx] = amp * np.exp(1j * phase) * f_vec
        
        return f_hat
    
    def apply_arithmetic_mask(self, u_hat: np.ndarray) -> np.ndarray:
        """Apply arithmetic mask M(k) multiplicatively"""
        if self.mask_type is None:
            return u_hat
        
        mask = np.ones_like(u_hat)
        
        if self.mask_type == "coprime":
            # Coprime-to-primorial mask
            primorial_p = 5  # 5# = 30
            for i in range(self.N):
                for j in range(self.N):
                    for k_idx in range(self.N):
                        k_m = int(np.sqrt(self.k_squared[i, j, k_idx]))
                        if k_m > 0 and math.gcd(k_m, primorial_p) == 1:
                            mask[:, i, j, k_idx] = 1.0
                        else:
                            mask[:, i, j, k_idx] = 0.0
        
        elif self.mask_type == "von_mangoldt":
            # Von Mangoldt weight
            alpha = 0.1
            for i in range(self.N):
                for j in range(self.N):
                    for k_idx in range(self.N):
                        k_m = int(np.sqrt(self.k_squared[i, j, k_idx]))
                        if k_m > 1:
                            # Simplified von Mangoldt weight
                            weight = alpha * math.log(k_m) if self._is_prime_power(k_m) else alpha
                            mask[:, i, j, k_idx] = weight
        
        elif self.mask_type == "prime_shell":
            # Prime shell window
            p_max = 10
            beta = 0.1
            for i in range(self.N):
                for j in range(self.N):
                    for k_idx in range(self.N):
                        k_m = int(np.sqrt(self.k_squared[i, j, k_idx]))
                        if self._is_prime(k_m) and k_m <= p_max:
                            mask[:, i, j, k_idx] = 1.0
                        else:
                            mask[:, i, j, k_idx] = beta
        
        return u_hat * mask
    
    def _is_prime(self, n: int) -> bool:
        """Check if n is prime"""
        if n < 2:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True
    
    def _is_prime_power(self, n: int) -> bool:
        """Check if n is a prime power"""
        if n < 2:
            return False
        for p in range(2, int(math.sqrt(n)) + 1):
            if self._is_prime(p):
                power = p
                while power < n:
                    power *= p
                if power == n:
                    return True
        return self._is_prime(n)
    
    def descent_term(self, u: np.ndarray) -> np.ndarray:
        """
        Descent term: gradient flow of T[u] = ½||u||² + α||∇u||²
        Add -ηΠ(u - αΔu)
        """
        u_hat = self.fft3d(u)
        
        # αΔu in k-space
        alpha_laplacian_u = -self.alpha_grad * self.k_squared * u_hat
        
        # u - αΔu
        u_minus_alpha_delta_u_hat = u_hat - alpha_laplacian_u
        
        # Project
        projected_hat = self.project_helmholtz_leray(u_minus_alpha_delta_u_hat)
        
        # -ηΠ(u - αΔu)
        descent_hat = -self.eta_descent * projected_hat
        
        return descent_hat
    
    def rk4_step(self, u: np.ndarray) -> np.ndarray:
        """RK4 time stepping"""
        u_hat = self.fft3d(u)
        
        # k1 = rhs(u)
        k1_hat = self.rhs(u_hat, u)
        
        # k2 = rhs(u + dt/2 * k1)
        u2_hat = u_hat + 0.5 * self.dt * k1_hat
        u2 = self.ifft3d(u2_hat)
        k2_hat = self.rhs(u2_hat, u2)
        
        # k3 = rhs(u + dt/2 * k2)
        u3_hat = u_hat + 0.5 * self.dt * k2_hat
        u3 = self.ifft3d(u3_hat)
        k3_hat = self.rhs(u3_hat, u3)
        
        # k4 = rhs(u + dt * k3)
        u4_hat = u_hat + self.dt * k3_hat
        u4 = self.ifft3d(u4_hat)
        k4_hat = self.rhs(u4_hat, u4)
        
        # Combine: u_new = u + dt/6 * (k1 + 2*k2 + 2*k3 + k4)
        u_new_hat = u_hat + self.dt / 6.0 * (k1_hat + 2*k2_hat + 2*k3_hat + k4_hat)
        u_new = self.ifft3d(u_new_hat)
        
        return u_new
    
    def rhs(self, u_hat: np.ndarray, u: np.ndarray) -> np.ndarray:
        """Right-hand side: N(u) + L(u) + F + descent"""
        # Nonlinearity
        N_hat = self.nonlinearity(u)
        
        # Viscosity
        L_hat = self.viscosity(u_hat)
        
        # Forcing
        F_hat = self.forcing()
        
        # Combine
        rhs_hat = N_hat + L_hat + F_hat
        
        # Apply arithmetic mask
        rhs_hat = self.apply_arithmetic_mask(rhs_hat)
        
        # Descent term
        if self.descent_enabled:
            D_hat = self.descent_term(u)
            rhs_hat += D_hat
        
        return rhs_hat
    
    def compute_divergence(self, u: np.ndarray) -> float:
        """Compute divergence: ||∇·u||₂"""
        u_hat = self.fft3d(u)
        
        # ∇·u = i(kx*u_x + ky*u_y + kz*u_z)
        div_hat = 1j * (self.kx * u_hat[0] + self.ky * u_hat[1] + self.kz * u_hat[2])
        div = self.ifft3d(div_hat)
        
        div_norm = np.sqrt(np.mean(div**2))
        return float(div_norm)
    
    def compute_energy(self, u: np.ndarray) -> float:
        """Energy: E = ½⟨|u|²⟩"""
        u_mag_sq = np.sum(u**2, axis=0)
        E = 0.5 * np.mean(u_mag_sq)
        return float(E)
    
    def compute_spectrum(self, u: np.ndarray) -> Dict[str, Any]:
        """Compute energy spectrum E(k) shell-averaged"""
        u_hat = self.fft3d(u)
        
        # Energy in k-space
        E_k_hat = 0.5 * np.sum(np.abs(u_hat)**2, axis=0)
        
        # Shell-average
        k_mag = np.sqrt(self.k_squared)
        k_max = int(np.max(k_mag))
        
        E_k = np.zeros(k_max + 1)
        k_counts = np.zeros(k_max + 1)
        
        for i in range(self.N):
            for j in range(self.N):
                for k_idx in range(self.N):
                    k_m = int(k_mag[i, j, k_idx])
                    if k_m <= k_max:
                        E_k[k_m] += E_k_hat[i, j, k_idx]
                        k_counts[k_m] += 1
        
        # Average
        for k in range(k_max + 1):
            if k_counts[k] > 0:
                E_k[k] /= k_counts[k]
        
        return {
            "E_k": E_k.tolist(),
            "k_values": list(range(k_max + 1))
        }
    
    def compute_flatness(self, u: np.ndarray) -> float:
        """Compute flatness of vorticity components"""
        u_hat = self.fft3d(u)
        
        # Vorticity: ω = ∇ × u
        omega_hat = np.zeros_like(u_hat)
        omega_hat[0] = 1j * (self.ky * u_hat[2] - self.kz * u_hat[1])
        omega_hat[1] = 1j * (self.kz * u_hat[0] - self.kx * u_hat[2])
        omega_hat[2] = 1j * (self.kx * u_hat[1] - self.ky * u_hat[0])
        
        omega = self.ifft3d(omega_hat)
        
        # Flatten to 1D
        omega_flat = omega.flatten()
        
        # Compute moments
        mean_omega = np.mean(omega_flat)
        std_omega = np.std(omega_flat)
        
        if std_omega == 0:
            return 0.0
        
        # Fourth moment
        fourth_moment = np.mean((omega_flat - mean_omega)**4)
        
        # Flatness: F = ⟨ω⁴⟩ / ⟨ω²⟩²
        flatness = fourth_moment / (std_omega**4)
        
        return float(flatness)
    
    def parseval_check(self, u: np.ndarray) -> Dict[str, float]:
        """Parseval check: energy conservation"""
        u_hat = self.fft3d(u)
        
        # Energy in x-space
        E_x = 0.5 * np.mean(np.sum(u**2, axis=0))
        
        # Energy in k-space
        E_k = 0.5 * np.mean(np.sum(np.abs(u_hat)**2, axis=0))
        
        diff = abs(E_x - E_k)
        rel_error = diff / max(E_x, E_k, 1e-20)
        
        return {
            "E_x": float(E_x),
            "E_k": float(E_k),
            "difference": float(diff),
            "relative_error": float(rel_error)
        }
    
    def simulate(self, n_steps: int, u0: Optional[np.ndarray] = None) -> Dict[str, Any]:
        """Run simulation"""
        # Initialize velocity field
        if u0 is None:
            u0 = np.random.randn(3, self.N, self.N, self.N) * 0.1
            u0_hat = self.fft3d(u0)
            u0 = self.ifft3d(self.project_helmholtz_leray(u0_hat))
        
        u = u0.copy()
        
        # Run simulation
        for step in range(n_steps):
            # Update CFL-limited dt
            self.dt = self._compute_cfl_dt(u)
            
            # Time step
            u = self.rk4_step(u)
            
            # Diagnostics
            if step % 10 == 0:
                div = self.compute_divergence(u)
                E = self.compute_energy(u)
                flatness = self.compute_flatness(u)
                parseval = self.parseval_check(u)
                
                self.diagnostics.append({
                    "step": step,
                    "time": step * self.dt,
                    "divergence": div,
                    "energy": E,
                    "flatness": flatness,
                    "parseval": parseval
                })
        
        # Final spectrum
        spectrum = self.compute_spectrum(u)
        
        return {
            "final_state": u.tolist(),
            "diagnostics": self.diagnostics,
            "spectrum": spectrum,
            "config": {
                "N": self.N,
                "nu": self.nu,
                "k_f": self.k_f,
                "dt": self.dt,
                "mask_type": self.mask_type,
                "descent_enabled": self.descent_enabled
            }
        }

def main():
    """Run 3D flow simulation"""
    import argparse
    
    parser = argparse.ArgumentParser(description="3D Periodic Flow Simulation")
    parser.add_argument("--N", type=int, default=64, help="Grid size N³")
    parser.add_argument("--nu", type=float, default=0.01, help="Viscosity")
    parser.add_argument("--k_f", type=float, default=2.0, help="Forcing wavenumber")
    parser.add_argument("--steps", type=int, default=100, help="Number of time steps")
    parser.add_argument("--mask", type=str, choices=["coprime", "von_mangoldt", "prime_shell"], 
                       help="Arithmetic mask type")
    parser.add_argument("--descent", action="store_true", help="Enable descent term")
    parser.add_argument("--output", type=str, default="results/ns_3d_flow.json", help="Output file")
    
    args = parser.parse_args()
    
    # Create simulator
    sim = NS3DFlow(N=args.N, nu=args.nu, k_f=args.k_f,
                   mask_type=args.mask, descent_enabled=args.descent)
    
    # Run simulation
    print(f"Running 3D flow simulation: N={args.N}, steps={args.steps}")
    print(f"  Mask: {args.mask or 'none'}")
    print(f"  Descent: {args.descent}")
    
    results = sim.simulate(args.steps)
    
    # Save results
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n✓ Simulation complete")
    print(f"  Final divergence: {results['diagnostics'][-1]['divergence']:.2e}")
    print(f"  Final energy: {results['diagnostics'][-1]['energy']:.6f}")
    print(f"  Final flatness: {results['diagnostics'][-1]['flatness']:.4f}")
    print(f"  Parseval error: {results['diagnostics'][-1]['parseval']['relative_error']:.2e}")
    print(f"  Results saved to: {output_path}")

if __name__ == "__main__":
    main()

