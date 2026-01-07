"""
Agent implementations for ACP simulation.

This module provides base classes and concrete implementations for:
- Attackers (CognitiveAttacker with IBLT learning)
- Defenders (Pessimistic and ACP strategies)
"""

from .attacker import CognitiveAttacker, ConfigurableAttacker
from .base import BaseAttacker, BaseDefender
from .defender import (
    ConfigurableACPDefender,
    ConfigurablePessimisticDefender,
    OptimisticACPDefender,
    PessimisticDefender,
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
