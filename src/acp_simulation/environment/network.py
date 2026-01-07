"""
Network environment for ACP simulation.

This module provides the simulation environment including:
- Network generation and management
- State tracking
- Cognitive latency window implementation
- Reward calculations
- Action execution
"""

from typing import Dict, List, Set, Tuple, Any, Optional
import numpy as np
import networkx as nx

from ..core.enums import ActionType, NodeState
from ..agents.base import BaseAttacker, BaseDefender


class NetworkEnvironment:
    """
    Cyber Network Simulation Environment with cognitive latency.

    Implements the core simulation mechanics including:
    - Dynamic network generation (Erdős-Rényi)
    - Node state management (CLEAN, COMPROMISED, etc.)
    - Cognitive latency window for ACP exploitation
    - Multi-phase execution timeline
    - Comprehensive metrics tracking

    Attributes
    ----------
    num_nodes : int
        Number of nodes in the network
    connectivity : float
        Network connectivity probability
    network : nx.Graph
        The network graph
    node_states : Dict[int, NodeState]
        Current state of each node
    vulnerabilities : Dict[int, float]
        Vulnerability level of each node (0-1)
    current_time : int
        Current simulation time step
    action_costs : Dict[ActionType, float]
        Cost for each action type
    metrics : Dict[str, Any]
        Tracking metrics for analysis
    """

    def __init__(
        self,
        num_nodes: int = 50,
        connectivity: float = 0.6,
        latency_window: Tuple[float, float] = (0.3, 0.8),
    ):
        """
        Initialize network environment.

        Parameters
        ----------
        num_nodes : int, default=50
            Number of nodes in the network
        connectivity : float, default=0.6
            Network connectivity (0.0 to 1.0)
        latency_window : Tuple[float, float], default=(0.3, 0.8)
            Min and max cognitive latency for attacker processing (time units)
        """
        self.num_nodes = num_nodes
        self.connectivity = connectivity
        self.latency_window = latency_window

        # Generate network
        self.network = self._generate_network()

        # Initialize node states
        self.node_states = {i: NodeState.CLEAN for i in range(num_nodes)}
        self.vulnerabilities = {i: np.random.beta(2, 5) for i in range(num_nodes)}

        self.current_time = 0

        # Action costs from thesis (Table 1)
        self.action_costs = {
            ActionType.SCAN: 0.5,
            ActionType.EXPLOIT: 2.0,
            ActionType.PROPAGATE: 1.0,
            ActionType.MONITOR: 0.1,
            ActionType.PATCH: 1.5,
            ActionType.ISOLATE: 3.0,
            ActionType.DEPLOY_HONEYPOT: 2.0,
            ActionType.ACP_DECEPTION: 1.0,
            ActionType.RESTORE_NODE: 6.0,  # CRITICAL: Most expensive
        }

        # Also store by name for easier access
        self.action_costs_by_name = {
            action.name: cost for action, cost in self.action_costs.items()
        }

        # Metrics tracking
        self.metrics = {
            "cognitive_latency_exploitations": 0,
            "acp_deceptions": [],
            "expensive_actions": [],
        }

    def _generate_network(self) -> nx.Graph:
        """
        Generate connected network with target connectivity.

        Uses Erdős-Rényi model and ensures connectivity.

        Returns
        -------
        nx.Graph
            Generated network graph
        """
        while True:
            G = nx.erdos_renyi_graph(self.num_nodes, self.connectivity)
            if nx.is_connected(G):
                return G

    def reset(self) -> Dict[str, Any]:
        """
        Reset environment for new episode.

        Returns
        -------
        Dict[str, Any]
            Initial state
        """
        self.node_states = {i: NodeState.CLEAN for i in range(self.num_nodes)}
        self.vulnerabilities = {i: np.random.beta(2, 5) for i in range(self.num_nodes)}
        self.current_time = 0

        # Reset metrics
        self.metrics = {
            "cognitive_latency_exploitations": 0,
            "acp_deceptions": [],
            "expensive_actions": [],
        }

        return self._get_state()

    def step(
        self,
        attacker_action: ActionType,
        defender_action: ActionType,
        attacker: BaseAttacker,
        defender: BaseDefender,
    ) -> Tuple[Dict[str, Any], float, float, bool]:
        """
        Execute one time step with COGNITIVE LATENCY WINDOW.

        Timeline:
        t0: Attacker observes state
        t1: Cognitive processing delay (0.3-0.8 time units)
        t2: Defender acts DURING delay (latency arbitrage!)
        t3: Attacker makes decision on (possibly poisoned) observation
        t4: Actions execute

        This is the KEY INNOVATION enabling ACP.

        Parameters
        ----------
        attacker_action : ActionType
            Attacker's selected action
        defender_action : ActionType
            Defender's selected action
        attacker : BaseAttacker
            Attacker agent
        defender : BaseDefender
            Defender agent

        Returns
        -------
        Tuple[Dict[str, Any], float, float, bool]
            (next_state, attacker_reward, defender_reward, done)
        """
        self.current_time += 1

        # ===== PHASE 1: Attacker observes state =====
        observation = self._get_state()

        # ===== PHASE 2: COGNITIVE LATENCY WINDOW (KEY!) =====
        cognitive_latency = np.random.uniform(*self.latency_window)

        # ===== PHASE 3: Defender acts DURING latency =====
        # This is "latency arbitrage" - analogous to HFT front-running
        defender_outcome = {"success": False}
        deception_results = {}

        if defender_action == ActionType.ACP_DECEPTION:
            # CRITICAL: Deploy deception BEFORE attacker finishes processing
            unknown_nodes = list(set(self.network.nodes()) - attacker.known_nodes)
            if unknown_nodes:
                # Target only unknown nodes (information asymmetry)
                targets = unknown_nodes[: min(5, len(unknown_nodes))]
                deception_results = defender.deploy_acp_deception(
                    targets, self.current_time, attacker.known_nodes
                )
                defender_outcome = {
                    "success": len(deception_results) > 0,
                    "deception_results": deception_results,
                }

                if deception_results:
                    self.metrics["cognitive_latency_exploitations"] += 1
                    self.metrics["acp_deceptions"].append(self.current_time)
        else:
            # Execute other defender actions
            defender_outcome = self._execute_defender_action(defender_action)

        # ===== PHASE 4: Attacker decides on (possibly poisoned) data =====
        attacker_outcome = self._execute_attacker_action(attacker_action, attacker)

        # ===== PHASE 5: Attacker learns from experience =====
        situation = attacker._encode_situation(observation)

        # CRITICAL: If ACP deception was deployed, reduce learning confidence
        # This poisons the attacker's memory
        if deception_results:
            learning_confidence = np.random.uniform(0.3, 0.5)  # Low confidence
        else:
            learning_confidence = 1.0  # Normal confidence

        attacker.learn(
            situation,
            attacker_action,
            attacker_outcome.get("reward", 0),
            self.current_time,
            confidence=learning_confidence,  # Memory poisoning happens here
        )

        # ===== PHASE 6: Calculate rewards =====
        attacker_reward = self._calculate_attacker_reward(attacker_action, attacker_outcome)
        defender_reward = self._calculate_defender_reward(defender_action, defender_outcome)

        # Track expensive actions
        if defender_action == ActionType.RESTORE_NODE:
            self.metrics["expensive_actions"].append(self.current_time)

        # Check termination
        done = self._check_termination()

        return self._get_state(), attacker_reward, defender_reward, done

    def _execute_attacker_action(
        self, action: ActionType, attacker: BaseAttacker
    ) -> Dict[str, Any]:
        """
        Execute attacker action and return outcome.

        Parameters
        ----------
        action : ActionType
            Attacker's action
        attacker : BaseAttacker
            Attacker agent

        Returns
        -------
        Dict[str, Any]
            Action outcome with success status and reward
        """
        outcome = {"success": False, "reward": 0, "new_nodes": set()}

        if action == ActionType.SCAN:
            # Discover new nodes through scanning
            if attacker.known_nodes:
                # Scan from known node
                current_node = np.random.choice(list(attacker.known_nodes))
                neighbors = set(self.network.neighbors(current_node))
                new_nodes = neighbors - attacker.known_nodes

                if new_nodes:
                    discovered = np.random.choice(list(new_nodes))
                    attacker.known_nodes.add(discovered)
                    outcome = {"success": True, "reward": 2.0, "new_nodes": {discovered}}
            else:
                # Initial scan - discover entry point
                start_node = np.random.choice(list(self.network.nodes()))
                attacker.known_nodes.add(start_node)
                outcome = {"success": True, "reward": 2.0, "new_nodes": {start_node}}

        elif action == ActionType.EXPLOIT:
            # Attempt to compromise a known node
            exploitable = [
                n for n in attacker.known_nodes if self.node_states[n] == NodeState.CLEAN
            ]

            if exploitable:
                target = np.random.choice(exploitable)

                # Success depends on vulnerability
                if np.random.random() < self.vulnerabilities[target]:
                    self.node_states[target] = NodeState.COMPROMISED
                    attacker.compromised_nodes.add(target)
                    outcome = {"success": True, "reward": 10.0}
                else:
                    outcome = {"success": False, "reward": -1.0}

        elif action == ActionType.PROPAGATE:
            # Lateral movement from compromised nodes
            if attacker.compromised_nodes:
                source = np.random.choice(list(attacker.compromised_nodes))
                neighbors = set(self.network.neighbors(source))
                targets = [
                    n
                    for n in neighbors
                    if n not in attacker.compromised_nodes
                    and self.node_states[n] == NodeState.CLEAN
                ]

                if targets:
                    target = np.random.choice(targets)
                    if np.random.random() < 0.6:
                        self.node_states[target] = NodeState.COMPROMISED
                        attacker.compromised_nodes.add(target)
                        attacker.known_nodes.add(target)
                        outcome = {"success": True, "reward": 5.0, "new_nodes": {target}}

        return outcome

    def _execute_defender_action(self, action: ActionType) -> Dict[str, Any]:
        """
        Execute defender action and return outcome.

        Parameters
        ----------
        action : ActionType
            Defender's action

        Returns
        -------
        Dict[str, Any]
            Action outcome with success status
        """
        outcome = {"success": False}

        if action == ActionType.MONITOR:
            # Passive monitoring - always succeeds
            outcome = {"success": True}

        elif action == ActionType.PATCH:
            # Reduce vulnerabilities
            vulnerable_nodes = [
                n
                for n, v in self.vulnerabilities.items()
                if v > 0.5 and self.node_states[n] == NodeState.CLEAN
            ]
            if vulnerable_nodes:
                target = np.random.choice(vulnerable_nodes)
                self.vulnerabilities[target] *= 0.5  # Reduce vulnerability
                self.node_states[target] = NodeState.PATCHED
                outcome = {"success": True}

        elif action == ActionType.ISOLATE:
            # Remove compromised node from network
            compromised = [n for n, s in self.node_states.items() if s == NodeState.COMPROMISED]
            if compromised:
                target = np.random.choice(compromised)
                self.node_states[target] = NodeState.ISOLATED
                outcome = {"success": True}

        elif action == ActionType.DEPLOY_HONEYPOT:
            # Create honeypot
            clean_nodes = [n for n, s in self.node_states.items() if s == NodeState.CLEAN]
            if clean_nodes:
                target = np.random.choice(clean_nodes)
                self.node_states[target] = NodeState.HONEYPOT
                outcome = {"success": True}

        elif action == ActionType.RESTORE_NODE:
            # EXPENSIVE: Complete system restore
            compromised = [n for n, s in self.node_states.items() if s == NodeState.COMPROMISED]
            if compromised:
                # Restore multiple nodes (expensive but effective)
                restore_count = min(3, len(compromised))
                for i in range(restore_count):
                    node = compromised[i]
                    self.node_states[node] = NodeState.CLEAN
                    self.vulnerabilities[node] = np.random.beta(2, 5)
                outcome = {"success": True, "restored_count": restore_count}

        return outcome

    def _calculate_attacker_reward(self, action: ActionType, outcome: Dict[str, Any]) -> float:
        """
        Calculate attacker's reward for action.

        Parameters
        ----------
        action : ActionType
            Attacker's action
        outcome : Dict[str, Any]
            Action outcome

        Returns
        -------
        float
            Attacker's reward
        """
        # Start with action cost (negative)
        reward = -self.action_costs[action]

        # Add outcome-based reward
        if outcome["success"]:
            reward += outcome.get("reward", 0)

        return reward

    def _calculate_defender_reward(self, action: ActionType, outcome: Dict[str, Any]) -> float:
        """
        Calculate defender's reward for action.

        Includes:
        - Action costs (negative)
        - Survival bonus for clean nodes (positive)
        - Success-based rewards
        - Penalty for compromises

        Parameters
        ----------
        action : ActionType
            Defender's action
        outcome : Dict[str, Any]
            Action outcome

        Returns
        -------
        float
            Defender's reward
        """
        # Start with action cost (negative)
        reward = -self.action_costs[action]

        # NEW: Survival bonus (positive reward for clean nodes)
        clean_nodes = sum(1 for s in self.node_states.values() if s == NodeState.CLEAN)
        reward += clean_nodes * 0.4  # 0.4 points per clean node

        # Success-based rewards
        if outcome["success"]:
            if action == ActionType.PATCH:
                reward += 4.0  # Good defensive action
            elif action == ActionType.ISOLATE:
                reward += 10.0  # Stopped active threat
            elif action == ActionType.DEPLOY_HONEYPOT:
                reward += 5.0  # Proactive defense
            elif action == ActionType.ACP_DECEPTION:
                # HIGH REWARD: Successful cognitive deception
                deception_count = len(outcome.get("deception_results", {}))
                reward += 15.0 * deception_count  # Major strategic advantage
            elif action == ActionType.RESTORE_NODE:
                # Expensive but effective
                reward += 12.0
            elif action == ActionType.MONITOR:
                reward += 1.0  # Small reward for surveillance

        # Penalty for compromises
        compromised_count = sum(1 for s in self.node_states.values() if s == NodeState.COMPROMISED)
        reward -= compromised_count * 2.0  # -2 points per compromise

        return reward

    def _get_state(self) -> Dict[str, Any]:
        """
        Get current state observation.

        Returns
        -------
        Dict[str, Any]
            Current state with metrics
        """
        compromised_count = sum(1 for s in self.node_states.values() if s == NodeState.COMPROMISED)
        clean_count = sum(1 for s in self.node_states.values() if s == NodeState.CLEAN)

        return {
            "compromised_count": compromised_count,
            "clean_count": clean_count,
            "alert_level": compromised_count / self.num_nodes,
            "network_health": clean_count / self.num_nodes,
            "time": self.current_time,
        }

    def _check_termination(self) -> bool:
        """
        Check if episode should terminate.

        Terminates if:
        1. Network mostly compromised (70%+)
        2. Time limit reached (50 steps)

        Returns
        -------
        bool
            Whether episode should terminate
        """
        compromised = sum(1 for s in self.node_states.values() if s == NodeState.COMPROMISED)

        return (compromised > self.num_nodes * 0.7) or (self.current_time > 50)


