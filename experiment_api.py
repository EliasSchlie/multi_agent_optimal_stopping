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
class SimulationResult:
    """Result from a single simulation run."""
    simulation_id: int
    efficiency_score: float
    match_rate: float
    rounds_taken: int
    policy_results: Dict[str, Dict[str, Any]]  # policy_name -> {matches, unmatches, qualities, rounds}


@dataclass
class ExperimentSummary:
    """Summary of multiple experiment runs."""
    num_experiments: int
    efficiency_scores: List[float]
    match_rates: List[float]
    rounds_taken: List[int]
    policy_stats: Dict[str, Dict[str, Any]]  # policy_name -> {raw data}
    simulation_results: List[SimulationResult]  # New: per-simulation detailed results


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
    
    # Create agents from specification - INTERLEAVED for fairness
    agents = []
    max_agents_per_policy = max(spec["number"] for spec in agent_specification)
    
    # Interleave agents from different policies
    for i in range(max_agents_per_policy):
        for spec in agent_specification:
            if i < spec["number"]:  # Only add if this policy has this many agents
                policy_name = spec["name"]
                policy_template = spec["policy"]
                
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
    simulation_results = []  # New: store per-simulation results
    
    # Initialize policy tracking
    for spec in agent_specification:
        policy_name = spec["name"]
        policy_stats[policy_name] = {
            "matches": 0,
            "unmatches": 0,
            "total_agents": spec["number"] * num_experiments,
            "qualities": [],
            "rounds_to_match": [],
            "rounds_all_agents": []
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
        match_rate = len(result.matched_pairs) / len(agents)
        match_rates.append(match_rate)
        rounds_taken.append(result.total_rounds)
        
        # Initialize per-simulation policy results
        sim_policy_results = {}
        for spec in agent_specification:
            policy_name = spec["name"]
            sim_policy_results[policy_name] = {
                "matches": 0,
                "unmatches": 0,
                "total_agents": spec["number"],
                "qualities": [],
                "rounds_to_match": [],
                "rounds_all_agents": []
            }
        
        # Track matches for this simulation
        for agent, house in result.matched_pairs:
            policy_name = agent.id.rsplit('_', 1)[0]  # Extract policy name safely
            
            # Update aggregated policy stats
            policy_stats[policy_name]["matches"] += 1
            policy_stats[policy_name]["qualities"].append(house.quality)
            policy_stats[policy_name]["rounds_to_match"].append(len(agent.seen_houses))
            policy_stats[policy_name]["rounds_all_agents"].append(len(agent.seen_houses))
            
            # Update per-simulation policy results
            sim_policy_results[policy_name]["matches"] += 1
            sim_policy_results[policy_name]["qualities"].append(house.quality)
            sim_policy_results[policy_name]["rounds_to_match"].append(len(agent.seen_houses))
            sim_policy_results[policy_name]["rounds_all_agents"].append(len(agent.seen_houses))
        
        # Track unmatched agents for this simulation
        for agent in result.unmatched_agents:
            policy_name = agent.id.rsplit('_', 1)[0]  # Extract policy name safely
            
            # Update aggregated policy stats
            policy_stats[policy_name]["unmatches"] += 1
            policy_stats[policy_name]["rounds_all_agents"].append(len(agent.seen_houses))
            
            # Update per-simulation policy results
            sim_policy_results[policy_name]["unmatches"] += 1
            sim_policy_results[policy_name]["rounds_all_agents"].append(len(agent.seen_houses))
        
        # Store this simulation's results
        simulation_results.append(SimulationResult(
            simulation_id=exp_id,
            efficiency_score=result.efficiency_score,
            match_rate=match_rate,
            rounds_taken=result.total_rounds,
            policy_results=sim_policy_results
        ))


    
    # Return ExperimentSummary object
    return ExperimentSummary(
        num_experiments=num_experiments,
        efficiency_scores=efficiency_scores,
        match_rates=match_rates,
        rounds_taken=rounds_taken,
        policy_stats=policy_stats,
        simulation_results=simulation_results
    )