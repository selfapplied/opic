#!/usr/bin/env python3
"""
CE1-ℋ Fusion Demonstration

This script demonstrates the integration of CE1 (Compositional Expression 
Language) with the harmonic operator ℋ(x), showing how ℋ(x)=0 becomes a 
CE1 fixed-point expression.

The harmonic operator is defined as:
    ℋ(x) = ln(x) · ζ(x) · i·tan(πx/2) · sin(πx) · i·cos(πx)

In CE1, this is expressed as:
    H(c) ::= {ln c} + [ζ c] + (tan c) + <sin c> + <i cos c>

And the root condition ℋ(x)=0 becomes:
    < H(c) >
"""

import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from aquifer.ce1 import CE1Parser, CE1Evaluator, create_ce1_context
from aquifer.harmonic import (
    HarmonicOperator,
    HarmonicRootFinder,
    create_harmonic_ce1_evaluator
)


def demo_ce1_basics():
    """Demonstrate basic CE1 bracket semantics."""
    print("=" * 70)
    print("CE1 BRACKET SEMANTICS DEMONSTRATION")
    print("=" * 70)
    print()
    
    print("1. BRACKET TYPES IN CE1:")
    print("-" * 70)
    print("  () : Morphism (height 1) - transformations, rotational dynamics")
    print("  <> : Fixed-point witness (height 0) - resolve equilibria")
    print("  {} : Boundary (height 0) - domain constraints, collapse")
    print("  [] : Memory (height 0) - LR sequencing, accumulation")
    print()
    
    print("2. PARSING CE1 EXPRESSIONS:")
    print("-" * 70)
    
    examples = [
        "< (H c) >",
        "{ln c}",
        "[ζ c]",
        "(tan c)",
        "<sin c>",
    ]
    
    for expr_str in examples:
        expr = CE1Parser.parse(expr_str)
        print(f"  Expression: {expr_str:15s} → {expr}")
    print()


def demo_harmonic_operator():
    """Demonstrate the harmonic operator ℋ(x)."""
    print("=" * 70)
    print("HARMONIC OPERATOR ℋ(x) DEMONSTRATION")
    print("=" * 70)
    print()
    
    print("1. HARMONIC OPERATOR DEFINITION:")
    print("-" * 70)
    print("  ℋ(x) = ln(x) · ζ(x) · i·tan(πx/2) · sin(πx) · i·cos(πx)")
    print()
    print("  Components:")
    print("    - ln(x)       : Collapse (boundary dynamics)")
    print("    - ζ(x)        : Accumulation (memory/series)")
    print("    - i·tan(πx/2) : Phase (morphism/rotation)")
    print("    - sin(πx)     : Oscillation (witness)")
    print("    - i·cos(πx)   : Oscillation (witness)")
    print()
    
    print("2. CE1 REPRESENTATION:")
    print("-" * 70)
    operator = HarmonicOperator()
    ce1_expr = operator.to_ce1_expression()
    ce1_root = operator.to_ce1_root_expression()
    print(f"  H(c) ::= {ce1_expr}")
    print(f"  Root:    {ce1_root}")
    print()
    
    print("3. EVALUATING ℋ(x) AT SAMPLE POINTS:")
    print("-" * 70)
    
    test_points = [
        (0.5 + 0.0j, "On critical line, t=0"),
        (0.5 + 14.134j, "Near first zeta zero"),
        (1.0 + 0.0j, "At s=1 (zeta pole)"),
        (2.0 + 0.0j, "Real axis, s=2"),
    ]
    
    for point, description in test_points:
        try:
            value = operator.evaluate(point)
            magnitude = abs(value)
            print(f"  ℋ({point}) = {value:.6f}")
            print(f"    |ℋ| = {magnitude:.6f} — {description}")
        except (ValueError, ZeroDivisionError, OverflowError) as e:
            # Catch expected numerical errors from harmonic operator evaluation
            print(f"  ℋ({point}) — Numerical error: {e}")
        print()


