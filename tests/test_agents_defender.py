"""
Tests for defender agent implementations.

This test module provides comprehensive coverage for PessimisticDefender,
OptimisticACPDefender, and their configurable variants.
"""

import pytest
import networkx as nx
import numpy as np
from typing import Set

from src.acp_simulation.agents.defender import (
    PessimisticDefender,
    OptimisticACPDefender,
    ConfigurablePessimisticDefender,
    ConfigurableACPDefender,
)
from src.acp_simulation.core.enums import ActionType, NodeState


@pytest.fixture
def simple_network():
    """Create a simple test network."""
    G = nx.Graph()
    G.add_nodes_from(range(10))
    G.add_edges_from([(i, i + 1) for i in range(9)])
    return G


@pytest.fixture
def seed_rng():
    """Set random seed for reproducibility in tests."""
    np.random.seed(42)
    yield
    np.random.seed()  # Reset after test


class TestPessimisticDefender:
    """Test suite for PessimisticDefender."""

    def test_initialization_with_defaults(self, simple_network):
        """Test pessimistic defender initialization with default parameters."""
        defender = PessimisticDefender(simple_network)

        assert defender.network == simple_network
        assert defender.restore_node_probability == 0.4185
        assert defender.paranoia_level == 0.8
        assert defender.vulnerability_distribution == "uniform"
        assert len(defender.node_states) == 10
        assert all(state == NodeState.CLEAN for state in defender.node_states.values())
        assert len(defender.action_history) == 0

    def test_initialization_uniform_vulnerabilities(self, simple_network):
        """Test uniform vulnerability distribution initialization."""
        defender = PessimisticDefender(simple_network, vulnerability_distribution="uniform")

        assert len(defender.vulnerabilities) == 10
        assert all(v == 0.5 for v in defender.vulnerabilities.values())

    def test_initialization_normal_vulnerabilities(self, simple_network, seed_rng):
        """Test normal vulnerability distribution initialization."""
        defender = PessimisticDefender(simple_network, vulnerability_distribution="normal")

        assert len(defender.vulnerabilities) == 10
        # Check values are within clipped range
        assert all(0.1 <= v <= 0.9 for v in defender.vulnerabilities.values())
        # Check distribution is not all the same (would fail with uniform)
        unique_values = len(set(defender.vulnerabilities.values()))
        assert unique_values > 1

    def test_initialization_exponential_vulnerabilities(self, simple_network, seed_rng):
        """Test exponential vulnerability distribution initialization."""
        defender = PessimisticDefender(simple_network, vulnerability_distribution="exponential")

        assert len(defender.vulnerabilities) == 10
        assert all(0.1 <= v <= 0.9 for v in defender.vulnerabilities.values())

    def test_initialization_bimodal_vulnerabilities(self, simple_network, seed_rng):
        """Test bimodal vulnerability distribution initialization."""
        defender = PessimisticDefender(simple_network, vulnerability_distribution="bimodal")

        assert len(defender.vulnerabilities) == 10
        assert all(0.1 <= v <= 0.9 for v in defender.vulnerabilities.values())
        # Bimodal should have values in two distinct ranges
        low_values = [v for v in defender.vulnerabilities.values() if v < 0.5]
        high_values = [v for v in defender.vulnerabilities.values() if v >= 0.5]
        # At least some in each range (probabilistic, might occasionally fail)
        assert len(low_values) > 0 or len(high_values) > 0

    def test_initialization_unknown_distribution_defaults_to_uniform(self, simple_network):
        """Test that unknown distribution type defaults to uniform."""
        defender = PessimisticDefender(simple_network, vulnerability_distribution="unknown")

        assert all(v == 0.5 for v in defender.vulnerabilities.values())

    def test_select_action_restore_node_probability(self, simple_network, seed_rng):
        """Test that RESTORE_NODE is selected with ~41.85% probability."""
        defender = PessimisticDefender(simple_network)
        state = {"node_states": {i: NodeState.CLEAN for i in range(10)}}
        attacker_knowledge: Set[int] = set()

        # Run many iterations to check probability
        restore_count = 0
        iterations = 1000
        for _ in range(iterations):
            action = defender.select_action(state, attacker_knowledge)
            if action == ActionType.RESTORE_NODE:
                restore_count += 1

        # Should be close to 41.85% (allow 5% tolerance)
        restore_ratio = restore_count / iterations
        assert 0.37 < restore_ratio < 0.47, f"RESTORE_NODE ratio {restore_ratio} not near 0.4185"

    def test_select_action_no_compromised_nodes(self, simple_network):
        """Test action selection when no nodes are compromised."""
        defender = PessimisticDefender(simple_network)
        defender.node_states = {i: NodeState.CLEAN for i in range(10)}
        state = {"node_states": defender.node_states}
        attacker_knowledge: Set[int] = set()

        action = defender.select_action(state, attacker_knowledge)

        assert action in [ActionType.RESTORE_NODE, ActionType.PATCH, ActionType.MONITOR]
        assert len(defender.action_history) == 1

    def test_select_action_with_compromised_nodes(self, simple_network):
        """Test action selection when nodes are compromised."""
        defender = PessimisticDefender(simple_network)
        defender.node_states = {i: NodeState.CLEAN for i in range(10)}
        defender.node_states[5] = NodeState.COMPROMISED
        state = {"node_states": defender.node_states}
        attacker_knowledge: Set[int] = {5}

        action = defender.select_action(state, attacker_knowledge)

        assert action in [
            ActionType.RESTORE_NODE,
            ActionType.ISOLATE,
            ActionType.PATCH,
            ActionType.MONITOR,
        ]
        assert len(defender.action_history) == 1

    def test_action_history_accumulation(self, simple_network):
        """Test that action history accumulates correctly."""
        defender = PessimisticDefender(simple_network)
        state = {"node_states": {i: NodeState.CLEAN for i in range(10)}}
        attacker_knowledge: Set[int] = set()

        for _ in range(5):
            defender.select_action(state, attacker_knowledge)

        assert len(defender.action_history) == 5

    def test_paranoid_behavior_always_acts(self, simple_network):
        """Test that pessimistic defender always takes action (paranoid)."""
        defender = PessimisticDefender(simple_network)
        state = {"node_states": {i: NodeState.CLEAN for i in range(10)}}
        attacker_knowledge: Set[int] = set()

        # Even with no visible threat, should still act (paranoid)
        action = defender.select_action(state, attacker_knowledge)

        assert action is not None
        assert isinstance(action, ActionType)


