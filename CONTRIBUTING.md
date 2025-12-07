# Contributing to opic

Thank you for your interest in contributing to opic! This guide will help you get started.

## Getting Started

opic is a self-hosting language — contribute by extending `.ops` files!

### Prerequisites

- Python 3.8 or higher
- Basic understanding of opic's voice and chain concepts
- Familiarity with the Core Axiom (see [docs/axiom.md](docs/axiom.md))

## How to Contribute

### 1. Fork and Clone

```bash
git clone https://github.com/yourusername/opic.git
cd opic
```

### 2. Create a Feature Branch

```bash
git checkout -b feature/amazing-feature
```

### 3. Make Your Changes

- Add your `.ops` files following opic's pattern language
- Ensure your voices preserve fundamental invariants
- Test your changes thoroughly

### 4. Follow Coding Conventions

- **Voices**: Define transformation functions that preserve invariants
- **Chains**: Compose voices using `->` for field flows
- **Documentation**: Add comments explaining complex invariant preservation logic
- **Testing**: Add tests that verify invariant preservation

### 5. Test Your Changes

Run the test suite to ensure your changes don't break existing functionality:

```bash
make test
```

Run case studies to verify integration:

```bash
make case-studies
```

### 6. Commit Your Changes

```bash
git commit -m 'Add amazing feature'
```

Use descriptive commit messages that explain what invariants your code preserves or what functionality it adds.

### 7. Push and Create a Pull Request

```bash
git push origin feature/amazing-feature
```

Then open a Pull Request on GitHub.

## Development Guidelines

### Invariant-Generative Worldbuilding

All contributions should align with opic's Core Axiom:

> All generative systems must preserve fundamental invariants under transformation.

When adding new features:
1. Identify what invariants must be preserved
2. Use Aquifer primitives (Feigenbaum, Zeta, RG flows) where appropriate
3. Verify invariant preservation in your tests

### Code Organization

- `core/` - Bootstrap voices and core functionality
- `systems/` - System-level voices and implementations
- `examples/` - Example programs and demonstrations
- `case_studies/` - Real-world applications and validation
- `docs/` - Documentation and theory
- `src/aquifer/` - Aquifer primitive implementations

### Testing

- Add tests for new voices in `examples/test_*.py`
- Use the TestRunner pattern from existing tests
- Verify invariant preservation numerically
- Test edge cases and boundary conditions

## Reporting Issues

Found a bug or have a feature request? Please open an issue on GitHub with:

- A clear description of the problem or feature
- Steps to reproduce (for bugs)
- Expected vs. actual behavior
- Relevant code snippets or error messages

## Questions?

- Open a discussion on GitHub
- Check existing documentation in `docs/`
- Review example programs in `examples/`

## License

By contributing to opic, you agree that your contributions will be licensed under the Creative Commons Attribution 4.0 International License.

---

**Built with opic, by opic, for opic —**

*Thank you for helping opic learn to speak for itself!*
