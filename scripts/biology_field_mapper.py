#!/usr/bin/env python3
"""
Biology Field Mapper — Map biological concepts to field equations
Shows how genetics, hormones, genes, chemistry = same equations at different scales
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Optional
import math

sys.path.insert(0, str(Path(__file__).parent))
from opic_executor import OpicExecutor

class BiologyFieldMapper:
    """
    Maps biological concepts to field equations.
    Shows that biology = Field Spec 0.7 at different scales.
    """
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.opic = OpicExecutor(project_root)
        
        # Scale-to-dimension mapping
        self.scale_dimensions = {
            "molecular": 2.5,      # Chemistry, bonds
            "genetic": 3.5,       # DNA, genes, alleles
            "hormonal": 3.5,      # Hormones, signaling
            "cellular": 4.0,      # Cells, organelles
            "organism": 4.5        # Organisms, systems
        }
        
        # Biological concept → field equation mappings
        self.biology_field_map = {
            # Genetics
            "gene": {
                "field_type": "operator",
                "scale": "genetic",
                "dimension": 3.5,
                "equation": "V(R) = k(q₁q₂)/((D-1)R^{D-1})",
                "description": "Gene = field operator carrying information"
            },
            "allele": {
                "field_type": "variant",
                "scale": "genetic",
                "dimension": 3.5,
                "equation": "ΔV = field.perturb(gene)",
                "description": "Allele = field variant (mutation perturbs field)"
            },
            "dna": {
                "field_type": "configuration",
                "scale": "genetic",
                "dimension": 3.5,
                "equation": "DNA → aperture.chain → phi_k",
                "description": "DNA sequence = field configuration"
            },
            "genetic_inheritance": {
                "field_type": "propagation",
                "scale": "genetic",
                "dimension": 3.5,
                "equation": "offspring = field.combine(parent1, parent2)",
                "description": "Inheritance = field combination"
            },
            
            # Hormones
            "hormone": {
                "field_type": "propagator",
                "scale": "hormonal",
                "dimension": 3.5,
                "equation": "signal = field.propagate(hormone, receptor)",
                "description": "Hormone = field propagator"
            },
            "receptor": {
                "field_type": "target",
                "scale": "hormonal",
                "dimension": 3.5,
                "equation": "binding = coulomb.compute_potential(hormone, receptor)",
                "description": "Receptor = target field"
            },
            "endocrine_system": {
                "field_type": "network",
                "scale": "hormonal",
                "dimension": 3.5,
                "equation": "system = field.network(glands, hormones)",
                "description": "Endocrine system = field network"
            },
            
            # Chemistry
            "chemical_bond": {
                "field_type": "interaction",
                "scale": "molecular",
                "dimension": 2.5,
                "equation": "F = k(q₁q₂)/R^D",
                "description": "Chemical bond = field interaction"
            },
            "molecule": {
                "field_type": "structure",
                "scale": "molecular",
                "dimension": 2.5,
                "equation": "structure = field.equilibrium(atoms)",
                "description": "Molecule = field equilibrium structure"
            },
            "enzyme": {
                "field_type": "catalyst",
                "scale": "molecular",
                "dimension": 2.5,
                "equation": "reaction = field.catalyze(substrate, enzyme)",
                "description": "Enzyme = field catalyst"
            },
            
            # Cells
            "cell": {
                "field_type": "unit",
                "scale": "cellular",
                "dimension": 4.0,
                "equation": "cell = field.unit(membrane, organelles, dna_field)",
                "description": "Cell = field unit with boundary"
            },
            "cell_division": {
                "field_type": "replication",
                "scale": "cellular",
                "dimension": 4.0,
                "equation": "daughter = field.replicate(parent)",
                "description": "Cell division = field replication"
            },
            
            # Organisms
            "organism": {
                "field_type": "system",
                "scale": "organism",
                "dimension": 4.5,
                "equation": "organism = field.system(cells, organs, metabolism)",
                "description": "Organism = integrated field system"
            }
        }
    
    def map_biology_to_field(self, concept: str) -> Dict:
        """
        Map a biological concept to field equations.
        
        Args:
            concept: Biological concept (e.g., "gene", "hormone", "enzyme")
        
        Returns:
            Field equation mapping
        """
        concept_lower = concept.lower()
        
        # Direct lookup
        if concept_lower in self.biology_field_map:
            return self.biology_field_map[concept_lower]
        
        # Fuzzy matching
        for key, mapping in self.biology_field_map.items():
            if key in concept_lower or concept_lower in key:
                return mapping
        
        # Default: generic biological field
        return {
            "field_type": "biological",
            "scale": "unknown",
            "dimension": 3.5,
            "equation": "V(R) = k(q₁q₂)/((D-1)R^{D-1})",
            "description": f"{concept} = biological field (same equations, different scale)"
        }
    
    def explain_biology_as_field(self, question: str) -> Dict:
        """
        Explain a biology question using field equations.
        
        Args:
            question: Biology question
        
        Returns:
            Field-based explanation
        """
        # Extract biological concepts from question
        concepts = self._extract_concepts(question)
        
        # Map each concept to field equations
        field_mappings = {}
        for concept in concepts:
            field_mappings[concept] = self.map_biology_to_field(concept)
        
        # Determine scale and dimension
        scales = [m["scale"] for m in field_mappings.values()]
        dimensions = [m["dimension"] for m in field_mappings.values()]
        
        avg_dimension = sum(dimensions) / len(dimensions) if dimensions else 3.5
        
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
        """Extract biological concepts from text"""
        concepts = []
        text_lower = text.lower()
        
        # Check for known concepts
        for concept in self.biology_field_map.keys():
            if concept in text_lower:
                concepts.append(concept)
        
        # Also check for common biology terms
        biology_terms = [
            "gene", "dna", "rna", "allele", "chromosome",
            "hormone", "receptor", "enzyme", "protein",
            "cell", "molecule", "atom", "bond",
            "mitochondria", "nucleus", "membrane"
        ]
        
        for term in biology_terms:
            if term in text_lower and term not in concepts:
                concepts.append(term)
        
        return concepts
    
    def _generate_explanation(self, question: str, mappings: Dict, dimension: float) -> str:
        """Generate field-based explanation"""
        if not mappings:
            return f"This biological process follows field equations at dimension D={dimension:.1f}."
        
        concept = list(mappings.keys())[0]
        mapping = mappings[concept]
        
        explanation = f"{concept.capitalize()} operates as a {mapping['field_type']} "
        explanation += f"at the {mapping['scale']} scale (D={mapping['dimension']:.1f}). "
        explanation += f"{mapping['description']} "
        explanation += f"The interaction follows: {mapping['equation']}"
        
        return explanation
    
    def add_biology_knowledge(self, question: str, answer: str) -> Dict:
        """
        Add biology knowledge entry with field mapping.
        
        Args:
            question: Biology question
            answer: Correct answer
        
        Returns:
            Knowledge entry with field properties
        """
        # Map question to field
        field_explanation = self.explain_biology_as_field(question)
        
        # Compute field properties
        concepts = field_explanation["concepts"]
        dimension = field_explanation["dimension"]
        
        # Estimate phi_k from dimension (higher D → higher phi_k)
        phi_k = dimension * 2.0
        
        # Create knowledge entry
        knowledge_entry = {
            "text": f"{question} {answer}",
            "domain": "biology",
            "concepts": concepts,
            "field_properties": {
                "phi_k": phi_k,
                "dimension": dimension,
                "scale": field_explanation["scale"],
                "field_mappings": field_explanation["field_mappings"]
            },
            "field_explanation": field_explanation["explanation"]
        }
        
        return knowledge_entry

def main():
    """Test biology field mapper"""
    project_root = Path(__file__).parent.parent
    mapper = BiologyFieldMapper(project_root)
    
    print("=" * 70)
    print("Biology Field Mapper")
    print("=" * 70)
    print("\nMapping: Biology = Field Equations at Different Scales")
    print("\n" + "=" * 70)
    
    # Example questions
    examples = [
        "How do hormones work?",
        "What is genetic inheritance?",
        "How do enzymes catalyze reactions?",
        "What is the role of DNA in cells?",
        "How do genes control traits?"
    ]
    
    for question in examples:
        print(f"\n📚 Question: {question}")
        explanation = mapper.explain_biology_as_field(question)
        print(f"   Concepts: {', '.join(explanation['concepts'])}")
        print(f"   Scale: {explanation['scale']}, Dimension: {explanation['dimension']:.1f}")
        print(f"   Explanation: {explanation['explanation']}")
    
    print("\n" + "=" * 70)
    print("Key Insight:")
    print("=" * 70)
    print("""
Biology follows the same field equations at different scales:

• Molecular (D≈2.5): Chemical bonds = field interactions
• Genetic (D≈3.5): Genes = field operators, DNA = field configuration
• Hormonal (D≈3.5): Hormones = field propagators
• Cellular (D≈4.0): Cells = field units
• Organism (D≈4.5): Organisms = integrated field systems

All follow: F = k(q₁q₂)/R^D
Same equations, different scales!
    """)

if __name__ == "__main__":
    main()

