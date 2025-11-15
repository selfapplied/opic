# OPIC Reorganization Plan: Systematic Condensation

## Current State Analysis

**Statistics:**
- 892 Python files (mostly redundant)
- 313 OPIC files (.ops) — **this is the core**
- 95 documentation files

**Problem:** Most Python scripts are experiments, demos, or one-off utilities that should be in `.ops` files or removed entirely.

## Core Principle

**OPIC is a language-first system.** Python should only exist for:
1. The executor runtime (`opic_executor.py`)
2. The parser (`generate.py` or equivalent)
3. Essential build/CI utilities

Everything else should be `.ops` files or documentation.

## Proposed Structure

```
opic/
├── core/                    # Essential runtime (minimal Python)
│   ├── opic_executor.py     # ONLY Python file needed
│   ├── parser.py            # Parse .ops → AST
│   └── primitives.py         # Built-in operations
│
├── systems/                  # All OPIC systems (.ops only)
│   ├── 00_core/             # Core field operations
│   │   ├── opic_field_0.7.ops
│   │   ├── opic_cosmogenesis.ops
│   │   └── ...
│   ├── 01_ce1/              # CE1 kernel stack
│   │   ├── ce1_field_kernel.ops
│   │   ├── ce1_pascal_kernel.ops
│   │   ├── ce1_zeta_core.ops
│   │   └── ...
│   ├── 02_runtime/          # ZetaCore runtime
│   │   ├── zetacore_runtime.ops
│   │   ├── sigmabody_interfaces.ops
│   │   └── signetwork_governance.ops
│   ├── 03_flow/             # 3D flow solver
│   │   ├── flow3d_core.ops
│   │   ├── flow3d_mask.ops
│   │   └── ...
│   ├── 04_mode7/            # Mode 7 perspective layer
│   │   ├── opic_mode7_perspective.ops
│   │   └── ...
│   └── 05_experiments/      # Experimental protocols
│       ├── ops_eval_fingerprint_persistence.ops
│       └── ...
│
├── docs/                     # Documentation (organized by topic)
│   ├── 00_specification/    # Complete specs (A-L)
│   │   ├── opic_complete_specification_index.md
│   │   ├── ce1_kernel_spec.md
│   │   └── ...
│   ├── 01_theory/           # Theoretical foundations
│   │   ├── opic_cosmogenesis.md
│   │   ├── mathematical_proof_annex.md
│   │   └── philosophical_synthesis.md
│   ├── 02_implementation/   # Implementation guides
│   │   ├── opic_engineering_spec.md
│   │   ├── developer_experiments_handbook.md
│   │   └── ...
│   └── 03_reference/        # API references, quick guides
│       └── ...
│
├── examples/                 # Example .ops files
│   ├── getting_started.ops
│   ├── riemann_experiment.ops
│   └── ...
│
├── tests/                    # Test .ops files
│   ├── test_opic_lab.ops
│   └── ...
│
└── scripts/                  # MINIMAL utilities (if needed)
    └── (only essential build/CI scripts)
```

## Migration Strategy

### Phase 1: Identify Essential Python

**Keep:**
- `scripts/opic_executor.py` → move to `core/opic_executor.py`
- `scripts/generate.py` (parser) → move to `core/parser.py`
- Any build/CI scripts (Makefile helpers)

**Archive/Remove:**
- All experiment scripts (`*_experiment.py`, `*_test.py`)
- All mapper scripts (`*_mapper.py`)
- All benchmark runners (move to `.ops`)
- All visualization scripts (move to `.ops` or remove)

### Phase 2: Convert Python → .ops

**Pattern:** Most Python scripts are one-off experiments that should be `.ops` files:

```python
# OLD: scripts/fingerprint_persistence_ab.py
# NEW: systems/05_experiments/ops_eval_fingerprint_persistence.ops

voice fingerprint.persistence.ab / {
  baseline_config + primorial_config -> 
  run.baseline -> 
  run.primorial -> 
  compare.results -> 
  fingerprint_result
}
```

### Phase 3: Consolidate Documentation

**Current:** 95 docs, many overlapping
**Target:** Organized by topic, single source of truth

**Structure:**
- `00_specification/` — Complete specs (Appendices A-L)
- `01_theory/` — Cosmogenesis, proofs, philosophy
- `02_implementation/` — Engineering, experiments, guides
- `03_reference/` — Quick references, API docs

### Phase 4: Clean Systems Directory

**Current:** 313 `.ops` files, mixed organization
**Target:** Numbered directories by domain

**Numbering scheme:**
- `00_core/` — Fundamental field operations
- `01_ce1/` — CE1 kernel stack
- `02_runtime/` — ZetaCore runtime
- `03_flow/` — Flow solvers
- `04_mode7/` — Mode 7 layer
- `05_experiments/` — Experimental protocols

## File Count Targets

**Before:**
- 892 Python files
- 313 `.ops` files
- 95 docs

**After:**
- ~5 Python files (core runtime only)
- ~200 `.ops` files (consolidated, organized)
- ~50 docs (organized, deduplicated)

## Implementation Steps

1. **Create new directory structure**
2. **Move essential Python to `core/`**
3. **Archive Python experiments to `archive/python_experiments/`**
4. **Organize `.ops` files into numbered directories**
5. **Consolidate documentation**
6. **Update all includes/references**
7. **Create migration script**

## Benefits

- **Clarity:** Clear separation of core vs. experiments
- **Maintainability:** Single source of truth for each concept
- **Language-first:** OPIC is the primary interface
- **Reduced complexity:** 95% fewer Python files
- **Better organization:** Numbered directories show hierarchy

## Migration: The OPIC Way

**Use OPIC to organize OPIC.** Instead of Python scripts, reorganization is defined as voices:

- `systems/reorganize.ops` — Core reorganization voices
- `systems/reorganize_plan.ops` — Planning and classification
- `systems/reorganize_execute.ops` — Step-by-step execution

**Execute:**
```bash
opic execute systems/reorganize_execute.ops
```

This is language-first: OPIC manages itself through its own voices.

## Questions to Resolve

1. **Parser location:** Is `generate.py` the parser, or is it elsewhere?
2. **Build system:** What Python scripts are needed for building?
3. **CI/CD:** What scripts are needed for testing/CI?
4. **Examples:** Which Python scripts should become `.ops` examples?

## Next Steps

1. Review this plan
2. Identify parser location
3. Create migration script
4. Execute Phase 1 (move core Python)
5. Execute Phase 2 (archive experiments)
6. Execute Phase 3 (organize `.ops`)
7. Execute Phase 4 (consolidate docs)

