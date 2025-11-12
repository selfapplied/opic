#!/usr/bin/env python3
"""
Pharmacology Evolution Mapper — Map catalysts, receptors, pharmacokinetics, evolution to field equations
Enzymes, receptors, drug kinetics, evolution = field equations
"""

import json
import sys
import math
from pathlib import Path
from typing import Dict, List, Optional

sys.path.insert(0, str(Path(__file__).parent))
from opic_executor import OpicExecutor

class PharmacologyEvolutionMapper:
    """
    Maps catalysts, receptors, pharmacokinetics, and evolution to field equations.
    Shows that enzymes, receptors, drug kinetics, evolution = field equations.
    """
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.opic = OpicExecutor(project_root)
        
        # Scale-to-dimension mapping
        self.scale_dimensions = {
            "catalytic": 2.5,      # Catalytic scale (enzymes, catalysts)
            "receptor": 3.0,      # Receptor scale (cell receptors)
            "pharmacokinetic": 3.0,# Pharmacokinetic scale (drug kinetics)
            "evolutionary": 3.5   # Evolutionary scale (populations)
        }
    
    def enzyme_catalysis(self, substrate_concentration: float, km: float,
                        vmax: float) -> Dict:
        """
        Compute enzyme catalysis rate (Michaelis-Menten kinetics).
        
        Args:
            substrate_concentration: [S] (M)
            km: Michaelis constant (M)
            vmax: Maximum velocity (M/s)
        
        Returns:
            Enzyme catalysis information
        """
        # Michaelis-Menten: v = (Vmax [S]) / (Km + [S])
        rate = (vmax * substrate_concentration) / (km + substrate_concentration)
        
        return {
            "substrate_concentration": substrate_concentration,
            "km": km,
            "vmax": vmax,
            "rate": rate,
            "field_interpretation": "Enzyme catalysis = field catalysis",
            "equation": "v = (Vmax [S]) / (Km + [S])"
        }
    
    def receptor_binding(self, ligand_concentration: float, kd: float,
                         receptor_concentration: float) -> Dict:
        """
        Compute receptor binding (binding isotherm).
        
        Args:
            ligand_concentration: [L] (M)
            kd: Dissociation constant (M)
            receptor_concentration: [R] (M)
        
        Returns:
            Receptor binding information
        """
        # Binding: [RL] = ([R] [L]) / (Kd + [L])
        bound_receptor = (receptor_concentration * ligand_concentration) / (kd + ligand_concentration)
        binding_fraction = bound_receptor / receptor_concentration if receptor_concentration > 0 else 0.0
        
        return {
            "ligand_concentration": ligand_concentration,
            "kd": kd,
            "receptor_concentration": receptor_concentration,
            "bound_receptor": bound_receptor,
            "binding_fraction": binding_fraction,
            "field_interpretation": "Receptor binding = field binding",
            "equation": "[RL] = ([R] [L]) / (Kd + [L])"
        }
    
    def drug_clearance(self, initial_concentration: float, clearance_rate: float,
                      time: float) -> Dict:
        """
        Compute drug clearance (first-order kinetics).
        
        Args:
            initial_concentration: C₀ (mg/L)
            clearance_rate: Clearance rate k (1/h)
            time: Time elapsed (h)
        
        Returns:
            Drug clearance information
        """
        # First-order clearance: C(t) = C₀ e^(-kt)
        concentration = initial_concentration * math.exp(-clearance_rate * time)
        half_life = math.log(2) / clearance_rate if clearance_rate > 0 else float('inf')
        
        return {
            "initial_concentration": initial_concentration,
            "clearance_rate": clearance_rate,
            "time": time,
            "concentration": concentration,
            "half_life": half_life,
            "field_interpretation": "Drug clearance = field clearance",
            "equation": "C(t) = C₀ e^(-kt)"
        }
    
    def allele_frequency_change(self, initial_frequency: float, selection_coefficient: float,
                               generations: int) -> Dict:
        """
        Compute allele frequency change under selection.
        
        Args:
            initial_frequency: Initial allele frequency p₀
            selection_coefficient: Selection coefficient s
            generations: Number of generations
        
        Returns:
            Allele frequency change information
        """
        # Simplified: p(t) ≈ p₀ e^(st) for small s
        # More accurate: p(t) = p₀ / (p₀ + (1-p₀)e^(-st))
        if selection_coefficient == 0:
            final_frequency = initial_frequency
        else:
            denominator = initial_frequency + (1 - initial_frequency) * math.exp(-selection_coefficient * generations)
            final_frequency = initial_frequency / denominator if denominator > 0 else 1.0
        
        frequency_change = final_frequency - initial_frequency
        
        return {
            "initial_frequency": initial_frequency,
            "selection_coefficient": selection_coefficient,
            "generations": generations,
            "final_frequency": final_frequency,
            "frequency_change": frequency_change,
            "field_interpretation": "Allele frequency change = field evolution",
            "equation": "p(t) = p₀ / (p₀ + (1-p₀)e^(-st))"
        }
    
    def explain_pharmacology_evolution(self, question: str) -> Dict:
        """
        Explain pharmacology or evolution using field equations.
        
        Args:
            question: Question about catalysts, receptors, pharmacokinetics, or evolution
        
        Returns:
            Field-based explanation
        """
        question_lower = question.lower()
        
        explanation = {
            "question": question,
            "concepts": [],
            "explanation": ""
        }
        
        # Check for catalyst/enzyme concepts
        if "enzyme" in question_lower or "catalyst" in question_lower:
            explanation["concepts"].append("catalyst")
            explanation["explanation"] += "Enzymes = field catalysts. "
            explanation["explanation"] += "Lower activation energy (field barrier) to speed up reactions. "
            explanation["explanation"] += "Michaelis-Menten kinetics: v = (Vmax [S]) / (Km + [S]). "
        
        # Check for receptor concepts
        if "receptor" in question_lower or "binding" in question_lower:
            explanation["concepts"].append("receptor")
            explanation["explanation"] += "Cell receptors = field receptors. "
            explanation["explanation"] += "Receptor binding = field binding, follows binding isotherm. "
            explanation["explanation"] += "Binding affinity = field coupling strength. "
            explanation["explanation"] += "Signal transduction = field propagation. "
        
        # Check for pharmacokinetics concepts
        if "pharmacokinetic" in question_lower or "drug" in question_lower or "clearance" in question_lower:
            explanation["concepts"].append("pharmacokinetics")
            explanation["explanation"] += "Pharmacokinetics = field kinetics. "
            explanation["explanation"] += "Absorption, distribution, metabolism, excretion all follow field equations. "
            explanation["explanation"] += "Drug clearance: C(t) = C₀ e^(-kt). "
        
        # Check for evolution concepts
        if "evolution" in question_lower or "natural selection" in question_lower:
            explanation["concepts"].append("evolution")
            explanation["explanation"] += "Evolution = field evolution. "
            explanation["explanation"] += "Natural selection = field selection, genetic drift = field drift. "
            explanation["explanation"] += "Mutation = field perturbation, gene flow = field flow. "
            explanation["explanation"] += "Modern evolutionary synthesis combines all field processes. "
        
        if "allele frequency" in question_lower or "population genetics" in question_lower:
            explanation["concepts"].append("population_genetics")
            explanation["explanation"] += "Population genetics = field genetics. "
            explanation["explanation"] += "Allele frequency change follows field evolution equations. "
            explanation["explanation"] += "Selection, drift, mutation, gene flow all follow field equations. "
        
        if not explanation["explanation"]:
            explanation["explanation"] = "Catalysts, receptors, pharmacokinetics, and evolution = field equations. "
            explanation["explanation"] += "All follow field equations at different scales."
        
        return explanation

