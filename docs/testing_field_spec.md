# Testing Field Spec 0.7

Comprehensive test suite for Field Specification 0.7 and Cycle-to-Dimension Principle.

## Test Files

### 1. `tests/test_cycle_to_dimension.ops`
Tests for the Cycle-to-Dimension Principle:
- Cycle phase computation
- Cycle charge computation
- Dimensional promotion
- Identity cycle → time operator
- Dialogue cycle → rotation operator
- 7-trace → complex unit
- Learning threshold
- Promotion functor
- Quantization rule
- Hermitian promotion

### 2. `tests/test_nlp_cycles.ops`
Tests for NLP cycle voices:
- Masked prediction cycle
- Masked promotion to context operator
- Attention cycle (Hermitian)
- Hermitian attention operator
- Attention dialogue → relational operator
- Multi-head spin network
- Training epoch cycle
- NLP learning threshold
- Token quantization
- Bidirectional complexification
- Hierarchical learning
- Semantic conservation

### 3. `tests/test_field_spec_0.7.ops`
Tests for Field Spec 0.7 components:
- Pascal Mod 10 operations
- Trigonometric operators
- Flow symmetry
- Bracket operators
- Galois extensions
- Voice formalism
- Dimensional expansion
- Cycle-to-dimension principle
- Dimensional Coulomb law
- ML connections

### 4. `tests/test_field_spec_capabilities.ops`
Capability tests (verify voices exist):
- Pascal operations available
- Trigonometric operators available
- Flow symmetry available
- Cycle-to-dimension available
- NLP cycles available
- Dimensional expansion available
- Field Spec 0.7 fully loaded

### 5. `scripts/test_field_spec.py`
Python test runner with execution tests:
- Voice availability verification
- Cycle execution tests
- NLP cycle execution tests

## Running Tests

### Run All Field Spec Tests

```bash
make test-field-spec
```

### Run Individual Test Files

```bash
# Cycle-to-dimension tests
python3 opic execute tests/test_cycle_to_dimension.ops

# NLP cycle tests
python3 opic execute tests/test_nlp_cycles.ops

# Field Spec component tests
python3 opic execute tests/test_field_spec_0.7.ops

# Capability tests
python3 opic execute tests/test_field_spec_capabilities.ops
```

### Run Python Test Runner

```bash
python3 scripts/test_field_spec.py
```

## Test Results

### Expected Output

```
============================================================
Field Spec 0.7 Tests
============================================================

Loaded 375 voices

Test 1: Voice Availability
------------------------------------------------------------
  ✓ pascal: PASS
  ✓ trig: PASS
  ✓ flow: PASS
  ✓ cycle: PASS
  ✓ nlp_cycles: PASS
  ✓ dimension: PASS

  Result: 6/6 categories available

Test 2: Cycle Execution
------------------------------------------------------------
  ✓ cycle_phase: PASS
  ✓ cycle_promotion: PASS
  ✓ learning_threshold: PASS

  Result: 3/3 tests passed

Test 3: NLP Cycle Execution
------------------------------------------------------------
  ✓ masked_cycle: PASS
  ✓ attention_cycle: PASS
  ✓ hermitian_attention: PASS

  Result: 3/3 tests passed

============================================================
Summary
============================================================
  Voice Availability: PASS
  Cycle Execution: PASS
  NLP Cycle Execution: PASS

  Overall: PASS
```

## What Tests Verify

1. **Voice Availability**: All Field Spec 0.7 voices are loaded by default
2. **Cycle Execution**: Cycle-to-dimension voices can be executed
3. **NLP Cycle Execution**: NLP cycle voices can be executed
4. **Capability Tests**: Voices exist and can be referenced

## Integration with CI/CD

Add to your CI pipeline:

```yaml
# Example GitHub Actions
- name: Test Field Spec 0.7
  run: make test-field-spec
```

## Test Coverage

- ✅ Pascal Mod 10 operations
- ✅ Trigonometric operators
- ✅ Flow symmetry
- ✅ Bracket operators
- ✅ Galois extensions
- ✅ Voice formalism
- ✅ Dimensional expansion
- ✅ Cycle-to-dimension principle (10 tests)
- ✅ NLP cycles (12 tests)
- ✅ Dimensional Coulomb law
- ✅ ML connections

---

*All tests verify that Field Spec 0.7 is loaded by default and all voices are available.*

