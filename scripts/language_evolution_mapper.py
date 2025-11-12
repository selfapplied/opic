#!/usr/bin/env python3
"""
Language Evolution Mapper — Map language evolution to field equations
Language change, spread, interaction = field equations
"""

import json
import sys
import math
from pathlib import Path
from typing import Dict, List, Optional

sys.path.insert(0, str(Path(__file__).parent))
from opic_executor import OpicExecutor

class LanguageEvolutionMapper:
    """
    Maps language evolution to field equations.
    Shows that language change, spread, interaction = field equations.
    """
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.opic = OpicExecutor(project_root)
        
        # Scale-to-dimension mapping
        self.scale_dimensions = {
            "phonetic": 2.5,       # Sound change (molecular scale)
            "semantic": 3.0,       # Meaning change (word scale)
            "grammatical": 3.5,    # Grammar change (sentence scale)
            "spread": 2.5,         # Language spread (spatial scale)
            "contact": 3.0         # Language contact (interaction scale)
        }
    
    def language_change(self, initial_form: str, change_rate: float, 
                      time: float) -> Dict:
        """
        Model language change as field evolution.
        
        Args:
            initial_form: Initial linguistic form
            change_rate: Rate of change (per time unit)
            time: Time elapsed
        
        Returns:
            Language change information
        """
        # Language change follows exponential evolution: f(t) = f₀ e^(rt)
        # For simplicity, model as probability of change
        change_probability = 1 - math.exp(-change_rate * time)
        
        return {
            "initial_form": initial_form,
            "change_rate": change_rate,
            "time": time,
            "change_probability": change_probability,
            "field_interpretation": "Language change = field evolution",
            "equation": "P(change) = 1 - e^(-rt)",
            "scale": "phonetic",
            "dimension": 2.5
        }
    
    def language_spread(self, source_population: float, transmission_rate: float,
                       distance: float, time: float) -> Dict:
        """
        Model language spread as field propagation.
        
        Args:
            source_population: Source population size
            transmission_rate: Transmission rate (per person per time)
            distance: Geographic distance
            time: Time elapsed
        
        Returns:
            Language spread information
        """
        # Language spread follows diffusion: N(t) = N₀ e^(-D/r²t)
        # Simplified: spread decreases with distance
        distance_factor = math.exp(-distance / 1000.0)  # Decay with distance
        spread = source_population * transmission_rate * time * distance_factor
        
        return {
            "source_population": source_population,
            "transmission_rate": transmission_rate,
            "distance": distance,
            "time": time,
            "spread": spread,
            "distance_factor": distance_factor,
            "field_interpretation": "Language spread = field propagation",
            "equation": "N(t) ∝ N₀ e^(-D/r²t)",
            "scale": "spread",
            "dimension": 2.5
        }
    
    def language_contact(self, language1_pop: float, language2_pop: float,
                        contact_intensity: float) -> Dict:
        """
        Model language contact as field interaction.
        
        Args:
            language1_pop: Population speaking language 1
            language2_pop: Population speaking language 2
            contact_intensity: Intensity of contact (0-1)
        
        Returns:
            Language contact information
        """
        # Language contact follows interaction: borrowing ∝ contact × populations
        borrowing_rate = contact_intensity * min(language1_pop, language2_pop)
        
        return {
            "language1_pop": language1_pop,
            "language2_pop": language2_pop,
            "contact_intensity": contact_intensity,
            "borrowing_rate": borrowing_rate,
            "field_interpretation": "Language contact = field interaction",
            "equation": "borrowing ∝ contact × min(pop1, pop2)",
            "scale": "contact",
            "dimension": 3.0
        }
    
    def language_divergence(self, proto_language: str, divergence_rate: float,
                           time: float) -> Dict:
        """
        Model language divergence as field divergence.
        
        Args:
            proto_language: Proto-language
            divergence_rate: Rate of divergence (per time unit)
            time: Time since divergence
        
        Returns:
            Language divergence information
        """
        # Language divergence: similarity = e^(-rt)
        similarity = math.exp(-divergence_rate * time)
        divergence = 1 - similarity
        
        return {
            "proto_language": proto_language,
            "divergence_rate": divergence_rate,
            "time": time,
            "similarity": similarity,
            "divergence": divergence,
            "field_interpretation": "Language divergence = field divergence",
            "equation": "similarity = e^(-rt)",
            "scale": "grammatical",
            "dimension": 3.5
        }
    
    def explain_language_evolution(self, question: str) -> Dict:
        """
        Explain language evolution using field equations.
        
        Args:
            question: Question about language evolution
        
        Returns:
            Field-based explanation
        """
        question_lower = question.lower()
        
        explanation = {
            "question": question,
            "concepts": [],
            "explanation": ""
        }
        
        # Check for language evolution concepts
        if "change" in question_lower and ("language" in question_lower or "linguistic" in question_lower):
            explanation["concepts"].append("language_change")
            explanation["explanation"] += "Language change = field evolution. "
            explanation["explanation"] += "Linguistic forms evolve following field evolution equations: f(t) = f₀ e^(rt). "
            explanation["explanation"] += "Phonetic, semantic, and grammatical changes all follow field evolution. "
        
        if "spread" in question_lower or "diffusion" in question_lower:
            explanation["concepts"].append("language_spread")
            explanation["explanation"] += "Language spread = field propagation. "
            explanation["explanation"] += "Languages spread through populations following field diffusion equations: N(t) ∝ N₀ e^(-D/r²t). "
            explanation["explanation"] += "Geographic distance affects spread rate through field distance. "
        
        if "contact" in question_lower or "borrowing" in question_lower:
            explanation["concepts"].append("language_contact")
            explanation["explanation"] += "Language contact = field interaction. "
            explanation["explanation"] += "Languages borrow features through contact, following field interaction equations. "
            explanation["explanation"] += "Borrowing rate ∝ contact intensity × population size. "
        
        if "family" in question_lower or "divergence" in question_lower or "proto" in question_lower:
            explanation["concepts"].append("language_divergence")
            explanation["explanation"] += "Language divergence = field divergence. "
            explanation["explanation"] += "Languages diverge from proto-languages following field divergence equations: similarity = e^(-rt). "
            explanation["explanation"] += "Over time, languages become less similar to their proto-language. "
        
        if "acquisition" in question_lower or "learning" in question_lower:
            explanation["concepts"].append("language_acquisition")
            explanation["explanation"] += "Language acquisition = field learning. "
            explanation["explanation"] += "Children learn languages through field learning mechanisms. "
        
        if "evolution" in question_lower:
            explanation["concepts"].append("language_evolution")
            explanation["explanation"] += "Language evolution = field evolution. "
            explanation["explanation"] += "All language change follows field evolution equations at different scales. "
        
        if not explanation["explanation"]:
            explanation["explanation"] = "Language evolution = field evolution. "
            explanation["explanation"] += "Language change, spread, and interaction all follow field equations."
        
        return explanation

