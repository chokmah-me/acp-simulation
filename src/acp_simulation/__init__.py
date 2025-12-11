"""
Asymmetric Cognitive Projection (ACP) Simulation Package.

A comprehensive simulation framework for evaluating strategic cybersecurity
defense mechanisms against instance-based learning attackers.

This package provides:
- Core data structures and enumerations
- Agent implementations (attackers and defenders)
- Network environment simulation
- Experiment runners and configuration management
- Statistical analysis and visualization tools

Version: 4.0.0
"""

__version__ = "4.0.0"
__author__ = "dyb"

from .core import (
    NodeState,
    ActionType,
    Instance,
    SimulationConfig,
    AgentState,
    RewardArray,
    EpisodeResult,
)

__all__ = [
    "__version__",
    "NodeState",
    "ActionType",
    "Instance",
    "SimulationConfig",
    "AgentState",
    "RewardArray",
    "EpisodeResult",
]