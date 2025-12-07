#!/usr/bin/env python3
"""
ZP35 Theory Demonstration

This script demonstrates the ZP35 theory of coherence geometry - a framework
for measuring how axiom systems relate through:

1. ZP-Metric: An ultrametric on theories
2. ZP-Embedding: A fractal embedding into [0,1]
3. ZP-Fixed Point Operator: Coherence operator with 0.35 attractor

The ZP35 constant (≈0.35) emerges as the first coherence equilibrium.
"""

import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from aquifer.zp35 import (
    ZP35_CONSTANT,
    Theory,
    ZPMetric,
    CantorFunction,
    ZPEmbedding,
    ZPFixedPointOperator,
    create_theory,
    compute_coherence,
    analyze_theory_collection,
)


def demo_zp_metric():
    """Demonstrate the ZP-Metric ultrametric on theories."""
    print("=" * 70)
    print("ZP-METRIC: ULTRAMETRIC ON THEORIES")
    print("=" * 70)
    print()
    
    print("1. METRIC DEFINITION:")
    print("-" * 70)
    print("  d(A,B) = inf { |C| : C ⊢ A ∧ C ⊢ B }")
    print()
    print("  The distance is the strength of the weakest theory that")
    print("  proves both A and B.")
    print()
    
    print("2. EXAMPLE THEORIES:")
    print("-" * 70)
    
    # Create sample theories with increasing proof-theoretic strength
    theories = [
        create_theory("PA", 100.0),  # Peano Arithmetic
        create_theory("ACA₀", 300.0),  # Arithmetic Comprehension
        create_theory("ATR₀", 500.0),  # Arithmetic Transfinite Recursion
        create_theory("Π¹₁-CA₀", 700.0),  # Π¹₁ Comprehension
    ]
    
    for theory in theories:
        print(f"  {theory.name:12s} : |T| = {theory.ordinal:.1f}")
    print()
    
    print("3. PAIRWISE DISTANCES:")
    print("-" * 70)
    
    metric = ZPMetric()
    
    for i, theory_a in enumerate(theories):
        for j, theory_b in enumerate(theories):
            if i < j:
                dist = metric.distance(theory_a, theory_b)
                print(f"  d({theory_a.name:12s}, {theory_b.name:12s}) = {dist:.1f}")
    print()
    
    print("4. ULTRAMETRIC PROPERTY VERIFICATION:")
    print("-" * 70)
    print("  d(A,C) ≤ max(d(A,B), d(B,C))")
    print()
    
    # Verify ultrametric property for all triples
    for i, theory_a in enumerate(theories):
        for j, theory_b in enumerate(theories):
            for k, theory_c in enumerate(theories):
                if i < j < k:
                    is_valid = metric.verify_ultrametric_property(
                        theory_a, theory_b, theory_c
                    )
                    print(f"  ({theory_a.name}, {theory_b.name}, {theory_c.name}): "
                          f"{'✓' if is_valid else '✗'}")
    print()


def demo_cantor_function():
    """Demonstrate the Cantor (Devil's Staircase) function."""
    print("=" * 70)
    print("CANTOR FUNCTION: FRACTAL EMBEDDING")
    print("=" * 70)
    print()
    
    print("1. CANTOR FUNCTION PROPERTIES:")
    print("-" * 70)
    print("  - Continuous and monotone increasing")
    print("  - Constant on removed intervals (Cantor set)")
    print("  - Derivative zero almost everywhere")
    print("  - Creates plateaus where values cluster")
    print("  - First major plateau near x ∈ [0.33, 0.36]")
    print()
    
    print("2. SAMPLE VALUES:")
    print("-" * 70)
    
    cantor = CantorFunction(iterations=10)
    
    test_points = [
        0.0, 0.1, 0.2, 0.25, 0.3, 0.33, 0.35, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0
    ]
    
    print("  x      f(x)")
    print("  " + "-" * 20)
    for x in test_points:
        fx = cantor(x)
        print(f"  {x:.2f}   {fx:.4f}")
    print()
    
    print("3. PLATEAU IDENTIFICATION:")
    print("-" * 70)
    
    # The main plateau is around 1/3 in the input space
    plateau_start, plateau_end = cantor.compute_plateau_range()
    print(f"  Main plateau: x ∈ [{plateau_start:.3f}, {plateau_end:.3f}]")
    print(f"  Function value: f(x) ≈ {cantor((plateau_start + plateau_end)/2):.4f}")
    print()


