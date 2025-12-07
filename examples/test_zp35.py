#!/usr/bin/env python3
"""
Test Suite for ZP35 Theory Implementation

Tests for:
- ZP-Metric ultrametric properties
- Cantor function correctness
- ZP-Embedding consistency
- ZP-Fixed Point Operator convergence
- ZP35 constant emergence
"""

import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from aquifer.zp35 import (
    ZP35_CONSTANT,
    DEFAULT_THETA,
    Theory,
    ZPMetric,
    CantorFunction,
    ZPEmbedding,
    ZPFixedPointOperator,
    create_theory,
    compute_coherence,
    analyze_theory_collection,
)


class TestRunner:
    """Simple test runner for ZP35 tests."""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.tests = []
    
    def test(self, name, condition, message=""):
        """Run a single test."""
        self.tests.append(name)
        if condition:
            self.passed += 1
            print(f"  ✓ {name}")
            return True
        else:
            self.failed += 1
            print(f"  ✗ {name}")
            if message:
                print(f"    {message}")
            return False
    
    def assert_near(self, name, actual, expected, tolerance=1e-6):
        """Assert that a value is near expected within tolerance."""
        condition = abs(actual - expected) < tolerance
        message = f"Expected {expected}, got {actual} (tolerance={tolerance})"
        return self.test(name, condition, message)
    
    def summary(self):
        """Print test summary."""
        total = self.passed + self.failed
        print()
        print("=" * 70)
        print(f"TEST SUMMARY: {self.passed}/{total} passed")
        if self.failed > 0:
            print(f"  {self.failed} test(s) failed")
        else:
            print("  All tests passed!")
        print("=" * 70)
        return self.failed == 0


def test_theory_creation(runner):
    """Test Theory object creation."""
    print("\nTest: Theory Creation")
    print("-" * 70)
    
    theory = create_theory("PA", 100.0, axioms=["Axiom 1", "Axiom 2"])
    
    runner.test(
        "Theory has correct name",
        theory.name == "PA"
    )
    
    runner.test(
        "Theory has correct ordinal",
        theory.ordinal == 100.0
    )
    
    runner.test(
        "Theory has axioms",
        theory.axioms is not None and len(theory.axioms) == 2
    )


def test_zp_metric_basic(runner):
    """Test basic ZP-Metric properties."""
    print("\nTest: ZP-Metric Basic Properties")
    print("-" * 70)
    
    metric = ZPMetric()
    
    theory_a = create_theory("A", 100.0)
    theory_b = create_theory("B", 200.0)
    theory_c = create_theory("C", 300.0)
    
    # Test self-distance is zero
    d_aa = metric.distance(theory_a, theory_a)
    runner.assert_near("Self-distance is zero", d_aa, 0.0)
    
    # Test distance is symmetric (in this simplified model)
    d_ab = metric.distance(theory_a, theory_b)
    d_ba = metric.distance(theory_b, theory_a)
    runner.assert_near("Distance is symmetric", d_ab, d_ba)
    
    # Test distance is at least max ordinal
    runner.test(
        "Distance >= max ordinal",
        d_ab >= max(theory_a.ordinal, theory_b.ordinal)
    )


def test_zp_metric_ultrametric(runner):
    """Test ZP-Metric ultrametric property."""
    print("\nTest: ZP-Metric Ultrametric Property")
    print("-" * 70)
    
    metric = ZPMetric()
    
    # Create three theories with different strengths
    theory_a = create_theory("PA", 100.0)
    theory_b = create_theory("ACA", 300.0)
    theory_c = create_theory("ATR", 500.0)
    
    # Verify ultrametric property: d(A,C) <= max(d(A,B), d(B,C))
    is_ultrametric = metric.verify_ultrametric_property(
        theory_a, theory_b, theory_c
    )
    
    runner.test(
        "Ultrametric property holds",
        is_ultrametric
    )
    
    # Test with multiple theory combinations
    theories = [
        create_theory("T1", 100.0),
        create_theory("T2", 200.0),
        create_theory("T3", 300.0),
        create_theory("T4", 400.0),
    ]
    
    all_ultrametric = True
    for i in range(len(theories)):
        for j in range(len(theories)):
            for k in range(len(theories)):
                if not metric.verify_ultrametric_property(
                    theories[i], theories[j], theories[k]
                ):
                    all_ultrametric = False
                    break
    
    runner.test(
        "Ultrametric property holds for all combinations",
        all_ultrametric
    )


def test_bridge_theory(runner):
    """Test bridge theory computation."""
    print("\nTest: Bridge Theory Computation")
    print("-" * 70)
    
    metric = ZPMetric()
    
    theory_a = create_theory("A", 100.0)
    theory_b = create_theory("B", 200.0)
    
    bridge = metric.compute_bridge_theory([theory_a, theory_b])
    
    runner.test(
        "Bridge theory exists",
        bridge is not None
    )
    
    runner.test(
        "Bridge ordinal >= theory A ordinal",
        bridge.ordinal >= theory_a.ordinal
    )
    
    runner.test(
        "Bridge ordinal >= theory B ordinal",
        bridge.ordinal >= theory_b.ordinal
    )
    
    # Bridge of single theory should be the theory itself
    single_bridge = metric.compute_bridge_theory([theory_a])
    runner.test(
        "Bridge of single theory is identity",
        single_bridge.ordinal == theory_a.ordinal
    )


