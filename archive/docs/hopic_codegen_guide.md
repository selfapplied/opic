# Hopic Code Generation Guide

**Using OPIC to generate implementations from `systems/hopic.ops`**

---

## Overview

`systems/hopic.ops` is a **runnable operator specification** where every equation becomes an operator. This guide shows how to use OPIC's code generation system (`systems/hopic_codegen.ops`) to turn the spec into concrete implementations.

---

## Real-World Use Cases

### Use Case 1: Generating Python Runtime for Research

**Scenario**: You're a researcher exploring the OPIC × Zeta Field runtime and need a Python implementation to run experiments.

**Problem**: You need:
- Complete Python implementation
- All operators with proper signatures
- Ability to run simulations

**Solution**:
```ops
;; Generate complete Python runtime
voice generate_python_runtime / {
  "systems/hopic.ops" + "python" + "all" -> 
  hopic.generate_implementation -> 
  python_code
}

;; Save to file
voice save_runtime / {
  python_code -> 
  write_file "opic_zeta_runtime.py" -> 
  saved
}

;; Use it
voice run_simulation / {
  -> 
  load_runtime -> 
  create_initial_state -> 
  run_sigma_evolution -> 
  results
}
```

**Output**: Complete `opic_zeta_runtime.py` with:
- `OPICState` class
- All 10 operator categories
- Invariant checking
- Runtime notes

---

### Use Case 2: Generating Rust for Performance

**Scenario**: You need a high-performance implementation for production use.

**Problem**: You need:
- Rust implementation for speed
- Memory safety
- Parallel execution support

**Solution**:
```ops
;; Generate Rust implementation
voice generate_rust_runtime / {
  "systems/hopic.ops" + "rust" + "all" -> 
  hopic.generate_implementation -> 
  rust_code
}

;; Generate with parallel features
voice generate_parallel_rust / {
  "systems/hopic.ops" + "rust" + "all" + "parallel" -> 
  hopic.generate_with_features -> 
  parallel_rust_code
}
```

**Output**: Rust crate with:
- `OPICState` struct
- Operators as functions
- `rayon` parallel iterators
- Memory-safe implementations

---

### Use Case 3: Generating TypeScript for Web Demo

**Scenario**: You want to create an interactive web demo of the OPIC × Zeta Field runtime.

**Problem**: You need:
- TypeScript/JavaScript implementation
- Browser-compatible code
- Visualization hooks

**Solution**:
```ops
;; Generate TypeScript implementation
voice generate_typescript_runtime / {
  "systems/hopic.ops" + "typescript" + "all" -> 
  hopic.generate_implementation -> 
  typescript_code
}

;; Add visualization hooks
voice add_viz_hooks / {
  typescript_code + ["state_update" "operator_call"] -> 
  hopic.add_hooks -> 
  code_with_hooks
}
```

**Output**: TypeScript module with:
- `OPICState` interface
- Operator functions
- Event emitters for visualization
- Browser-compatible code

---

### Use Case 4: Incremental Generation (Phase by Phase)

**Scenario**: You want to test each phase separately before generating the full runtime.

**Problem**: You need:
- Generate one phase at a time
- Test each phase independently
- Debug incrementally

**Solution**:
```ops
;; Generate Phase 1 only (Foundation)
voice generate_phase1 / {
  "systems/hopic.ops" + "python" + "1" -> 
  hopic.gen_phase1 -> 
  phase1_code
}

;; Test Phase 1
voice test_phase1 / {
  phase1_code -> 
  create_test_state -> 
  test_sigma_step -> 
  verify_invariants -> 
  phase1_works
}

;; Generate Phase 2 (if Phase 1 works)
voice generate_phase2 / {
  "systems/hopic.ops" + "python" + "2" -> 
  hopic.gen_phase2 -> 
  phase2_code
}
```

**Output**: Incremental code generation:
- Phase 1: State + Sigma Evolution Kernel
- Phase 2: Component Operators
- Phase 3: Differential Σ-Layer
- ... and so on