def demo_root_finding():
    """Demonstrate finding roots of ℋ(x)=0."""
    print("=" * 70)
    print("ROOT FINDING: SOLVING ℋ(x) = 0")
    print("=" * 70)
    print()
    
    print("1. CREATING ROOT FINDER:")
    print("-" * 70)
    operator = HarmonicOperator()
    finder = HarmonicRootFinder(operator)
    print("  Root finder created with harmonic operator ℋ(x)")
    print()
    
    print("2. FINDING SINGLE ROOT:")
    print("-" * 70)
    initial_guess = 0.5 + 14.0j
    print(f"  Initial guess: {initial_guess}")
    
    root, converged, iterations = finder.find_root(initial_guess)
    print(f"  Result: {root}")
    print(f"  Converged: {converged}")
    print(f"  Iterations: {iterations}")
    
    if converged:
        residual = abs(operator.evaluate(root))
        print(f"  Residual |ℋ(root)| = {residual:.2e}")
    print()
    
    print("3. SEARCHING CRITICAL LINE Re(s) = 1/2:")
    print("-" * 70)
    print("  This is the key line for zeta zeros (Riemann Hypothesis)")
    roots = finder.find_roots_on_critical_line(t_min=10.0, t_max=30.0, num_guesses=5)
    
    if roots:
        print(f"  Found {len(roots)} root(s):")
        for i, (root, residual) in enumerate(roots, 1):
            print(f"    Root {i}: s = {root.real:.4f} + {root.imag:.4f}i")
            print(f"             |ℋ(s)| = {residual:.2e}")
    else:
        print("  No roots found in this range (may need more iterations)")
    print()


def demo_ce1_harmonic_fusion():
    """Demonstrate the complete CE1-ℋ fusion."""
    print("=" * 70)
    print("CE1-ℋ FUSION: UNIFIED OPERATOR-UNIVERSE")
    print("=" * 70)
    print()
    
    print("1. THE FUSION CONCEPT:")
    print("-" * 70)
    print("  ℋ(x)=0 is expressed as a CE1 fixed-point condition:")
    print()
    print("    < H(c) >")
    print()
    print("  where H(c) encodes the full harmonic structure using")
    print("  CE1 bracket semantics:")
    print()
    print("    H(c) ::= {ln c} + [ζ c] + (tan c) + <sin c> + <i cos c>")
    print()
    print("  Each bracket maps to a component of ℋ(x):")
    print("    {ln c}    ↔ collapse/boundary")
    print("    [ζ c]     ↔ accumulation/memory")
    print("    (tan c)   ↔ phase/morphism")
    print("    <sin c>   ↔ oscillation/witness")
    print("    <i cos c> ↔ oscillation/witness")
    print()
    
    print("2. CE1 AS UNIVERSAL OPERATOR ALGEBRA:")
    print("-" * 70)
    print("  With this fusion, CE1 can now express:")
    print("    ✓ Analytic roots")
    print("    ✓ Zeta-like structures")
    print("    ✓ Singularities")
    print("    ✓ Oscillatory equilibria")
    print("    ✓ Fixed-point operators")
    print()
    print("  The bracket system becomes a genuine operator algebra")
    print("  for harmonic analysis.")
    print()
    
    print("3. CAPABILITIES ENABLED:")
    print("-" * 70)
    print("  • Collapse dynamics (log)")
    print("  • Accumulation dynamics (zeta)")
    print("  • Phase dynamics (tan)")
    print("  • Oscillation dynamics (sin/cos)")
    print("  • Fixed-point solver (<>)")
    print()
    print("  This is sufficient to express:")
    print("    • The Euler product")
    print("    • The analytic continuation of zeta")
    print("    • The functional equation")
    print("    • The zeta zeros")
    print("    • π, e, and harmonic constants")
    print("    • Any analytic fixed-point operator")
    print()


def main():
    """Run all demonstrations."""
    print()
    print("#" * 70)
    print("#" + " " * 68 + "#")
    print("#" + "  CE1-ℋ FUSION: THE HARMONIC OPERATOR AS CE1 EXPRESSION".center(68) + "#")
    print("#" + " " * 68 + "#")
    print("#" * 70)
    print()
    
    demo_ce1_basics()
    print()
    
    demo_harmonic_operator()
    print()
    
    demo_root_finding()
    print()
    
    demo_ce1_harmonic_fusion()
    print()
    
    print("=" * 70)
    print("DEMONSTRATION COMPLETE")
    print("=" * 70)
    print()
    print("The CE1-ℋ fusion transforms ℋ(x)=0 into a CE1 fixed-point")
    print("expression, making CE1 a universal calculus for singularity-")
    print("balanced functions.")
    print()


if __name__ == "__main__":
    main()