def demo_zp_embedding():
    """Demonstrate the ZP-Embedding of theories into [0,1]."""
    print("=" * 70)
    print("ZP-EMBEDDING: FRACTAL MAPPING INTO [0,1]")
    print("=" * 70)
    print()
    
    print("1. EMBEDDING DEFINITION:")
    print("-" * 70)
    print("  φ(T) = f(|T| / Θ)")
    print()
    print("  where f is the Cantor function and Θ is a cutoff ordinal.")
    print()
    
    print("2. THEORY EMBEDDINGS:")
    print("-" * 70)
    
    # Create theories spanning different ordinal ranges
    theories = [
        create_theory("PA", 100.0),
        create_theory("PA + Con(PA)", 150.0),
        create_theory("ACA₀", 300.0),
        create_theory("ACA₀⁺", 350.0),
        create_theory("ATR₀", 500.0),
        create_theory("Π¹₁-CA₀", 700.0),
        create_theory("∆¹₂-CA₀", 800.0),
    ]
    
    embedding = ZPEmbedding(theta=1000.0)
    
    print("  Theory           |T|      φ(T)")
    print("  " + "-" * 45)
    for theory in theories:
        embedded = embedding.embed(theory)
        print(f"  {theory.name:15s}  {theory.ordinal:6.1f}   {embedded:.4f}")
    print()
    
    print("3. PLATEAU GROUPING:")
    print("-" * 70)
    print("  Theories with similar embedded values cluster in plateaus:")
    print()
    
    plateaus = embedding.find_plateau_theories(theories, tolerance=0.02)
    
    for i, (plateau_value, plateau_theories) in enumerate(sorted(plateaus.items())):
        print(f"  Plateau {i+1} (φ ≈ {plateau_value:.4f}):")
        for theory in plateau_theories:
            print(f"    - {theory.name}")
    print()


def demo_zp_fixed_point_operator():
    """Demonstrate the ZP-Fixed Point Operator."""
    print("=" * 70)
    print("ZP-FIXED POINT OPERATOR: COHERENCE WITH 0.35 ATTRACTOR")
    print("=" * 70)
    print()
    
    print("1. OPERATOR DEFINITION:")
    print("-" * 70)
    print("  κ(A,B) = φ(Bridge(A,B))")
    print()
    print("  The operator combines ultrametric and fractal embedding.")
    print()
    
    print("2. PAIRWISE COHERENCE:")
    print("-" * 70)
    
    theories = [
        create_theory("PA", 100.0),
        create_theory("ACA₀", 300.0),
        create_theory("ATR₀", 500.0),
        create_theory("Π¹₁-CA₀", 700.0),
    ]
    
    operator = ZPFixedPointOperator(theta=1000.0)
    
    print("  Theory Pair              κ(A,B)")
    print("  " + "-" * 45)
    
    for i, theory_a in enumerate(theories):
        for j, theory_b in enumerate(theories):
            if i < j:
                coherence = operator.apply(theory_a, theory_b)
                print(f"  ({theory_a.name:7s}, {theory_b.name:9s})    {coherence:.4f}")
    print()
    
    print("3. FIXED POINT & FIELD CURVATURE:")
    print("-" * 70)
    
    fixed_point, converged = operator.find_fixed_point(theories)
    kappa = operator.compute_kappa_curvature(fixed_point)
    
    print(f"  Fixed point (φ*): {fixed_point:.4f}")
    print(f"  ZP35 base (Z):    {ZP35_CONSTANT:.4f}")
    print(f"  κ-curvature:      {kappa:+.4f}")
    print()
    print(f"  Geometric decomposition: φ* = Z + κ")
    print(f"  Converged: {'Yes' if converged else 'No'}")
    print()
    
    if abs(kappa) < 0.05:
        print("  ✓ Small field curvature |κ| < 0.05")
        print("    Theory stack is near the base coherence plane.")
    else:
        print(f"  ⚠ Field curvature κ = {kappa:+.4f}")
        print("    Theory stack has bent the coherence plane.")
    print()


