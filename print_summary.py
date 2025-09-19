import numpy as np


def print_experiment_summary(summary):
    """Print a formatted summary of experiment results."""
    print("=" * 60)
    print("EXPERIMENT SUMMARY")
    print("=" * 60)
    print(f"Number of experiments: {summary.num_experiments}")
    print(f"Average efficiency: {np.mean(summary.efficiency_scores):.3f} ± {np.std(summary.efficiency_scores):.3f}")
    print(f"Average match rate: {np.mean(summary.match_rates):.3f} ± {np.std(summary.match_rates):.3f}")
    print(f"Average rounds: {np.mean(summary.rounds_taken):.1f} ± {np.std(summary.rounds_taken):.1f}")
    
    print("\nPOLICY PERFORMANCE:")
    print("-" * 60)
    print(f"{'Policy':<20} {'Match Rate':<12} {'Avg Quality':<12} {'Avg Rounds':<12} {'Matches':<8} {'Unmatched':<10}")
    print("-" * 60)
    
    for policy_name, stats in summary.policy_stats.items():
        match_rate = stats['matches'] / stats['total_agents']
        avg_quality = np.mean(stats['qualities']) if stats['qualities'] else 0
        avg_rounds = np.mean(stats['rounds_to_match']) if stats['rounds_to_match'] else 0
        
        print(f"{policy_name:<20} "
              f"{match_rate:<12.3f} "
              f"{avg_quality:<12.3f} "
              f"{avg_rounds:<12.1f} "
              f"{stats['matches']:<8} "
              f"{stats['unmatches']:<10}")
    print("=" * 60)