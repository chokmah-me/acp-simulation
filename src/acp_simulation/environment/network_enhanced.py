"""
Enhanced network environment with realistic enterprise topologies.

This module extends the base network environment to support:
- Hub-and-spoke topologies (corporate server-client architectures)
- Hierarchical topologies (security zones: DMZ, internal, endpoints)
- Topology-aware vulnerability distributions
- Network structure metrics calculation
"""

from typing import Dict, List, Set, Tuple, Any, Optional
import numpy as np
import networkx as nx

from ..core.enums import ActionType, NodeState
from ..agents.base import BaseAttacker, BaseDefender
from .topology_generators import (
    generate_hub_spoke_topology,
    generate_hierarchical_topology,
    calculate_topology_metrics,
    assign_vulnerability_by_topology,
)


class EnhancedNetworkEnvironment:
    """
    Enhanced cyber network environment with enterprise-realistic topologies.

    Supports multiple topology types for  conference validation:
    - Hub-and-spoke (star): Corporate networks with server-client architecture
    - Hierarchical (tree): Security zones with DMZ, internal, endpoints
    - Erdős-Rényi: Random baseline
    - Barabási-Albert: Scale-free networks

    Attributes
    ----------
    num_nodes : int
        Number of nodes in the network
    connectivity : float
        Network connectivity parameter
    topology_type : str
        Network topology type
    vulnerability_distribution : str
        Vulnerability distribution strategy
    network : nx.Graph
        The network graph
    node_states : Dict[int, NodeState]
        Current state of each node
    vulnerabilities : Dict[int, float]
        Vulnerability level of each node (0-1)
    topology_metrics : Dict[str, float]
        Calculated topology metrics
    """

    def __init__(
        self,
        num_nodes: int = 50,
        connectivity: float = 0.6,
        topology_type: str = "auto",
        vulnerability_distribution: str = "auto",
        latency_window: Tuple[float, float] = (0.3, 0.8),
        random_seed: Optional[int] = None,
    ):
        """
        Initialize enhanced network environment.

        Parameters
        ----------
        num_nodes : int, default=50
            Number of nodes
        connectivity : float, default=0.6
            Network connectivity
        topology_type : str, default='auto'
            Topology: 'auto', 'erdos_renyi', 'barabasi_albert', 'hub_spoke', 'hierarchical'
        vulnerability_distribution : str, default='auto'
            Vulnerability: 'auto', 'uniform', 'gradient', 'inverse'
        latency_window : Tuple[float, float], default=(0.3, 0.8)
            Min and max cognitive latency for attacker processing
        random_seed : Optional[int], default=None
            Random seed for reproducibility
        """
        self.num_nodes = num_nodes
        self.connectivity = connectivity
        self.topology_type = topology_type
        self.vulnerability_distribution = vulnerability_distribution
        self.latency_window = latency_window
        self.random_seed = random_seed

        # Set random seed if provided
        if random_seed is not None:
            np.random.seed(random_seed)

        # Generate network topology
        self.network = self._generate_topology()

        # Calculate topology metrics for analysis
        self.topology_metrics = calculate_topology_metrics(self.network)

        # Initialize node states
        self.node_states = {node: NodeState.CLEAN for node in self.network.nodes()}
        self.current_time = 0

        # Initialize vulnerabilities
        self._initialize_vulnerabilities()

        # Action costs from thesis validation
        self.action_costs = {
            ActionType.SCAN: 0.5,
            ActionType.EXPLOIT: 2.0,
            ActionType.PROPAGATE: 1.0,
            ActionType.MONITOR: 0.1,
            ActionType.PATCH: 1.5,
            ActionType.ISOLATE: 3.0,
            ActionType.DEPLOY_HONEYPOT: 2.0,
            ActionType.RESTORE_NODE: 6.0,  # Most expensive -  abstract shows pessimistic overuse
            ActionType.ACP_DECEPTION: 1.0,
        }

        # Metrics tracking
        self.metrics = {
            "cognitive_latency_exploitations": 0,
            "acp_deceptions": [],
            "expensive_actions": [],
            "restore_node_count": 0,  # Track for  validation
            "topology_type": self.topology_type,
            "topology_metrics": self.topology_metrics,
        }

    def _generate_topology(self) -> nx.Graph:
        """
        Generate network topology based on topology_type parameter.

        Returns
        -------
        nx.Graph
            Generated network graph
        """
        if self.topology_type == "auto":
            # Auto-select based on size (legacy behavior)
            if self.num_nodes <= 100:
                topology = "erdos_renyi"
            else:
                topology = "barabasi_albert"
        else:
            topology = self.topology_type

        # Generate based on selected topology
        if topology == "hub_spoke":
            G = generate_hub_spoke_topology(
                self.num_nodes, hub_ratio=0.1, connectivity=self.connectivity
            )

        elif topology == "hierarchical":
            G = generate_hierarchical_topology(self.num_nodes, branching_factor=3, depth=3)

        elif topology == "barabasi_albert":
            m = max(1, int(self.num_nodes * self.connectivity / 10))
            G = nx.barabasi_albert_graph(self.num_nodes, m, seed=self.random_seed)

        else:  # Default: erdos_renyi
            G = nx.erdos_renyi_graph(self.num_nodes, self.connectivity, seed=self.random_seed)

        # Ensure connectivity
        if not nx.is_connected(G):
            components = list(nx.connected_components(G))
            for i in range(len(components) - 1):
                node1 = list(components[i])[0]
                node2 = list(components[i + 1])[0]
                G.add_edge(node1, node2)

        return G

    def _initialize_vulnerabilities(self) -> None:
        """
        Initialize node vulnerabilities based on topology and distribution.
        """
        if self.vulnerability_distribution == "auto":
            # Auto-select based on topology
            if self.topology_type in ["hub_spoke", "hierarchical"]:
                dist = "gradient"
            else:
                dist = "uniform"
        else:
            dist = self.vulnerability_distribution

        # Use topology-aware distribution if applicable
        if dist in ["gradient", "inverse"] and self.topology_type in ["hub_spoke", "hierarchical"]:
            self.vulnerabilities = assign_vulnerability_by_topology(self.network, dist)
        else:
            # Use uniform or legacy distributions
            n_nodes = len(self.network.nodes())

            if dist == "uniform":
                self.vulnerabilities = {node: 0.5 for node in self.network.nodes()}

            elif dist == "normal":
                vulns = np.random.normal(0.5, 0.15, n_nodes)
                vulns = np.clip(vulns, 0.1, 0.9)
                self.vulnerabilities = {node: v for node, v in zip(self.network.nodes(), vulns)}

            elif dist == "exponential":
                vulns = np.random.exponential(0.3, n_nodes)
                vulns = np.clip(vulns, 0.1, 0.9)
                self.vulnerabilities = {node: v for node, v in zip(self.network.nodes(), vulns)}

            elif dist == "bimodal":
                vulns = []
                for _ in range(n_nodes):
                    if np.random.random() < 0.5:
                        vulns.append(np.random.uniform(0.1, 0.3))
                    else:
                        vulns.append(np.random.uniform(0.7, 0.9))
                self.vulnerabilities = {node: v for node, v in zip(self.network.nodes(), vulns)}

            else:  # default uniform
                self.vulnerabilities = {node: 0.5 for node in self.network.nodes()}

    def reset(self) -> Dict[str, Any]:
        """
        Reset environment for new episode.

        Returns
        -------
        Dict[str, Any]
            Initial state
        """
        self.node_states = {node: NodeState.CLEAN for node in self.network.nodes()}
        self.current_time = 0

        # Regenerate vulnerabilities with same distribution
        self._initialize_vulnerabilities()

        # Reset metrics
        self.metrics = {
            "cognitive_latency_exploitations": 0,
            "acp_deceptions": [],
            "expensive_actions": [],
            "restore_node_count": 0,
            "topology_type": self.topology_type,
            "topology_metrics": self.topology_metrics,
        }

        return self._get_state()

    def _get_state(self) -> Dict[str, Any]:
        """
        Get current environment state.

        Returns
        -------
        Dict[str, Any]
            State dictionary with network information
        """
        return {
            "node_states": self.node_states.copy(),
            "vulnerabilities": self.vulnerabilities.copy(),
            "time": self.current_time,
            "network": self.network,
            "topology_metrics": self.topology_metrics,
        }

    def get_topology_report(self) -> Dict[str, Any]:
        """
        Get comprehensive topology analysis report.

        Returns
        -------
        Dict[str, Any]
            Report with topology metrics and characteristics
        """
        report = {
            "topology_type": self.topology_type,
            "num_nodes": self.network.number_of_nodes(),
            "num_edges": self.network.number_of_edges(),
            "metrics": self.topology_metrics,
            "vulnerability_stats": {
                "mean": np.mean(list(self.vulnerabilities.values())),
                "std": np.std(list(self.vulnerabilities.values())),
                "min": min(self.vulnerabilities.values()),
                "max": max(self.vulnerabilities.values()),
            },
        }

        # Add topology-specific information
        if "is_hub" in self.network.nodes[0]:
            num_hubs = sum(1 for n in self.network.nodes() if self.network.nodes[n]["is_hub"])
            report["hub_count"] = num_hubs
            report["peripheral_count"] = self.network.number_of_nodes() - num_hubs

        if "level" in self.network.nodes[0]:
            levels = [self.network.nodes[n]["level"] for n in self.network.nodes()]
            report["max_depth"] = max(levels)
            report["nodes_per_level"] = {level: levels.count(level) for level in set(levels)}

        return report
