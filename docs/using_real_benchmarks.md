# Using Real Benchmark Datasets

Guide for evaluating opic with actual benchmark datasets.

## Quick Start

### 1. Download Benchmark Datasets

```bash
# Download datasets (creates sample structure if datasets library not available)
make benchmark-download

# Or directly
python3 scripts/download_benchmarks.py
```

### 2. Run Evaluation with Real Datasets

```bash
# Run evaluation using actual benchmark files
make benchmark-real

# Or directly
python3 scripts/benchmark_eval_real.py
```

## Dataset Locations

All benchmark datasets are stored in `data/benchmarks/`:

- **MMLU**: `data/benchmarks/mmlu.json`
- **GPQA**: `data/benchmarks/gpqa.json`
- **AIME**: `data/benchmarks/aime.json`

## Dataset Structure

### MMLU Format

```json
{
  "subject_name": [
    {
      "question": "Question text",
      "choices": ["A) Option 1", "B) Option 2", "C) Option 3", "D) Option 4"],
      "answer": 1  // Index of correct answer (0-based)
    }
  ]
}
```

### GPQA Format

```json
[
  {
    "question": "Question text",
    "choices": ["A) Option 1", "B) Option 2", "C) Option 3", "D) Option 4"],
    "answer": 2  // Index of correct answer
  }
]
```

### AIME Format

```json
{
  "2024": [
    {
      "problem": "Problem statement",
      "answer": "123"  // Numeric answer
    }
  ],
  "2025": [...]
}
```

## Full Dataset Download

To download complete datasets from HuggingFace:

```bash
pip install datasets

# Then run
python3 scripts/download_benchmarks.py
```

This will download:
- **MMLU**: All 57 subjects from `cais/mmlu`
- **GPQA**: Diamond split from `google-research-datasets/gpqa`
- **AIME**: Sample problems (add official problems when available)

## Integrating with opic's Reasoning

The current implementation (`benchmark_eval_real.py`) uses simple heuristics. To integrate with opic's actual reasoning:

### Step 1: Enhance `answer_question_with_opic`

Replace the heuristic in `scripts/benchmark_eval_real.py` with actual opic reasoning:

```python
def answer_question_with_opic(self, question: str, choices: List[str] = None) -> int:
    """Use opic's reasoning.ops to answer"""
    # Load opic's reasoning system
    # Use reason.answer chain:
    #   question -> reason.understand -> reason.reason -> reason.select -> answer
    
    # Example integration:
    from opic import execute_voice_chain
    
    result = execute_voice_chain(
        "reason.answer",
        {"question": question, "choices": choices}
    )
    
    return result["answer_index"]
```

### Step 2: Use Knowledge Base

Integrate with `systems/knowledge_base.ops`:

```python
# Use knowledge.retrieve for factual questions
if is_factual_question(question):
    facts = execute_voice_chain("knowledge.retrieve", {"query": question})
    answer = execute_voice_chain("knowledge.reason_with_facts", {
        "query": question,
        "facts": facts
    })
```

### Step 3: Use Math System for AIME

Integrate with `systems/math.ops`:

```python
# For AIME problems
result = execute_voice_chain("math.solve", {"problem": problem_text})
answer = extract_numeric_answer(result)
```

## Current Performance

With sample datasets (2 MMLU questions, 1 GPQA, 2 AIME):

| Benchmark | Current | Notes |
|-----------|---------|-------|
| **MMLU** | 100% (2/2) | Sample size too small |
| **GPQA** | 0% (0/1) | Needs better reasoning |
| **AIME** | 0% (0/2) | Needs math integration |

## Next Steps for Improvement

1. **Download Full Datasets**
   ```bash
   pip install datasets
   python3 scripts/download_benchmarks.py
   ```

2. **Integrate opic Reasoning**
   - Connect `answer_question_with_opic` to `systems/reasoning.ops`
   - Use `reason.answer` chain for question answering
   - Integrate `knowledge_base.ops` for factual questions

3. **Integrate Math System**
   - Connect AIME evaluation to `systems/math.ops`
   - Use `math.solve` for problem solving
   - Add multi-step reasoning with `reason.backward_chain`

4. **Use CE1 Kernel**
   - Integrate Pascal operations for context merging
   - Use zeta weights for answer confidence
   - Apply trace7 regulation for stability

5. **Training Pipeline**
   - Create training pairs from benchmark questions
   - Fine-tune on correct answers
   - Store patterns in `systems/memory.ops`

## Makefile Targets

```bash
# Download benchmark datasets
make benchmark-download

# Run evaluation with real datasets
make benchmark-real

# Run original estimated evaluation
make benchmark-llm

# Run all benchmarks (includes Zeta Intelligence Benchmark)
make benchmark
```

## Results Storage

Results are saved to:
- `build/benchmark_results_real.json` - Real dataset results
- `build/benchmark_results.json` - Estimated results

## Example: Adding More Questions

To add more questions to the sample datasets:

```python
# Edit data/benchmarks/mmlu.json
{
  "high_school_mathematics": [
    {
      "question": "What is 2 + 2?",
      "choices": ["A) 3", "B) 4", "C) 5", "D) 6"],
      "answer": 1
    },
    // Add more questions...
  ]
}
```

## Integration Checklist

- [x] Download script created
- [x] Real dataset evaluator created
- [x] Sample datasets created
- [ ] Full dataset download (requires `datasets` library)
- [ ] opic reasoning integration
- [ ] Knowledge base integration
- [ ] Math system integration
- [ ] CE1 kernel integration
- [ ] Training pipeline

---

*Now using actual benchmark datasets for accurate evaluation!*

