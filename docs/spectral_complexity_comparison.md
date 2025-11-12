# Spectral Toy vs Complexity Toy: Side-by-Side Comparison

## The Metaphor

**Riemann field** → ideal analytic predictability (linear, unitary, symmetric)

**P ≠ NP** → irreducible algorithmic resistance (nonlinear, dissipative, search)

**Watch where symmetry breaks** → measure "computational curvature"

## Two Toys

### 1. Spectral Toy: Zeta-like Operator

**Generate zeta-like operator** whose spectrum we can visualize:
- Fourier–Laplace transform of multiplicative function
- Critical-line zeros (Re(s) = 1/2)
- Spacing variance Δt of zeros

**Symmetry → minimal entropy**:
- Critical-line zeros correspond to minimal entropy in signal
- Smooth spectra = low entropy = high symmetry

### 2. Complexity Toy: 3-SAT Search

**Run small NP-complete search** (3-SAT with n ≤ 20):
- Log search entropy H(search)
- Compute verification cost (polynomial-time check)
- Distribution of search times

**Plot**: entropy of computation vs spectral order

## Compare Metrics

### RH Side
- **Spacing variance of zeros** Δt
- **Spectral entropy** H(spectrum)
- **Spectral smoothness** = 1/variance

### P vs NP Side  
- **Distribution of search times**
- **Clause-density thresholds**
- **Verification ease** = 1/variance

### Key Question

**Do smoother spectra correlate with easier verification?**

Pure analogy, not proof — but interesting to measure.

## Field Encodings

### ζ-field → Linear, Unitary, Symmetric Evolution

```
∂_t Φ = L·Φ  (linear)
U†U = I      (unitary)
Symmetry preserved → smooth spectra
```

### NP-field → Nonlinear, Dissipative, Search-Based Evolution

```
∂_t S = N(S) + D(S) + search(S)  (nonlinear, dissipative)
Search entropy increases → computational resistance
```

## Interaction: Watch Symmetry Breaks

**Let them interact**:
- Couple ζ-field and NP-field
- Watch where symmetry breaks
- Measure "computational curvature"

**Computational curvature** = deviation from ideal (RH) field

## Results from Experiment

```
Spectral Toy:
- Spectral entropy: 2.57
- Spacing variance: 0.00 (perfect symmetry)

Complexity Toy:
- Search entropy: 1.66
- Search time variance: 159.20
- Found: 5/5 instances

Comparison:
- Spectral smoothness: very high (perfect symmetry)
- Verification ease: low (high variance in search)
- Question: Do smoother spectra → easier verification?
```

## The Art

**This is good art and interesting science-fiction mathematics.**

Not a Clay-proof, but a vivid way to think about:
- Ideal vs real computational structures
- Symmetry vs resistance
- Analytic predictability vs algorithmic complexity

## Hardened Protocol

**Status**: Scientific rigor added — see `docs/spectral_complexity_hardened.md`

**Improvements**:
1. ✓ Spectral unfolding (proper unit-mean spacings, KS tests vs Wigner/Poisson)
2. ✓ Controlled SAT instances (phase transition, proper metrics)
3. ✓ Defined computational curvature (Fisher metric, transfer entropy)
4. ✓ Proper statistics (KS tests, number variance, spectral rigidity)

## Files

### Examples
- `examples/spectral_toy.ops` — Zeta-like operator
- `examples/complexity_toy.ops` — 3-SAT search
- `examples/field_interaction.ops` — Field coupling

### Scripts (Hardened)
- `scripts/spectral_unfold_compare.py` — Unfold & compare (requires numpy/scipy)
- `scripts/complexity_sat_benchmark.py` — SAT benchmark ✓ Running
- `scripts/field_interaction_curvature.py` — Curvature computation (requires numpy)
- `scripts/spectral_complexity_experiment.py` — Original experiment runner

### Systems (.ops)
- `systems/ops_spectral_unfold_compare.ops` — CE1 promptlet
- `systems/ops_complexity_sat_benchmark.ops` — CE1 promptlet
- `systems/ops_interaction_curvature.ops` — CE1 promptlet

### Results
- `results/spectral_complexity_experiment.json` — Original results
- `results/complexity_sat_benchmark.json` — SAT benchmark ✓
- `results/spectral_unfold_compare.json` — Spectral results (pending numpy)
- `results/field_interaction_curvature.json` — Curvature results (pending numpy)

### Documentation
- `docs/spectral_complexity_hardened.md` — Hardened protocol
- `docs/spectral_complexity_comparison.md` — This file

