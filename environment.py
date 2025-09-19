import random
from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass
from models import House, Agent


@dataclass
class SimulationResult:
    """Results from a simulation run."""
    matched_pairs: List[Tuple[Agent, House]]
    unmatched_agents: List[Agent]
    unmatched_houses: List[House]
    total_rounds: int
    efficiency_score: float


class Environment:
    """Environment for multi-agent optimal stopping simulation."""
    
    def __init__(self, random_seed: Optional[int] = None):
        self.random_seed = random_seed
        if random_seed is not None:
            random.seed(random_seed)
    
    def run_simulation(self, agents: List[Agent], houses: List[House], 
                      max_iter: Optional[int] = None) -> SimulationResult:
        """
        Run a complete simulation until no active agents or houses remain.
        
        Args:
            agents: List of agents to participate
            houses: List of houses available
            max_iter: Maximum number of iterations (default: min(len(agents), len(houses)) * 2)
            
        Returns:
            SimulationResult with complete simulation data
        """
        # Reset all agents
        for agent in agents:
            agent.reset()
            
        # Create working copies
        active_agents = [a for a in agents if a.is_active]
        available_houses = houses.copy()
        matched_pairs = []
        round_number = 0
        
        total_agents = len(agents)
        total_houses = len(houses)
        
        if max_iter is None:
            max_iter = min(len(agents), len(houses)) * 2
            
        while active_agents and available_houses and round_number < max_iter:
            round_number += 1
            
            # Create random matches for this round
            matches = self._create_matches(active_agents, available_houses)
            
            # Process each match
            for agent, house in matches:
                agents_left = len(active_agents)
                houses_left = len(available_houses)
                
                if agent.evaluate_house(house, round_number, max_iter, total_agents, 
                                      total_houses, agents_left, houses_left):
                    matched_pairs.append((agent, house))
                    available_houses.remove(house)
            
            # Update active agents list
            active_agents = [a for a in active_agents if a.is_active]
        
        # Calculate efficiency
        efficiency = self._calculate_efficiency(matched_pairs, agents, houses)
        
        unmatched_agents = [a for a in agents if a.selected_house is None]
        
        return SimulationResult(
            matched_pairs=matched_pairs,
            unmatched_agents=unmatched_agents,
            unmatched_houses=available_houses,
            total_rounds=round_number,
            efficiency_score=efficiency
        )
    
    def _create_matches(self, agents: List[Agent], houses: List[House]) -> List[Tuple[Agent, House]]:
        """Create random agent-house pairs for a round."""
        min_count = min(len(agents), len(houses))
        
        selected_agents = random.sample(agents, min_count)
        selected_houses = random.sample(houses, min_count)
        
        return list(zip(selected_agents, selected_houses))
    
    def _calculate_efficiency(self, matched_pairs: List[Tuple[Agent, House]], 
                            all_agents: List[Agent], all_houses: List[House]) -> float:
        """Calculate simulation efficiency based on total quality achieved."""
        if not matched_pairs:
            return 0.0
            
        # Calculate achieved quality
        achieved_quality = sum(house.quality for _, house in matched_pairs)
        
        # Calculate theoretical maximum (top houses matched optimally)
        max_possible_matches = min(len(all_agents), len(all_houses))
        sorted_houses = sorted(all_houses, key=lambda h: h.quality, reverse=True)
        max_possible_quality = sum(h.quality for h in sorted_houses[:max_possible_matches])
        
        return achieved_quality / max_possible_quality if max_possible_quality > 0 else 0.0
    
