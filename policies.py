import numpy as np
from typing import List
from models import House
from models.agent import Policy


class GreedyPolicy(Policy):
    """Always accept the first house offered."""
    
    def should_accept(self, house, seen_houses, total_rounds, rounds_left, 
                     total_agents, agents_left, total_houses, houses_left) -> bool:
        return True


class ThresholdPolicy(Policy):
    """Accept house if it meets a minimum threshold quality."""
    
    def __init__(self, threshold: float = 5.0):
        self.threshold = threshold
    
    def should_accept(self, house, seen_houses, total_rounds, rounds_left,
                     total_agents, agents_left, total_houses, houses_left) -> bool:
        if rounds_left == 0:
            return True

        return house.quality >= self.threshold


class OptimalStoppingPolicy(Policy):
    """Classic optimal stopping rule based on exploration ratio."""
    
    def __init__(self, exploration_ratio: float = 0.37):
        self.exploration_ratio = exploration_ratio
        self.max_exploration_quality = None
    
    def should_accept(self, house: House, seen_houses: List[House], 
                     total_rounds: int, rounds_left: int, total_agents: int, 
                     agents_left: int, total_houses: int, houses_left: int) -> bool:
        exploration_houses = int(total_houses * self.exploration_ratio)
        
        if rounds_left == 0:
            return True

        # Still in exploration phase (seen_houses will include current house after decision)
        if len(seen_houses) < exploration_houses:
            return False
            
        # Set max exploration quality based on completed exploration
        if self.max_exploration_quality is None:
            if seen_houses:
                self.max_exploration_quality = max(h.quality for h in seen_houses[:exploration_houses])
            else:
                self.max_exploration_quality = 0

        # Accept if current house is better than best seen during exploration
        return house.quality > self.max_exploration_quality

    def reset(self):
        """Reset policy state for new simulation."""
        self.max_exploration_quality = None
