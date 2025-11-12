#!/usr/bin/env python3
"""
Neuroscience Consciousness Mapper — Map neuroscience and consciousness to field equations
Neural networks, brain dynamics, consciousness = field equations
"""

import json
import sys
import math
from pathlib import Path
from typing import Dict, List, Optional

sys.path.insert(0, str(Path(__file__).parent))
from opic_executor import OpicExecutor

class NeuroscienceConsciousnessMapper:
    """
    Maps neuroscience and consciousness to field equations.
    Shows that neural networks, brain dynamics, consciousness = field equations.
    """
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.opic = OpicExecutor(project_root)
        
        # Scale-to-dimension mapping
        self.scale_dimensions = {
            "neural": 3.5,         # Neural scale (neurons, synapses)
            "network": 4.0,        # Network scale (neural networks)
            "cognitive": 4.5,      # Cognitive scale (memory, attention)
            "consciousness": 5.0   # Consciousness scale (D≥5 from Field Spec)
        }
        
        # Neuroscience concept → field equation mappings
        self.neuroscience_field_map = {
            # Neurons
            "neuron": {
                "field_type": "unit",
                "scale": "neural",
                "dimension": 3.5,
                "equation": "neuron = field.unit(membrane_potential, threshold, synapses)",
                "description": "Neuron = field unit"
            },
            "action_potential": {
                "field_type": "spike",
                "scale": "neural",
                "dimension": 3.5,
                "equation": "spike = field.spike(membrane_potential, threshold)",
                "description": "Action potential = field spike"
            },
            "synapse": {
                "field_type": "connection",
                "scale": "neural",
                "dimension": 3.5,
                "equation": "transmission = field.transmit(presynaptic, neurotransmitter, postsynaptic)",
                "description": "Synaptic transmission = field transmission"
            },
            
            # Neural Networks
            "neural_network": {
                "field_type": "network",
                "scale": "network",
                "dimension": 4.0,
                "equation": "network = field.network(neurons, connections, weights)",
                "description": "Neural network = field network"
            },
            "activation": {
                "field_type": "activation",
                "scale": "network",
                "dimension": 4.0,
                "equation": "activation = field.activate(input, weights, bias)",
                "description": "Neural activation = field activation"
            },
            "learning": {
                "field_type": "learning",
                "scale": "network",
                "dimension": 4.0,
                "equation": "weight_update = field.update(error, weights)",
                "description": "Neural learning = field learning"
            },
            
            # Consciousness
            "consciousness": {
                "field_type": "consciousness",
                "scale": "consciousness",
                "dimension": 5.0,
                "equation": "consciousness = field.consciousness(integrated_information, awareness, self_model)",
                "description": "Consciousness = field consciousness (requires D≥5)"
            },
            "integrated_information": {
                "field_type": "integration",
                "scale": "consciousness",
                "dimension": 5.0,
                "equation": "Φ = field.integrate(neural_activity)",
                "description": "Integrated information = field integration"
            },
            "awareness": {
                "field_type": "awareness",
                "scale": "consciousness",
                "dimension": 5.0,
                "equation": "awareness = field.awareness(integrated_information)",
                "description": "Awareness = field awareness"
            },
            
            # Cognitive Processes
            "memory": {
                "field_type": "memory",
                "scale": "cognitive",
                "dimension": 4.5,
                "equation": "memory = field.store(experience, neural_network)",
                "description": "Memory = field memory"
            },
            "attention": {
                "field_type": "attention",
                "scale": "cognitive",
                "dimension": 4.5,
                "equation": "attended = field.attend(input, attention_weights)",
                "description": "Attention = field attention"
            },
            "decision": {
                "field_type": "decision",
                "scale": "cognitive",
                "dimension": 4.5,
                "equation": "decision = field.decide(options, values)",
                "description": "Decision making = field decision"
            }
        }
    
    def map_neuroscience_to_field(self, concept: str) -> Dict:
        """
        Map a neuroscience concept to field equations.
        
        Args:
            concept: Neuroscience concept
        
        Returns:
            Field equation mapping
        """
        concept_lower = concept.lower().replace(" ", "_")
        
        # Direct lookup
        if concept_lower in self.neuroscience_field_map:
            return self.neuroscience_field_map[concept_lower]
        
        # Fuzzy matching
        for key, mapping in self.neuroscience_field_map.items():
            if key in concept_lower or concept_lower in key:
                return mapping
        
        # Default
        return {
            "field_type": "neural",
            "scale": "neural",
            "dimension": 3.5,
            "equation": "F = k(q₁q₂)/R^D",
            "description": f"{concept} = neural field (same equations, different scale)"
        }
    
    def neural_activation(self, input_sum: float, threshold: float = 0.0) -> Dict:
        """
        Compute neural activation (sigmoid activation).
        
        Args:
            input_sum: Sum of weighted inputs
            threshold: Activation threshold
        
        Returns:
            Neural activation information
        """
        # Sigmoid activation: σ(x) = 1/(1+e^(-x))
        activation = 1.0 / (1.0 + math.exp(-(input_sum - threshold)))
        
        return {
            "input_sum": input_sum,
            "threshold": threshold,
            "activation": activation,
            "field_interpretation": "Neural activation = field activation",
            "equation": "σ(x) = 1/(1+e^(-x))"
        }
    
    def integrated_information(self, neural_activity: List[float]) -> Dict:
        """
        Estimate integrated information (simplified Φ).
        
        Args:
            neural_activity: List of neural activity values
        
        Returns:
            Integrated information
        """
        if not neural_activity:
            return {"phi": 0.0, "field_interpretation": "No activity"}
        
        # Simplified: Φ ≈ variance of activity (measures integration)
        mean_activity = sum(neural_activity) / len(neural_activity)
        variance = sum((x - mean_activity)**2 for x in neural_activity) / len(neural_activity)
        
        # Φ increases with integration (higher variance = more integration)
        phi = math.sqrt(variance) if variance > 0 else 0.0
        
        return {
            "neural_activity": neural_activity,
            "phi": phi,
            "field_interpretation": "Integrated information = field integration",
            "equation": "Φ ≈ field.integrate(neural_activity)",
            "dimension": 5.0  # Consciousness requires D≥5
        }
    
    def explain_neuroscience(self, question: str) -> Dict:
        """
        Explain neuroscience using field equations.
        
        Args:
            question: Question about neuroscience or consciousness
        
        Returns:
            Field-based explanation
        """
        question_lower = question.lower()
        
        explanation = {
            "question": question,
            "concepts": [],
            "explanation": ""
        }
        
        # Check for neural concepts
        if "neuron" in question_lower or "action potential" in question_lower or "firing" in question_lower:
            explanation["concepts"].append("neuron")
            explanation["explanation"] += "Neurons = field units. "
            explanation["explanation"] += "Action potential = field spike, follows field spike equations. "
            explanation["explanation"] += "Membrane potential = field potential, threshold = field threshold. "
        
        if "synapse" in question_lower or "synaptic" in question_lower:
            explanation["concepts"].append("synapse")
            explanation["explanation"] += "Synapses = field connections. "
            explanation["explanation"] += "Synaptic transmission = field transmission. "
            explanation["explanation"] += "Neurotransmitters = field propagators. "
        
        if "neural network" in question_lower or "neural" in question_lower:
            explanation["concepts"].append("neural_network")
            explanation["explanation"] += "Neural networks = field networks. "
            explanation["explanation"] += "Neural activation = field activation: σ(x) = 1/(1+e^(-x)). "
            explanation["explanation"] += "Neural learning = field learning, weight updates follow field update equations. "
        
        if "consciousness" in question_lower or "awareness" in question_lower:
            explanation["concepts"].append("consciousness")
            explanation["explanation"] += "Consciousness = field consciousness. "
            explanation["explanation"] += "Requires dimension D≥5 (from Field Spec §8.10). "
            explanation["explanation"] += "Integrated information Φ = field integration. "
            explanation["explanation"] += "Awareness = field awareness, self-model = field self-model. "
        
        if "memory" in question_lower:
            explanation["concepts"].append("memory")
            explanation["explanation"] += "Memory = field memory. "
            explanation["explanation"] += "Storage = field.store, retrieval = field.retrieve. "
            explanation["explanation"] += "Follows field memory equations. "
        
        if "attention" in question_lower:
            explanation["concepts"].append("attention")
            explanation["explanation"] += "Attention = field attention. "
            explanation["explanation"] += "Attended input = field.attend(input, attention_weights). "
            explanation["explanation"] += "Follows field attention equations. "
        
        if not explanation["explanation"]:
            explanation["explanation"] = "Neuroscience = neural field dynamics. "
            explanation["explanation"] += "Neural networks, brain dynamics, and consciousness all follow field equations."
        
        return explanation

