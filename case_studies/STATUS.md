# Case Studies Status - One by One Review

## 1. COSMOLOGY

**Current Files:**
- `zeta_cosmological_correspondence.ops` - Field correspondences (definitions)
- `cosmological_extended.ops` - NFW, CMB, BAO definitions
- `main.ops` - **NEW** - Attempts to generate predictions (has syntax issues)

**Issues:**
- ❌ `main.ops` uses invalid OPIC syntax (`=`, `[]`, `*`)
- ❌ References archived `systems/cosmology_field.ops`
- ❌ Defines structures but doesn't compute actual values
- ❌ No actual numerical output

**What It Should Do:**
- Compute CMB power spectrum C_ℓ for ℓ = 2 to 2500
- Compute NFW density profiles for sample radii
- Compute BAO correlation functions
- Output formatted numerical results

**Status:** ⚠️ Needs complete rewrite to use valid OPIC syntax

---

## 2. REASONING

**Current Files:**
- `reasoning.ops` - Reasoning capabilities (definitions)
- `explain.ops` - Self-explanation system
- `self_explanation.ops` - OPIC explains itself
- `explanation_plan.ops` - Explanation planning

**What It Should Do:**
- Generate actual explanations
- Show reasoning chains
- Output explanations to file

**Status:** ✅ Has target/main - needs testing

---

## 3. TESTS

**Current Files:**
- `scoring.ops` - Field curvature scoring
- `self.ops` - Self-tests
- `executor_flow.ops` - Executor tests

**What It Should Do:**
- Run tests and generate proof results
- Output test scores/proofs

**Status:** ✅ Has target/main - needs testing

---

## 4. COMPRESSION

**Current Files:**
- `critical_geometry_codec.ops` - Compression codec
- `compression.ops` - Inflate/deflate
- `zeta_compression.ops` - Zeta-based compression

**What It Should Do:**
- Compress sample data
- Show compression ratios
- Output compression results

**Status:** ✅ Has target/main - needs testing

---

## 5. EMERGENT

**Current Files:**
- `actor_coupled_modeling.ops` - ACM base abstraction

**What It Should Do:**
- Generate emergent behavior examples
- Show self-organizing patterns
- Output emergent structures

**Status:** ✅ Has target/main - needs testing

---

## 6. SOLVE

**Current Files:**
- `solve_simple.ops` - Solver implementation
- `example.ops` - Solver example
- `runtime.ops` - Runtime emission example

**What It Should Do:**
- Generate actual runtime code (Python/Rust/WASM)
- Show code generation results

**Status:** ✅ Has target/main - needs testing

---

## Next Steps

1. **Fix cosmology** - Rewrite main.ops with valid OPIC syntax
2. **Test each case study** - Run them and see what they actually output
3. **Enhance as needed** - Make sure each generates novel output
4. **Validate Makefile targets** - Ensure all work correctly

