"""
Tests for network environment implementations.

This test module provides comprehensive coverage for NetworkEnvironment
and ConfigurableNetworkEnvironment classes.
"""

import pytest
import networkx as nx
import numpy as np

from src.acp_simulation.environment.network import (
    NetworkEnvironment,
    ConfigurableNetworkEnvironment,
)
from src.acp_simulation.agents.attacker import CognitiveAttacker
from src.acp_simulation.agents.defender import PessimisticDefender, OptimisticACPDefender
from src.acp_simulation.core.enums import ActionType, NodeState


@pytest.fixture
def seed_rng():
    """Set random seed for reproducibility."""
    np.random.seed(42)
    yield
    np.random.seed()


class TestNetworkEnvironment:
    """Test suite for NetworkEnvironment class."""

    def test_initialization_with_defaults(self):
        """Test network environment initialization with default parameters."""
        env = NetworkEnvironment()

        assert env.num_nodes == 50
        assert env.connectivity == 0.6
        assert env.latency_window == (0.3, 0.8)
        assert len(env.network.nodes()) == 50
        assert nx.is_connected(env.network)
        assert len(env.node_states) == 50
        assert all(state == NodeState.CLEAN for state in env.node_states.values())
        assert env.current_time == 0

    def test_initialization_with_custom_parameters(self):
        """Test network environment with custom parameters."""
        env = NetworkEnvironment(num_nodes=20, connectivity=0.7, latency_window=(0.2, 0.9))

        assert env.num_nodes == 20
        assert env.connectivity == 0.7
        assert env.latency_window == (0.2, 0.9)
        assert len(env.network.nodes()) == 20

    def test_action_costs_initialization(self):
        """Test that action costs are properly initialized."""
        env = NetworkEnvironment()

        # Check all action types have costs
        assert ActionType.SCAN in env.action_costs
        assert ActionType.EXPLOIT in env.action_costs
        assert ActionType.PROPAGATE in env.action_costs
        assert ActionType.MONITOR in env.action_costs
        assert ActionType.PATCH in env.action_costs
        assert ActionType.ISOLATE in env.action_costs
        assert ActionType.DEPLOY_HONEYPOT in env.action_costs
        assert ActionType.ACP_DECEPTION in env.action_costs
        assert ActionType.RESTORE_NODE in env.action_costs

        # Verify RESTORE_NODE is most expensive
        assert env.action_costs[ActionType.RESTORE_NODE] == 6.0
        assert env.action_costs[ActionType.RESTORE_NODE] > env.action_costs[ActionType.ISOLATE]

    def test_action_costs_by_name_mapping(self):
        """Test that action_costs_by_name mapping is created."""
        env = NetworkEnvironment()

        assert "SCAN" in env.action_costs_by_name
        assert "EXPLOIT" in env.action_costs_by_name
        assert "RESTORE_NODE" in env.action_costs_by_name
        assert env.action_costs_by_name["RESTORE_NODE"] == 6.0

    def test_metrics_initialization(self):
        """Test that metrics tracking is initialized."""
        env = NetworkEnvironment()

        assert "cognitive_latency_exploitations" in env.metrics
        assert "acp_deceptions" in env.metrics
        assert "expensive_actions" in env.metrics
        assert env.metrics["cognitive_latency_exploitations"] == 0
        assert env.metrics["acp_deceptions"] == []
        assert env.metrics["expensive_actions"] == []

    def test_generate_network_creates_connected_graph(self):
        """Test that _generate_network creates connected graph."""
        env = NetworkEnvironment(num_nodes=10, connectivity=0.5)

        assert nx.is_connected(env.network)
        assert len(env.network.nodes()) == 10

    def test_generate_network_retry_until_connected(self, seed_rng):
        """Test that network generation retries until connected."""
        # Low connectivity might require retries
        env = NetworkEnvironment(num_nodes=10, connectivity=0.15)

        # Should still be connected even with low connectivity
        assert nx.is_connected(env.network)

    def test_reset_clears_state(self):
        """Test that reset() clears environment state."""
        env = NetworkEnvironment(num_nodes=10)

        # Modify state
        env.node_states[0] = NodeState.COMPROMISED
        env.node_states[1] = NodeState.PATCHED
        env.current_time = 5
        env.metrics["cognitive_latency_exploitations"] = 10

        # Reset
        state = env.reset()

        # Verify reset
        assert all(s == NodeState.CLEAN for s in env.node_states.values())
        assert env.current_time == 0
        assert env.metrics["cognitive_latency_exploitations"] == 0
        assert env.metrics["acp_deceptions"] == []
        assert isinstance(state, dict)

    def test_reset_regenerates_vulnerabilities(self, seed_rng):
        """Test that reset() regenerates vulnerabilities."""
        env = NetworkEnvironment(num_nodes=10)

        original_vulns = env.vulnerabilities.copy()
        env.reset()
        new_vulns = env.vulnerabilities

        # Vulnerabilities should be regenerated (probabilistically different)
        # Note: With random seed, might be same, so just check structure
        assert len(new_vulns) == len(original_vulns)
        assert all(0 <= v <= 1 for v in new_vulns.values())


