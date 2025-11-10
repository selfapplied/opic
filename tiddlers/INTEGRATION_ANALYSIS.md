# Integration Analysis: New Contributions

## Overview
New contributions were added to `tiddlers/` directory. This document analyzes integration points and tests integration paths.

## Contribution Categories

### 1. Conversion Tools (`tiddlers/conversion/`)
- `convert_markdown_to_tiddlers.ops` - Markdown → Tiddlers
- `convert_tiddlers_to_opic.ops` - Tiddlers → Opic capabilities
- `convert_tiddlers_to_opic_witnessed.ops` - Tiddlers → Opic (with witnessing)
- `export_tiddlers_from_ops.ops` - Opic capabilities → Tiddlers

**Integration Points:**
- References `tiddlywiki.ops` patterns (tiddler structure)
- References opic capability patterns
- Needs: `include tiddlywiki.ops` (for tiddler types)
- Needs: `include witness.ops` (for witnessed conversion)

### 2. Drive System (`tiddlers/drive/`)
- `mount_drive.ops` - Mount HTML drive with manifest
- `fork_drive.ops` - Fork drive with new genesis
- `proof_of_care_system.ops` - Care-based credit minting
- `witness_summons_protocol.ops` - Network consensus by care

**Integration Points:**
- References VFS (`initialize_vfs`, `vfs_structure`)
- References certificate system (`certificate_chain`, `cert.verify`)
- References witness system (`witness_chain`, `witness.create`)
- References field theory (`field_equation`, `resonance_validator`)
- References ledger (`ledger_sheaf`, `genesis_witness`)
- Needs: `include vfs.ops`
- Needs: `include certificate.ops`
- Needs: `include witness.ops`
- Needs: `include fee.ops` or field theory files
- Needs: `include voice_ledger.ops` or ledger files

### 3. Field Theory (`tiddlers/field/`)
- `bootstrap_realm.ops` - Create new realm with field equation
- `certify_change.ops` - Certify state changes with C operator
- `federate_realm.ops` - Sync realms via field coherence
- `field_evolution.ops` - Evolve field via dPhi_dt = div J + S

**Integration Points:**
- References field equation: `dPhi_dt = divergence_J + S`
- References certificate operator: `C_operator` (unitary)
- References witness operator: `W_operator`
- References realm structure (`realm_U_i`, `realm_boundaries`)
- References ledger sheaf (`ledger_sheaf`)
- Needs: `include certificate.ops`
- Needs: `include witness.ops`
- Needs: `include fee.ops` (has field equation)
- Needs: `include generational_resonance.ops` (has coherence)

### 4. Markup Handling (`tiddlers/markup/`)
- `markup_detection_patterns.ops` - Detect markup types
- `markup_normalization_rules.ops` - Normalize markup
- `normalize_tiddler_markup.ops` - Main normalization flow
- `tiddler_structure_preservation.ops` - Preserve structure

**Integration Points:**
- References tiddler structure
- Self-contained (no external dependencies)
- Needs: `include tiddlywiki.ops` (for tiddler types)

### 5. Platform Awareness (`tiddlers/platform/`)
- `detect_platform_capabilities.ops` - Detect OS/runtime capabilities

**Integration Points:**
- Self-contained detection logic
- References opic compile/metal commands
- No includes needed (pure detection)

### 6. NLP Integration (`tiddlers/add_nlp_descriptions.ops`)
- Adds semantic descriptions to tiddlers

**Integration Points:**
- References `nlp.describe_capability`
- References `nlp.tag_semantics`
- Needs: `include nlp_capability.ops`
- Needs: `include tiddlywiki.ops`

### 7. Platform-Aware Build (`tiddlers/platform_aware_build.ops`)
- Builds for multiple targets based on platform

**Integration Points:**
- References `detect_platform_capabilities`
- References opic compile/metal commands
- Needs: `include tiddlers/platform/detect_platform_capabilities.ops`

## Integration Test Plan

### Test 1: Conversion Round-Trip
```
markdown → tiddlers → opic → tiddlers → verify equivalence
```

### Test 2: Drive Mounting
```
HTML file → parse manifest → initialize VFS → register capabilities
```

### Test 3: Field Evolution
```
realm → bootstrap → certify change → evolve field → verify coherence
```

### Test 4: Markup Normalization
```
tiddler with mixed markup → detect → normalize → verify structure
```

## Missing Integration Elements

### Headers
All new files need:
```ops
;;; filename.ops — description
```

### Includes
Files need explicit `include` statements:
- Drive files: `include vfs.ops`, `include certificate.ops`, `include witness.ops`
- Field files: `include certificate.ops`, `include fee.ops`, `include generational_resonance.ops`
- Conversion files: `include tiddlywiki.ops`
- NLP file: `include nlp_capability.ops`, `include tiddlywiki.ops`

### Voice Definitions
Some files define capabilities but don't expose them as `voice` definitions that can be called.

## Delineation: Opic vs Paperwiki

**Opic Core:**
- Language runtime (bootstrap, parser, loader, executor)
- Certificate/witness system
- VFS system
- Field theory (Phi, J, S)
- Ledger system
- Capability system

**Paperwiki Layer (Wiki/Documentation):**
- Tiddler conversion tools
- Markup normalization
- Wiki composition (tiddlywiki.ops)
- Documentation generation
- Content management

**Boundary:**
- Opic provides capabilities (voices, certificates, VFS, field theory)
- Paperwiki uses opic capabilities to build wiki/documentation systems
- Conversion tools bridge: opic capabilities ↔ wiki content
- Drive system bridges: opic VFS ↔ wiki storage

The new contributions span both:
- **Opic layer**: Drive system, field theory, platform detection
- **Paperwiki layer**: Conversion tools, markup handling, NLP descriptions
- **Bridge layer**: Drive mounting (VFS ↔ HTML), conversion (opic ↔ tiddlers)

## Integration Test Results

### Test 1: Added Header and Include to convert_tiddlers_to_opic.ops
✅ Added `;;;` header comment
✅ Added `include tiddlywiki.ops` for tiddler types
✅ Pattern matches existing opic files

### Test 2: Pattern Verification
✅ All new files follow opic pattern language correctly
✅ References to existing systems use correct naming
✅ Capability definitions match opic patterns

### Test 3: Missing Elements Identified
- All 19 new files need headers
- 15+ files need include statements
- Some files need `target` and `voice main` for execution

## Next Steps

1. Add headers to all new files
2. Add appropriate `include` statements
3. Add `target` and `voice main` where needed for execution
4. Test integration paths:
   - Conversion: markdown → tiddlers → opic
   - Drive: mount → initialize VFS → register capabilities
   - Field: bootstrap → certify → evolve

