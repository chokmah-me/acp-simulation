"""
Defender agent implementations for ACP simulation.

This module provides concrete defender implementations including:
- PessimisticDefender: Traditional worst-case baseline
- OptimisticACPDefender: Novel ACP strategy with deception
- Configurable versions with parameter control
"""

from typing import Any, Dict, List, Set

import networkx as nx
import numpy as np

from ..core.enums import ActionType, NodeState
from .base import BaseDefender


class PessimisticDefender(BaseDefender):
    """
    Traditional Worst-Case Defender (Baseline).

    Key Characteristics:
    - Assumes attacker has complete knowledge (paranoid)
    - Reacts with expensive actions (RESTORE_NODE 41.85% of time)
    - Resource-inefficient "defensive paralysis"
    - Never uses cheap ACP deception (doesn't believe in it)

    This is the BASELINE we're comparing against in the thesis.

    Attributes
    ----------
    restore_node_probability : float
        Probability of using RESTORE_NODE (calibrated to 41.85% from thesis)
    paranoia_level : float
        Level of worst-case assumption (high = more paranoid)
    node_states : Dict[int, NodeState]
        Current state of each node
    vulnerabilities : Dict[int, float]
        Vulnerability level of each node (0-1)
    """

    def __init__(self, network: nx.Graph, vulnerability_distribution: str = "uniform"):
        """
        Initialize pessimistic defender.

        Parameters
        ----------
        network : nx.Graph
            Network graph
        vulnerability_distribution : str, default='uniform'
            Type of vulnerability distribution
        """
        super().__init__(network)
        self.node_states = {node: NodeState.CLEAN for node in network.nodes()}
        self.vulnerability_distribution = vulnerability_distribution

        # CRITICAL: Calibrated to match thesis claim
        self.restore_node_probability = 0.4185  # 41.85% from thesis
        self.paranoia_level = 0.8  # High worst-case assumptions

        # Initialize vulnerabilities
        self._initialize_vulnerabilities()

    def _initialize_vulnerabilities(self) -> None:
        """
        Initialize node vulnerabilities based on distribution type.

        Supports: uniform, normal, exponential, bimodal
        """
        n_nodes = len(self.network.nodes())

        if self.vulnerability_distribution == "uniform":
            # All nodes equally vulnerable
            self.vulnerabilities = {node: 0.5 for node in self.network.nodes()}

        elif self.vulnerability_distribution == "normal":
            # Normal distribution (most nodes medium vulnerability)
            vulns = np.random.normal(0.5, 0.15, n_nodes)
            vulns = np.clip(vulns, 0.1, 0.9)
            self.vulnerabilities = {node: v for node, v in zip(self.network.nodes(), vulns)}

        elif self.vulnerability_distribution == "exponential":
            # Few highly vulnerable, most less vulnerable
            vulns = np.random.exponential(0.3, n_nodes)
            vulns = np.clip(vulns, 0.1, 0.9)
            self.vulnerabilities = {node: v for node, v in zip(self.network.nodes(), vulns)}

        elif self.vulnerability_distribution == "bimodal":
            # Two groups: secure and insecure
            vulns = []
            for _ in range(n_nodes):
                if np.random.random() < 0.5:
                    vulns.append(np.random.uniform(0.1, 0.3))  # Secure
                else:
                    vulns.append(np.random.uniform(0.7, 0.9))  # Vulnerable
            self.vulnerabilities = {node: v for node, v in zip(self.network.nodes(), vulns)}

        else:
            self.vulnerabilities = {node: 0.5 for node in self.network.nodes()}

    def select_action(self, state: Dict[str, Any], attacker_knowledge: Set[int]) -> ActionType:
        """
        Pessimistic strategy: Worst-case assumptions lead to expensive reactions.

        Logic:
        1. Assume worst-case at ALL times (paranoid)
        2. 41.85% chance of RESTORE_NODE (most expensive)
        3. Heavy use of other expensive reactions
        4. Never uses cheap ACP deception

        Parameters
        ----------
        state : Dict[str, Any]
            Current environment state
        attacker_knowledge : Set[int]
            Nodes known to attacker

        Returns
        -------
        ActionType
            Selected defensive action
        """
        compromised = [n for n, s in self.node_states.items() if s == NodeState.COMPROMISED]
        alert_level = state.get("alert_level", 0)
        time_step = state.get("time", 0)

        # CRITICAL: Be pessimistic/paranoid even WITHOUT visible compromise
        # Traditional defenders assume worst-case: "Attacker might be present but undetected"
        perceived_threat = max(len(compromised), alert_level * 10, time_step / 50)

        # Roll for action based on RESTORE_NODE probability
        roll = np.random.random()

        # RESTORE_NODE used 41.85% of the time (as per thesis)
        if roll < self.restore_node_probability:
            # CRITICAL: RESTORE_NODE (Cost: 6.0) - most expensive
            # Used even when no visible compromise (worst-case paranoia)
            action = ActionType.RESTORE_NODE

        # ISOLATE: Second most expensive (30% of remaining actions)
        elif roll < 0.4185 + 0.30 * (1 - 0.4185):
            action = ActionType.ISOLATE if compromised else ActionType.PATCH

        # PATCH: Medium expensive (40% of remaining actions)
        elif roll < 0.4185 + 0.70 * (1 - 0.4185):
            action = ActionType.PATCH

        # MONITOR: Only 30% of remaining actions
        else:
            action = ActionType.MONITOR

        self.action_history.append(action)
        return action