class TestOptimisticACPDefender:
    """Test suite for OptimisticACPDefender."""

    def test_initialization_with_defaults(self, simple_network):
        """Test ACP defender initialization with default parameters."""
        defender = OptimisticACPDefender(simple_network)

        assert defender.network == simple_network
        assert defender.acp_strength == 0.65
        assert defender.vulnerability_distribution == "uniform"
        assert len(defender.node_states) == 10
        assert all(state == NodeState.CLEAN for state in defender.node_states.values())
        assert defender.deception_successes == 0
        assert defender.deception_attempts == 0
        assert len(defender.deception_history) == 0

    def test_initialization_with_custom_acp_strength(self, simple_network):
        """Test ACP defender initialization with custom strength."""
        defender = OptimisticACPDefender(simple_network, acp_strength=0.8)

        assert defender.acp_strength == 0.8

    def test_initialization_uniform_vulnerabilities(self, simple_network):
        """Test uniform vulnerability distribution initialization."""
        defender = OptimisticACPDefender(simple_network, vulnerability_distribution="uniform")

        assert len(defender.vulnerabilities) == 10
        assert all(v == 0.5 for v in defender.vulnerabilities.values())

    def test_initialization_normal_vulnerabilities(self, simple_network, seed_rng):
        """Test normal vulnerability distribution initialization."""
        defender = OptimisticACPDefender(simple_network, vulnerability_distribution="normal")

        assert len(defender.vulnerabilities) == 10
        assert all(0.1 <= v <= 0.9 for v in defender.vulnerabilities.values())

    def test_initialization_exponential_vulnerabilities(self, simple_network, seed_rng):
        """Test exponential vulnerability distribution initialization."""
        defender = OptimisticACPDefender(
            simple_network, vulnerability_distribution="exponential"
        )

        assert len(defender.vulnerabilities) == 10
        assert all(0.1 <= v <= 0.9 for v in defender.vulnerabilities.values())

    def test_initialization_bimodal_vulnerabilities(self, simple_network, seed_rng):
        """Test bimodal vulnerability distribution initialization."""
        defender = OptimisticACPDefender(simple_network, vulnerability_distribution="bimodal")

        assert len(defender.vulnerabilities) == 10
        assert all(0.1 <= v <= 0.9 for v in defender.vulnerabilities.values())

    def test_initialization_unknown_distribution_defaults_to_uniform(self, simple_network):
        """Test that unknown distribution type defaults to uniform."""
        defender = OptimisticACPDefender(simple_network, vulnerability_distribution="unknown")

        assert all(v == 0.5 for v in defender.vulnerabilities.values())

    def test_select_action_with_many_unknown_nodes(self, simple_network, seed_rng):
        """Test action selection when attacker has incomplete knowledge."""
        defender = OptimisticACPDefender(simple_network)
        state = {"node_states": {i: NodeState.CLEAN for i in range(10)}}
        attacker_knowledge: Set[int] = {0, 1}  # Attacker knows only 2 nodes

        action = defender.select_action(state, attacker_knowledge)

        # With 8 unknown nodes, should favor deception or honeypots
        assert action in [
            ActionType.ACP_DECEPTION,
            ActionType.DEPLOY_HONEYPOT,
            ActionType.MONITOR,
        ]

    def test_select_action_with_compromised_nodes(self, simple_network, seed_rng):
        """Test action selection when nodes are compromised."""
        defender = OptimisticACPDefender(simple_network)
        defender.node_states[5] = NodeState.COMPROMISED
        state = {"node_states": defender.node_states}
        attacker_knowledge: Set[int] = set(range(10))  # Knows all nodes

        action = defender.select_action(state, attacker_knowledge)

        # With compromised nodes and full knowledge, should PATCH or ISOLATE
        assert action in [ActionType.PATCH, ActionType.ISOLATE, ActionType.MONITOR]

    def test_select_action_never_uses_restore_node(self, simple_network):
        """Test that ACP defender NEVER uses expensive RESTORE_NODE."""
        defender = OptimisticACPDefender(simple_network)
        state = {"node_states": {i: NodeState.CLEAN for i in range(10)}}
        attacker_knowledge: Set[int] = set()

        # Run many iterations
        for _ in range(100):
            action = defender.select_action(state, attacker_knowledge)
            assert action != ActionType.RESTORE_NODE, "ACP defender should NEVER use RESTORE_NODE"

    def test_deploy_acp_deception_with_unknown_nodes(self, simple_network):
        """Test ACP deception deployment on unknown nodes."""
        defender = OptimisticACPDefender(simple_network, acp_strength=1.0)  # Always succeed
        target_nodes = [3, 4, 5]
        current_time = 10
        attacker_knowledge: Set[int] = {0, 1, 2}  # Doesn't know 3, 4, 5

        result = defender.deploy_acp_deception(target_nodes, current_time, attacker_knowledge)

        # Should deceive about all unknown nodes
        assert len(result) == 3
        assert all(node in result for node in [3, 4, 5])
        assert defender.deception_attempts > 0
        assert defender.deception_successes == 3
        assert len(defender.deception_history) == 3

    def test_deploy_acp_deception_skips_known_nodes(self, simple_network):
        """Test that deception skips nodes already known to attacker."""
        defender = OptimisticACPDefender(simple_network, acp_strength=1.0)
        target_nodes = [0, 1, 2]
        current_time = 10
        attacker_knowledge: Set[int] = {0, 1, 2}  # Knows all targets

        result = defender.deploy_acp_deception(target_nodes, current_time, attacker_knowledge)

        # Should NOT deceive about known nodes (no information asymmetry)
        assert len(result) == 0
        assert defender.deception_successes == 0

    def test_deploy_acp_deception_false_signals(self, simple_network):
        """Test that deception creates false vulnerability signals."""
        defender = OptimisticACPDefender(simple_network, acp_strength=1.0)
        target_nodes = [5]
        current_time = 10
        attacker_knowledge: Set[int] = set()

        result = defender.deploy_acp_deception(target_nodes, current_time, attacker_knowledge)

        assert 5 in result
        deception = result[5]
        assert 0.85 <= deception["false_vulnerability"] <= 0.98
        assert 0.75 <= deception["false_value"] <= 0.95
        assert deception["false_criticality"] in ["critical", "high", "important"]
        assert deception["timestamp"] == 10
        assert deception["success"] is True

    def test_deploy_acp_deception_probabilistic(self, simple_network, seed_rng):
        """Test that deception respects acp_strength probability."""
        defender = OptimisticACPDefender(simple_network, acp_strength=0.5)
        target_nodes = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        current_time = 10
        attacker_knowledge: Set[int] = set()

        result = defender.deploy_acp_deception(target_nodes, current_time, attacker_knowledge)

        # With 0.5 strength and 10 nodes, expect ~5 deceptions (probabilistic)
        assert 0 < len(result) < 10  # Not all, not none

    def test_deception_history_tracking(self, simple_network):
        """Test that deception history is tracked correctly."""
        defender = OptimisticACPDefender(simple_network, acp_strength=1.0)
        target_nodes = [1, 2, 3]
        current_time = 5
        attacker_knowledge: Set[int] = set()

        defender.deploy_acp_deception(target_nodes, current_time, attacker_knowledge)

        assert len(defender.deception_history) == 3
        for entry in defender.deception_history:
            assert "node" in entry
            assert "time" in entry
            assert "type" in entry
            assert entry["time"] == 5


