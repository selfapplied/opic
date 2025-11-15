# OPIC Router System: Summary

## Status: Router-First Lab System Implemented

**Philosophy**: OPIC routes; the lab listens.

The lab is now a self-steering system where OPIC arbitrates between configurations, features, decoders, and guards.

## Architecture

### Core Components

1. **Router** (`opic_route_primorial.ops`)
   - Thompson Sampling with hard constraints
   - Action space: config × features × decoder × p# × η
   - Objective: maximize accuracy + ΔMI − samples − time
   - Exploration schedule: 30% → 10% (decay on parity ≥ 0.9)

2. **Guardrails** (`ops_eval_guard_hygiene.ops`)
   - Always-on circuit breaker
   - divL2 ≤ 1e−10 per RK substage
   - Parseval ≤ 1e−12
   - Energy budget closure

3. **Features** (`ops_features_v1_v3.ops`)
   - v1: shell power + slopes (cheap)
   - v2: v1 + cross-shell + anisotropy (richer)
   - v3: v2 + phase-increments + bispectrum (bite)
   - Router promotes v1→v2→v3 based on accuracy/ΔMI

4. **Decoders** (`ops_decode_stack.ops`)
   - lasso → mlp fallback
   - Parity-consistency constraint
   - Permutation control

5. **MI Evaluation** (`ops_eval_mi.ops`)
   - InfoNCE critic
   - ΔMI vs controls ± CI

6. **Batch Reporting** (`ops_report_batch.ops`)
   - One-page dashboard
   - Spectral dents, accuracy vs samples, MI bars, health strip

7. **Main Lab** (`opic_primorial_lab.ops`)
   - Integrates all components
   - Enforces control quotas (≥25%)
   - CABA archiving (Mode A/B)

## Key Features

### Router Contract
- **Inputs**: manifest, health, last_metrics, budget
- **Outputs**: route_decision, run_id, scheduled guards, control slots
- **Constraints**: health guards always enforced

### Guardrails
- **Circuit breaker**: any health fail → baseline + log
- **Seed discipline**: pre-drawn seeds, no mid-run requests
- **Manifesting**: every run writes manifest + CABA with hash verification

### Feature Promotion
- Start v1→v2
- Promote to v3 only if accuracy < 0.9 but ΔMI shows lift

### Decoder Policy
- Start lasso
- If AUC < 0.8 → mlp
- Parity-consistency: bit votes must satisfy parity
- Penalize if accuracy improves but ΔMI doesn't

### Control Quotas
- Every batch: ≥25% controls (baseline, random-mask, linearized)
- Results invalid without controls

## Metrics Emitted Per Trial

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

## Next Steps

1. **Turn router on**: explore 30%, batch size ~32 runs
2. **Start v2 features**: power, slopes, cross-shell, anisotropy
3. **Quota controls**: enforce ≥25% per batch, record ΔMI
4. **Promote v3**: only if parity < 0.9 but ΔMI shows lift
5. **Lock CABA**: Mode A fields (Δt=1), Mode B spectra (Δt=0.5)

## Success Criteria

**If parity > 0.9** with primorial mask and drops to ~0.5 on random-mask/linearized:
→ Computational channel worth writing up

**If it doesn't**:
→ Mapped limits with style and receipts—also a win

## Files

### Router System
- `systems/opic_route_primorial.ops` — Router
- `systems/ops_eval_guard_hygiene.ops` — Guardrails
- `systems/ops_features_v1_v3.ops` — Feature packs
- `systems/ops_decode_stack.ops` — Decoder stack
- `systems/ops_eval_mi.ops` — MI evaluation
- `systems/ops_report_batch.ops` — Batch reporting
- `systems/opic_primorial_lab.ops` — Main lab integration

### Documentation
- `docs/opic_router_spec_v0.1.md` — Full spec
- `docs/opic_router_summary.md` — This file

## Integration

The router system integrates with:
- `systems/flow3d_core.ops` — Flow solver
- `systems/flow3d_mask.ops` — Primorial masks
- `systems/caba_spec.ops` — CABA archiving

All components are declarative `.ops` voices that OPIC routes naturally.

