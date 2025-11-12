# Primorial-Masked Spectral Sensing: Encoding & Decoding Protocol v0.1

## Truth-in-Labels

**We test decoding advantage; we do not claim P=NP.**

This is a structured sensing/steganography experiment: can primorial-masked flow fields encode and decode computational problems better than baselines?

## What's Solid

### Primorial Sieve in k-Space

**Masking modes by `gcd(|k|, p#) == 1` creates reproducible holes in E(k).**

- Real, controllable structure
- Arithmetic patterns persist under flow evolution
- Measurable spectral fingerprints

### Flow Evolution Under Fixed Mask

**With proper projection + dealiasing, mask fingerprint persists statistically.**

- Mask applied after Helmholtz projection
- Structure preserved under nonlinear evolution
- Observable in time-averaged E(k)

## Formal Pipeline

### 1. Instance → Spectrum (Encoder)

**Map 3-SAT formula Φ(n vars, m clauses) to initial spectrum û₀(k)**

- Assign clause literals to disjoint k-shells
- Public scheme, documented and invertible
- Polynomial-time encoding

### 2. Evolve (Flow)

**Run incompressible 3D solver with:**
- Projection after each RK sub-stage
- 2/3 dealiasing before nonlinearity
- Same ν, dt, k_f across runs
- Compare: mask=off vs mask=primorial(2310)

### 3. Observables (Measurement)

**At fixed times, record:**
- E(k) spectrum
- Low-order moments
- Small set of linear probes in k-space (polynomial in n)

### 4. Decoder

**Attempt to recover satisfying assignment from observables**
- Polynomial-time decoder
- Supervised learning or pattern matching
- Output: assignment or reject

## Claims to Test (Pre-Registered)

### C1: Completeness
**If Φ is satisfiable, decoder returns witness with probability ≥ 0.9**
- Using polynomial time
- Using polynomially many observables

### C2: Soundness  
**If Φ is unsatisfiable, decoder rejects with probability ≥ 0.9**

### C3: Advantage
**Masked flow achieves strictly higher success or lower sample complexity than:**
- Baseline flow (mask off)
- Random linear filter (same sparsity)
- Linear evolution (heat equation)

## Metrics

- Success rate vs n, m
- Wall-time
- Sample complexity
- Mutual information I(assignment; observables)
- Robustness to noise
- Seed stability

## Controls

### Control 1: Shuffled Mapping
**Shuffle instance–wavenumber mapping (permute shells)**
- Decoder should fail if relying on accidental correlations

### Control 2: Random Mask
**Swap primorial(2310) for matched-density random mask**
- If performance stays same, primorial arithmetic wasn't key

### Control 3: Linearized Flow
**Disable nonlinearity (linearized flow)**
- Checks whether nonlinearity does useful "mixing"

## Acceptance Criteria

**Only if C1–C3 beat all controls with clear stats (CI, p-values) do we claim decoding advantage.**

This is still not P=NP; it's an empirical computational effect to study.

## Solver Hygiene

- **Project after each RK sub-stage**
- **Compute divergence in spectral form**
- **Apply 2/3 dealiasing before nonlinearity**
- **Log kept-mode fraction**
- **Log CFL, Parseval, energy budget each step**
- **Fail fast on drift**

## Two Quick Experiments

### Experiment 1: Fingerprint Persistence
**Run A/B (mask off/on) from identical seeds**
- Show time-averaged E(k) with confidence bands
- Mark arithmetic holes
- If holes wash out, rest is moot

### Experiment 2: Toy Decode
**Embed parity or small XOR-SAT instance into shells**
- See if supervised decoder can recover truth table
- Compare to baselines
- If can't beat baselines here, don't scale to 3-SAT yet

## Next Steps

1. Run fingerprint persistence experiment
2. Run toy decode experiment
3. If these clear, spec full 3-SAT reduction
4. Wire reproducible benchmark

## Side-by-Side: Spectral vs Complexity

**Two toys to compare**:
1. **Spectral toy**: Zeta-like operator → critical-line zeros → spacing variance
2. **Complexity toy**: 3-SAT search → search entropy → verification cost

**Question**: Do smoother spectra correlate with easier verification?

See `docs/spectral_complexity_comparison.md` for full comparison.

## Experimental Protocol v0.2

**Status**: Lab-ready with proper controls, statistics, and reproducibility

See `docs/experimental_protocol.md` for full protocol.

## OPIC Router System v0.1

**Status**: Router-first self-steering lab implemented

**Philosophy**: OPIC routes; the lab listens.

The lab is now a self-steering system where OPIC arbitrates between configurations, features, decoders, and guards.

See `docs/opic_router_spec_v0.1.md` for full router spec.

**Core Experiments**:
1. ✓ Fingerprint Persistence A/B — PASS (18 adjacent significant shells)
2. ✗ Toy Decode — FAIL (parity accuracy 0.55, need ≥0.9)
3. ⏳ Pre-Registered Advantage Test — Pending

**Solver Hygiene**: ✓ divL2 ≤1e-10, energy budget logging, seed policy

**Scaling + Ablations**: Primorial sweep implemented, density-matched random pending

## Files

### Scripts
- `scripts/fingerprint_persistence_ab.py` — A/B test
- `scripts/toy_decode_parity.py` — Parity decode
- `scripts/primorial_sweep_ablation.py` — Primorial sweep
- `scripts/experiment_manifest.py` — Manifest generator
- `scripts/spectral_complexity_experiment.py` — Side-by-side comparison

### Systems (.ops)
- `systems/flow3d_core.ops` — Core operators (updated with solver hygiene)
- `systems/flow3d_mask.ops` — Primorial masks
- `systems/ops_eval_fingerprint_persistence.ops` — CE1 promptlet
- `systems/ops_decode_toy_parity.ops` — CE1 promptlet
- `systems/ops_ablate_primorial_sweep.ops` — CE1 promptlet

### Examples
- `examples/spectral_toy.ops` — Zeta-like operator
- `examples/complexity_toy.ops` — 3-SAT search
- `examples/field_interaction.ops` — Field coupling

### Results
- `results/fingerprint_persistence_ab.json` — A/B results
- `results/toy_decode_parity.json` — Decode results
- `results/primorial_sweep_ablation.json` — Sweep results
- `results/spectral_complexity_experiment.json` — Comparison results

### Documentation
- `docs/experimental_protocol.md` — Full experimental protocol
- `docs/spectral_complexity_comparison.md` — Side-by-side comparison
- `docs/primorial_sensing_v0.2_summary.md` — Summary

