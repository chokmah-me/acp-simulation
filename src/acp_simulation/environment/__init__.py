"""
Environment simulation for ACP.

This module provides the network environment and simulation mechanics
including cognitive latency windows and reward calculations.
"""

from .network import ConfigurableNetworkEnvironment, NetworkEnvironment

__all__ = [
    "NetworkEnvironment",
    "ConfigurableNetworkEnvironment",
]
