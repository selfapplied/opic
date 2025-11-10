#!/usr/bin/env python3
"""Zeta Intelligence Benchmark — Harmonic signatures and intelligence spectra"""

import json
import math
import time
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import subprocess
import sys

def load_zib_definitions():
    """Load ZIB definitions from zib.ops"""
    from generate import parse_ops
    
    zib_file = Path(__file__).parent / "zib.ops"
    if zib_file.exists():
        defs, voices = parse_ops(zib_file.read_text())
        return defs, voices
    return {}, {}

def compute_entropy(results):
    """Compute Shannon entropy of test results"""
    if not results:
        return 0.0
    
    # Normalize results to probabilities
    total = sum(results.values())
    if total == 0:
        return 0.0
    
    probs = [v / total for v in results.values() if v > 0]
    entropy = -sum(p * math.log2(p) for p in probs)
    return entropy

def compute_coherence(test_results):
    """Compute coherence metric — how well tests align"""
    if len(test_results) < 2:
        return 1.0
    
    # Coherence = 1 - variance of normalized scores
    scores = [1.0 if r else 0.0 for r in test_results.values()]
    mean = sum(scores) / len(scores)
    variance = sum((s - mean) ** 2 for s in scores) / len(scores)
    coherence = 1.0 - variance
    return max(0.0, coherence)

def compute_phase_error(test_results, expected_phase=1.0):
    """Compute phase error — deviation from expected harmonic phase"""
    # Phase error measures how far results deviate from perfect alignment
    scores = [1.0 if r else 0.0 for r in test_results.values()]
    actual_phase = sum(scores) / len(scores) if scores else 0.0
    phase_error = abs(actual_phase - expected_phase)
    return phase_error

def compute_harmonic_signature(test_results):
    """Compute complete harmonic signature for test results"""
    signature = {
        'entropy': compute_entropy(test_results),
        'coherence': compute_coherence(test_results),
        'phase_error': compute_phase_error(test_results),
        'amplitude': sum(1.0 if r else 0.0 for r in test_results.values()) / len(test_results) if test_results else 0.0,
        'frequency': len(test_results),
    }
    
    # Compute resonance (inverse of phase error, weighted by coherence)
    signature['resonance'] = signature['coherence'] * (1.0 - signature['phase_error'])
    
    return signature

def run_intelligence_tests():
    """Run intelligence tests and return results"""
    script = Path(__file__).parent / "intelligence_test.py"
    result = subprocess.run(
        [sys.executable, str(script)],
        capture_output=True,
        text=True,
        timeout=60
    )
    
    # Parse results from output
    test_results = {}
    if result.returncode == 0:
        lines = result.stdout.splitlines()
        for line in lines:
            if "✓ PASS" in line:
                test_name = line.split("✓ PASS")[1].strip()
                test_results[test_name] = True
            elif "✗ FAIL" in line:
                test_name = line.split("✗ FAIL")[1].strip()
                test_results[test_name] = False
    
    return test_results, result.stdout

def load_historical_data():
    """Load historical benchmark data"""
    data_file = Path(__file__).parent / ".zib_history.json"
    if data_file.exists():
        with open(data_file) as f:
            return json.load(f)
    return []

def save_benchmark(signature, test_results, timestamp):
    """Save benchmark data"""
    data_file = Path(__file__).parent / ".zib_history.json"
    history = load_historical_data()
    
    entry = {
        'timestamp': timestamp,
        'signature': signature,
        'test_results': {k: 1.0 if v else 0.0 for k, v in test_results.items()},
        'score': signature['amplitude'],
    }
    
    history.append(entry)
    
    # Keep last 100 entries
    if len(history) > 100:
        history = history[-100:]
    
    with open(data_file, 'w') as f:
        json.dump(history, f, indent=2)
    
    return entry

def compute_deltas(current, previous):
    """Compute deltas between current and previous benchmark"""
    if not previous:
        return {}
    
    deltas = {}
    for key in current['signature']:
        if key in previous['signature']:
            deltas[key] = current['signature'][key] - previous['signature'][key]
    
    deltas['score'] = current['score'] - previous['score']
    return deltas

