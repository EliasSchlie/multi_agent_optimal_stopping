"""
Simplified Multi-Agent Optimal Stopping Experiment API

Provides a clean interface for running experiments with customizable agent specifications
and house generators.
"""

import random
import numpy as np
import copy
from typing import List, Dict, Callable, Any
from dataclasses import dataclass

from models import House, Agent
from environment import Environment


@dataclass
class ExperimentSummary:
    """Summary of multiple experiment runs."""
    num_experiments: int
    efficiency_scores: List[float]
    match_rates: List[float]
    rounds_taken: List[int]
    policy_stats: Dict[str, Dict[str, Any]]  # policy_name -> {raw data}


def run_simulations(agent_specification: List[Dict[str, Any]], 
                   house_generator: Callable[[], List[House]], 
                   num_experiments: int, 
                   max_iter: int = 50) -> ExperimentSummary:
    """
    Run multiple simulation experiments with specified agents and house generator.
    
    Args:
        agent_specification: List of dicts with keys:
            - "name": policy name (str)
            - "policy": policy function/class instance
            - "number": number of agents with this policy (int)
        house_generator: Function that returns a list of House objects
        num_experiments: Number of experiments to run
        max_iter: Maximum iterations per simulation
        
    Returns:
        ExperimentSummary with aggregated results
    """
    
    # Create agents from specification
    agents = []
    for spec in agent_specification:
        policy_name = spec["name"]
        policy_template = spec["policy"]
        num_agents = spec["number"]
        
        for i in range(num_agents):
            agent_id = f"{policy_name}_{i+1}"
            # Create a new policy instance for each agent to avoid shared state
            policy = copy.deepcopy(policy_template)
            agent = Agent(agent_id, policy)
            agents.append(agent)
    
    # Track results
    efficiency_scores = []
    match_rates = []
    rounds_taken = []
    policy_stats = {}
    
    # Initialize policy tracking
    for spec in agent_specification:
        policy_name = spec["name"]
        policy_stats[policy_name] = {
            "matches": 0,
            "unmatches": 0,
            "total_agents": spec["number"] * num_experiments,
            "qualities": [],
            "rounds_to_match": []
        }
    
    # Run experiments
    for exp_id in range(num_experiments):
        # Generate houses for this experiment
        houses = house_generator()
        
        # Reset all agents
        for agent in agents:
            agent.reset()
        
        # Run simulation
        env = Environment(random_seed=exp_id)
        result = env.run_simulation(agents, houses, max_iter=max_iter)
        
        # Process results
        efficiency_scores.append(result.efficiency_score)
        match_rates.append(len(result.matched_pairs) / len(agents))
        rounds_taken.append(result.total_rounds)
        
        # Track matches
        for agent, house in result.matched_pairs:
            policy_name = agent.id.rsplit('_', 1)[0]  # Extract policy name safely
            
            # Update policy stats
            policy_stats[policy_name]["matches"] += 1
            policy_stats[policy_name]["qualities"].append(house.quality)
            policy_stats[policy_name]["rounds_to_match"].append(len(agent.seen_houses))
        
        # Track unmatched agents
        for agent in result.unmatched_agents:
            policy_name = agent.id.rsplit('_', 1)[0]  # Extract policy name safely
            policy_stats[policy_name]["unmatches"] += 1


    
    # Return ExperimentSummary object
    return ExperimentSummary(
        num_experiments=num_experiments,
        efficiency_scores=efficiency_scores,
        match_rates=match_rates,
        rounds_taken=rounds_taken,
        policy_stats=policy_stats
    )