# Experimental Protocol: Primorial Spectral Sensing v0.2

## Minimal Plan to Lock in Evidence

### 1) Fingerprint Persistence (Fast A/B)

**Goal**: Does the primorial mask leave a stable, time-averaged dent/plateau in E(k)?

**Runs**:
- Baseline (mask off) vs primorial(2310) (mask on)
- Same seed, ν, k_f, dt, RK4 with per-stage projection + 2/3 dealiasing

**Collect**:
- E(k) every Δt, average over late-time window
- Bootstrap 95% CIs per shell

**Test**:
- Per-shell difference with multiple-comparison control (Benjamini–Hochberg)

**Pass**: ≥3 adjacent shells show significant, repeatable deviation across seeds

**Status**: ✓ PASS (18 adjacent significant shells)

### 2) Toy Decode (Prove You Can Read Structure)

**Encode**: Parity/XOR-SAT on m bits → map each bit to a disjoint k-shell; parity = product sign

**Observables**: [E(k_s)] on those shells + a few linear probes

**Decoder**: Logistic or LASSO on [E(k_s)] to recover each bit and the parity

**Baselines**:
- (i) mask off
- (ii) random mask (same sparsity)
- (iii) linearized flow

**Metric**: Balanced accuracy, sample complexity (observations per bit), wall time

**Pass**: Masked flow beats all baselines with CI; parity recovered at ≥0.9 accuracy over seeds

**Status**: ✗ FAIL (parity accuracy 0.55, need ≥0.9) — needs improvement

### 3) Pre-Registered Advantage Test

**C1/C2**: Completeness/soundness thresholds (already written)

**C3**: Advantage over controls:
- Δsuccess and Δsamples with CIs

**MI**: Classifier-based mutual information I(assignment; observables) (InfoNCE or MINE) to quantify "how much" is extractable

## Solver Hygiene

### divL2 Goal
- **Spec**: ≤1e-10 (spectral metric)
- **Implementation**: Print divL2 at each RK substage
- **If it spikes**: You know which stage leaks

### Energy Budget
- **Log**: dE/dt vs injected − dissipated
- **Plot**: Residuals
- **Mask accounting**: If mask applies post-projection, include it in the accounting (it's a modeling operator; be explicit)

### Seed Policy
- **Pre-draw seeds**: Bind them to runs
- **Store in results JSON**: Avoid subconscious cherry-picks

## Scaling + Ablations

### Primorial Family
- **Values**: p#_4=210, p#_5=2310, p#_6=30030
- **Track**:
  - (i) kept-mode fraction
  - (ii) fingerprint SNR
  - (iii) decoder accuracy
- **Expect**: U-shape (too sparse → underpowered; too dense → fingerprint washes out)

### Mask Density-Matched Random Filters
- **Same # of kept modes**: Random placement
- **If performance stays equal**: The arithmetic is not the lever

### Descent Knob η
- **Grid**: 0, 0.02, 0.05
- **If fingerprints only appear with huge η**: It's the descent—not the primorial—doing the work

## CE1 Promptlets

### ops.eval.fingerprint_persistence
- **Runs**: A=baseline, B=primorial(2310)
- **Outputs**: E(k) mean±CI, ΔE(k) with FDR correction, kept-mode %, SNR
- **Pass**: ≥3 adjacent shells significant across seeds

### ops.decode.toy_parity
- **Encode**: m shells ↔ bits; parity target
- **Observe**: Spectra at those shells
- **Decode**: Logistic/LASSO; report accuracy, samples, time
- **Controls**: Baseline, random mask, linearized flow
- **Pass**: Masked flow > controls with CI

### ops.ablate.primorial_sweep
- **p#**: {210, 2310, 30030}
- **Record**: Density, fingerprint SNR, decoder metrics
- **Output**: Scaling plot (density → MI, density → accuracy)

## Visualization

### Baselines & Controls Panel
- Keep it on page 1

### Spectral Dents Plot
- Time-averaged E(k) with CIs
- Mark arithmetic "holes"

### Confusion Matrices
- Toy decode across runs
- Seed-wise scatter with mean±CI

### Effect Size Dashboard
- Δaccuracy and Δsamples vs controls, with CIs

## Repo Hygiene

### Manifest.json Per Experiment
- Code commit
- Config YAML
- Seeds
- Hashes of initial spectra
- Primorial value
- Wall-clock time
- Hardware note

### CABA Archive
- Auto-emit for each snapshot
- Mode A for fields, Mode B for spectra
- Verify on write

## Stretch (Only if A/B/C Pass)

- Replace parity with small 3-SAT blocks (≤20 vars)
- Keep encoder public and invertible
- Pre-register success criteria
- Keep controls identical

## Files

- `scripts/fingerprint_persistence_ab.py` — A/B test
- `scripts/toy_decode_parity.py` — Parity decode
- `scripts/primorial_sweep_ablation.py` — Primorial sweep
- `scripts/experiment_manifest.py` — Manifest generator
- `systems/ops_eval_fingerprint_persistence.ops` — CE1 promptlet
- `systems/ops_decode_toy_parity.ops` — CE1 promptlet
- `systems/ops_ablate_primorial_sweep.ops` — CE1 promptlet
- `results/fingerprint_persistence_ab.json` — A/B results
- `results/toy_decode_parity.json` — Decode results
- `results/primorial_sweep_ablation.json` — Sweep results

