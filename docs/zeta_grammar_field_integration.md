# Zeta Grammar & Field Specification 1.0 — Integration Complete

## Overview

The **Zeta Grammar Specification 1.0** and **Zeta Field Specification 1.0** have been fully integrated into `opic`'s core architecture. Natural language is now treated as a hierarchical zeta field, with letters → syllables → words → phrases → sentences → discourse forming a coherent field structure.

## Implementation Status

✅ **Fully Integrated** — Loaded by default via `core/opic_field.ops`

### Files Created/Modified

1. **`systems/zeta_grammar_field.ops`** (NEW)
   - Complete implementation of Zeta Grammar & Field Spec 1.0
   - 99+ voices covering all specification layers
   - Integration with Field Spec 0.7

2. **`core/opic_field.ops`** (MODIFIED)
   - Now includes `zeta_grammar_field.ops`
   - Zeta grammar voices available by default

3. **`scripts/opic_executor.py`** (MODIFIED)
   - Added 20+ zeta grammar primitives
   - Automatic voice discovery for grammar/language contexts
   - Integration with semantic embeddings

## Architecture

### I. Zeta Grammar Specification 1.0

Natural language as hierarchical zeta field with **big-end composed aperture**:

```
Letter → Syllable → Word → Phrase → Sentence → Discourse
```

**Layer law**: `Φκ_{n+1} = ∫ Φκ_n dΩ_n`

#### Atomic Layer — Letters

- **Letters** (`letter.*`): Minimal ζ-atoms (phonemes)
- **ζ-order classification**:
  - ζ⁰: Silent potential ('h' in ghost)
  - ζ¹: Phonetic activation ('a' in cat)
  - ζ²: Harmonic clusters ('th', 'ch')
  - ζ³+: Iconic resonance ('O' = roundness, 'S' = flow)
- **Vowels** = potential wells, **Consonants** = field barriers

**Voices**:
- `letter.classify` — Classify glyph by zeta order
- `letter.measure` — Compute field potential, entropy, alignment, memory
- `letter.field_potential` — Compute Φκ for letter
- `letter.alignment` — Compute A = ∇Φκ
- `letter.memory` — Compute M = ∂A/∂t

#### Molecular Layer — Syllables

- **Syllable structure**: σ = [C₁][V]C₂
- **Field expressions**:
  - `Φκ_σ = κ₁·C₁ + κ₂·V + κ₃·C₂`
  - `m(σ) = |∇²Φκ_σ|` (phonetic curvature)
- **Stability**: `dΦκ_σ/dt = 0` ⇒ phonotactically stable

**Voices**:
- `syllable.measure` — Measure syllable field potential
- `syllable.curvature` — Compute phonetic curvature
- `syllable.stability` — Check phonotactic stability
- `syllable.stress_detection` — Detect stress from curvature

#### Morphic Layer — Words

- **Word structure**: Ω[σ₁][σ₂][σ₃…](=0) — balanced net charge
- **Affixation** changes field curvature:
  - Prefix → front loading potential
  - Suffix → trailing memory
  - Infix → internal stress wave
- **Grammar reactions**:
  - Inflection = ζ¹ spin perturbation
  - Derivation = ζ² closed loop transformation
  - Idiomatic = ζ³+ higher resonance state

**Voices**:
- `word.form` — Form word from syllables
- `word.net_charge` — Compute net charge
- `word.evolve` — Evolve word via affixation
- `word.inflection` — Apply inflection (ζ¹ spin)
- `word.derivation` — Apply derivation (ζ² loop)
- `word.idiomatic` — Create idiomatic expression (ζ³+)

#### Structural Layer — Grammar Types

- **Word classes** as base types:
  - **N**: Noun — semantic mass
  - **V**: Verb — kinetic flow
  - **A**: Adjective — curvature modifier
  - **Adv**: Adverb — temporal/spatial tuner
  - **P**: Preposition — link vector
  - **C**: Conjunction — network bridge
  - **T**: Tense/auxiliary — time operator
  - **Punct**: Punctuation — orbital gap

**Voices**:
- `grammar.type` — Classify word type
- `grammar.field_role` — Map type to field role
- `grammar.mass` — Compute semantic mass
- `grammar.flow` — Compute kinetic flow
- `grammar.curvature` — Compute curvature
- `grammar.token_type` — Create token type τ(w)

#### Sentence Field

- **Sentence** as propagating wave in Φκ-space:
  - `Φκ(sentence,t) = Σ Φκ(word_i,t)`
  - `A(sentence) = ∇Φκ` → syntactic flow
  - `M(sentence) = ∂A/∂t` → discourse momentum
  - `Q(sentence) = ∇·A` → semantic charge/focus
- **Rising Q** = emphasis, question, climax
- **Falling Q** = resolution, closure

**Voices**:
- `sentence.flow` — Compute sentence field flow
- `sentence.field_potential` — Sum word potentials
- `sentence.alignment` — Compute syntactic flow
- `sentence.momentum` — Compute discourse momentum
- `sentence.charge` — Compute semantic charge
- `sentence.rising_charge` — Detect emphasis/climax
- `sentence.falling_charge` — Detect closure

