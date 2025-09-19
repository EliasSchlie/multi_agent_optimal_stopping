# Run experiments
See: `example_experiments.ipynb` or `example_experiment.py` for how to run experiments

# Policies
Edit and create policies in `policies.py` (the ones I created are just examples. Please try to understand them before you use any of them in the research)

# What to do now
You have to exactly understand what experiments you want to run.

### Possible inputs that you can change
- Types of policies
- How many agents of each policy search for a house
- How many houses are available (you can try with more agents than houses, equal nubers or more houses than agents)
- Distribution of house quality (e.g. normal distribution vs. uniform distribution vs. ...)

Make sure to create a baseline with how a single agent does with a given policy (From my experimentation it seems like the optimal stopping agent is amazing alone, but sucks in groups...)

Make sure that you truly understand the policies that you are experimenting with. This will likely be the biggest place for errors