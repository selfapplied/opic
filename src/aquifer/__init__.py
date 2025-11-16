"""
Aquifer: Invariant-Preserving Primitives for OPIC

The Aquifer framework provides mathematical primitives that encode deep
structural invariants from chaos theory, spectral analysis, and renormalization
group theory. These primitives enable programs to naturally respect physical
and mathematical invariants during composition and evolution.

Core Primitives:
- Feigenbaum: Universal scaling laws in bifurcation cascades
- Zeta: Spectral decomposition and prime structure
- RG Flow: Renormalization group transformations for multi-scale analysis
"""

from .feigenbaum import feigenbaum_constrain
from .zeta import zeta_spectral_filter
from .rg import rg_flow

__all__ = [
    'feigenbaum_constrain',
    'zeta_spectral_filter',
    'rg_flow',
]

__version__ = '0.1.0'
