# 3D Periodic Flow — Clean Navier-Stokes Simulation

## Goal

A clean, incompressible 3D periodic flow with optional "arithmetic mask" and "descent" term. No grand claims—measure spectra, invariants, stability.

## Grid

- **N³** periodic grid, double precision
- Default **N=64**
- Periodic boundary conditions

## State

- **Velocity** `u(x,t) ∈ ℝ³`
- Work in **Fourier space** with wavevectors `k`

## Operators

### 1. Projection (enforce incompressibility)

```
Π̂u(k) = û(k) - k(k·û(k))/|k|²  for k≠0
```

Helmholtz-Leray projection removes divergence.

### 2. Nonlinearity

```
N(u) = Π(-u·∇u)
```

Pseudospectral: compute in x-space, FFT back to k-space.

### 3. Viscosity

```
L(u) = νΔu  →  in k-space multiply by -ν|k|²
```

### 4. Forcing

- Narrow shell `|k| ≈ k_f`
- Divergence-free
- Fixed seed (deterministic)

### 5. Arithmetic Mask (optional)

`M(k)` applied multiplicatively to `û` after projection:

- **Coprime mask**: Keep modes coprime to primorial (e.g., 5# = 30)
- **Von Mangoldt weight**: Weight by `log(p)` for prime powers
- **Prime shell window**: Attenuate non-prime shells

### 6. Descent Term (optional)

Gradient flow of `T[u] = ½||u||² + α||∇u||²`:

Add `-ηΠ(u - αΔu)`

## Time Stepping

- **RK4**: Runge-Kutta 4th order in spectral space
- **CFL-limited** `dt`: `dt = CFL * min(Δx / max|u|)`

## Diagnostics

### Divergence
```
||∇·u||₂  (target < 1e-12)
```

### Energy
```
E = ½⟨|u|²⟩
```

### Spectrum
```
E(k)  (shell-averaged)
```

### Flatness
3D proxy of intermittency: flatness of vorticity components

### Parseval Check
Energy conservation: `E_x = E_k` (within numerical precision)

### Gravity Toy (optional)
Compute Newtonian quadrupole from synthetic density:
```
ρ = ρ₀ + ε∇·(u⊗u)
```
Generate dimensionless waveform (analogy, not LIGO physics).

## Usage

### Basic Simulation
```bash
make ns-3d-flow
```

### With Arithmetic Mask
```bash
make ns-3d-flow-mask
```

### With Descent Term
```bash
make ns-3d-flow-descent
```

### Python API
```python
from scripts.ns_3d_flow import NS3DFlow

# Create simulator
sim = NS3DFlow(N=64, nu=0.01, k_f=2.0, 
               mask_type="coprime", descent_enabled=True)

# Run simulation
results = sim.simulate(n_steps=100)

# Access diagnostics
for diag in results['diagnostics']:
    print(f"Step {diag['step']}: E={diag['energy']:.6f}, "
          f"div={diag['divergence']:.2e}")
```

## Files

- `systems/ns_3d_flow.ops` — Operator definitions in `.ops`
- `scripts/ns_3d_flow.py` — Python implementation
- `docs/ns_3d_flow.md` — This documentation

## Requirements

- **NumPy**: For efficient 3D FFT operations
  ```bash
  pip install numpy
  ```

## Output

Results saved to `results/ns_3d_flow.json`:

```json
{
  "final_state": [...],
  "diagnostics": [
    {
      "step": 0,
      "time": 0.0,
      "divergence": 1e-15,
      "energy": 0.123456,
      "flatness": 3.2,
      "parseval": {
        "E_x": 0.123456,
        "E_k": 0.123456,
        "relative_error": 1e-12
      }
    }
  ],
  "spectrum": {
    "E_k": [...],
    "k_values": [...]
  },
  "config": {...}
}
```

## Invariants

1. **Divergence**: Should remain < 1e-12 throughout simulation
2. **Energy**: Conserved (up to forcing and dissipation)
3. **Parseval**: `E_x = E_k` (within numerical precision)
4. **Spectrum**: `E(k)` should show expected scaling

## Notes

- **No grand claims**: This is a clean implementation for measuring spectra, invariants, and stability
- **Arithmetic mask**: Models filtering effects (e.g., primorial filter)
- **Descent term**: Adds stability via gradient flow
- **Gravity toy**: Optional quadrupole computation (analogy only)


