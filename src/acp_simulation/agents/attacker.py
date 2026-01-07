"""
Attacker agent implementations for ACP simulation.

This module provides concrete attacker implementations including:
- CognitiveAttacker: IBLT-based learning attacker
- ConfigurableAttacker: Extended version with configurable learning rate
"""

from typing import Dict, List, Set, Tuple, Any
from collections import defaultdict
import numpy as np
from numpy.typing import NDArray

from .base import BaseAttacker
from ..core.dataclasses import Instance
from ..core.enums import ActionType


class CognitiveAttacker(BaseAttacker):
    """
    Instance-Based Learning Theory (IBLT) Attacker.

    Implements cognitive model from Du et al. (2025) with:
    - Memory-based learning (not static rules)
    - Activation-weighted blending for decisions
    - Recency effects and confidence tracking
    - Vulnerability to memory poisoning from ACP

    Attributes
    ----------
    memory : List[Instance]
        Stored experiences for IBLT retrieval
    decay_rate : float
        Memory decay rate (d parameter in IBLT equation)
    noise : float
        Decision noise (σ parameter)
    known_nodes : Set[int]
        Nodes discovered by attacker
    compromised_nodes : Set[int]
        Nodes successfully compromised
    overall_confidence : float
        Tracks memory poisoning effects
    learning_history : List[Dict]
        History of learning events for analysis
    """

    def __init__(self, decay_rate: float = 0.8, noise: float = 0.1):
        """
        Initialize cognitive attacker.

        Parameters
        ----------
        decay_rate : float, default=0.8
            Memory decay rate for IBLT
        noise : float, default=0.1
            Decision noise level
        """
        super().__init__(decay_rate, noise)
        self.memory: List[Instance] = []
        self.learning_history: List[Dict] = []

    def activation(self, instance: Instance, current_time: int) -> float:
        """
        Calculate IBLT activation: A = ln(Σ(t-t')^-d) * confidence + σξ.

        This determines how "activated" a past memory is:
        - Recent memories have higher activation
        - High-confidence memories have higher activation
        - Noise adds stochasticity

        Parameters
        ----------
        instance : Instance
            Memory instance to calculate activation for
        current_time : int
            Current time step

        Returns
        -------
        float
            Activation value for this memory
        """
        time_diff = current_time - instance.timestamp
        if time_diff <= 0:
            return 0.0

        # Core IBLT activation equation
        base_activation = np.log(max(time_diff ** (-self.decay_rate), 1e-10))

        # CRITICAL: Confidence weighting (degraded by ACP deception)
        confidence_weight = instance.confidence

        # Noise term
        noise_term = self.noise * np.random.normal(0, 1)

        return (base_activation * confidence_weight) + noise_term

    def select_action(self, state: Dict[str, Any], current_time: int) -> ActionType:
        """
        Select BEST action based on expected value from memory.

        Calculates expected value for each action based on memory retrieval
        and selects the action with highest expected outcome.

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
        if not self.memory:
            # No experience yet - start with exploration
            return ActionType.SCAN

        # Group memories by action type
        action_memories = defaultdict(list)
        for instance in self.memory:
            if instance.action in [ActionType.SCAN, ActionType.EXPLOIT, ActionType.PROPAGATE]:
                action_memories[instance.action].append(instance)

        # Calculate expected value for each action
        action_values = {}

        for action, memories in action_memories.items():
            if not memories:
                continue

            # Calculate activations for all memories of this action
            activations = np.array([self.activation(mem, current_time) for mem in memories])

            # Get outcomes for these memories
            outcomes = np.array([mem.outcome for mem in memories])

            # Softmax weighting (higher activation = more weight)
            if len(activations) > 0:
                weights = self._softmax(activations)
                expected_value = np.sum(weights * outcomes)
                action_values[action] = expected_value

        # Add exploration bonus for unseen actions
        for action in [ActionType.SCAN, ActionType.EXPLOIT, ActionType.PROPAGATE]:
            if action not in action_values:
                # Unknown actions get random value (encourages exploration)
                action_values[action] = np.random.uniform(-2, 2)

        # CRITICAL: Select BEST action (not random)
        if action_values:
            best_action = max(action_values.items(), key=lambda x: x[1])[0]

            # Small exploration noise (10% chance of random action)
            if np.random.random() < 0.1:
                best_action = np.random.choice(
                    [ActionType.SCAN, ActionType.EXPLOIT, ActionType.PROPAGATE]
                )

            return best_action

        return ActionType.SCAN

    def learn(
        self,
        situation: Tuple,
        action: ActionType,
        outcome: float,
        timestamp: int,
        confidence: float = 1.0,
    ) -> None:
        """
        Store new experience in memory.

        CRITICAL: confidence parameter allows ACP to poison memory
        - Normal learning: confidence = 1.0
        - ACP-poisoned learning: confidence = 0.3-0.5

        Parameters
        ----------
        situation : Tuple
            Encoded situation representation
        action : ActionType
            Action taken
        outcome : float
            Reward or outcome from action
        timestamp : int
            Current time step
        confidence : float, default=1.0
            Confidence level for this memory
        """
        instance = Instance(situation, action, outcome, timestamp, confidence)
        self.memory.append(instance)

        # Track learning history for analysis
        self.learning_history.append(
            {"timestamp": timestamp, "action": action, "outcome": outcome, "confidence": confidence}
        )

        # Update overall confidence (degrades with poisoned memories)
        if len(self.memory) > 0:
            # Recent memory confidence average
            recent_confidences = [inst.confidence for inst in self.memory[-20:]]
            avg_confidence = np.mean(recent_confidences)

            # Exponential moving average
            self.overall_confidence = 0.9 * self.overall_confidence + 0.1 * avg_confidence

        # Memory management: Keep bounded size
        if len(self.memory) > 150:
            # Keep most important memories (high activation potential)
            def activation_potential(inst):
                return self.activation(inst, timestamp) * inst.confidence

            self.memory.sort(key=activation_potential, reverse=True)
            self.memory = self.memory[:100]

    def _encode_situation(self, state: Dict[str, Any]) -> Tuple:
        """
        Encode current situation for memory indexing.

        Parameters
        ----------
        state : Dict[str, Any]
            Current state

        Returns
        -------
        tuple
            Encoded situation: (known_nodes, compromised_nodes, alert_level, time_bin)
        """
        return (
            len(self.known_nodes),
            len(self.compromised_nodes),
            state.get("alert_level", 0),
            state.get("time", 0) // 10,  # Coarse time bins
        )

    def _softmax(self, x: NDArray[np.float64]) -> NDArray[np.float64]:
        """
        Stable softmax implementation.

        Parameters
        ----------
        x : NDArray[np.float64]
            Input array

        Returns
        -------
        NDArray[np.float64]
            Softmax probabilities
        """
        x = x - np.max(x)
        exp_x = np.exp(np.clip(x, -100, 100))
        return exp_x / (np.sum(exp_x) + 1e-10)


class ConfigurableAttacker(CognitiveAttacker):
    """
    Cognitive attacker with configurable learning rate.

    Extends CognitiveAttacker to allow adjustable learning speed,
    enabling sensitivity analysis of attacker adaptation rates.

    Attributes
    ----------
    learning_rate : float
        Multiplier for learning speed (higher = faster adaptation)
    """

    def __init__(self, decay_rate: float = 0.8, noise: float = 0.1, learning_rate: float = 1.0):
        """
        Initialize configurable attacker.

        Parameters
        ----------
        decay_rate : float, default=0.8
            Memory decay rate
        noise : float, default=0.1
            Decision noise level
        learning_rate : float, default=1.0
            Learning rate multiplier (higher = faster adaptation)
        """
        super().__init__(decay_rate, noise)
        self.learning_rate = learning_rate

    def learn(
        self,
        situation: Tuple,
        action: ActionType,
        outcome: float,
        timestamp: int,
        confidence: float = 1.0,
    ) -> None:
        """
        Store instance with configurable learning rate.

        Adjusts activation based on learning rate to simulate
        different attacker adaptation speeds.

        Parameters
        ----------
        situation : Tuple
            Encoded situation representation
        action : ActionType
            Action taken
        outcome : float
            Reward from action
        timestamp : int
            Current time step
        confidence : float, default=1.0
            Confidence level
        """
        # Adjust learning based on rate
        adjusted_confidence = confidence * self.learning_rate

        # Call parent learn with adjusted confidence
        super().learn(situation, action, outcome, timestamp, adjusted_confidence)