---

### Use Case 5: Custom Language Template

**Scenario**: You want to generate code for a language not yet supported (e.g., Go, C++).

**Problem**: You need:
- Add new language support
- Define language-specific formatting
- Generate code in new language

**Solution**:
```ops
;; Define Go language template
voice create_go_template / {
  -> 
  language_template.create "go" 
    "// "           ;; doc_prefix
    ""              ;; doc_suffix
    "func"          ;; function_keyword
    ", "            ;; param_separator
    " "             ;; return_arrow
    "\t"            ;; indent
    ""              ;; line_end
    "if"            ;; assert_keyword
    "// "           ;; comment_prefix
    "{"             ;; block_open
    "}"             ;; block_close
    "type"          ;; struct_keyword
    -> 
  go_template
}

;; Register template
voice register_go_template / {
  go_template -> 
  language_template.register -> 
  registered
}

;; Generate Go code
voice generate_go_runtime / {
  "systems/hopic.ops" + "go" + "all" -> 
  hopic.generate_implementation -> 
  go_code
}
```

**Output**: Go package with:
- `OPICState` struct
- Operator functions
- Go-idiomatic code

---

## The OPIC Code Generation System

OPIC can generate code from operator specifications. Use `systems/hopic_codegen.ops` to:

1. **Parse** `systems/hopic.ops` 
2. **Extract** operator signatures, update rules, and invariants
3. **Generate** implementations in target languages (Python, Rust, TypeScript, Swift, Julia)
4. **Combine** into complete runtime

---

## Quick Start

### Generate Phase 1 (Foundation)

```bash
# Using OPIC's codegen system
opic generate systems/hopic_codegen.ops --target python --phase 1
```

This generates:
- OPICState structure
- SigmaStep operator
- C_op, A_op, G_op, S_op operators  
- ZetaTrace operator

### Generate All Phases

```bash
opic generate systems/hopic_codegen.ops --target python --phase all
```

---

## Using the OPIC Codegen Voices

### Generate State Structure

```ops
voice main / {
  "python" -> 
  hopic.gen_state_structure -> 
  state_code
}
```

### Generate Single Operator

```ops
voice main / {
  "C.op" + C_op_voice + "python" -> 
  hopic.gen_operator -> 
  operator_code
}
```

### Generate Phase by Phase

```ops
voice main / {
  "python" -> 
  hopic.gen_phase1 -> 
  phase1_code
}
```

### Complete Generation Pipeline

```ops
voice main / {
  "systems/hopic.ops" + "python" + "all" -> 
  hopic.generate_implementation -> 
  complete_code
}
```

---

## Generated Code Structure

The OPIC codegen system produces:

### 1. State Structure

```python
@dataclass
class OPICState:
    x_t: np.ndarray          # State vector ∈ 𝒳
    u_t: np.ndarray          # Input vector ∈ 𝒰
    C_t: float               # Continued fraction component
    A_t: float               # Alternating accumulator
    G_t: GeometricProduct    # Geometric product (inner + outer)
    S_t: np.ndarray          # Smoothing component
    zeta_array: List[complex]  # ζ_i actors
    W: np.ndarray            # Coupling matrix
    Z_field: np.ndarray      # Field 𝒵
    S_set: List[Singularity] # Singularity set
    F_set: List[Point]       # Fractal memory set
    H_region: Region         # Hull region
    R: np.ndarray            # Resonance matrix
    Phi: float               # Field potential
    t: float                 # Time
    dt: float                # Time step
    alpha: float            # Smoothing parameter
```

### 2. Operator Functions

Each operator becomes a pure function:

```python
def C_op(state: OPICState, u_t: float) -> float:
    """
    Operator ID: C_op
    Symbol: C_{t+1} = u_t + 1/(1+C_t)
    Signature: C : (ℝ, ℝ) → ℝ
    Invariants: Avoid denominator ≈ 0; enforce |1 + C_t| > ε
    Role: Deepening / nesting of context
    """
    # Generated from hopic.ops
    denominator = 1.0 + state.C_t
    epsilon = 1e-10
    if abs(denominator) < epsilon:
        denominator = epsilon if denominator >= 0 else -epsilon
    C_next = u_t + 1.0 / denominator
    return C_next
```