def print_intelligence_spectrum(signature, deltas=None):
    """Print intelligence spectrum visualization"""
    print("\n" + "=" * 70)
    print("Intelligence Spectrum")
    print("=" * 70)
    
    metrics = [
        ('Amplitude', signature['amplitude'], 'Score'),
        ('Coherence', signature['coherence'], 'Alignment'),
        ('Resonance', signature['resonance'], 'Harmonic quality'),
        ('Entropy', signature['entropy'], 'Information diversity'),
        ('Phase Error', signature['phase_error'], 'Deviation'),
    ]
    
    for name, value, desc in metrics:
        bar_length = int(value * 50)
        bar = '█' * bar_length + '░' * (50 - bar_length)
        delta_str = ""
        if deltas and name.lower().replace(' ', '_') in deltas:
            delta = deltas[name.lower().replace(' ', '_')]
            delta_str = f" ({delta:+.3f})" if delta != 0 else ""
        print(f"  {name:<15} [{bar}] {value:.3f}{delta_str}")
        print(f"    {desc}")
    
    print("=" * 70)

def print_harmonic_signature(signature):
    """Print harmonic signature in mathematical notation"""
    print("\nHarmonic Signature:")
    print(f"  H(θ) = {signature['amplitude']:.3f} · e^(i·{signature['phase_error']:.3f}π)")
    print(f"  Coherence: {signature['coherence']:.3f}")
    print(f"  Resonance: {signature['resonance']:.3f}")
    print(f"  Entropy: {signature['entropy']:.3f} bits")

def run_zib():
    """Run Zeta Intelligence Benchmark"""
    print("=" * 70)
    print("Zeta Intelligence Benchmark (ZIB)")
    print("=" * 70)
    print()
    
    # Load ZIB definitions from opic
    defs, voices = load_zib_definitions()
    if voices:
        print("✓ Loaded ZIB definitions from zib.ops")
        print(f"  Voices: {', '.join(list(voices.keys())[:5])}...")
        print()
    
    timestamp = datetime.now().isoformat()
    
    # Run intelligence tests
    print("Running intelligence tests...")
    test_results, test_output = run_intelligence_tests()
    
    if not test_results:
        print("⚠ No test results obtained")
        return
    
    print(f"✓ Completed {len(test_results)} tests")
    print()
    
    # Compute harmonic signature
    signature = compute_harmonic_signature(test_results)
    
    # Load historical data
    history = load_historical_data()
    previous = history[-1] if history else None
    
    # Compute deltas
    deltas = None
    if previous:
        deltas = compute_deltas({'signature': signature, 'score': signature['amplitude']}, previous)
    
    # Save benchmark
    entry = save_benchmark(signature, test_results, timestamp)
    
    # Print results
    print_intelligence_spectrum(signature, deltas)
    print_harmonic_signature(signature)
    
    # Print temporal analysis
    if len(history) > 1:
        print("\n" + "=" * 70)
        print("Temporal Analysis")
        print("=" * 70)
        
        scores = [e['score'] for e in history[-10:]]  # Last 10 runs
        if len(scores) > 1:
            trend = "↑" if scores[-1] > scores[0] else "↓" if scores[-1] < scores[0] else "→"
            print(f"  Trend: {trend} (last {len(scores)} runs)")
            print(f"  Current: {scores[-1]:.3f}")
            print(f"  Average: {sum(scores)/len(scores):.3f}")
            print(f"  Peak: {max(scores):.3f}")
        
        if deltas:
            print("\n  Deltas from previous run:")
            for key, delta in deltas.items():
                if abs(delta) > 0.001:  # Only show significant changes
                    print(f"    {key}: {delta:+.3f}")
    
    print("\n" + "=" * 70)
    print("Benchmark complete")
    print("=" * 70)

if __name__ == "__main__":
    run_zib()

