"""
Experiment runners for ACP simulation.

This module provides functions to run ACP experiments including:
- Single episode execution
- Full experiments (ACP vs Traditional)
- Parallel processing support
- Result collection and aggregation
"""

from typing import Dict, List, Tuple, Any
import numpy as np
from numpy.typing import NDArray
from multiprocessing import Pool, cpu_count
from functools import partial

from ..core import SimulationConfig, ActionType
from ..agents import (
    CognitiveAttacker,
    PessimisticDefender,
    OptimisticACPDefender,
    ConfigurableAttacker,
    ConfigurablePessimisticDefender,
    ConfigurableACPDefender,
)
from ..environment import NetworkEnvironment, ConfigurableNetworkEnvironment
from ..analysis import analyze_experiment_results


def run_single_episode(episode_id: int, use_acp: bool, config: SimulationConfig) -> Dict[str, Any]:
    """
    Run a single episode of ACP simulation.

    Parameters
    ----------
    episode_id : int
        Unique episode identifier
    use_acp : bool
        Whether to use ACP defender (True) or Traditional (False)
    config : SimulationConfig
        Simulation configuration

    Returns
    -------
    Dict[str, Any]
        Episode results including rewards, actions, and metrics
    """
    # Set deterministic seed for this episode
    episode_seed = config.get_episode_seed(episode_id)
    np.random.seed(episode_seed)

    # Also set Python's random seed for any other random operations
    import random

    random.seed(episode_seed)

    # Create environment
    if (
        config.num_nodes == 50
        and config.connectivity == 0.6
        and config.vulnerability_distribution == "uniform"
    ):
        # Use base environment for default parameters
        env = NetworkEnvironment(num_nodes=config.num_nodes, connectivity=config.connectivity)
    else:
        # Use configurable environment for custom parameters
        env = ConfigurableNetworkEnvironment(
            num_nodes=config.num_nodes,
            connectivity=config.connectivity,
            vulnerability_distribution=config.vulnerability_distribution,
        )

    state = env.reset()

    # Create attacker
    if config.learning_rate == 1.0 and config.decay_rate == 0.8 and config.noise == 0.1:
        # Use base attacker for default parameters
        attacker = CognitiveAttacker(decay_rate=config.decay_rate, noise=config.noise)
    else:
        # Use configurable attacker for custom parameters
        attacker = ConfigurableAttacker(
            decay_rate=config.decay_rate, noise=config.noise, learning_rate=config.learning_rate
        )

    # Create defender
    if use_acp:
        if config.acp_strength == 0.65 and config.vulnerability_distribution == "uniform":
            # Use base ACP defender for default parameters
            defender = OptimisticACPDefender(env.network, acp_strength=config.acp_strength)
        else:
            # Use configurable ACP defender for custom parameters
            defender = ConfigurableACPDefender(
                env.network,
                acp_strength=config.acp_strength,
                vulnerability_distribution=config.vulnerability_distribution,
            )
    else:
        if config.vulnerability_distribution == "uniform":
            # Use base traditional defender for default parameters
            defender = PessimisticDefender(env.network)
        else:
            # Use configurable traditional defender for custom parameters
            defender = ConfigurablePessimisticDefender(
                env.network, vulnerability_distribution=config.vulnerability_distribution
            )

    # Run episode
    episode_reward = 0.0
    step_count = 0
    actions = []
    rewards_per_step = []
    attacker_confidence_trajectory = []

    max_steps = min(config.max_steps_per_episode, config.num_nodes)

    while True:
        # Attacker selects action
        attacker_action = attacker.select_action(state, env.current_time)

        # Defender selects action
        defender_action = defender.select_action(state, attacker.known_nodes)

        # Execute step
        next_state, a_reward, d_reward, done = env.step(
            attacker_action, defender_action, attacker, defender
        )

        episode_reward += d_reward
        step_count += 1

        # Record data
        actions.append(defender_action)
        rewards_per_step.append(d_reward)
        attacker_confidence_trajectory.append(attacker.overall_confidence)

        state = next_state

        if done or step_count > max_steps:
            break

    # Count actions
    from collections import defaultdict

    action_counts = defaultdict(int)
    for action in actions:
        action_counts[action.name] += 1

    return {
        "episode_id": episode_id,
        "use_acp": use_acp,
        "total_reward": episode_reward,
        "steps": step_count,
        "actions": actions,
        "action_counts": dict(action_counts),
        "rewards_per_step": rewards_per_step,
        "final_attacker_confidence": attacker.overall_confidence,
        "attacker_confidence_trajectory": attacker_confidence_trajectory,
        "config": config.to_dict(),
    }


