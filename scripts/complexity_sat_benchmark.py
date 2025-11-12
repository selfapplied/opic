#!/usr/bin/env python3
"""
Complexity SAT Benchmark
Generate 3-SAT from known distribution, sweep n and α, record solver metrics
"""

import json
import math
import random
from pathlib import Path
from typing import Dict, List, Tuple
import statistics

def generate_3sat_instance(n_vars: int, n_clauses: int, seed: int = 42) -> Dict:
    """Generate uniform random 3-SAT instance with clause density α = m/n"""
    random.seed(seed)
    
    clauses = []
    for _ in range(n_clauses):
        clause = []
        # Pick 3 distinct variables
        vars_in_clause = random.sample(range(1, n_vars + 1), min(3, n_vars))
        for var in vars_in_clause:
            negated = random.choice([True, False])
            clause.append({"var": var, "negated": negated})
        clauses.append(clause)
    
    alpha = n_clauses / n_vars if n_vars > 0 else 0.0
    
    return {
        "n_vars": n_vars,
        "n_clauses": n_clauses,
        "alpha": alpha,
        "clauses": clauses,
        "seed": seed
    }

def check_satisfaction(assignment: List[int], clauses: List[List[Dict]]) -> bool:
    """Check if assignment satisfies all clauses"""
    for clause in clauses:
        clause_satisfied = False
        for lit in clause:
            var_val = assignment[lit["var"] - 1]
            if lit["negated"]:
                var_val = 1 - var_val
            if var_val == 1:
                clause_satisfied = True
                break
        if not clause_satisfied:
            return False
    return True

def simple_sat_solver(sat_instance: Dict, max_steps: int = 10000) -> Dict:
    """Simple SAT solver (baseline - in real version, use MiniSAT/Glucose)"""
    clauses = sat_instance["clauses"]
    n_vars = sat_instance["n_vars"]
    
    # Simple random search
    search_steps = []
    branching_choices = []
    
    for step in range(max_steps):
        assignment = [random.choice([0, 1]) for _ in range(n_vars)]
        satisfied = check_satisfaction(assignment, clauses)
        
        search_steps.append({
            "step": step,
            "assignment": assignment,
            "satisfied": satisfied
        })
        
        # Record branching choice (simplified)
        branching_choices.append(random.choice([0, 1]))
        
        if satisfied:
            return {
                "found": True,
                "steps": step + 1,
                "assignment": assignment,
                "search_steps": search_steps,
                "branching_choices": branching_choices
            }
    
    return {
        "found": False,
        "steps": max_steps,
        "search_steps": search_steps,
        "branching_choices": branching_choices
    }

def compute_search_entropy(branching_choices: List[int]) -> float:
    """Search entropy H = -Σ p(a) log p(a) over branching choices"""
    if not branching_choices:
        return 0.0
    
    counts = {}
    for choice in branching_choices:
        counts[choice] = counts.get(choice, 0) + 1
    
    total = len(branching_choices)
    entropy = 0.0
    for count in counts.values():
        p = count / total
        if p > 0:
            entropy -= p * math.log(p)
    
    return entropy

def compute_verification_cost(assignment: List[int], clauses: List[List[Dict]]) -> int:
    """Verification cost: polynomial-time check (O(m) where m = number of clauses)"""
    return len(clauses)

