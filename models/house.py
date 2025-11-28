"""
House model for multi-agent optimal stopping problem.

This module defines the House class which represents properties in the housing market
simulation. Each house has a unique identifier and a quality score that agents use
to make acceptance decisions.

Classes:
    House: Represents a house with quality attributes
"""

from dataclasses import dataclass


@dataclass
class House:
    """Represents a house in the optimal stopping problem."""
    
    id: str
    quality: float  # 0-10 scale representing overall house quality
