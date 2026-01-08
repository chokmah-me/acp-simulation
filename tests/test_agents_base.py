"""
Tests for base agent classes (BaseAttacker and BaseDefender).

This test module provides comprehensive coverage for abstract base classes,
including initialization, state management, and interface validation.
"""

import pytest
from typing import Any, Dict, Set

from src.acp_simulation.agents.base import BaseAttacker, BaseDefender
from src.acp_simulation.core.enums import ActionType


# Concrete implementations for testing abstract classes
class ConcreteAttacker(BaseAttacker):
    """Minimal concrete implementation of BaseAttacker for testing."""

    def select_action(self, state: Dict[str, Any], current_time: int) -> ActionType:
        """Select a random attack action."""
        return ActionType.EXPLOIT

    def learn(
        self,
        situation: tuple,
        action: ActionType,
        outcome: float,
        timestamp: int,
        confidence: float = 1.0,
    ) -> None:
        """No-op learning for testing."""
        pass

    def _encode_situation(self, state: Dict[str, Any]) -> tuple:
        """Encode state as tuple of node states."""
        return tuple(state.get("node_states", []))


class ConcreteDefender(BaseDefender):
    """Minimal concrete implementation of BaseDefender for testing."""

    def select_action(self, state: Dict[str, Any], attacker_knowledge: Set[int]) -> ActionType:
        """Select a random defense action."""
        return ActionType.MONITOR


class TestBaseAttacker:
    """Test suite for BaseAttacker abstract base class."""

    def test_cannot_instantiate_abstract_base_class(self):
        """Verify that BaseAttacker cannot be directly instantiated."""
        with pytest.raises(TypeError, match="Can't instantiate abstract class"):
            BaseAttacker()  # type: ignore

    def test_initialization_with_defaults(self):
        """Test attacker initialization with default parameters."""
        attacker = ConcreteAttacker()

        assert attacker.decay_rate == 0.8
        assert attacker.noise == 0.1
        assert attacker.known_nodes == set()
        assert attacker.compromised_nodes == set()
        assert attacker.overall_confidence == 1.0

    def test_initialization_with_custom_params(self):
        """Test attacker initialization with custom parameters."""
        attacker = ConcreteAttacker(decay_rate=0.9, noise=0.05)

        assert attacker.decay_rate == 0.9
        assert attacker.noise == 0.05
        assert attacker.overall_confidence == 1.0

    def test_known_nodes_tracking(self):
        """Test that known_nodes set can be modified."""
        attacker = ConcreteAttacker()
        attacker.known_nodes.add(1)
        attacker.known_nodes.add(2)

        assert attacker.known_nodes == {1, 2}

    def test_compromised_nodes_tracking(self):
        """Test that compromised_nodes set can be modified."""
        attacker = ConcreteAttacker()
        attacker.compromised_nodes.add(5)
        attacker.compromised_nodes.add(10)

        assert attacker.compromised_nodes == {5, 10}

    def test_select_action_interface(self):
        """Test that select_action interface works correctly."""
        attacker = ConcreteAttacker()
        state = {"node_states": [0, 1, 2], "vulnerable": [0, 1]}

        action = attacker.select_action(state, current_time=0)

        assert isinstance(action, ActionType)
        assert action == ActionType.EXPLOIT

    def test_learn_interface(self):
        """Test that learn interface works correctly."""
        attacker = ConcreteAttacker()
        situation = (0, 1, 2)
        action = ActionType.EXPLOIT
        outcome = 1.0
        timestamp = 5
        confidence = 0.9

        # Should not raise any errors
        attacker.learn(situation, action, outcome, timestamp, confidence)

    def test_encode_situation_interface(self):
        """Test that _encode_situation interface works correctly."""
        attacker = ConcreteAttacker()
        state = {"node_states": [0, 1, 2]}

        situation = attacker._encode_situation(state)

        assert isinstance(situation, tuple)
        assert situation == (0, 1, 2)

    def test_overall_confidence_modification(self):
        """Test that overall_confidence can be modified."""
        attacker = ConcreteAttacker()
        attacker.overall_confidence = 0.75

        assert attacker.overall_confidence == 0.75

    def test_state_initialization_independence(self):
        """Test that multiple instances have independent state."""
        attacker1 = ConcreteAttacker()
        attacker2 = ConcreteAttacker()

        attacker1.known_nodes.add(1)
        attacker2.known_nodes.add(2)

        assert attacker1.known_nodes == {1}
        assert attacker2.known_nodes == {2}


