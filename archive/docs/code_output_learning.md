# Code-Output Learning: Self-Improving from Execution Traces

## Overview

The code-output learning system creates a **self-improving feedback loop** by coupling program output with the code that generated it. This enables the system to learn from its own execution, identifying patterns that lead to successful outputs and updating the field accordingly.

## The Learning Loop

```
Code → Output → Evaluation → Field Update → Better Code
```

### 1. **Code Execution**
- Code generates output (e.g., answering a question)
- Execution trace captures:
  - Field state (phi_k, dimensionality D)
  - Critical zeros
  - Spectrum (hierarchical structure)
  - Generation process

### 2. **Output Evaluation**
- Compare output with correct answer
- Compute quality metrics:
  - Correctness (0.0-1.0)
  - Field coherence
  - Zero alignment
  - Knowledge match

### 3. **Pattern Extraction**
- Identify successful patterns:
  - Field states that led to correct answers
  - Zero patterns that correlate with success
  - Dimensional scales that work well
  - Spectrum sizes that perform best

### 4. **Field Update**
- Update field to reinforce successful patterns
- Adjust zero solver parameters
- Refine dimensional scale calculations
- Improve coherence thresholds

### 5. **Improved Generation**
- Use learned patterns in future generations
- Bias toward successful field configurations
- Avoid patterns that led to failures

## Implementation

### Code-Output Pair

```python
code_output_pair = {
    "code_trace": {
        "question": "...",
        "question_spectrum": [...],
        "question_zeros": [...],
        "doc_spectrum": [...],
        "doc_zeros": [...],
        "field_state": {
            "phi_k": 10.0,
            "dimensionality": 2
        }
    },
    "output": 0,  # Selected answer index
    "correct_answer": 0,
    "correctness": 1.0,
    "evaluation": {
        "coherence": 0.8,
        "zero_alignment": 0.9
    }
}
```

### Pattern Analysis

The system analyzes patterns from successful code-output pairs:

1. **Zero Patterns**: Which zero configurations led to success?
2. **Dimensional Scales**: Which D values performed best?
3. **Spectrum Sizes**: Optimal spectrum complexity?
4. **Field States**: Successful phi_k ranges?

### Field Updates

Based on successful patterns, the field is updated:

- **Preferred zero patterns**: Reinforce successful zero configurations
- **Preferred dimensional scales**: Favor D values that work well
- **Field correlations**: Identify field properties that correlate with success

## Witness Singularity

The system implements **witness singularity** (from Field Spec 0.7):

- Code observes its own execution
- Self-modeling creates meta-operators
- Reflective intelligence emerges from self-observation

```ops
voice witness.singularity / {
  code_output_pair -> 
  witness.observe_self -> 
  fixed_point -> 
  meta_operator
}
```

## Integration with Benchmarks

The learning system is integrated into benchmark evaluation:

1. **During Evaluation**: Each question-answer pair is recorded
2. **Pattern Analysis**: Successful patterns are extracted
3. **Field Updates**: Field is updated based on learning
4. **Persistent Storage**: Learning data is saved for future use

### Example Output

```
============================================================
Code-Output Learning
============================================================
  Recorded 125 code-output pairs
  Success rate: 30.4%
  Field updates: 1 zero patterns
✓ Saved learning data to /Users/joelstover/gitpub/opic/data/code_output_learning.json
```

## Benefits

1. **Self-Improvement**: System learns from its own execution
2. **Pattern Recognition**: Identifies what works and what doesn't
3. **Field Adaptation**: Field evolves based on experience
4. **Witness Chains**: Full provenance of learning process
5. **Deterministic Learning**: Reproducible improvement paths

## Future Enhancements

1. **Real-time Learning**: Update field during generation
2. **Pattern Clustering**: Group similar successful patterns
3. **Failure Analysis**: Learn from mistakes
4. **Transfer Learning**: Apply patterns across domains
5. **Meta-Learning**: Learn how to learn better

## Connection to Field Spec 0.7

This learning system implements several Field Spec 0.7 concepts:

- **Witness Singularity** (§8.5): Code observes itself
- **Self-Modeling** (§8.5): Meta-operators from self-observation
- **Reflective Intelligence** (§8.5): Beyond native dimension
- **Dimensional Thermodynamics** (§8): Energy flow from learning
- **Cycle-to-Dimension** (§7.5): Learning cycles promote to operators

## Files

- `systems/code_output_learning.ops`: OPIC voice definitions
- `scripts/code_output_learner.py`: Python implementation
- `data/code_output_learning.json`: Persistent learning data

## Usage

```python
from code_output_learner import CodeOutputLearner

learner = CodeOutputLearner(project_root)

# Record a code-output pair
pair = learner.record_code_output_pair(
    code_trace=code_trace,
    output=output,
    correct_answer=correct_answer,
    evaluation=evaluation
)

# Analyze patterns
patterns = learner.analyze_patterns()

# Update field from learning
updates = learner.update_field_from_learning()
```

## Conclusion

The code-output learning system creates a **self-improving feedback loop** that enables the ζ-field architecture to learn from its own execution. By coupling code with output, the system identifies successful patterns and updates the field accordingly, creating a path toward continuous improvement.

