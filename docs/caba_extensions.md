# CABA v0.1 Extensions

## Overview

Extensions to CABA v0.1 specification implementing the roadmap items:

1. **2D/3D Radial Binning** — 5–20× compression on isotropic textures
2. **Phase-Delta Coding** — Push `~1.94×` toward `~3×` on real data
3. **Bispectrum-Lite** — 50–200 triangles capture targeted non-Gaussianity

## Extension 1: 2D/3D Radial Binning (Mode B)

### Purpose
For isotropic fields, binning power spectrum into radial shells dramatically reduces storage while preserving two-point statistics.

### Implementation
- Compute radial wavenumber: `k = √(kx² + ky² + kz²)`
- Bin `P(k)` into radial shells
- Store only binned values + binning schema

### Compression Ratio
- **Expected**: 5–20× compression on isotropic textures
- **Example**: 64³ grid → 32 radial bins = 64× compression

### Usage
```ops
voice compress.with.radial.binning / {
  field.values + n.bins "32" -> 
  caba.pack.mode.B.radial -> 
  ⟨caba_archive_B_radial⟩
}
```

## Extension 2: Phase-Delta Coding (Mode A)

### Purpose
Delta-encode unwrapped phases to improve compression ratio while staying lossless.

### Implementation
1. Extract phases from complex spectrum
2. Unwrap phases radially along k
3. Delta-encode: `Δφ = φ[i] - φ[i-1]`
4. Store deltas + initial phase

### Compression Ratio
- **Current**: ~1.94× (Mode A baseline)
- **Target**: 2.6–3.5× on natural fields
- **Remains**: Lossless (exact reconstruction)

### Usage
```ops
voice compress.with.phase.delta / {
  field.values -> 
  caba.pack.mode.A.delta -> 
  ⟨caba_archive_A_delta⟩
}
```

## Extension 3: Bispectrum-Lite (Mode B+)

### Purpose
Preserve targeted non-Gaussian features by storing sparse bispectrum patch list.

### Implementation
- Compute bispectrum: `B(k1,k2,k3) = ⟨F(k1)F(k2)F*(k1+k2)⟩`
- Select top 50–200 triangles by magnitude
- Store triangle indices + bispectrum values
- Apply constraints during phase generation

### Storage Overhead
- **Triangles**: 50–200
- **Per triangle**: 3 indices (k1, k2, k3) + 1 complex value
- **Total**: ~400–1600 numbers (tiny compared to full field)

### Usage
```ops
voice compress.with.bispectrum / {
  field.values + max.triangles "100" -> 
  caba.pack.mode.B.bispectrum -> 
  ⟨caba_archive_B_bispectrum⟩
}
```

## Complete Extended Container

### Header Extensions
- `compressor_id`: "radial_bin", "phase_delta", "bispectrum", "ANS", "none"
- `binning_schema`: Radial binning parameters
- `bispectrum_patches`: Triangle list

### Usage
```ops
voice compress.extended / {
  field.values + compression.mode + extension.flags + random.seed -> 
  caba.container.extended -> 
  ⟨caba_container_extended⟩
}
```

## Files

- `systems/caba_extended.ops` — Extension definitions
- `scripts/opic_executor.py` — Python primitives:
  - `bin_power_spectrum_radial`
  - `delta_encode_phases`
  - `reconstruct_phases_from_deltas`
  - `compute_bispectrum_triangle`
  - `select_bispectrum_triangles`

## Next Steps

1. **Test extensions** with real field data
2. **Measure compression ratios** on various field types
3. **Validate** that two-point stats are preserved
4. **Optimize** binning and triangle selection algorithms


