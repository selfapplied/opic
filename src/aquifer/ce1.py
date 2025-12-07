"""
CE1: Compositional Expression Language Level 1

CE1 is a bracket-based expression language that provides a universal calculus
for singularity-balanced functions. It uses four types of brackets to encode
different semantic layers:

- () : Morphism (height 1) - transformations and rotational dynamics
- <> : Fixed-point witness (height 0) - resolve equilibria
- {} : Boundary (height 0) - domain constraints and collapse
- [] : Memory (height 0) - LR sequencing and accumulation

The CE1 system provides:
1. Height-based type system for bracket nesting
2. Fixed-point resolution semantics via <E>
3. Compositional evaluation rules
4. Integration with harmonic operators

This module implements the CE1 grammar, evaluation semantics, and provides
the foundation for expressing harmonic operators like ℋ(x) as CE1 expressions.
"""

from typing import Any, Union, List, Dict, Tuple, Optional, Callable
from dataclasses import dataclass
from enum import Enum
import math
import cmath


class BracketType(Enum):
    """Types of brackets in CE1 with their semantic meanings."""
    MORPHISM = "morphism"      # () - height 1, transformations
    WITNESS = "witness"        # <> - height 0, fixed-point resolver
    BOUNDARY = "boundary"      # {} - height 0, domain/collapse
    MEMORY = "memory"          # [] - height 0, LR sequencing


@dataclass
class CE1Expression:
    """
    A CE1 expression with bracket type, content, and height.
    
    Attributes:
        bracket_type: The type of bracket enclosing this expression
        content: The expression content (can be nested CE1Expression, constant, or symbol)
        height: Semantic height (0 for constants/witnesses, 1 for morphisms)
    """
    bracket_type: BracketType
    content: Any
    height: int = 0
    
    def __repr__(self):
        return f"CE1({self.bracket_type.value}, height={self.height})"


class CE1Parser:
    """Parser for CE1 expressions."""
    
    @staticmethod
    def parse(expr_str: str) -> CE1Expression:
        """
        Parse a CE1 expression string into a CE1Expression tree.
        
        Args:
            expr_str: String representation of CE1 expression
            
        Returns:
            Parsed CE1Expression
            
        Example:
            >>> parse("< (H c) >")
            CE1Expression with witness bracket containing morphism
        """
        # Simplified parser - full implementation would handle nested brackets
        expr_str = expr_str.strip()
        
        # Detect bracket type
        if expr_str.startswith('<') and expr_str.endswith('>'):
            bracket_type = BracketType.WITNESS
            inner = expr_str[1:-1].strip()
        elif expr_str.startswith('(') and expr_str.endswith(')'):
            bracket_type = BracketType.MORPHISM
            inner = expr_str[1:-1].strip()
        elif expr_str.startswith('{') and expr_str.endswith('}'):
            bracket_type = BracketType.BOUNDARY
            inner = expr_str[1:-1].strip()
        elif expr_str.startswith('[') and expr_str.endswith(']'):
            bracket_type = BracketType.MEMORY
            inner = expr_str[1:-1].strip()
        else:
            # Constant or symbol
            return CE1Expression(
                bracket_type=BracketType.WITNESS,  # Default to witness for constants
                content=expr_str,
                height=0
            )
        
        # Determine height
        height = 1 if bracket_type == BracketType.MORPHISM else 0
        
        # Parse inner content (recursive)
        if inner and any(c in inner for c in '()<>[]{}'):
            content = CE1Parser.parse(inner)
        else:
            content = inner
        
        return CE1Expression(
            bracket_type=bracket_type,
            content=content,
            height=height
        )