### 3. Numerical Methods

Euler stepping, finite differences, integration:

```python
def euler_step(x_t, f, dt):
    """Generated from hopic.gen_euler_step"""
    return x_t + dt * f(x_t)
```

### 4. Main Runtime Loop

```python
def hopic_step(state: OPICState) -> OPICState:
    """Generated from hopic.step"""
    state = sigma_step(state, state.u_t)
    state = zeta_coupler(state, state.dt)
    state = zeta_field_compose(state)
    # ... all operators ...
    return state
```

---

## Phase Implementation Order

The OPIC codegen system generates operators in phases:

### Phase 1: Foundation
- `sigma.step` - Main state update
- `C.op`, `A.op`, `G.op`, `S.op` - Component operators
- `zeta.trace` - Basic ζ evaluation

### Phase 2: Dynamics  
- `zeta.coupler` - Actor coupling dynamics
- `sigma.flow` - Continuous flow mode
- `zeta.field_compose` - Field synthesis

### Phase 3: Detection & Memory
- `sigma.strength` - Singularity detection
- `singularity.set_update` - Event marking
- `fractal.closure` - Memory formation

### Phase 4: Resonance
- `resonance.matrix` - Cross-resonance
- `field.potential` - Harmony measure
- `harmony.flow` - Learning rule

### Phase 5: Field & Energy
- `zeta.wave_step` - PDE time-stepper
- `energy.density` - Energy computation
- `conservation.check` - Sanity monitor
- `opic.hamiltonian` - Global energy

### Phase 6: Hopic Condition
- `hopic.check_vanishing_gradient` - The resonant limit

---

## Language Support

The OPIC codegen system supports:

- **Python**: NumPy arrays, dataclasses, type hints
- **Rust**: ndarray, structs, strong typing
- **TypeScript**: Typed arrays, interfaces
- **Swift**: Native arrays, structs
- **Julia**: Native arrays, multiple dispatch

Generate for a language:

```ops
voice main / {
  "systems/hopic.ops" + "rust" + "all" -> 
  hopic.generate_implementation -> 
  rust_code
}
```

---

## Customization

### Add Custom Numerical Methods

Extend `hopic_codegen.ops`:

```ops
voice hopic.gen_custom_method / {
  method_name + target_language -> 
  format_custom_method -> 
  custom_code
}
```

### Add Language Templates

```ops
voice hopic.format_custom_lang / {
  function_name + signature + body -> 
  format_custom_template -> 
  custom_lang_code
}
```

---

## Testing Generation

The OPIC codegen system can also generate tests:

```ops
voice main / {
  "python" + operators_list -> 
  hopic.add_tests -> 
  implementation_with_tests
}
```

Generates:
- Unit tests for each operator
- Invariant tests
- Integration tests for `hopic.step`
- Conservation tests

---

## Integration with OPIC Compile System

Use OPIC's self-compilation system:

```ops
voice main / {
  "systems/hopic_codegen.ops" -> 
  opic.generate + "python" -> 
  opic.compile -> 
  hopic_runtime
}
```

---

## Example: Complete Generation

```ops
;; Generate Python implementation
voice main / {
  "systems/hopic.ops" + "python" + "all" -> 
  hopic.generate_implementation -> 
  hopic.add_tests -> 
  write_code_to_file "hopic_runtime.py" -> 
  generated
}
```

---

## Next Steps

1. **Run codegen**: `opic generate systems/hopic_codegen.ops --target python`
2. **Review generated code**: Check operator implementations
3. **Test**: Run generated tests
4. **Iterate**: Refine operators in `hopic.ops`, regenerate
5. **Extend**: Add custom methods or languages

---

*"Every equation becomes an operator, every operator becomes code—generated by OPIC itself."*
