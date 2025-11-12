#!/usr/bin/env python3
"""
Astronomy Field Mapper — Map astronomical concepts to field equations
Shows how gravity, orbits, stellar dynamics = same equations at different scales
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Optional
import math

sys.path.insert(0, str(Path(__file__).parent))
from opic_executor import OpicExecutor

class AstronomyFieldMapper:
    """
    Maps astronomical concepts to field equations.
    Shows that astronomy = Field Spec 0.7 at cosmic scales.
    """
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.opic = OpicExecutor(project_root)
        
        # Scale-to-dimension mapping
        self.scale_dimensions = {
            "planetary": 2.0,      # Planetary orbits (inverse-square)
            "stellar": 2.5,         # Stellar dynamics
            "galactic": 3.5,        # Galactic structure
            "cosmological": 4.0     # Universe expansion
        }
        
        # Astronomical concept → field equation mappings
        self.astronomy_field_map = {
            # Gravity
            "gravity": {
                "field_type": "interaction",
                "scale": "planetary",
                "dimension": 2.0,
                "equation": "F = k(m₁m₂)/R^D",
                "description": "Gravity = field interaction (mass as charge)"
            },
            "gravitational_force": {
                "field_type": "force",
                "scale": "planetary",
                "dimension": 2.0,
                "equation": "F = G(m₁m₂)/R²",
                "description": "Gravitational force = dimensional Coulomb law"
            },
            "gravitational_potential": {
                "field_type": "potential",
                "scale": "planetary",
                "dimension": 2.0,
                "equation": "V(R) = -G(m₁m₂)/R",
                "description": "Gravitational potential = field potential"
            },
            
            # Orbits
            "orbit": {
                "field_type": "trajectory",
                "scale": "planetary",
                "dimension": 2.0,
                "equation": "orbit = field.trajectory(central_body, orbiting_body)",
                "description": "Orbit = field trajectory"
            },
            "orbital_motion": {
                "field_type": "motion",
                "scale": "planetary",
                "dimension": 2.0,
                "equation": "motion = field.evolve(orbit)",
                "description": "Orbital motion = field evolution"
            },
            "kepler_laws": {
                "field_type": "laws",
                "scale": "planetary",
                "dimension": 2.0,
                "equation": "laws = field.potential → field.trajectory",
                "description": "Kepler's laws = field equations"
            },
            
            # Stars
            "star": {
                "field_type": "source",
                "scale": "stellar",
                "dimension": 2.5,
                "equation": "star = field.source(mass, radius, temperature)",
                "description": "Star = field source"
            },
            "stellar_evolution": {
                "field_type": "evolution",
                "scale": "stellar",
                "dimension": 2.5,
                "equation": "evolution = field.evolve(star)",
                "description": "Stellar evolution = field evolution"
            },
            "stellar_fusion": {
                "field_type": "interaction",
                "scale": "stellar",
                "dimension": 2.5,
                "equation": "fusion = coulomb.compute_force(nuclei)",
                "description": "Stellar fusion = field interaction"
            },
            "stellar_spectrum": {
                "field_type": "spectrum",
                "scale": "stellar",
                "dimension": 2.5,
                "equation": "spectrum = field.spectrum(star)",
                "description": "Stellar spectrum = field spectrum"
            },
            
            # Planets
            "planet": {
                "field_type": "body",
                "scale": "planetary",
                "dimension": 2.0,
                "equation": "planet = field.body(mass, radius, orbit)",
                "description": "Planet = field body"
            },
            "planetary_motion": {
                "field_type": "motion",
                "scale": "planetary",
                "dimension": 2.0,
                "equation": "motion = field.evolve(planet, gravitational_field)",
                "description": "Planetary motion = field motion"
            },
            
            # Galaxies
            "galaxy": {
                "field_type": "system",
                "scale": "galactic",
                "dimension": 3.5,
                "equation": "galaxy = field.system(stars, dark_matter, rotation)",
                "description": "Galaxy = field system"
            },
            "galactic_rotation": {
                "field_type": "rotation",
                "scale": "galactic",
                "dimension": 3.5,
                "equation": "rotation = field.rotate(galaxy)",
                "description": "Galactic rotation = field rotation"
            },
            "dark_matter": {
                "field_type": "dark_field",
                "scale": "galactic",
                "dimension": 3.5,
                "equation": "dark_matter = field.measure(galaxy) - visible_field",
                "description": "Dark matter = dark field (unseen charge)"
            },
            
            # Cosmology
            "universe": {
                "field_type": "universe",
                "scale": "cosmological",
                "dimension": 4.0,
                "equation": "universe = field.universe(expansion, curvature, dark_energy)",
                "description": "Universe = field universe"
            },
            "cosmic_expansion": {
                "field_type": "expansion",
                "scale": "cosmological",
                "dimension": 4.0,
                "equation": "expansion = field.expand(universe)",
                "description": "Cosmic expansion = field expansion"
            },
            "big_bang": {
                "field_type": "singularity",
                "scale": "cosmological",
                "dimension": 4.0,
                "equation": "big_bang = field.singularity → field.expand",
                "description": "Big Bang = field singularity → expansion"
            }
        }
    
    def map_astronomy_to_field(self, concept: str) -> Dict:
        """
        Map an astronomical concept to field equations.
        
        Args:
            concept: Astronomical concept (e.g., "gravity", "orbit", "star")
        
        Returns:
            Field equation mapping
        """
        concept_lower = concept.lower()
        
        # Direct lookup
        if concept_lower in self.astronomy_field_map:
            return self.astronomy_field_map[concept_lower]
        
        # Fuzzy matching
        for key, mapping in self.astronomy_field_map.items():
            if key in concept_lower or concept_lower in key:
                return mapping
        
        # Default: generic astronomical field
        return {
            "field_type": "astronomical",
            "scale": "unknown",
            "dimension": 2.5,
            "equation": "F = k(m₁m₂)/R^D",
            "description": f"{concept} = astronomical field (same equations, different scale)"
        }
    
    def explain_astronomy_as_field(self, question: str) -> Dict:
        """
        Explain an astronomy question using field equations.
        
        Args:
            question: Astronomy question
        
        Returns:
            Field-based explanation
        """
        # Extract astronomical concepts from question
        concepts = self._extract_concepts(question)
        
        # Map each concept to field equations
        field_mappings = {}
        for concept in concepts:
            field_mappings[concept] = self.map_astronomy_to_field(concept)
        
        # Determine scale and dimension
        scales = [m["scale"] for m in field_mappings.values()]
        dimensions = [m["dimension"] for m in field_mappings.values()]
        
        avg_dimension = sum(dimensions) / len(dimensions) if dimensions else 2.5
        
        # Generate field-based explanation
        explanation = {
            "question": question,
            "concepts": concepts,
            "field_mappings": field_mappings,
            "scale": scales[0] if scales else "unknown",
            "dimension": avg_dimension,
            "explanation": self._generate_explanation(question, field_mappings, avg_dimension)
        }
        
        return explanation
    
    def _extract_concepts(self, text: str) -> List[str]:
        """Extract astronomical concepts from text"""
        concepts = []
        text_lower = text.lower()
        
        # Check for known concepts
        for concept in self.astronomy_field_map.keys():
            if concept in text_lower:
                concepts.append(concept)
        
        # Also check for common astronomy terms
        astronomy_terms = [
            "gravity", "gravitational", "orbit", "orbital", "planet", "planetary",
            "star", "stellar", "sun", "solar", "galaxy", "galactic", "galaxies",
            "universe", "cosmic", "cosmological", "big bang", "big_bang",
            "dark matter", "dark_matter", "dark energy", "dark_energy", 
            "fusion", "spectrum", "rotation", "rotate", "nebula", "black hole"
        ]
        
        for term in astronomy_terms:
            if term in text_lower:
                # Map to canonical concept name
                if term == "galaxies" or term == "galactic":
                    concept_name = "galaxy"
                elif term == "rotate" or term == "rotation":
                    concept_name = "galactic_rotation"
                elif term == "dark matter":
                    concept_name = "dark_matter"
                elif term == "dark energy":
                    concept_name = "dark_energy"
                elif term == "big bang":
                    concept_name = "big_bang"
                else:
                    concept_name = term
                
                if concept_name not in concepts:
                    concepts.append(concept_name)
        
        return concepts
    
    def _generate_explanation(self, question: str, mappings: Dict, dimension: float) -> str:
        """Generate field-based explanation"""
        if not mappings:
            return f"This astronomical process follows field equations at dimension D={dimension:.1f}."
        
        concept = list(mappings.keys())[0]
        mapping = mappings[concept]
        
        explanation = f"{concept.capitalize()} operates as a {mapping['field_type']} "
        explanation += f"at the {mapping['scale']} scale (D={mapping['dimension']:.1f}). "
        explanation += f"{mapping['description']} "
        explanation += f"The interaction follows: {mapping['equation']}"
        
        return explanation

def main():
    """Test astronomy field mapper"""
    project_root = Path(__file__).parent.parent
    mapper = AstronomyFieldMapper(project_root)
    
    print("=" * 70)
    print("Astronomy Field Mapper")
    print("=" * 70)
    print("\nMapping: Astronomy = Field Equations at Different Scales")
    print("\n" + "=" * 70)
    
    # Example questions
    examples = [
        "How do planets orbit stars?",
        "What causes stellar fusion?",
        "How do galaxies rotate?",
        "What is gravitational force?",
        "What is dark matter?"
    ]
    
    for question in examples:
        print(f"\n🌌 Question: {question}")
        explanation = mapper.explain_astronomy_as_field(question)
        print(f"   Concepts: {', '.join(explanation['concepts'])}")
        print(f"   Scale: {explanation['scale']}, Dimension: {explanation['dimension']:.1f}")
        print(f"   Explanation: {explanation['explanation']}")
    
    print("\n" + "=" * 70)
    print("Key Insight:")
    print("=" * 70)
    print("""
Astronomy follows the same field equations at different scales:

• Planetary (D≈2.0): Gravity = field interaction, Orbits = field trajectories
• Stellar (D≈2.5): Stars = field sources, Fusion = field interactions
• Galactic (D≈3.5): Galaxies = field systems, Dark matter = dark field
• Cosmological (D≈4.0): Universe = field universe, Expansion = field expansion

All follow: F = k(m₁m₂)/R^D
Same equations, different scales!
    """)

if __name__ == "__main__":
    main()

