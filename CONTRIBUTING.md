# Contributing to opic

Thank you for your interest in contributing to opic! This document provides guidelines and instructions for contributing.

## How to Contribute

opic is self-hosting — contribute by extending `.ops` files!

### Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/opic.git`
3. Create a feature branch: `git checkout -b feature/amazing-feature`
4. Make your changes
5. Test your changes
6. Commit your changes: `git commit -m 'Add amazing feature'`
7. Push to your branch: `git push origin feature/amazing-feature`
8. Open a Pull Request

### Code Style

#### File Headers

All `.ops` files should start with a header comment:

```ops
;;; filename.ops — brief description
```

#### Includes

Use `include` statements to connect to existing opic systems:

```ops
include certificate.ops
include witness.ops
include tiddlywiki.ops
```

#### Voice Definitions

Follow opic's pattern language:

```ops
voice action.name / {input -> step1 -> step2 -> output}
```

#### Capability Definitions

Use capability pattern syntax:

```ops
capability.name:
  If condition
  Then step1
  Then step2
```

### Project Structure

- **Core Systems** (`*.ops` in root) — Language runtime, certificates, VFS
- **Launch Systems** (`*.ops` in root) — FEE, RCT, learning pools
- **Wiki Layer** (`tiddlers/`) — Conversion tools, markup handling, drive system
- **Documentation** (`*.md`) — README, CONTRIBUTING, integration papers

### Testing

Before submitting a pull request:

1. Test your changes: `make test`
2. Run opic bootstrap: `make bootstrap`
3. Verify integration points connect correctly
4. Check that includes resolve properly

### Integration Guidelines

When adding new capabilities:

1. **Identify Integration Points** — What existing systems does your code connect to?
2. **Add Includes** — Include necessary opic systems
3. **Follow Patterns** — Use existing opic pattern language
4. **Document** — Add comments explaining your contribution

### Pull Request Process

1. Update documentation if needed
2. Add tests if applicable
3. Ensure all includes resolve
4. Follow existing code style
5. Write clear commit messages

### Questions?

- Check existing `.ops` files for examples
- Review `tiddlers/INTEGRATION_PAPER.md` for integration patterns
- Open an issue for discussion

Thank you for contributing to opic!

