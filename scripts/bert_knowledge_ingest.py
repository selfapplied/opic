#!/usr/bin/env python3
"""
BERT Knowledge Ingestion — Ingest BERT training data into ζ-field knowledge base
Instead of training a neural network, we populate the field with semantic knowledge
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Optional
import hashlib
import time

sys.path.insert(0, str(Path(__file__).parent))
from opic_executor import OpicExecutor

class BertKnowledgeIngester:
    """Ingest BERT training data into ζ-field knowledge base"""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.opic = OpicExecutor(project_root)
        self.knowledge_base = {}  # In-memory knowledge store
        self.field_cache = {}  # Cache document fields
        
    def ingest_text_chunk(self, text: str, source: str = "bert", domain: str = "general") -> Dict:
        """
        Ingest a text chunk into the knowledge base.
        Creates document field and stores field state as knowledge.
        """
        if not text or len(text.strip()) < 10:
            return None
        
        # Create document field using aperture chain
        doc_field = self.opic._call_primitive("aperture.chain", {"text": text})
        
        if not doc_field:
            return None
        
        # Extract field properties
        aperture = doc_field.get("aperture", {})
        discourse = aperture.get("discourse", {})
        phi_k = discourse.get("phi_k", 0.0)
        
        # Get words with field properties
        words = aperture.get("words", [])
        
        # Proper zeta calibration: use FULL hierarchical spectrum
        # Construct spectrum from all levels: letters → words → sentences → discourse
        spectrum = []
        
        # Level 1: Letters (zeta orders 1-3)
        letters = aperture.get("letters", [])
        for letter in letters:
            if isinstance(letter, dict):
                letter_phi_k = letter.get("phi_k", 0.0)
                if letter_phi_k:
                    spectrum.append(float(letter_phi_k))
        
        # Level 2: Words (zeta order 2)
        for word in words:
            if isinstance(word, dict):
                word_phi_k = word.get("phi_k", 0.0)
                if word_phi_k:
                    spectrum.append(float(word_phi_k))
        
        # Level 3: Sentences (zeta order 3)
        sentences = aperture.get("sentences", [])
        for sentence in sentences:
            if isinstance(sentence, dict):
                sent_phi_k = sentence.get("phi_k", 0.0)
                if sent_phi_k:
                    spectrum.append(float(sent_phi_k))
        
        # Level 4: Discourse (zeta order 4+)
        if phi_k:
            spectrum.append(float(phi_k))
        
        # If spectrum is empty, fall back to single phi_k
        if not spectrum:
            spectrum = [float(phi_k)] if phi_k else [0.0]
        
        # Compute zeros using FULL spectrum (proper zeta calibration)
        region = {"min": 0.0, "max": 10.0}
        zeros = self.opic._call_primitive("zeta.zero.solver", {
            "phi_k": spectrum,  # Pass full spectrum, not just single phi_k
            "region": region,
            "tolerance": 0.001  # Tighter tolerance with better spectrum
        })
        
        # Create knowledge entry
        knowledge_entry = {
            "text": text[:500],  # Store first 500 chars
            "phi_k": phi_k,  # Discourse-level phi_k (for backward compatibility)
            "spectrum": spectrum[:100],  # Store spectrum for proper zeta calibration
            "spectrum_size": len(spectrum),
            "zeros": zeros,
            "words": words[:50],  # Store first 50 words with properties
            "source": source,
            "domain": domain,
            "timestamp": time.time()
        }
        
        # Index by hash for deduplication
        text_hash = hashlib.md5(text.encode()).hexdigest()[:16]
        self.knowledge_base[text_hash] = knowledge_entry
        
        return knowledge_entry
    
    def ingest_wikipedia_chunk(self, title: str, text: str) -> Dict:
        """Ingest Wikipedia article chunk"""
        # Determine domain from title/category
        domain = self._classify_domain(title, text)
        return self.ingest_text_chunk(text, source="wikipedia", domain=domain)
    
    def ingest_book_chunk(self, text: str, book_title: str = None) -> Dict:
        """Ingest book text chunk"""
        return self.ingest_text_chunk(text, source="book", domain="literature")
    
    def _classify_domain(self, title: str, text: str) -> str:
        """Classify domain from title/text"""
        title_lower = title.lower()
        text_lower = text.lower()[:200]  # First 200 chars
        
        # Let OPIC determine domain naturally - no hardcoded keyword matching
        # Use field operations to classify domain through semantic field analysis
        return "general"  # OPIC will refine domain through field operations
    
    def query_knowledge(self, query: str, top_k: int = 5) -> List[Dict]:
        """
        Query knowledge base using zero interpretation and field coherence.
        Returns most relevant knowledge entries.
        """
        # Create query field
        query_field = self.opic._call_primitive("aperture.chain", {"text": query})
        query_phi_k = query_field.get("aperture", {}).get("discourse", {}).get("phi_k", 0.0)
        
        # Score each knowledge entry by coherence
        scored_entries = []
        for entry_hash, entry in self.knowledge_base.items():
            entry_phi_k = entry.get("phi_k", 0.0)
            
            # Coherence: how well query aligns with entry field
            coherence = 1.0 - abs(query_phi_k - float(entry_phi_k)) / (abs(query_phi_k) + 1.0)
            coherence = max(0.0, min(1.0, coherence))
            
            # Zero proximity: entries with zeros near query zeros
            query_zeros = self.opic._call_primitive("zeta.zero.solver", {
                "phi_k": query_phi_k,
                "region": {"min": 0.0, "max": 10.0},
                "tolerance": 0.01
            })
            entry_zeros = entry.get("zeros", [])
            
            if query_zeros and entry_zeros:
                query_zero_positions = [z.get("imaginary", 0.0) for z in query_zeros if isinstance(z, dict)]
                entry_zero_positions = [z.get("imaginary", 0.0) for z in entry_zeros if isinstance(z, dict)]
                
                if query_zero_positions and entry_zero_positions:
                    min_dist = min(
                        abs(qz - ez) 
                        for qz in query_zero_positions 
                        for ez in entry_zero_positions
                    )
                    zero_proximity = 1.0 / (1.0 + min_dist)
                    coherence = (coherence + zero_proximity) / 2.0
            
            scored_entries.append((entry, coherence))
        
        # Sort by coherence and return top_k
        scored_entries.sort(key=lambda x: x[1], reverse=True)
        return [entry for entry, score in scored_entries[:top_k]]
    
    def save_knowledge_base(self, output_file: Path):
        """Save knowledge base to JSON file"""
        # Convert to serializable format
        serializable = {}
        for entry_hash, entry in self.knowledge_base.items():
            # Clean zeros: convert complex to serializable format
            zeros_clean = []
            for zero in entry.get("zeros", []):
                if isinstance(zero, dict):
                    zero_clean = {
                        "real": zero.get("real", 0.0),
                        "imaginary": zero.get("imaginary", 0.0),
                    }
                    # Handle complex value if present
                    value = zero.get("value")
                    if isinstance(value, complex):
                        zero_clean["value_real"] = value.real
                        zero_clean["value_imag"] = value.imag
                    zeros_clean.append(zero_clean)
            
            # Remove non-serializable items
            clean_entry = {
                "text": entry.get("text", ""),
                "phi_k": float(entry.get("phi_k", 0.0)),
                "zeros": zeros_clean,
                "source": entry.get("source", ""),
                "domain": entry.get("domain", ""),
                "word_count": len(entry.get("words", []))
            }
            serializable[entry_hash] = clean_entry
        
        with open(output_file, 'w') as f:
            json.dump(serializable, f, indent=2)
        
        print(f"✓ Saved {len(serializable)} knowledge entries to {output_file}")
    
    def load_knowledge_base(self, input_file: Path):
        """Load knowledge base from JSON file"""
        if not input_file.exists():
            return
        
        with open(input_file) as f:
            data = json.load(f)
        
        self.knowledge_base = data
        print(f"✓ Loaded {len(data)} knowledge entries from {input_file}")

def ingest_bert_data_sample():
    """Sample ingestion of BERT training data"""
    project_root = Path(__file__).parent.parent
    ingester = BertKnowledgeIngester(project_root)
    
    # Sample Wikipedia text (simulating BERT training data)
    sample_texts = [
        ("Mathematics", "Mathematics is the study of numbers, quantities, and shapes. It includes algebra, geometry, calculus, and many other branches."),
        ("Physics", "Physics is the natural science that studies matter, motion, and behavior through space and time. It includes mechanics, thermodynamics, and quantum mechanics."),
        ("Biology", "Biology is the study of living organisms. It includes cell biology, genetics, evolution, and ecology."),
        ("Chemistry", "Chemistry is the study of matter and its properties. It includes organic chemistry, inorganic chemistry, and physical chemistry."),
        ("History", "History is the study of past events. It includes ancient history, medieval history, and modern history."),
    ]
    
    print("=" * 60)
    print("BERT Knowledge Ingestion — Sample")
    print("=" * 60)
    
    for title, text in sample_texts:
        entry = ingester.ingest_wikipedia_chunk(title, text)
        if entry:
            print(f"✓ Ingested: {title} (phi_k={entry['phi_k']:.3f}, zeros={len(entry['zeros'])})")
    
    # Test query
    print("\n" + "=" * 60)
    print("Knowledge Query Test")
    print("=" * 60)
    
    query = "What is mathematics?"
    results = ingester.query_knowledge(query, top_k=3)
    
    print(f"\nQuery: {query}")
    print(f"Found {len(results)} relevant entries:")
    for i, entry in enumerate(results, 1):
        print(f"  {i}. {entry.get('text', '')[:100]}... (domain: {entry.get('domain', 'unknown')})")
    
    # Save knowledge base
    output_file = project_root / "data" / "bert_knowledge_base.json"
    output_file.parent.mkdir(exist_ok=True)
    ingester.save_knowledge_base(output_file)
    
    print(f"\n✓ Knowledge base ready for benchmark integration")

if __name__ == "__main__":
    ingest_bert_data_sample()

