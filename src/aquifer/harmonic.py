"""
Harmonic Operator ℋ(x) - CE1 Integration

The harmonic operator ℋ(x) is defined as:

    ℋ(x) = ln(x) · ζ(x) · i·tan(πx/2) · sin(πx) · i·cos(πx)

This operator encodes:
- Collapse dynamics (ln)
- Accumulation dynamics (ζ)
- Phase dynamics (tan)
- Oscillation dynamics (sin/cos)

Roots of ℋ(x) = 0 characterize harmonic singularities and are related to
zeta zeros through the balanced oscillation condition.

In CE1, the harmonic operator is expressed as:

    H(c) ::= {ln c} + [ζ c] + (tan c) + <sin c> + <i cos c>

where:
- {ln c} : boundary/collapse (log controls domain)
- [ζ c] : memory/accumulation (zeta is LR-accumulated series)
- (tan c) : morphism/phase (rotational singularities)
- <sin c> : witness/oscillation (sin anchors fixed points)
- <i cos c> : witness/oscillation (cos anchors fixed points)

And the root condition is expressed as:

    < H(c) >

which evaluates to the fixed point where ℋ(x) = 0.
"""

import cmath
import math
from typing import Union, Tuple, Optional, List
from .ce1 import CE1Expression, CE1Evaluator, BracketType, create_ce1_context


def compute_zeta_approx(s: complex, num_terms: int = 1000) -> complex:
    """
    Approximate Riemann zeta function using Dirichlet series.
    
    ζ(s) = Σ(n=1 to ∞) n^(-s)
    
    This is a simple approximation valid for Re(s) > 1.
    For other values, proper analytic continuation would be needed.
    
    Args:
        s: Complex argument
        num_terms: Number of terms to sum
        
    Returns:
        Approximate value of ζ(s)
    """
    if s.real <= 1:
        # For Re(s) ≤ 1, proper implementation would use the functional equation:
        # ζ(s) = 2^s · π^(s-1) · sin(πs/2) · Γ(1-s) · ζ(1-s)
        # This requires computing the gamma function and is beyond the scope
        # of this demonstration. Instead, we use rough approximations:
        if abs(s - 1) < 0.1:
            # Near pole at s=1, zeta has a simple pole
            return complex(10.0, 0.0)  # Large value approximating pole behavior
        # Very rough approximation for demonstration purposes only
        # Real implementation should use Riemann-Siegel formula or similar
        return complex(1.0 / (1.0 - s.real), 0.0)
    
    # Dirichlet series for Re(s) > 1
    result = 0.0 + 0.0j
    for n in range(1, num_terms + 1):
        result += 1.0 / (n ** s)
    
    return result


class HarmonicOperator:
    """
    The harmonic operator ℋ(x) as a CE1-encoded structure.
    
    Attributes:
        collapse_weight: Weight for ln(x) term (default 1.0)
        accumulation_weight: Weight for ζ(x) term (default 1.0)
        phase_weight: Weight for tan(πx/2) term (default 1.0)
        oscillation_sin_weight: Weight for sin(πx) term (default 1.0)
        oscillation_cos_weight: Weight for i·cos(πx) term (default 1.0)
    """
    
    def __init__(self, 
                 collapse_weight: float = 1.0,
                 accumulation_weight: float = 1.0,
                 phase_weight: float = 1.0,
                 oscillation_sin_weight: float = 1.0,
                 oscillation_cos_weight: float = 1.0):
        self.collapse_weight = collapse_weight
        self.accumulation_weight = accumulation_weight
        self.phase_weight = phase_weight
        self.oscillation_sin_weight = oscillation_sin_weight
        self.oscillation_cos_weight = oscillation_cos_weight
    
    def evaluate(self, x: complex) -> complex:
        """
        Evaluate ℋ(x) at a given point.
        
        ℋ(x) = ln(x) · ζ(x) · i·tan(πx/2) · sin(πx) · i·cos(πx)
        
        Args:
            x: Point to evaluate at
            
        Returns:
            Value of ℋ(x)
        """
        # Handle edge cases
        if abs(x) < 1e-10:
            # Singularity at x=0 due to ln(x)
            # Return a large finite value to avoid numerical issues
            return complex(1e10, 0.0)
        
        # Collapse component: ln(x)
        try:
            collapse = cmath.log(x) * self.collapse_weight
        except (ValueError, ZeroDivisionError):
            # Use large finite value instead of infinity for numerical stability
            collapse = complex(1e10, 0.0)
        
        # Accumulation component: ζ(x)
        try:
            accumulation = compute_zeta_approx(x) * self.accumulation_weight
        except (ValueError, ZeroDivisionError, OverflowError):
            accumulation = complex(1.0, 0.0)
        
        # Phase component: i·tan(πx/2)
        try:
            phase_arg = cmath.pi * x / 2.0
            phase = 1j * cmath.tan(phase_arg) * self.phase_weight
        except (ValueError, ZeroDivisionError, OverflowError):
            phase = complex(0.0, 1.0)  # Default to i
        
        # Oscillation components: sin(πx) and i·cos(πx)
        try:
            osc_arg = cmath.pi * x
            osc_sin = cmath.sin(osc_arg) * self.oscillation_sin_weight
            osc_cos = 1j * cmath.cos(osc_arg) * self.oscillation_cos_weight
        except (ValueError, OverflowError):
            osc_sin = complex(0.0, 0.0)
            osc_cos = complex(0.0, 1.0)
        
        # Combine all components (multiplicative structure)
        result = collapse * accumulation * phase * osc_sin * osc_cos
        
        return result
    
    def to_ce1_expression(self) -> str:
        """
        Convert the harmonic operator to CE1 expression syntax.
        
        Returns:
            CE1 string representation:
            H(c) ::= {ln c} + [ζ c] + (tan c) + <sin c> + <i cos c>
        """
        return "{ln c} + [ζ c] + (tan c) + <sin c> + <i cos c>"
    
    def to_ce1_root_expression(self) -> str:
        """
        Convert the root condition ℋ(x) = 0 to CE1 expression.
        
        Returns:
            CE1 string representation: < H(c) >
        """
        return "< H(c) >"


