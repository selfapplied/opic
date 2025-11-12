# Default Systems in opic

What opic loads by default vs. what requires explicit inclusion.

## Default Load (Automatic)

When opic starts, it automatically loads:

1. **`core/bootstrap.ops`** — Minimal kernel
   - `opic.parse_ops` — Parser
   - `opic.load_recursive` — Loader
   - `opic.execute_chain` — Executor
   - Basic types: `type`, `voice`, `target`, `flow`

2. **`core/core.ops`** — Core types and primitives
   - Basic types: `str`, `int`, `file`, `error`
   - Core voices: `compose`, `emit`, `reflect`
   - Stoichiometry rules

3. **Repository extensions** — Auto-discovered `.ops` files in current directory

## NOT Loaded by Default (Require Explicit Include)

These systems are **available** but **not automatically loaded**:

### Field Specification Systems
- ❌ `systems/opic_field_0.7.ops` — OPIC Field Specification 0.7
- ❌ `systems/ce1_kernel.ops` — CE1 Kernel (Pascal-Zeta)
- ❌ `systems/zetacore_runtime.ops` — ZetaCore Runtime
- ❌ `systems/sigmabody.ops` — ΣBody interfaces

### Runtime Systems
- ❌ `systems/runtime/hopic.ops` — Zeta field runtime (Σ-operator)
- ❌ `systems/reasoning.ops` — Reasoning capabilities
- ❌ `systems/math.ops` — Mathematical operations

### Other Systems
- ❌ `systems/knowledge_base.ops` — Knowledge storage
- ❌ `systems/benchmark.ops` — Benchmark evaluation
- ❌ `systems/memory.ops` — Memory system

## How to Use Field Specification 0.7

### Option 1: Explicit Include (Recommended)

In your `.ops` file:

```ops
include systems/opic_field_0.7.ops

voice main / {
  input -> 
  pascal.mod10_projection -> 
  trig.tan_theta -> 
  output
}
```

### Option 2: Auto-Load via Namespace

If you reference namespaced voices, opic's attention system may auto-load:

```ops
voice main / {
  input -> 
  pascal.add ->  ;; May auto-load if namespace mapped
  output
}
```

### Option 3: Make Default (Modify Bootstrap)

To make Field Specification 0.7 available by default, you could:

1. Add to `core/bootstrap.ops`:
```ops
include systems/opic_field_0.7.ops
```

2. Or create a `core/opic_field.ops` that includes it:
```ops
include systems/opic_field_0.7.ops
include systems/ce1_kernel.ops
```

## Current Architecture Philosophy

opic follows a **minimal kernel** philosophy:

- **Core**: Only essential parsing, loading, execution
- **Extensions**: Loaded on-demand via `include` statements
- **Attention**: Auto-loads based on namespace references

This keeps opic lightweight while allowing rich extensions.

## Recommendation

**Keep Field Specification 0.7 as optional** (current design):
- ✅ Keeps core minimal
- ✅ Allows selective inclusion
- ✅ Maintains flexibility
- ✅ Users include only what they need

**To use Field Spec 0.7**, explicitly include it:

```ops
include systems/opic_field_0.7.ops
include systems/ce1_kernel.ops
include systems/runtime/hopic.ops

voice main / {
  your_field_computation
}
```

---

*Field Specification 0.7 is available but not loaded by default—include it explicitly when needed.*

