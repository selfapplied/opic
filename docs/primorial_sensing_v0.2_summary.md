# Primorial Spectral Sensing v0.2: Experimental Summary

## Status: Lab-Ready Protocol

**Reframing**: Primorial masks → structured sensing/steganography (not P=NP proof)

**Posture**: Clean, falsifiable claims, real controls

## Three Core Experiments

### 1. Fingerprint Persistence A/B ✓ PASS

**Goal**: Stable, time-averaged dent/plateau in E(k) from primorial mask

**Results**:
- 18 adjacent significant shells (need ≥3)
- Kept-mode fraction: 21.9%
- SNR: 0.78
- **Status**: ✓ PASS

**Files**:
- `scripts/fingerprint_persistence_ab.py`
- `systems/ops_eval_fingerprint_persistence.ops`
- `results/fingerprint_persistence_ab.json`

### 2. Toy Decode ✗ FAIL (Needs Improvement)

**Goal**: Encode parity → decode from observables

**Results**:
- Parity accuracy: 0.55 (need ≥0.9)
- Primorial accuracy: 0.56
- Baseline accuracy: 1.00
- **Status**: ✗ FAIL — decoder needs improvement

**Files**:
- `scripts/toy_decode_parity.py`
- `systems/ops_decode_toy_parity.ops`
- `results/toy_decode_parity.json`

### 3. Pre-Registered Advantage Test (Pending)

**C1/C2**: Completeness/soundness thresholds
**C3**: Advantage over controls (Δsuccess, Δsamples with CIs)
**MI**: Mutual information I(assignment; observables)

## Solver Hygiene ✓ Implemented

### divL2 Goal
- **Spec**: ≤1e-10 (spectral metric)
- **Implementation**: Print divL2 at each RK substage
- **Status**: ✓ Added to `stepper_rk4`

### Energy Budget
- **Log**: dE/dt vs injected − dissipated
- **Plot**: Residuals
- **Status**: ✓ Added `log.energy.budget` voice

### Seed Policy
- **Pre-draw seeds**: Bind to runs
- **Store in JSON**: Avoid cherry-picks
- **Status**: ✓ Implemented in all scripts

## Scaling + Ablations

### Primorial Sweep
- **Values**: p#_4=210, p#_5=2310, p#_6=30030
- **Results**: 
  - 210: 25.0% kept, SNR 0.75, accuracy 1.00
  - 2310: 21.9% kept, SNR 0.78, accuracy 0.94
  - 30030: 18.8% kept, SNR 0.81, accuracy 0.88
- **U-shape**: Not detected (needs more data)

**Files**:
- `scripts/primorial_sweep_ablation.py`
- `systems/ops_ablate_primorial_sweep.ops`
- `results/primorial_sweep_ablation.json`

### Density-Matched Random (Pending)
- Same # of kept modes, random placement
- Test: If performance stays equal, arithmetic is not the lever

### Descent Knob η (Pending)
- Grid: 0, 0.02, 0.05
- Test: If fingerprints only appear with huge η, it's descent—not primorial

## CE1 Promptlets ✓ Implemented

- `ops.eval.fingerprint_persistence` — A/B test
- `ops.decode.toy_parity` — Parity decode
- `ops.ablate.primorial_sweep` — Primorial sweep

## Visualization (Pending)

- Baselines & controls panel
- Spectral dents plot (time-averaged E(k) with CIs)
- Confusion matrices (toy decode across runs)
- Effect size dashboard (Δaccuracy, Δsamples vs controls)

## Repo Hygiene ✓ Implemented

### Manifest.json
- Code commit, config YAML, seeds, hashes, wall-clock time, hardware
- **Status**: ✓ `scripts/experiment_manifest.py`

### CABA Archive (Pending)
- Auto-emit for each snapshot
- Mode A for fields, Mode B for spectra
- Verify on write

## Next Steps

1. **Improve toy decode**: Fix decoder to achieve ≥0.9 parity accuracy
2. **Run density-matched random**: Test if arithmetic is the lever
3. **Run descent knob sweep**: Test if descent is doing the work
4. **Add visualization**: Spectral dents, confusion matrices, effect size dashboard
5. **Wire CABA**: Auto-emit archives for each snapshot
6. **Pre-register advantage test**: Formalize C1/C2/C3 and MI metrics

## Key Insight

**This is good art and interesting science-fiction mathematics.**

Not a Clay-proof, but a vivid way to think about:
- Ideal vs real computational structures
- Symmetry vs resistance
- Analytic predictability vs algorithmic complexity

## Files Summary

### Scripts
- `scripts/fingerprint_persistence_ab.py` — A/B test
- `scripts/toy_decode_parity.py` — Parity decode
- `scripts/primorial_sweep_ablation.py` — Primorial sweep
- `scripts/experiment_manifest.py` — Manifest generator
- `scripts/spectral_complexity_experiment.py` — Side-by-side comparison

### Systems (.ops)
- `systems/ops_eval_fingerprint_persistence.ops` — CE1 promptlet
- `systems/ops_decode_toy_parity.ops` — CE1 promptlet
- `systems/ops_ablate_primorial_sweep.ops` — CE1 promptlet
- `systems/flow3d_core.ops` — Updated with solver hygiene

### Results
- `results/fingerprint_persistence_ab.json` — A/B results
- `results/toy_decode_parity.json` — Decode results
- `results/primorial_sweep_ablation.json` — Sweep results
- `results/spectral_complexity_experiment.json` — Comparison results

### Documentation
- `docs/experimental_protocol.md` — Full protocol
- `docs/primorial_spectral_sensing.md` — Main spec
- `docs/spectral_complexity_comparison.md` — Side-by-side comparison
- `docs/primorial_sensing_v0.2_summary.md` — This file

