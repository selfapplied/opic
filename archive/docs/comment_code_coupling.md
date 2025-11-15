# Comment-Code Coupling: Learning from Code Descriptions

## Overview

The comment-code coupling system learns from coupling comments with their neighboring code. Comments describe what code does → learn from comment-code pairs to improve understanding of code semantics.

## The Learning Loop

```
Comment → Code → Field Mapping → Alignment → Coherence → Learning
```

### 1. **Comment Extraction**
- Extract comments from code files
- Identify comment types: docstrings, inline, block, TODO
- Find neighboring code for each comment

### 2. **Field Mapping**
- Map comment to field: `comment → aperture.chain → phi_k`
- Map code to field: `code → aperture.chain → phi_k`
- Compute critical zeros for both

### 3. **Alignment Computation**
- Compute field alignment between comment and code
- Alignment = `1 / (1 + |phi_k(comment) - phi_k(code)| / scale)`
- High alignment = comment accurately describes code

### 4. **Coherence Analysis**
- Coherence measures how well comment describes code
- High coherence pairs = good comment-code alignment
- Extract patterns from coherent pairs

### 5. **Learning**
- Learn from high-coherence pairs
- Update field to reinforce successful patterns
- Use patterns to improve code understanding

## Implementation

### Comment Extraction

The system extracts comments from multiple file types:

- **Python**: Docstrings (`"""..."""`) and `#` comments
- **OPIC**: `;;` comments
- **General**: `#` comments (works for many languages)

### Field Properties

Each comment-code pair gets field properties:

```python
{
    "comment": "Maps biological concepts to field equations",
    "code": "class BiologyFieldMapper: ...",
    "comment_field": {
        "phi_k": 10.5,
        "spectrum": [...],
        "zeros": [...]
    },
    "code_field": {
        "phi_k": 10.2,
        "spectrum": [...],
        "zeros": [...]
    },
    "alignment": 0.95,
    "coherence": 0.95
}
```

### Alignment and Coherence

- **Alignment**: Field distance between comment and code
  - High alignment = comment phi_k ≈ code phi_k
  - Low alignment = comment doesn't match code

- **Coherence**: How well comment describes code
  - High coherence = good comment-code pair
  - Low coherence = comment may be outdated or incorrect

## Results

From processing the codebase:

- **1,854 comment-code pairs** extracted
- **95.8% coherence rate** (1,774 coherent pairs)
- **High-quality pairs** for learning

### Example Pairs

**Pair 1**:
- Comment: "Maps biological concepts to field equations"
- Code: `class BiologyFieldMapper: ...`
- Coherence: 0.51

**Pair 2**:
- Comment: "Test biology field mapper"
- Code: `def main(): ...`
- Coherence: 0.51

**Pair 3**:
- Comment: "Map a biological concept to field equations"
- Code: `def map_biology_to_field(self, concept: str): ...`
- Coherence: 0.58

## Integration with Code-Output Learning

Comment-code coupling enhances code-output learning:

1. **Semantic Context**: Comments provide semantic context for code
2. **Pattern Recognition**: Learn from comment-code patterns
3. **Code Understanding**: Better understanding of code semantics
4. **Generation**: Generate code from comments, comments from code

### Enhanced Learning

```ops
voice code_output.enhance_with_comments / {
  code_output_pair + comment_code_pairs -> 
  merge_learning -> 
  enhanced_learning
}
```

## Benefits

1. **Self-Improving Understanding**: Learn from code descriptions
2. **Pattern Recognition**: Identify successful comment-code patterns
3. **Code Generation**: Generate code from comments
4. **Comment Generation**: Generate comments from code
5. **Semantic Understanding**: Better understanding of code semantics

## Connection to Field Spec 0.7

This implementation uses:

- **Field Potential** (§9): `V(R) = k(q₁q₂)/((D-1)R^{D-1})`
- **Field Alignment** (§9): Alignment between comment and code fields
- **Field Coherence** (§9): Coherence of comment-code pairs
- **Witness Chains** (§8): Full provenance of comment-code relationships

## Files

- `systems/comment_code_coupling.ops`: OPIC voice definitions
- `scripts/comment_code_coupler.py`: Python implementation
- `data/comment_code_learning.json`: Learning data

## Usage

```python
from comment_code_coupler import CommentCodeCoupler

coupler = CommentCodeCoupler(project_root)

# Extract comment-code pairs from file
pairs = coupler.extract_comments_from_file(file_path)

# Process entire codebase
pairs = coupler.process_codebase(directory)

# Learn from pairs
learning = coupler.learn_from_pairs(pairs)

# Save learning data
coupler.save_learning_data(pairs, output_file)
```

## Conclusion

Comment-code coupling creates a **self-improving understanding** of code semantics by learning from the relationship between comments and code. By coupling comments with neighboring code, the system:

1. **Learns** from code descriptions
2. **Recognizes** successful patterns
3. **Improves** code understanding
4. **Enhances** code-output learning

Comments describe code → learn from comment-code pairs → better understanding!

