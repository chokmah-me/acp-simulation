"""
Tests for simulation runner.
"""

import pytest
import numpy as np
from acp_simulation import SimulationConfig
from acp_simulation.simulation import run_single_episode, run_experiment


class TestSimulationRunner:
    """Test simulation runner functionality."""

    def test_run_single_episode_acp(self):
        """Test running a single episode with ACP defender."""
        config = SimulationConfig(num_episodes=10, num_nodes=20, random_seed=42)

        result = run_single_episode(0, True, config)

        assert result["episode_id"] == 0
        assert result["use_acp"] is True
        assert "total_reward" in result
        assert "steps" in result
        assert "actions" in result
        assert "action_counts" in result
        assert isinstance(result["total_reward"], (int, float))
        assert result["steps"] > 0
        assert result["steps"] <= config.max_steps_per_episode

    def test_run_single_episode_traditional(self):
        """Test running a single episode with Traditional defender."""
        config = SimulationConfig(num_episodes=10, num_nodes=20, random_seed=42)

        result = run_single_episode(1, False, config)

        assert result["episode_id"] == 1
        assert result["use_acp"] is False
        assert "total_reward" in result
        assert result["steps"] > 0

    def test_run_single_episode_reproducibility(self):
        """Test that same seed produces same results."""
        config = SimulationConfig(num_episodes=10, num_nodes=20, random_seed=42)

        result1 = run_single_episode(5, True, config)
        result2 = run_single_episode(5, True, config)

        # Should be identical due to same seed
        assert result1["total_reward"] == result2["total_reward"]
        assert result1["steps"] == result2["steps"]
        assert result1["action_counts"] == result2["action_counts"]

    def test_run_experiment_small(self):
        """Test running a small experiment."""
        config = SimulationConfig(num_episodes=20, num_nodes=20, random_seed=42)

        acp_rewards, traditional_rewards, analysis = run_experiment(config, verbose=False)

        # Check reward arrays
        assert len(acp_rewards) == 10  # Half of episodes
        assert len(traditional_rewards) == 10
        assert np.all(np.isfinite(acp_rewards))
        assert np.all(np.isfinite(traditional_rewards))

        # Check analysis
        assert "acp_mean" in analysis
        assert "traditional_mean" in analysis
        assert "delta" in analysis
        assert "power_analysis" in analysis
        assert "confidence_intervals" in analysis

        # Check power analysis
        pa = analysis["power_analysis"]
        assert "cohen_d" in pa
        assert "p_value" in pa
        assert "achieved_power" in pa

    def test_configurable_parameters(self):
        """Test experiment with custom parameters."""
        config = SimulationConfig(
            num_episodes=20,
            num_nodes=30,
            connectivity=0.7,
            acp_strength=0.8,
            learning_rate=1.5,
            random_seed=123,
        )

        acp_rewards, traditional_rewards, analysis = run_experiment(config, verbose=False)

        assert len(acp_rewards) == 10
        assert len(traditional_rewards) == 10
        assert "config" in analysis
        assert analysis["config"]["acp_strength"] == 0.8
        assert analysis["config"]["learning_rate"] == 1.5

    def test_action_distribution_tracking(self):
        """Test that action distributions are tracked correctly."""
        config = SimulationConfig(num_episodes=20, num_nodes=20, random_seed=42)

        acp_rewards, traditional_rewards, analysis = run_experiment(config, verbose=False)

        # Check action distributions exist
        assert "acp_action_distribution" in analysis
        assert "traditional_action_distribution" in analysis

        # Check distributions sum to 1
        acp_dist = analysis["acp_action_distribution"]
        trad_dist = analysis["traditional_action_distribution"]

        assert abs(sum(acp_dist.values()) - 1.0) < 0.01
        assert abs(sum(trad_dist.values()) - 1.0) < 0.01

        # Check that RESTORE_NODE is tracked
        assert "RESTORE_NODE" in trad_dist

    def test_confidence_tracking(self):
        """Test that attacker confidence is tracked."""
        config = SimulationConfig(num_episodes=20, num_nodes=20, random_seed=42)

        acp_rewards, traditional_rewards, analysis = run_experiment(config, verbose=False)

        # Check confidence metrics
        assert "acp_attacker_confidence" in analysis
        assert "traditional_attacker_confidence" in analysis
        assert "confidence_degradation" in analysis

        # Confidence should be between 0 and 1
        assert 0 <= analysis["acp_attacker_confidence"] <= 1
        assert 0 <= analysis["traditional_attacker_confidence"] <= 1
