# Emit to Runtime

**Solve semantically, then emit to target runtime.**

## What It Demonstrates

This case study crystallizes the "solve → emit" pattern:

1. **OPIC solves semantically** through its implicit system
2. **Then emits** that meaning to a target runtime
3. **No complex constraint graphs** - just emission

## Key Files

- `emit.ops` — Example showing semantic solve + runtime emission

## Philosophy

**Don't fight the implicit system. Use it.**

OPIC's semantic gravity already resolves meaning. The solver just formats that meaning for different runtimes. No complex constraint graphs. No distortion analysis. Just: "here's your OPIC, here's your runtime, go."

## How It Works

1. Define computation in OPIC terms (symbols/parts/fields)
2. Declare target runtime (e.g., `python.cp311`, `rust`, `wasm`)
3. Solver projects semantic meaning to runtime format

## Connection to Other Case Studies

- **Implicit System** — Uses OPIC's implicit semantic resolution
- **Learn** — Part of the learning/solving family
- **Tests** — Validates runtime projections

## Usage

```ops
;; Solve for Python
voice solve_for_python / {
  "emit.ops" + "python.cp311" ->
  solve ->
  python_code + report
}
```

This file doesn't need to fully implement yet - it fixes the idea in OPIC form, so future tools have a clear "this is the intended behavior" artifact.

