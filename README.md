# opic

**Event-Based Compositional Language** — A self-hosting, self-compiling language where programs are voices and chains, backed by a cryptographic nervous system.

## What is opic?

opic is a compositional language where:
- **Programs are voices** — Each operation is a voice that transforms input to output
- **Composition is chaining** — Voices compose via `{step1 -> step2 -> step3}` chains
- **Self-hosting** — opic defines its own parser, loader, and executor in `.ops` files
- **Cryptographic nervous system** — Certificate-based permissions, realms, and signed voices
- **Generational ethics** — Seven-generation resonance functions and coherence tracking

## Quick Start

### Interactive opic shell (default)

```bash
make
```

This gives you an interactive shell with opic available. Type opic commands or `.ops` files:

```
opic> bootstrap.ops
opic> repos.ops
opic> plan.ops
opic> exit
```

### Bring opic up

```bash
make bootstrap
```

Creates `.opicup` witness checkpoint (opic is self-hosting).

### Install opic (persists between restarts)

```bash
make install
```

Installs opic system-wide so it's available after restart. Run `opic` from anywhere.

### Build your company seed

```bash
make seed
```

### Generate the technical bluepaper

```bash
make whitepaper
```

### Get a plan for your directory

```bash
make plan
```

## Core Concepts

### Voices

A voice is a transformation:

```ops
voice greet / {name -> "Hello " + name -> greeting}
```

### Chains

Voices compose into chains:

```ops
voice main / {greet "world" -> greet}
```

### Self-Hosting

opic defines itself in `.ops` files:
- `bootstrap.ops` — Minimal kernel
- `opic_parse.ops` — Self-parser
- `opic_load.ops` — Self-loader
- `opic_compile.ops` — Self-compiler

## Certificate System

opic includes a cryptographic nervous system:

### Realms

Each agent has its own realm and certificate authority:

```ops
def realm { name, ca, agents, boundaries }
def certificate { issuer, subject, permissions, signature, realm, ca }
```

### File Access

Files are protected by certificates:

```ops
voice opic.check_file_permission / {file_path + agent_realm + ca -> cert.check_file_read -> if_permitted}
```

### Voice Execution

Voices require permission to execute:

```ops
voice opic.check_voice_permission / {voice_name + agent_realm + ca -> cert.check_voice_execute -> if_permitted}
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

## Launch Components

### Field Equation Exchange (FEE)

Learning-based currency system:

```bash
make fee
```

- **6-layer architecture**: Wiki nodes → Learning verification → Ledger → Blockchain → Pools → Exchange
- **Field equation**: `f(∆t, ΔΦ, proof_of_care) → LEU`
- **Resonance credits**: Minted from coherence growth

### Recursive Contract Theory (RCT)

Self-referential smart contracts:

```bash
make rct
```

- Contracts that reference themselves
- Recursive backing for tokens
- Self-amending governance DAOs

### Wild Sort Site

Your company seed with:

```bash
make build-seed
```

- **Technical bluepaper** (`make whitepaper`)
- **Getting started guide** (`make getting-started`)
- **Art gallery** (`make gallery`)
- **Wild Sort as a Service** (`make service`)

## Make Targets

**Default:** `make` → Interactive opic shell

**Core verbs:**
```bash
make bootstrap      # Bring opic up (creates .opicup witness checkpoint)
make install        # Install opic system-wide (persists between restarts)
make build          # Build TiddlyWiki
make seed           # Build company seed
make compile        # Self-compile opic to Metal
make test           # Run runtime interface tests
make plan           # opic suggests a plan for directory
make repos          # List repositories
```

**Launch components:**
```bash
make whitepaper     # Generate FEE + RCT bluepaper
make guide          # Generate getting started guide
make gallery        # Generate art gallery
make service        # Generate Wild Sort service
```

**System components:**
```bash
make fee            # Field Equation Exchange
make rct            # Recursive Contract Theory
make pools          # Learning Pools
```

## Witness Checkpoint System

opic creates a `.opicup` file when it successfully self-hosts. This is the **memory bank** - persistent proof that opic is up.

**Locations checked:**
- `.opicup` (project root)
- `$HOME/.opicup` (user home)
- `/usr/local/share/opic/.opicup` (system-wide, after install)

**Makefile as Memory Bank:**
- Before opic is self-hosting: Make ensures opic is built and usable
- After opic is self-hosting: Make checks `.opicup` as witness checkpoint
- Default: Interactive shell with opic available
- Install: Makes opic persist between restarts

## System Architecture

### Core Systems

- **bootstrap.ops** — Minimal kernel
- **certificate.ops** — Permission system
- **signed.ops** — Signed voice headers
- **witness.ops** — Execution witnessing
- **proof.ops** — Proof engine

### Launch Systems

- **fee.ops** — Field Equation Exchange
- **recursive_contract_theory.ops** — RCT
- **learning_pools.ops** — Learning pools
- **whitepaper.ops** — Technical bluepaper
- **company_seed.ops** — Company seed

### Governance Systems

- **governance.ops** — Legal & governance blueprint
- **consensus.ops** — Meta-concordance protocol
- **registry.ops** — Realm registry
- **treaty.ops** — Inter-realm treaties

### Generational Systems

- **generational_resonance.ops** — Seven-generation ethics
- **memory_bank.ops** — Generational memory
- **resonance_currency.ops** — Resonant currency
- **land_stewardship.ops** — Land stewardship

## Examples

### Simple voice

```ops
voice add / {a + b -> a + b -> sum}
voice main / {add 2 3 -> add}
```

### Chain composition

```ops
voice process / {input -> step1 -> step2 -> step3 -> output}
voice main / {process "data" -> process}
```

### Self-hosting

```ops
voice opic.parse_ops / {ops_text -> split_lines -> parse_each -> defs + voices}
voice opic.load_recursive / {file_path + agent_realm + ca -> opic.load_with_verification -> voices}
```

## Environment Variables

```bash
export OPIC_REALM="your_realm"      # Set your agent realm (default: opic_realm)
export OPIC_CA="your_ca"            # Set your certificate authority (default: opic_ca)
export OPIC_REPOS_DIR="/path/to/repos"  # Set repos directory (default: $HOME)
```

## Witness Checkpoint

When opic successfully self-hosts, it creates `.opicup`:
```
opicup
realm=opic_realm
ca=opic_ca
```

This file is the **memory bank** - persistent proof that opic is self-hosting. The Makefile checks for this file as a witness checkpoint before running opic commands.

## Philosophy

opic embodies:
- **Recursive self-reference** — opic defines itself
- **Compositional elegance** — Voices compose naturally
- **Cryptographic trust** — Certificates enforce boundaries
- **Generational ethics** — Seven-generation resonance
- **Distributed cognition** — Federated realms

## License

[Your license here]

## Contributing

opic is self-hosting — contribute by extending `.ops` files!

## Resources

- **Technical Bluepaper**: `make whitepaper`
- **Getting Started**: `make getting-started`
- **System Plan**: `python3 opic execute opic_plan.ops`

---

**Built with opic, by opic, for opic.**
