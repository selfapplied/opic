# Registry Help & Discoverability Guide

**How to use help commands and discoverability in registry systems**

---

## Overview

All registry systems now include built-in help, discoverability, and usage instructions. This makes registries self-documenting and easy to explore.

---

## Real-World Use Cases

### Use Case 1: Managing Realm Status Transitions

**Scenario**: You're building a realm management system and need to track realm statuses (active, suspended, dissolved) with proper transitions.

**Problem**: You need to know:
- What statuses are available?
- What transitions are valid?
- How to check if a transition is allowed?

**Solution**:
```ops
;; Initialize status registry
voice init_realm_status / {
  -> 
  status.init_registry -> 
  realm_status_registry
}

;; Check what statuses are available
voice check_available_statuses / {
  realm_status_registry -> 
  status.help -> 
  ;; Returns: active, suspended, dissolved, pending with descriptions
  available_statuses
}

;; Check if transition is valid
voice can_suspend_realm / {
  realm_status_registry + "active" + "suspended" -> 
  status.can_transition -> 
  ;; Returns: true (active -> suspended is valid)
  transition_allowed
}

;; Get help for specific status
voice learn_about_suspended / {
  realm_status_registry + "suspended" -> 
  status.help_status -> 
  ;; Returns: description, usage, examples, related statuses
  suspended_info
}
```

**Output Example**:
```
Status: suspended
Description: Suspended status - entity temporarily non-operational
Usage: Use when entity needs temporary suspension, can reactivate
Examples: ["registry.suspend_realm realm reason"]
Related: ["active"]
Valid Transitions From: ["active"]
```

---

### Use Case 2: Filtering Files by Category

**Scenario**: You're building a project planning tool that categorizes files (core, systems, launch, examples).

**Problem**: You need to:
- Filter files by category
- Discover what categories exist
- Find files matching a pattern

**Solution**:
```ops
;; Initialize filter registry
voice init_plan_filters / {
  -> 
  filter.init_registry -> 
  plan_filter_registry
}

;; Get all available categories
voice list_categories / {
  plan_filter_registry -> 
  filter.help -> 
  ;; Returns: core, systems, launch, examples with descriptions
  categories
}

;; Filter files by category
voice get_core_files / {
  files + plan_filter_registry -> 
  category.apply "core" -> 
  ;; Returns: bootstrap.ops, parse.ops, load.ops, execute.ops
  core_files
}

;; Discover filters matching a query
voice find_build_filters / {
  plan_filter_registry + "build" -> 
  filter.discover -> 
  ;; Returns: filters related to building/compiling
  build_filters
}
```

**Output Example**:
```
Category: core
Filters: bootstrap, parse, load, execute, compile
Description: Core language runtime files
Usage: plan.filter_core files
```

---

### Use Case 3: Translating Code Between Languages

**Scenario**: You're building a code generator that translates OPIC code to Swift.

**Problem**: You need to:
- Find translation rules for a language pair
- Discover available translations
- Get examples of translations

**Solution**:
```ops
;; Initialize translation registry
voice init_translations / {
  -> 
  translation.init_registry -> 
  translation_registry
}

;; List available language pairs
voice list_languages / {
  translation_registry -> 
  translation.list_languages -> 
  ;; Returns: [("opic", "swift"), ("opic", "python"), ...]
  language_pairs
}

;; Get translation rules for specific pair
voice get_swift_rules / {
  translation_registry + "opic" + "swift" -> 
  translation.list_rules -> 
  ;; Returns: mse, crossentropy, gradient, optimize rules
  swift_rules
}

;; Translate code
voice translate_to_swift / {
  translation_registry + "error = prediction - target" + "opic" + "swift" -> 
  translation.translate -> 
  ;; Returns: "let error = prediction - target; return error * error"
  swift_code
}

;; Get help for specific rule
voice learn_mse_translation / {
  translation_registry + "mse" -> 
  translation.help_rule -> 
  ;; Returns: description, pattern, template, examples
  mse_info
}
```

**Output Example**:
```
Rule: mse
Pattern: "error = prediction - target"
Template: "let error = prediction - target; return error * error"
Source: opic
Target: swift
Examples: ["error = prediction - target → let error = ..."]
```

---

### Use Case 4: Composing Musical Elements

**Scenario**: You're building a music composition tool that uses scales, chords, and patterns.

**Problem**: You need to:
- Find available scales/chords/patterns
- Compose musical elements together
- Discover related elements

**Solution**:
```ops
;; Initialize music registry
voice init_music / {
  -> 
  music.init_registry -> 
  music_impl_registry
}

;; List all scales
voice list_scales / {
  music_impl_registry -> 
  music.list_scales -> 
  ;; Returns: major, minor, pentatonic
  scales
}

;; Get scale intervals
voice get_major_scale / {
  music_impl_registry + "major" -> 
  scale.get -> 
  ;; Returns: scale with intervals "2,2,1,2,2,2,1"
  major_scale
}

;; Compose musical elements
voice compose_song / {
  music_impl_registry + "major" + ["major" "minor"] + "arpeggio" + "quarter" -> 
  music.compose -> 
  ;; Returns: composition using major scale, major/minor chords, arpeggio pattern, quarter rhythm
  composition
}

;; Discover minor-related elements
voice find_minor_elements / {
  music_impl_registry + "minor" -> 
  music.discover -> 
  ;; Returns: minor scale, minor chord, minor-related patterns
  minor_elements
}
```

**Output Example**:
```
Scale: major
Intervals: 2,2,1,2,2,2,1
Root: C
Related: ["minor" "pentatonic"]
Usage: scale.get music_registry "major"
```

---

## Base Registry Help Features

Every registry provides these help/discoverability features:

