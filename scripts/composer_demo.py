#!/usr/bin/env python3
"""
Composer Planning & Generation Demo
Demonstrates: enhanced zero interpretation + composer planning with zeros.on.critical
"""

from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent))

from opic_executor import OpicExecutor

def demo_enhanced_zero_interpretation():
    """Test enhanced zero interpretation"""
    print("=" * 60)
    print("Enhanced Zero Interpretation")
    print("=" * 60)
    
    executor = OpicExecutor(Path(__file__).parent.parent)
    
    # Simulate zero movements
    movements = {
        "movements": [
            {"movement": 0.7, "magnitude": 0.7, "new_zero": False},
            {"movement": 0.3, "magnitude": 0.3, "new_zero": False}
        ],
        "max_movement": 0.7,
        "total_movement": 1.0
    }
    
    question = "What does the zeta field represent?"
    
    result = executor._call_primitive("interpret_movement", {
        "movements": movements,
        "question": question
    })
    
    print(f"\nQuestion: {question}")
    print(f"Zero movements: {movements['max_movement']:.3f}")
    print(f"Interpretation: {result}")
    print()

def demo_ion_extraction():
    """Test ion extraction from intent"""
    print("=" * 60)
    print("Ion Extraction")
    print("=" * 60)
    
    executor = OpicExecutor(Path(__file__).parent.parent)
    
    intent = "zeta field represents coherence potential"
    
    result = executor._call_primitive("extract_ions", {
        "intent": intent
    })
    
    print(f"\nIntent: {intent}")
    print(f"\nExtracted {len(result)} ions:")
    for ion in result:
        print(f"  - {ion.get('word')}: q={ion.get('q')}, type={ion.get('type')}, phi_k={ion.get('phi_k'):.3f}")
    print()

def demo_composer_planning():
    """Test composer planning with zeros.on.critical"""
    print("=" * 60)
    print("Composer Planning with Zeros.on.Critical")
    print("=" * 60)
    
    executor = OpicExecutor(Path(__file__).parent.parent)
    
    intent = "zeta field represents coherence potential"
    
    # Extract ions
    ions = executor._call_primitive("extract_ions", {"intent": intent})
    
    # Composer plan
    plan_result = executor._call_primitive("composer.plan", {"ions": ions})
    
    print(f"\nIntent: {intent}")
    print(f"\nPlan:")
    print(f"  - Ions: {plan_result.get('ion_count', 0)}")
    print(f"  - Zeros found: {len(plan_result.get('zeros', []))}")
    print(f"  - Coherence: {plan_result.get('coherence', 0.0):.3f}")
    print(f"  - Witnesses: {len(plan_result.get('witnesses', []))}")
    
    print(f"\nPlan steps:")
    for step in plan_result.get('plan', [])[:5]:  # Show first 5
        ion = step.get('ion', {})
        print(f"  {step.get('index')}: {ion.get('word')} ({step.get('action')}) - coherence: {step.get('coherence'):.3f}")
    print()

def demo_coherence_maximization():
    """Test coherence maximization"""
    print("=" * 60)
    print("Coherence Maximization")
    print("=" * 60)
    
    executor = OpicExecutor(Path(__file__).parent.parent)
    
    intent = "zeta field represents coherence potential"
    
    # Get plan
    ions = executor._call_primitive("extract_ions", {"intent": intent})
    plan_result = executor._call_primitive("composer.plan", {"ions": ions})
    
    # Maximize coherence
    optimal_result = executor._call_primitive("composer.coherence_maximization", {
        "plan": plan_result.get("plan", [])
    })
    
    print(f"\nOriginal coherence: {plan_result.get('coherence', 0.0):.3f}")
    print(f"Optimal coherence: {optimal_result.get('coherence', 0.0):.3f}")
    print(f"Average coherence: {optimal_result.get('avg_coherence', 0.0):.3f}")
    print(f"Steps optimized: {optimal_result.get('steps', 0)}")
    print()

def demo_generation_pipeline():
    """Test full generation pipeline"""
    print("=" * 60)
    print("Full Generation Pipeline")
    print("=" * 60)
    
    executor = OpicExecutor(Path(__file__).parent.parent)
    
    intent = "zeta field represents coherence potential"
    
    result = executor._call_primitive("generate.coherent", {
        "intent": intent
    })
    
    print(f"\nIntent: {intent}")
    print(f"\nGenerated output: {result.get('output', '')}")
    print(f"Coherence: {result.get('coherence', 0.0):.3f}")
    print(f"Is coherent: {result.get('is_coherent', False)}")
    print(f"Zeros used: {len(result.get('zeros', []))}")
    print(f"Witnesses: {len(result.get('witnesses', []))}")
    print()

def main():
    print("\n" + "=" * 60)
    print("Composer Planning & Generation Demo")
    print("=" * 60)
    
    demo_enhanced_zero_interpretation()
    demo_ion_extraction()
    demo_composer_planning()
    demo_coherence_maximization()
    demo_generation_pipeline()
    
    print("=" * 60)
    print("✓ Demo complete")
    print("=" * 60)

if __name__ == "__main__":
    main()

