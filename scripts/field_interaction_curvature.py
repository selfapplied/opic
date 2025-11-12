#!/usr/bin/env .venv/bin/python
"""
Field Interaction: Computational Curvature
Couple ζ-field and NP-field, measure curvature via Fisher metric
"""

import json
import math
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple

def zeta_field_evolution(z: np.ndarray, H: np.ndarray, dt: float) -> np.ndarray:
    """ζ-field: linear unitary ẋ = iHz"""
    # Simplified: z' = z + i*H*z*dt
    return z + 1j * H @ z * dt

def np_field_evolution(x: np.ndarray, V_grad: np.ndarray, noise: np.ndarray, dt: float) -> np.ndarray:
    """NP-field: dissipative search ẋ = -∇V(x) + noise"""
    # Simplified: x' = x - ∇V*dt + noise*dt
    return x - V_grad * dt + noise * dt

def coupled_evolution(z: np.ndarray, x: np.ndarray, H: np.ndarray, V_grad: np.ndarray,
                     C_zx: np.ndarray, C_xz: np.ndarray, epsilon: float, dt: float,
                     noise: np.ndarray = None) -> Tuple[np.ndarray, np.ndarray]:
    """Coupled evolution: ẋ += ε C_xz Re(z), ż += ε C_zx x"""
    if noise is None:
        noise = np.zeros_like(x)
    
    # ζ-field evolution
    dz_dt = 1j * H @ z + epsilon * C_zx @ x
    z_new = z + dz_dt * dt
    
    # NP-field evolution
    dx_dt = -V_grad + noise + epsilon * C_xz @ np.real(z)
    x_new = x + dx_dt * dt
    
    return z_new, x_new

def compute_lyapunov_exponents(trajectory: np.ndarray, dt: float) -> np.ndarray:
    """Compute Lyapunov exponents from trajectory"""
    # Simplified: use eigenvalues of Jacobian
    # In real version, use QR decomposition of tangent map
    n = trajectory.shape[1]
    jacobian = np.eye(n)  # Placeholder
    eigenvalues = np.real(np.linalg.eigvals(jacobian))
    lyapunov = eigenvalues / dt if dt > 0 else eigenvalues
    return lyapunov

def transfer_entropy(x_history: np.ndarray, z_history: np.ndarray, lag: int = 1) -> float:
    """Transfer entropy T_{z→x}"""
    # Simplified: mutual information I(x_{t+lag}; z_t | x_t)
    # In real version, use proper information-theoretic computation
    if len(x_history) < lag + 1:
        return 0.0
    
    # Placeholder: simplified mutual information proxy
    x_future = x_history[lag:]
    x_past = x_history[:-lag]
    z_past = z_history[:-lag]
    
    # Simplified correlation-based proxy
    correlation = np.corrcoef(x_future.flatten(), z_past.flatten())[0, 1]
    te = abs(correlation) * 0.1  # Placeholder scaling
    
    return float(te)

def spectral_kl_divergence(E_k_coupled: np.ndarray, E_k_solo: np.ndarray) -> float:
    """Spectral KL divergence D_KL(E(k)_coupled || E(k)_solo)"""
    # Normalize to probabilities
    E_k_coupled_norm = E_k_coupled / (np.sum(E_k_coupled) + 1e-10)
    E_k_solo_norm = E_k_solo / (np.sum(E_k_solo) + 1e-10)
    
    # KL divergence
    kl = np.sum(E_k_coupled_norm * np.log(E_k_coupled_norm / (E_k_solo_norm + 1e-10) + 1e-10))
    
    return float(kl)

def compute_fisher_metric(decoder_likelihood, theta: np.ndarray) -> np.ndarray:
    """Compute Fisher metric g_ij = E[∂² log p_θ / ∂θ_i ∂θ_j]"""
    # Simplified: use Hessian of log-likelihood
    # In real version, compute expected value over data
    n = len(theta)
    hessian = np.eye(n) * 0.1  # Placeholder
    fisher_metric = -hessian  # Fisher = -Hessian of log-likelihood
    return fisher_metric

def compute_scalar_curvature(fisher_metric: np.ndarray) -> float:
    """Compute scalar curvature R from Fisher metric"""
    # Simplified: use determinant or trace
    # In real version, compute Ricci scalar
    det_g = np.linalg.det(fisher_metric)
    if det_g <= 0:
        return 0.0
    
    # Placeholder: scalar curvature proxy
    R = 1.0 / (det_g + 1e-10)
    return float(R)

def run_interaction_experiment(epsilon_values: List[float], n_steps: int = 100) -> Dict:
    """Run interaction experiment: vary coupling ε"""
    n_dim = 10
    
    # Initialize fields
    z = np.random.randn(n_dim) + 1j * np.random.randn(n_dim)
    x = np.random.randn(n_dim)
    
    # Operators
    H = np.eye(n_dim)  # Hermitian operator for ζ-field
    V_grad = x * 0.1  # Gradient of potential for NP-field
    C_zx = np.eye(n_dim) * 0.1  # Coupling matrix
    C_xz = np.eye(n_dim) * 0.1
    
    dt = 0.01
    
    results = []
    
    for epsilon in epsilon_values:
        # Evolve coupled system
        z_history = [z.copy()]
        x_history = [x.copy()]
        
        for step in range(n_steps):
            noise = np.random.randn(n_dim) * 0.01
            z, x = coupled_evolution(z, x, H, V_grad, C_zx, C_xz, epsilon, dt, noise)
            z_history.append(z.copy())
            x_history.append(x.copy())
        
        z_history = np.array(z_history)
        x_history = np.array(x_history)
        
        # Compute metrics
        lyapunov = compute_lyapunov_exponents(x_history, dt)
        te_zx = transfer_entropy(x_history, z_history)
        te_xz = transfer_entropy(z_history, x_history)
        
        # Spectral KL (simplified)
        E_k_coupled = np.abs(z_history[-1])**2
        E_k_solo = np.abs(z_history[0])**2
        kl_div = spectral_kl_divergence(E_k_coupled, E_k_solo)
        
        # Curvature (simplified)
        theta = np.concatenate([np.real(z_history[-1]), x_history[-1]])
        fisher_metric = compute_fisher_metric(None, theta)
        curvature = compute_scalar_curvature(fisher_metric)
        
        results.append({
            "epsilon": epsilon,
            "lyapunov_max": float(np.max(lyapunov)),
            "transfer_entropy_zx": te_zx,
            "transfer_entropy_xz": te_xz,
            "spectral_kl": kl_div,
            "curvature": curvature
        })
    
    return {"results": results}

def main():
    print("=" * 60)
    print("Field Interaction: Computational Curvature")
    print("=" * 60)
    
    epsilon_values = [0.0, 0.01, 0.02, 0.05, 0.1, 0.2]
    n_steps = 100
    
    print(f"\nConfiguration:")
    print(f"  ε values: {epsilon_values}")
    print(f"  Steps: {n_steps}")
    
    print("\nRunning interaction experiment...")
    results = run_interaction_experiment(epsilon_values, n_steps)
    
    print("\nResults:")
    for res in results["results"]:
        print(f"  ε={res['epsilon']:.3f}: "
              f"λ_max={res['lyapunov_max']:.4f}, "
              f"T_z→x={res['transfer_entropy_zx']:.4f}, "
              f"KL={res['spectral_kl']:.4f}, "
              f"R={res['curvature']:.4f}")
    
    # Save results
    output_path = Path('results/field_interaction_curvature.json')
    output_path.parent.mkdir(exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n✓ Results saved to {output_path}")

if __name__ == "__main__":
    main()

