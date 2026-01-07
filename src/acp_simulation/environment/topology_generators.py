"""
Network topology generators for enterprise-realistic cyber environments.

This module provides topology generation functions for creating realistic
network structures beyond simple random graphs:
- Hub-and-spoke (star topologies)
- Hierarchical (tree structures with DMZ, internal, endpoints)
- Topology metrics calculation
"""

from typing import Dict, List, Tuple

import networkx as nx
import numpy as np


def generate_hub_spoke_topology(
    num_nodes: int, hub_ratio: float = 0.1, connectivity: float = 0.6
) -> nx.Graph:
    """
    Generate a hub-and-spoke (star) network topology.

    Typical of corporate networks with server-client architecture:
    - Small number of hub nodes (servers, critical infrastructure)
    - Large number of peripheral nodes (clients, endpoints)
    - Hubs are highly connected, periphery connects primarily to hubs

    Parameters
    ----------
    num_nodes : int
        Total number of nodes in the network
    hub_ratio : float, default=0.1
        Fraction of nodes that are hubs (0.0-1.0)
    connectivity : float, default=0.6
        Base connectivity for additional edges beyond hub-spoke structure

    Returns
    -------
    nx.Graph
        Hub-spoke network topology

    Notes
    -----
    Network structure:
    - Hub nodes: First hub_ratio * num_nodes nodes
    - Peripheral nodes: Remaining nodes
    - Each peripheral node connects to at least one random hub
    - Hubs are fully connected to each other (create a core)
    - Additional random edges added based on connectivity parameter

    Examples
    --------
    >>> G = generate_hub_spoke_topology(50, hub_ratio=0.1, connectivity=0.3)
    >>> # Creates network with 5 hubs, 45 peripheral nodes
    """
    G = nx.Graph()
    G.add_nodes_from(range(num_nodes))

    # Determine hub and peripheral nodes
    num_hubs = max(1, int(num_nodes * hub_ratio))
    hub_nodes = list(range(num_hubs))
    peripheral_nodes = list(range(num_hubs, num_nodes))

    # Step 1: Create fully-connected hub core
    for i in range(len(hub_nodes)):
        for j in range(i + 1, len(hub_nodes)):
            G.add_edge(hub_nodes[i], hub_nodes[j])

    # Step 2: Connect each peripheral node to 1-3 random hubs
    for periph in peripheral_nodes:
        num_connections = min(len(hub_nodes), np.random.randint(1, 4))
        connected_hubs = np.random.choice(hub_nodes, size=num_connections, replace=False)
        for hub in connected_hubs:
            G.add_edge(periph, hub)

    # Step 3: Add random edges between peripheral nodes for realism
    # Based on connectivity parameter
    num_additional_edges = int(connectivity * len(peripheral_nodes) * 2)
    for _ in range(num_additional_edges):
        if len(peripheral_nodes) < 2:
            break
        node1, node2 = np.random.choice(peripheral_nodes, size=2, replace=False)
        if not G.has_edge(node1, node2):
            G.add_edge(node1, node2)

    # Mark hub nodes as node attribute for vulnerability assignment
    nx.set_node_attributes(G, {node: (node in hub_nodes) for node in G.nodes()}, "is_hub")

    return G


def generate_hierarchical_topology(
    num_nodes: int, branching_factor: int = 3, depth: int = 3
) -> nx.Graph:
    """
    Generate a hierarchical (tree) network topology.

    Typical of enterprise networks with security zones:
    - Level 0: DMZ / Internet-facing (most vulnerable)
    - Level 1: Internal services
    - Level 2: Workstations / Endpoints

    Parameters
    ----------
    num_nodes : int
        Total number of nodes (will be adjusted to fit tree structure)
    branching_factor : int, default=3
        Number of children per parent node
    depth : int, default=3
        Depth of the tree (number of levels)

    Returns
    -------
    nx.Graph
        Hierarchical tree topology

    Notes
    -----
    Network structure:
    - Tree with configurable branching factor and depth
    - Each node connects to its parent and children
    - Cross-level connections added for realism (e.g., workstation to DMZ service)
    - Nodes labeled by level for vulnerability gradient assignment

    The actual number of nodes will be:
    sum(branching_factor^i for i in range(depth))
    which may differ from num_nodes parameter.

    Examples
    --------
    >>> G = generate_hierarchical_topology(50, branching_factor=3, depth=3)
    >>> # Creates tree: 1 root + 3 level-1 + 9 level-2 = 13 nodes (adjusted)
    """
    # Calculate optimal depth to approximate num_nodes
    total_nodes = 0
    for d in range(depth):
        total_nodes += branching_factor**d

    # Generate balanced tree
    G = nx.balanced_tree(branching_factor, depth - 1, create_using=nx.Graph())

    # If we have fewer nodes than requested, add more at the bottom level
    current_nodes = G.number_of_nodes()
    if current_nodes < num_nodes:
        leaf_nodes = [n for n in G.nodes() if G.degree(n) == 1]
        nodes_to_add = min(num_nodes - current_nodes, len(leaf_nodes) * branching_factor)

        next_node_id = current_nodes
        for _ in range(nodes_to_add):
            parent = np.random.choice(leaf_nodes)
            G.add_edge(parent, next_node_id)
            next_node_id += 1

    # Assign levels based on distance from root (node 0)
    levels = nx.single_source_shortest_path_length(G, 0)
    nx.set_node_attributes(G, levels, "level")

    # Add cross-level edges for realism (e.g., workstations accessing DMZ services)
    num_cross_edges = max(1, int(G.number_of_nodes() * 0.1))
    nodes_list = list(G.nodes())
    for _ in range(num_cross_edges):
        node1, node2 = np.random.choice(nodes_list, size=2, replace=False)
        # Only add if nodes are at different levels and not already connected
        if levels[node1] != levels[node2] and not G.has_edge(node1, node2):
            G.add_edge(node1, node2)

    return G


