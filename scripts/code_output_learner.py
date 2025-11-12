#!/usr/bin/env python3
"""
Code-Output Learning System — Learn from coupling code with its output
Self-improving system: code → output → evaluation → field update → better code
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Optional
from collections import defaultdict
import time

sys.path.insert(0, str(Path(__file__).parent))
from opic_executor import OpicExecutor

class CodeOutputLearner:
    """
    Learn from coupling program output with the code that generated it.
    Creates a feedback loop: code → output → evaluation → field update → better code
    """
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.opic = OpicExecutor(project_root)
        self.learning_pairs = []  # Store code-output pairs
        self.successful_patterns = defaultdict(list)  # Patterns that led to success
        self.field_updates = {}  # Field updates from learning
        
    def record_code_output_pair(self, code_trace: Dict, output: int, 
                               correct_answer: int, evaluation: Dict) -> Dict:
        """
        Record a code-output pair for learning.
        
        Args:
            code_trace: Execution trace (field state, zeros, generation process)
            output: Generated output
            correct_answer: Correct answer
            evaluation: Quality evaluation
        
        Returns:
            code_output_pair dict
        """
        correctness = 1.0 if output == correct_answer else 0.0
        
        pair = {
            "code_trace": code_trace,
            "output": output,
            "correct_answer": correct_answer,
            "correctness": correctness,
            "evaluation": evaluation,
            "timestamp": time.time()
        }
        
        self.learning_pairs.append(pair)
        
        # If successful, extract patterns
        if correctness > 0.5:
            self._extract_successful_patterns(pair)
        
        return pair
    
    def _extract_successful_patterns(self, pair: Dict):
        """Extract patterns from successful code-output pairs"""
        code_trace = pair["code_trace"]
        field_state = code_trace.get("field_state", {})
        question_zeros = code_trace.get("question_zeros", [])
        doc_zeros = code_trace.get("doc_zeros", [])
        
        # Pattern 1: Successful field states
        phi_k = field_state.get("phi_k", 0.0)
        D = field_state.get("dimensionality", 1)
        
        # Pattern 2: Successful zero patterns
        if question_zeros and doc_zeros:
            zero_pattern = {
                "question_zeros": question_zeros,
                "doc_zeros": doc_zeros,
                "zero_count": len(question_zeros) + len(doc_zeros)
            }
            self.successful_patterns["zero_patterns"].append(zero_pattern)
        
        # Pattern 3: Successful dimensional scales
        self.successful_patterns["dimensional_scales"].append({
            "D": D,
            "phi_k": phi_k
        })
        
        # Pattern 4: Successful spectrum sizes
        question_spectrum = code_trace.get("question_spectrum", [])
        doc_spectrum = code_trace.get("doc_spectrum", [])
        self.successful_patterns["spectrum_sizes"].append({
            "question_spectrum_size": len(question_spectrum),
            "doc_spectrum_size": len(doc_spectrum)
        })
    
    def analyze_patterns(self) -> Dict:
        """
        Analyze patterns: what code patterns lead to good outputs?
        Returns field correlations and successful patterns.
        """
        if not self.learning_pairs:
            return {}
        
        # Separate successful and failed pairs
        successful = [p for p in self.learning_pairs if p["correctness"] > 0.5]
        failed = [p for p in self.learning_pairs if p["correctness"] <= 0.5]
        
        # Compute field correlations
        correlations = {
            "success_rate": len(successful) / len(self.learning_pairs) if self.learning_pairs else 0.0,
            "successful_count": len(successful),
            "failed_count": len(failed)
        }
        
        # Analyze successful patterns
        if successful:
            # Average successful field properties
            avg_phi_k = sum(
                p["code_trace"].get("field_state", {}).get("phi_k", 0.0) 
                for p in successful
            ) / len(successful)
            
            avg_D = sum(
                p["code_trace"].get("field_state", {}).get("dimensionality", 1)
                for p in successful
            ) / len(successful)
            
            correlations["successful_avg_phi_k"] = avg_phi_k
            correlations["successful_avg_D"] = avg_D
        
        return {
            "correlations": correlations,
            "successful_patterns": dict(self.successful_patterns),
            "total_pairs": len(self.learning_pairs)
        }
    
    def update_field_from_learning(self):
        """
        Update field based on successful patterns.
        This creates the learning feedback loop.
        """
        patterns = self.analyze_patterns()
        
        if not patterns.get("successful_patterns"):
            return
        
        # Extract most common successful patterns
        zero_patterns = patterns["successful_patterns"].get("zero_patterns", [])
        dimensional_scales = patterns["successful_patterns"].get("dimensional_scales", [])
        
        # Update field to favor successful patterns
        # This could update:
        # - Zero solver parameters
        # - Dimensional scale calculations
        # - Field coherence thresholds
        
        # For now, store updates for future use
        self.field_updates = {
            "preferred_zero_patterns": zero_patterns[:10] if zero_patterns else [],
            "preferred_dimensional_scales": dimensional_scales[:10] if dimensional_scales else [],
            "success_rate": patterns["correlations"]["success_rate"]
        }
        
        return self.field_updates
    
    def save_learning_data(self, output_file: Path):
        """Save learning data for future use"""
        data = {
            "learning_pairs": self.learning_pairs[-1000:],  # Keep last 1000 pairs
            "successful_patterns": dict(self.successful_patterns),
            "field_updates": self.field_updates,
            "analysis": self.analyze_patterns()
        }
        
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"✓ Saved learning data to {output_file}")
    
    def load_learning_data(self, input_file: Path):
        """Load learning data"""
        if not input_file.exists():
            return
        
        with open(input_file) as f:
            data = json.load(f)
        
        self.learning_pairs = data.get("learning_pairs", [])
        self.successful_patterns = defaultdict(list, data.get("successful_patterns", {}))
        self.field_updates = data.get("field_updates", {})
        
        print(f"✓ Loaded {len(self.learning_pairs)} learning pairs from {input_file}")

def main():
    """Test code-output learning system"""
    project_root = Path(__file__).parent.parent
    learner = CodeOutputLearner(project_root)
    
    print("=" * 60)
    print("Code-Output Learning System")
    print("=" * 60)
    
    # Example: record a code-output pair
    code_trace = {
        "question": "What is 2+2?",
        "question_spectrum": [1.0, 2.0, 3.0],
        "question_zeros": [0.5, 1.5],
        "doc_spectrum": [1.0, 2.0, 3.0, 4.0],
        "doc_zeros": [0.5, 1.5, 2.5],
        "field_state": {
            "phi_k": 10.0,
            "dimensionality": 2
        }
    }
    
    pair = learner.record_code_output_pair(
        code_trace=code_trace,
        output=0,  # Selected first choice
        correct_answer=0,  # Correct!
        evaluation={"coherence": 0.8, "zero_alignment": 0.9}
    )
    
    print(f"✓ Recorded code-output pair (correctness: {pair['correctness']})")
    
    # Analyze patterns
    patterns = learner.analyze_patterns()
    print(f"\nPattern Analysis:")
    print(f"  Success rate: {patterns['correlations']['success_rate']:.1%}")
    print(f"  Successful pairs: {patterns['correlations']['successful_count']}")
    
    # Update field from learning
    updates = learner.update_field_from_learning()
    print(f"\nField Updates:")
    print(f"  Preferred zero patterns: {len(updates.get('preferred_zero_patterns', []))}")
    print(f"  Preferred dimensional scales: {len(updates.get('preferred_dimensional_scales', []))}")
    
    # Save learning data
    output_file = project_root / "data" / "code_output_learning.json"
    output_file.parent.mkdir(exist_ok=True)
    learner.save_learning_data(output_file)
    
    print("\n✓ Code-output learning system ready")
    print("\nThis system learns from coupling code with its output,")
    print("creating a self-improving feedback loop.")

if __name__ == "__main__":
    main()

