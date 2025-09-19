from dataclasses import dataclass


@dataclass
class House:
    """Represents a house in the optimal stopping problem."""
    
    id: str
    quality: float  # 0-10 scale representing overall house quality