def calculate_topology_metrics(G: nx.Graph) -> Dict[str, float]:
    """
    Calculate network topology metrics for analysis.

    Parameters
    ----------
    G : nx.Graph
        Network graph

    Returns
    -------
    Dict[str, float]
        Dictionary of topology metrics:
        - clustering_coefficient: Average clustering coefficient
        - average_path_length: Average shortest path length
        - diameter: Network diameter (longest shortest path)
        - density: Network density (actual edges / possible edges)
        - degree_centrality_max: Maximum degree centrality
        - degree_centrality_mean: Mean degree centrality
        - assortativity: Degree assortativity coefficient

    Notes
    -----
    These metrics characterize network structure and are useful for:
    - Validating topology generators produce expected structures
    - Analyzing how network structure affects attack/defense dynamics
    - Ensuring reproducibility of network topologies

    Examples
    --------
    >>> G = generate_hub_spoke_topology(50)
    >>> metrics = calculate_topology_metrics(G)
    >>> print(f"Clustering: {metrics['clustering_coefficient']:.3f}")
    """
    metrics = {}

    # Clustering coefficient (high in hub-spoke, low in hierarchical)
    metrics["clustering_coefficient"] = nx.average_clustering(G)

    # Path lengths (only for connected graphs)
    if nx.is_connected(G):
        metrics["average_path_length"] = nx.average_shortest_path_length(G)
        metrics["diameter"] = nx.diameter(G)
    else:
        # For disconnected graphs, use largest component
        largest_cc = max(nx.connected_components(G), key=len)
        subgraph = G.subgraph(largest_cc)
        metrics["average_path_length"] = nx.average_shortest_path_length(subgraph)
        metrics["diameter"] = nx.diameter(subgraph)

    # Density (edges / possible edges)
    metrics["density"] = nx.density(G)

    # Degree centrality
    degree_centrality = nx.degree_centrality(G)
    metrics["degree_centrality_max"] = max(degree_centrality.values())
    metrics["degree_centrality_mean"] = np.mean(list(degree_centrality.values()))

    # Assortativity (do high-degree nodes connect to other high-degree nodes?)
    try:
        metrics["assortativity"] = nx.degree_assortativity_coefficient(G)
    except Exception:
        metrics["assortativity"] = 0.0  # Can fail for certain graph types

    return metrics


def assign_vulnerability_by_topology(
    G: nx.Graph, distribution: str = "gradient"
) -> Dict[int, float]:
    """
    Assign node vulnerabilities based on topology structure.

    Parameters
    ----------
    G : nx.Graph
        Network graph (must have topology attributes from generators)
    distribution : str, default='gradient'
        Vulnerability assignment strategy:
        - 'gradient': Hub-spoke: hubs more secure; Hierarchical: outer layers more vulnerable
        - 'uniform': All nodes equal vulnerability (baseline)
        - 'inverse': Hubs/core more vulnerable (insider threat model)

    Returns
    -------
    Dict[int, float]
        Mapping of node ID to vulnerability level (0.0-1.0)

    Notes
    -----
    Realistic vulnerability distributions:
    - Hub-spoke: Hubs are servers (hardened), periphery is endpoints (vulnerable)
    - Hierarchical: DMZ is exposed (vulnerable), internal is protected (secure)
    - This creates attack surface similar to real enterprise networks

    Examples
    --------
    >>> G = generate_hub_spoke_topology(50)
    >>> vulns = assign_vulnerability_by_topology(G, distribution='gradient')
    """
    vulnerabilities = {}

    # Check if this is a hub-spoke topology
    if "is_hub" in G.nodes[0]:
        # Hub-spoke topology
        for node in G.nodes():
            if distribution == "gradient":
                # Hubs are more secure (lower vulnerability)
                vulnerabilities[node] = 0.2 if G.nodes[node]["is_hub"] else 0.7
            elif distribution == "inverse":
                # Hubs are more vulnerable (insider threat)
                vulnerabilities[node] = 0.8 if G.nodes[node]["is_hub"] else 0.3
            else:  # uniform
                vulnerabilities[node] = 0.5

    # Check if this is a hierarchical topology
    elif "level" in G.nodes[0]:
        # Hierarchical topology
        max_level = max(G.nodes[node]["level"] for node in G.nodes())
        for node in G.nodes():
            level = G.nodes[node]["level"]
            if distribution == "gradient":
                # Outer layers (higher level) are more vulnerable
                vulnerabilities[node] = 0.3 + (level / max_level) * 0.6
            elif distribution == "inverse":
                # Core (lower level) is more vulnerable
                vulnerabilities[node] = 0.8 - (level / max_level) * 0.6
            else:  # uniform
                vulnerabilities[node] = 0.5

    else:
        # Unknown topology type, use uniform
        for node in G.nodes():
            vulnerabilities[node] = 0.5

    return vulnerabilities