def main():
    """Test pharmacology evolution mapper"""
    project_root = Path(__file__).parent.parent
    mapper = PharmacologyEvolutionMapper(project_root)
    
    print("=" * 70)
    print("Pharmacology Evolution Mapper")
    print("=" * 70)
    print("\nMapping: Catalysts, Receptors, Pharmacokinetics, Evolution = Field Equations")
    print("\n" + "=" * 70)
    
    # Enzyme catalysis
    print("\n⚗️  Enzyme Catalysis:")
    print("-" * 70)
    enzyme = mapper.enzyme_catalysis(substrate_concentration=0.1, km=0.05, vmax=1.0)
    print(f"Substrate: {enzyme['substrate_concentration']:.2f} M")
    print(f"Km: {enzyme['km']:.2f} M, Vmax: {enzyme['vmax']:.2f} M/s")
    print(f"Rate: {enzyme['rate']:.3f} M/s")
    print(f"Field interpretation: {enzyme['field_interpretation']}")
    print(f"Equation: {enzyme['equation']}")
    
    # Receptor binding (using realistic Kd values)
    print("\n🔬 Receptor Binding:")
    print("-" * 70)
    # Realistic: Kd = 1 μM = 0.000001 M (typical for many receptors)
    receptor = mapper.receptor_binding(ligand_concentration=0.00001, kd=0.000001, receptor_concentration=0.001)
    print(f"Ligand: {receptor['ligand_concentration']:.6f} M ({receptor['ligand_concentration']*1000000:.2f} μM)")
    print(f"Kd: {receptor['kd']:.6f} M ({receptor['kd']*1000000:.2f} μM)")
    print(f"Bound receptor: {receptor['bound_receptor']:.6f} M")
    print(f"Binding fraction: {receptor['binding_fraction']:.1%}")
    print(f"Field interpretation: {receptor['field_interpretation']}")
    
    # Drug clearance
    print("\n💊 Drug Clearance:")
    print("-" * 70)
    clearance = mapper.drug_clearance(initial_concentration=100.0, clearance_rate=0.1, time=5.0)
    print(f"Initial concentration: {clearance['initial_concentration']:.1f} mg/L")
    print(f"Clearance rate: {clearance['clearance_rate']:.2f} 1/h")
    print(f"Concentration at t={clearance['time']:.1f}h: {clearance['concentration']:.2f} mg/L")
    print(f"Half-life: {clearance['half_life']:.2f} h")
    print(f"Field interpretation: {clearance['field_interpretation']}")
    
    # Allele frequency change
    print("\n🧬 Allele Frequency Change:")
    print("-" * 70)
    evolution = mapper.allele_frequency_change(initial_frequency=0.1, selection_coefficient=0.01, generations=100)
    print(f"Initial frequency: {evolution['initial_frequency']:.1%}")
    print(f"Selection coefficient: {evolution['selection_coefficient']:.3f}")
    print(f"Final frequency: {evolution['final_frequency']:.1%}")
    print(f"Frequency change: {evolution['frequency_change']:+.1%}")
    print(f"Field interpretation: {evolution['field_interpretation']}")
    
    # Explanations
    print("\n📚 Pharmacology & Evolution Explanations:")
    print("-" * 70)
    
    questions = [
        "How do enzymes work?",
        "How do cell receptors work?",
        "How does drug clearance work?",
        "How does evolution work?"
    ]
    
    for question in questions:
        explanation = mapper.explain_pharmacology_evolution(question)
        print(f"\nQ: {question}")
        print(f"   {explanation['explanation']}")
    
    print("\n" + "=" * 70)
    print("Key Insight:")
    print("=" * 70)
    print("""
Catalysts, Receptors, Pharmacokinetics, Evolution = field equations!

• Enzymes = field catalysts (lower activation energy = lower field barrier)
• Receptors = field receptors (binding = field binding, transduction = field propagation)
• Pharmacokinetics = field kinetics (ADME all follow field equations)
• Evolution = field evolution (selection = field selection, drift = field drift)

All follow field equations at different scales!
    """)

if __name__ == "__main__":
    main()

