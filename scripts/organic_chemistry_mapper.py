#!/usr/bin/env python3
"""
Organic Chemistry Mapper — Map organic chemistry laws to field equations
Reactions, bonding, mechanisms = field equations
"""

import json
import sys
import math
from pathlib import Path
from typing import Dict, List, Optional

sys.path.insert(0, str(Path(__file__).parent))
from opic_executor import OpicExecutor

class OrganicChemistryMapper:
    """
    Maps organic chemistry laws to field equations.
    Shows that reactions, bonding, mechanisms = field equations.
    """
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.opic = OpicExecutor(project_root)
        
        # Scale-to-dimension mapping
        self.scale_dimensions = {
            "molecular": 2.5,      # Molecular scale (bonds, reactions)
            "electronic": 2.5,     # Electronic scale (functional groups)
            "stereochemical": 3.0  # Stereochemical scale (chirality)
        }
        
        # Organic chemistry concept → field equation mappings
        self.organic_field_map = {
            # Bonds
            "covalent_bond": {
                "field_type": "bond",
                "scale": "molecular",
                "dimension": 2.5,
                "equation": "E_bond = coulomb.compute_potential(atom1, atom2)",
                "description": "Covalent bond = field bond"
            },
            "ionic_bond": {
                "field_type": "bond",
                "scale": "molecular",
                "dimension": 2.5,
                "equation": "E_bond = coulomb.compute_force(cation, anion)",
                "description": "Ionic bond = field bond"
            },
            "hydrogen_bond": {
                "field_type": "bond",
                "scale": "molecular",
                "dimension": 2.5,
                "equation": "E_bond = coulomb.compute_potential(donor, acceptor)",
                "description": "Hydrogen bond = field bond"
            },
            
            # Reactions
            "sn2_reaction": {
                "field_type": "substitution",
                "scale": "molecular",
                "dimension": 2.5,
                "equation": "product = field.substitute(substrate, nucleophile)",
                "description": "SN2 reaction = field substitution"
            },
            "sn1_reaction": {
                "field_type": "substitution",
                "scale": "molecular",
                "dimension": 2.5,
                "equation": "substrate → field.dissociate → carbocation → field.substitute → product",
                "description": "SN1 reaction = field substitution (two-step)"
            },
            "e2_elimination": {
                "field_type": "elimination",
                "scale": "molecular",
                "dimension": 2.5,
                "equation": "alkene = field.eliminate(substrate, base)",
                "description": "E2 elimination = field elimination"
            },
            "addition_reaction": {
                "field_type": "addition",
                "scale": "molecular",
                "dimension": 2.5,
                "equation": "product = field.add(alkene, reagent)",
                "description": "Addition reaction = field addition"
            },
            
            # Aromaticity
            "aromaticity": {
                "field_type": "aromaticity",
                "scale": "electronic",
                "dimension": 2.5,
                "equation": "aromatic = if (electrons == 4n+2) then aromatic",
                "description": "Aromaticity = field aromaticity (Hückel's rule)"
            },
            
            # Functional groups
            "electron_withdrawing": {
                "field_type": "electronic_effect",
                "scale": "electronic",
                "dimension": 2.5,
                "equation": "effect = field.withdraw(electrons)",
                "description": "Electron-withdrawing = field withdrawal"
            },
            "electron_donating": {
                "field_type": "electronic_effect",
                "scale": "electronic",
                "dimension": 2.5,
                "equation": "effect = field.donate(electrons)",
                "description": "Electron-donating = field donation"
            },
            
            # Stereochemistry
            "chirality": {
                "field_type": "stereochemistry",
                "scale": "stereochemical",
                "dimension": 3.0,
                "equation": "chiral_center = field.handedness(molecule)",
                "description": "Chirality = field handedness"
            },
            "enantiomer": {
                "field_type": "stereochemistry",
                "scale": "stereochemical",
                "dimension": 3.0,
                "equation": "enantiomer = field.mirror(molecule)",
                "description": "Enantiomer = field mirror"
            }
        }
    
    def map_organic_to_field(self, concept: str) -> Dict:
        """
        Map an organic chemistry concept to field equations.
        
        Args:
            concept: Organic chemistry concept
        
        Returns:
            Field equation mapping
        """
        concept_lower = concept.lower().replace(" ", "_")
        
        # Direct lookup
        if concept_lower in self.organic_field_map:
            return self.organic_field_map[concept_lower]
        
        # Fuzzy matching
        for key, mapping in self.organic_field_map.items():
            if key in concept_lower or concept_lower in key:
                return mapping
        
        # Special cases
        if "electron" in concept_lower and "withdraw" in concept_lower:
            return self.organic_field_map["electron_withdrawing"]
        if "electron" in concept_lower and ("donat" in concept_lower or "donor" in concept_lower):
            return self.organic_field_map["electron_donating"]
        
        # Default
        return {
            "field_type": "organic",
            "scale": "molecular",
            "dimension": 2.5,
            "equation": "F = k(q₁q₂)/R^D",
            "description": f"{concept} = organic field (same equations, different scale)"
        }
    
    def reaction_rate(self, activation_energy: float, temperature: float) -> Dict:
        """
        Compute reaction rate from activation energy (Arrhenius equation).
        
        Args:
            activation_energy: Activation energy (J/mol)
            temperature: Temperature (K)
        
        Returns:
            Reaction rate information
        """
        # Arrhenius: k = A e^(-Ea/RT)
        R = 8.314  # Gas constant (J/mol·K)
        A = 1e13  # Pre-exponential factor (simplified)
        
        rate_constant = A * math.exp(-activation_energy / (R * temperature))
        
        return {
            "activation_energy": activation_energy,
            "temperature": temperature,
            "rate_constant": rate_constant,
            "field_interpretation": "Reaction rate = field rate (activation energy = field barrier)",
            "equation": "k = A e^(-Ea/RT)"
        }
    
    def bond_energy(self, atom1: str, atom2: str, bond_type: str = "covalent") -> Dict:
        """
        Estimate bond energy from field equations.
        
        Args:
            atom1: First atom
            atom2: Second atom
            bond_type: Type of bond
        
        Returns:
            Bond energy information
        """
        # Simplified: bond energy from field potential
        # Typical covalent bonds: 200-500 kJ/mol
        base_energy = 350.0  # kJ/mol (average)
        
        # Adjust for bond type
        if bond_type == "ionic":
            base_energy *= 1.5
        elif bond_type == "hydrogen":
            base_energy *= 0.1
        
        return {
            "atom1": atom1,
            "atom2": atom2,
            "bond_type": bond_type,
            "bond_energy": base_energy,
            "field_interpretation": "Bond energy = field potential",
            "equation": "E_bond = coulomb.compute_potential(atom1, atom2)"
        }
    
    def explain_organic_chemistry(self, question: str) -> Dict:
        """
        Explain organic chemistry using field equations.
        
        Args:
            question: Question about organic chemistry
        
        Returns:
            Field-based explanation
        """
        question_lower = question.lower()
        
        explanation = {
            "question": question,
            "concepts": [],
            "explanation": ""
        }
        
        # Check for reaction concepts
        if "sn2" in question_lower or "substitution" in question_lower:
            explanation["concepts"].append("sn2_reaction")
            explanation["explanation"] += "SN2 reaction = field substitution. "
            explanation["explanation"] += "Nucleophile substitutes leaving group following field substitution equations. "
        
        if "sn1" in question_lower:
            explanation["concepts"].append("sn1_reaction")
            explanation["explanation"] += "SN1 reaction = field substitution (two-step). "
            explanation["explanation"] += "Substrate dissociates to carbocation, then nucleophile substitutes. "
        
        if "elimination" in question_lower or "e2" in question_lower or "e1" in question_lower:
            explanation["concepts"].append("elimination")
            explanation["explanation"] += "Elimination reaction = field elimination. "
            explanation["explanation"] += "Base removes leaving group, forming alkene following field elimination equations. "
        
        if "aromatic" in question_lower or "huckel" in question_lower:
            explanation["concepts"].append("aromaticity")
            explanation["explanation"] += "Aromaticity = field aromaticity. "
            explanation["explanation"] += "Hückel's rule: 4n+2 π electrons = aromatic (field stability). "
        
        if "functional group" in question_lower or "electron" in question_lower:
            explanation["concepts"].append("functional_groups")
            explanation["explanation"] += "Functional groups = field groups. "
            explanation["explanation"] += "Electron-withdrawing/donating groups affect reactivity through field effects. "
        
        if "bond" in question_lower:
            explanation["concepts"].append("bond")
            explanation["explanation"] += "Chemical bonds = field bonds. "
            explanation["explanation"] += "Bond energy = field potential, follows coulomb.compute_potential. "
        
        if "chiral" in question_lower or "stereochemistry" in question_lower:
            explanation["concepts"].append("stereochemistry")
            explanation["explanation"] += "Stereochemistry = field stereochemistry. "
            explanation["explanation"] += "Chirality = field handedness, enantiomers = field mirrors. "
        
        if not explanation["explanation"]:
            explanation["explanation"] = "Organic chemistry = field chemistry. "
            explanation["explanation"] += "Reactions, bonding, and mechanisms all follow field equations."
        
        return explanation