def main():
    """Test neuroscience consciousness mapper"""
    project_root = Path(__file__).parent.parent
    mapper = NeuroscienceConsciousnessMapper(project_root)
    
    print("=" * 70)
    print("Neuroscience Consciousness Mapper")
    print("=" * 70)
    print("\nMapping: Neuroscience = Neural Field Dynamics")
    print("\n" + "=" * 70)
    
    # Neural activation
    print("\n🧠 Neural Activation:")
    print("-" * 70)
    activation = mapper.neural_activation(input_sum=2.0, threshold=0.0)
    print(f"Input sum: {activation['input_sum']:.1f}")
    print(f"Activation: {activation['activation']:.3f}")
    print(f"Field interpretation: {activation['field_interpretation']}")
    print(f"Equation: {activation['equation']}")
    
    # Integrated information
    print("\n💭 Integrated Information:")
    print("-" * 70)
    phi = mapper.integrated_information([0.1, 0.3, 0.5, 0.7, 0.9])
    print(f"Neural activity: {phi['neural_activity']}")
    print(f"Φ (integrated information): {phi['phi']:.3f}")
    print(f"Dimension: {phi['dimension']:.1f} (consciousness requires D≥5)")
    print(f"Field interpretation: {phi['field_interpretation']}")
    
    # Concept mappings
    print("\n📚 Neuroscience Concepts:")
    print("-" * 70)
    concepts = ["neuron", "neural network", "consciousness", "memory"]
    for concept in concepts:
        mapping = mapper.map_neuroscience_to_field(concept)
        print(f"\n{concept}:")
        print(f"  Field type: {mapping['field_type']}")
        print(f"  Scale: {mapping['scale']}, Dimension: {mapping['dimension']}")
        print(f"  Description: {mapping['description']}")
        print(f"  Equation: {mapping['equation']}")
    
    # Explanations
    print("\n📚 Neuroscience Explanations:")
    print("-" * 70)
    
    questions = [
        "How do neurons fire?",
        "What is consciousness?",
        "How does memory work?",
        "How do neural networks learn?"
    ]
    
    for question in questions:
        explanation = mapper.explain_neuroscience(question)
        print(f"\nQ: {question}")
        print(f"   {explanation['explanation']}")
    
    print("\n" + "=" * 70)
    print("Key Insight:")
    print("=" * 70)
    print("""
Neuroscience = neural field dynamics!

• Neurons = field units (membrane potential = field potential)
• Action potential = field spike (threshold = field threshold)
• Neural networks = field networks (activation = field activation)
• Consciousness = field consciousness (requires D≥5, integrated information Φ)
• Memory = field memory (storage = field.store, retrieval = field.retrieve)
• Attention = field attention (attended = field.attend)

All neuroscience follows field equations!
    """)

if __name__ == "__main__":
    main()