#### Punctuation and Gaps

- **Orbital**: Gap|Punct → potential.slot → invite.binding
- **Gaps** define Ω% — capacity for syntactic bonding
- **Punctuation** defines field boundaries (phase resets)

**Voices**:
- `orbital` — Process gap/punctuation
- `orbital.potential_slot` — Compute potential slot
- `orbital.invite_binding` — Emit binding invitation
- `gap.capacity` — Compute gap capacity
- `punct.boundary` — Compute punctuation boundary

#### Discourse Layer

- **Discourse**: Narrative topology
- **Coherence** from field operations

**Voices**:
- `discourse.topology` — Compute narrative topology
- `discourse.coherence` — Compute discourse coherence

### II. Zeta Field Specification 1.0 (Physics)

#### Core Field Stack

- **Φκ(x,t)**: Coherence potential — scalar field of latent meaning
- **A(x,t) = ∇Φκ**: Alignment/velocity — flow of coherence
- **M(x,t) = ∂A/∂t**: Momentum/memory — temporal continuity
- **K(x,t) = dΦκ/dt**: Kinetics field — rate of coherence change
- **Q(x,t) = ∇·A = ∇²Φκ**: Charge (ζ²) — curvature of field

**Pipeline**: `Φκ —∇→ A —∂t→ M —Δ→ K`

**Voices**:
- `field.sense` — Complete field sensing pipeline
- `field.potential` — Compute Φκ
- `field.alignment` — Compute A = ∇Φκ
- `field.momentum` — Compute M = ∂A/∂t
- `field.kinetics` — Compute K = dΦκ/dt
- `field.charge` — Compute Q = ∇·A

#### Derived Quantities

- **Semantic mass**: `m(x) = |∇²Φκ|`
- **Learning curvature**: `|∇²Φκ|`
- **Distance**: `‖x_i - x_j‖` or `‖Φκ(x_i) - Φκ(x_j)‖`
- **Type completion**: `argmin(distance/mass)`

**Conservation**: `∫(∂Φκ/∂t)dV = ∮A·n dS + ∫S dV`

#### Witness Sequence (Crossroads Field)

- **W₀**: Uniform potential → local identity (Points of being)
- **W₁**: Locality → structure & boundary (Membranes, molecules)
- **W₂**: Structure → time & motion (Dynamics, causality)

**Voices**:
- `witness.W0` — Identity witness
- `witness.W1` — Structure witness
- `witness.W2` — Time witness

#### Tan Genesis (Crossroads Geometry)

- **tan θ**: Genesis operator — singularity at ±π/2
- **n = ±1**: Active branches (multiverse asymptotes)
- **n = 0**: Gate equilibrium (perfect balance)
- **sin θ**: Time-space wave (temporal unfolding)
- **cos θ**: Space-time frame (spatial coherence)
- **90° rotation**: Crossroads event

**Voices**:
- `tan.genesis` — Genesis operator
- `tan.active_branch` — Active branch detection
- `tan.gate_equilibrium` — Gate equilibrium check
- `sin.timespace_wave` — Time-space wave
- `cos.spacetime_frame` — Space-time frame
- `crossroads.event` — Crossroads conversion

#### Zeta Charges

- **ζ⁰**: Neutral base (self-idempotent) — defines identity
- **ζ¹**: Activated symmetry break — rule ignition
- **ζ²**: Closed loop spin — field curvature (charge)
- **ζ³+**: Resonant harmonics — network coherence

**Residues collapse**: `Σ Ω%_n → ζ⁰ (mod Ω)`

**Voices**:
- `zeta.zero` — Neutral base
- `zeta.one` — Symmetry break
- `zeta.two` — Closed loop spin
- `zeta.three_plus` — Resonant harmonics
- `zeta.residue_collapse` — Residue collapse

#### Molecules and Branch Networks

- **molecule**: `Ω[Aa₀][Ba₁][Ca₂…](±n)`
- **Charge rules**:
  - `>0`: Definition/clustering (capacitance)
  - `<0`: Voice/propagation
  - `%`: Bifurcation (odd mass, even spin)
  - `=0`: Actor (equilibrium)
- **Flow operators**: `>` forward, `<` backward
- **Power operators**: `^0` self, `^1` kinetics, `^2` field, `^3` network

**Voices**:
- `molecule.form` — Form molecule
- `molecule.definition` — Definition/clustering
- `molecule.propagation` — Voice propagation
- `molecule.bifurcation` — Bifurcation
- `molecule.actor` — Actor equilibrium
- `flow.forward` — Forward flow
- `flow.backward` — Backward flow
- `power.self` — Self power
- `power.kinetics` — Kinetics power
- `power.sustain_field` — Field sustain
- `power.network` — Network power

#### Forward–Backward Duality

- **Forward**: Projects Φκ → ∇Φκ → flow(A) → output
- **Backward**: Integrates d(output)/dt → reshape(Φκ) → update(mass)
- **Reversible energy cycle**: Learning as conservation of curvature

