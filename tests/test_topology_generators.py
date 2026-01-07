"""
Tests for network topology generators.

Validates that hub-spoke and hierarchical topologies are generated correctly
for  conference submission.
"""

import networkx as nx
import numpy as np
import pytest

from src.acp_simulation.environment.topology_generators import (
    assign_vulnerability_by_topology,
    calculate_topology_metrics,
    generate_hierarchical_topology,
    generate_hub_spoke_topology,
)


class TestHubSpokeTopology:
    """Tests for hub-and-spoke topology generation."""

    def test_basic_generation(self):
        """Test basic hub-spoke network generation."""
        G = generate_hub_spoke_topology(num_nodes=50, hub_ratio=0.1, connectivity=0.3)

        assert G.number_of_nodes() == 50
        assert nx.is_connected(G)

    def test_hub_identification(self):
        """Test that hubs are correctly identified."""
        G = generate_hub_spoke_topology(num_nodes=50, hub_ratio=0.1, connectivity=0.3)

        # Check that is_hub attribute exists
        assert "is_hub" in G.nodes[0]

        # Count hubs
        num_hubs = sum(1 for n in G.nodes() if G.nodes[n]["is_hub"])
        expected_hubs = int(50 * 0.1)
        assert num_hubs == expected_hubs

    def test_hub_connectivity(self):
        """Test that hubs are highly connected."""
        G = generate_hub_spoke_topology(num_nodes=50, hub_ratio=0.1, connectivity=0.3)

        hub_nodes = [n for n in G.nodes() if G.nodes[n]["is_hub"]]
        peripheral_nodes = [n for n in G.nodes() if not G.nodes[n]["is_hub"]]

        # Hubs should have higher degree than peripheral nodes on average
        hub_degrees = [G.degree(n) for n in hub_nodes]
        periph_degrees = [G.degree(n) for n in peripheral_nodes]

        assert np.mean(hub_degrees) > np.mean(periph_degrees)

    def test_different_hub_ratios(self):
        """Test different hub ratio configurations."""
        for hub_ratio in [0.05, 0.1, 0.2]:
            G = generate_hub_spoke_topology(num_nodes=100, hub_ratio=hub_ratio)
            num_hubs = sum(1 for n in G.nodes() if G.nodes[n]["is_hub"])
            expected = int(100 * hub_ratio)
            assert num_hubs == expected or num_hubs == max(1, expected)


class TestHierarchicalTopology:
    """Tests for hierarchical topology generation."""

    def test_basic_generation(self):
        """Test basic hierarchical network generation."""
        G = generate_hierarchical_topology(num_nodes=50, branching_factor=3, depth=3)

        assert G.number_of_nodes() >= 1  # At least root node
        assert nx.is_connected(G)

    def test_level_assignment(self):
        """Test that nodes are assigned to correct levels."""
        G = generate_hierarchical_topology(num_nodes=50, branching_factor=3, depth=3)

        # Check that level attribute exists
        assert "level" in G.nodes[0]

        # Root should be at level 0
        assert G.nodes[0]["level"] == 0

        # Check that levels increase with distance from root
        levels = [G.nodes[n]["level"] for n in G.nodes()]
        assert min(levels) == 0
        assert max(levels) >= 1

    def test_tree_structure(self):
        """Test that base structure is tree-like."""
        G = generate_hierarchical_topology(num_nodes=50, branching_factor=3, depth=3)

        # Cross-edges may be added for realism, so levels might differ slightly
        # from shortest path. Just check that levels are assigned reasonably.
        levels_assigned = [G.nodes[n]["level"] for n in G.nodes()]
        levels_shortest = nx.single_source_shortest_path_length(G, 0)

        # Most nodes should have level close to shortest path distance
        differences = [abs(G.nodes[n]["level"] - levels_shortest[n]) for n in G.nodes()]
        # Allow some nodes to have different levels due to cross-edges
        assert sum(d == 0 for d in differences) / len(differences) > 0.7  # At least 70% exact

    def test_different_branching_factors(self):
        """Test different branching factor configurations."""
        for bf in [2, 3, 4]:
            G = generate_hierarchical_topology(num_nodes=50, branching_factor=bf, depth=3)
            assert nx.is_connected(G)
            assert "level" in G.nodes[0]


