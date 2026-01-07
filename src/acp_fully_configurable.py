"""
FULLY CONFIGURABLE ACP SIMULATION - Advanced Parameter Control
Comprehensive parameter sweep capabilities for sensitivity analysis

All configurable parameters:
- ACP strength (deception probability)
- Network size (nodes)
- Network connectivity
- Confidence intervals
- Bootstrap samples
- Attacker learning rate
- Vulnerability distribution

Author: dyb
Date: December 09, 2025
"""

import argparse
import json
import pickle

# Import core classes
import sys
import time
from collections import defaultdict
from multiprocessing import Pool, cpu_count
from typing import Dict, List, Set, Tuple

import networkx as nx
import numpy as np
from scipy import stats

sys.path.insert(0, ".")
from acp_corrected_final import (  # noqa: E402
    ActionType,
    CognitiveAttacker,
    Instance,
    NetworkEnvironment,
    NodeState,
)

# ============================================================================
# CONFIGURABLE DEFENDER CLASSES
# ============================================================================


class ConfigurablePessimisticDefender:
    """
    Traditional pessimistic defender with configurable parameters
    """

    def __init__(self, network: nx.Graph, vulnerability_distribution: str = "uniform"):
        self.network = network
        self.node_states = {node: NodeState.CLEAN for node in network.nodes()}
        self.vulnerability_distribution = vulnerability_distribution
        self.action_history = []

        # Initialize vulnerability levels based on distribution
        self._initialize_vulnerabilities()

    def _initialize_vulnerabilities(self):
        """Initialize node vulnerabilities based on distribution type"""
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

    def select_action(self, state: Dict, attacker_known_nodes: Set[int]) -> ActionType:
        """Select defensive action - pessimistic strategy"""
        compromised = [n for n, s in self.node_states.items() if s == NodeState.COMPROMISED]

        if compromised:
            # High vulnerability nodes get RESTORE_NODE more often
            if compromised:
                avg_vuln = np.mean([self.vulnerabilities[n] for n in compromised])
                if np.random.random() < 0.4 + avg_vuln * 0.2:
                    action = ActionType.RESTORE_NODE
                else:
                    action = ActionType.ISOLATE if np.random.random() < 0.15 else ActionType.PATCH
            else:
                action = ActionType.PATCH
        else:
            action = ActionType.MONITOR if np.random.random() < 0.7 else ActionType.PATCH

        self.action_history.append(action)
        return action


class ConfigurableACPDefender:
    """
    ACP optimistic defender with configurable strength and parameters
    """

    def __init__(
        self,
        network: nx.Graph,
        acp_strength: float = 0.65,
        vulnerability_distribution: str = "uniform",
    ):
        self.network = network
        self.node_states = {node: NodeState.CLEAN for node in network.nodes()}
        self.acp_strength = acp_strength  # Probability of using ACP tactics
        self.vulnerability_distribution = vulnerability_distribution
        self.action_history = []
        self.acp_deployments = 0

        # Initialize vulnerabilities
        self._initialize_vulnerabilities()

    def _initialize_vulnerabilities(self):
        """Initialize node vulnerabilities based on distribution type"""
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

    def select_action(self, state: Dict, attacker_known_nodes: Set[int]) -> ActionType:
        """Select defensive action using ACP strategy"""

        # Information asymmetry: defender knows full network
        unknown_to_attacker = set(self.network.nodes()) - attacker_known_nodes
        compromised = [n for n, s in self.node_states.items() if s == NodeState.COMPROMISED]

        # ACP decision: use deception based on acp_strength
        if unknown_to_attacker and np.random.random() < self.acp_strength:
            # Deploy ACP deception or honeypot
            if np.random.random() < 0.7:
                action = ActionType.ACP_DECEPTION
                self.acp_deployments += 1
            else:
                action = ActionType.DEPLOY_HONEYPOT
        elif compromised:
            # Surgical response (never RESTORE_NODE)
            if np.random.random() < 0.1:
                action = ActionType.ISOLATE
            else:
                action = ActionType.PATCH
        else:
            action = ActionType.MONITOR

        self.action_history.append(action)
        return action