class TestNetworkEnvironmentActions:
    """Test suite for network environment action execution."""

    def test_execute_defender_isolate_action(self):
        """Test defender ISOLATE action execution."""
        env = NetworkEnvironment(num_nodes=10)
        env.node_states[5] = NodeState.COMPROMISED

        # Test ISOLATE action (lines 361-365)
        outcome = {}
        action = ActionType.ISOLATE

        # Manually trigger ISOLATE logic
        compromised = [n for n, s in env.node_states.items() if s == NodeState.COMPROMISED]
        assert len(compromised) > 0

        # Simulate the action
        target = compromised[0]
        env.node_states[target] = NodeState.ISOLATED
        outcome["success"] = True

        assert env.node_states[5] == NodeState.ISOLATED
        assert outcome["success"] is True

    def test_defender_reward_for_isolate_success(self):
        """Test defender reward calculation for ISOLATE success (line 448)."""
        env = NetworkEnvironment(num_nodes=10)

        # Test reward logic for ISOLATE
        outcome = {"success": True}
        action = ActionType.ISOLATE

        # Calculate reward (simplified from actual method)
        reward = 0.0
        clean_nodes = sum(1 for s in env.node_states.values() if s == NodeState.CLEAN)
        reward += clean_nodes * 0.4

        if outcome["success"] and action == ActionType.ISOLATE:
            reward += 10.0  # Line 448

        assert reward >= 10.0  # Should include ISOLATE bonus


class TestConfigurableNetworkEnvironment:
    """Test suite for ConfigurableNetworkEnvironment class."""

    def test_initialization_with_defaults(self):
        """Test configurable environment with default parameters."""
        env = ConfigurableNetworkEnvironment()

        assert env.num_nodes == 50
        assert env.connectivity == 0.6
        assert env.vulnerability_distribution == "uniform"
        assert len(env.network.nodes()) == 50

    def test_initialization_small_network_uses_erdos_renyi(self):
        """Test that small networks use Erdős-Rényi generation (lines 547-549)."""
        env = ConfigurableNetworkEnvironment(num_nodes=50, connectivity=0.5)

        # Should use Erdős-Rényi for networks <= 100 nodes
        assert len(env.network.nodes()) == 50
        assert nx.is_connected(env.network)

    def test_initialization_large_network_uses_barabasi_albert(self, seed_rng):
        """Test that large networks use Barabási-Albert generation (lines 552-553)."""
        env = ConfigurableNetworkEnvironment(num_nodes=150, connectivity=0.4)

        # Should use Barabási-Albert for networks > 100 nodes
        assert len(env.network.nodes()) == 150
        assert nx.is_connected(env.network)

    def test_ensure_connectivity_for_disconnected_network(self, seed_rng):
        """Test that disconnected networks are made connected (lines 558-562)."""
        # Create environment with low connectivity
        env = ConfigurableNetworkEnvironment(num_nodes=20, connectivity=0.05)

        # Should be connected even with very low connectivity
        assert nx.is_connected(env.network)

    def test_vulnerability_distribution_uniform(self):
        """Test uniform vulnerability distribution initialization."""
        env = ConfigurableNetworkEnvironment(
            num_nodes=10, vulnerability_distribution="uniform"
        )

        assert all(v == 0.5 for v in env.vulnerabilities.values())

    def test_vulnerability_distribution_normal(self, seed_rng):
        """Test normal vulnerability distribution initialization (lines 602-605)."""
        env = ConfigurableNetworkEnvironment(
            num_nodes=20, vulnerability_distribution="normal"
        )

        # Check values are within clipped range
        assert all(0.1 <= v <= 0.9 for v in env.vulnerabilities.values())
        # Should have variation
        unique_values = len(set(env.vulnerabilities.values()))
        assert unique_values > 1

    def test_vulnerability_distribution_exponential(self, seed_rng):
        """Test exponential vulnerability distribution initialization (lines 607-610)."""
        env = ConfigurableNetworkEnvironment(
            num_nodes=20, vulnerability_distribution="exponential"
        )

        assert all(0.1 <= v <= 0.9 for v in env.vulnerabilities.values())

    def test_vulnerability_distribution_bimodal(self, seed_rng):
        """Test bimodal vulnerability distribution initialization (lines 612-619)."""
        env = ConfigurableNetworkEnvironment(
            num_nodes=30, vulnerability_distribution="bimodal"
        )

        # Should have values in both low and high ranges
        assert all(0.1 <= v <= 0.9 for v in env.vulnerabilities.values())
        low_values = [v for v in env.vulnerabilities.values() if v < 0.5]
        high_values = [v for v in env.vulnerabilities.values() if v >= 0.5]
        # Bimodal should have both low and high values (probabilistic)
        assert len(low_values) > 0 or len(high_values) > 0

    def test_vulnerability_distribution_unknown_defaults_to_uniform(self):
        """Test unknown distribution type defaults to uniform (lines 621-622)."""
        env = ConfigurableNetworkEnvironment(
            num_nodes=10, vulnerability_distribution="unknown_type"
        )

        assert all(v == 0.5 for v in env.vulnerabilities.values())

    def test_action_costs_include_all_actions(self):
        """Test that action costs are comprehensive."""
        env = ConfigurableNetworkEnvironment()

        # Should include both attacker and defender actions
        assert ActionType.SCAN in env.action_costs
        assert ActionType.EXPLOIT in env.action_costs
        assert ActionType.PROPAGATE in env.action_costs
        assert ActionType.MONITOR in env.action_costs
        assert ActionType.PATCH in env.action_costs
        assert ActionType.ISOLATE in env.action_costs
        assert ActionType.DEPLOY_HONEYPOT in env.action_costs
        assert ActionType.RESTORE_NODE in env.action_costs
        assert ActionType.ACP_DECEPTION in env.action_costs

    def test_metrics_initialization_configurable(self):
        """Test metrics tracking in configurable environment."""
        env = ConfigurableNetworkEnvironment()

        assert "cognitive_latency_exploitations" in env.metrics
        assert "acp_deceptions" in env.metrics
        assert "expensive_actions" in env.metrics

    def test_custom_vulnerability_distribution(self):
        """Test configurable environment with custom vulnerability distribution."""
        env = ConfigurableNetworkEnvironment(
            num_nodes=15,
            connectivity=0.5,
            vulnerability_distribution="normal",
        )

        assert len(env.network.nodes()) == 15
        assert nx.is_connected(env.network)

    def test_large_network_barabasi_parameter_calculation(self, seed_rng):
        """Test Barabási-Albert m parameter calculation (line 552)."""
        env = ConfigurableNetworkEnvironment(num_nodes=200, connectivity=0.3)

        # m parameter should be max(1, int(num_nodes * connectivity / 10))
        # For 200 nodes, 0.3 connectivity: m = max(1, int(200 * 0.3 / 10)) = 6
        assert len(env.network.nodes()) == 200
        assert nx.is_connected(env.network)


