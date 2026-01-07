"""
Agent implementations for ACP simulation.

This module provides base classes and concrete implementations for:
- Attackers (CognitiveAttacker with IBLT learning)
- Defenders (Pessimistic and ACP strategies)
"""

from .base import BaseAttacker, BaseDefender
from .attacker import CognitiveAttacker, ConfigurableAttacker
from .defender import (
    PessimisticDefender,
    OptimisticACPDefender,
    ConfigurablePessimisticDefender,
    ConfigurableACPDefender,
)

__all__ = [
    "BaseAttacker",
    "BaseDefender",
    "CognitiveAttacker",
    "ConfigurableAttacker",
    "PessimisticDefender",
    "OptimisticACPDefender",
    "ConfigurablePessimisticDefender",
    "ConfigurableACPDefender",
]
