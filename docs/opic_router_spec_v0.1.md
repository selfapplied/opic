# OPIC Router Spec v0.1 — "Primorial Sensing"

## Philosophy

**OPIC routes; the lab listens.**

Turn the lab into a living, self-steering system where OPIC arbitrates between configurations, features, decoders, and guards.

## Roles (Voices)

### Core Flow
- `source.flow` — emits fields/spectra (A/B/C/D configs)
- `filter.primorial` — applies mask (p#_4, p#_5, p#_6)
- `observe.features` — extracts features (power, slopes, cross-shells, anisotropy, phase-increments, bispectrum)

### Decoders
- `decode.lasso` — supervised decoder (feature selection)
- `decode.mlp` — fallback decoder (1×64 hidden)

### Evaluation
- `eval.stats` — CIs, BH-corrected p-values, MI (InfoNCE)
- `guard.hygiene` — divL2 stage checks, Parseval, energy budget

### Archive
- `archive.caba` — Mode A for fields, Mode B for spectra/features

### Router
- `policy.router` — bandit that chooses configs, features, decoders

## Router Contract (policy.router)

### Inputs
- `manifest` — commit, seeds
- `health` — divL2, Parseval
- `last_metrics` — SNR, ΔE(k), accuracy, ΔMI
- `budget` — steps, walltime

### Action Space
```
(config ∈ {baseline, primorial, random, linearized})
× (features ∈ {v1, v2, v3})
× (decoder ∈ {lasso, mlp})
× (p# ∈ {210, 2310, 30030})
× (η ∈ {0, 0.02, 0.05})
```

### Objective
Maximize score = `w1*accuracy + w2*ΔMI − w3*samples − w4*time`

Subject to health constraints.

### Algorithm
**Thompson Sampling** (or UCB) with hard constraints:

1. **guard.hygiene.divL2 ≤ 1e−10** each RK substage, else circuit-break to baseline
2. **Parseval relative error ≤ 1e−12**
3. **Exploration schedule**: 30% explore until parity ≥ 0.9 on validation ≥ 3 seeds; then decay to 10%
4. **Early-stop**: if three consecutive seeds fail to beat random-mask on accuracy and ΔMI, down-rank that branch for 10 trials

## Guardrails (Always-On by OPIC)

### Circuit Breaker
Any health fail → route to `source.flow` → baseline and log incident.

### Seed Discipline
Seeds pre-drawn; router may not request a new seed mid-run.

### Manifesting
Every routed run writes `manifest.json` + CABA artifacts; hashes must match.

## Feature Packs

### v1 (Cheap)
- Shell power + slopes

### v2 (Richer)
- v1 + cross-shell couplings + anisotropy bins (6–12/shell)

### v3 (Bite)
- v2 + phase-increments (circular means) + 50–100 bispectrum triplets

### Router Policy
- Start v1→v2
- Promote to v3 only if accuracy < 0.9 but ΔMI shows lift

## Decoder Policy

1. **Start lasso** (feature selection)
2. **If validation AUC < 0.8**, route to mlp (1×64 hidden) with early stop
3. **Parity-consistency constraint**: bit votes must satisfy parity
4. **If mlp improves accuracy but not ΔMI vs baselines**, penalize (possible overfit)

## Baselines & Controls (Must-Run Quotas)

Every batch must include:
- `baseline` flow (mask off)
- `random-mask` (density-matched)
- `linearized`

Router enforces ≥25% of trials as controls; results are invalid without them.

## Metrics OPIC Must Emit Per Trial

### Health
- divL2 at each substage
- Parseval delta
- CFL

### Fingerprint
- ΔE(k) with BH-corrected significance
- Kept-mode %

### Decode
- Accuracy ± CI
- Samples
- Walltime
- Permutation p-value

### Info
- ΔMI vs controls ± CI

### Provenance
- Commit
- Seeds
- Config hash
- Feature schema hash

## CE1 Promptlets

### `systems/opic_route_primorial.ops`
- Router: choose (config, features, decoder, p#, η) via Thompson Sampling
- Emit: manifest, run-id, scheduled guards, control slots

### `systems/ops_eval_guard_hygiene.ops`
- Assert: divL2_stage ≤ 1e−10, Parseval ≤ 1e−12, energy budget closure
- On fail: raise circuit_breaker, re-route to baseline + log

### `systems/ops_features_v1_v3.ops`
- v1/v2/v3 extractors with deterministic schema + CABA(B) write/verify

### `systems/ops_decode_stack.ops`
- lasso → mlp fallback; parity-consistent post-processing; permutation control

### `systems/ops_eval_mi.ops`
- InfoNCE critic (small) with seeds fixed; report MI and ΔMI vs baselines

### `systems/ops_report_batch.ops`
- One-page dashboard: spectral dents with CIs, accuracy vs samples, MI bars, health strip, manifest digest

## Immediate Next Moves (Router-Aware)

1. **Turn router on** with explore 30%; batch size ~32 runs. Health guard live.
2. **Start v2 features** (power, slopes, cross-shell, anisotropy); keep v3 gated.
3. **Quota controls** in every batch and record ΔMI—unlock the "Pending" advantage test.
4. **Promote to v3** only if parity stalls <0.9 but ΔMI shows real lift.
5. **Lock CABA**: Mode A fields every Δt=1; Mode B spectra/features every Δt=0.5. Verify on write.

## Success Criteria

**If parity pops >0.9** with primorial mask and drops to ~0.5 on random-mask/linearized:
→ We've got a computational channel worth writing up.

**If it doesn't**:
→ We've mapped the limits with style and receipts—also a win.

## Mode 7 Integration

**Mode 7** wraps the router system with a perspective layer:
- Parallax dashboards (foreground/midground/background)
- Fusion moment detection
- Perspective-invariant features
- Harvest loops and replay

See `docs/opic_mode7_spec.md` for full Mode 7 specification.

## Files

### Router System
- `systems/opic_route_primorial.ops` — Router
- `systems/ops_eval_guard_hygiene.ops` — Guardrails
- `systems/ops_features_v1_v3.ops` — Feature packs
- `systems/ops_decode_stack.ops` — Decoder stack
- `systems/ops_eval_mi.ops` — MI evaluation
- `systems/ops_report_batch.ops` — Batch reporting
- `systems/opic_primorial_lab.ops` — Main lab integration

### Mode 7 System
- `systems/opic_mode7_perspective.ops` — Core perspective layer
- `systems/opic_mode7_dashboard.ops` — Parallax dashboard
- `systems/opic_mode7_fusion.ops` — Fusion detection
- `systems/opic_mode7_features.ops` — Perspective-invariant features
- `systems/opic_mode7_harvest.ops` — Harvest loops
- `systems/opic_mode7_lab.ops` — Integrated lab

