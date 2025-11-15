# Program Solver & Runtime Emission

**Solve semantically, then emit to target runtime.**

## What It Demonstrates

This case study shows the complete "solve → emit" pattern:

1. **OPIC solves semantically** through its implicit system
2. **Then emits** that meaning to a target runtime
3. **No complex constraint graphs** - just projection

## Key Files

- `solve_simple.ops` — Solver implementation (projects OPIC to runtimes)
- `example.ops` — Simple example showing solver usage
- `runtime.ops` — Example showing runtime emission to Python/Rust/WASM

## Philosophy

**Don't fight the implicit system. Use it.**

OPIC's semantic gravity already resolves meaning. The solver just formats that meaning for different runtimes. No complex constraint graphs. No distortion analysis. Just: "here's your OPIC, here's your runtime, go."

## How It Works

1. Define computation in OPIC terms (symbols/parts/fields)
2. Declare target runtime (e.g., `python.cp311`, `rust`, `wasm`)
3. Solver projects semantic meaning to runtime format

## Runtimes Supported

- `rust` — Rust structs and functions
- `python` — Python classes and functions  
- `wasm` — WebAssembly types and functions
- Generic fallback for others

## Connection to Other Case Studies

- **Implicit System** — Uses OPIC's implicit semantic resolution
- **Tests** — Validates runtime projections

## Usage

```ops
;; Solve for Python
voice solve_for_python / {
  "example.ops" + "python.cp311" ->
  solve ->
  python_code + report
}
```