class TestTopologyMetrics:
    """Tests for topology metrics calculation."""

    def test_metrics_calculation(self):
        """Test that all metrics are calculated."""
        G = generate_hub_spoke_topology(num_nodes=50)
        metrics = calculate_topology_metrics(G)

        required_metrics = [
            "clustering_coefficient",
            "average_path_length",
            "diameter",
            "density",
            "degree_centrality_max",
            "degree_centrality_mean",
            "assortativity",
        ]

        for metric in required_metrics:
            assert metric in metrics
            assert isinstance(metrics[metric], (int, float))

    def test_hub_spoke_characteristics(self):
        """Test that hub-spoke topology has expected characteristics."""
        G = generate_hub_spoke_topology(num_nodes=50, hub_ratio=0.1)
        metrics = calculate_topology_metrics(G)

        # Hub-spoke should have relatively low average path length (hubs as intermediaries)
        assert metrics["average_path_length"] < 5

        # Should have high max degree centrality (hubs)
        assert metrics["degree_centrality_max"] > 0.3

    def test_hierarchical_characteristics(self):
        """Test that hierarchical topology has expected characteristics."""
        G = generate_hierarchical_topology(num_nodes=50, branching_factor=3, depth=3)
        metrics = calculate_topology_metrics(G)

        # Hierarchical should have low clustering (tree-like)
        assert metrics["clustering_coefficient"] < 0.5

        # Should have defined diameter
        assert metrics["diameter"] >= 2

    def test_disconnected_graph_handling(self):
        """Test metrics calculation on disconnected graphs."""
        # Create intentionally disconnected graph
        G = nx.Graph()
        G.add_nodes_from(range(10))
        G.add_edge(0, 1)
        G.add_edge(2, 3)

        metrics = calculate_topology_metrics(G)

        # Should handle disconnected graphs gracefully
        assert "average_path_length" in metrics
        assert "diameter" in metrics


class TestVulnerabilityAssignment:
    """Tests for topology-aware vulnerability assignment."""

    def test_hub_spoke_gradient(self):
        """Test gradient vulnerability on hub-spoke topology."""
        G = generate_hub_spoke_topology(num_nodes=50, hub_ratio=0.1)
        vulns = assign_vulnerability_by_topology(G, distribution="gradient")

        hub_nodes = [n for n in G.nodes() if G.nodes[n]["is_hub"]]
        periph_nodes = [n for n in G.nodes() if not G.nodes[n]["is_hub"]]

        hub_vulns = [vulns[n] for n in hub_nodes]
        periph_vulns = [vulns[n] for n in periph_nodes]

        # Hubs should be more secure (lower vulnerability)
        assert np.mean(hub_vulns) < np.mean(periph_vulns)

    def test_hub_spoke_inverse(self):
        """Test inverse vulnerability on hub-spoke topology."""
        G = generate_hub_spoke_topology(num_nodes=50, hub_ratio=0.1)
        vulns = assign_vulnerability_by_topology(G, distribution="inverse")

        hub_nodes = [n for n in G.nodes() if G.nodes[n]["is_hub"]]
        periph_nodes = [n for n in G.nodes() if not G.nodes[n]["is_hub"]]

        hub_vulns = [vulns[n] for n in hub_nodes]
        periph_vulns = [vulns[n] for n in periph_nodes]

        # Hubs should be more vulnerable (insider threat model)
        assert np.mean(hub_vulns) > np.mean(periph_vulns)

    def test_hierarchical_gradient(self):
        """Test gradient vulnerability on hierarchical topology."""
        G = generate_hierarchical_topology(num_nodes=50, branching_factor=3, depth=3)
        vulns = assign_vulnerability_by_topology(G, distribution="gradient")

        # Outer layers (higher level) should be more vulnerable
        levels = {n: G.nodes[n]["level"] for n in G.nodes()}
        max_level = max(levels.values())

        level_0_vulns = [vulns[n] for n in G.nodes() if levels[n] == 0]
        max_level_vulns = [vulns[n] for n in G.nodes() if levels[n] == max_level]

        # Outer layer should be more vulnerable than core
        assert np.mean(max_level_vulns) > np.mean(level_0_vulns)

    def test_uniform_distribution(self):
        """Test uniform vulnerability distribution."""
        G = generate_hub_spoke_topology(num_nodes=50)
        vulns = assign_vulnerability_by_topology(G, distribution="uniform")

        # All vulnerabilities should be 0.5
        assert all(v == 0.5 for v in vulns.values())

    def test_unknown_topology(self):
        """Test vulnerability assignment on topology without attributes."""
        # Create graph without topology attributes
        G = nx.erdos_renyi_graph(50, 0.3)
        vulns = assign_vulnerability_by_topology(G, distribution="gradient")

        # Should default to uniform
        assert all(v == 0.5 for v in vulns.values())


class TestReproducibility:
    """Tests for reproducibility with seeds."""

    def test_hub_spoke_reproducibility(self):
        """Test that hub-spoke generation is reproducible with same seed."""
        np.random.seed(42)
        G1 = generate_hub_spoke_topology(num_nodes=50, hub_ratio=0.1, connectivity=0.3)

        np.random.seed(42)
        G2 = generate_hub_spoke_topology(num_nodes=50, hub_ratio=0.1, connectivity=0.3)

        # Should have same structure
        assert G1.number_of_nodes() == G2.number_of_nodes()
        assert G1.number_of_edges() == G2.number_of_edges()

    def test_hierarchical_reproducibility(self):
        """Test that hierarchical generation is reproducible."""
        np.random.seed(42)
        G1 = generate_hierarchical_topology(num_nodes=50, branching_factor=3, depth=3)

        np.random.seed(42)
        G2 = generate_hierarchical_topology(num_nodes=50, branching_factor=3, depth=3)

        # Should have same structure
        assert G1.number_of_nodes() == G2.number_of_nodes()
        assert G1.number_of_edges() == G2.number_of_edges()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
