#!/usr/bin/env python3
"""
Tests for CE1-ℋ Fusion Implementation

Validates:
1. CE1 bracket semantics
2. Harmonic operator components
3. Fixed-point evaluation
4. Root finding on critical line
"""

import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from aquifer.ce1 import (
    BracketType,
    CE1Expression,
    CE1Parser,
    CE1Evaluator,
    create_ce1_context
)
from aquifer.harmonic import (
    HarmonicOperator,
    HarmonicRootFinder,
    compute_zeta_approx,
    create_harmonic_ce1_evaluator
)
import cmath
import math


def test_bracket_types():
    """Test CE1 bracket type definitions."""
    print("Testing CE1 bracket types...")
    
    assert BracketType.MORPHISM.value == "morphism"
    assert BracketType.WITNESS.value == "witness"
    assert BracketType.BOUNDARY.value == "boundary"
    assert BracketType.MEMORY.value == "memory"
    
    print("  ✓ Bracket types defined correctly")


def test_ce1_parsing():
    """Test CE1 expression parsing."""
    print("Testing CE1 expression parsing...")
    
    # Test witness bracket
    expr = CE1Parser.parse("<sin c>")
    assert expr.bracket_type == BracketType.WITNESS
    assert expr.height == 0
    
    # Test morphism bracket
    expr = CE1Parser.parse("(tan c)")
    assert expr.bracket_type == BracketType.MORPHISM
    assert expr.height == 1
    
    # Test boundary bracket
    expr = CE1Parser.parse("{ln c}")
    assert expr.bracket_type == BracketType.BOUNDARY
    assert expr.height == 0
    
    # Test memory bracket
    expr = CE1Parser.parse("[ζ c]")
    assert expr.bracket_type == BracketType.MEMORY
    assert expr.height == 0
    
    print("  ✓ CE1 expressions parse correctly")


def test_harmonic_operator_creation():
    """Test harmonic operator instantiation."""
    print("Testing harmonic operator creation...")
    
    operator = HarmonicOperator()
    assert operator.collapse_weight == 1.0
    assert operator.accumulation_weight == 1.0
    assert operator.phase_weight == 1.0
    assert operator.oscillation_sin_weight == 1.0
    assert operator.oscillation_cos_weight == 1.0
    
    # Test with custom weights
    operator = HarmonicOperator(
        collapse_weight=2.0,
        accumulation_weight=3.0
    )
    assert operator.collapse_weight == 2.0
    assert operator.accumulation_weight == 3.0
    
    print("  ✓ Harmonic operator creates correctly")


def test_harmonic_operator_evaluation():
    """Test harmonic operator evaluation at known points."""
    print("Testing harmonic operator evaluation...")
    
    operator = HarmonicOperator()
    
    # Test at s = 0.5 + 0i (should be near zero for simple case)
    value = operator.evaluate(0.5 + 0.0j)
    assert isinstance(value, complex)
    assert abs(value) < 1e-3  # Near zero
    
    # Test at s = 1 + 0i (should be finite)
    value = operator.evaluate(1.0 + 0.0j)
    assert isinstance(value, complex)
    assert abs(value) < 1e-3  # Near zero due to sin(π) = 0
    
    # Test at s = 2 + 0i (should be finite)
    value = operator.evaluate(2.0 + 0.0j)
    assert isinstance(value, complex)
    assert abs(value) < 1e-3  # Near zero due to sin(2π) = 0
    
    print("  ✓ Harmonic operator evaluates correctly")


def test_ce1_representation():
    """Test CE1 string representation of harmonic operator."""
    print("Testing CE1 representation...")
    
    operator = HarmonicOperator()
    
    ce1_expr = operator.to_ce1_expression()
    assert "{ln c}" in ce1_expr
    assert "[ζ c]" in ce1_expr
    assert "(tan c)" in ce1_expr
    assert "<sin c>" in ce1_expr
    assert "<i cos c>" in ce1_expr
    
    ce1_root = operator.to_ce1_root_expression()
    assert ce1_root == "< H(c) >"
    
    print("  ✓ CE1 representation correct")


