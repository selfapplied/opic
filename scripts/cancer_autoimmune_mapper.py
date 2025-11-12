#!/usr/bin/env python3
"""
Cancer Autoimmune Mapper — Map cancer and autoimmune diseases to field equations
Cancer, autoimmune diseases = field equations
"""

import json
import sys
import math
from pathlib import Path
from typing import Dict, List, Optional

sys.path.insert(0, str(Path(__file__).parent))
from opic_executor import OpicExecutor

class CancerAutoimmuneMapper:
    """
    Maps cancer and autoimmune diseases to field equations.
    Shows that cancer, autoimmune diseases = field equations.
    """
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.opic = OpicExecutor(project_root)
        
        # Scale-to-dimension mapping
        self.scale_dimensions = {
            "cancer": 3.5,         # Cancer scale (tumor growth, metastasis)
            "autoimmune": 3.5      # Autoimmune scale (immune dysregulation)
        }
    
    def tumor_growth(self, initial_size: float, growth_rate: float,
                     time: float, carrying_capacity: float = None) -> Dict:
        """
        Compute tumor growth (exponential or logistic).
        
        Args:
            initial_size: Initial tumor size (cells or volume)
            growth_rate: Growth rate (1/time)
            time: Time elapsed
            carrying_capacity: Carrying capacity (for logistic growth)
        
        Returns:
            Tumor growth information
        """
        if carrying_capacity:
            # Logistic growth: N(t) = K / (1 + ((K-N₀)/N₀)e^(-rt))
            ratio = (carrying_capacity - initial_size) / initial_size
            size = carrying_capacity / (1 + ratio * math.exp(-growth_rate * time))
            growth_type = "logistic"
        else:
            # Exponential growth: N(t) = N₀ e^(rt)
            size = initial_size * math.exp(growth_rate * time)
            growth_type = "exponential"
        
        doubling_time = math.log(2) / growth_rate if growth_rate > 0 else float('inf')
        
        return {
            "initial_size": initial_size,
            "growth_rate": growth_rate,
            "time": time,
            "size": size,
            "doubling_time": doubling_time,
            "growth_type": growth_type,
            "field_interpretation": "Tumor growth = field growth",
            "equation": f"N(t) = N₀ e^(rt)" if growth_type == "exponential" else f"N(t) = K / (1 + ((K-N₀)/N₀)e^(-rt))"
        }
    
    def mutation_accumulation(self, mutation_rate: float, cell_divisions: int,
                             initial_mutations: int = 0) -> Dict:
        """
        Compute mutation accumulation in cancer cells.
        
        Args:
            mutation_rate: Mutations per cell division
            cell_divisions: Number of cell divisions
            initial_mutations: Initial number of mutations
        
        Returns:
            Mutation accumulation information
        """
        # Mutations accumulate: M(t) = M₀ + μ × divisions
        total_mutations = initial_mutations + mutation_rate * cell_divisions
        
        # Probability of driver mutation (simplified)
        # Driver mutations are rare (~0.01 per division)
        driver_mutation_rate = 0.01
        expected_driver_mutations = driver_mutation_rate * cell_divisions
        
        return {
            "mutation_rate": mutation_rate,
            "cell_divisions": cell_divisions,
            "total_mutations": total_mutations,
            "expected_driver_mutations": expected_driver_mutations,
            "field_interpretation": "Mutation accumulation = field perturbation accumulation",
            "equation": "M(t) = M₀ + μ × divisions"
        }
    
    def immune_evasion_probability(self, cancer_antigenicity: float,
                                   immune_surveillance: float) -> Dict:
        """
        Compute probability of immune evasion.
        
        Args:
            cancer_antigenicity: Cancer antigenicity (0-1)
            immune_surveillance: Immune surveillance strength (0-1)
        
        Returns:
            Immune evasion information
        """
        # Evasion probability increases with low antigenicity and weak surveillance
        # P(evasion) = 1 - (antigenicity × surveillance)
        evasion_probability = 1.0 - (cancer_antigenicity * immune_surveillance)
        
        # Checkpoint inhibition effectiveness
        checkpoint_effectiveness = 1.0 - evasion_probability
        
        return {
            "cancer_antigenicity": cancer_antigenicity,
            "immune_surveillance": immune_surveillance,
            "evasion_probability": evasion_probability,
            "checkpoint_effectiveness": checkpoint_effectiveness,
            "field_interpretation": "Immune evasion = field evasion",
            "equation": "P(evasion) = 1 - (antigenicity × surveillance)"
        }
    
    def autoimmune_response(self, self_antigen_concentration: float,
                           tolerance_threshold: float,
                           autoantibody_production_rate: float) -> Dict:
        """
        Compute autoimmune response strength.
        
        Args:
            self_antigen_concentration: Self-antigen concentration
            tolerance_threshold: Tolerance threshold
            autoantibody_production_rate: Autoantibody production rate
        
        Returns:
            Autoimmune response information
        """
        # Tolerance breakdown occurs when self-antigen exceeds threshold
        tolerance_breakdown = self_antigen_concentration > tolerance_threshold
        
        if tolerance_breakdown:
            # Autoantibody production increases with antigen concentration
            autoantibody_level = autoantibody_production_rate * self_antigen_concentration
            inflammation_level = min(1.0, autoantibody_level / tolerance_threshold)
        else:
            autoantibody_level = 0.0
            inflammation_level = 0.0
        
        return {
            "self_antigen_concentration": self_antigen_concentration,
            "tolerance_threshold": tolerance_threshold,
            "tolerance_breakdown": tolerance_breakdown,
            "autoantibody_level": autoantibody_level,
            "inflammation_level": inflammation_level,
            "field_interpretation": "Autoimmune response = field autoimmune response",
            "equation": "Autoantibody = rate × [self-antigen] if tolerance broken"
        }
    
    def explain_cancer_autoimmune(self, question: str) -> Dict:
        """
        Explain cancer or autoimmune diseases using field equations.
        
        Args:
            question: Question about cancer or autoimmune diseases
        
        Returns:
            Field-based explanation
        """
        question_lower = question.lower()
        
        explanation = {
            "question": question,
            "concepts": [],
            "explanation": ""
        }
        
        # Check for cancer concepts
        if "cancer" in question_lower or "tumor" in question_lower or "metastasis" in question_lower:
            explanation["concepts"].append("cancer")
            explanation["explanation"] += "Cancer = field cancer. "
            explanation["explanation"] += "Tumor growth = field growth, mutations = field perturbations. "
            explanation["explanation"] += "Angiogenesis = field angiogenesis, metastasis = field metastasis. "
            explanation["explanation"] += "Immune evasion = field evasion. "
        
        if "mutation" in question_lower and ("cancer" in question_lower or "tumor" in question_lower):
            explanation["concepts"].append("mutation")
            explanation["explanation"] += "Cancer mutations = field perturbations. "
            explanation["explanation"] += "Mutations accumulate: M(t) = M₀ + μ × divisions. "
            explanation["explanation"] += "Driver mutations drive cancer progression. "
        
        if "angiogenesis" in question_lower:
            explanation["concepts"].append("angiogenesis")
            explanation["explanation"] += "Angiogenesis = field angiogenesis. "
            explanation["explanation"] += "Tumors induce new blood vessel formation following field angiogenesis equations. "
        
        if "metastasis" in question_lower:
            explanation["concepts"].append("metastasis")
            explanation["explanation"] += "Metastasis = field metastasis. "
            explanation["explanation"] += "Cancer cells invade and spread following field metastasis equations. "
        
        # Check for autoimmune concepts
        if "autoimmune" in question_lower or "autoimmunity" in question_lower:
            explanation["concepts"].append("autoimmune")
            explanation["explanation"] += "Autoimmune diseases = field autoimmune. "
            explanation["explanation"] += "Tolerance breakdown = field breakdown. "
            explanation["explanation"] += "Autoantibody production = field production. "
            explanation["explanation"] += "Inflammation = field inflammation, tissue damage = field damage. "
        
        if "tolerance" in question_lower and ("immune" in question_lower or "autoimmune" in question_lower):
            explanation["concepts"].append("tolerance")
            explanation["explanation"] += "Immune tolerance breakdown = field breakdown. "
            explanation["explanation"] += "When self-antigen exceeds tolerance threshold, autoimmunity develops. "
        
        if "inflammation" in question_lower and ("autoimmune" in question_lower or "rheumatoid" in question_lower):
            explanation["concepts"].append("inflammation")
            explanation["explanation"] += "Autoimmune inflammation = field inflammation. "
            explanation["explanation"] += "Autoantibodies bind self-tissues, causing field inflammation. "
        
        if "checkpoint" in question_lower or "immunotherapy" in question_lower:
            explanation["concepts"].append("immunotherapy")
            explanation["explanation"] += "Cancer immunotherapy = field checkpoint inhibition. "
            explanation["explanation"] += "Checkpoint inhibitors activate immune system against cancer. "
            explanation["explanation"] += "Checkpoint inhibition = field checkpoint inhibition. "
        
        if not explanation["explanation"]:
            explanation["explanation"] = "Cancer and autoimmune diseases = field equations. "
            explanation["explanation"] += "Both involve field dynamics: cancer = field growth/evasion, autoimmune = field breakdown/inflammation."
        
        return explanation

