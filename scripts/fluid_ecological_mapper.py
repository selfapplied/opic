#!/usr/bin/env python3
"""
Fluid Ecological Mapper — Map jetstreams, algal blooms, viruses to field equations
Atmospheric flow, population dynamics, viral propagation = field equations
"""

import json
import sys
import math
from pathlib import Path
from typing import Dict, List, Optional

sys.path.insert(0, str(Path(__file__).parent))
from opic_executor import OpicExecutor

class FluidEcologicalMapper:
    """
    Maps jetstreams, algal blooms, and viruses to field equations.
    Shows that atmospheric flow, population dynamics, viral propagation = field equations.
    """
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.opic = OpicExecutor(project_root)
        
        # Scale-to-dimension mapping
        self.scale_dimensions = {
            "atmospheric": 2.5,    # Jetstreams (fluid dynamics)
            "ecological": 2.5,     # Algal blooms (population dynamics)
            "molecular": 2.5       # Viruses (molecular scale)
        }
    
    def jetstream_flow(self, pressure_gradient: float, coriolis: float = 1.0) -> Dict:
        """
        Compute jetstream flow from pressure gradient.
        
        Args:
            pressure_gradient: Pressure gradient (Pa/m)
            coriolis: Coriolis parameter (1/s)
        
        Returns:
            Jetstream flow information
        """
        # Geostrophic balance: fV = (1/ρ) ∂p/∂x
        # For typical values: ρ ≈ 1.2 kg/m³, f ≈ 10⁻⁴ s⁻¹
        rho = 1.2  # Air density (kg/m³)
        velocity = pressure_gradient / (coriolis * rho)  # Geostrophic velocity
        
        return {
            "pressure_gradient": pressure_gradient,
            "coriolis": coriolis,
            "velocity": velocity,
            "field_interpretation": "Jetstream flow = atmospheric field flow",
            "equation": "V ∝ (1/f) ∂p/∂x",
            "scale": "atmospheric",
            "dimension": 2.5
        }
    
    def algal_bloom_growth(self, initial_population: float, growth_rate: float,
                          carrying_capacity: float, time: float) -> Dict:
        """
        Compute algal bloom growth using logistic model.
        
        Args:
            initial_population: Initial population density
            growth_rate: Growth rate (1/time)
            carrying_capacity: Carrying capacity
            time: Time elapsed
        
        Returns:
            Population growth information
        """
        # Logistic growth: N(t) = K / (1 + ((K-N₀)/N₀)e^(-rt))
        if initial_population > 0:
            ratio = (carrying_capacity - initial_population) / initial_population
            population = carrying_capacity / (1 + ratio * math.exp(-growth_rate * time))
        else:
            population = 0.0
        
        # Growth rate
        growth = population - initial_population
        
        return {
            "initial_population": initial_population,
            "growth_rate": growth_rate,
            "carrying_capacity": carrying_capacity,
            "time": time,
            "population": population,
            "growth": growth,
            "field_interpretation": "Algal bloom growth = population field growth",
            "equation": "N(t) = K / (1 + ((K-N₀)/N₀)e^(-rt))",
            "scale": "ecological",
            "dimension": 2.5
        }
    
    def viral_propagation(self, initial_infected: float, transmission_rate: float,
                         recovery_rate: float, time: float) -> Dict:
        """
        Compute viral propagation using SIR model.
        
        Args:
            initial_infected: Initial infected population
            transmission_rate: Transmission rate β
            recovery_rate: Recovery rate γ
            time: Time elapsed
        
        Returns:
            Viral propagation information
        """
        # Simplified SIR: I(t) ≈ I₀ e^((β-γ)t) for early stages
        if recovery_rate > 0:
            effective_rate = transmission_rate - recovery_rate
            infected = initial_infected * math.exp(effective_rate * time)
        else:
            infected = initial_infected * math.exp(transmission_rate * time)
        
        # Basic reproduction number
        R0 = transmission_rate / recovery_rate if recovery_rate > 0 else float('inf')
        
        return {
            "initial_infected": initial_infected,
            "transmission_rate": transmission_rate,
            "recovery_rate": recovery_rate,
            "time": time,
            "infected": infected,
            "R0": R0,
            "field_interpretation": "Viral propagation = molecular field propagation",
            "equation": "I(t) ≈ I₀ e^((β-γ)t)",
            "scale": "molecular",
            "dimension": 2.5
        }
    
    def explain_complex_system(self, question: str) -> Dict:
        """
        Explain complex system using field equations.
        
        Args:
            question: Question about jetstreams, algal blooms, or viruses
        
        Returns:
            Field-based explanation
        """
        question_lower = question.lower()
        
        explanation = {
            "question": question,
            "concepts": [],
            "explanation": ""
        }
        
        # Check for jetstream concepts
        if "jetstream" in question_lower or "atmospheric" in question_lower:
            explanation["concepts"].append("jetstream")
            explanation["explanation"] += "Jetstreams = atmospheric field flow. "
            explanation["explanation"] += "Pressure gradients create field flow, Coriolis effect creates rotation. "
            explanation["explanation"] += "Follows fluid dynamics field equations. "
        
        # Check for algal bloom concepts
        if "algal bloom" in question_lower or "bloom" in question_lower:
            explanation["concepts"].append("algal_bloom")
            explanation["explanation"] += "Algal blooms = population field dynamics. "
            explanation["explanation"] += "Population growth follows logistic field growth: N(t) = K/(1+((K-N₀)/N₀)e^(-rt)). "
            explanation["explanation"] += "Nutrients act as field sources, predators as field sinks. "
        
        # Check for virus concepts
        if "virus" in question_lower or "viral" in question_lower:
            explanation["concepts"].append("virus")
            explanation["explanation"] += "Viruses = molecular field propagators. "
            explanation["explanation"] += "Viral infection = field coupling, replication = field replication. "
            explanation["explanation"] += "Propagation follows field propagation equations. "
        
        if not explanation["explanation"]:
            explanation["explanation"] = "Complex systems follow field equations. "
            explanation["explanation"] += "Jetstreams, algal blooms, and viruses all follow dimensional Coulomb law at different scales."
        
        return explanation

