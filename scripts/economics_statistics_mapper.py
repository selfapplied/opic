#!/usr/bin/env python3
"""
Economics Statistics Mapper — Map economics and statistics to field equations
Markets, prices, distributions, probabilities = field equations
"""

import json
import sys
import math
from pathlib import Path
from typing import Dict, List, Optional

sys.path.insert(0, str(Path(__file__).parent))
from opic_executor import OpicExecutor

class EconomicsStatisticsMapper:
    """
    Maps economics and statistics to field equations.
    Shows that markets, prices, distributions, probabilities = field equations.
    """
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.opic = OpicExecutor(project_root)
        
        # Scale-to-dimension mapping
        self.scale_dimensions = {
            "market": 2.5,         # Market scale (supply/demand)
            "statistical": 2.5,    # Statistical scale (distributions)
            "economic": 3.0        # Economic scale (systems)
        }
        
        # Economics concept → field equation mappings
        self.economics_field_map = {
            "supply": {
                "field_type": "source",
                "scale": "market",
                "dimension": 2.5,
                "equation": "supply = field.source(price, cost)",
                "description": "Supply = field source"
            },
            "demand": {
                "field_type": "sink",
                "scale": "market",
                "dimension": 2.5,
                "equation": "demand = field.sink(price, utility)",
                "description": "Demand = field sink"
            },
            "price": {
                "field_type": "potential",
                "scale": "market",
                "dimension": 2.5,
                "equation": "price = field.potential(supply, demand)",
                "description": "Price = field potential"
            },
            "equilibrium": {
                "field_type": "equilibrium",
                "scale": "market",
                "dimension": 2.5,
                "equation": "equilibrium = field.equilibrium(supply, demand)",
                "description": "Market equilibrium = field equilibrium"
            }
        }
        
        # Statistics concept → field equation mappings
        self.statistics_field_map = {
            "probability": {
                "field_type": "probability",
                "scale": "statistical",
                "dimension": 2.5,
                "equation": "P(event) = field.probability(event, sample_space)",
                "description": "Probability = field probability"
            },
            "distribution": {
                "field_type": "distribution",
                "scale": "statistical",
                "dimension": 2.5,
                "equation": "distribution = field.distribution(values, probabilities)",
                "description": "Probability distribution = field distribution"
            },
            "mean": {
                "field_type": "center",
                "scale": "statistical",
                "dimension": 2.5,
                "equation": "mean = field.center(distribution)",
                "description": "Mean = field center"
            },
            "variance": {
                "field_type": "spread",
                "scale": "statistical",
                "dimension": 2.5,
                "equation": "variance = field.variance(distribution)",
                "description": "Variance = field spread"
            },
            "correlation": {
                "field_type": "correlation",
                "scale": "statistical",
                "dimension": 2.5,
                "equation": "correlation = field.correlate(variable1, variable2)",
                "description": "Correlation = field correlation"
            }
        }
    
    def market_equilibrium(self, supply_slope: float, demand_slope: float,
                          supply_intercept: float, demand_intercept: float) -> Dict:
        """
        Compute market equilibrium from supply and demand curves.
        
        Args:
            supply_slope: Slope of supply curve
            demand_slope: Slope of demand curve (negative)
            supply_intercept: Supply curve intercept
            demand_intercept: Demand curve intercept
        
        Returns:
            Market equilibrium information
        """
        # Equilibrium: supply = demand
        # Supply: Q = a + bP, Demand: Q = c + dP (d < 0)
        # Equilibrium: a + bP = c + dP → P = (c - a)/(b - d)
        equilibrium_price = (demand_intercept - supply_intercept) / (supply_slope - demand_slope)
        equilibrium_quantity = supply_slope * equilibrium_price + supply_intercept
        
        return {
            "supply_slope": supply_slope,
            "supply_intercept": supply_intercept,
            "demand_slope": demand_slope,
            "demand_intercept": demand_intercept,
            "equilibrium_price": equilibrium_price,
            "equilibrium_quantity": equilibrium_quantity,
            "field_interpretation": "Market equilibrium = field equilibrium",
            "equation": "equilibrium = field.equilibrium(supply, demand)"
        }
    
    def normal_distribution(self, mean: float, variance: float, x: float) -> Dict:
        """
        Compute normal distribution probability density.
        
        Args:
            mean: Mean of distribution
            variance: Variance of distribution
            x: Value to evaluate
        
        Returns:
            Normal distribution information
        """
        # Normal PDF: f(x) = (1/√(2πσ²)) e^(-(x-μ)²/(2σ²))
        std_dev = math.sqrt(variance)
        coefficient = 1.0 / (std_dev * math.sqrt(2 * math.pi))
        exponent = -((x - mean)**2) / (2 * variance)
        pdf = coefficient * math.exp(exponent)
        
        return {
            "mean": mean,
            "variance": variance,
            "std_dev": std_dev,
            "x": x,
            "pdf": pdf,
            "field_interpretation": "Normal distribution = field normal distribution",
            "equation": "f(x) = (1/√(2πσ²)) e^(-(x-μ)²/(2σ²))"
        }
    
    def correlation(self, x_values: List[float], y_values: List[float]) -> Dict:
        """
        Compute correlation coefficient.
        
        Args:
            x_values: X variable values
            y_values: Y variable values
        
        Returns:
            Correlation information
        """
        if len(x_values) != len(y_values) or len(x_values) == 0:
            return {"correlation": 0.0, "field_interpretation": "Invalid data"}
        
        n = len(x_values)
        
        # Compute means
        mean_x = sum(x_values) / n
        mean_y = sum(y_values) / n
        
        # Compute covariance and variances
        covariance = sum((x_values[i] - mean_x) * (y_values[i] - mean_y) for i in range(n)) / n
        var_x = sum((x - mean_x)**2 for x in x_values) / n
        var_y = sum((y - mean_y)**2 for y in y_values) / n
        
        # Correlation: r = cov(X,Y) / (σ_X σ_Y)
        if var_x > 0 and var_y > 0:
            correlation = covariance / math.sqrt(var_x * var_y)
        else:
            correlation = 0.0
        
        return {
            "covariance": covariance,
            "correlation": correlation,
            "field_interpretation": "Correlation = field correlation",
            "equation": "r = cov(X,Y) / (σ_X σ_Y)"
        }
    
    def explain_economics_statistics(self, question: str) -> Dict:
        """
        Explain economics or statistics using field equations.
        
        Args:
            question: Question about economics or statistics
        
        Returns:
            Field-based explanation
        """
        question_lower = question.lower()
        
        explanation = {
            "question": question,
            "concepts": [],
            "explanation": ""
        }
        
        # Check for economics concepts
        if "supply" in question_lower and "demand" in question_lower:
            explanation["concepts"].append("market")
            explanation["explanation"] += "Supply and demand = field supply and demand. "
            explanation["explanation"] += "Supply = field source, demand = field sink. "
            explanation["explanation"] += "Market equilibrium = field equilibrium, price = field potential. "
        
        if "market" in question_lower or "price" in question_lower:
            explanation["concepts"].append("market")
            explanation["explanation"] += "Markets = field markets. "
            explanation["explanation"] += "Price = field potential, market dynamics = field dynamics. "
            explanation["explanation"] += "Follows field market equations. "
        
        # Check for statistics concepts
        if "probability" in question_lower or "distribution" in question_lower:
            explanation["concepts"].append("probability")
            explanation["explanation"] += "Probability = field probability. "
            explanation["explanation"] += "Probability distributions = field distributions. "
            explanation["explanation"] += "Normal distribution = field normal distribution. "
        
        if "correlation" in question_lower:
            explanation["concepts"].append("correlation")
            explanation["explanation"] += "Correlation = field correlation. "
            explanation["explanation"] += "Measures field relationships between variables. "
            explanation["explanation"] += "r = cov(X,Y) / (σ_X σ_Y). "
        
        if "mean" in question_lower or "average" in question_lower:
            explanation["concepts"].append("mean")
            explanation["explanation"] += "Mean = field center. "
            explanation["explanation"] += "Average value = field center of distribution. "
        
        if "variance" in question_lower or "standard deviation" in question_lower:
            explanation["concepts"].append("variance")
            explanation["explanation"] += "Variance = field spread. "
            explanation["explanation"] += "Measures field spread of distribution. "
        
        if not explanation["explanation"]:
            explanation["explanation"] = "Economics and statistics = field dynamics. "
            explanation["explanation"] += "Markets, prices, distributions, and probabilities all follow field equations."
        
        return explanation

