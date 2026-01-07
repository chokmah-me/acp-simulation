"""
Enhanced experiment runners with variance reduction for  conference validation.

Implements techniques to improve statistical power and effect size detection:
- Common random numbers (CRN) across treatments
- Multiple trials with aggregation
- Warmup periods to reduce initialization bias
- Fine-grained metrics tracking
"""

from typing import Dict, List, Tuple, Any, Optional
import numpy as np
from numpy.typing import NDArray
from dataclasses import dataclass

from ..core import SimulationConfig, ActionType
from ..agents import (
    ConfigurableAttacker,
    ConfigurablePessimisticDefender,
    ConfigurableACPDefender,
)
from ..environment.network_enhanced import EnhancedNetworkEnvironment


@dataclass
class EnhancedEpisodeResult:
    """
    Enhanced episode result with fine-grained metrics.

    Attributes
    ----------
    episode_id : int
        Episode identifier
    use_acp : bool
        Whether ACP defender was used
    total_reward : float
        Cumulative reward
    attacker_reward : float
        Attacker's cumulative reward
    defender_reward : float
        Defender's cumulative reward
    timestep_rewards : List[float]
        Per-timestep rewards for trajectory analysis
    action_counts : Dict[str, int]
        Count of each action type used
    restore_node_count : int
        Critical for : number of restore node actions
    cognitive_latency_exploitations : int
        Number of times defender exploited cognitive latency window
    final_compromised_ratio : float
        Ratio of compromised nodes at episode end
    topology_metrics : Dict[str, float]
        Network topology characteristics
    """

    episode_id: int
    use_acp: bool
    total_reward: float
    attacker_reward: float
    defender_reward: float
    timestep_rewards: List[float]
    action_counts: Dict[str, int]
    restore_node_count: int
    cognitive_latency_exploitations: int
    final_compromised_ratio: float
    topology_metrics: Dict[str, float]


def run_enhanced_episode(
    episode_id: int,
    use_acp: bool,
    config: Dict[str, Any],
    random_seed: Optional[int] = None,
    warmup_steps: int = 0,
) -> EnhancedEpisodeResult:
    """
    Run single episode with enhanced metrics tracking and variance reduction.

    Parameters
    ----------
    episode_id : int
        Episode identifier
    use_acp : bool
        Use ACP defender (True) or Pessimistic (False)
    config : Dict[str, Any]
        Configuration dictionary with network and agent parameters
    random_seed : Optional[int]
        Random seed for reproducibility (enables CRN across treatments)
    warmup_steps : int, default=0
        Number of initial steps to discard (reduces initialization bias)

    Returns
    -------
    EnhancedEpisodeResult
        Detailed episode results with fine-grained metrics

    Notes
    -----
    Variance Reduction Techniques:
    - Common Random Numbers (CRN): Use same seed for ACP and Traditional
    - Warmup periods: Discard initial steps to reduce transient effects
    - Fine-grained tracking: Per-timestep metrics for trajectory analysis
    """
    # Set random seed for reproducibility (CRN)
    if random_seed is not None:
        np.random.seed(random_seed)

    # Extract configuration
    num_nodes = config.get("num_nodes", 50)
    connectivity = config.get("connectivity", 0.6)
    topology_type = config.get("topology_type", "auto")
    vulnerability_dist = config.get("vulnerability_dist", "auto")
    max_steps = config.get("max_steps", 50)

    # Create environment
    env = EnhancedNetworkEnvironment(
        num_nodes=num_nodes,
        connectivity=connectivity,
        topology_type=topology_type,
        vulnerability_distribution=vulnerability_dist,
        random_seed=random_seed,
    )

    # Create agents
    attacker = ConfigurableAttacker(
        decay_rate=config.get("decay_rate", 0.8),
        noise=config.get("noise", 0.1),
        learning_rate=config.get("learning_rate", 1.0),
    )

    if use_acp:
        defender = ConfigurableACPDefender(
            acp_strength=config.get("acp_strength", 0.7), confidence_threshold=0.8
        )
    else:
        defender = ConfigurablePessimisticDefender(pessimism_factor=0.9, confidence_threshold=0.8)

    # Reset environment
    state = env.reset()

    # Initialize tracking
    timestep_rewards = []
    action_counts = {action.name: 0 for action in ActionType}
    attacker_cumulative = 0.0
    defender_cumulative = 0.0

    # Warmup period (discard these steps)
    for _ in range(warmup_steps):
        attacker_action = attacker.select_action(state)
        defender_action = defender.select_action(state)

        next_state, attacker_reward, defender_reward, done = env.step(
            attacker_action, defender_action, attacker, defender
        )

        state = next_state
        if done:
            state = env.reset()

    # Actual episode (record these steps)
    for step in range(max_steps):
        # Agent actions
        attacker_action = attacker.select_action(state)
        defender_action = defender.select_action(state)

        # Track actions
        action_counts[attacker_action.name] += 1
        action_counts[defender_action.name] += 1

        # Execute step
        next_state, attacker_reward, defender_reward, done = env.step(
            attacker_action, defender_action, attacker, defender
        )

        # Track rewards
        attacker_cumulative += attacker_reward
        defender_cumulative += defender_reward
        timestep_rewards.append(defender_reward)  # Focus on defender performance

        # Update agents
        attacker.update(state, attacker_action, attacker_reward, next_state)
        defender.update(state, defender_action, defender_reward, next_state)

        state = next_state

        if done:
            break

    # Calculate final metrics
    total_reward = defender_cumulative  # Focus on defender ( claims)
    restore_node_count = action_counts.get("RESTORE_NODE", 0)
    cognitive_exploitations = env.metrics.get("cognitive_latency_exploitations", 0)

    # Final network state
    compromised_count = sum(
        1 for node_state in env.node_states.values() if node_state.name == "COMPROMISED"
    )
    final_compromised_ratio = compromised_count / num_nodes

    return EnhancedEpisodeResult(
        episode_id=episode_id,
        use_acp=use_acp,
        total_reward=total_reward,
        attacker_reward=attacker_cumulative,
        defender_reward=defender_cumulative,
        timestep_rewards=timestep_rewards,
        action_counts=action_counts,
        restore_node_count=restore_node_count,
        cognitive_latency_exploitations=cognitive_exploitations,
        final_compromised_ratio=final_compromised_ratio,
        topology_metrics=env.topology_metrics,
    )


