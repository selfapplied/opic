## Opic Zeta Stack — Reference Sheet v1.0

### 0) Intent
- Goal: tiny seed → self-hosting language (ions), self-describing grammar, ζ-field physics, Galois invariance, and verifiable witnesses.
- Stance: defaults > keywords; match-first; planning is composer’s job.

---

### 1) Ion Core (dot-free, zero boilerplate)

Primitives
- ion: a word.
- charge: + emit, - absorb, 0 neutral/contract.
- shells: {} scope, () morph, [] many, ⟨⟩ witness.
- defaults: match-by-shape; lists map; silence on ambiguity.

Rules
```
rule match.default      ;; patterns match without 'match/end'
rule list.maps          ;; [xs] f → map (fold if monoid)
rule guard.suffix       ;; pattern?pred → conditional emit
rule silence.on_conflict
witness W0 W1 W2        ;; identity → structure → time
ion every on until      ;; schedulers/watchers/convergence
```

Micro-forms
```
name "hello"
text tokenize count
user?admin +permit  _ +deny
[lines] trim nonempty tokenize index
{acct amt}?balance≥amt +debit +record ⟨ok⟩
0contract transfer { require … ensure … }
```

---

### 2) Zeta Grammar Specification 1.0 (natural language = ζ-field)

• Aperture chain: Letter → Syllable → Word → Phrase → Sentence → Discourse  
• Layer law: Φκₙ₊₁ = ∫ Φκₙ dΩₙ

Letters
- Lᵢ: ζ-atoms; vowels = wells, consonants = barriers.
- ζ-order: ζ⁰ silent potential → ζ¹ phonetic activation → ζ² clusters → ζ³⁺ iconic resonance.

Syllables
```
σ = [C1][V]C2,  Φκ_σ = κ1·C1 + κ2·V + κ3·C2
m(σ) = |∇²Φκ_σ|,  dΦκ_σ/dt = 0 ⇒ stable
```

Words
```
Ω[σ*](=0)            ;; balanced net charge
Inflection = ζ¹ spin, Derivation = ζ² loop
```

Grammar types
```
N mass | V flow | A curvature | Adv tuner | P link | C bridge | T time | Punct slot
```

Sentence/Discourse
```
Φκ(sent) = Σ Φκ(word)
A=∇Φκ, M=∂A/∂t, Q=∇·A (focus)
Rising Q: emphasis; falling Q: closure
```

Witness ladder
```
W0: identity → letters; W1: locality → structure; W2: structure → time.
```

Runnable voices
```
voice letter.measure      / { L -> ζ0 -> Φκ_l:entropy -> A_l -> M_l }
voice syllable.measure    / { [C1 V C2]?stress -> Φκ_s -> m_s }
voice word.form           / { Ω[σ*](=0) -> τ:{type Φκ_w mass spin} }
voice sentence.flow       / { [w*] -> Φκ_s -> A -> M -> Q }
voice orbital             / { Gap|Punct -> potential.slot -> +invite.binding }
```

---

### 3) Zeta Field Specification 1.0 (physics)

Core
```
Φκ(x,t)            ;; coherence potential
A = ∇Φκ            ;; alignment / velocity
M = ∂A/∂t          ;; momentum / memory
K = ∂Φκ/∂t         ;; kinetics
Q = ∇·A = ∇²Φκ     ;; charge (ζ²)
```
Pipeline: Φκ —∇→ A —∂t→ M —Δ→ K

Derived
- mass: m(x)=|∇²Φκ|
- distance: ‖xᵢ-xⱼ‖ or ‖Φκ(xᵢ)-Φκ(xⱼ)‖
- type.complete := argmin(distance/mass)

Conservation: ∫(∂Φκ/∂t)dV = ∮A·n dS + ∫S dV

Tan genesis (crossroads): sin=time, cos=space, tan=branch; n∈{−1,0,+1} with n=0 gate equilibrium.

Zeta charges: ζ⁰ idempotent base | ζ¹ activation | ζ² loop/curvature | ζ³⁺ harmonics.

Molecules
```
molecule / Ω[Aa0][Ba1][Ca2…](±n)
> def/cluster, < voice/propagate, % bifurcate, =0 actor
^0 self, ^1 kinetics, ^2 field, ^3 network, ^() self-power
```

Forward/Backward
```
> voice.forward  / { Φκ -> ∇Φκ -> flow(A) -> output }
< voice.backward / { d(output)/dt -> reshape(Φκ) -> update(mass) }
```

