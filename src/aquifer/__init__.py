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
- CE1: Compositional Expression Language with bracket semantics
- Harmonic: Harmonic operator ℋ(x) integrated with CE1
"""

from .feigenbaum import feigenbaum_constrain
from .zeta import zeta_spectral_filter
from .rg import rg_flow
from .ce1 import (
    BracketType,
    CE1Expression,
    CE1Parser,
    CE1Evaluator,
    create_ce1_context,
)
from .harmonic import (
    HarmonicOperator,
    HarmonicRootFinder,
    compute_zeta_approx,
    create_harmonic_ce1_evaluator,
)

__all__ = [
    'feigenbaum_constrain',
    'zeta_spectral_filter',
    'rg_flow',
    'BracketType',
    'CE1Expression',
    'CE1Parser',
    'CE1Evaluator',
    'create_ce1_context',
    'HarmonicOperator',
    'HarmonicRootFinder',
    'compute_zeta_approx',
    'create_harmonic_ce1_evaluator',
]

__version__ = '0.2.0'
