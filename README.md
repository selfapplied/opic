# Opic — Event-Based Compositional Language

Opic is an event-based compositional language. Programs are arrangements of typed flows called voices, resolved by a Composer that finds balanced transformations between types. The goal is not compilation but resonant composition—a lawful transformation of energy, structure, and intent.

## Structure

```
opic/
 ├── core.ops          # kernel and stoichiometry rules
 ├── runtime.ops       # manifest of bootstraps
 ├── tiddlywiki.ops    # TiddlyWiki composition definitions
 ├── python_boot.py    # CLI / scripting bootstrap
 ├── build_tiddlywiki.py  # TiddlyWiki build process
 ├── opic_boot.wasm    # web / low-level runtime
 ├── opic.html         # browser interface
 ├── opic.workflow     # macOS Automator wrapper
 └── tiddlers/         # family-organized content
     ├── ambiance.ops  # theme, palette, layout
     ├── widgets.ops   # navigation, search, editor
     ├── actions.ops   # save, load, compose
     └── content.ops   # content tiddlers
```

## TiddlyWiki Integration

Opic composes TiddlyWiki wikis from `.ops` scores organized by families:

- **ambiance** (order: 1) — themes, palettes, layouts
- **widgets** (order: 2) — navigation, search, editor components
- **actions** (order: 3) — save, load, compose handlers
- **tiddlers** (order: 4) — content tiddlers

### Building

```bash
python3 build_tiddlywiki.py
```

This reads `tiddlywiki.ops` and all `.ops` files in `tiddlers/`, then composes `tiddlywiki.html`.

### Adding Content

Add definitions to family files in `tiddlers/`:

```ops
content mypage / { title: "My Page", text: "Content here", tags: ["family/tiddlers"] }
```

The build process automatically collects and orders tiddlers by family.

## Core Concepts

- **def** — Defines a type (positive form, structure)
- **voice** — Defines a transformation or event (negative form, flow)
- **target** — Declares an output domain (text, Zig, WASM, etc.)
- **compose** — Solver that finds minimal-energy flow between input and output
- **charge** — Polarity of flow: + emit, - absorb
- **mass** — Informational weight of a type

## Stoichiometry

Every transformation conserves informational mass and charge:

Σ(inputs.mass × inputs.charge) = Σ(outputs.mass × outputs.charge)

This guarantees reversible computation and enables energy-aware scheduling.

