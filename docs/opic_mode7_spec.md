# Mode 7: Perspective Layer for Lab Harvest

## Philosophy

**Mode 7** turns flat, local traces into a single, navigable world.

Think of it as a perspective layer that creates parallax depth—foreground moves fast (alerts), background moves slow (aggregates), creating a fused horizon you can steer, replay, and compare.

## Core Concepts

### 1. Parallax Dashboards (One Reality, Layered Speeds)

**Foreground**: Live health strip
- divL2 per RK substage
- Parseval
- CFL
- Scroll speed: fast (alerts nudge)

**Midground**: Experiment state
- Mask on/off
- p#, η
- Decoder type
- ΔMI
- Scroll speed: medium

**Background**: Slow-rolling aggregates
- E(k) dents with CIs
- Decode accuracy vs samples
- Scroll speed: slow (calm layers glide)

**OPIC sets scroll speed per layer**: Calm layers glide, alerts nudge faster—attention without alarms.

### 2. Perspective-Invariant Views

**Same data, different projections**:
- Unfolded spectra
- ΔE(k)
- MI bars
- Decoder SHAP

All projected onto a shared "map."

**Zoom** = sample size  
**Rotation** = condition (baseline / primorial / random / linearized)

You don't redraw plots—you reproject them, keeping cognitive continuity.

### 3. Tiled k-Space (SNES Map Sheets)

**Shell-binned k-space as tiles**:
- Primorial-kept tiles get higher "elevation"
- Parallax shows dents/plateaus as terrain
- Quickly surfaces stable fingerprints across seeds

### 4. Fusion Moments

**Detect when layers lock**:
- Trigger fusion flag when three layers align:
  1. Significant shells (q<0.05)
  2. ΔMI>0
  3. Decode↑ on validation

**Store fusion as CABA bundle**:
- Fields (Mode A)
- Spectra/features (Mode B)
- OPIC note (narration)

### 5. Time Warps

**Respect causality**:
- Fast-forward during stable regimes
- Slow-motion around divergences or routing pivots

**OPIC narrates**: "router: slowing near ε=0.2; curvature slope changed sign."

### 6. Perspective-Invariant Features

**Features that survive zoom/rotation**:
- Local spectral slopes
- Anisotropy bins
- Phase-increment means
- Small bispectrum set (50-100 triplets)

**Train once; reproject for each condition** to compare geometry, not just numbers.

### 7. Harvest Loops

**Mode 7 pass emits**:
- Current viewpoint (zoom, rotation)
- Layer states
- Fusion flags
- CABA artifacts

**Replays are exact**: Same seeds + same camera path ⇒ same film.

## Integration with Router System

Mode 7 wraps the router system:
- Router decisions → midground layer
- Health guards → foreground layer
- Aggregates → background layer
- Fusion moments → snapshots
- Perspective-invariant features → stronger decoder

## Next Moves

1. **Wrap current experiments** in parallax dashboard:
   - Foreground: health
   - Mid: run config + ΔMI
   - Back: aggregates

2. **Add fusion flags** and store moments as named snapshots

3. **Switch decoder training** to perspective-invariant features; rerun parity task

4. **Publish one-minute Mode 7 reel** from golden seed:
   - baseline → primorial → random-mask
   - Same camera path

## Payoff

**You don't just have results—you have a world you can fly through.**

Mode 7 turns distributed traces into a fused horizon you can:
- Steer
- Replay
- Compare

Without losing the thread of the dance.

## Files

- `systems/opic_mode7_perspective.ops` — Core perspective layer
- `systems/opic_mode7_dashboard.ops` — Parallax dashboard
- `systems/opic_mode7_fusion.ops` — Fusion detection
- `systems/opic_mode7_features.ops` — Perspective-invariant features
- `systems/opic_mode7_harvest.ops` — Harvest loops and replay
- `systems/opic_mode7_lab.ops` — Integrated lab system

