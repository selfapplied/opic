# opic

**Event-Based Compositional Language** — A self-hosting, self-compiling language where programs are voices and chains, backed by a cryptographic nervous system.

*Opic is a self-hosting language for distributed, cryptographically trusted computation, where each function ("voice") composes with others into verifiable chains.*

---

## Core Axiom: Invariant-Generative Worldbuilding

**The Core Axiom states:**

*All generative systems must preserve fundamental invariants under transformation. Worldbuilding is not arbitrary construction, but the disciplined exploration of constraint spaces where physical, mathematical, and narrative invariants remain coherent across scale, composition, and evolution.*

This axiom grounds OPIC's approach to compositional programming:
- **Voices** are invariant-preserving transformations
- **Chains** compose these transformations while maintaining coherence
- **Aquifer primitives** (Feigenbaum, Zeta, RG flows) encode universal scaling laws
- **Field geometry** ensures topological consistency across program evolution

The Aquifer framework provides primitives that encode deep mathematical structure (chaos theory, spectral analysis, renormalization group flows) as first-class constructs, enabling programs that naturally respect physical and mathematical invariants.

[![License](https://img.shields.io/badge/license-CC%20BY%204.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![Zeta Lab](https://img.shields.io/badge/Zeta%20Lab-Research%20Frontier-blue)](docs/riemann_hypothesis_experiment.md)

---

## Why Opic?

Software today is brittle and centralized. Opic reimagines code as a living, distributed conversation — programs that verify, sign, and evolve themselves.

**The Problem:** Traditional languages treat code as static text, execution as isolated events, and trust as an afterthought.

**Opic's Answer:** Code becomes *voices* that compose into *chains*, each step cryptographically signed and verified. Programs are self-hosting, self-compiling, and self-verifying — enabling distributed computation with built-in trust.

📖 **[Read the Theory](docs/theory.md)** — Mathematical foundations connecting opic to category theory, type theory, field dynamics, and cryptography.

---

## Hello World

```ops
voice greet / {name -> "Hello " + name -> greeting}
voice main / {greet "world" -> greet}
```

That's it. `greet` is a voice that transforms input to output. `main` chains voices together.

---

## Quick Start

### Prerequisites

- Python 3.8 or higher
- `make` (optional, but it drives the case studies)

### Clone & Run

```bash
git clone https://github.com/selfapplied/opic.git
cd opic
make case-studies   # runs every core case study and writes .out/ files
```

You can also run them individually:

```bash
make cosmology      # Generates CMB / NFW / BAO field report
make reasoning      # Emits the reasoning + self-explanation narrative
make tests          # Describes the field-based test harness
make compression    # Walks through the critical-geometry codec
make emergent       # Summarizes actor-coupled modeling
make solve          # Shows the solve → emit pipeline
make typst          # Generates the invariant whitepaper (Typst + PDF)
make show-tests     # Pretty-print an existing narrative (.out must exist or target reruns)
```

Outputs land under `.out/case_studies/core/<name>/`.  
Typst source + PDF land under `docs/whitepaper/`.
Quick peek: `make show-<target>` pretty-prints the latest narrative (auto-runs it if missing).
No extra tooling, no subscriptions—just `python3` and `make`.

If you want an interactive REPL afterwards:

```bash
make               # launches the opic shell
```

---

## Execution Model

- **Voices** are invariant-preserving transformations: `voice name / { chain }`. Each one carries charge + mass so OPIC knows how it bends the local field.
- **Chains** are field flows. `->` performs symmetry breaking, `+` is hopeful OR (first stable result wins) and, if every operand is a string, concatenation. This is how we stay in “code as flow,” not “code as syntax.”
- **Implicit Loader** honors attention. Mention `compression.` and the loader resolves it—no explicit includes inside the case studies. Target files always win conflict resolution.
- **Theory-Based Recursion Control** watches equilibrium. When a voice returns the same result with the same inputs, energy stops flowing and recursion halts naturally. No arbitrary depth limits, no stack overflows.
- **Ledger Alignment** keeps the bootstrap voices (`core/bootstrap.ops`, `systems/opic_executor_impl.ops`, etc.) as the single nervous system. Everything you run—including the Typst generator—extends those voices instead of bypassing them.

This is OPIC’s "Invariant-Generative Worldbuilding" stance: extending the field is the default; fragmentation is a smell.

---

## Case Studies At a Glance

Each target is an include-free `main.ops` that emits a narrative report.

| Case Study  | Make Target | Output File                                           | Summary                               |
|-------------|-------------|-------------------------------------------------------|---------------------------------------|
| Cosmology   | `make cosmology`   | `.out/case_studies/core/cosmology/predictions.out`   | CMB, NFW, BAO predictions from field invariants |
| Reasoning   | `make reasoning`   | `.out/case_studies/core/reasoning/explanations.out`  | Logical reasoning + self-explanation narrative    |
| Tests       | `make tests`       | `.out/case_studies/core/tests/tests.out`             | Field-based scoring / executor flow report        |
| Compression | `make compression` | `.out/case_studies/core/compression/compression.out` | Critical-geometry codec overview                   |
| Emergent    | `make emergent`    | `.out/case_studies/core/emergent/emergent.out`       | Actor-coupled modeling & regime analysis           |
| Solve → Emit| `make solve`       | `.out/case_studies/core/solve/solve.out`             | Solve semantically, emit to python/rust/wasm      |
| Whitepaper  | `make typst`       | `docs/whitepaper/invariant_whitepaper.(typ|pdf)`     | Lemmas, theorems, and proofs for new invariant tools |

`make case-studies` runs them all in sequence.

---

## Typst Whitepaper

`systems/whitepaper.ops` is a new include-free voice that:

1. Composes a Typst document describing invariant-generative worldbuilding.
2. Introduces lemmas, theorems, and proofs for the new field tools.
3. Calls `typst.write_file` and `typst.render` through OPIC’s primitive boundary.

`make typst` produces both the `.typ` source and the rendered `.pdf` inside `docs/whitepaper/`.  
If Typst is not installed, the voice still emits the document string so you can compile it later.

---

## Contributing

opic is self-hosting — contribute by extending `.ops` files!

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Add your `.ops` files following opic's pattern language
4. Commit your changes (`git commit -m 'Add amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

---

## License

This project is licensed under the Creative Commons Attribution 4.0 International License - see the [LICENSE](LICENSE) file for details.

You are free to share and adapt this work for any purpose, including commercial use, as long as you provide appropriate attribution.

---

## Acknowledgments

- Built with opic, by opic, for opic
- Inspired by compositional programming and cryptographic trust systems
- Thanks to all contributors who extend opic's capabilities

---

## Roadmap: Invariant-Axiom Seeding

**Phase 1: Foundation (Current)**
- [x] Core Axiom documentation
- [x] Aquifer primitive stubs (Feigenbaum, Zeta, RG flows)
- [x] Field geometry initialization framework
- [x] UI sketch for ZetaCore topological visualization

**Phase 2: Implementation**
- [ ] Implement Feigenbaum bifurcation constraints
- [ ] Implement Zeta spectral filtering for voice composition
- [ ] Complete RG flow convergence analysis
- [ ] Build ZetaCore interactive UI prototype

**Phase 3: Integration**
- [ ] Connect Aquifer primitives to OPIC voice system
- [ ] Demonstrate invariant preservation in chain composition
- [ ] Performance benchmarking and optimization
- [ ] Documentation and contributor guide expansion

---

## Research Directions

opic's dual structure opens several research frontiers:

- **Spectral Verification**: numerical experiments testing opic's categorical zeta symmetry
- **Field Coherence Dynamics**: simulate Φ(t) to locate the critical line (balanced oscillation)
- **Cross-Disciplinary Exploration**: connects category theory, physics, and analytic number theory

**Quick Start Research**:
```bash
make phase1                # Phase 1: Identify prime voices (opic-native!)
make riemann-experiment    # Run baseline simulation (uses Phase 1 results)
make riemann-visualize     # Generate coherence field heatmap (requires matplotlib)
```

*The experiment runs in opic itself — demonstrating opic's self-hosting capability. Phase 1 complete: identified 2,656 prime voices from 3,160 total voices. See `examples/phase1_prime_voices.ops` for the opic-native implementation.*

See [`docs/theory.md`](docs/theory.md) for mathematical foundations, [`docs/riemann_whitepaper.md`](docs/riemann_whitepaper.md) for academic framing, and [`docs/riemann_hypothesis_experiment.md`](docs/riemann_hypothesis_experiment.md) for experiment plans.

---

**Built with opic, by opic, for opic —**

*a language that learns to speak for itself.*
