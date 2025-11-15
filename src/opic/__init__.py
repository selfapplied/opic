"""
OPIC: Event-Based Compositional Language

Core module for OPIC field geometry and voice composition.
"""

from .parser import initialize_field_geometry, parse_json_config

__all__ = [
    'initialize_field_geometry',
    'parse_json_config',
]

__version__ = '0.1.0'
