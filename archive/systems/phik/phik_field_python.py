#!.venv/bin/python
"""
phik_field_python.py — Reference Python implementation of stabilizing Φκ-field

This is a clean-room implementation of the Φκ-field construction,
following the mathematical specification exactly.

Requires: numpy (pip install numpy)
"""

import sys
import os

# Ensure we can import numpy
try:
    import numpy as np
except ImportError:
    print("Error: numpy is required. Install with: pip install numpy", file=sys.stderr)
    print(f"Python executable: {sys.executable}", file=sys.stderr)
    print(f"Python path: {sys.path}", file=sys.stderr)
    sys.exit(1)

from typing import Tuple, Dict, Optional
from dataclasses import dataclass


@dataclass
class PhikField:
    """Stabilizing Φκ-field structure"""
    I: np.ndarray  # Intensity
    A: np.ndarray  # Alignment
    C: np.ndarray  # Chroma (categorical channels)
    alpha: np.ndarray  # Gradient magnitude
    Phi_kappa: np.ndarray  # Field potential
    kappa: Dict[str, float]  # Weights
    x_0: Tuple[int, int]  # Reference point


class PhikFieldBuilder:
    """Step-by-step construction of Φκ-field"""
    
    def __init__(self, H: int, W: int):
        """Initialize domain Ω ⊂ ℤ²"""
        self.H = H
        self.W = W
        self.domain_shape = (H, W)
    
    # ========================================================================
    # 1. DOMAIN Ω
    # ========================================================================
    
    def create_domain(self) -> np.ndarray:
        """Create empty domain grid"""
        return np.zeros(self.domain_shape, dtype=np.float64)
    
    # ========================================================================
    # 2. FOUR BASE CHANNELS
    # ========================================================================
    
    def init_intensity(self, source: Optional[np.ndarray] = None) -> np.ndarray:
        """Initialize intensity channel I(x)"""
        if source is not None:
            return source.astype(np.float64)
        # Synthetic: noise or pattern
        return np.random.randn(self.H, self.W)
    
    def compute_gradient_orientation(self, I: np.ndarray) -> np.ndarray:
        """Compute alignment A(x) = gradient orientation of I"""
        # Discrete gradient
        gx = np.zeros_like(I)
        gy = np.zeros_like(I)
        
        # gx = I[2:,1:-1] - I[:-2,1:-1]
        gx[1:-1, 1:-1] = I[2:, 1:-1] - I[:-2, 1:-1]
        
        # gy = I[1:-1,2:] - I[1:-1,:-2]
        gy[1:-1, 1:-1] = I[1:-1, 2:] - I[1:-1, :-2]
        
        # Orientation: atan2(gy, gx)
        A = np.arctan2(gy, gx)
        return A
    
    def init_chroma(self, num_channels: int = 3) -> np.ndarray:
        """Initialize chroma/categorical channels C(x)"""
        return np.random.rand(self.H, self.W, num_channels)
    
    def compute_gradient_magnitude(self, I: np.ndarray) -> np.ndarray:
        """Compute gradient magnitude α(x) = |∇I|"""
        gx = np.zeros_like(I)
        gy = np.zeros_like(I)
        
        gx[1:-1, 1:-1] = I[2:, 1:-1] - I[:-2, 1:-1]
        gy[1:-1, 1:-1] = I[1:-1, 2:] - I[1:-1, :-2]
        
        # α = sqrt(gx² + gy²)
        alpha = np.sqrt(gx**2 + gy**2)
        return alpha
    
    def init_channels(self, source: Optional[np.ndarray] = None) -> Dict[str, np.ndarray]:
        """Initialize all four base channels"""
        I = self.init_intensity(source)
        A = self.compute_gradient_orientation(I)
        C = self.init_chroma()
        alpha = self.compute_gradient_magnitude(I)
        
        return {
            'I': I,
            'A': A,
            'C': C,
            'alpha': alpha
        }
    
    # ========================================================================
    # 3. FIELD CONSTRUCTION
    # ========================================================================
    
    def manhattan_distance(self, x: Tuple[int, int], x_0: Tuple[int, int]) -> float:
        """Manhattan distance d₁(x, x₀)"""
        return abs(x[0] - x_0[0]) + abs(x[1] - x_0[1])
    
    def compute_field(
        self,
        I: np.ndarray,
        A: np.ndarray,
        alpha: np.ndarray,
        x_0: Tuple[int, int],
        kappa: Dict[str, float]
    ) -> np.ndarray:
        """
        Compute Φκ(x) = κ₁I(x) + κ₂A(x) - κ₃d₁(x,x₀) + κ₄α(x)
        """
        H, W = I.shape
        Phi_kappa = np.zeros((H, W), dtype=np.float64)
        
        # Build distance field
        d_field = np.zeros((H, W), dtype=np.float64)
        for i in range(H):
            for j in range(W):
                d_field[i, j] = self.manhattan_distance((i, j), x_0)
        
        # Combine terms
        Phi_kappa = (
            kappa['kappa_1'] * I +
            kappa['kappa_2'] * A -
            kappa['kappa_3'] * d_field +
            kappa['kappa_4'] * alpha
        )
        
        return Phi_kappa
    
    # ========================================================================
    # 4. DERIVE FLOWS (Stability Dynamics)
    # ========================================================================
    
    def compute_alignment(self, Phi_kappa: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """A(x) = ∇Φκ(x)"""
        gx = np.zeros_like(Phi_kappa)
        gy = np.zeros_like(Phi_kappa)
        
        gx[1:-1, 1:-1] = Phi_kappa[2:, 1:-1] - Phi_kappa[:-2, 1:-1]
        gy[1:-1, 1:-1] = Phi_kappa[1:-1, 2:] - Phi_kappa[1:-1, :-2]
        
        return gx, gy
    
    def compute_momentum(self, A: Tuple[np.ndarray, np.ndarray], 
                        A_prev: Optional[Tuple[np.ndarray, np.ndarray]]) -> Tuple[np.ndarray, np.ndarray]:
        """M(x) = ∂ₜA(x) = A - A_prev"""
        if A_prev is None:
            return (np.zeros_like(A[0]), np.zeros_like(A[1]))
        return (A[0] - A_prev[0], A[1] - A_prev[1])
    
    def compute_kinetics(self, Phi_kappa: np.ndarray, Phi_kappa_prev: Optional[np.ndarray]) -> np.ndarray:
        """K(x) = dΦκ/dt = Φκ - Φκ_prev"""
        if Phi_kappa_prev is None:
            return np.zeros_like(Phi_kappa)
        return Phi_kappa - Phi_kappa_prev
    
    def compute_charge(self, Phi_kappa: np.ndarray) -> np.ndarray:
        """Q(x) = ∇·A = ∇²Φκ(x)"""
        # Discrete Laplacian
        laplacian = np.zeros_like(Phi_kappa)
        laplacian[1:-1, 1:-1] = (
            Phi_kappa[2:, 1:-1] +
            Phi_kappa[:-2, 1:-1] +
            Phi_kappa[1:-1, 2:] +
            Phi_kappa[1:-1, :-2] -
            4 * Phi_kappa[1:-1, 1:-1]
        )
        return laplacian
    
    # ========================================================================
    # 5. STABILITY CONDITION
    # ========================================================================
    
    def check_stability(
        self,
        M: Tuple[np.ndarray, np.ndarray],
        K: np.ndarray,
        Q: np.ndarray,
        epsilon: float = 1e-6
    ) -> Dict[str, bool]:
        """Check if field has stabilized"""
        # Momentum stability: |M|.mean() < ε
        M_mag = np.sqrt(M[0]**2 + M[1]**2)
        momentum_stable = np.mean(np.abs(M_mag)) < epsilon
        
        # Kinetics stability: |K|.mean() < ε
        kinetics_stable = np.mean(np.abs(K)) < epsilon
        
        # Charge sign consistency
        Q_sign = np.sign(Q)
        sign_changes = np.sum(np.abs(np.diff(Q_sign, axis=0))) + np.sum(np.abs(np.diff(Q_sign, axis=1)))
        charge_stable = sign_changes < Q.size * 0.1  # Less than 10% sign changes
        
        return {
            'momentum_stable': momentum_stable,
            'kinetics_stable': kinetics_stable,
            'charge_stable': charge_stable,
            'is_stable': momentum_stable and kinetics_stable and charge_stable
        }
    
    # ========================================================================
    # 6. EVOLUTION
    # ========================================================================
    
    def evolve(
        self,
        I: np.ndarray,
        Phi_kappa: np.ndarray,
        Q: np.ndarray,
        eta: float = 0.01
    ) -> np.ndarray:
        """Evolve intensity: I = I + ηQ (self-healing potential)"""
        return I + eta * Q
    
    # ========================================================================
    # 7. COMPLETE FIELD CONSTRUCTION
    # ========================================================================
    
    def build_field(
        self,
        source: Optional[np.ndarray] = None,
        kappa: Optional[Dict[str, float]] = None,
        x_0: Optional[Tuple[int, int]] = None
    ) -> PhikField:
        """Complete field construction"""
        # Default kappa weights (stability condition: all > 0)
        if kappa is None:
            kappa = {
                'kappa_1': 1.0,  # Structure
                'kappa_2': 0.5,  # Flow
                'kappa_3': 0.1,  # Anchoring
                'kappa_4': 0.8   # Edges
            }
        
        # Default reference point (center)
        if x_0 is None:
            x_0 = (self.H // 2, self.W // 2)
        
        # Initialize channels
        channels = self.init_channels(source)
        I = channels['I']
        A = channels['A']
        C = channels['C']
        alpha = channels['alpha']
        
        # Compute field
        Phi_kappa = self.compute_field(I, A, alpha, x_0, kappa)
        
        return PhikField(
            I=I,
            A=A,
            C=C,
            alpha=alpha,
            Phi_kappa=Phi_kappa,
            kappa=kappa,
            x_0=x_0
        )


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == '__main__':
    # Create field
    builder = PhikFieldBuilder(H=64, W=64)
    field = builder.build_field()
    
    # Compute flows
    A = builder.compute_alignment(field.Phi_kappa)
    Q = builder.compute_charge(field.Phi_kappa)
    K = builder.compute_kinetics(field.Phi_kappa, None)
    M = builder.compute_momentum(A, None)
    
    # Check stability
    stability = builder.check_stability(M, K, Q)
    
    print("Φκ-Field Construction Complete")
    print(f"Field shape: {field.Phi_kappa.shape}")
    print(f"Stability: {stability['is_stable']}")
    print(f"  Momentum stable: {stability['momentum_stable']}")
    print(f"  Kinetics stable: {stability['kinetics_stable']}")
    print(f"  Charge stable: {stability['charge_stable']}")

