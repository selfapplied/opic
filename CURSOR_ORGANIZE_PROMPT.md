# Cursor Prompt: Organize Case Studies

## Goal

Organize the OPIC repository into coherent case studies, moving everything else to archive, following the structure defined in `case_studies.md`.

## Quick Start

**Automated Script Available:**

A Python script is available to automate this organization:

```bash
# Dry run (preview what will happen)
python scripts/organize_case_studies.py

# Execute actual organization
python scripts/organize_case_studies.py --execute
```

The script will:
1. Create all directory structures
2. Copy case study files
3. Create README files
4. Show what would be archived (dry run) or actually archive (--execute)

**Manual Steps:**

If you prefer manual organization or need to customize, follow the steps below.

## Structure

The case studies are organized in two tiers:

1. **Core OPIC Patterns** (1.1-1.7): How OPIC thinks
   - Predictive Models (CMB)
   - Natural Language Reasoning
   - Implicit System
   - Tests as Proofs
   - Compression Solver
   - Emergent Behaviors
   - Fun Learning Curve

2. **Domain Lenses** (2.1-2.4): How OPIC sees the world
   - Biology as Field Equations
   - Machine Learning as Compositional Fields
   - Internet Protocols as Value Fields
   - Medicine & Healthcare as Field Coherence

## Steps

### 1. Create Archive Structure

Create these directories:
```
archive/
├── systems/
├── action/
├── docs/
├── build/
└── resources/
```

### 2. Create Case Study Directories

Create these directories:
```
case_studies/
├── core/
│   ├── cosmology/
│   ├── reasoning/
│   ├── implicit/
│   ├── tests/
│   ├── compression/
│   ├── emergent/
│   └── learn/
└── domains/
    ├── biology/
    ├── ml/
    ├── protocols/
    └── medicine/
```

### 3. Copy Core Pattern Files

**1.1 Predictive Models (CMB):**
- `systems/zeta/zeta_cosmological_correspondence.ops` → `case_studies/core/cosmology/`
- `systems/cosmology/cosmological_extended.ops` → `case_studies/core/cosmology/`
- `docs/cosmological_validation.md` → `case_studies/core/cosmology/`

**1.2 Natural Language Reasoning:**
- `systems/reasoning.ops` → `case_studies/core/reasoning/`
- `systems/explain.ops` → `case_studies/core/reasoning/`
- `action/tests/explanation_plan.ops` → `case_studies/core/reasoning/`
- `action/tests/self_explanation.ops` → `case_studies/core/reasoning/`

**1.3 Implicit System:**
- `core/implicit.ops` → `case_studies/core/implicit/`
- `core/bootstrap.ops` → `case_studies/core/implicit/`
- `core/opic_parse.ops` → `case_studies/core/implicit/`
- `core/opic_load.ops` → `case_studies/core/implicit/`
- `core/opic_execute.ops` → `case_studies/core/implicit/`
- `core/opic_executor.py` → `case_studies/core/implicit/`

**1.4 Tests as Proofs:**
- `action/tests/scoring.ops` → `case_studies/core/tests/`
- `action/tests/self.ops` → `case_studies/core/tests/`
- `action/tests/executor_flow.ops` → `case_studies/core/tests/`

**1.5 Compression Solver:**
- `systems/critical_geometry_codec.ops` → `case_studies/core/compression/`
- `systems/compression/compression.ops` → `case_studies/core/compression/`
- `systems/zeta/zeta_compression.ops` → `case_studies/core/compression/`

**1.6 Emergent Behaviors:**
- `systems/actor_coupled_modeling.ops` → `case_studies/core/emergent/`

**1.7 Fun Learning Curve:**
- `systems/solve/solve_simple.ops` → `case_studies/core/learn/`
- `systems/solve/example.ops` → `case_studies/core/learn/`

### 4. Copy Domain Lens Files

**2.1 Biology as Field Equations:**
- `systems/fields/biology_field.ops` → `case_studies/domains/biology/`
- `docs/biology_field_equations.md` → `case_studies/domains/biology/`

**2.2 Machine Learning:**
- `action/ml/ml.ops` → `case_studies/domains/ml/`
- `action/ml/gann.ops` → `case_studies/domains/ml/`
- `action/ml/generate.ops` → `case_studies/domains/ml/`
- `action/ml/train.ops` → `case_studies/domains/ml/`
- `action/ml/attention.ops` → `case_studies/domains/ml/`

**2.3 Internet Protocols:**
- `systems/protocol/peer.ops` → `case_studies/domains/protocols/`
- `systems/protocol/certificate.ops` → `case_studies/domains/protocols/`
- `systems/protocol/consensus.ops` → `case_studies/domains/protocols/`
- `systems/protocol/governance.ops` → `case_studies/domains/protocols/`

**2.4 Medicine & Healthcare:**
- `systems/fields/biology_field.ops` (disease/healing sections) → `case_studies/domains/medicine/`
- Create `case_studies/domains/medicine/health_monitoring.ops` from biology_field.ops concepts

### 5. Move Everything Else to Archive

Move remaining files:
- `systems/` → `archive/systems/` (except files already copied)
- `action/` → `archive/action/` (except files already copied)
- `docs/` → `archive/docs/` (except files already copied)
- `build/` → `archive/build/`
- `resources/` → `archive/resources/`

### 6. Create Minimal Active Structure

Keep in root:
- `core/` → Only essential runtime files (bootstrap, executor)
- `systems/` → Only `systems/solve/` for now
- `case_studies.md` → The master case studies document
- `README.md` → Updated to point to case studies
- `REFACTOR_PLAN.md` → Reference document

### 7. Create README Files

Create `README.md` in each case study directory explaining:
- What it demonstrates
- Key files
- How to run examples
- Connection to other case studies

## Principles

1. **Preserve OPIC semantics** — Don't change any `.ops` file content
2. **Maintain references** — Update include paths if needed
3. **Keep it coherent** — Each case study should stand alone
4. **Document connections** — Show how case studies relate through implicit system

## Verification

After organization, verify:
- [ ] All case study files copied correctly
- [ ] Archive contains everything else
- [ ] Core OPIC runtime still works
- [ ] Case studies can be discovered through implicit system
- [ ] Documentation updated to reflect new structure

## Notes

- The implicit system will automatically discover case studies through namespace mentions
- Each case study should have a `main` voice that demonstrates its core capability
- Examples should be progressive: simple → complex
- Tests should prove expected behavior, not just check outputs

## Automation Script

The script `scripts/organize_case_studies.py` automates this entire process:

**Features:**
- Creates all directory structures
- Copies files to case study directories
- Handles duplicate file names (adds category prefix)
- Dry run mode to preview changes
- Tracks missing files
- Creates placeholder README files

**Usage:**
```bash
# Preview (safe, no changes)
python scripts/organize_case_studies.py

# Execute (actually moves files)
python scripts/organize_case_studies.py --execute
```

**After Running:**
1. Review the summary output
2. Fix any missing file paths if needed
3. Update include paths in `.ops` files if they reference moved files
4. Test that core OPIC runtime still works
5. Verify case studies can be discovered through implicit system

