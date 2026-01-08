"""
Extended tests for simulation runner to increase coverage.

This test module provides additional coverage for edge cases and
alternative code paths in the simulation runner.
"""

import pytest
import numpy as np
from unittest.mock import patch
import io

from src.acp_simulation import SimulationConfig
from src.acp_simulation.simulation import run_experiment, run_single_episode, run_experiment_parallel


class TestRunnerAlternativePaths:
    """Test alternative code paths in runner functions."""

    def test_run_single_episode_with_base_environment(self):
        """Test that base NetworkEnvironment is used for default parameters (line 65)."""
        # Default parameters should trigger NetworkEnvironment
        config = SimulationConfig(
            num_nodes=50,  # default
            connectivity=0.6,  # default
            vulnerability_distribution="uniform",  # default
            random_seed=42,
        )

        result = run_single_episode(0, True, config)

        assert result["episode_id"] == 0
        assert result["use_acp"] is True
        assert isinstance(result["total_reward"], (int, float))

    def test_run_single_episode_with_custom_network_params(self):
        """Test that ConfigurableNetworkEnvironment is used for custom params."""
        config = SimulationConfig(
            num_nodes=30,  # non-default
            connectivity=0.7,  # non-default
            vulnerability_distribution="normal",  # non-default
            random_seed=42,
        )

        result = run_single_episode(0, True, config)

        assert result["episode_id"] == 0
        assert isinstance(result["total_reward"], (int, float))

    def test_run_single_episode_traditional_with_custom_vulnerability(self):
        """Test traditional defender with custom vulnerability distribution (line 104)."""
        config = SimulationConfig(
            num_nodes=20,
            vulnerability_distribution="exponential",  # non-uniform
            random_seed=42,
        )

        # Use traditional defender (use_acp=False)
        result = run_single_episode(0, False, config)

        assert result["use_acp"] is False
        assert isinstance(result["total_reward"], (int, float))

    def test_run_single_episode_traditional_with_uniform_vulnerability(self):
        """Test traditional defender with uniform vulnerability distribution (line 101)."""
        config = SimulationConfig(
            num_nodes=20,
            vulnerability_distribution="uniform",
            random_seed=42,
        )

        # Use traditional defender with uniform (should use PessimisticDefender)
        result = run_single_episode(0, False, config)

        assert result["use_acp"] is False
        assert isinstance(result["total_reward"], (int, float))

    def test_run_single_episode_with_custom_attacker_params(self):
        """Test that ConfigurableAttacker is used for custom parameters."""
        config = SimulationConfig(
            num_nodes=20,
            learning_rate=1.5,  # non-default
            decay_rate=0.9,  # non-default
            noise=0.2,  # non-default
            random_seed=42,
        )

        result = run_single_episode(0, True, config)

        assert result["episode_id"] == 0
        assert isinstance(result["total_reward"], (int, float))

    def test_run_single_episode_acp_with_custom_acp_strength(self):
        """Test ACP defender with custom strength (non-default)."""
        config = SimulationConfig(
            num_nodes=20,
            acp_strength=0.8,  # non-default (default is 0.65)
            vulnerability_distribution="bimodal",  # non-uniform
            random_seed=42,
        )

        # Use ACP defender with custom params
        result = run_single_episode(0, True, config)

        assert result["use_acp"] is True
        assert isinstance(result["total_reward"], (int, float))


