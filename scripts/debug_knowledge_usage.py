#!/usr/bin/env python3
"""
Debug Knowledge Base Usage — See how knowledge is being used in answer selection
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from opic_executor import OpicExecutor

def debug_answer_selection():
    """Debug how knowledge base is used in answer selection"""
    project_root = Path(__file__).parent.parent
    executor = OpicExecutor(project_root)
    
    # Sample MMLU question
    question = "What is the primary function of mitochondria?"
    choices = [
        "Energy production",
        "Protein synthesis", 
        "DNA replication",
        "Waste removal"
    ]
    
    print("=" * 60)
    print("Debugging Knowledge Base Usage")
    print("=" * 60)
    
    print(f"\nQuestion: {question}")
    print(f"Choices: {choices}")
    
    # Check knowledge base
    knowledge_file = project_root / "data" / "bert_knowledge_base.json"
    if knowledge_file.exists():
        with open(knowledge_file) as f:
            knowledge_base = json.load(f)
        
        print(f"\nKnowledge base: {len(knowledge_base)} entries")
        
        # Query knowledge base
        query_field = executor._call_primitive("aperture.chain", {"text": question})
        query_phi_k = query_field.get("aperture", {}).get("discourse", {}).get("phi_k", 0.0)
        
        print(f"Query phi_k: {query_phi_k:.3f}")
        
        # Score knowledge entries
        scored_entries = []
        for entry_hash, entry in knowledge_base.items():
            entry_phi_k = entry.get("phi_k", 0.0)
            coherence = 1.0 - abs(query_phi_k - float(entry_phi_k)) / (abs(query_phi_k) + 1.0)
            coherence = max(0.0, min(1.0, coherence))
            scored_entries.append((entry, coherence, entry_hash))
        
        scored_entries.sort(key=lambda x: x[1], reverse=True)
        
        print(f"\nTop 5 knowledge entries:")
        for i, (entry, coherence, entry_hash) in enumerate(scored_entries[:5], 1):
            text = entry.get("text", "")[:100]
            domain = entry.get("domain", "unknown")
            print(f"  {i}. Coherence: {coherence:.3f}, Domain: {domain}")
            print(f"     Text: {text}...")
        
        # Check if any entries mention mitochondria
        mitochondria_entries = [
            (entry, coherence, entry_hash)
            for entry, coherence, entry_hash in scored_entries
            if "mitochondria" in entry.get("text", "").lower() or "energy" in entry.get("text", "").lower()
        ]
        
        print(f"\nEntries mentioning 'mitochondria' or 'energy': {len(mitochondria_entries)}")
        if mitochondria_entries:
            for i, (entry, coherence, entry_hash) in enumerate(mitochondria_entries[:3], 1):
                print(f"  {i}. Coherence: {coherence:.3f}")
                print(f"     Text: {entry.get('text', '')[:150]}...")
        else:
            print("  ⚠ No entries found mentioning mitochondria or energy!")
            print("  This suggests the knowledge base doesn't have relevant biology content.")
    
    # Test answer selection
    print("\n" + "=" * 60)
    print("Answer Selection Process")
    print("=" * 60)
    
    # Simulate the answer selection
    doc_text = question + " " + " ".join(choices)
    doc_field = executor._call_primitive("aperture.chain", {"text": doc_text})
    question_phi_k = doc_field.get("aperture", {}).get("discourse", {}).get("phi_k", 0.0)
    
    print(f"\nQuestion+choices phi_k: {question_phi_k:.3f}")
    
    choice_scores = []
    for i, choice in enumerate(choices):
        choice_intent = f"{question} {choice}"
        choice_ions = executor._call_primitive("extract_ions", {"intent": choice_intent})
        choice_phi_k = sum(ion.get("phi_k", 0.0) for ion in choice_ions if isinstance(ion, dict))
        
        coherence = 1.0 - abs(choice_phi_k - float(question_phi_k)) / (abs(question_phi_k) + 1.0)
        coherence = max(0.0, min(1.0, coherence))
        
        # Check knowledge boost
        knowledge_boost = 0.0
        if knowledge_file.exists():
            with open(knowledge_file) as f:
                kb = json.load(f)
            top_entries = [e for e, c, h in scored_entries[:3]]
            for kb_entry in top_entries:
                kb_text = kb_entry.get("text", "").lower()
                choice_lower = choice.lower()
                choice_words = choice_lower.split()
                matches = sum(1 for word in choice_words if word in kb_text)
                if matches > 0:
                    knowledge_boost += 0.1 * matches / len(choice_words)
        
        final_coherence = min(1.0, coherence + knowledge_boost)
        choice_scores.append((i, choice, coherence, knowledge_boost, final_coherence))
        
        print(f"\nChoice {i}: {choice}")
        print(f"  Choice phi_k: {choice_phi_k:.3f}")
        print(f"  Base coherence: {coherence:.3f}")
        print(f"  Knowledge boost: {knowledge_boost:.3f}")
        print(f"  Final coherence: {final_coherence:.3f}")
    
    choice_scores.sort(key=lambda x: x[4], reverse=True)
    print(f"\nSelected answer: {choice_scores[0][1]} (index {choice_scores[0][0]})")
    print(f"Correct answer should be: {choices[0]} (Energy production)")

if __name__ == "__main__":
    debug_answer_selection()