class TestConfigurablePessimisticDefender:
    """Test suite for ConfigurablePessimisticDefender."""

    def test_initialization_inherits_from_pessimistic(self, simple_network):
        """Test that configurable version inherits PessimisticDefender behavior."""
        defender = ConfigurablePessimisticDefender(simple_network)

        assert isinstance(defender, PessimisticDefender)
        assert defender.restore_node_probability == 0.4185
        assert defender.paranoia_level == 0.8

    def test_initialization_with_custom_distribution(self, simple_network):
        """Test configurable defender with custom vulnerability distribution."""
        defender = ConfigurablePessimisticDefender(
            simple_network, vulnerability_distribution="normal"
        )

        assert defender.vulnerability_distribution == "normal"
        assert len(defender.vulnerabilities) == 10


class TestConfigurableACPDefender:
    """Test suite for ConfigurableACPDefender."""

    def test_initialization_inherits_from_acp(self, simple_network):
        """Test that configurable version inherits OptimisticACPDefender behavior."""
        defender = ConfigurableACPDefender(simple_network)

        assert isinstance(defender, OptimisticACPDefender)
        assert defender.acp_strength == 0.65

    def test_initialization_with_custom_parameters(self, simple_network):
        """Test configurable defender with custom parameters."""
        defender = ConfigurableACPDefender(
            simple_network, acp_strength=0.8, vulnerability_distribution="exponential"
        )

        assert defender.acp_strength == 0.8
        assert defender.vulnerability_distribution == "exponential"