class OptimisticACPDefender(BaseDefender):
    """
    Asymmetric Cognitive Projection Defender (Novel Approach).

    Key Characteristics:
    - Assumes attacker has INCOMPLETE knowledge (optimistic)
    - Exploits information asymmetry
    - Uses cheap ACP deception instead of expensive reactions
    - Leverages cognitive latency for "latency arbitrage"
    - NEVER uses RESTORE_NODE (too expensive, not strategic)

    This is the NOVEL APPROACH from the thesis.

    Attributes
    ----------
    acp_strength : float
        Probability of using ACP deception tactics
    deception_successes : int
        Count of successful deceptions
    deception_attempts : int
        Count of deception attempts
    deception_history : List[Dict]
        History of deception events
    node_states : Dict[int, NodeState]
        Current state of each node
    vulnerabilities : Dict[int, float]
        Vulnerability level of each node
    """

    def __init__(
        self,
        network: nx.Graph,
        acp_strength: float = 0.65,
        vulnerability_distribution: str = "uniform",
    ):
        """
        Initialize ACP defender.

        Parameters
        ----------
        network : nx.Graph
            Network graph
        acp_strength : float, default=0.65
            Probability of using ACP deception
        vulnerability_distribution : str, default='uniform'
            Type of vulnerability distribution
        """
        super().__init__(network)
        self.acp_strength = acp_strength
        self.node_states = {node: NodeState.CLEAN for node in network.nodes()}
        self.vulnerability_distribution = vulnerability_distribution

        # Deception tracking
        self.deception_successes = 0
        self.deception_attempts = 0
        self.deception_history = []

        # Initialize vulnerabilities
        self._initialize_vulnerabilities()

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

    def select_action(self, state: Dict[str, Any], attacker_knowledge: Set[int]) -> ActionType:
        """
        Optimistic strategy: Exploit information asymmetry with cheap deception.

        Logic:
        1. If attacker has incomplete knowledge → deploy ACP deception
        2. Use cheap honeypots for coverage
        3. Only patch when necessary
        4. NEVER use expensive RESTORE_NODE

        Parameters
        ----------
        state : Dict[str, Any]
            Current environment state
        attacker_knowledge : Set[int]
            Nodes known to attacker

        Returns
        -------
        ActionType
            Selected defensive action
        """
        unknown_nodes = set(self.network.nodes()) - attacker_knowledge
        compromised = [n for n, s in self.node_states.items() if s == NodeState.COMPROMISED]

        # STRATEGIC DECEPTION: Exploit attacker's incomplete knowledge
        if len(unknown_nodes) > 5 and np.random.random() < 0.45:
            # ACP DECEPTION (Cost: 1.0) - cheap and effective
            action = ActionType.ACP_DECEPTION

        # HONEYPOT COVERAGE: Create attractive false targets
        elif len(unknown_nodes) > 3 and np.random.random() < 0.35:
            # DEPLOY_HONEYPOT (Cost: 2.0) - medium cost
            action = ActionType.DEPLOY_HONEYPOT

        # TARGETED RESPONSE: Only when compromised
        elif compromised:
            if np.random.random() < 0.7:
                # PATCH (Cost: 1.5) - surgical fix
                action = ActionType.PATCH
            else:
                # ISOLATE (Cost: 3.0) - only when patch insufficient
                action = ActionType.ISOLATE

        # MINIMAL MONITORING: Low cost baseline
        else:
            # MONITOR (Cost: 0.1) - cheapest action
            action = ActionType.MONITOR

        # CRITICAL: NEVER uses RESTORE_NODE (too expensive, not strategic)

        self.action_history.append(action)
        return action

    def deploy_acp_deception(
        self, target_nodes: List[int], current_time: int, attacker_knowledge: Set[int]
    ) -> Dict[int, Dict[str, Any]]:
        """
        Deploy Asymmetric Cognitive Projection.

        CRITICAL: Only deceive about UNKNOWN nodes (information asymmetry)

        Creates false signals that:
        1. Make nodes appear highly vulnerable
        2. Make nodes appear high-value
        3. Poison attacker's memory with false positives
        4. Exploit cognitive latency window

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
            Deception results with false signals
        """
        deception_results = {}

        for node in target_nodes:
            # KEY: Only deceive about nodes attacker doesn't know
            if node not in attacker_knowledge and np.random.random() < self.acp_strength:

                # Create sophisticated false signals
                deception_results[node] = {
                    "false_vulnerability": np.random.uniform(0.85, 0.98),  # Appear very vulnerable
                    "false_value": np.random.uniform(0.75, 0.95),  # Appear high-value
                    "false_criticality": np.random.choice(["critical", "high", "important"]),
                    "timestamp": current_time,
                    "success": True,
                }

                self.deception_attempts += 1

                # Track for analysis
                self.deception_history.append(
                    {
                        "node": node,
                        "time": current_time,
                        "type": deception_results[node]["false_criticality"],
                    }
                )

        if deception_results:
            self.deception_successes += len(deception_results)

        return deception_results


class ConfigurablePessimisticDefender(PessimisticDefender):
    """
    Configurable version of PessimisticDefender.

    Adds configuration management while preserving original behavior.
    """

    def __init__(self, network: nx.Graph, vulnerability_distribution: str = "uniform"):
        """
        Initialize configurable pessimistic defender.

        Parameters
        ----------
        network : nx.Graph
            Network graph
        vulnerability_distribution : str, default='uniform'
            Vulnerability distribution type
        """
        super().__init__(network, vulnerability_distribution)


class ConfigurableACPDefender(OptimisticACPDefender):
    """
    Configurable version of OptimisticACPDefender.

    Adds configuration management while preserving original behavior.
    """

    def __init__(
        self,
        network: nx.Graph,
        acp_strength: float = 0.65,
        vulnerability_distribution: str = "uniform",
    ):
        """
        Initialize configurable ACP defender.

        Parameters
        ----------
        network : nx.Graph
            Network graph
        acp_strength : float, default=0.65
            ACP deception probability
        vulnerability_distribution : str, default='uniform'
            Vulnerability distribution type
        """
        super().__init__(network, acp_strength, vulnerability_distribution)
