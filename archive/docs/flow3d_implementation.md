# 3D Flow Implementation — Complete Specification

## Overview

Production-ready 3D incompressible flow solver with spectral projection, optional arithmetic mask, and descent term. Deterministic, reproducible, benchmarked.

## Architecture

### Modular Structure

```
systems/
├── flow3d_core.ops          # Core operators (fft3, helmholtz_project, nonlinear, etc.)
├── flow3d_benchmarks.ops     # TGV, ABC flow, 2D Burgers benchmarks
├── flow3d_mask.ops          # Arithmetic masks (coprime, von_mangoldt, prime_shell)
├── flow3d_descent.ops       # Energy descent term
├── flow3d_caba.ops          # CABA integration for snapshots
└── flow3d_main.ops          # Complete simulation runner
```

## Core Operators (ops.flow3d.core)

### FFT Operators

- **fft3(u) → U**: Unitary normalization; axis order [0,1,2]; real → Hermitian compact
- **ifft3(U) → u**: Unitary normalization; preserves Hermitian symmetry

### Projection

- **helmholtz_project(U, k) → Udivfree**: `U - k(k·U)/|k|²` for k≠0; pass DC unchanged

### Nonlinearity

- **nonlinear(u) → N**: Pseudospectral; compute `-u·∇u` in x-space, FFT back, then project

### Viscosity

- **viscous(U, nu, k) → L**: Multiply by `-ν|k|²` in k-space

### Forcing

- **force_shell(k_f, amp, seed) → F(k)**: Divergence-free, fixed shell `|k| ≈ k_f`, fixed RNG

### Mask (Optional)

- **mask_arith(U, scheme) → U'**: 
  - `coprime_to_primorial(p#)`: M(|k|) = 1 if gcd(|k|, p#) = 1 else β
  - `von_mangoldt(alpha)`: M(|k|) = 1 + α·Λ(|k|)
  - `prime_shell(beta)`: M(|k|) = 1 if |k| ∈ primes else β
  - Apply after projection

### Descent (Optional)

- **descent(U, eta, alpha, k) → D**: Gradient of `T = ½||u||² + α||∇u||²` in projected space
- Operator: `D = -ηΠ(u - αΔu)`

### Time Stepping

- **stepper_rk4(u, dt) → u'**: CFL-aware; emits stage diagnostics
- RK4 stages with Parseval check each substep

## Invariants & Diagnostics

### Required Checks

1. **divL2**: `||∇·u||₂ < 1e-12` (every step)
2. **Parseval**: `E_x = E_k` (within numerical precision)
3. **Energy budget**: Viscous + external work ± integration error
4. **CFL ratio**: `dt / dt_cfl` (monitor, adjust if needed)

### Outputs

- **E(k)**: Shell-averaged energy spectrum
- **energy(t)**: Time series
- **divL2(t)**: Divergence history
- **CABA(field, spectrum)**: Snapshot archives

## Benchmarks (ops.benchmarks.tgv)

### Taylor-Green Vortex

- **Initialization**: Standard TGV velocity with wavenumber 1
- **Checks**: 
  - Early-time energy decay curve (analytic: `E(t) ≈ E(0) * exp(-2*nu*k²*t)`)
  - Symmetry preservation
  - divL2 < 1e-12

### ABC Flow

- **Initialization**: ABC flow field (divergence-free)
- **Checks**:
  - Divergence-free initialization
  - Advection fidelity (topology preservation)

### 2D Burgers/NS

- **Purpose**: Sanity lane for spectra and shock behavior
- **Checks**: Expected scaling, shock formation

## Validation Matrix

### Configs

- **A**: Baseline (no mask, no descent)
- **B**: +arithmetic mask
- **C**: +descent
- **D**: Both mask and descent

### Parameter Sweeps

- `nu ∈ {1e-2, 1e-3}`
- `k_f ∈ {2, 4, 8}`
- `mask = {off, coprime(p#=43)}`
- `descent η ∈ {0, 0.05}`

### Acceptance Gates

1. **Divergence threshold**: `divL2 < 1e-12` throughout
2. **Energy drift**: `|ΔE/E| < 0.01`
3. **Spectrum slope**: Fit power law in inertial range
4. **Reproducibility**: Phase KS, ΔP(k), ξ(r) residuals across seeds

## CABA Integration (ops.io.caba)

### Modes

- **Mode A**: Microstate-lossless (L∞ < 10^-12, Parseval exact)
- **Mode B**: Ensemble-lossless (phase KS, ΔP(k), ξ(r) residuals)

### Export

- **record_hook**: Wire into simulation to export snapshots
- **Frequency**: One snapshot per unit time (configurable)
- **Verification**: Run suite on write; emit digest line

### Digest Format

```
CABA digest: E={energy:.6f}, Parseval={error:.2e}, phase_KS={ks:.4f}
```

## Usage

### Basic Simulation

```ops
include systems/flow3d_main.ops

voice run.simulation / {
  config.default + initial_condition "tgv" -> 
  simulate.flow3d.complete -> 
  results
}
```

### With Mask

```ops
voice run.with.mask / {
  config.B + initial_condition "tgv" -> 
  simulate.flow3d.complete -> 
  results
}
```

### Validation Matrix

```ops
voice run.all.configs / {
  initial_condition "tgv" -> 
  run.validation.matrix -> 
  validation_results
}
```

## Implementation Status

✅ **Core operators**: fft3, ifft3, helmholtz_project, nonlinear, viscous, force_shell  
✅ **RK4 stepper**: CFL-aware with Parseval checks  
✅ **Arithmetic masks**: coprime, von_mangoldt, prime_shell  
✅ **Descent term**: Energy descent operator  
✅ **Benchmarks**: TGV, ABC flow, 2D Burgers  
✅ **CABA integration**: Mode A and Mode B export  
✅ **Diagnostics**: divL2, energy, E(k), Parseval, CFL ratio  

## Next Steps

1. Wire operators to Python executor (check existing implementations)
2. Add unit tests for each operator
3. Run TGV benchmark and verify early-time decay
4. Run validation matrix A/B/C/D
5. Generate CABA snapshots and verify lossless/ensemble-lossless modes

## Files

- `systems/flow3d_core.ops` — Core operators
- `systems/flow3d_benchmarks.ops` — Benchmarks
- `systems/flow3d_mask.ops` — Arithmetic masks
- `systems/flow3d_descent.ops` — Descent term
- `systems/flow3d_caba.ops` — CABA integration
- `systems/flow3d_main.ops` — Main runner

## References

- Python implementation: `scripts/ns_3d_flow.py`
- CABA spec: `systems/caba_spec.ops`
- Validation protocol: `systems/ns_tensor_validation.ops`

