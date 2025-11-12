# Automatic Voice Discovery in opic

opic's execution semantics now include **automatic voice discovery** - voices are automatically discovered and made available during chain execution based on context.

## How It Works

### Discovery Mechanism

When executing a voice chain, opic automatically discovers relevant voices based on:

1. **Chain context**: Keywords in the chain steps
2. **Step context**: The voice being executed and its body
3. **Semantic matching**: Voice namespaces that match the context

### Discovery Patterns

| Context Keywords | Discovered Voices |
|-----------------|-------------------|
| `learn`, `energy`, `density`, `critical`, `phase`, `resonance`, `cycle` | `thermo.*` |
| `energy`, `curvature`, `potential`, `field`, `wave`, `flow`, `xi` | `field.*` |
| `cycle`, `promote`, `dimension`, `operator`, `resonance` | `cycle.*` |
| `combinatorial`, `mod`, `projection`, `pascal` | `pascal.*` |
| `symmetry`, `curvature`, `theta`, `tan`, `sin`, `cos` | `trig.*` |
| `flow`, `equilibrium`, `hermitian`, `forward`, `backward` | `flow.*` |
| `language`, `attention`, `masked`, `token`, `semantic` | `nlp.*` |
| `dimension`, `symmetry`, `witness`, `expand` | `dimension.*` |

### Example

When executing `reason.answer`:

```ops
voice reason.answer / {question -> reason.understand -> reason.reason -> reason.select -> answer}
```

opic automatically discovers:
- `thermo.*` voices (if context involves learning/energy)
- `field.*` voices (if context involves energy/curvature)
- `cycle.*` voices (if context involves cycles/promotion)
- Other relevant voices based on semantic context

## Integration with §8 and §9

### Dimensional Thermodynamics (§8)

When executing chains involving:
- Learning (`learn`, `energy`, `density`)
- Criticality (`critical`, `phase`)
- Cycles (`cycle`, `resonance`)

→ Automatically discovers `thermo.*` voices:
- `thermo.learning_density`
- `thermo.dimensional_criticality`
- `thermo.cycle_annihilation`
- `thermo.witness_singularity`
- ... (47 total thermo voices)

### Dimensional Field Equations (§9)

When executing chains involving:
- Energy (`energy`, `curvature`, `potential`)
- Fields (`field`, `wave`, `flow`)
- Xi-form (`xi`, `energy`, `flow`)

→ Automatically discovers `field.*` voices:
- `field.xi_operator`
- `field.wave_equation`
- `field.energy_exchange`
- `field.ricci_zeta_flow`
- ... (29 total field voices)

## Usage

### Automatic Discovery During Execution

```python
from scripts.opic_executor import OpicExecutor
from pathlib import Path

executor = OpicExecutor(Path('.'))

# Execute reason.answer - thermo/field voices automatically discovered
result = executor.answer_question("What is energy?", ["A", "B", "C", "D"])

# During execution:
# 1. Discovers thermo.* voices (energy context)
# 2. Discovers field.* voices (energy context)
# 3. Makes them available for automatic composition
```

### Manual Discovery

```python
# Discover voices for a specific context
discovered = executor._discover_relevant_voices("learn energy density critical")
# Returns: ['thermo.learning_density', 'thermo.dimensional_criticality', ...]
```

## Benefits

1. **No explicit composition needed**: Voices are discovered automatically
2. **Context-aware**: Discovery matches semantic context
3. **Extensible**: New voices are automatically discoverable
4. **Backward compatible**: Existing chains work unchanged

## Implementation

The discovery mechanism is implemented in `scripts/opic_executor.py`:

- `_discover_relevant_voices()`: Discovers voices based on context
- `_execute_opic_chain()`: Uses discovery during chain execution
- `_enhance_with_discovered()`: Enhances results with discovered voices

## Status

✅ **Implemented**: Automatic voice discovery  
✅ **Integrated**: Works with §8 (thermo) and §9 (field) voices  
✅ **Active**: Discovery happens during chain execution  
🔄 **Enhancement**: Automatic composition of discovered voices (future)

---

*Automatic voice discovery makes opic's execution semantics truly automatic - voices are discovered and used based on context, not explicit references.*

