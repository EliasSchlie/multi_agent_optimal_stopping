"""
Agent and Policy classes for multi-agent optimal stopping problem.

This module defines the core agent architecture and policy interface for simulating
multi-agent house selection scenarios. Agents use policies to make decisions about
whether to accept or reject house offers based on various factors including the
current house quality, previously seen houses, and market conditions.

Classes:
    Policy: Abstract base class for decision-making policies
    Agent: Represents an individual agent in the simulation
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from .house import House


class Policy(ABC):
    """Abstract base class for agent policies."""
    
    def reset(self):
        """Reset policy state for a new simulation. Override if policy has internal state."""
        pass
    
    @abstractmethod
    def should_accept(
        self, 
        house: House, 
        seen_houses: List[House], 
        total_rounds: int,
        rounds_left: int,
        total_agents: int, 
        agents_left: int, 
        total_houses: int,
        houses_left: int
        ) -> bool:
        """
        Decide whether to accept a house offer.
        
        Args:
            house: The current house being offered
            seen_houses: List of previously seen houses
            round_number: Current round (1-indexed)
            total_agents: Total number of agents in simulation
            total_houses: Total number of houses in simulation
            agents_left: Number of active agents remaining
            houses_left: Number of houses remaining
            
        Returns:
            True if house should be accepted, False otherwise
        """
        pass


class Agent:
    """Represents an agent in the optimal stopping problem."""
    
    def __init__(self, id: str, policy: Policy):
        self.id = id
        self.policy = policy
        self.seen_houses: List[House] = []
        self.selected_house: Optional[House] = None
        self.is_active = True
        
    def evaluate_house(self, house: House, round_number: int, total_rounds: int, 
                      total_agents: int, total_houses: int, agents_left: int, houses_left: int) -> bool:
        """Evaluate a house using the agent's policy."""
        if not self.is_active:
            return False
            
        rounds_left = total_rounds - round_number
        decision = self.policy.should_accept(
            house, self.seen_houses.copy(), total_rounds, rounds_left,
            total_agents, agents_left, total_houses, houses_left
        )
        
        self.seen_houses.append(house)
        
        if decision:
            self.selected_house = house
            self.is_active = False
            
        return decision
    
    def reset(self):
        """Reset agent for new simulation."""
        self.seen_houses = []
        self.selected_house = None
        self.is_active = True
        self.policy.reset()  # Reset policy state