class ConfigurableAttacker(CognitiveAttacker):
    """
    Cognitive attacker with configurable learning rate
    """

    def __init__(self, decay_rate: float = 0.8, noise: float = 0.1, learning_rate: float = 1.0):
        super().__init__(decay_rate, noise)
        self.learning_rate = learning_rate  # Multiplier for learning speed

    def learn(self, state, action, reward, next_state, current_time, confidence=1.0):
        """Store instance with configurable learning rate"""
        # Adjust activation based on learning rate
        base_activation = np.log(1 + reward + 10)  # Base activation
        adjusted_activation = base_activation * self.learning_rate

        instance = Instance(
            state=frozenset(state.items()) if isinstance(state, dict) else state,
            action=action,
            reward=reward,
            timestamp=current_time,
            activation=adjusted_activation,
            confidence=confidence,
        )
        self.memory.append(instance)


# ============================================================================
# CONFIGURABLE ENVIRONMENT
# ============================================================================


class ConfigurableNetworkEnvironment(NetworkEnvironment):
    """
    Network environment with configurable parameters
    """

    def __init__(
        self,
        num_nodes: int = 50,
        connectivity: float = 0.6,
        vulnerability_distribution: str = "uniform",
        latency_window: Tuple[float, float] = (0.3, 0.8),
    ):
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

        self.node_states = {node: NodeState.CLEAN for node in self.network.nodes()}
        self.current_time = 0
        self.metrics = defaultdict(list)

        # Action costs
        self.action_costs = {
            ActionType.MONITOR: 0.1,
            ActionType.PATCH: 1.5,
            ActionType.ISOLATE: 3.0,
            ActionType.DEPLOY_HONEYPOT: 2.0,
            ActionType.RESTORE_NODE: 6.0,
            ActionType.ACP_DECEPTION: 1.0,
        }


# ============================================================================
# CONFIGURABLE EXPERIMENT RUNNER
# ============================================================================


def run_configurable_episode(episode_id: int, use_acp: bool, config: Dict) -> Dict:
    """
    Run single episode with full configuration control
    """
    np.random.seed(episode_id)

    # Create environment with config
    env = ConfigurableNetworkEnvironment(
        num_nodes=config["num_nodes"],
        connectivity=config["connectivity"],
        vulnerability_distribution=config["vulnerability_distribution"],
        latency_window=config["latency_window"],
    )
    state = env.reset()

    # Create attacker with config
    attacker = ConfigurableAttacker(
        decay_rate=config["decay_rate"],
        noise=config["noise"],
        learning_rate=config["learning_rate"],
    )

    # Create defender with config
    if use_acp:
        defender = ConfigurableACPDefender(
            env.network,
            acp_strength=config["acp_strength"],
            vulnerability_distribution=config["vulnerability_distribution"],
        )
    else:
        defender = ConfigurablePessimisticDefender(
            env.network, vulnerability_distribution=config["vulnerability_distribution"]
        )

    # Run episode
    episode_reward = 0
    step_count = 0
    episode_data = {
        "episode_id": episode_id,
        "use_acp": use_acp,
        "actions": [],
        "rewards_per_step": [],
        "attacker_confidence_trajectory": [],
        "config": config,
    }

    max_steps = min(60, config["num_nodes"])  # Scale with network size

    while True:
        attacker_action = attacker.select_action(state, env.current_time)
        defender_action = defender.select_action(state, attacker.known_nodes)

        next_state, a_reward, d_reward, done = env.step(
            attacker_action, defender_action, attacker, defender
        )

        episode_reward += d_reward
        step_count += 1

        episode_data["actions"].append(defender_action)
        episode_data["rewards_per_step"].append(d_reward)
        episode_data["attacker_confidence_trajectory"].append(attacker.overall_confidence)

        state = next_state

        if done or step_count > max_steps:
            break

    # Summary statistics
    action_counts = defaultdict(int)
    for action in episode_data["actions"]:
        action_counts[action.name] += 1

    episode_data["total_reward"] = episode_reward
    episode_data["steps"] = step_count
    episode_data["final_attacker_confidence"] = attacker.overall_confidence
    episode_data["action_counts"] = dict(action_counts)
    episode_data["acp_deceptions"] = getattr(defender, "acp_deployments", 0)
    episode_data["latency_exploitations"] = len(env.metrics.get("acp_deceptions", []))

    return episode_data


