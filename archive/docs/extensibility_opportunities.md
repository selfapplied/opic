# Extensibility Opportunities

**Files that could benefit from reusable extensible patterning**

---

## 1. Status/State Registry System

### Current: `systems/registry.ops`

**Problem**: Hardcoded status types and check functions

```ops
def realm_status { active, suspended, dissolved, pending }
voice registry.check_status / {registry_entry -> extract_status -> status}
voice registry.update_status / {realm + new_status + reason -> ...}
```

**Solution**: Create `systems/status_registry.ops`
- Extensible status types registry
- Status transition rules
- Status-specific handlers
- Reusable for any entity (realms, certificates, nodes, etc.)

**Benefits**:
- Add new statuses without modifying core logic
- Consistent status handling across systems
- Status transition validation
- Audit trail for status changes

---

## 2. File Filter/Categorization Registry

### Current: `systems/opic_plan.ops`

**Problem**: Hardcoded filter patterns duplicated across files

```ops
voice plan.filter_core / {files -> filter "bootstrap" + filter "parse" + ...}
voice plan.filter_systems / {files -> filter "fee" + filter "rct" + ...}
voice plan.filter_launch / {files -> filter "whitepaper" + ...}
```

**Solution**: Create `systems/filter_registry.ops`
- Extensible category registry
- Pattern-based filtering
- Category metadata (purpose, priority, etc.)
- Reusable filter chains

**Benefits**:
- Add new categories without code changes
- Consistent filtering across projects
- Metadata-driven categorization
- Easy to extend for new file types

---

## 3. Markup Normalization Rules

### Current: Multiple files with similar patterns
- `wiki/tiddlers/markup/markup_normalization_rules.ops`
- `wiki/tiddlers/markup/markup_detection_patterns.ops`
- `wiki/tiddlers/markup/tiddler_structure_preservation.ops`

**Problem**: Duplicated normalization patterns

```ops
convert_double_dollar_to_display:
  Pattern: \$\$(.+?)\$\$
  Replacement: \\[\1\\]
```

**Solution**: Create `systems/markup_normalization.ops`
- Extensible rule registry
- Pattern → replacement mapping
- Rule priority/ordering
- Rule composition

**Benefits**:
- Add new markup formats easily
- Consistent normalization across systems
- Rule testing and validation
- Reusable for any markup system

---

## 4. Translation Rule Registry

### Current: `ml/generate_impl.ops`

**Problem**: Hardcoded translation patterns

```ops
voice translate.mse.to.swift / "let error = prediction - target..."
voice translate.crossentropy.to.swift / "let epsilon = 1e-15..."
voice match.mse.pattern / "error = prediction - target"
```

**Solution**: Create `systems/translation_registry.ops`
- Extensible source → target language mappings
- Pattern matching rules
- Template-based translation
- Language-specific optimizations

**Benefits**:
- Add new languages/patterns easily
- Consistent translation logic
- Pattern reuse across languages
- Template-driven generation

---

## 5. Music Scale/Pattern Registry

### Current: `ml/music_impl.ops`

**Problem**: Hardcoded scales and patterns

```ops
voice scale.major.intervals / "2,2,1,2,2,2,1"
voice scale.minor.intervals / "2,1,2,2,1,2,2"
voice chord.major / "0,4,7"
voice rhythm.whole / "4.0"
```

**Solution**: Create `systems/music_registry.ops`
- Extensible scale registry
- Chord pattern registry
- Rhythm pattern registry
- Musical element composition

**Benefits**:
- Add new scales/chords/rhythms easily
- Consistent musical element handling
- Pattern composition and variation
- Reusable for any music system

---

## 6. Governance Template Registry

### Current: `systems/governance.ops`

**Problem**: Hardcoded template values

```ops
voice governance.set_board / {board_size -> if_not_set -> 3 + 7 -> board_clause}
voice governance.set_amendment / {amendment_quorum -> if_not_set -> "2/3 resonance quorum" -> amendment_clause}
```

**Solution**: Create `systems/governance_template.ops`
- Extensible template registry
- Jurisdiction-specific templates
- Template inheritance/composition
- Default value management

**Benefits**:
- Add new governance models easily
- Jurisdiction-specific customization
- Template reuse and composition
- Consistent governance structure

---

## 7. Service Tier Registry

### Current: `wild_sort_service.ops`

**Problem**: Hardcoded tier definitions

```ops
voice service.tier_wild / {agent_realm + ca -> create_tier "wild" + price + features -> wild_tier}
voice service.tier_wilder / {agent_realm + ca -> create_tier "wilder" + price + features -> wilder_tier}
```

**Solution**: Create `systems/service_tier_registry.ops`
- Extensible tier registry
- Tier feature composition
- Pricing model templates
- Access level management

**Benefits**:
- Add new tiers easily
- Consistent tier structure
- Feature composition
- Reusable for any service system

---

## 8. Certificate Permission Registry

### Current: `systems/certificate.ops`

**Problem**: Hardcoded permission checks

```ops
voice cert.check_permission / {certificate + resource + action -> ...}
```

**Solution**: Create `systems/permission_registry.ops`
- Extensible permission types
- Permission composition rules
- Resource-action mapping
- Permission inheritance

**Benefits**:
- Add new permissions easily
- Consistent permission checking
- Permission composition
- Reusable across systems

---

## 9. Format/Output Registry

### Current: Multiple files with format-specific logic

**Problem**: Format handling scattered across files

```ops
voice plan.format_markdown / {suggestions -> format_as_markdown -> markdown_plan}
voice registry.format_html_report / {data -> format_html -> html_report}
voice registry.format_pdf_report / {data -> format_pdf -> pdf_report}
```

**Solution**: Create `systems/format_registry.ops`
- Extensible format registry
- Format-specific templates
- Format conversion rules
- Output pipeline composition

**Benefits**:
- Add new formats easily
- Consistent formatting across systems
- Format conversion
- Template-driven output

---

## 10. Field Discovery Registry

### Current: `systems/repo_realm.ops`

**Problem**: Hardcoded field detection logic

```ops
voice repo.analyze_language / {file_structure -> detect_languages -> primary_language}
voice repo.analyze_build / {file_structure -> detect_build_system -> build_system}
```

**Solution**: Create `systems/field_discovery_registry.ops`
- Extensible field type registry
- Detection rule registry
- Field extraction patterns
- Field composition rules

**Benefits**:
- Add new field types easily
- Consistent field discovery
- Pattern-based detection
- Reusable across projects

---

## Implementation Pattern

All these systems can follow the same extensible pattern:

```ops
;; Registry definition
def registry { name, entries, lookup_rules, composition_rules }

;; Register new entry
voice registry.register / {name + config -> add_to_registry -> registered}

;; Lookup entry
voice registry.get / {name -> lookup -> entry}

;; Compose entries
voice registry.compose / {entries + rules -> combine -> composed}

;; Extend registry
voice registry.extend / {registry + new_entries -> merge -> extended}
```

---

## Priority Recommendations

1. **Status Registry** - High impact, used across many systems
2. **Filter Registry** - High reuse, simplifies many operations
3. **Translation Registry** - Already partially implemented, easy to generalize
4. **Permission Registry** - Security-critical, needs consistency
5. **Format Registry** - High reuse, many output formats needed

---

*"Build once, extend everywhere"*