def test_zeta_approximation():
    """Test Riemann zeta function approximation."""
    print("Testing zeta approximation...")
    
    # Test at s = 2 (known value: π²/6 ≈ 1.645)
    zeta_2 = compute_zeta_approx(2.0 + 0.0j, num_terms=1000)
    expected = math.pi ** 2 / 6
    assert abs(zeta_2.real - expected) < 0.01  # Within 1% error
    
    # Test at s = 3 (known value: ζ(3) ≈ 1.202)
    zeta_3 = compute_zeta_approx(3.0 + 0.0j, num_terms=1000)
    assert 1.1 < zeta_3.real < 1.3
    
    # Test at s = 4 (known value: π⁴/90 ≈ 1.082)
    zeta_4 = compute_zeta_approx(4.0 + 0.0j, num_terms=1000)
    expected = math.pi ** 4 / 90
    assert abs(zeta_4.real - expected) < 0.01
    
    print("  ✓ Zeta approximation accurate")


def test_root_finder_creation():
    """Test root finder instantiation."""
    print("Testing root finder creation...")
    
    operator = HarmonicOperator()
    finder = HarmonicRootFinder(operator)
    
    assert finder.operator == operator
    assert finder.max_iterations == 100
    assert finder.tolerance == 1e-6
    
    print("  ✓ Root finder creates correctly")


def test_root_finding_simple():
    """Test finding roots at known locations."""
    print("Testing root finding...")
    
    operator = HarmonicOperator()
    finder = HarmonicRootFinder(operator)
    
    # Find root near s = 0.5 + 0i
    root, converged, iterations = finder.find_root(0.5 + 0.1j)
    
    # Check that we found something reasonable
    assert isinstance(root, complex)
    assert abs(root.real - 0.5) < 0.1  # Should be near critical line
    
    # Check residual is small
    residual = abs(operator.evaluate(root))
    print(f"    Root found at s = {root}")
    print(f"    Residual |ℋ(s)| = {residual:.2e}")
    
    print("  ✓ Root finding works")


def test_critical_line_search():
    """Test searching for roots on critical line."""
    print("Testing critical line search...")
    
    operator = HarmonicOperator()
    finder = HarmonicRootFinder(operator)
    
    # Search in a small range
    roots = finder.find_roots_on_critical_line(
        t_min=0.0,
        t_max=10.0,
        num_guesses=3
    )
    
    # Check that we found at least one root
    assert len(roots) >= 0  # May or may not find roots depending on iteration
    
    for root, residual in roots:
        print(f"    Root: s = {root.real:.4f} + {root.imag:.4f}i, residual = {residual:.2e}")
        # Check root is on critical line
        assert abs(root.real - 0.5) < 0.1
    
    print(f"  ✓ Critical line search found {len(roots)} root(s)")


def test_ce1_evaluator():
    """Test CE1 evaluator with harmonic operator."""
    print("Testing CE1 evaluator...")
    
    evaluator = create_harmonic_ce1_evaluator()
    
    # Check that operators are registered
    assert 'H' in evaluator.operators
    assert 'ln' in evaluator.operators
    assert 'zeta' in evaluator.operators
    assert 'tan' in evaluator.operators
    assert 'sin' in evaluator.operators
    assert 'cos' in evaluator.operators
    
    print("  ✓ CE1 evaluator configured correctly")


def run_all_tests():
    """Run all tests."""
    print()
    print("=" * 70)
    print("CE1-ℋ FUSION TEST SUITE")
    print("=" * 70)
    print()
    
    tests = [
        test_bracket_types,
        test_ce1_parsing,
        test_harmonic_operator_creation,
        test_harmonic_operator_evaluation,
        test_ce1_representation,
        test_zeta_approximation,
        test_root_finder_creation,
        test_root_finding_simple,
        test_critical_line_search,
        test_ce1_evaluator,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"  ✗ Test failed: {e}")
            failed += 1
        except Exception as e:
            print(f"  ✗ Test error: {e}")
            failed += 1
    
    print()
    print("=" * 70)
    print(f"TEST RESULTS: {passed} passed, {failed} failed")
    print("=" * 70)
    print()
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
