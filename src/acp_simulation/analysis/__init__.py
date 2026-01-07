"""
Statistical analysis and visualization for ACP simulation.

This module provides:
- Statistical analysis (power analysis, confidence intervals)
- Visualization functions for publication-quality figures
- Result processing and summarization
"""

from .statistics import (
    analyze_experiment_results,
    bootstrap_confidence_intervals,
    calculate_power_analysis,
)
from .visualization import (
    create_results_figure,
    plot_action_distribution,
    plot_confidence_degradation,
    plot_reward_comparison,
)

__all__ = [
    "calculate_power_analysis",
    "bootstrap_confidence_intervals",
    "analyze_experiment_results",
    "create_results_figure",
    "plot_reward_comparison",
    "plot_action_distribution",
    "plot_confidence_degradation",
]