def run_configurable_experiment(
    config: Dict, verbose: bool = True
) -> Tuple[List[Dict], List[Dict]]:
    """
    Run experiment with full configuration
    """
    num_episodes = config["num_episodes"]
    n_cores = config.get("n_cores", None)

    if n_cores is None:
        n_cores = min(cpu_count(), 16)

    if verbose:
        print("=" * 80)
        print("CONFIGURABLE ACP EXPERIMENT")
        print("=" * 80)
        print(f"Total episodes: {num_episodes}")
        print(f"CPU cores: {n_cores}")
        print()
        print("Configuration:")
        for key, value in sorted(config.items()):
            if key not in ["num_episodes", "n_cores"]:
                print(f"  • {key:25s}: {value}")
        print("=" * 80)
        print()

    start_time = time.time()

    # Prepare episode parameters
    episode_params = []
    for episode_id in range(num_episodes):
        use_acp = episode_id % 2 == 0
        episode_params.append((episode_id, use_acp, config))

    # Run in parallel
    if verbose:
        print(f"Starting parallel execution on {n_cores} cores...")

    with Pool(processes=n_cores) as pool:
        results = pool.starmap(run_configurable_episode, episode_params)

    runtime = time.time() - start_time

    if verbose:
        print(f"[SUCCESS] Completed {num_episodes} episodes in {runtime:.2f} seconds")
        print(f"   Average: {runtime/num_episodes*1000:.1f} ms per episode")
        print()

    # Separate results
    acp_results = [r for r in results if r["use_acp"]]
    traditional_results = [r for r in results if not r["use_acp"]]

    return acp_results, traditional_results


# ============================================================================
# STATISTICAL ANALYSIS WITH CONFIGURABLE CI
# ============================================================================


def calculate_configurable_power_analysis(
    acp_rewards: np.ndarray, traditional_rewards: np.ndarray, alpha: float = 0.05
) -> Dict:
    """Power analysis with configurable alpha"""
    mean_acp = np.mean(acp_rewards)
    mean_trad = np.mean(traditional_rewards)
    std_acp = np.std(acp_rewards, ddof=1)
    std_trad = np.std(traditional_rewards, ddof=1)

    pooled_std = np.sqrt((std_acp**2 + std_trad**2) / 2)
    cohen_d = (mean_acp - mean_trad) / pooled_std

    t_stat, p_value = stats.ttest_ind(acp_rewards, traditional_rewards)

    n1 = len(acp_rewards)
    n2 = len(traditional_rewards)
    df = n1 + n2 - 2

    ncp = np.abs(cohen_d) * np.sqrt(n1 * n2 / (n1 + n2))
    critical_t = stats.t.ppf(1 - alpha / 2, df)

    power = 1 - stats.nct.cdf(critical_t, df, ncp) + stats.nct.cdf(-critical_t, df, ncp)

    return {
        "mean_acp": mean_acp,
        "mean_traditional": mean_trad,
        "std_acp": std_acp,
        "std_traditional": std_trad,
        "cohen_d": cohen_d,
        "t_statistic": t_stat,
        "p_value": p_value,
        "degrees_freedom": df,
        "achieved_power": power,
        "alpha": alpha,
        "confidence_level": 1 - alpha,
    }


