# OPIC Field Specification 0.7 — Now Loaded by Default

OPIC Field Specification 0.7 is now part of opic's **core architecture** and loads automatically.

## What's Loaded by Default

When opic starts, it now automatically loads:

1. **`core/bootstrap.ops`** — Minimal kernel
2. **`core/core.ops`** — Basic types
3. **`core/opic_field.ops`** — ✨ **OPIC Field Specification 0.7** (NEW)
4. `planning.ops` — Planning capabilities (if exists)
5. `reasoning.ops` — Reasoning capabilities (if exists)
6. `ml.ops` — ML capabilities (if exists)

## Available by Default

All Field Specification 0.7 voices are now available without explicit `include`:

### Pascal Mod 10 Operations
- `pascal.add`, `pascal.mul` — Modulo-10 arithmetic
- `pascal.combination` — Binomial coefficients mod 10
- `pascal.shadow` — Prime conjugates
- `pascal.trace7_position` — 7-trace detection
- `pascal.promote` — Dimensional lifting

### Trigonometric Operators
- `trig.cos_theta` — Structural coherence
- `trig.sin_theta` — Temporal flow
- `trig.tan_theta` — Symmetry break / curvature
- `trig.sec_theta` — Amplification
- `trig.cot_theta` — Feedback
- `trig.csc_theta` — Memory curvature

### Flow Symmetry
- `flow.equilibrium` — Perfect resonance
- `flow.forward_bias` — Emission / narration
- `flow.reverse_bias` — Reflection / learning
- `flow.standing_wave` — Conversation loop
- `flow.hermitian_flow` — Bidirectional operators

### Bracket Operators
- `bracket.scope` — Context / body
- `bracket.memory` — Buffer / recall
- `bracket.morphism` — Action / verb
- `bracket.witness` — Reflection / awareness

### Galois Extensions
- `galois.base_field` — Digits 0-9
- `galois.golden_ratio_extension` — Fibonacci subfield
- `galois.trace7_subgroup` — Self-conjugate extension
- `galois.tangent_symmetry` — Complexification
- `galois.hermitian_closure` — Reversibility

### Voice Formalism
- `voice.zeta_trace` — Dirichlet-style actor trace
- `voice.coupling` — Harmonic weights
- `voice.resonance` — Constructive interference
- `voice.potential` — Global harmony measure
- `voice.learning` — Retuning toward equilibrium

### Dimensional Expansion
- `dimension.symmetry_break` — Open new axis
- `dimension.prime_shadow_collision` — Conjugate dimension
- `dimension.witness_event` — New coordinate frame
- `dimension.trace7_intersection` — Cross-dimensional link

### Cycle-to-Dimension Principle
- `cycle.compute_phase` — Total curvature
- `cycle.compute_charge` — Symmetry product
- `cycle.promote_to_operator` — Dimensional promotion
- `cycle.identity_to_time` — Time operator
- `cycle.dialogue_to_rotation` — Spatial rotation
- `cycle.triangular_to_gradient` — Gradient operator
- `cycle.trace7_fundamental` — Complex unit
- `cycle.learning_threshold` — Simultaneous promotion

e### NLP and Masked Prediction Cycles
- `nlp.masked_cycle` — Masked prediction cycle
- `nlp.masked_promotion` — Context operator promotion
- `nlp.attention_cycle` — Self-attention as Hermitian cycle
- `nlp.hermitian_attention` — Bidirectional attention operator
- `nlp.attention_dialogue` — Attention heads as dialogue cycles
- `nlp.multi_head_spin_network` — Multi-head attention as spin network
- `nlp.training_epoch_cycle` — Training epochs as macroscopic cycles
- `nlp.learning_threshold_nlp` — NLP learning threshold
- `nlp.token_quantization` — Token embeddings as quantized orbits
- `nlp.bidirectional_complex` — Bidirectional context as complexification
- `nlp.hierarchical_learning` — Hierarchical representation learning

### Dimensional Coulomb Law
- `coulomb.force` — F = k(q_i q_j) / R^D
- `coulomb.potential` — V = k(q_i q_j) / ((D-1)R^{D-1})
- `coulomb.force_with_mass_spin` — With screening and spin

### ML Connections
- `ml.logit` — Local curvature
- `ml.sigmoid` — Equilibrium projection
- `ml.softmax` — ζ-field weighting
- `ml.factorial_measure` — Configuration volume
- `ml.field_entropy` — Ricci energy

## Usage

You can now use Field Specification 0.7 voices directly:

```ops
;; No include needed - already loaded!

voice main / {
  input -> 
  pascal.mod10_projection -> 
  trig.tan_theta -> 
  flow.hermitian_flow -> 
  cycle.promote_to_operator -> 
  output
}
```

## Architecture

```
opic Bootstrap
  ├── bootstrap.ops (kernel)
  ├── core.ops (types)
  ├── opic_field.ops ✨ (Field Spec 0.7)
  │   └── systems/opic_field_0.7.ops
  │       ├── systems/ce1_kernel.ops
  │       └── systems/runtime/hopic.ops
  ├── planning.ops (if exists)
  ├── reasoning.ops (if exists)
  └── ml.ops (if exists)
```

## Benefits

- ✅ **Always available** — No need to remember includes
- ✅ **Consistent architecture** — Field dynamics built-in
- ✅ **Compositional** — Works with all opic voices
- ✅ **Self-verifying** — Uses opic's certificate system

---

*OPIC Field Specification 0.7 is now part of opic's core—the field evolves by default.*