class CE1Evaluator:
    """
    Evaluator for CE1 expressions with fixed-point semantics.
    
    The evaluator implements:
    - Fixed-point resolution for <E> expressions
    - Morphism application for (f x) expressions
    - Boundary constraint evaluation for {E} expressions
    - Memory sequencing for [E] expressions
    """
    
    def __init__(self):
        self.operators: Dict[str, Callable] = {}
        self.max_iterations = 100
        self.tolerance = 1e-10
    
    def register_operator(self, name: str, func: Callable):
        """Register a named operator (morphism) for evaluation."""
        self.operators[name] = func
    
    def evaluate(self, expr: Union[CE1Expression, str], context: Dict[str, Any] = None) -> Any:
        """
        Evaluate a CE1 expression.
        
        Args:
            expr: CE1Expression or string to evaluate
            context: Variable bindings and operator definitions
            
        Returns:
            Evaluated result
        """
        if context is None:
            context = {}
        
        # Parse if string
        if isinstance(expr, str):
            expr = CE1Parser.parse(expr)
        
        # If content is a simple value, return it
        if not isinstance(expr, CE1Expression):
            return expr
        
        # Handle different bracket types
        if expr.bracket_type == BracketType.WITNESS:
            # <E> - resolve fixed point
            return self._evaluate_witness(expr, context)
        elif expr.bracket_type == BracketType.MORPHISM:
            # (f x) - apply morphism
            return self._evaluate_morphism(expr, context)
        elif expr.bracket_type == BracketType.BOUNDARY:
            # {E} - evaluate with boundary constraints
            return self._evaluate_boundary(expr, context)
        elif expr.bracket_type == BracketType.MEMORY:
            # [E] - evaluate with LR sequencing
            return self._evaluate_memory(expr, context)
        
        return expr.content
    
    def _evaluate_witness(self, expr: CE1Expression, context: Dict[str, Any]) -> Any:
        """
        Evaluate witness bracket: <E> resolves to fixed point.
        
        For <f(x)>, find x such that f(x) = 0 (root) or f(x) = x (fixed point).
        """
        content = expr.content
        
        # If content is a morphism, find its fixed point
        if isinstance(content, CE1Expression) and content.bracket_type == BracketType.MORPHISM:
            return self._find_fixed_point(content, context)
        
        # Otherwise, evaluate content directly
        return self.evaluate(content, context)
    
    def _evaluate_morphism(self, expr: CE1Expression, context: Dict[str, Any]) -> Any:
        """
        Evaluate morphism bracket: (f x) applies f to x.
        """
        content = str(expr.content).strip()
        
        # Parse "operator argument" pattern
        parts = content.split(None, 1)
        if len(parts) == 2:
            op_name, arg_str = parts
            
            # Look up operator
            if op_name in self.operators:
                # Evaluate argument
                arg = self.evaluate(arg_str, context)
                # Apply operator
                return self.operators[op_name](arg)
            elif op_name in context:
                func = context[op_name]
                arg = self.evaluate(arg_str, context)
                return func(arg)
        
        return content
    
    def _evaluate_boundary(self, expr: CE1Expression, context: Dict[str, Any]) -> Any:
        """
        Evaluate boundary bracket: {E} enforces domain constraints.
        """
        # For now, simply evaluate content with boundary awareness
        return self.evaluate(expr.content, context)
    
    def _evaluate_memory(self, expr: CE1Expression, context: Dict[str, Any]) -> Any:
        """
        Evaluate memory bracket: [E] uses LR sequencing.
        """
        # For now, simply evaluate content
        return self.evaluate(expr.content, context)
    
    def _find_fixed_point(self, morphism_expr: CE1Expression, context: Dict[str, Any], 
                         initial_guess: complex = 0.5) -> complex:
        """
        Find fixed point of a morphism using iterative method.
        
        For morphism f, find x such that f(x) = 0.
        Uses Newton-Raphson-like iteration.
        """
        x = initial_guess
        
        for i in range(self.max_iterations):
            # Evaluate f(x)
            context_with_x = {**context, 'x': x}
            fx = self.evaluate(morphism_expr, context_with_x)
            
            # Check if we found a root
            if isinstance(fx, (int, float, complex)):
                if abs(fx) < self.tolerance:
                    return x
                
                # Simple iteration: x_next = x - f(x) / f'(x)
                # For now, use simple update
                h = self.tolerance * 10
                context_with_x_h = {**context, 'x': x + h}
                fx_h = self.evaluate(morphism_expr, context_with_x_h)
                
                # Numerical derivative
                if isinstance(fx_h, (int, float, complex)) and isinstance(fx, (int, float, complex)):
                    df = (fx_h - fx) / h
                    if abs(df) > self.tolerance:
                        x = x - fx / df
                    else:
                        break
            else:
                break
        
        return x


def create_ce1_context() -> Dict[str, Any]:
    """
    Create a standard CE1 context with common mathematical operators.
    
    Returns:
        Dictionary of operator name -> function mappings
    """
    return {
        'sin': cmath.sin,
        'cos': cmath.cos,
        'tan': cmath.tan,
        'ln': cmath.log,
        'exp': cmath.exp,
        'sqrt': cmath.sqrt,
    }


# Export public API
__all__ = [
    'BracketType',
    'CE1Expression',
    'CE1Parser',
    'CE1Evaluator',
    'create_ce1_context',
]
