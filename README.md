# Multi-Agent Optimal Stopping Problem

This repository contains a simulation framework for studying how the presence of multiple agents influences the efficiency of different decision-making policies in the optimal stopping problem, specifically applied to a house selection scenario.

## Overview

The **optimal stopping problem** is a classic decision-making challenge where an agent must choose when to stop a sequential search process to maximize their outcome. In the traditional single-agent version (secretary problem), the optimal strategy involves exploring a fraction of options and then selecting the first option that exceeds the best seen during exploration.

This project extends the problem to a **multi-agent setting** where multiple agents with potentially different policies compete for limited resources (houses), creating strategic interactions and market dynamics that don't exist in the single-agent case.

## Possible Research Questions to Explore With This Repo

- How does the presence of other agents affect the efficiency of different policies?
- Which policies perform best in competitive multi-agent environments?
- How do market conditions (house quality distributions, agent-to-house ratios) influence outcomes?
- What is the trade-off between exploration and exploitation in competitive settings?

## Project Structure

This repository was build and used in the context of a Multi-Agent Systems course. All the experiments mentioned in our final submission have been executed in: **`project_experiments.ipynb`** 

### Core Components

- **`models/`** - Core data structures
  - `agent.py` - Agent class and Policy interface
  - `house.py` - House representation with quality attributes

- **`environment.py`** - Simulation orchestrator that manages agent-house interactions

- **`policies.py`** - Decision-making strategies for agents:
  - `GreedyPolicy` - Accept first offer
  - `ThresholdPolicy` - Accept offers above quality threshold  
  - `OptimalStoppingPolicy` - Classic secretary problem solution

- **`house_generators.py`** - Functions to create diverse market scenarios:
  - Uniform, normal, and bimodal quality distributions

### Experiment Framework

- **`experiment_api.py`** - Simplified API for running experiments with multiple policies
- **`example_experiment.py`** - Example usage and basic policy comparisons
- **`example_experiments.ipynb`** - Interactive notebook with detailed experiments
- **`print_summary.py`** - Formatted output for experiment results
- **`project_experiments.ipynb`** - Project Experiment is run here

## Quick Start

### Running Basic Experiments

```python
from experiment_api import run_simulations
from house_generators import uniform_house_generator
from policies import GreedyPolicy, ThresholdPolicy, OptimalStoppingPolicy

# Define agent mix
agent_spec = [
    {"name": "Greedy", "policy": GreedyPolicy(), "number": 10},
    {"name": "Threshold", "policy": ThresholdPolicy(threshold=6.0), "number": 10},
    {"name": "Optimal", "policy": OptimalStoppingPolicy(), "number": 10},
]

# Create house market
house_gen = uniform_house_generator(n_houses=50, min_quality=1.0, max_quality=10.0)

# Run experiments
results = run_simulations(
    agent_specification=agent_spec,
    house_generator=house_gen,
    num_experiments=100
)
```

### Example Experiments

1. **Basic comparison**: `python example_experiment.py`
2. **Interactive analysis**: Open `example_experiments.ipynb`
3. **Advanced scenarios**: Open `project_experiments.ipynb`

## Key Experimental Variables

### Agent Policies
- **Types**: Greedy, Threshold-based, Optimal Stopping
- **Numbers**: Vary agent counts per policy to study population dynamics
- **Parameters**: Threshold values, exploration ratios

### Market Conditions
- **House quantities**: More/fewer houses than agents
- **Quality distributions**: Uniform, normal, bimodal
- **Market size**: Small vs. large markets

### Performance Metrics
- **Efficiency Score**: Ratio of achieved quality to theoretical maximum
- **Match Rate**: Percentage of agents that successfully match
- **Rounds to Match**: Speed of decision-making

## Research Insights

From initial experimentation:
- **Optimal stopping agents** excel in single-agent scenarios but struggle in competitive multi-agent environments
- **Market competition** fundamentally changes optimal strategies
- **Policy diversity** in agent populations creates complex dynamics
- **Exploration vs. exploitation** trade-offs are amplified in competitive settings

## Installation

This project uses `uv` for dependency management:

```bash
# Install dependencies
uv sync

# Run example
uv run example_experiment.py
```