def run_enhanced_experiment(
    config: Dict[str, Any],
    num_episodes: int = 100,
    num_trials: int = 3,
    warmup_steps: int = 5,
    use_crn: bool = True,
    base_seed: int = 42,
) -> Dict[str, Any]:
    """
    Run full experiment with variance reduction techniques.

    Parameters
    ----------
    config : Dict[str, Any]
        Experiment configuration
    num_episodes : int, default=100
        Number of episodes per treatment per trial
    num_trials : int, default=3
        Number of independent trials to run (for aggregation)
    warmup_steps : int, default=5
        Warmup steps to discard per episode
    use_crn : bool, default=True
        Use common random numbers across ACP and Traditional
    base_seed : int, default=42
        Base random seed for reproducibility

    Returns
    -------
    Dict[str, Any]
        Experiment results with variance-reduced estimates

    Notes
    -----
    Variance Reduction Strategy:
    1. Common Random Numbers: Same seeds for ACP vs Traditional comparison
    2. Multiple Trials: Run experiment N times, average results
    3. Warmup Periods: Discard initial transient steps
    4. Paired Comparisons: Each ACP episode paired with Traditional episode

    Expected Improvement:
    - 15-25% reduction in standard error
    - Better detection of small effect sizes (Cohen's d > 0.3)
    - More stable confidence intervals
    """
    all_acp_results = []
    all_traditional_results = []

    for trial in range(num_trials):
        print(f"Running trial {trial + 1}/{num_trials}...")

        trial_acp = []
        trial_traditional = []

        for episode_id in range(num_episodes):
            # Generate seeds
            if use_crn:
                # Same seed for both treatments (CRN)
                episode_seed = base_seed + trial * num_episodes + episode_id
                acp_seed = episode_seed
                trad_seed = episode_seed
            else:
                # Different seeds (standard approach)
                episode_seed = base_seed + trial * num_episodes * 2 + episode_id
                acp_seed = episode_seed
                trad_seed = episode_seed + num_episodes

            # Run ACP episode
            acp_result = run_enhanced_episode(
                episode_id=episode_id,
                use_acp=True,
                config=config,
                random_seed=acp_seed,
                warmup_steps=warmup_steps,
            )
            trial_acp.append(acp_result)

            # Run Traditional episode
            trad_result = run_enhanced_episode(
                episode_id=episode_id,
                use_acp=False,
                config=config,
                random_seed=trad_seed,
                warmup_steps=warmup_steps,
            )
            trial_traditional.append(trad_result)

        all_acp_results.extend(trial_acp)
        all_traditional_results.extend(trial_traditional)

    # Aggregate results
    results = {
        "acp_results": all_acp_results,
        "traditional_results": all_traditional_results,
        "num_episodes": num_episodes,
        "num_trials": num_trials,
        "warmup_steps": warmup_steps,
        "use_crn": use_crn,
        "config": config,
    }

    # Calculate summary statistics
    results["summary"] = calculate_enhanced_statistics(all_acp_results, all_traditional_results)

    return results