class HarmonicRootFinder:
    """
    Find roots of the harmonic operator ℋ(x) = 0.
    
    Uses Newton-Raphson method with complex arithmetic to find points
    where the harmonic operator vanishes.
    """
    
    def __init__(self, operator: HarmonicOperator, 
                 max_iterations: int = 100,
                 tolerance: float = 1e-6,
                 critical_line_tolerance: float = 0.1):
        self.operator = operator
        self.max_iterations = max_iterations
        self.tolerance = tolerance
        self.critical_line_tolerance = critical_line_tolerance  # Tolerance for Re(s) = 1/2 projection
    
    def find_root(self, initial_guess: complex = 0.5 + 14.0j) -> Tuple[complex, bool, int]:
        """
        Find a root of ℋ(x) = 0 starting from an initial guess.
        
        Args:
            initial_guess: Starting point for iteration (default near first zeta zero)
            
        Returns:
            Tuple of (root, converged, iterations)
            - root: The found root (or last iterate)
            - converged: Whether iteration converged
            - iterations: Number of iterations performed
        """
        x = initial_guess
        h = 1e-8  # Step size for numerical derivative
        
        for i in range(self.max_iterations):
            # Evaluate ℋ(x)
            fx = self.operator.evaluate(x)
            
            # Check convergence
            if abs(fx) < self.tolerance:
                return x, True, i + 1
            
            # Check for numerical issues
            if math.isnan(fx.real) or math.isnan(fx.imag) or math.isinf(fx.real) or math.isinf(fx.imag):
                return x, False, i + 1
            
            # Compute numerical derivative ℋ'(x)
            fx_h = self.operator.evaluate(x + h)
            dfx = (fx_h - fx) / h
            
            # Check if derivative is too small
            if abs(dfx) < self.tolerance:
                # Try different direction
                fx_h = self.operator.evaluate(x + 1j * h)
                dfx = (fx_h - fx) / (1j * h)
                
                if abs(dfx) < self.tolerance:
                    return x, False, i + 1
            
            # Newton-Raphson update
            x = x - fx / dfx
            
            # Keep on critical line Re(s) = 1/2 (for zeta-related roots)
            if abs(x.real - 0.5) > self.critical_line_tolerance:
                x = complex(0.5, x.imag)
        
        return x, False, self.max_iterations
    
    def find_roots_on_critical_line(self, 
                                     t_min: float = 0.0,
                                     t_max: float = 50.0,
                                     num_guesses: int = 10) -> List[Tuple[complex, float]]:
        """
        Search for roots on the critical line Re(s) = 1/2.
        
        Args:
            t_min: Minimum imaginary part to search
            t_max: Maximum imaginary part to search
            num_guesses: Number of initial guesses to try
            
        Returns:
            List of (root, residual) tuples for found roots
        """
        roots = []
        
        # Generate initial guesses along critical line
        for i in range(num_guesses):
            t = t_min + (t_max - t_min) * i / (num_guesses - 1)
            initial_guess = complex(0.5, t)
            
            root, converged, _ = self.find_root(initial_guess)
            
            if converged:
                # Check if root is truly on critical line
                if abs(root.real - 0.5) < 0.01:
                    residual = abs(self.operator.evaluate(root))
                    
                    # Check if this is a new root (not too close to existing ones)
                    is_new = True
                    for existing_root, _ in roots:
                        if abs(root - existing_root) < 0.5:
                            is_new = False
                            break
                    
                    if is_new:
                        roots.append((root, residual))
        
        # Sort by imaginary part
        roots.sort(key=lambda x: x[0].imag)
        
        return roots


def create_harmonic_ce1_evaluator() -> CE1Evaluator:
    """
    Create a CE1 evaluator configured with the harmonic operator.
    
    Returns:
        CE1Evaluator with H operator registered
    """
    evaluator = CE1Evaluator()
    operator = HarmonicOperator()
    
    # Register H operator
    evaluator.register_operator('H', operator.evaluate)
    
    # Register component operators
    evaluator.register_operator('ln', lambda x: cmath.log(x) if abs(x) > 1e-10 else complex(float('inf'), 0))
    evaluator.register_operator('zeta', compute_zeta_approx)
    evaluator.register_operator('tan', lambda x: cmath.tan(cmath.pi * x / 2))
    evaluator.register_operator('sin', lambda x: cmath.sin(cmath.pi * x))
    evaluator.register_operator('cos', lambda x: cmath.cos(cmath.pi * x))
    
    return evaluator


# Export public API
__all__ = [
    'HarmonicOperator',
    'HarmonicRootFinder',
    'compute_zeta_approx',
    'create_harmonic_ce1_evaluator',
]