class TestBaseDefender:
    """Test suite for BaseDefender abstract base class."""

    def test_cannot_instantiate_abstract_base_class(self):
        """Verify that BaseDefender cannot be directly instantiated."""
        with pytest.raises(TypeError, match="Can't instantiate abstract class"):
            BaseDefender(network=None)  # type: ignore

    def test_initialization_with_network(self):
        """Test defender initialization with network parameter."""
        network = {"nodes": 10, "edges": [(0, 1), (1, 2)]}
        defender = ConcreteDefender(network)

        assert defender.network == network
        assert defender.action_history == []

    def test_select_action_interface(self):
        """Test that select_action interface works correctly."""
        defender = ConcreteDefender(network={})
        state = {"node_states": [0, 1, 2]}
        attacker_knowledge = {0, 1}

        action = defender.select_action(state, attacker_knowledge)

        assert isinstance(action, ActionType)
        assert action == ActionType.MONITOR

    def test_action_history_tracking(self):
        """Test that action_history list can be modified."""
        defender = ConcreteDefender(network={})
        defender.action_history.append(ActionType.MONITOR)
        defender.action_history.append(ActionType.PATCH)

        assert defender.action_history == [ActionType.MONITOR, ActionType.PATCH]

    def test_deploy_acp_deception_default_empty(self):
        """Test that default deception returns empty dict."""
        defender = ConcreteDefender(network={})
        target_nodes = [1, 2, 3]
        current_time = 5
        attacker_knowledge = {0, 1}

        result = defender.deploy_acp_deception(target_nodes, current_time, attacker_knowledge)

        assert result == {}

    def test_get_action_distribution_empty_history(self):
        """Test action distribution with empty history."""
        defender = ConcreteDefender(network={})

        distribution = defender.get_action_distribution()

        assert distribution == {}

    def test_get_action_distribution_single_action(self):
        """Test action distribution with single action type."""
        defender = ConcreteDefender(network={})
        defender.action_history = [ActionType.MONITOR, ActionType.MONITOR, ActionType.MONITOR]

        distribution = defender.get_action_distribution()

        assert distribution == {ActionType.MONITOR: 1.0}

    def test_get_action_distribution_multiple_actions(self):
        """Test action distribution with multiple action types."""
        defender = ConcreteDefender(network={})
        defender.action_history = [
            ActionType.MONITOR,
            ActionType.MONITOR,
            ActionType.PATCH,
            ActionType.ISOLATE,
        ]

        distribution = defender.get_action_distribution()

        assert distribution[ActionType.MONITOR] == 0.5
        assert distribution[ActionType.PATCH] == 0.25
        assert distribution[ActionType.ISOLATE] == 0.25

    def test_get_action_distribution_equal_distribution(self):
        """Test action distribution with equal frequency."""
        defender = ConcreteDefender(network={})
        defender.action_history = [
            ActionType.MONITOR,
            ActionType.PATCH,
            ActionType.ISOLATE,
        ]

        distribution = defender.get_action_distribution()

        assert all(freq == pytest.approx(1.0 / 3) for freq in distribution.values())

    def test_state_initialization_independence(self):
        """Test that multiple instances have independent state."""
        defender1 = ConcreteDefender(network={"id": 1})
        defender2 = ConcreteDefender(network={"id": 2})

        defender1.action_history.append(ActionType.MONITOR)
        defender2.action_history.append(ActionType.PATCH)

        assert len(defender1.action_history) == 1
        assert len(defender2.action_history) == 1
        assert defender1.action_history[0] == ActionType.MONITOR
        assert defender2.action_history[0] == ActionType.PATCH


class TestBaseAttackerAbstractMethods:
    """Test suite for verifying abstract method requirements."""

    def test_missing_select_action_raises_error(self):
        """Test that missing select_action implementation raises error."""

        class IncompleteAttacker(BaseAttacker):
            def learn(self, situation, action, outcome, timestamp, confidence=1.0):
                pass

            def _encode_situation(self, state):
                return tuple()

        with pytest.raises(TypeError, match="Can't instantiate abstract class"):
            IncompleteAttacker()  # type: ignore

    def test_missing_learn_raises_error(self):
        """Test that missing learn implementation raises error."""

        class IncompleteAttacker(BaseAttacker):
            def select_action(self, state, current_time):
                return ActionType.EXPLOIT

            def _encode_situation(self, state):
                return tuple()

        with pytest.raises(TypeError, match="Can't instantiate abstract class"):
            IncompleteAttacker()  # type: ignore

    def test_missing_encode_situation_raises_error(self):
        """Test that missing _encode_situation implementation raises error."""

        class IncompleteAttacker(BaseAttacker):
            def select_action(self, state, current_time):
                return ActionType.EXPLOIT

            def learn(self, situation, action, outcome, timestamp, confidence=1.0):
                pass

        with pytest.raises(TypeError, match="Can't instantiate abstract class"):
            IncompleteAttacker()  # type: ignore


class TestBaseDefenderAbstractMethods:
    """Test suite for verifying abstract method requirements."""

    def test_missing_select_action_raises_error(self):
        """Test that missing select_action implementation raises error."""

        class IncompleteDefender(BaseDefender):
            pass

        with pytest.raises(TypeError, match="Can't instantiate abstract class"):
            IncompleteDefender(network={})  # type: ignore