class TestRunExperimentVerbose:
    """Test run_experiment with verbose output."""

    def test_run_experiment_verbose_output(self):
        """Test that verbose mode prints output (lines 182-188, 196, 211-212)."""
        config = SimulationConfig(num_episodes=10, num_nodes=15, random_seed=42)

        # Capture stdout
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            acp_rewards, traditional_rewards, analysis = run_experiment(config, verbose=True)

            output = fake_out.getvalue()

            # Check that verbose output was printed
            assert "ACP EXPERIMENT" in output
            assert "Episodes:" in output
            assert "Configuration:" in output
            assert "Episode 0/" in output or "Completed" in output

        assert len(acp_rewards) == 5
        assert len(traditional_rewards) == 5

    def test_run_experiment_verbose_progress_reporting(self):
        """Test that verbose mode reports progress every 50 episodes (line 196)."""
        config = SimulationConfig(num_episodes=100, num_nodes=15, random_seed=42)

        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            run_experiment(config, verbose=True)

            output = fake_out.getvalue()

            # Check progress reporting at episode 0 and 50
            assert "Episode 0/100" in output or "Episode 50/100" in output

    def test_run_experiment_completion_message(self):
        """Test that verbose mode prints completion message (lines 211-212)."""
        config = SimulationConfig(num_episodes=10, num_nodes=15, random_seed=42)

        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            run_experiment(config, verbose=True)

            output = fake_out.getvalue()

            # Check completion message
            assert "Completed 10 episodes" in output or "Completed" in output


class TestRunExperimentParallel:
    """Test parallel experiment execution."""

    def test_run_experiment_parallel_basic(self):
        """Test parallel experiment with default workers (lines 276-345)."""
        config = SimulationConfig(num_episodes=20, num_nodes=15, random_seed=42)

        acp_rewards, traditional_rewards, analysis = run_experiment_parallel(
            config, n_workers=2, verbose=False
        )

        # Check results
        assert len(acp_rewards) == 10
        assert len(traditional_rewards) == 10
        assert "acp_mean" in analysis
        assert "traditional_mean" in analysis
        assert "acp_episodes" in analysis
        assert "traditional_episodes" in analysis

    def test_run_experiment_parallel_with_none_workers(self):
        """Test parallel experiment with n_workers=None (line 277)."""
        config = SimulationConfig(num_episodes=10, num_nodes=15, random_seed=42)

        # n_workers=None should default to min(cpu_count(), 16)
        acp_rewards, traditional_rewards, analysis = run_experiment_parallel(
            config, n_workers=None, verbose=False
        )

        assert len(acp_rewards) == 5
        assert len(traditional_rewards) == 5

    def test_run_experiment_parallel_verbose_output(self):
        """Test parallel experiment with verbose output (lines 279-286, 292-300)."""
        config = SimulationConfig(num_episodes=10, num_nodes=15, random_seed=42)

        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            run_experiment_parallel(config, n_workers=2, verbose=True)

            output = fake_out.getvalue()

            # Check verbose output
            assert "PARALLEL ACP EXPERIMENT" in output or "parallel" in output.lower()
            assert "Episodes:" in output or "Completed" in output

    def test_run_experiment_parallel_action_aggregation(self):
        """Test that parallel experiment aggregates actions correctly (lines 313-322)."""
        config = SimulationConfig(num_episodes=20, num_nodes=15, random_seed=42)

        acp_rewards, traditional_rewards, analysis = run_experiment_parallel(
            config, n_workers=2, verbose=False
        )

        # Check action distributions
        assert "acp_action_distribution" in analysis
        assert "traditional_action_distribution" in analysis

        # Distributions should sum to 1
        acp_dist = analysis["acp_action_distribution"]
        trad_dist = analysis["traditional_action_distribution"]

        assert abs(sum(acp_dist.values()) - 1.0) < 0.01
        assert abs(sum(trad_dist.values()) - 1.0) < 0.01

    def test_run_experiment_parallel_confidence_aggregation(self):
        """Test that parallel experiment aggregates confidence scores (lines 324-328)."""
        config = SimulationConfig(num_episodes=20, num_nodes=15, random_seed=42)

        acp_rewards, traditional_rewards, analysis = run_experiment_parallel(
            config, n_workers=2, verbose=False
        )

        # Check confidence metrics
        assert "acp_attacker_confidence" in analysis
        assert "traditional_attacker_confidence" in analysis

        # Confidence should be between 0 and 1
        assert 0 <= analysis["acp_attacker_confidence"] <= 1
        assert 0 <= analysis["traditional_attacker_confidence"] <= 1

    def test_run_experiment_parallel_episode_details(self):
        """Test that episode details are included in analysis (lines 342-343)."""
        config = SimulationConfig(num_episodes=10, num_nodes=15, random_seed=42)

        acp_rewards, traditional_rewards, analysis = run_experiment_parallel(
            config, n_workers=2, verbose=False
        )

        # Check episode details
        assert "acp_episodes" in analysis
        assert "traditional_episodes" in analysis
        assert len(analysis["acp_episodes"]) == 5
        assert len(analysis["traditional_episodes"]) == 5

        # Check episode structure
        for episode in analysis["acp_episodes"]:
            assert "episode_id" in episode
            assert "use_acp" in episode
            assert episode["use_acp"] is True

        for episode in analysis["traditional_episodes"]:
            assert "use_acp" in episode
            assert episode["use_acp"] is False

    def test_run_experiment_parallel_single_worker(self):
        """Test parallel experiment with single worker."""
        config = SimulationConfig(num_episodes=10, num_nodes=15, random_seed=42)

        acp_rewards, traditional_rewards, analysis = run_experiment_parallel(
            config, n_workers=1, verbose=False
        )

        assert len(acp_rewards) == 5
        assert len(traditional_rewards) == 5

    def test_run_experiment_parallel_many_workers(self):
        """Test parallel experiment with many workers."""
        config = SimulationConfig(num_episodes=20, num_nodes=15, random_seed=42)

        acp_rewards, traditional_rewards, analysis = run_experiment_parallel(
            config, n_workers=4, verbose=False
        )

        assert len(acp_rewards) == 10
        assert len(traditional_rewards) == 10


