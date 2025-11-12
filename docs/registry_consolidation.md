# Registry Consolidation

**All registries moved to `systems/registry/` and syntax defined via registry**

---

## ✅ Consolidated Registry Structure

All registry files are now in `systems/registry/`:

```
systems/registry/
├── base.ops          (was base_registry.ops)
├── status.ops        (was status_registry.ops)
├── filter.ops        (was filter_registry.ops)
├── translation.ops   (was translation_registry.ops)
└── music.ops         (was music_registry.ops)
```

---

## ✅ Updated Includes

All files now use consistent paths:
- `include registry/base.ops`
- `include registry/status.ops`
- `include registry/filter.ops`
- `include registry/translation.ops`
- `include registry/music.ops`

---

## ✅ Grammar Syntax via Registry

Grammar extensions are now registered in the registry system:

### Syntax Registry
```ops
include grammar/syntax.ops

;; Initialize syntax registry
voice init_syntax / {
  -> 
  syntax.init -> 
  syntax_registry
}

;; Get help for syntax rules
voice get_syntax_help / {
  syntax_registry -> 
  syntax.help -> 
  syntax_help
}

;; Discover syntax rules
voice find_syntax / {
  syntax_registry + "register" -> 
  syntax.discover -> 
  matching_rules
}
```

### Registering New Syntax Rules

```ops
;; Register custom syntax rule
voice add_custom_syntax / {
  syntax_registry + "register_scale" + "register scale" + "grammar.transform_register_scale" + 1 + 
    "Transforms 'register scale \"name\" with {...}' to scale.register call" + 
    "register scale \"major\" with { intervals: \"2,2,1,2,2,2,1\" }" + 
    ["register scale \"major\" with { intervals: \"2,2,1,2,2,2,1\" }"] -> 
  grammar.register_rule -> 
  updated_registry
}
```

---

## 📋 Benefits

1. **Single Location**: All registries in one place
2. **Consistent Naming**: No underscores, short names
3. **Discoverable**: Syntax rules registered and discoverable
4. **Extensible**: Add new syntax rules via registry
5. **Self-Documenting**: Syntax rules have help/description/examples

---

## 🎯 Usage Example

### Before (Verbose)
```ops
voice register_active / {
  status_registry + "active" + "Active" + [] + [] + {} + 
    "Active status" + 
    "Use when active" + 
    ["example"] + 
    ["suspended"] -> 
  status.register -> 
  updated
}
```

### After (Crisp)
```ops
include grammar/syntax.ops

register status "active" with {
  display: "Active"
  transitions: []
  handlers: []
  metadata: {}
  description: "Active status"
  usage: "Use when active"
  examples: ["example"]
  related: ["suspended"]
}
```

---

*"All registries in one place, syntax defined via registry"*