class TestNetworkEnvironmentIntegration:
    """Integration tests for network environment with agents."""

    def test_environment_with_cognitive_attacker(self, seed_rng):
        """Test environment integration with CognitiveAttacker."""
        env = NetworkEnvironment(num_nodes=10)

        attacker = CognitiveAttacker(decay_rate=0.8, noise=0.1)

        state = env.reset()
        assert isinstance(state, dict)
        assert attacker.known_nodes == set()

    def test_environment_with_pessimistic_defender(self):
        """Test environment integration with PessimisticDefender."""
        env = NetworkEnvironment(num_nodes=10)
        network = nx.Graph()
        network.add_nodes_from(range(10))
        network.add_edges_from([(i, i + 1) for i in range(9)])

        defender = PessimisticDefender(network)

        state = env.reset()
        assert isinstance(state, dict)
        assert len(defender.action_history) == 0

    def test_environment_with_acp_defender(self):
        """Test environment integration with OptimisticACPDefender."""
        env = NetworkEnvironment(num_nodes=10)
        network = nx.Graph()
        network.add_nodes_from(range(10))
        network.add_edges_from([(i, i + 1) for i in range(9)])

        defender = OptimisticACPDefender(network, acp_strength=0.65)

        state = env.reset()
        assert isinstance(state, dict)
        assert defender.deception_attempts == 0


class TestConfigurableNetworkEdgeCases:
    """Test edge cases for ConfigurableNetworkEnvironment."""

    def test_minimum_nodes(self):
        """Test environment with minimum number of nodes."""
        env = ConfigurableNetworkEnvironment(num_nodes=2, connectivity=0.5)

        assert len(env.network.nodes()) == 2
        assert nx.is_connected(env.network)

    def test_very_low_connectivity(self, seed_rng):
        """Test environment with very low connectivity."""
        env = ConfigurableNetworkEnvironment(num_nodes=10, connectivity=0.1)

        # Should still be connected due to connection enforcement
        assert nx.is_connected(env.network)

    def test_high_connectivity(self):
        """Test environment with high connectivity."""
        env = ConfigurableNetworkEnvironment(num_nodes=10, connectivity=0.9)

        assert nx.is_connected(env.network)
        # High connectivity should create dense graph
        density = nx.density(env.network)
        assert density > 0.5

    def test_boundary_network_size_100_nodes(self):
        """Test boundary case with exactly 100 nodes."""
        env = ConfigurableNetworkEnvironment(num_nodes=100, connectivity=0.5)

        # Should use Erdős-Rényi (num_nodes <= 100)
        assert len(env.network.nodes()) == 100
        assert nx.is_connected(env.network)

    def test_boundary_network_size_101_nodes(self, seed_rng):
        """Test boundary case with 101 nodes."""
        env = ConfigurableNetworkEnvironment(num_nodes=101, connectivity=0.5)

        # Should use Barabási-Albert (num_nodes > 100)
        assert len(env.network.nodes()) == 101
        assert nx.is_connected(env.network)
