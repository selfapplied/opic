# OPIC Examples: CE1-ℋ Fusion

This directory contains examples demonstrating the CE1-ℋ fusion implementation.

## Overview

The CE1-ℋ fusion integrates CE1 (Compositional Expression Language Level 1) with the harmonic operator ℋ(x), creating a unified operator-universe where `ℋ(x)=0` becomes a CE1 fixed-point expression.

## Files

### Python Examples

#### `ce1_harmonic_demo.py`
Comprehensive demonstration of the CE1-ℋ fusion:
- CE1 bracket semantics
- Harmonic operator components
- Root finding on the critical line
- The complete fusion concept

Run with:
```bash
python3 examples/ce1_harmonic_demo.py
```

#### `test_ce1_harmonic.py`
Test suite validating the implementation:
- CE1 bracket types and parsing
- Harmonic operator evaluation
- Zeta function approximation
- Root finding algorithms
- CE1 evaluator configuration

Run with:
```bash
python3 examples/test_ce1_harmonic.py
```

### OPIC Examples

#### `ce1_harmonic_case_study.ops`
Case study in native OPIC format demonstrating:
- CE1 bracket semantics in OPIC
- Harmonic operator component mapping
- CE1 encoding of ℋ(x)
- The fusion explanation

Run with:
```bash
# From OPIC execution environment
opic execute examples/ce1_harmonic_case_study.ops
```

## Key Concepts

### CE1 Bracket Types

| Bracket | Type | Height | Semantic Meaning |
|---------|------|--------|------------------|
| `()` | Morphism | 1 | Transformations, rotational dynamics |
| `<>` | Witness | 0 | Fixed-point resolver, equilibria |
| `{}` | Boundary | 0 | Domain constraints, collapse |
| `[]` | Memory | 0 | LR sequencing, accumulation |

### Harmonic Operator

The harmonic operator is defined as:

```
ℋ(x) = ln(x) · ζ(x) · i·tan(πx/2) · sin(πx) · i·cos(πx)
```

### CE1 Encoding

In CE1, the harmonic operator is expressed as:

```
H(c) ::= {ln c} + [ζ c] + (tan c) + <sin c> + <i cos c>
```

Where each bracket maps to a component:
- `{ln c}` ↔ collapse/boundary
- `[ζ c]` ↔ accumulation/memory
- `(tan c)` ↔ phase/morphism
- `<sin c>` ↔ oscillation/witness
- `<i cos c>` ↔ oscillation/witness

### Root Condition

The root condition ℋ(x) = 0 becomes:

```
< H(c) >
```

This is a CE1 fixed-point expression that resolves to the x where ℋ(x) = 0.

## Expected Output

When running the demo, you should see:

1. **CE1 Bracket Semantics**: Demonstration of bracket types and parsing
2. **Harmonic Operator**: Definition, CE1 representation, and evaluation at sample points
3. **Root Finding**: Single root finding and critical line search
4. **CE1-ℋ Fusion**: Complete explanation of the unified operator-universe

When running the tests, you should see:

```
======================================================================
CE1-ℋ FUSION TEST SUITE
======================================================================

Testing CE1 bracket types...
  ✓ Bracket types defined correctly
Testing CE1 expression parsing...
  ✓ CE1 expressions parse correctly
...
======================================================================
TEST RESULTS: 10 passed, 0 failed
======================================================================
```

## Next Steps

After exploring these examples, you can:

1. **Extend CE1**: Add more bracket types or evaluation rules
2. **Improve ℋ(x)**: Refine the harmonic operator components
3. **Advanced Root Finding**: Implement more sophisticated numerical methods
4. **CE2**: Extend to CE2 with time-evolution
5. **Integration**: Use CE1-ℋ in your own OPIC programs

## References

- [CE1-ℋ Fusion Documentation](../docs/ce1_harmonic_fusion.md)
- [Aquifer Framework](../src/aquifer/)
- [OPIC Systems](../systems/)

## License

This project is licensed under the Creative Commons Attribution 4.0 International License.
