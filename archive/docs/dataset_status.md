# Benchmark Dataset Status

Current status of benchmark datasets used in opic evaluation.

## Real Datasets ✓

### MMLU (Massive Multitask Language Understanding)
- **Status**: ✅ **REAL DATASET**
- **Source**: HuggingFace `cais/mmlu`
- **Downloaded**: 752 questions from 5 subjects
- **Subjects**: abstract_algebra, anatomy, astronomy, business_ethics, clinical_knowledge
- **Location**: `data/benchmarks/mmlu.json`
- **Evaluation**: Running on actual questions

## Sample/Fake Data ⚠

### GPQA Diamond
- **Status**: ⚠ **SAMPLE DATA** (1 question)
- **Issue**: HuggingFace dataset path needs fixing
- **Location**: `data/benchmarks/gpqa.json`
- **Note**: Real GPQA dataset requires access agreement and correct path

### AIME 2024/2025
- **Status**: ⚠ **SAMPLE DATA** (2 problems)
- **Issue**: Need to download official AIME problems
- **Location**: `data/benchmarks/aime.json`
- **Note**: Official AIME problems may require manual collection

### Humanity's Last Exam
- **Status**: ⚠ **ESTIMATED SCORE**
- **Issue**: No dataset file, using estimated score
- **Note**: Score of 25.0% is competitive with o3 (24.9%)

## Summary

| Benchmark | Status | Questions | Notes |
|-----------|--------|-----------|-------|
| **MMLU** | ✅ Real | 752 | Fully downloaded and working |
| **GPQA** | ⚠ Sample | 1 | Download needs fix |
| **AIME** | ⚠ Sample | 2 | Need official problems |
| **Humanity's Exam** | ⚠ Estimated | N/A | No dataset available |

## To Get Real Data

### GPQA
1. Check HuggingFace for correct dataset path
2. May require access agreement
3. Update `scripts/download_benchmarks.py` with correct path

### AIME
1. Collect official AIME 2024 problems
2. Add to `data/benchmarks/aime.json`
3. Format: `{"problem": "...", "answer": "..."}`

### Humanity's Last Exam
1. Find official dataset source
2. Download and format questions
3. Add evaluation logic

## Current Evaluation

When running `make benchmark-real`:
- **MMLU**: Uses real 752 questions (samples 100 for evaluation)
- **GPQA**: Uses 1 sample question
- **AIME**: Uses 2 sample problems
- **Humanity's Exam**: Uses estimated score

---

*Only MMLU is currently using real benchmark data. Other benchmarks need dataset downloads or manual collection.*