def bootstrap_configurable_ci(
    acp_rewards: np.ndarray,
    traditional_rewards: np.ndarray,
    n_bootstrap: int = 10000,
    confidence_level: float = 0.95,
) -> Dict:
    """Bootstrap CI with configurable samples and confidence level"""
    np.random.seed(42)

    boot_mean_acp = []
    boot_mean_trad = []
    boot_delta = []
    boot_cohen_d = []

    for _ in range(n_bootstrap):
        sample_acp = np.random.choice(acp_rewards, size=len(acp_rewards), replace=True)
        sample_trad = np.random.choice(
            traditional_rewards, size=len(traditional_rewards), replace=True
        )

        mean_acp = np.mean(sample_acp)
        mean_trad = np.mean(sample_trad)
        delta = mean_acp - mean_trad

        pooled_std = np.sqrt((np.var(sample_acp) + np.var(sample_trad)) / 2)
        cohen_d = delta / pooled_std

        boot_mean_acp.append(mean_acp)
        boot_mean_trad.append(mean_trad)
        boot_delta.append(delta)
        boot_cohen_d.append(cohen_d)

    alpha = 1 - confidence_level
    lower_percentile = alpha / 2 * 100
    upper_percentile = (1 - alpha / 2) * 100

    return {
        "mean_acp_ci": np.percentile(boot_mean_acp, [lower_percentile, upper_percentile]),
        "mean_traditional_ci": np.percentile(boot_mean_trad, [lower_percentile, upper_percentile]),
        "delta_ci": np.percentile(boot_delta, [lower_percentile, upper_percentile]),
        "cohen_d_ci": np.percentile(boot_cohen_d, [lower_percentile, upper_percentile]),
        "confidence_level": confidence_level,
        "n_bootstrap": n_bootstrap,
    }


def analyze_configurable_results(
    acp_results: List[Dict], traditional_results: List[Dict], config: Dict
) -> Dict:
    """Comprehensive analysis with configuration"""

    acp_rewards = np.array([r["total_reward"] for r in acp_results])
    trad_rewards = np.array([r["total_reward"] for r in traditional_results])

    analysis = {
        "acp_mean": np.mean(acp_rewards),
        "acp_std": np.std(acp_rewards, ddof=1),
        "acp_median": np.median(acp_rewards),
        "traditional_mean": np.mean(trad_rewards),
        "traditional_std": np.std(trad_rewards, ddof=1),
        "traditional_median": np.median(trad_rewards),
        "delta": np.mean(acp_rewards) - np.mean(trad_rewards),
        "percent_improvement": (np.mean(acp_rewards) - np.mean(trad_rewards))
        / np.abs(np.mean(trad_rewards))
        * 100,
    }

    # Statistical tests with configured alpha
    alpha = 1 - config.get("confidence_level", 0.95)
    power_results = calculate_configurable_power_analysis(acp_rewards, trad_rewards, alpha)
    analysis["power_analysis"] = power_results

    # Confidence intervals with config
    ci_results = bootstrap_configurable_ci(
        acp_rewards,
        trad_rewards,
        n_bootstrap=config.get("bootstrap_samples", 10000),
        confidence_level=config.get("confidence_level", 0.95),
    )
    analysis["confidence_intervals"] = ci_results

    # Action distributions
    acp_actions = defaultdict(int)
    trad_actions = defaultdict(int)

    for result in acp_results:
        for action, count in result["action_counts"].items():
            acp_actions[action] += count

    for result in traditional_results:
        for action, count in result["action_counts"].items():
            trad_actions[action] += count

    total_acp = sum(acp_actions.values())
    total_trad = sum(trad_actions.values())

    analysis["acp_action_distribution"] = {k: v / total_acp for k, v in acp_actions.items()}
    analysis["traditional_action_distribution"] = {
        k: v / total_trad for k, v in trad_actions.items()
    }

    # Confidence degradation
    acp_conf = [r["final_attacker_confidence"] for r in acp_results]
    trad_conf = [r["final_attacker_confidence"] for r in traditional_results]

    analysis["acp_attacker_confidence"] = np.mean(acp_conf)
    analysis["traditional_attacker_confidence"] = np.mean(trad_conf)
    analysis["confidence_degradation"] = (1 - np.mean(acp_conf) / np.mean(trad_conf)) * 100

    # ACP metrics
    analysis["total_acp_deceptions"] = sum(r["acp_deceptions"] for r in acp_results)
    analysis["total_latency_exploitations"] = sum(r["latency_exploitations"] for r in acp_results)
    analysis["deceptions_per_episode"] = analysis["total_acp_deceptions"] / len(acp_results)

    # Configuration info
    analysis["config"] = config

    return analysis


