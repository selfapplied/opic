# Primorial Sensing: Baselines & Controls

## Scientific Posture at a Glance

### What We're Testing

**Hypothesis**: Primorial-masked flow fields provide decoding advantage for computational problems vs baselines.

**Not claiming**: P=NP proof

**Claiming**: Empirical computational effect (if controls pass)

## Baselines & Controls

### Baseline 1: Mask Off
**No arithmetic filter**
- Standard Navier-Stokes evolution
- All modes evolve normally
- **Control**: Does mask actually help?

### Baseline 2: Random Linear Filter
**Matched-density random mask**
- Same sparsity as primorial mask
- Random mode selection (not arithmetic)
- **Control**: Is arithmetic structure key, or just sparsity?

### Baseline 3: Linear Evolution
**Heat equation (no nonlinearity)**
- Linear diffusion only
- No advection/mixing
- **Control**: Does nonlinearity do useful "mixing"?

### Control 1: Shuffled Mapping
**Permute instance–wavenumber assignment**
- Same encoding scheme, different shell mapping
- **Control**: Decoder fails if relying on accidental correlations

### Control 2: Seed Stability
**Multiple seeds, same instance**
- Check reproducibility
- **Control**: Results aren't seed-dependent artifacts

## Acceptance Criteria

**Only if primorial mask beats all baselines AND passes all controls** do we claim decoding advantage.

This requires:
- Clear statistical significance (CI, p-values)
- Reproducible results
- Robust to noise
- Polynomial-time decoder

## Visualization

```
Baseline Comparison:
─────────────────────────────────────────────────────
Method              Success Rate    Sample Complexity
─────────────────────────────────────────────────────
Primorial Mask      TBD            TBD
Mask Off            TBD            TBD  
Random Filter       TBD            TBD
Linear Evolution    TBD            TBD
─────────────────────────────────────────────────────

Controls:
─────────────────────────────────────────────────────
Control             Pass/Fail       Notes
─────────────────────────────────────────────────────
Shuffled Mapping    TBD            Should fail
Random Mask         TBD            Should match baseline
Seed Stability      TBD            Should be stable
─────────────────────────────────────────────────────
```

## Files

- `scripts/primorial_fingerprint_experiment.py` — Fingerprint analysis
- `scripts/toy_decode_experiment.py` — Toy decode test
- `results/primorial_fingerprints.json` — Fingerprint data
- `results/toy_decode_results.json` — Decode results

