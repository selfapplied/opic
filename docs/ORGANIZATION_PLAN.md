# File Organization Plan

## Directory Structure

```
opic/
├── core/              # Core language runtime
│   ├── bootstrap.ops
│   ├── opic_parse.ops
│   ├── opic_load.ops
│   ├── opic_execute.ops
│   ├── core.ops
│   ├── parser.ops
│   ├── execute.ops
│   ├── pure_execute.ops
│   └── self_execute.ops
│
├── systems/           # System capabilities
│   ├── certificate.ops
│   ├── witness.ops
│   ├── signed.ops
│   ├── proof.ops
│   ├── vfs.ops
│   ├── vmap.ops
│   ├── voice_ledger.ops
│   ├── fee.ops
│   ├── generational_resonance.ops
│   └── ... (all system files)
│
├── wiki/              # Wiki/documentation layer
│   ├── tiddlywiki.ops
│   ├── tiddlywiki_build.ops
│   ├── tiddlywiki_network.ops
│   └── tiddlers/      # (stays in wiki/)
│
├── examples/          # Example files
├── tests/             # Test files
└── docs/              # Documentation
```

## Include Path Updates Needed

After moving files, update includes:
- `include bootstrap.ops` → `include core/bootstrap.ops`
- `include certificate.ops` → `include systems/certificate.ops`
- `include tiddlywiki.ops` → `include wiki/tiddlywiki.ops`
- etc.