def main():
    """Test economics statistics mapper"""
    project_root = Path(__file__).parent.parent
    mapper = EconomicsStatisticsMapper(project_root)
    
    print("=" * 70)
    print("Economics Statistics Mapper")
    print("=" * 70)
    print("\nMapping: Economics & Statistics = Field Dynamics")
    print("\n" + "=" * 70)
    
    # Market equilibrium
    print("\n💰 Market Equilibrium:")
    print("-" * 70)
    equilibrium = mapper.market_equilibrium(
        supply_slope=2.0,
        demand_slope=-1.0,
        supply_intercept=0.0,
        demand_intercept=100.0
    )
    print(f"Supply: Q = {equilibrium['supply_slope']:.1f}P")
    print(f"Demand: Q = {equilibrium['demand_intercept']:.0f} + {equilibrium['demand_slope']:.1f}P")
    print(f"Equilibrium price: {equilibrium['equilibrium_price']:.2f}")
    print(f"Equilibrium quantity: {equilibrium['equilibrium_quantity']:.2f}")
    print(f"Field interpretation: {equilibrium['field_interpretation']}")
    
    # Normal distribution
    print("\n📊 Normal Distribution:")
    print("-" * 70)
    normal = mapper.normal_distribution(mean=0.0, variance=1.0, x=1.0)
    print(f"Mean: {normal['mean']:.1f}, Variance: {normal['variance']:.1f}")
    print(f"PDF at x={normal['x']:.1f}: {normal['pdf']:.4f}")
    print(f"Field interpretation: {normal['field_interpretation']}")
    
    # Correlation
    print("\n📈 Correlation:")
    print("-" * 70)
    x_vals = [1, 2, 3, 4, 5]
    y_vals = [2, 4, 6, 8, 10]  # Perfect positive correlation
    corr = mapper.correlation(x_vals, y_vals)
    print(f"X: {x_vals}")
    print(f"Y: {y_vals}")
    print(f"Correlation: {corr['correlation']:.3f}")
    print(f"Covariance: {corr['covariance']:.2f}")
    print(f"Field interpretation: {corr['field_interpretation']}")
    
    # Explanations
    print("\n📚 Economics & Statistics Explanations:")
    print("-" * 70)
    
    questions = [
        "How do markets work?",
        "What is probability?",
        "What is correlation?",
        "How do supply and demand determine price?"
    ]
    
    for question in questions:
        explanation = mapper.explain_economics_statistics(question)
        print(f"\nQ: {question}")
        print(f"   {explanation['explanation']}")
    
    print("\n" + "=" * 70)
    print("Key Insight:")
    print("=" * 70)
    print("""
Economics & Statistics = field dynamics!

• Supply = field source, Demand = field sink
• Price = field potential, Market equilibrium = field equilibrium
• Probability = field probability, Distributions = field distributions
• Mean = field center, Variance = field spread
• Correlation = field correlation (measures field relationships)

All economics and statistics follow field equations!
    """)

if __name__ == "__main__":
    main()