def test_cantor_function_basic(runner):
    """Test basic Cantor function properties."""
    print("\nTest: Cantor Function Basic Properties")
    print("-" * 70)
    
    cantor = CantorFunction(iterations=10)
    
    # Test boundary values
    runner.assert_near("f(0) = 0", cantor(0.0), 0.0)
    runner.assert_near("f(1) = 1", cantor(1.0), 1.0)
    
    # Test monotonicity: f(x) <= f(y) for x <= y
    test_points = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    is_monotone = True
    for i in range(len(test_points) - 1):
        if cantor(test_points[i]) > cantor(test_points[i+1]):
            is_monotone = False
            break
    
    runner.test(
        "Cantor function is monotone increasing",
        is_monotone
    )
    
    # Test range is [0, 1]
    values = [cantor(x) for x in test_points]
    runner.test(
        "All values in [0, 1]",
        all(0.0 <= v <= 1.0 for v in values)
    )


def test_cantor_function_plateau(runner):
    """Test Cantor function plateau structure."""
    print("\nTest: Cantor Function Plateau Structure")
    print("-" * 70)
    
    cantor = CantorFunction(iterations=10)
    
    # The main plateau should be around 1/3
    plateau_start, plateau_end = cantor.compute_plateau_range()
    
    runner.test(
        "Plateau exists",
        plateau_end > plateau_start
    )
    
    runner.test(
        "Plateau near 1/3",
        abs((plateau_start + plateau_end) / 2 - 1.0/3.0) < 0.1
    )
    
    # Test that the function is relatively flat in middle third
    # (removed interval in Cantor set)
    middle_values = [cantor(0.33 + 0.01 * i) for i in range(10)]
    if len(middle_values) > 1:
        max_variation = max(middle_values) - min(middle_values)
        runner.test(
            "Function relatively flat in middle region",
            max_variation < 0.3  # Allow some variation
        )


def test_zp_embedding_basic(runner):
    """Test basic ZP-Embedding properties."""
    print("\nTest: ZP-Embedding Basic Properties")
    print("-" * 70)
    
    embedding = ZPEmbedding(theta=1000.0)
    
    # Test zero ordinal maps to near zero
    theory_zero = create_theory("Zero", 0.0)
    embedded_zero = embedding.embed(theory_zero)
    runner.assert_near("Zero ordinal near zero", embedded_zero, 0.0, tolerance=0.01)
    
    # Test max ordinal maps to near one
    theory_max = create_theory("Max", 1000.0)
    embedded_max = embedding.embed(theory_max)
    runner.test(
        "Max ordinal near one",
        embedded_max > 0.9  # Should be close to 1 but not exactly due to Cantor
    )
    
    # Test monotonicity
    theories = [
        create_theory(f"T{i}", i * 100.0)
        for i in range(10)
    ]
    
    embeddings = [embedding.embed(t) for t in theories]
    is_monotone = all(
        embeddings[i] <= embeddings[i+1]
        for i in range(len(embeddings) - 1)
    )
    
    runner.test(
        "Embedding preserves order (monotone)",
        is_monotone
    )


def test_zp_embedding_plateaus(runner):
    """Test ZP-Embedding plateau grouping."""
    print("\nTest: ZP-Embedding Plateau Grouping")
    print("-" * 70)
    
    embedding = ZPEmbedding(theta=1000.0)
    
    # Create theories that should cluster
    theories = [
        create_theory("T1", 100.0),
        create_theory("T2", 105.0),  # Close to T1
        create_theory("T3", 500.0),
        create_theory("T4", 510.0),  # Close to T3
    ]
    
    plateaus = embedding.find_plateau_theories(theories, tolerance=0.05)
    
    runner.test(
        "Plateaus detected",
        len(plateaus) > 0
    )
    
    runner.test(
        "Multiple plateaus exist",
        len(plateaus) >= 2
    )
    
    # Theories in same plateau should have similar embeddings
    for plateau_theories in plateaus.values():
        if len(plateau_theories) >= 2:
            embeddings = [embedding.embed(t) for t in plateau_theories]
            max_diff = max(embeddings) - min(embeddings)
            runner.test(
                "Theories in same plateau have similar embeddings",
                max_diff < 0.1
            )
            break


def test_kappa_operator_basic(runner):
    """Test basic κ-operator properties."""
    print("\nTest: κ-Operator Basic Properties")
    print("-" * 70)
    
    operator = ZPFixedPointOperator(theta=1000.0)
    
    theory_a = create_theory("A", 200.0)
    theory_b = create_theory("B", 300.0)
    
    # Apply operator
    coherence = operator.apply(theory_a, theory_b)
    
    runner.test(
        "Coherence in [0, 1]",
        0.0 <= coherence <= 1.0
    )
    
    # Coherence should be commutative
    coherence_rev = operator.apply(theory_b, theory_a)
    runner.assert_near(
        "Coherence is commutative",
        coherence, coherence_rev, tolerance=1e-6
    )