def demo_comprehensive_analysis():
    """Demonstrate comprehensive theory collection analysis."""
    print("=" * 70)
    print("COMPREHENSIVE ZP35 ANALYSIS")
    print("=" * 70)
    print()
    
    print("1. THEORY COLLECTION:")
    print("-" * 70)
    
    # Create a diverse collection of theories
    theories = [
        create_theory("Robinson Q", 50.0),
        create_theory("PA", 100.0),
        create_theory("PA + Con(PA)", 150.0),
        create_theory("ACA₀", 300.0),
        create_theory("ATR₀", 500.0),
        create_theory("Π¹₁-CA₀", 700.0),
        create_theory("ZFC-", 850.0),
        create_theory("ZFC", 900.0),
    ]
    
    for theory in theories:
        print(f"  {theory.name:20s} : |T| = {theory.ordinal:.1f}")
    print()
    
    print("2. RUNNING ANALYSIS...")
    print("-" * 70)
    
    analysis = analyze_theory_collection(theories, theta=1000.0)
    
    print()
    print("3. EMBEDDINGS:")
    print("-" * 70)
    for name, value in sorted(analysis['embeddings'].items(), 
                              key=lambda x: x[1]):
        print(f"  {name:20s} → {value:.4f}")
    print()
    
    print("4. PLATEAU STRUCTURE:")
    print("-" * 70)
    for plateau_value, theory_names in sorted(analysis['plateaus'].items()):
        print(f"  φ ≈ {plateau_value:.4f}:")
        for name in theory_names:
            print(f"    - {name}")
    print()
    
    print("5. COHERENCE FIXED POINT (AFFINE DECOMPOSITION):")
    print("-" * 70)
    print(f"  Fixed point (φ*): {analysis['fixed_point']:.4f}")
    print(f"  ZP35 base (Z):    {ZP35_CONSTANT:.4f}")
    print(f"  κ-curvature:      {analysis['kappa_curvature']:+.4f}")
    print()
    print(f"  Affine form: φ* = Z + κ")
    print(f"               {analysis['fixed_point']:.4f} = {ZP35_CONSTANT:.4f} + {analysis['kappa_curvature']:+.4f}")
    print()
    print(f"  Converged: {'Yes' if analysis['fixed_point_converged'] else 'No'}")
    print(f"  |κ| < 0.05: {'Yes (near base phase)' if analysis['is_near_zp35'] else 'No (curved phase)'}")
    print()
    
    if analysis['is_near_zp35']:
        print("  ✓ Small curvature - theory stack is near the base coherence plane.")
    else:
        print(f"  ⚠ Field curvature κ = {analysis['kappa_curvature']:+.4f}")
        print("    Theory stack has bent the coherence plane.")
    print()


def main():
    """Run all demonstrations."""
    print()
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 20 + "ZP35 THEORY DEMONSTRATION" + " " * 23 + "║")
    print("║" + " " * 68 + "║")
    print("║" + "  Theory of Coherence Geometry: Metric, Embedding, Fixed-Point  " + " " * 3 + "║")
    print("╚" + "═" * 68 + "╝")
    print()
    
    demos = [
        ("ZP-Metric", demo_zp_metric),
        ("Cantor Function", demo_cantor_function),
        ("ZP-Embedding", demo_zp_embedding),
        ("ZP-Fixed Point Operator", demo_zp_fixed_point_operator),
        ("Comprehensive Analysis", demo_comprehensive_analysis),
    ]
    
    for i, (name, demo_func) in enumerate(demos):
        if i > 0:
            print()
            print()
        demo_func()
    
    print()
    print("=" * 70)
    print("DEMONSTRATION COMPLETE")
    print("=" * 70)
    print()
    print("Summary:")
    print("  • ZP-Metric provides an ultrametric on theories")
    print("  • Cantor function creates fractal embedding structure")
    print("  • ZP-Embedding maps theories into [0,1] with plateaus")
    print(f"  • Fixed point φ* decomposes as: φ* = Z + κ")
    print(f"    - Z = {ZP35_CONSTANT} is the base coherence plane (ZP35 constant)")
    print("    - κ is the field curvature (how much the stack bends the plane)")
    print("  • ZP35 emerges as the origin of coherence geometry")
    print()
    print("The ZP35 constant is not mystical - it's the flat coherence plane.")
    print("Field curvature κ measures how theory stacks bend that plane.")
    print()


if __name__ == "__main__":
    main()
