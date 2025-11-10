# opic

**Event-Based Compositional Language** — A self-hosting, self-compiling language where programs are voices and chains, backed by a cryptographic nervous system.

*Opic is a self-hosting language for distributed, cryptographically trusted computation, where each function ("voice") composes with others into verifiable chains.*

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
- Make (optional, but recommended)

### Installation

```bash
git clone https://github.com/selfapplied/opic.git
cd opic
make
```

This gives you an interactive opic shell:

```
opic> bootstrap.ops
opic> repos.ops
opic> plan.ops
opic> exit
```

### One-Minute Demo

```bash
make bootstrap    # Bring opic up
make test         # Run tests
```

---

## How It Works

### Voices

A voice is a transformation:

```ops
voice add / {a + b -> a + b -> sum}
```

### Chains

Voices compose into chains:

```ops
voice process / {input -> step1 -> step2 -> step3 -> output}
voice main / {process "data" -> process}
```

### Self-Hosting

opic defines itself in `.ops` files:
- `bootstrap.ops` — Minimal kernel
- `opic_parse.ops` — Self-parser
- `opic_load.ops` — Self-loader
- `opic_execute.ops` — Self-executor

```
┌─────────────┐
│ parser.ops  │ ──┐
└─────────────┘   │
                  ├──> opic executes itself
┌─────────────┐   │
│ loader.ops  │ ──┤
└─────────────┘   │
                  │
┌─────────────┐   │
│ executor.ops│ ──┘
└─────────────┘
```

---

## Cryptographic Nervous System

Each voice is signed with a certificate that defines its realm and permissions. Executing a voice requires verifying its signature — ensuring trust in distributed execution.

### Realms

Each agent has its own realm and certificate authority:

```ops
def realm { name, ca, agents, boundaries }
def certificate { issuer, subject, permissions, signature, realm, ca }
```

### Certificate Flow

```
┌──────────────┐
│   Voice      │
│  Definition  │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Certificate  │ ──> Signed with realm CA
│   Signing    │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Execution   │ ──> Verify signature before run
│  Verification│
└──────────────┘
```

### Signed Voices

`.ops` files can include signed headers:

```ops
---
signature: sha256:abc123...
ca: opic_ca
realm: opic_realm
---
voice example / {input -> transform -> output}
```

---

## System Architecture

### Core Systems

- **bootstrap.ops** — Minimal kernel
- **certificate.ops** — Permission system
- **signed.ops** — Signed voice headers
- **witness.ops** — Execution witnessing
- **proof.ops** — Proof engine
- **vfs.ops** — Virtual filesystem

### Launch Systems

- **fee.ops** — Field Equation Exchange
- **recursive_contract_theory.ops** — RCT
- **learning_pools.ops** — Learning pools
- **whitepaper.ops** — Technical bluepaper

### Wiki/Documentation Layer

- **tiddlywiki.ops** — Tiddler types and composition
- **tiddlers/** — Conversion tools, markup handling, drive system

See [System Architecture](docs/architecture.md) for details.

---

## Make Targets

**Default:** `make` → Interactive opic shell

**Core Commands:**
```bash
make bootstrap      # Bring opic up (creates .opicup witness checkpoint)
make install        # Install opic system-wide
make build          # Build TiddlyWiki
make seed           # Build company seed
make compile        # Self-compile opic to Metal
make test           # Run runtime interface tests
make plan           # opic suggests a plan for directory
```

**Launch Components:**
```bash
make whitepaper     # Generate FEE + RCT bluepaper
make fee            # Field Equation Exchange
make rct            # Recursive Contract Theory
```

---

## Examples

### Simple Voice

```ops
voice add / {a + b -> a + b -> sum}
voice main / {add 2 3 -> add}
```

### Chain Composition

```ops
voice process / {input -> step1 -> step2 -> step3 -> output}
voice main / {process "data" -> process}
```

### Self-Hosting

```ops
voice opic.parse_ops / {ops_text -> split_lines -> parse_each -> defs + voices}
voice opic.load_recursive / {file_path + agent_realm + ca -> opic.load_with_verification -> voices}
```

---

## Environment Variables

```bash
export OPIC_REALM="your_realm"      # Set your agent realm (default: opic_realm)
export OPIC_CA="your_ca"            # Set your certificate authority (default: opic_ca)
export OPIC_REPOS_DIR="/path/to/repos"  # Set repos directory (default: $HOME)
```

---

## Witness Checkpoint System

opic creates a `.opicup` file when it successfully self-hosts. This is the **memory bank** - persistent proof that opic is up.

**Locations checked:**
- `.opicup` (project root)
- `$HOME/.opicup` (user home)
- `/usr/local/share/opic/.opicup` (system-wide, after install)

---

## Philosophy

opic embodies:
- **Recursive self-reference** — opic defines itself
- **Compositional elegance** — Voices compose naturally
- **Cryptographic trust** — Certificates enforce boundaries
- **Generational ethics** — Seven-generation resonance
- **Distributed cognition** — Federated realms

Learn more in [`docs/philosophy.md`](docs/philosophy.md) — field equations, seven-generation ethics, resonant trust theory, and more.

---

## The Riemann Connection

opic's architecture naturally expresses the duality at the heart of analytic number theory.

- **Left Flank — Category (Discrete)**: voices compose into a spectrum of *prime morphisms*, forming an Euler-like product.
- **Right Flank — Field (Continuous)**: coherence evolves under field equations whose Fourier–Mellin transform mirrors ζ(s)'s analytic continuation.
- **Bridge — Certificate Operator**: a unitary transformation equating the two halves, echoing ζ(s) = χ(s) ζ(1 − s).

Together, these create a "pincer model" where discrete structure and continuous resonance meet along a critical line of coherence.

See [`docs/riemann_hypothesis_experiment.md`](docs/riemann_hypothesis_experiment.md) for the full theory and experiment plan.

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

## Documentation

- **[Theory](docs/theory.md)** — Mathematical foundations (category theory, type theory, field dynamics)
- **[Philosophy](docs/philosophy.md)** — Core principles and vision
- **[Architecture](docs/architecture.md)** — System architecture overview
- **[Riemann Hypothesis Whitepaper](docs/riemann_whitepaper.md)** — Theoretical framing and baseline results
- **[Riemann Experiment Plan](docs/riemann_hypothesis_experiment.md)** — Full experiment plan with 7 phases
- **Technical Bluepaper**: `make whitepaper`
- **Getting Started**: `make getting-started`
- **System Plan**: `python3 opic execute systems/opic_plan.ops`
- **Integration Paper**: See `wiki/tiddlers/INTEGRATION_PAPER.md`

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