class ConfigurableNetworkEnvironment(NetworkEnvironment):
    """
    Configurable network environment with parameter control.

    Extends base environment to support:
    - Configurable network size and connectivity
    - Multiple network models (Erdős-Rényi, Barabási-Albert)
    - Vulnerability distribution options

    Attributes
    ----------
    vulnerability_distribution : str
        Type of vulnerability distribution
    """

    def __init__(
        self,
        num_nodes: int = 50,
        connectivity: float = 0.6,
        vulnerability_distribution: str = "uniform",
        latency_window: Tuple[float, float] = (0.3, 0.8),
    ):
        """
        Initialize configurable network environment.

        Parameters
        ----------
        num_nodes : int, default=50
            Number of nodes
        connectivity : float, default=0.6
            Network connectivity
        vulnerability_distribution : str, default='uniform'
            Vulnerability distribution type
        latency_window : Tuple[float, float], default=(0.3, 0.8)
            Min and max cognitive latency for attacker processing (time units)
        """
        self.num_nodes = num_nodes
        self.connectivity = connectivity
        self.vulnerability_distribution = vulnerability_distribution
        self.latency_window = latency_window

        # Create network based on size
        if num_nodes <= 100:
            # Use Erdős-Rényi for small networks
            self.network = nx.erdos_renyi_graph(num_nodes, connectivity, seed=None)
        else:
            # Use Barabási-Albert for large networks (scale-free)
            m = max(1, int(num_nodes * connectivity / 10))
            self.network = nx.barabasi_albert_graph(num_nodes, m, seed=None)

        # Ensure connectivity
        if not nx.is_connected(self.network):
            # Add edges to make connected
            components = list(nx.connected_components(self.network))
            for i in range(len(components) - 1):
                node1 = list(components[i])[0]
                node2 = list(components[i + 1])[0]
                self.network.add_edge(node1, node2)

        # Initialize node states
        self.node_states = {node: NodeState.CLEAN for node in self.network.nodes()}
        self.current_time = 0

        # Initialize vulnerabilities based on distribution
        self._initialize_vulnerabilities()

        # Action costs (include all actions for both agents)
        self.action_costs = {
            # Attacker actions
            ActionType.SCAN: 0.5,
            ActionType.EXPLOIT: 2.0,
            ActionType.PROPAGATE: 1.0,
            # Defender actions
            ActionType.MONITOR: 0.1,
            ActionType.PATCH: 1.5,
            ActionType.ISOLATE: 3.0,
            ActionType.DEPLOY_HONEYPOT: 2.0,
            ActionType.RESTORE_NODE: 6.0,
            ActionType.ACP_DECEPTION: 1.0,
        }

        # Metrics tracking
        self.metrics = {
            "cognitive_latency_exploitations": 0,
            "acp_deceptions": [],
            "expensive_actions": [],
        }

    def _initialize_vulnerabilities(self) -> None:
        """
        Initialize node vulnerabilities based on distribution type.
        """
        n_nodes = len(self.network.nodes())

        if self.vulnerability_distribution == "uniform":
            self.vulnerabilities = {node: 0.5 for node in self.network.nodes()}

        elif self.vulnerability_distribution == "normal":
            vulns = np.random.normal(0.5, 0.15, n_nodes)
            vulns = np.clip(vulns, 0.1, 0.9)
            self.vulnerabilities = {node: v for node, v in zip(self.network.nodes(), vulns)}

        elif self.vulnerability_distribution == "exponential":
            vulns = np.random.exponential(0.3, n_nodes)
            vulns = np.clip(vulns, 0.1, 0.9)
            self.vulnerabilities = {node: v for node, v in zip(self.network.nodes(), vulns)}

        elif self.vulnerability_distribution == "bimodal":
            vulns = []
            for _ in range(n_nodes):
                if np.random.random() < 0.5:
                    vulns.append(np.random.uniform(0.1, 0.3))
                else:
                    vulns.append(np.random.uniform(0.7, 0.9))
            self.vulnerabilities = {node: v for node, v in zip(self.network.nodes(), vulns)}

        else:
            self.vulnerabilities = {node: 0.5 for node in self.network.nodes()}