# ============================================================================
# MAIN WITH FULL ARGUMENT PARSING
# ============================================================================


def main():
    parser = argparse.ArgumentParser(
        description="Fully Configurable ACP Simulation - Advanced Parameter Control",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic run with 1000 episodes
  python %(prog)s --num-episodes 1000

  # Sensitivity analysis: vary ACP strength
  python %(prog)s --acp-strength 0.5 --num-episodes 5000

  # Large network simulation
  python %(prog)s --num-nodes 500 --connectivity 0.4 --num-episodes 2000

  # High precision with 99%% CI
  python %(prog)s --confidence-level 0.99 --bootstrap-samples 50000

  # Fast attacker learning
  python %(prog)s --learning-rate 2.0 --num-episodes 5000

  # Bimodal vulnerability distribution
  python %(prog)s --vulnerability-distribution bimodal --num-episodes 5000
        """,
    )

    # Episode configuration
    parser.add_argument(
        "--num-episodes", type=int, default=1000, help="Total number of episodes (default: 1000)"
    )
    parser.add_argument(
        "--cores", type=int, default=None, help="Number of CPU cores (default: auto-detect)"
    )

    # ACP configuration
    parser.add_argument(
        "--acp-strength",
        type=float,
        default=0.65,
        help="ACP deception probability 0.0-1.0 (default: 0.65)",
    )

    # Network configuration
    parser.add_argument(
        "--num-nodes", type=int, default=50, help="Number of nodes in network (default: 50)"
    )
    parser.add_argument(
        "--connectivity",
        type=float,
        default=0.6,
        help="Network connectivity 0.0-1.0 (default: 0.6)",
    )

    # Latency configuration
    parser.add_argument(
        "--latency-window-min",
        type=float,
        default=0.3,
        help="Minimum cognitive latency for attacker (default: 0.3)",
    )
    parser.add_argument(
        "--latency-window-max",
        type=float,
        default=0.8,
        help="Maximum cognitive latency for attacker (default: 0.8)",
    )

    # Statistical configuration
    parser.add_argument(
        "--confidence-level",
        type=float,
        default=0.95,
        help="Confidence level 0.90/0.95/0.99 (default: 0.95)",
    )
    parser.add_argument(
        "--bootstrap-samples", type=int, default=10000, help="Bootstrap samples (default: 10000)"
    )

    # Attacker configuration
    parser.add_argument(
        "--learning-rate",
        type=float,
        default=1.0,
        help="Attacker learning rate multiplier (default: 1.0)",
    )
    parser.add_argument(
        "--decay-rate", type=float, default=0.8, help="Memory decay rate (default: 0.8)"
    )
    parser.add_argument("--noise", type=float, default=0.1, help="Decision noise (default: 0.1)")

    # Vulnerability configuration
    parser.add_argument(
        "--vulnerability-distribution",
        type=str,
        default="uniform",
        choices=["uniform", "normal", "exponential", "bimodal"],
        help="Vulnerability distribution (default: uniform)",
    )

    # Output configuration
    parser.add_argument(
        "--output-dir", type=str, default=".", help="Output directory (default: current)"
    )
    parser.add_argument(
        "--output-prefix", type=str, default="config", help="Output file prefix (default: config)"
    )
    parser.add_argument(
        "--save-config", action="store_true", help="Save configuration to JSON file"
    )

    args = parser.parse_args()

    # Validate parameters
    if not 0.0 <= args.acp_strength <= 1.0:
        parser.error("--acp-strength must be between 0.0 and 1.0")
    if not 0.0 <= args.connectivity <= 1.0:
        parser.error("--connectivity must be between 0.0 and 1.0")
    if not 0.0 <= args.latency_window_min <= 5.0:
        parser.error("--latency-window-min must be between 0.0 and 5.0")
    if not 0.0 <= args.latency_window_max <= 5.0:
        parser.error("--latency-window-max must be between 0.0 and 5.0")
    if args.latency_window_min > args.latency_window_max:
        parser.error("--latency-window-min must be <= --latency-window-max")
    if args.confidence_level not in [0.90, 0.95, 0.99]:
        parser.error("--confidence-level must be 0.90, 0.95, or 0.99")
    if args.num_nodes < 10:
        parser.error("--num-nodes must be at least 10")

    # Build configuration
    config = {
        "num_episodes": args.num_episodes,
        "n_cores": args.cores,
        "acp_strength": args.acp_strength,
        "num_nodes": args.num_nodes,
        "connectivity": args.connectivity,
        "latency_window": (args.latency_window_min, args.latency_window_max),
        "confidence_level": args.confidence_level,
        "bootstrap_samples": args.bootstrap_samples,
        "learning_rate": args.learning_rate,
        "decay_rate": args.decay_rate,
        "noise": args.noise,
        "vulnerability_distribution": args.vulnerability_distribution,
    }

    # Save configuration if requested
    if args.save_config:
        config_file = f"{args.output_dir}/{args.output_prefix}_config.json"
        with open(config_file, "w") as f:
            json.dump(config, f, indent=2)
        print(f"✅ Configuration saved to {config_file}")
        print()

    # Print header
    print("\n" + "=" * 80)
    print("CONFIGURABLE ACP SIMULATION - ADVANCED PARAMETERS".center(80))
    print("=" * 80)
    print()

    # Run experiment
    acp_results, traditional_results = run_configurable_experiment(config, verbose=True)

    # Analyze results
    print("Performing statistical analysis...")
    analysis = analyze_configurable_results(acp_results, traditional_results, config)

    # Print results
    print()
    print("=" * 80)
    print("RESULTS SUMMARY")
    print("=" * 80)
    print()

    pa = analysis["power_analysis"]
    ci = analysis["confidence_intervals"]

    print("Configuration Parameters:")
    print(f"  • ACP Strength: {config['acp_strength']:.2f}")
    print(f"  • Network Size: {config['num_nodes']} nodes")
    print(f"  • Connectivity: {config['connectivity']:.2f}")
    print(f"  • Learning Rate: {config['learning_rate']:.2f}x")
    print(f"  • Vulnerability: {config['vulnerability_distribution']}")
    print(f"  • Confidence Level: {config['confidence_level']*100:.0f}%")
    print()

    print("Statistical Results:")
    print(
        f"  • ACP Mean: {analysis['acp_mean']:.2f} "
        f"[{ci['mean_acp_ci'][0]:.2f}, {ci['mean_acp_ci'][1]:.2f}]"
    )
    print(
        f"  • Traditional Mean: {analysis['traditional_mean']:.2f} "
        f"[{ci['mean_traditional_ci'][0]:.2f}, {ci['mean_traditional_ci'][1]:.2f}]"
    )
    print(f"  • Improvement: {analysis['percent_improvement']:.1f}%")
    print(
        f"  • Cohen's d: {pa['cohen_d']:.3f} [{ci['cohen_d_ci'][0]:.3f}, {ci['cohen_d_ci'][1]:.3f}]"
    )
    print(f"  • p-value: {pa['p_value']:.2e}")
    print(f"  • Power: {pa['achieved_power']:.4f}")
    print()

    # Save results
    output_file = f"{args.output_dir}/{args.output_prefix}_results.pkl"
    results_package = {
        "acp_results": acp_results,
        "traditional_results": traditional_results,
        "analysis": analysis,
        "config": config,
        "timestamp": time.time(),
    }

    with open(output_file, "wb") as f:
        pickle.dump(results_package, f)

    print(f"[SUCCESS] Results saved to {output_file}")
    print()
    print("=" * 80)
    print("EXPERIMENT COMPLETE")
    print("=" * 80)
    print()


if __name__ == "__main__":
    main()