def main():
    """Test language evolution mapper"""
    project_root = Path(__file__).parent.parent
    mapper = LanguageEvolutionMapper(project_root)
    
    print("=" * 70)
    print("Language Evolution Mapper")
    print("=" * 70)
    print("\nMapping: Language Evolution = Field Evolution")
    print("\n" + "=" * 70)
    
    # Language change
    print("\n📝 Language Change:")
    print("-" * 70)
    change = mapper.language_change("old_form", change_rate=0.01, time=100)
    print(f"Initial form: {change['initial_form']}")
    print(f"Change rate: {change['change_rate']} per time unit")
    print(f"Time: {change['time']} time units")
    print(f"Change probability: {change['change_probability']:.2%}")
    print(f"Field interpretation: {change['field_interpretation']}")
    print(f"Equation: {change['equation']}")
    
    # Language spread
    print("\n🌍 Language Spread:")
    print("-" * 70)
    spread = mapper.language_spread(
        source_population=1000,
        transmission_rate=0.1,
        distance=500,
        time=10
    )
    print(f"Source population: {spread['source_population']:.0f}")
    print(f"Distance: {spread['distance']:.0f} km")
    print(f"Spread: {spread['spread']:.1f} speakers")
    print(f"Distance factor: {spread['distance_factor']:.3f}")
    print(f"Field interpretation: {spread['field_interpretation']}")
    
    # Language contact
    print("\n🤝 Language Contact:")
    print("-" * 70)
    contact = mapper.language_contact(
        language1_pop=5000,
        language2_pop=3000,
        contact_intensity=0.5
    )
    print(f"Language 1 population: {contact['language1_pop']:.0f}")
    print(f"Language 2 population: {contact['language2_pop']:.0f}")
    print(f"Contact intensity: {contact['contact_intensity']:.1f}")
    print(f"Borrowing rate: {contact['borrowing_rate']:.1f}")
    print(f"Field interpretation: {contact['field_interpretation']}")
    
    # Language divergence
    print("\n🌳 Language Divergence:")
    print("-" * 70)
    divergence = mapper.language_divergence(
        proto_language="Proto-Indo-European",
        divergence_rate=0.001,
        time=5000
    )
    print(f"Proto-language: {divergence['proto_language']}")
    print(f"Time since divergence: {divergence['time']} years")
    print(f"Similarity: {divergence['similarity']:.3f}")
    print(f"Divergence: {divergence['divergence']:.3f}")
    print(f"Field interpretation: {divergence['field_interpretation']}")
    
    # Explanations
    print("\n📚 Language Evolution Explanations:")
    print("-" * 70)
    
    questions = [
        "How do languages change?",
        "How do languages spread?",
        "What causes language contact?",
        "How do language families form?"
    ]
    
    for question in questions:
        explanation = mapper.explain_language_evolution(question)
        print(f"\nQ: {question}")
        print(f"   {explanation['explanation']}")
    
    print("\n" + "=" * 70)
    print("Key Insight:")
    print("=" * 70)
    print("""
Language evolution = field evolution!

• Language change = field evolution (f(t) = f₀ e^(rt))
• Language spread = field propagation (diffusion equations)
• Language contact = field interaction (borrowing ∝ contact)
• Language divergence = field divergence (similarity = e^(-rt))
• Language acquisition = field learning

All language evolution follows field equations!
    """)

if __name__ == "__main__":
    main()