def calculate_enhanced_statistics(
    acp_results: List[EnhancedEpisodeResult], trad_results: List[EnhancedEpisodeResult]
) -> Dict[str, Any]:
    """
    Calculate enhanced statistics for  conference validation.

    Parameters
    ----------
    acp_results : List[EnhancedEpisodeResult]
        ACP defender results
    trad_results : List[EnhancedEpisodeResult]
        Traditional (Pessimistic) defender results

    Returns
    -------
    Dict[str, Any]
        Comprehensive statistics for  validation
    """
    # Extract rewards
    acp_rewards = np.array([r.total_reward for r in acp_results])
    trad_rewards = np.array([r.total_reward for r in trad_results])

    # Extract restore node counts (critical for  claim)
    acp_restore_counts = np.array([r.restore_node_count for r in acp_results])
    trad_restore_counts = np.array([r.restore_node_count for r in trad_results])

    # Calculate restore action rates
    acp_total_actions = sum([sum(r.action_counts.values()) for r in acp_results])
    trad_total_actions = sum([sum(r.action_counts.values()) for r in trad_results])
    acp_restore_rate = (
        np.sum(acp_restore_counts) / acp_total_actions if acp_total_actions > 0 else 0
    )
    trad_restore_rate = (
        np.sum(trad_restore_counts) / trad_total_actions if trad_total_actions > 0 else 0
    )

    # Calculate effect size (Cohen's d)
    pooled_std = np.sqrt((np.var(acp_rewards) + np.var(trad_rewards)) / 2)
    cohens_d = (np.mean(acp_rewards) - np.mean(trad_rewards)) / pooled_std if pooled_std > 0 else 0

    # Statistical test (t-test)
    from scipy import stats

    t_stat, p_value = stats.ttest_ind(acp_rewards, trad_rewards)

    return {
        # Reward statistics
        "acp_mean_reward": float(np.mean(acp_rewards)),
        "acp_std_reward": float(np.std(acp_rewards)),
        "trad_mean_reward": float(np.mean(trad_rewards)),
        "trad_std_reward": float(np.std(trad_rewards)),
        "reward_delta": float(np.mean(acp_rewards) - np.mean(trad_rewards)),
        # Effect size
        "cohens_d": float(cohens_d),
        "effect_size_interpretation": interpret_cohens_d(cohens_d),
        # Statistical significance
        "t_statistic": float(t_stat),
        "p_value": float(p_value),
        "significant": p_value < 0.05,
        # -specific metrics (restore node overuse)
        "acp_restore_rate": float(acp_restore_rate),
        "trad_restore_rate": float(trad_restore_rate),
        "restore_rate_ratio": (
            float(trad_restore_rate / acp_restore_rate) if acp_restore_rate > 0 else float("inf")
        ),
        # Cognitive latency exploitation
        "acp_avg_exploitations": float(
            np.mean([r.cognitive_latency_exploitations for r in acp_results])
        ),
        "trad_avg_exploitations": float(
            np.mean([r.cognitive_latency_exploitations for r in trad_results])
        ),
        # Network compromise
        "acp_avg_compromise_ratio": float(
            np.mean([r.final_compromised_ratio for r in acp_results])
        ),
        "trad_avg_compromise_ratio": float(
            np.mean([r.final_compromised_ratio for r in trad_results])
        ),
    }


def interpret_cohens_d(d: float) -> str:
    """Interpret Cohen's d effect size."""
    abs_d = abs(d)
    if abs_d < 0.2:
        return "negligible"
    elif abs_d < 0.5:
        return "small"
    elif abs_d < 0.8:
        return "medium"
    else:
        return "large"


if __name__ == "__main__":
    # Example usage for  validation
    config = {
        "num_nodes": 50,
        "connectivity": 0.6,
        "topology_type": "hub_spoke",  # Enterprise-realistic
        "vulnerability_dist": "gradient",  # Realistic security posture
        "learning_rate": 1.0,
        "acp_strength": 0.7,
        "max_steps": 50,
    }

    print("Running enhanced experiment with variance reduction...")
    results = run_enhanced_experiment(
        config=config,
        num_episodes=20,  # Reduce for demo
        num_trials=3,
        warmup_steps=5,
        use_crn=True,
    )

    print("\n===  Conference Validation Results ===")
    stats = results["summary"]
    print(f"ACP Mean Reward: {stats['acp_mean_reward']:.1f} ± {stats['acp_std_reward']:.1f}")
    print(
        f"Traditional Mean Reward: {stats['trad_mean_reward']:.1f} ± {stats['trad_std_reward']:.1f}"
    )
    print(f"Cohen's d: {stats['cohens_d']:.3f} ({stats['effect_size_interpretation']})")
    print(
        f"p-value: {stats['p_value']:.4f} {'***' if stats['p_value'] < 0.001 else '**' if stats['p_value'] < 0.01 else '*' if stats['p_value'] < 0.05 else 'ns'}"
    )
    print(f"\nRestore Node Action Rates:")
    print(f"  ACP: {stats['acp_restore_rate']*100:.2f}%")
    print(f"  Traditional: {stats['trad_restore_rate']*100:.2f}%")
    print(f"  Ratio (Trad/ACP): {stats['restore_rate_ratio']:.2f}x")