class TestRunnerReproducibility:
    """Test reproducibility across serial and parallel execution."""

    def test_parallel_vs_serial_reproducibility(self):
        """Test that parallel and serial runs produce same results."""
        config = SimulationConfig(num_episodes=20, num_nodes=15, random_seed=42)

        # Run serial
        acp_serial, trad_serial, _ = run_experiment(config, verbose=False)

        # Run parallel
        acp_parallel, trad_parallel, _ = run_experiment_parallel(
            config, n_workers=2, verbose=False
        )

        # Results should be identical (same seeds)
        np.testing.assert_array_equal(acp_serial, acp_parallel)
        np.testing.assert_array_equal(trad_serial, trad_parallel)


class TestRunnerEdgeCases:
    """Test edge cases in simulation runner."""

    def test_run_experiment_minimal_episodes(self):
        """Test experiment with minimal number of episodes."""
        config = SimulationConfig(num_episodes=2, num_nodes=10, random_seed=42)

        acp_rewards, traditional_rewards, analysis = run_experiment(config, verbose=False)

        assert len(acp_rewards) == 1
        assert len(traditional_rewards) == 1

    def test_run_experiment_all_parameters_custom(self):
        """Test experiment with all custom parameters."""
        config = SimulationConfig(
            num_episodes=10,
            num_nodes=25,
            connectivity=0.8,
            acp_strength=0.9,
            learning_rate=2.0,
            decay_rate=0.95,
            noise=0.05,
            vulnerability_distribution="bimodal",
            random_seed=123,
        )

        acp_rewards, traditional_rewards, analysis = run_experiment(config, verbose=False)

        assert len(acp_rewards) == 5
        assert len(traditional_rewards) == 5
        assert "config" in analysis
        assert analysis["config"]["num_nodes"] == 25
        assert analysis["config"]["connectivity"] == 0.8

    def test_parallel_experiment_with_odd_episodes(self):
        """Test parallel experiment with odd number of episodes."""
        config = SimulationConfig(num_episodes=11, num_nodes=15, random_seed=42)

        acp_rewards, traditional_rewards, analysis = run_experiment_parallel(
            config, n_workers=2, verbose=False
        )

        # 11 episodes: 6 ACP (even indices), 5 traditional (odd indices)
        assert len(acp_rewards) == 6
        assert len(traditional_rewards) == 5
