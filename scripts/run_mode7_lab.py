#!/usr/bin/env python3
"""
Mode 7 Lab Runner
Execute the self-steering lab with Mode 7 perspective layer
"""

import json
import time
from pathlib import Path
from typing import Dict, List

def simulate_router_decision(budget: Dict, health: Dict, last_metrics: Dict) -> Dict:
    """Simulate router decision (Thompson Sampling)"""
    # Simplified: choose config based on exploration rate
    exploration_rate = 0.3  # Start at 30%
    
    if last_metrics.get("parity_accuracy", 0) >= 0.9:
        exploration_rate = 0.1  # Decay to 10%
    
    import random
    if random.random() < exploration_rate:
        # Explore
        config = random.choice(["baseline", "primorial", "random", "linearized"])
        features = random.choice(["v1", "v2"])
        decoder = random.choice(["lasso", "mlp"])
        primorial_val = random.choice([210, 2310, 30030])
        eta = random.choice([0, 0.02, 0.05])
    else:
        # Exploit (simplified: prefer primorial)
        config = "primorial"
        features = "v2"
        decoder = "lasso"
        primorial_val = 2310
        eta = 0.02
    
    return {
        "config": config,
        "features": features,
        "decoder": decoder,
        "primorial": primorial_val,
        "eta": eta,
        "exploration_rate": exploration_rate
    }

def check_health_guards(divL2: float, parseval: float) -> Dict:
    """Check health guards"""
    divL2_ok = divL2 <= 1e-10
    parseval_ok = parseval <= 1e-12
    
    health_ok = divL2_ok and parseval_ok
    
    return {
        "divL2": divL2,
        "divL2_ok": divL2_ok,
        "parseval": parseval,
        "parseval_ok": parseval_ok,
        "health_ok": health_ok
    }

def detect_fusion_moment(significant_shells: bool, delta_mi: float, decode_improved: bool) -> bool:
    """Detect fusion moment: three layers align"""
    return significant_shells and delta_mi > 0 and decode_improved

def run_mode7_lab(budget: Dict, seeds: List[int], n_runs: int = 10) -> Dict:
    """Run Mode 7 lab"""
    print("=" * 60)
    print("Mode 7 Lab: Self-Steering with Perspective Layer")
    print("=" * 60)
    
    results = []
    fusion_moments = []
    
    # Initialize
    health = {"divL2": 1e-11, "parseval": 1e-13}  # Good health
    last_metrics = {"parity_accuracy": 0.0, "delta_mi": 0.0}
    
    for run in range(n_runs):
        print(f"\n--- Run {run+1}/{n_runs} ---")
        
        # Router decision
        router_decision = simulate_router_decision(budget, health, last_metrics)
        print(f"Router: {router_decision['config']} | {router_decision['features']} | "
              f"p#{router_decision['primorial']} | η={router_decision['eta']}")
        print(f"  Exploration: {router_decision['exploration_rate']:.0%}")
        
        # Health guards
        health_check = check_health_guards(health["divL2"], health["parseval"])
        if not health_check["health_ok"]:
            print("  ⚠ Circuit breaker: routing to baseline")
            router_decision["config"] = "baseline"
        
        # Simulate run (simplified)
        import random
        parity_accuracy = random.uniform(0.5, 0.95) if router_decision["config"] == "primorial" else random.uniform(0.4, 0.6)
        delta_mi = random.uniform(-0.1, 0.3) if router_decision["config"] == "primorial" else random.uniform(-0.2, 0.1)
        significant_shells = parity_accuracy > 0.7
        decode_improved = parity_accuracy > 0.6
        
        # Update metrics
        last_metrics = {
            "parity_accuracy": parity_accuracy,
            "delta_mi": delta_mi
        }
        
        # Fusion moment detection
        fusion = detect_fusion_moment(significant_shells, delta_mi, decode_improved)
        if fusion:
            print(f"  ✨ FUSION MOMENT detected!")
            fusion_moments.append({
                "run": run + 1,
                "config": router_decision["config"],
                "parity_accuracy": parity_accuracy,
                "delta_mi": delta_mi
            })
        
        # Parallax layers
        print(f"  Foreground (health): divL2={health['divL2']:.2e}, Parseval={health['parseval']:.2e}")
        print(f"  Midground (state): {router_decision['config']}, ΔMI={delta_mi:.4f}")
        print(f"  Background (aggregates): parity={parity_accuracy:.2%}")
        
        results.append({
            "run": run + 1,
            "router_decision": router_decision,
            "health": health_check,
            "metrics": last_metrics,
            "fusion": fusion
        })
        
        # Slight health drift (simulated)
        health["divL2"] *= random.uniform(0.9, 1.1)
        health["parseval"] *= random.uniform(0.9, 1.1)
    
    print(f"\n{'='*60}")
    print(f"Lab Complete: {n_runs} runs, {len(fusion_moments)} fusion moments")
    print(f"{'='*60}")
    
    return {
        "runs": results,
        "fusion_moments": fusion_moments,
        "summary": {
            "total_runs": n_runs,
            "fusion_count": len(fusion_moments),
            "avg_parity": sum(r["metrics"]["parity_accuracy"] for r in results) / len(results),
            "avg_delta_mi": sum(r["metrics"]["delta_mi"] for r in results) / len(results)
        }
    }

def main():
    budget = {"steps": 100, "walltime": 3600}
    seeds = [42, 123, 456, 789, 1000]
    
    print("\nStarting Mode 7 Lab...")
    print(f"Budget: {budget['steps']} steps, {budget['walltime']}s walltime")
    print(f"Seeds: {seeds}")
    
    results = run_mode7_lab(budget, seeds, n_runs=10)
    
    # Save results
    output_path = Path('results/mode7_lab_run.json')
    output_path.parent.mkdir(exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n✓ Results saved to {output_path}")
    
    # Print summary
    print(f"\nSummary:")
    print(f"  Total runs: {results['summary']['total_runs']}")
    print(f"  Fusion moments: {results['summary']['fusion_count']}")
    print(f"  Avg parity accuracy: {results['summary']['avg_parity']:.2%}")
    print(f"  Avg ΔMI: {results['summary']['avg_delta_mi']:.4f}")
    
    if results['fusion_moments']:
        print(f"\n✨ Fusion Moments:")
        for fm in results['fusion_moments']:
            print(f"  Run {fm['run']}: {fm['config']}, parity={fm['parity_accuracy']:.2%}, ΔMI={fm['delta_mi']:.4f}")

if __name__ == "__main__":
    main()