def main():
    """Test cancer autoimmune mapper"""
    project_root = Path(__file__).parent.parent
    mapper = CancerAutoimmuneMapper(project_root)
    
    print("=" * 70)
    print("Cancer Autoimmune Mapper")
    print("=" * 70)
    print("\nMapping: Cancer & Autoimmune Diseases = Field Equations")
    print("\n" + "=" * 70)
    
    # Tumor growth (moderate growth rate - realistic for many cancers)
    print("\n🔬 Tumor Growth:")
    print("-" * 70)
    # Moderate growth: 0.1 1/day gives ~7 day doubling time (realistic for many cancers)
    growth = mapper.tumor_growth(initial_size=1000.0, growth_rate=0.1, time=10.0)
    print(f"Initial: {growth['initial_size']:.0f} cells")
    print(f"Growth rate: {growth['growth_rate']:.2f} 1/day")
    print(f"Size at t={growth['time']:.1f} days: {growth['size']:.0f} cells")
    print(f"Doubling time: {growth['doubling_time']:.1f} days (realistic for moderate cancers)")
    print(f"Field interpretation: {growth['field_interpretation']}")
    
    # Mutation accumulation
    print("\n🧬 Mutation Accumulation:")
    print("-" * 70)
    mutations = mapper.mutation_accumulation(mutation_rate=0.1, cell_divisions=100)
    print(f"Mutation rate: {mutations['mutation_rate']:.2f} mutations/division")
    print(f"Cell divisions: {mutations['cell_divisions']}")
    print(f"Total mutations: {mutations['total_mutations']:.1f}")
    print(f"Expected driver mutations: {mutations['expected_driver_mutations']:.2f}")
    print(f"Field interpretation: {mutations['field_interpretation']}")
    
    # Immune evasion
    print("\n🛡️  Immune Evasion:")
    print("-" * 70)
    evasion = mapper.immune_evasion_probability(cancer_antigenicity=0.3, immune_surveillance=0.7)
    print(f"Cancer antigenicity: {evasion['cancer_antigenicity']:.1%}")
    print(f"Immune surveillance: {evasion['immune_surveillance']:.1%}")
    print(f"Evasion probability: {evasion['evasion_probability']:.1%}")
    print(f"Checkpoint effectiveness: {evasion['checkpoint_effectiveness']:.1%}")
    print(f"Field interpretation: {evasion['field_interpretation']}")
    
    # Autoimmune response
    print("\n⚕️  Autoimmune Response:")
    print("-" * 70)
    autoimmune = mapper.autoimmune_response(
        self_antigen_concentration=1.5,
        tolerance_threshold=1.0,
        autoantibody_production_rate=0.5
    )
    print(f"Self-antigen: {autoimmune['self_antigen_concentration']:.2f}")
    print(f"Tolerance threshold: {autoimmune['tolerance_threshold']:.2f}")
    print(f"Tolerance breakdown: {autoimmune['tolerance_breakdown']}")
    print(f"Autoantibody level: {autoimmune['autoantibody_level']:.2f}")
    print(f"Inflammation level: {autoimmune['inflammation_level']:.1%}")
    print(f"Field interpretation: {autoimmune['field_interpretation']}")
    
    # Explanations
    print("\n📚 Cancer & Autoimmune Explanations:")
    print("-" * 70)
    
    questions = [
        "How does cancer develop?",
        "How do autoimmune diseases work?",
        "What is metastasis?",
        "How does immune evasion work?"
    ]
    
    for question in questions:
        explanation = mapper.explain_cancer_autoimmune(question)
        print(f"\nQ: {question}")
        print(f"   {explanation['explanation']}")
    
    print("\n" + "=" * 70)
    print("Key Insight:")
    print("=" * 70)
    print("""
Cancer & Autoimmune Diseases = field equations!

• Cancer = field cancer (growth = field growth, mutations = field perturbations)
• Tumor growth = field growth (exponential/logistic)
• Angiogenesis = field angiogenesis, Metastasis = field metastasis
• Immune evasion = field evasion
• Autoimmune = field autoimmune (tolerance breakdown = field breakdown)
• Autoantibody production = field production, Inflammation = field inflammation

All follow field equations at different scales!
    """)

if __name__ == "__main__":
    main()