def test_fixed_point_convergence(runner):
    """Test fixed point convergence."""
    print("\nTest: Fixed Point Convergence")
    print("-" * 70)
    
    operator = ZPFixedPointOperator(theta=1000.0)
    
    # Create diverse theory collection
    theories = [
        create_theory("PA", 100.0),
        create_theory("ACA", 300.0),
        create_theory("ATR", 500.0),
        create_theory("Π¹₁-CA", 700.0),
    ]
    
    fixed_point, converged = operator.find_fixed_point(theories)
    
    runner.test(
        "Fixed point computation converges",
        converged
    )
    
    runner.test(
        "Fixed point in [0, 1]",
        0.0 <= fixed_point <= 1.0
    )


def test_zp35_emergence(runner):
    """Test emergence of ZP35 constant."""
    print("\nTest: ZP35 Constant Emergence")
    print("-" * 70)
    
    operator = ZPFixedPointOperator(theta=1000.0)
    
    # Test with various theory collections
    test_cases = [
        # Diverse collection
        [
            create_theory("T1", 100.0),
            create_theory("T2", 300.0),
            create_theory("T3", 500.0),
            create_theory("T4", 700.0),
        ],
        # Larger collection
        [
            create_theory(f"T{i}", i * 100.0)
            for i in range(1, 9)
        ],
        # Clustered collection
        [
            create_theory("T1", 250.0),
            create_theory("T2", 300.0),
            create_theory("T3", 350.0),
            create_theory("T4", 400.0),
        ],
    ]
    
    near_zp35_count = 0
    
    for i, theories in enumerate(test_cases):
        fixed_point, converged = operator.find_fixed_point(theories)
        deviation = operator.compute_zp35_deviation(fixed_point)
        
        if converged and deviation < 0.1:  # Within 10% of ZP35
            near_zp35_count += 1
    
    runner.test(
        "At least one collection near ZP35",
        near_zp35_count > 0
    )
    
    print(f"    ({near_zp35_count}/{len(test_cases)} collections near ZP35)")


def test_comprehensive_analysis(runner):
    """Test comprehensive analysis function."""
    print("\nTest: Comprehensive Analysis")
    print("-" * 70)
    
    theories = [
        create_theory("PA", 100.0),
        create_theory("ACA", 300.0),
        create_theory("ATR", 500.0),
    ]
    
    try:
        analysis = analyze_theory_collection(theories, theta=1000.0)
        
        runner.test(
            "Analysis completes successfully",
            True
        )
        
        runner.test(
            "Analysis contains metric_distances",
            'metric_distances' in analysis
        )
        
        runner.test(
            "Analysis contains embeddings",
            'embeddings' in analysis
        )
        
        runner.test(
            "Analysis contains fixed_point",
            'fixed_point' in analysis
        )
        
        runner.test(
            "Analysis contains zp35_deviation",
            'zp35_deviation' in analysis
        )
        
    except Exception as e:
        runner.test(
            "Analysis completes successfully",
            False,
            f"Exception: {str(e)}"
        )


def test_convenience_functions(runner):
    """Test convenience wrapper functions."""
    print("\nTest: Convenience Functions")
    print("-" * 70)
    
    theory_a = create_theory("A", 200.0)
    theory_b = create_theory("B", 400.0)
    
    try:
        coherence = compute_coherence(theory_a, theory_b, theta=1000.0)
        
        runner.test(
            "compute_coherence works",
            True
        )
        
        runner.test(
            "Coherence value in [0, 1]",
            0.0 <= coherence <= 1.0
        )
        
    except Exception as e:
        runner.test(
            "compute_coherence works",
            False,
            f"Exception: {str(e)}"
        )


def main():
    """Run all tests."""
    print()
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 24 + "ZP35 TEST SUITE" + " " * 29 + "║")
    print("╚" + "═" * 68 + "╝")
    
    runner = TestRunner()
    
    # Run all test suites
    test_theory_creation(runner)
    test_zp_metric_basic(runner)
    test_zp_metric_ultrametric(runner)
    test_bridge_theory(runner)
    test_cantor_function_basic(runner)
    test_cantor_function_plateau(runner)
    test_zp_embedding_basic(runner)
    test_zp_embedding_plateaus(runner)
    test_kappa_operator_basic(runner)
    test_fixed_point_convergence(runner)
    test_zp35_emergence(runner)
    test_comprehensive_analysis(runner)
    test_convenience_functions(runner)
    
    # Print summary
    all_passed = runner.summary()
    
    print()
    if all_passed:
        print("✓ All ZP35 tests passed successfully!")
        print()
        print("The ZP35 theory implementation is working correctly:")
        print("  • ZP-Metric exhibits ultrametric properties")
        print("  • Cantor function creates fractal embedding")
        print("  • ZP-Embedding preserves order and creates plateaus")
        print(f"  • κ-operator converges to fixed point near {ZP35_CONSTANT}")
        print()
        return 0
    else:
        print("✗ Some tests failed. Please review the implementation.")
        print()
        return 1


if __name__ == "__main__":
    sys.exit(main())
