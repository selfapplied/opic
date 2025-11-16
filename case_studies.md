# Case Studies

OPIC’s case studies are now pure voices: include-free `main.ops` files that resolve entirely through the implicit loader.  
Run `make case-studies` (or any individual target) to emit the narratives under `.out/case_studies/core/<name>/`.

---

## Core Patterns — How OPIC Thinks

| Pattern | Run | Output | Focus |
| --- | --- | --- | --- |
| **Cosmology** | `make cosmology` | `.out/case_studies/core/cosmology/predictions.out` | Field equations → CMB, NFW, BAO predictions with real parameters. |
| **Reasoning** | `make reasoning` | `.out/case_studies/core/reasoning/explanations.out` | Deductive / inductive / abductive chains plus self-explanation. |
| **Tests as Proofs** | `make tests` | `.out/case_studies/core/tests/tests.out` | Field-scoring loop, executor trace, self-validating harness. |
| **Compression Solver** | `make compression` | `.out/case_studies/core/compression/compression.out` | Critical-geometry codec and adaptive routing across regimes. |
| **Emergent Behaviors** | `make emergent` | `.out/case_studies/core/emergent/emergent.out` | Actor-coupled modeling, regime reveal, causal graph tracking. |
| **Solve → Emit** | `make solve` | `.out/case_studies/core/solve/solve.out` | Solve in invariant space, emit to runtimes without losing semantics. |

Key shared traits:

- **Target-file override:** each `main.ops` owns its namespace, so the ledger never confuses user work with bootstrap wiring.  
- **Implicit routing:** mentioning a namespace (e.g., `compression.`) is enough for attention-based loading—no manual includes remain.  
- **Theory-based recursion control:** all case studies rely on the same equilibrium detection now guarding `opic.execute_chain`.

---

## Domain Lenses — How OPIC Sees the World

These sections seed future repos (Field OS, ZetaCore). They describe how the same invariant calculus shows up in different disciplines.

- **Biology as Field Equations:** molecules → tissues share one grammar; healing = restoring coherence.  
- **Machine Learning as Compositional Fields:** GANs/LLMs become particles with measures; training is compression plus emergence.  
- **Internet Protocols as Value Fields:** trust, routing, consensus map to energy flow rather than RFC checklists.  
- **Medicine & Healthcare as Field Coherence:** diagnostics as proofs, treatments as operators pushing the field back to stability.

Use these write-ups when you need narrative anchors for new domains; they keep us extending the existing hull instead of inventing parallel stacks.

### Diophantine Coherence (Circular Diffeomorphisms)

| Rotation Number ($\rho$) | Continued Fraction $\rho = [a_0; a_1, a_2, \dots]$ | Largest Quotient $\mu = \sup\{a_n\}$ | Diophantine Class | Dynamical Coherence |
| --- | --- | --- | --- | --- |
| Golden Ratio $\frac{\sqrt{5}-1}{2}$ | $[0; 1, 1, 1, 1, \dots]$ | $\mu = 1$ | Diophantine (maximally stable) | Highest coherence: $f$ is the smoothest and orbits are uniformly distributed. |
| $e-2 \approx 0.71828$ | $[0; 1, 2, 1, 1, 4, 1, 1, 6, \dots]$ | $\mu$ unbounded | Non-Diophantine | Moderate coherence: intermittent near-periodicity when large $a_n$ appears. |
| $\pi \bmod 1 \approx 0.14159$ | $[0; 7, 15, 1, \mathbf{292}, 1, 1, \dots]$ | $\mu = 292$ (so far) | Non-Diophantine | Low coherence: massive partial quotient triggers sharp stability loss. |
| Liouville $\sum_{k=1}^{\infty} 10^{-k!}$ | $[0; 9, 99, 9999, \dots]$ | $\mu \to \infty$ | Liouville (minimally stable) | Coherence breakdown: $f$ cannot remain smooth; rationals dominate. |

**Interpretation**

1. **High coherence (golden ratio):** worst-approximable irrational → maximally stable circular diffeomorphism.  
2. **Moderate/low coherence ($e$, $\pi$):** sporadic large $a_n$ inject temporary periodic locks—local cracks in the invariant flow.  
3. **Breakdown (Liouville):** exponential continued-fraction growth ensures constant resonance with rationals, so smooth conjugacy fails.

This lens doubles as a practical scoring rubric: the Diophantine $\mu$ metric drops straight into the coherence/charge register OPIC already tracks for implicit solvers.

---

## Typst Whitepaper

- **Run:** `make typst`  
- **Voice:** `systems/whitepaper.ops` (include-free)  
- **Artifacts:** `docs/whitepaper/invariant_whitepaper.typ` + `.pdf`

The whitepaper generator is a case study too: it assembles lemma/theorem/proof sections inside OPIC, writes the Typst file via `typst.write_file`, and calls `typst.render`. No extra tooling required beyond the usual equilibrium-aware executor.

---

## Field Atlas Structure

1. **Core Patterns** — executable narratives proving the implicit model in action.  
2. **Domain Lenses** — conceptual guides for how the same math refracts through biology, ML, networking, and medicine.  
3. **Typst Whitepaper** — formal documentation living inside the same architecture.

If you add a new case study, keep it narrative-first, include-free, and hook it into the Makefile so `make case-studies` stays the single command that explores the entire field. Extend, don’t fork.


