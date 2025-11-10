# File Organization Plan

## Proposed Structure

```
opic/
├── core/              # Core language runtime
│   ├── bootstrap.ops
│   ├── opic_parse.ops
│   ├── opic_load.ops
│   ├── opic_execute.ops
│   └── core.ops
│
├── systems/           # System capabilities
│   ├── certificate.ops
│   ├── witness.ops
│   ├── signed.ops
│   ├── vfs.ops
│   ├── vmap.ops
│   ├── voice_ledger.ops
│   ├── fee.ops
│   ├── generational_resonance.ops
│   └── ...
│
├── wiki/              # Wiki/documentation layer
│   ├── tiddlywiki.ops
│   ├── tiddlywiki_build.ops
│   └── tiddlers/
│
├── examples/           # Example files
│   ├── example_signed.ops
│   └── ...
│
├── tests/             # Test files
│   ├── test.ops
│   ├── tests.ops
│   └── ...
│
├── docs/              # Documentation
│   ├── philosophy.md
│   ├── architecture.md
│   └── ...
│
└── [root]             # Entry points and build
    ├── opic           # CLI entry point
    ├── Makefile
    └── README.md
