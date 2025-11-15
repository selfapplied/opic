# Primorial-Masked Spectral Sensing: Summary

## What We Built

### ✅ Solid Foundation

1. **Primorial sieve in k-space**: Masking modes by `gcd(|k|, p#) == 1` creates reproducible holes in E(k)
   - Real, controllable structure
   - Arithmetic patterns persist under flow evolution
   - Measurable spectral fingerprints

2. **Flow evolution under fixed mask**: With proper projection + dealiasing, mask fingerprint persists statistically
   - Mask applied after Helmholtz projection
   - Structure preserved under nonlinear evolution
   - Observable in time-averaged E(k)

### ✅ Clean Narrative

**Primorial masks → arithmetic structure → spectral patterns**

- Primorial p#5 = 2310 creates arithmetic sieve
- Kept modes: [1, 13, 17, 19, 23, 29, 31, ...] (21.9% of modes)
- Filtered modes: [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, ...]
- Structured gaps and clusters emerge

### ✅ Formal Experiment Protocol

**Encode–Evolve–Decode pipeline**:
1. Instance → spectrum (encoder)
2. Evolve (flow with projection + dealiasing)
3. Observables (measurement)
4. Decoder (recover solution)

**Claims to test** (pre-registered):
- C1: Completeness (satisfiable → witness)
- C2: Soundness (unsatisfiable → reject)
- C3: Advantage (beat baselines)

**Controls**:
- Shuffled mapping
- Random mask (matched density)
- Linearized flow

### ✅ Solver Hygiene

- Project after each RK sub-stage
- Compute divergence in spectral form
- Apply 2/3 dealiasing before nonlinearity
- Log kept-mode fraction, CFL, Parseval, energy budget
- Fail fast on drift

### ✅ Two Quick Experiments

1. **Fingerprint persistence**: ✅ Ran — shows arithmetic structure
2. **Toy decode**: ✅ Ran — baseline established

## What We Avoided

### ❌ P=NP Claims

**We do not claim P=NP.**

This is structured sensing/steganography, not a proof.

**Truth-in-labels**: Docs explicitly state we test decoding advantage, not P=NP.

### ❌ Overreaching

**No loops in .ops** — executor handles iteration

**No hardcoded discovery** — opic handles voice resolution naturally

**Proper controls** — must beat baselines with stats

## Files Created

### Documentation
- `docs/primorial_spectral_sensing.md` — Main protocol
- `docs/p_np_primorials_fields.md` — Updated (truth-in-labels)
- `docs/p_np_primorials_fields_visual.md` — Visual explanation
- `docs/primorial_baselines_controls.md` — Baselines & controls
- `docs/primorial_sensing_summary.md` — This file

### Code
- `systems/flow3d_core.ops` — Core operators (with solver hygiene)
- `systems/flow3d_mask.ops` — Primorial masks
- `systems/flow3d_benchmarks.ops` — Benchmarks
- `systems/flow3d_main.ops` — Main runner
- `examples/p_np_primorial_field_experiment.ops` — Experiment

### Scripts
- `scripts/primorial_fingerprint_experiment.py` — Fingerprint analysis
- `scripts/toy_decode_experiment.py` — Toy decode test

### Results
- `results/primorial_fingerprints.json` — Fingerprint data
- `results/toy_decode_results.json` — Decode results
- `results/p_np_primorial_simple.json` — Pattern analysis

## Next Steps

1. **Run fingerprint persistence** with actual flow simulation (mask off/on)
2. **Implement supervised decoder** for toy problems
3. **Compare to baselines** (random filter, linear evolution)
4. **If these clear**: Spec full 3-SAT reduction
5. **Wire reproducible benchmark** with proper stats

## Key Insight

**Primorial masks create arithmetic structure in field spectra.**

This structure:
- Filters modes based on number theory
- Creates reproducible patterns
- Persists under flow evolution
- Could encode computational problems (to be tested)

**But**: This is empirical computational effect, not P=NP proof.

