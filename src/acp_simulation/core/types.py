"""
Type aliases for ACP simulation.
"""

from typing import Any, Dict, List, Tuple, Union

import numpy as np
from numpy.typing import NDArray

# Type aliases for better code readability
AgentState = Dict[str, Any]
"""Agent state dictionary containing current observation and metadata."""

RewardArray = NDArray[np.float64]
"""Array of reward values from simulation episodes."""

EpisodeResult = Dict[str, Any]
"""Dictionary containing results from a single episode."""

# Network types
NodeID = int
"""Identifier for a network node."""

NetworkState = Dict[NodeID, Any]
"""Dictionary mapping node IDs to their states."""

# Memory types
MemoryInstance = Tuple
"""Encoded memory instance for IBLT retrieval."""

# Action and reward types
ActionValue = float
"""Expected value of taking an action in a given state."""

ActivationValue = float
"""Activation value for memory retrieval in IBLT."""

# Configuration types
ConfigDict = Dict[str, Any]
"""Dictionary representation of configuration."""

# Statistical types
ConfidenceInterval = Tuple[float, float]
"""Lower and upper bounds of a confidence interval."""

EffectSize = float
"""Statistical effect size (e.g., Cohen's d)."""

PValue = float
"""Statistical p-value."""

Power = float
"""Statistical power (0 to 1)."""

# Visualization types
PlotData = Dict[str, Any]
"""Data structure for plotting functions."""

# Export commonly used types
__all__ = [
    "AgentState",
    "RewardArray",
    "EpisodeResult",
    "NodeID",
    "NetworkState",
    "MemoryInstance",
    "ActionValue",
    "ActivationValue",
    "ConfigDict",
    "ConfidenceInterval",
    "EffectSize",
    "PValue",
    "Power",
    "PlotData",
]
