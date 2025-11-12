#!/usr/bin/env python3
"""Summarize hardened protocol results"""
import json
from pathlib import Path

print("=" * 60)
print("Hardened Protocol Results Summary")
print("=" * 60)

# SAT Benchmark
sat_path = Path('results/complexity_sat_benchmark.json')
if sat_path.exists():
    with open(sat_path) as f:
        sat_data = json.load(f)
    
    print("\n✓ SAT Benchmark Results:")
    results = sat_data['benchmark']['results']
    print("\nPhase Transition Analysis (n=20):")
    for r in [r for r in results if r['n'] == 20]:
        print(f"  α={r['alpha']:.2f}: success={r['success_rate']:.1%}, "
              f"median_steps={r['median_steps']:.0f}, "
              f"entropy={r['mean_search_entropy']:.4f}")
    
    print("\nLearning Curve:")
    lc = sat_data['learning_curve']['learning_curve']
    for p in lc[:3]:
        print(f"  {p['n_observables']} observables: "
              f"accuracy={p['mean_accuracy']:.4f} ± {p['std_accuracy']:.4f}")

# Spectral Unfold
spectral_path = Path('results/spectral_unfold_compare.json')
if spectral_path.exists():
    with open(spectral_path) as f:
        spectral_data = json.load(f)
    
    print("\n✓ Spectral Unfold Results:")
    for name, res in spectral_data.items():
        print(f"\n{name}:")
        print(f"  Spacing variance: {res['spacing_stats']['variance']:.6f}")
        print(f"  KS vs GOE: p={res['ks_tests']['goe']['p_value']:.4f}")
        print(f"  KS vs Poisson: p={res['ks_tests']['poisson']['p_value']:.4f}")
        print(f"  Spectral entropy: {res['spectral_entropy']:.4f}")

# Field Interaction
interaction_path = Path('results/field_interaction_curvature.json')
if interaction_path.exists():
    with open(interaction_path) as f:
        interaction_data = json.load(f)
    
    print("\n✓ Field Interaction Results:")
    for res in interaction_data['results'][:3]:
        print(f"  ε={res['epsilon']:.3f}: "
              f"λ_max={res['lyapunov_max']:.4f}, "
              f"T_z→x={res['transfer_entropy_zx']:.4f}, "
              f"R={res['curvature']:.4f}")

print("\n" + "=" * 60)
print("Status:")
print("  ✓ SAT Benchmark: Running")
print("  ✓ Spectral Unfold: Running (uses .venv/bin/python3)")
print("  ✓ Field Interaction: Running (uses .venv/bin/python3)")
print("=" * 60)