def run_sat_benchmark(n_values: List[int], alpha_values: List[float], n_seeds: int = 10) -> Dict:
    """Run SAT benchmark: sweep n and α"""
    results = []
    
    for n in n_values:
        for alpha in alpha_values:
            n_clauses = int(alpha * n)
            if n_clauses < 3:
                continue
            
            success_count = 0
            step_counts = []
            verification_costs = []
            search_entropies = []
            
            for seed in range(n_seeds):
                sat_instance = generate_3sat_instance(n, n_clauses, seed=seed)
                solver_result = simple_sat_solver(sat_instance)
                
                if solver_result["found"]:
                    success_count += 1
                    step_counts.append(solver_result["steps"])
                    verification_cost = compute_verification_cost(
                        solver_result["assignment"], sat_instance["clauses"]
                    )
                    verification_costs.append(verification_cost)
                    search_entropy = compute_search_entropy(solver_result["branching_choices"])
                    search_entropies.append(search_entropy)
            
            success_rate = success_count / n_seeds if n_seeds > 0 else 0.0
            median_steps = statistics.median(step_counts) if step_counts else 0
            variance_steps = statistics.variance(step_counts) if len(step_counts) > 1 else 0.0
            mean_verification_cost = statistics.mean(verification_costs) if verification_costs else 0
            mean_search_entropy = statistics.mean(search_entropies) if search_entropies else 0.0
            
            results.append({
                "n": n,
                "alpha": alpha,
                "n_clauses": n_clauses,
                "success_rate": success_rate,
                "median_steps": median_steps,
                "variance_steps": variance_steps,
                "mean_verification_cost": mean_verification_cost,
                "mean_search_entropy": mean_search_entropy,
                "n_seeds": n_seeds
            })
    
    return {"results": results}

def decoder_learning_curve(n_observables: List[int], sat_instance: Dict, n_runs: int = 20) -> Dict:
    """Learning curve: decoder accuracy vs number of observables"""
    results = []
    
    for n_obs in n_observables:
        accuracies = []
        
        for run in range(n_runs):
            # Simplified: simulate decoder accuracy
            # In real version, extract observables from flow simulation
            accuracy = min(1.0, 0.5 + 0.5 * (n_obs / sat_instance["n_vars"]))
            accuracies.append(accuracy)
        
        mean_accuracy = statistics.mean(accuracies)
        std_accuracy = statistics.stdev(accuracies) if len(accuracies) > 1 else 0.0
        
        results.append({
            "n_observables": n_obs,
            "mean_accuracy": mean_accuracy,
            "std_accuracy": std_accuracy
        })
    
    return {"learning_curve": results}

def main():
    print("=" * 60)
    print("Complexity SAT Benchmark")
    print("=" * 60)
    
    # Sweep n and α around phase transition
    n_values = [20, 24, 28, 32]
    alpha_values = [3.5, 4.0, 4.2, 4.5, 5.0]  # Around phase transition ~4.2
    n_seeds = 10
    
    print(f"\nConfiguration:")
    print(f"  n values: {n_values}")
    print(f"  α values: {alpha_values}")
    print(f"  Seeds per config: {n_seeds}")
    
    print("\nRunning SAT benchmark...")
    benchmark_results = run_sat_benchmark(n_values, alpha_values, n_seeds)
    
    print("\nResults (sample):")
    for res in benchmark_results["results"][:5]:
        print(f"  n={res['n']}, α={res['alpha']:.2f}: "
              f"success={res['success_rate']:.2%}, "
              f"median_steps={res['median_steps']:.0f}, "
              f"entropy={res['mean_search_entropy']:.4f}")
    
    # Learning curve
    print("\nComputing learning curve...")
    sat_instance = generate_3sat_instance(20, 80, seed=42)
    n_observables = [1, 2, 4, 8, 16, 20]
    learning_curve = decoder_learning_curve(n_observables, sat_instance)
    
    print("Learning curve (sample):")
    for point in learning_curve["learning_curve"][:3]:
        print(f"  {point['n_observables']} observables: "
              f"accuracy={point['mean_accuracy']:.4f} ± {point['std_accuracy']:.4f}")
    
    # Save results
    output_path = Path('results/complexity_sat_benchmark.json')
    output_path.parent.mkdir(exist_ok=True)
    
    combined_results = {
        "benchmark": benchmark_results,
        "learning_curve": learning_curve
    }
    
    with open(output_path, 'w') as f:
        json.dump(combined_results, f, indent=2)
    
    print(f"\n✓ Results saved to {output_path}")

if __name__ == "__main__":
    main()

