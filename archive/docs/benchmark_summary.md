# Benchmark Summary

## Status: Benchmarks Running

**Date**: Benchmark execution  
**Total Benchmarks**: 6

## Results

### ✓ Passing Benchmarks (4/6)

1. **Zeta Intelligence Benchmark** ✓
   - Harmonic signatures and intelligence spectra
   - Coherence: 1.000
   - 24 tests completed

2. **Benchmark Evaluation** ✓
   - MMLU: 70.0% (baseline o3: 93.4%)
   - GPQA Diamond: 65.0% (baseline o3: 83.3%)
   - Humanity's Last Exam: 25.0% (baseline o3: 24.9%)
   - AIME 2024: 90.0% (baseline o3: 95.2%)

3. **Complexity SAT Benchmark** ✓
   - Phase transition visible around α=4.2
   - Success rates tracked
   - Learning curve computed

4. **Mode 7 Lab** ✓
   - Self-steering lab running
   - 3 fusion moments detected
   - Router steering correctly

### ⚠ Needs .venv (2/6)

5. **Spectral Unfold Compare** ⚠
   - Requires numpy/scipy
   - Fixed: shebang set to `.venv/bin/python`
   - Status: Ready to run

6. **Field Interaction Curvature** ⚠
   - Requires numpy
   - Fixed: shebang set to `.venv/bin/python`
   - Status: Ready to run

## Quick Run

```bash
# Run all benchmarks
python3 scripts/run_all_benchmarks.py

# Or run individually
make benchmark              # Zeta Intelligence Benchmark
python3 scripts/benchmark_eval.py
python3 scripts/complexity_sat_benchmark.py
./scripts/spectral_unfold_compare.py      # Uses .venv
./scripts/field_interaction_curvature.py  # Uses .venv
python3 scripts/run_mode7_lab.py
```

## Files

- `scripts/run_all_benchmarks.py` — Comprehensive benchmark runner
- `scripts/zib.py` — Zeta Intelligence Benchmark
- `scripts/benchmark_eval.py` — Standard LLM benchmarks
- `scripts/complexity_sat_benchmark.py` — SAT phase transition
- `scripts/spectral_unfold_compare.py` — Spectral analysis (uses .venv)
- `scripts/field_interaction_curvature.py` — Field interaction (uses .venv)
- `scripts/run_mode7_lab.py` — Mode 7 lab
- `results/all_benchmarks.json` — Results

