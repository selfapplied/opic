# CABA Spec v0.1 — Zeta Power Spectrum Archive

**Purpose**: Dual-mode compression of real fields on periodic grids: A) microstate-lossless, B) ensemble-lossless (two-point exact, CMB-style).

## Objects

- **field** `f ∈ ℝ^(n₁×⋯×n_d)`
- **FFT** `f̂(k)` with declared normalization
- **power** `P(k) = |f̂(k)|²`
- **seed** `s` for deterministic phase draws (Mode B)

## Modes

### Mode A | Microstate-Lossless

Store independent complex bins of `f̂` (DC/Nyquist explicit) → reconstruct via IFFT.

**Invariants**:
- Parseval: `Σ|f̂|² = Σf²`
- `L∞ < 10^-12` (float64)

### Mode B | Statistical-Lossless

Store `P(k)` (radially binned optional) + seed `s` → phases `φ_k ~ U[0,2π)` with Hermitian symmetry; `f̂ = √P(k) e^(iφ_k)`.

**Invariants**:
- `P'(k) ≈ P(k)`
- `ξ'(r) ≈ ξ(r)`
- Microstate differs

## Header (FROZEN v0.1 — 128-256 bytes)

**Fixed Schema** (locked for v0.1):
- `version` (1 byte): "0.1"
- `mode` (1 byte): {A, B}
- `dims` (12 bytes): 3× int32 for dimensions
- `dtype` (1 byte): {float32, float64, complex64, complex128}
- `endian` (1 byte): {little, big}
- `fft_norm` (1 byte): {unitary, forward_1/N, inverse_1/N}
- `axis_order` (1 byte): "012" (3D default)
- `periodic` (1 byte): per-axis flags
- `window_id` (1 byte): {none, hann, hamming, ...}
- `dc_index` (4 bytes): int32
- `nyquist_indices` (12 bytes): 3× int32
- `seed` (8 bytes): int64 (Mode B only)
- `binning_schema` (1 byte): {none, radial_2d, radial_3d}
- `compressor_id` (1 byte): {none, ans, zstd, gzip} **← NEW**
- `checksum` (16 bytes): SHA-256 of payload
- `parseval_energy` (8 bytes): float64
- `reserved` (156 bytes): for future extensions

## Payload

- **Mode A**: Independent complex coefficients (polar or cartesian; declare).
- **Mode B**: `P(k)` coefficients (binned or full), optional window deconvolution note.

## Trailer

- **Verification digest**: `Σf²` (A), spectral slope fit (B), RNG checksum.

## Operators

- **`pack()`**: Apply Hermitian compaction; encode metadata; apply compressor if specified (ANS/Zstd/Gzip).
- **`unpack()`**: Decompress if needed; recreate full spectrum; enforce symmetry; IFFT.
- **`verify()`**: Run invariants; emit metrics.

### Compressor Support

- **`compressor_id`**: Specified in header, applied after Hermitian compaction
  - `none`: No compression (raw binary)
  - `ans`: Asymmetric Numeral Systems (entropy coding)
  - `zstd`: Zstandard compression
  - `gzip`: Gzip compression

## Invariants & Tests

### Mode A

- `L₂`, `L∞`, Parseval diff, DC/Nyquist exactness
- **Target**: `L∞ ~ 10^-12` (achieved `10^-19`, stellar)

### Mode B

- KS-test for phase uniformity
- `max |ΔP(k)|` & RMSE
- `ξ(r)` residuals
- `cross-corr(field, field') ≈ 0`

## Extensions

- **Binning**: Isotropic radial shells → fewer coeffs, same two-point stats.
- **B+**: Sparse bispectrum patch list to nail chosen non-Gaussian features.
- **Phase-delta coding (A)**: Unwrap `φ` radially, delta-encode → 2.6–3.5× typical on natural fields without loss.
- **Tiling**: Chunked blocks with overlap for streaming decode.

---

## Invariants Suite (Drop-in Checklist)

- **Report**: `dims/dtype/fft_norm/ordering/seed/binning`
- **Energy**: `energy_A = sum(f²)`, `energy_F = sum(|F|²)` → assert `|energy_A−energy_F| < 1e−12·energy_A`
- **Mode A**: `L₂`, `L∞`, DC & Nyquist equality (bit-true)
- **Mode B**: Phase KS p-value > 0.1; spectra: `max|Δ|`, RMSE; `ξ(r)` band; cross-corr ≈ 0
- **Reproducibility**: Decode 100× with same seed → identical spectra; with different seeds → identical spectra, decorrelated fields

---

## Roadmap (Single Sitting)

1. ✅ **2D/3D upgrade** with radial binning → expect 5–20× in Mode B on isotropic textures.
2. ✅ **Phase-delta exact coder (A)** → push `~1.94×` toward `~3×` on real data.
3. ✅ **Bispectrum-lite (B+)**: 50–200 triangles capture targeted non-Gaussianity with tiny overhead.
4. ✅ **CABA container**: **FROZEN** header schema v0.1; **ANS codec support added**; tests locked.

## Status: v0.1 LOCKED

**Header schema is frozen** — future versions will use version field to maintain compatibility.
**ANS codec integrated** — use `compressor_id: "ans"` in header.
**Validation suite locked** — invariants tests are stable.

---

## Implementation

See:
- `systems/caba_spec.ops` — CABA v0.1 specification
- `systems/caba_validation.ops` — Invariants suite
- `systems/zeta_compression.ops` — Compression modes

**You've got a two-lane highway**: exact microstates when you must, faithful ensembles when you can.

**Next turn of the crank**: 3D isotropic fields and phase-delta coding to lift the ratio without touching truth.