def run_experiment(
    config: SimulationConfig, verbose: bool = True
) -> Tuple[NDArray[np.float64], NDArray[np.float64], Dict[str, Any]]:
    """
    Run complete ACP experiment (ACP vs Traditional).

    Parameters
    ----------
    config : SimulationConfig
        Experiment configuration
    verbose : bool, default=True
        Print progress information

    Returns
    -------
    Tuple[NDArray[np.float64], NDArray[np.float64], Dict[str, Any]]
        (acp_rewards, traditional_rewards, analysis_results)
    """
    if verbose:
        print("=" * 80)
        print("ACP EXPERIMENT")
        print("=" * 80)
        print(f"Episodes: {config.num_episodes}")
        print(f"Configuration: {config.to_dict()}")
        print("=" * 80)
        print()

    # Run episodes
    acp_results = []
    traditional_results = []

    for episode_id in range(config.num_episodes):
        if verbose and episode_id % 50 == 0:
            print(f"Episode {episode_id}/{config.num_episodes}")

        # Alternate between ACP and Traditional
        use_acp = episode_id % 2 == 0

        # Run episode
        result = run_single_episode(episode_id, use_acp, config)

        # Store results
        if use_acp:
            acp_results.append(result)
        else:
            traditional_results.append(result)

    if verbose:
        print(f"Completed {config.num_episodes} episodes")
        print()

    # Extract reward arrays
    acp_rewards = np.array([r["total_reward"] for r in acp_results])
    traditional_rewards = np.array([r["total_reward"] for r in traditional_results])

    # Aggregate action counts
    from collections import defaultdict

    acp_action_counts = defaultdict(int)
    traditional_action_counts = defaultdict(int)

    for result in acp_results:
        for action, count in result["action_counts"].items():
            acp_action_counts[action] += count

    for result in traditional_results:
        for action, count in result["action_counts"].items():
            traditional_action_counts[action] += count

    # Aggregate confidence scores
    acp_confidence_scores = np.array([r["final_attacker_confidence"] for r in acp_results])
    traditional_confidence_scores = np.array(
        [r["final_attacker_confidence"] for r in traditional_results]
    )

    # Analyze results
    analysis = analyze_experiment_results(
        acp_results=acp_rewards,
        traditional_results=traditional_rewards,
        acp_action_counts=dict(acp_action_counts),
        traditional_action_counts=dict(traditional_action_counts),
        acp_confidence_scores=acp_confidence_scores,
        traditional_confidence_scores=traditional_confidence_scores,
        config=config.to_dict(),
    )

    # Add episode details to analysis
    analysis["acp_episodes"] = acp_results
    analysis["traditional_episodes"] = traditional_results

    return acp_rewards, traditional_rewards, analysis


def run_experiment_parallel(
    config: SimulationConfig, n_workers: int = None, verbose: bool = True
) -> Tuple[NDArray[np.float64], NDArray[np.float64], Dict[str, Any]]:
    """
    Run ACP experiment in parallel using multiprocessing.

    Parameters
    ----------
    config : SimulationConfig
        Experiment configuration
    n_workers : int, optional
        Number of parallel workers (default: cpu_count())
    verbose : bool, default=True
        Print progress information

    Returns
    -------
    Tuple[NDArray[np.float64], NDArray[np.float64], Dict[str, Any]]
        (acp_rewards, traditional_rewards, analysis_results)
    """
    if n_workers is None:
        n_workers = min(cpu_count(), 16)

    if verbose:
        print("=" * 80)
        print("PARALLEL ACP EXPERIMENT")
        print("=" * 80)
        print(f"Episodes: {config.num_episodes}")
        print(f"Workers: {n_workers}")
        print("=" * 80)
        print()

    # Prepare episode parameters
    episode_params = [(i, (i % 2 == 0), config) for i in range(config.num_episodes)]

    # Run in parallel
    if verbose:
        print(f"Starting parallel execution...")

    with Pool(processes=n_workers) as pool:
        results = pool.starmap(run_single_episode, episode_params)

    if verbose:
        print(f"Completed {config.num_episodes} episodes")
        print()

    # Separate results
    acp_results = [r for r in results if r["use_acp"]]
    traditional_results = [r for r in results if not r["use_acp"]]

    # Extract reward arrays
    acp_rewards = np.array([r["total_reward"] for r in acp_results])
    traditional_rewards = np.array([r["total_reward"] for r in traditional_results])

    # Aggregate action counts
    from collections import defaultdict

    acp_action_counts = defaultdict(int)
    traditional_action_counts = defaultdict(int)

    for result in acp_results:
        for action, count in result["action_counts"].items():
            acp_action_counts[action] += count

    for result in traditional_results:
        for action, count in result["action_counts"].items():
            traditional_action_counts[action] += count

    # Aggregate confidence scores
    acp_confidence_scores = np.array([r["final_attacker_confidence"] for r in acp_results])
    traditional_confidence_scores = np.array(
        [r["final_attacker_confidence"] for r in traditional_results]
    )

    # Analyze results
    analysis = analyze_experiment_results(
        acp_results=acp_rewards,
        traditional_results=traditional_rewards,
        acp_action_counts=dict(acp_action_counts),
        traditional_action_counts=dict(traditional_action_counts),
        acp_confidence_scores=acp_confidence_scores,
        traditional_confidence_scores=traditional_confidence_scores,
        config=config.to_dict(),
    )

    # Add episode details to analysis
    analysis["acp_episodes"] = acp_results
    analysis["traditional_episodes"] = traditional_results

    return acp_rewards, traditional_rewards, analysis