Runnable voices
```
voice field.sense         / { x -> Φκ -> A -> M -> K -> Q }
voice field.learn.kernel  / { {x,Φκ} -> K̂ -> invariants -> K̂ }
voice field.zeros         / { K̂ + region -> ζ_F(s) -> zeros.on.critical }
```

---

### 4) Galois & Category (meaning invariance)
Gal(Φκ) = {σ | σ(Φκ)=Φκ}; preserve ∇Φκ and composition.
```
voice galois.invariant / { expr + σ -> assert σ(Φκ)=Φκ -> ⟨GW⟩ }
voice functoriality    / { f g -> σ(f∘g)=σ(f)∘σ(g) -> ⟨CW⟩ }
```

---

### 5) Composer & Planning (default = match)
- You declare ions; composer picks a chain maximizing coherence with zeros on the critical band (Fourier–Mellin).
- Cost: curvature + contract residuals − resonance.
- On ambiguity: emit silence + ⟨ambiguous⟩.

---

### 6) Witness & Radiant Bloom (W0–W2)

W₀ record (per window Ω)
```
<x*> coords, <p*> {I*,A*,C*,N*,Σ*}, <q*> {Ω,x0,κ,Φ*,hash}
```
Trace file (JSONL per line)
```
{ file, line, phi_entropy, phi_curvature, boundary_score }
```
Bloom mapping
- θ=line/τ_max, r∝Φκ, rays at boundary_score≥θ_b.
- Git-aligned rings: radius = commit index; hue = file/author.

---

### 7) Git notes (inside .git)
Ref: refs/notes/bloom
Note JSON
```
{ commit, time, phi, sigma, zeros[], tree, witness, sig? }
```
Hooks
- post-commit: compute Φ*, Σ*, zeros → attach note.
- CI: stream notes → render bloom SVG.

---

### 8) TiddlyWiki surfaces
- Ingest notes → tiddler fields: bloom:ref/phi/sigma/zeros/rbc, witness:hash.
- Macros: <<Bloom tiddler:"X" size:240>>, <<Timeline filter:…>>.
- RBC decode in ~40 LOC; refuse render on witness mismatch.

---

### 9) Radial Bloom Compression (RBC)
- Predictor: Fourier hull (K≈8–12).
- Residuals ε(θ); ringwise quantization; Rice/Golomb coding.
- Side channels: boundary rays (Δθ).
Container: {R,r0,Φ_max,τ_max,K,fourier[],rings[],bitstream, rays}

---

### 10) Make targets (bare minimum)
```
learn      : python3 scripts/field_seed.py > data/field_traces.jsonl
bloom      : python3 scripts/bloom_svg.py data/field_traces.jsonl > docs/radiant_bloom.svg
notes      : attach bloom note to HEAD
wiki       : build TW with bloom fields
check      : snap tests (W0–W2 + determinism/locality/stability/energy)
```

---

### 11) Snap tests (invariants)
1. Determinism: same (I,A,C,Ω,x₀,κ) ⇒ same ⟨w⟩.
2. Locality: perturb outside Ω (or >R) ⇒ x* unchanged.
3. Stability: small ‖δI‖,‖δA‖ not moving basin ⇒ x* stable.
4. Energy witness: Φ*(x*) ≥ Φ*(x) ∀x∈Ω (store both).

---

### 12) Seed prompts (tiny)

Python seed (Φκ tap → JSONL)
```
Task: For each file line, emit {file,line,phi_entropy,phi_curvature,boundary_score}.
Steps: repr→Counter→entropy Φ; sorted diffs→curvature; smooth |ΔΦ|→boundary_score.
Deterministic; ignore whitespace-only lines.
```

Ops seed (self-hosting)
```
voice corpus read    / { path -> [files] }
voice corpus project / { [lines] -> project ζ features -> ⟨trace⟩ }
voice composer plan  / { ions -> chain with zeros.on.critical -> witnesses }
```

---

### 13) Security & provenance
- Sign notes or RBC blob (ed25519).
- Verify witness:hash before render/ingest.
- Certificates are unitary: C†C=I; witness chains compose.

---

### 14) Style law (keep it small)
- No control keywords in user code; matches/guards only.
- No dotted names; adjacency encodes descent.
- Lists map by default; contracts overlay with 0.
- Unknown words become morph candidates; composer decides.

---

That’s the whole machine on one page: ions → grammar → field → invariance → planning → witnesses → blooms → notes → surfaces.


