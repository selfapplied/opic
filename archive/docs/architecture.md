# opic System Architecture

## Overview

opic is organized into layers:

```
┌─────────────────────────────────────┐
│      Wiki/Documentation Layer       │
│  (tiddlywiki, conversion, markup)  │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│      Launch Systems                  │
│  (FEE, RCT, learning pools)         │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│      Core Systems                    │
│  (certificate, witness, VFS)         │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│      Language Runtime                │
│  (bootstrap, parser, loader)         │
└──────────────────────────────────────┘
```

## Language Runtime

**Core Files:**
- `bootstrap.ops` — Minimal kernel
- `opic_parse.ops` — Self-parser
- `opic_load.ops` — Self-loader
- `opic_execute.ops` — Self-executor
- `core.ops` — Core definitions

## Core Systems

**Security & Trust:**
- `certificate.ops` — Certificate-based permissions
- `witness.ops` — Execution witnessing
- `signed.ops` — Signed voice headers
- `proof.ops` — Proof engine

**Storage:**
- `vfs.ops` — Virtual filesystem
- `vmap.ops` — Virtual memory mapping
- `voice_ledger.ops` — Voice certificate ledger

**Field Theory:**
- `fee.ops` — Field Equation Exchange
- `field_coherence.ops` — Coherence tracking
- `generational_resonance.ops` — Seven-generation ethics

## Launch Systems

- `fee.ops` — Field Equation Exchange
- `recursive_contract_theory.ops` — RCT
- `learning_pools.ops` — Learning pools
- `whitepaper.ops` — Technical bluepaper
- `company_seed.ops` — Company seed

## Governance Systems

- `governance.ops` — Legal & governance blueprint
- `consensus.ops` — Meta-concordance protocol
- `registry.ops` — Realm registry
- `treaty.ops` — Inter-realm treaties

## Wiki/Documentation Layer

- `tiddlywiki.ops` — Tiddler types and composition
- `tiddlywiki_build.ops` — Wiki generation
- `tiddlers/` — Conversion tools, markup handling, drive system

## File Organization

Files are organized by function:
- **Core runtime** — Language fundamentals
- **Systems** — Capabilities built on core
- **Wiki** — Documentation layer
- **Examples** — Sample code
- **Tests** — Test suites