def main():
    """Test fluid ecological mapper"""
    project_root = Path(__file__).parent.parent
    mapper = FluidEcologicalMapper(project_root)
    
    print("=" * 70)
    print("Fluid Ecological Mapper")
    print("=" * 70)
    print("\nMapping: Jetstreams, Algal Blooms, Viruses = Field Equations")
    print("\n" + "=" * 70)
    
    # Jetstream flow
    print("\n🌪️  Jetstream Flow:")
    print("-" * 70)
    jetstream = mapper.jetstream_flow(pressure_gradient=100.0, coriolis=1.0e-4)
    print(f"Pressure gradient: {jetstream['pressure_gradient']} Pa/m")
    print(f"Velocity: {jetstream['velocity']:.2f} m/s")
    print(f"Field interpretation: {jetstream['field_interpretation']}")
    print(f"Equation: {jetstream['equation']}")
    
    # Algal bloom growth
    print("\n🌊 Algal Bloom Growth:")
    print("-" * 70)
    bloom = mapper.algal_bloom_growth(
        initial_population=100.0,
        growth_rate=0.1,
        carrying_capacity=10000.0,
        time=10.0
    )
    print(f"Initial population: {bloom['initial_population']:.1f}")
    print(f"Population at t={bloom['time']:.1f}: {bloom['population']:.1f}")
    print(f"Growth: {bloom['growth']:.1f}")
    print(f"Field interpretation: {bloom['field_interpretation']}")
    print(f"Equation: {bloom['equation']}")
    
    # Viral propagation
    print("\n🦠 Viral Propagation:")
    print("-" * 70)
    virus = mapper.viral_propagation(
        initial_infected=10.0,
        transmission_rate=0.3,
        recovery_rate=0.1,
        time=5.0
    )
    print(f"Initial infected: {virus['initial_infected']:.1f}")
    print(f"Infected at t={virus['time']:.1f}: {virus['infected']:.1f}")
    print(f"R₀ (basic reproduction number): {virus['R0']:.2f}")
    print(f"Field interpretation: {virus['field_interpretation']}")
    print(f"Equation: {virus['equation']}")
    
    # Explanations
    print("\n📚 Complex Systems Explanations:")
    print("-" * 70)
    
    questions = [
        "How do jetstreams form?",
        "What causes algal blooms?",
        "How do viruses spread?"
    ]
    
    for question in questions:
        explanation = mapper.explain_complex_system(question)
        print(f"\nQ: {question}")
        print(f"   {explanation['explanation']}")
    
    print("\n" + "=" * 70)
    print("Key Insight:")
    print("=" * 70)
    print("""
Complex systems = field equations!

• Jetstreams = atmospheric field flow (pressure gradients → flow)
• Algal blooms = population field dynamics (logistic growth)
• Viruses = molecular field propagators (infection → propagation)

All follow: F = k(q₁q₂)/R^D
Same equations, different scales!
    """)

if __name__ == "__main__":
    main()

