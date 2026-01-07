"""
Base agent classes for ACP simulation.

This module provides abstract base classes for attackers and defenders,
defining common interfaces and shared functionality.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Set, Any
import numpy as np
from numpy.typing import NDArray

from ..core.enums import ActionType


class BaseAttacker(ABC):
    """
    Abstract base class for all attacker agents.

    Defines the interface that all attacker implementations must follow,
    including action selection and learning capabilities.
    """

    def __init__(self, decay_rate: float = 0.8, noise: float = 0.1):
        """
        Initialize base attacker.

        Parameters
        ----------
        decay_rate : float, default=0.8
            Memory decay rate for IBLT
        noise : float, default=0.1
            Decision noise level
        """
        self.decay_rate = decay_rate
        self.noise = noise
        self.known_nodes: Set[int] = set()
        self.compromised_nodes: Set[int] = set()
        self.overall_confidence = 1.0

    @abstractmethod
    def select_action(self, state: Dict[str, Any], current_time: int) -> ActionType:
        """
        Select an action based on current state.

        Parameters
        ----------
        state : Dict[str, Any]
            Current environment state
        current_time : int
            Current time step

        Returns
        -------
        ActionType
            Selected action
        """
        pass

    @abstractmethod
    def learn(
        self,
        situation: tuple,
        action: ActionType,
        outcome: float,
        timestamp: int,
        confidence: float = 1.0,
    ) -> None:
        """
        Learn from experience and update memory.

        Parameters
        ----------
        situation : tuple
            Encoded situation representation
        action : ActionType
            Action taken
        outcome : float
            Reward or outcome from action
        timestamp : int
            Time when action was taken
        confidence : float, default=1.0
            Confidence level for this learning instance
        """
        pass

    @abstractmethod
    def _encode_situation(self, state: Dict[str, Any]) -> tuple:
        """
        Encode current situation for memory indexing.

        Parameters
        ----------
        state : Dict[str, Any]
            Current state

        Returns
        -------
        tuple
            Encoded situation representation
        """
        pass


class BaseDefender(ABC):
    """
    Abstract base class for all defender agents.

    Defines the interface that all defender implementations must follow,
    including action selection and ACP deception capabilities.
    """

    def __init__(self, network: Any):
        """
        Initialize base defender.

        Parameters
        ----------
        network : Any
            Network graph object
        """
        self.network = network
        self.action_history: List[ActionType] = []

    @abstractmethod
    def select_action(self, state: Dict[str, Any], attacker_knowledge: Set[int]) -> ActionType:
        """
        Select a defensive action.

        Parameters
        ----------
        state : Dict[str, Any]
            Current environment state
        attacker_knowledge : Set[int]
            Set of nodes known to attacker

        Returns
        -------
        ActionType
            Selected defensive action
        """
        pass

    def deploy_acp_deception(
        self, target_nodes: List[int], current_time: int, attacker_knowledge: Set[int]
    ) -> Dict[int, Dict[str, Any]]:
        """
        Deploy ACP deception (default: no deception).

        Parameters
        ----------
        target_nodes : List[int]
            Target nodes for deception
        current_time : int
            Current time step
        attacker_knowledge : Set[int]
            Nodes known to attacker

        Returns
        -------
        Dict[int, Dict[str, Any]]
            Deception results (empty by default)
        """
        return {}

    def get_action_distribution(self) -> Dict[ActionType, float]:
        """
        Calculate action distribution from history.

        Returns
        -------
        Dict[ActionType, float]
            Mapping of actions to their frequencies
        """
        if not self.action_history:
            return {}

        total = len(self.action_history)
        distribution = {}
        for action in set(self.action_history):
            distribution[action] = self.action_history.count(action) / total

        return distribution
