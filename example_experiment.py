#!/usr/bin/env python3
"""
Example experiment using the simplified API.

This demonstrates how to run experiments with different policies and house generators.
"""

import random
from experiment_api import run_simulations
from print_summary import print_experiment_summary
from house_generators import uniform_house_generator
from policies import (
    GreedyPolicy, ThresholdPolicy, OptimalStoppingPolicy
)


def example_basic_comparison():
    """Example 1: Basic policy comparison with uniform house distribution."""
    print("Example 1: Basic Policy Comparison")
    print("=" * 50)

    random.seed(42)
    
    # Define agent specification
    agent_spec = [
        {"name": "Greedy", "policy": GreedyPolicy(), "number": 10},
        {"name": "Threshold_6", "policy": ThresholdPolicy(threshold=6.0), "number": 10},
        {"name": "Threshold_8", "policy": ThresholdPolicy(threshold=8.0), "number": 10},
        {"name": "Optimal_Stopping", "policy": OptimalStoppingPolicy(exploration_ratio=0.1), "number": 10},
    ]
    
    # Use uniform house generator
    house_gen = uniform_house_generator(n_houses=100, min_quality=1.0, max_quality=10.0)
    
    # Run experiments
    results = run_simulations(
        agent_specification=agent_spec,
        house_generator=house_gen,
        num_experiments=100,
        max_iter=30
    )
    
    print_experiment_summary(results)

if __name__ == "__main__":
    example_basic_comparison()