### 1. Get Help for Registry
```ops
voice main / {
  registry -> 
  registry.help -> 
  help_output
}
```

Shows:
- Registry description
- List of all entries with descriptions
- Usage instructions
- Examples

### 2. Get Help for Specific Entry
```ops
voice main / {
  registry + entry_name -> 
  registry.help_entry -> 
  entry_help
}
```

Shows:
- Entry description
- Usage instructions
- Examples
- Related entries

### 3. Discover Entries by Query
```ops
voice main / {
  registry + "query text" -> 
  registry.discover -> 
  matching_entries
}
```

Searches:
- Entry descriptions
- Metadata
- Related entries

### 4. List All Entries
```ops
voice main / {
  registry -> 
  registry.list -> 
  entry_list
}
```

### 5. Interactive Discovery
```ops
voice main / {
  registry -> 
  registry.interactive_discover -> 
  discovery_results
}
```

Shows menu and handles queries interactively.

### 6. Generate Discoverability Data (for agents)
```ops
voice main / {
  registry -> 
  registry.generate_discoverability -> 
  discoverability_json
}
```

Generates structured JSON with all entries, descriptions, usage, and examples.

---

## Status Registry Help

### Get Help
```ops
voice main / {
  realm_status_registry -> 
  status.help -> 
  status_help
}
```

### Help for Specific Status
```ops
voice main / {
  realm_status_registry + "suspended" -> 
  status.help_status -> 
  status_help
}
```

### Discover Statuses
```ops
voice main / {
  realm_status_registry + "temporary" -> 
  status.discover -> 
  matching_statuses
}
```

### Show Usage Examples
```ops
voice main / {
  realm_status_registry -> 
  status.show_examples -> 
  examples
}
```

### List Valid Transitions
```ops
voice main / {
  realm_status_registry + "active" -> 
  status.list_transitions -> 
  valid_transitions
}
```

---

## Filter Registry Help

### Get Help
```ops
voice main / {
  plan_filter_registry -> 
  filter.help -> 
  filter_help
}
```

### Help for Specific Filter
```ops
voice main / {
  plan_filter_registry + "bootstrap" -> 
  filter.help_filter -> 
  filter_help
}
```

### Discover Filters
```ops
voice main / {
  plan_filter_registry + "core" -> 
  filter.discover -> 
  matching_filters
}
```

### Category Help
```ops
voice main / {
  plan_filter_registry + "core" -> 
  category.help -> 
  category_help
}
```

---

## Music Registry Help

### Get Help
```ops
voice main / {
  music_impl_registry -> 
  music.help -> 
  music_help
}
```

### List All Scales
```ops
voice main / {
  music_impl_registry -> 
  music.list_scales -> 
  scale_list
}
```

### List All Chords
```ops
voice main / {
  music_impl_registry -> 
  music.list_chords -> 
  chord_list
}
```

### Discover Musical Elements
```ops
voice main / {
  music_impl_registry + "minor" -> 
  music.discover -> 
  matching_elements
}
```

---

## Translation Registry Help

### Get Help
```ops
voice main / {
  translation_registry -> 
  translation.help -> 
  translation_help
}
```

### List Language Pairs
```ops
voice main / {
  translation_registry -> 
  translation.list_languages -> 
  language_pairs
}
```

### List Rules for Language Pair
```ops
voice main / {
  translation_registry + "opic" + "swift" -> 
  translation.list_rules -> 
  rule_list
}
```

---

## Registering Entries with Help

When registering entries, include help information:

### Example: Registering a Custom Status

```ops
;; Register a new "archived" status with full help info
voice add_archived_status / {
  realm_status_registry + "archived" + "Archived" + [] + [] + {} + 
    "Archived status - entity permanently stored but inactive" + 
    "Use when entity is archived for historical reference" + 
    ["registry.archive_realm realm reason"] + 
    ["dissolved"] -> 
  status.register -> 
  updated_registry
}

;; Now it's discoverable
voice find_archived / {
  realm_status_registry + "archive" -> 
  status.discover -> 
  ;; Returns: archived status
  archived_status
}
```

### Example: Registering a Custom Filter

```ops
;; Register a new "test" filter for test files
voice add_test_filter / {
  plan_filter_registry + "test" + ["test" "spec"] + "examples" + {} + 
    "Test files - unit tests and specifications" + 
    "plan.filter_test files" + 
    ["plan.filter_test ops_files"] + 
    ["example"] -> 
  filter.register -> 
  updated_registry
}

;; Use it
voice get_test_files / {
  files + plan_filter_registry -> 
  category.apply "examples" -> 
  filter.apply "test" -> 
  test_files
}
```

### Example: Registering a Custom Translation Rule

```ops
;; Register a new Python translation rule
voice add_python_rule / {
  translation_registry + "mse" + "error = prediction - target" + 
    "error = prediction - target\nreturn error * error" + 
    "opic" + "python" + {} -> 
  translation.register -> 
  updated_registry
}

;; Use it
voice translate_mse_to_python / {
  translation_registry + "error = prediction - target" + "opic" + "python" -> 
  translation.translate -> 
  ;; Returns: "error = prediction - target\nreturn error * error"
  python_code
}
```

---

## Benefits

1. **Self-Documenting**: Registries explain themselves
2. **Discoverable**: Easy to find what you need
3. **Agent-Friendly**: Structured data for programmatic access
4. **Human-Friendly**: Clear descriptions and examples
5. **Consistent**: Same help interface across all registries

---

## Integration with Agent Help System

Registries integrate with `systems/agent_help.ops`:

```ops
include systems/agent_help.ops
include systems/registry/status.ops

voice help.registry_status / {
  realm_status_registry -> 
  status.help -> 
  format_for_agent -> 
  agent_help_data
}
```

---

*"Every registry knows how to explain itself"*

