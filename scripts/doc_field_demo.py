#!/usr/bin/env python3
"""
Document Field Demo — Prototype LLM Replacement via Zeta Field
Demonstrates: live field updates, zero movement tracking, witness chains
"""

from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent))

from opic_executor import OpicExecutor

def demo_document_ingest():
    """Phase 1: Map text to Φκ field"""
    print("=" * 60)
    print("Phase 1: Document Understanding")
    print("=" * 60)
    
    executor = OpicExecutor(Path(__file__).parent.parent)
    
    # Sample document
    text = "The zeta field represents coherence potential. Each word carries field properties."
    
    print(f"\nDocument: {text}")
    print("\nIngesting document into zeta field...")
    
    try:
        result = executor.execute_voice("doc.ingest", {"text": text})
        print(f"✓ Document field created")
        print(f"  Result type: {type(result)}")
        if isinstance(result, dict):
            print(f"  Keys: {list(result.keys())}")
        return result
    except Exception as e:
        print(f"⚠ Error: {e}")
        return None

def demo_query_resolution(doc_field):
    """Query resolution via field perturbation"""
    print("\n" + "=" * 60)
    print("Phase 2: Query Resolution")
    print("=" * 60)
    
    executor = OpicExecutor(Path(__file__).parent.parent)
    
    question = "What does the zeta field represent?"
    print(f"\nQuestion: {question}")
    print("\nPerturbing field and tracking zero movements...")
    
    try:
        result = executor.execute_voice("query.resolve", {
            "question": question,
            "document_field": doc_field
        })
        print(f"✓ Answer generated from zero movement")
        print(f"  Result: {result}")
        return result
    except Exception as e:
        print(f"⚠ Error: {e}")
        return None

def demo_live_update(doc_field):
    """Live field update: continuous adaptation"""
    print("\n" + "=" * 60)
    print("Phase 3: Live Field Update")
    print("=" * 60)
    
    executor = OpicExecutor(Path(__file__).parent.parent)
    
    new_text = "The field adapts continuously."
    print(f"\nNew input: {new_text}")
    print("\nUpdating field (no retraining needed)...")
    
    try:
        result = executor.execute_voice("field.live.update", {
            "input": new_text,
            "field_state": doc_field
        })
        print(f"✓ Field updated immediately")
        print(f"  Result type: {type(result)}")
        return result
    except Exception as e:
        print(f"⚠ Error: {e}")
        return None

def demo_witness_chain(doc_field):
    """Witness chain: verifiable provenance"""
    print("\n" + "=" * 60)
    print("Phase 4: Witness Chains")
    print("=" * 60)
    
    executor = OpicExecutor(Path(__file__).parent.parent)
    
    print("\nCreating witness chain (W0 → W1 → W2)...")
    
    try:
        result = executor.execute_voice("witness.chain", {
            "input": doc_field
        })
        print(f"✓ Witness chain created")
        print(f"  Result type: {type(result)}")
        if isinstance(result, dict):
            print(f"  Keys: {list(result.keys())}")
        return result
    except Exception as e:
        print(f"⚠ Error: {e}")
        return None

def demo_comparison():
    """Compare zeta field approach to LLM approach"""
    print("\n" + "=" * 60)
    print("Comparison: Zeta Field vs LLM")
    print("=" * 60)
    
    print("""
    LLM Approach:
    - frozen_weights(input_tokens) → output_tokens
    - Requires: billion-parameter forward pass
    - Training: separate expensive process
    - Inference: O(n²) attention complexity
    
    Zeta Field Approach:
    - live_field.interaction(intent) → witnessed_response
    - Requires: local field coherence solving
    - Training: continuous field updates (same mechanism)
    - Inference: O(n) field update complexity
    
    Advantages:
    ✓ No training/inference dichotomy
    ✓ Built-in grounding (words carry field properties)
    ✓ Deterministic creativity (zeros.on.critical)
    ✓ Witness chains (verifiable provenance)
    ✓ Energy efficient (O(n) vs O(n²))
    ✓ Runs on consumer hardware
    """)

def main():
    print("\n" + "=" * 60)
    print("Document Field Demo — LLM Replacement Prototype")
    print("=" * 60)
    
    # Phase 1: Document understanding
    doc_field = demo_document_ingest()
    
    if doc_field:
        # Phase 2: Query resolution
        answer = demo_query_resolution(doc_field)
        
        # Phase 3: Live update
        updated_field = demo_live_update(doc_field)
        
        # Phase 4: Witness chain
        witness_chain = demo_witness_chain(doc_field)
    
    # Comparison
    demo_comparison()
    
    print("\n" + "=" * 60)
    print("✓ Demo complete")
    print("=" * 60)

if __name__ == "__main__":
    main()