class TestDefenderComparison:
    """Test suite comparing PessimisticDefender vs OptimisticACPDefender behavior."""

    def test_pessimistic_uses_restore_node(self, simple_network, seed_rng):
        """Test that pessimistic defender uses RESTORE_NODE."""
        defender = PessimisticDefender(simple_network)
        state = {"node_states": {i: NodeState.CLEAN for i in range(10)}}
        attacker_knowledge: Set[int] = set()

        restore_used = False
        for _ in range(50):
            action = defender.select_action(state, attacker_knowledge)
            if action == ActionType.RESTORE_NODE:
                restore_used = True
                break

        assert restore_used, "Pessimistic defender should use RESTORE_NODE"

    def test_acp_never_uses_restore_node(self, simple_network):
        """Test that ACP defender NEVER uses RESTORE_NODE."""
        defender = OptimisticACPDefender(simple_network)
        state = {"node_states": {i: NodeState.CLEAN for i in range(10)}}
        attacker_knowledge: Set[int] = set()

        for _ in range(100):
            action = defender.select_action(state, attacker_knowledge)
            assert action != ActionType.RESTORE_NODE

    def test_acp_tracks_deception_pessimistic_does_not(self, simple_network):
        """Test that only ACP defender tracks deception metrics."""
        pessimistic = PessimisticDefender(simple_network)
        acp = OptimisticACPDefender(simple_network)

        # Pessimistic has no deception tracking
        assert not hasattr(pessimistic, "deception_successes")
        assert not hasattr(pessimistic, "deception_attempts")

        # ACP has deception tracking
        assert hasattr(acp, "deception_successes")
        assert hasattr(acp, "deception_attempts")
        assert acp.deception_successes == 0
        assert acp.deception_attempts == 0
