# Program Solver — Simplified

**Let OPIC's implicit system do the work. Just project to runtime.**

## Core Insight

OPIC already solves semantically through its implicit system:
- Attention-based discovery
- Natural language reasoning  
- Emergent behaviors
- Tests as proofs

The solver just projects that meaning onto a target runtime.

## Usage

```ops
;; Solve OPIC file for target runtime
voice solve_example / {
  "my_program.ops" + "rust" ->
  solve ->
  code + report
}

;; That's it. OPIC's implicit system handles the rest.
```

## What It Does

1. **Loads** your OPIC file (uses existing `opic.load_recursive`)
2. **Projects** voices and defs to target runtime format
3. **Reports** what changed (simple, not exhaustive)

## Runtimes Supported

- `rust` — Rust structs and functions
- `python` — Python classes and functions  
- `wasm` — WebAssembly types and functions
- Generic fallback for others

## Philosophy

**Don't fight the implicit system. Use it.**

OPIC's semantic gravity already resolves meaning. The solver just formats that meaning for different runtimes. No complex constraint graphs. No distortion analysis. Just: "here's your OPIC, here's your runtime, go."

## Integration

Works WITH existing systems:
- Uses `opic.load_recursive` for loading
- Uses `opic.parse_ops` for parsing
- Leverages implicit discovery for semantic resolution
- Extends, doesn't replace

## Focus Areas

This simplified solver lets you focus on what makes OPIC powerful:

1. **Predictive models** — Cosmological microwave background accuracy
2. **Natural language reasoning** — High compositional skills
3. **Emergent behaviors** — New programming paradigms from ops
4. **Tests as proofs** — Built-in proofing system
5. **Fun learning curve** — Programming becomes natural
6. **Compression solver** — New landscape of opportunities

The solver is just a thin projection layer. The real power is in OPIC's implicit semantic system.