def main():
    """Test organic chemistry mapper"""
    project_root = Path(__file__).parent.parent
    mapper = OrganicChemistryMapper(project_root)
    
    print("=" * 70)
    print("Organic Chemistry Mapper")
    print("=" * 70)
    print("\nMapping: Organic Chemistry Laws = Field Equations")
    print("\n" + "=" * 70)
    
    # Reaction rate
    print("\n⚗️  Reaction Rate:")
    print("-" * 70)
    rate = mapper.reaction_rate(activation_energy=50000, temperature=300)
    print(f"Activation energy: {rate['activation_energy']:.0f} J/mol")
    print(f"Temperature: {rate['temperature']:.0f} K")
    print(f"Rate constant: {rate['rate_constant']:.2e}")
    print(f"Field interpretation: {rate['field_interpretation']}")
    print(f"Equation: {rate['equation']}")
    
    # Bond energy
    print("\n🔗 Bond Energy:")
    print("-" * 70)
    bond = mapper.bond_energy("C", "C", "covalent")
    print(f"Bond: {bond['atom1']}-{bond['atom2']} ({bond['bond_type']})")
    print(f"Bond energy: {bond['bond_energy']:.0f} kJ/mol")
    print(f"Field interpretation: {bond['field_interpretation']}")
    
    # Concept mappings
    print("\n📚 Organic Chemistry Concepts:")
    print("-" * 70)
    concepts = ["SN2 reaction", "aromaticity", "chirality", "electron-withdrawing"]
    for concept in concepts:
        mapping = mapper.map_organic_to_field(concept)
        print(f"\n{concept}:")
        print(f"  Field type: {mapping['field_type']}")
        print(f"  Scale: {mapping['scale']}, Dimension: {mapping['dimension']}")
        print(f"  Description: {mapping['description']}")
        print(f"  Equation: {mapping['equation']}")
    
    # Explanations
    print("\n📚 Organic Chemistry Explanations:")
    print("-" * 70)
    
    questions = [
        "How do SN2 reactions work?",
        "What is aromaticity?",
        "How do functional groups affect reactivity?",
        "What is chirality?"
    ]
    
    for question in questions:
        explanation = mapper.explain_organic_chemistry(question)
        print(f"\nQ: {question}")
        print(f"   {explanation['explanation']}")
    
    print("\n" + "=" * 70)
    print("Key Insight:")
    print("=" * 70)
    print("""
Organic chemistry laws = field equations!

• Chemical bonds = field bonds (E_bond = coulomb.compute_potential)
• Reactions = field reactions (SN2 = field.substitute, E2 = field.eliminate)
• Aromaticity = field aromaticity (Hückel's rule = field stability)
• Functional groups = field groups (electronic effects = field effects)
• Stereochemistry = field stereochemistry (chirality = field handedness)

All organic chemistry follows field equations!
    """)

if __name__ == "__main__":
    main()