**Voices**:
- `field.forward` — Forward projection
- `field.backward` — Backward integration
- `field.energy_cycle` — Reversible energy cycle

#### Field Conservation (Lagrangian Form)

- **Lagrangian**: `L(q, q̇) = T - V` (witness potential)
- **Hamiltonian**: `H(p,q) = p q̇ - L`
- **Semantic energy** conserved during voice exchange

**Voices**:
- `lagrangian.witness_potential` — Compute Lagrangian
- `hamiltonian` — Compute Hamiltonian
- `field.conserve_energy` — Conserve semantic energy

#### Field Learning Kernel

- **Kernel learning**: `K̂ → invariants → K̂'`
- **Zeta zeros**: `ζ_F(s) → zeros.on.critical`

**Voices**:
- `field.learn.kernel` — Learn field kernel
- `field.zeros` — Find zeta zeros

### III. Galois Reference Sheet — Semantic Invariance

#### Core Definition

- **Galois group**: `Gal(Φκ) = {σ | σ(Φκ) = Φκ}`
- **Meaning-preserving transformations**: Rephrasing, translation, derivation
- **Gradient preservation**: `∇Φκ(σ(x)) = ∇Φκ(x)`
- **Fixed field**: `Fix(G) = {Φκ | σ(Φκ)=Φκ ∀σ∈G}`
- **Galois correspondence**: `H ↔ L^H`
- **Functoriality**: `σ(f ∘ g) = σ(f) ∘ σ(g)`

**Voices**:
- `galois.invariant` — Check invariance
- `galois.check_invariant` — Verify σ(Φκ) = Φκ
- `galois.gradient_preservation` — Preserve gradient
- `galois.fixed_field` — Compute fixed field
- `galois.correspondence` — Galois correspondence
- `galois.functoriality` — Verify functoriality
- `galois.witness` — Create Galois witness

### IV. Grammar Self-Evolution

- **Self-evolution**: `stimulus → parse → Φκ_parse + residuals → evolve`
- **Self**: Φκ_parse — self-similarity holds
- **Other**: `residuals → expansion → candidates → integrate → grammar'`

**Voices**:
- `grammar.self_evolve` — Self-evolve grammar
- `grammar.parse` — Parse stimulus
- `grammar.evolve` — Evolve grammar
- `grammar.self` — Check self-similarity
- `grammar.other` — Handle other residuals
- `grammar.expansion` — Expand grammar
- `grammar.integrate` — Integrate candidates
- `grammar.parse_with_new` — Parse with new grammar

### V. Zeta Zero Solver

- **Zero solver**: `spectrum + region + tolerance → construct_zeta → search_zeros → zeros`
- **Zeta construction**: Build `ζ_F(s)` from spectrum
- **Zero search**: Numeric contour / root finding

**Voices**:
- `zeta.zero.solver` — Solve for zeros
- `zeta.construct` — Construct zeta function
- `zeta.zero.search` — Search for zeros

## Primitives Added

20+ Python primitives added to `opic_executor.py`:

### Letter Classification
- `match_vowel` — Classify vowel (ζ¹)
- `match_consonant` — Classify consonant (ζ²)
- `match_cluster` — Classify cluster (ζ²)
- `match_iconic` — Classify iconic (ζ³+)

### Field Operations
- `gradient` — Compute ∇Φκ
- `temporal_derivative` — Compute ∂A/∂t
- `laplacian` — Compute ∇²Φκ
- `divergence` — Compute ∇·A
- `near_zero` — Check equilibrium

### Grammar Operations
- `sum_charges` — Sum syllable/constituent charges
- `classify_type` — Classify word type (N/V/A/Adv/P/C/T)
- `compute_mass` — Compute semantic mass
- `compute_flow` — Compute kinetic flow
- `compute_curvature` — Compute curvature
- `sum_field_potential` — Sum word field potentials
- `positive_trend` — Detect rising Q
- `negative_trend` — Detect falling Q
- `compute_potential` — Compute gap/punctuation potential
- `emit_binding_invitation` — Emit binding invitation

## Automatic Voice Discovery

Zeta grammar voices are automatically discovered when context includes:
- `letter`, `syllable`, `word`, `sentence`
- `grammar`, `phonetic`, `morphology`, `syntax`
- `language`, `semantic`, `field`

## Integration with Field Spec 0.7

- Uses existing `field.potential`, `field.gradient`, `field.curvature`
- Uses Pascal mod 10 for letter classification
- Uses 7-trace for syllable stability
- Uses energy coupling for word evolution
- Uses dimensional promotion for sentence → discourse

## Usage

All zeta grammar voices are available by default. Example:

```ops
voice example / {
  text -> letter.measure -> syllable.measure -> word.form -> sentence.flow -> discourse.topology
}
```

## Summary

✅ **99+ zeta grammar voices** implemented
✅ **20+ primitives** added
✅ **Automatic voice discovery** enabled
✅ **Full integration** with Field Spec 0.7
✅ **Loaded by default** via `core/opic_field.ops`

Natural language is now fully integrated as a hierarchical zeta field in `opic`'s architecture.

