"""
Tests for core dataclasses.
"""

import json
import os
import tempfile
from pathlib import Path

import pytest

from acp_simulation.core.dataclasses import Instance, SimulationConfig
from acp_simulation.core.enums import ActionType


class TestInstance:
    """Test Instance dataclass."""

    def test_instance_creation(self):
        """Test creating an Instance with default confidence."""
        situation = (1, 2, 3)
        action = ActionType.SCAN
        outcome = 10.5
        timestamp = 5

        instance = Instance(situation, action, outcome, timestamp)

        assert instance.situation == situation
        assert instance.action == action
        assert instance.outcome == outcome
        assert instance.timestamp == timestamp
        assert instance.confidence == 1.0  # Default value

    def test_instance_creation_with_custom_confidence(self):
        """Test creating an Instance with custom confidence."""
        situation = (1, 2, 3)
        action = ActionType.EXPLOIT
        outcome = -2.0
        timestamp = 10
        confidence = 0.5

        instance = Instance(situation, action, outcome, timestamp, confidence)

        assert instance.confidence == confidence

    def test_instance_immutability(self):
        """Test that Instance attributes cannot be modified."""
        instance = Instance((1, 2), ActionType.SCAN, 5.0, 1)

        # Attempting to modify should raise AttributeError
        with pytest.raises(AttributeError):
            instance.confidence = 0.5

    def test_instance_equality(self):
        """Test Instance equality comparison."""
        instance1 = Instance((1, 2), ActionType.SCAN, 5.0, 1)
        instance2 = Instance((1, 2), ActionType.SCAN, 5.0, 1)
        instance3 = Instance((1, 2), ActionType.SCAN, 5.0, 2)  # Different timestamp

        assert instance1 == instance2
        assert instance1 != instance3

    def test_instance_repr(self):
        """Test Instance string representation."""
        instance = Instance((1, 2), ActionType.SCAN, 5.0, 1, 0.8)
        repr_str = repr(instance)

        assert "Instance" in repr_str
        assert "SCAN" in repr_str
        assert "confidence=0.8" in repr_str


class TestSimulationConfig:
    """Test SimulationConfig dataclass."""

    def test_default_config(self):
        """Test creating config with default values."""
        config = SimulationConfig()

        assert config.num_episodes == 1000
        assert config.num_nodes == 50
        assert config.connectivity == 0.6
        assert config.acp_strength == 0.65
        assert config.learning_rate == 1.0
        assert config.decay_rate == 0.8
        assert config.noise == 0.1
        assert config.confidence_level == 0.95
        assert config.bootstrap_samples == 10000
        assert config.vulnerability_distribution == "uniform"
        assert config.random_seed == 42
        assert config.n_cores is None
        assert config.max_steps_per_episode == 60

    def test_custom_config(self):
        """Test creating config with custom values."""
        config = SimulationConfig(
            num_episodes=5000, acp_strength=0.8, num_nodes=100, random_seed=123
        )

        assert config.num_episodes == 5000
        assert config.acp_strength == 0.8
        assert config.num_nodes == 100
        assert config.random_seed == 123
        # Other values should be defaults
        assert config.connectivity == 0.6

    def test_config_immutability(self):
        """Test that SimulationConfig is immutable."""
        config = SimulationConfig()

        with pytest.raises(AttributeError):
            config.num_episodes = 2000

    def test_config_validation_acp_strength(self):
        """Test validation of acp_strength parameter."""
        # Valid values
        SimulationConfig(acp_strength=0.0)
        SimulationConfig(acp_strength=1.0)
        SimulationConfig(acp_strength=0.5)

        # Invalid values
        with pytest.raises(ValueError, match="acp_strength must be between"):
            SimulationConfig(acp_strength=-0.1)

        with pytest.raises(ValueError, match="acp_strength must be between"):
            SimulationConfig(acp_strength=1.5)

    def test_config_validation_connectivity(self):
        """Test validation of connectivity parameter."""
        # Valid values
        SimulationConfig(connectivity=0.0)
        SimulationConfig(connectivity=1.0)
        SimulationConfig(connectivity=0.5)

        # Invalid values
        with pytest.raises(ValueError, match="connectivity must be between"):
            SimulationConfig(connectivity=-0.1)

        with pytest.raises(ValueError, match="connectivity must be between"):
            SimulationConfig(connectivity=1.5)

    def test_config_validation_confidence_level(self):
        """Test validation of confidence_level parameter."""
        # Valid values
        SimulationConfig(confidence_level=0.90)
        SimulationConfig(confidence_level=0.95)
        SimulationConfig(confidence_level=0.99)

        # Invalid values
        with pytest.raises(ValueError, match="confidence_level must be"):
            SimulationConfig(confidence_level=0.85)

        with pytest.raises(ValueError, match="confidence_level must be"):
            SimulationConfig(confidence_level=0.50)

    def test_config_validation_num_nodes(self):
        """Test validation of num_nodes parameter."""
        # Valid values
        SimulationConfig(num_nodes=10)
        SimulationConfig(num_nodes=100)

        # Invalid values
        with pytest.raises(ValueError, match="num_nodes must be at least"):
            SimulationConfig(num_nodes=5)

        with pytest.raises(ValueError, match="num_nodes must be at least"):
            SimulationConfig(num_nodes=0)

    def test_config_validation_num_episodes(self):
        """Test validation of num_episodes parameter."""
        # Valid values
        SimulationConfig(num_episodes=1)
        SimulationConfig(num_episodes=100)

        # Invalid values
        with pytest.raises(ValueError, match="num_episodes must be at least"):
            SimulationConfig(num_episodes=0)

        with pytest.raises(ValueError, match="num_episodes must be at least"):
            SimulationConfig(num_episodes=-10)

    def test_config_validation_bootstrap_samples(self):
        """Test validation of bootstrap_samples parameter."""
        # Valid values
        SimulationConfig(bootstrap_samples=100)
        SimulationConfig(bootstrap_samples=10000)

        # Invalid values
        with pytest.raises(ValueError, match="bootstrap_samples must be at least"):
            SimulationConfig(bootstrap_samples=50)

        with pytest.raises(ValueError, match="bootstrap_samples must be at least"):
            SimulationConfig(bootstrap_samples=0)

    def test_config_save_and_load(self):
        """Test saving and loading configuration to/from JSON."""
        # Create a temporary file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            temp_path = f.name

        try:
            # Create and save config
            original_config = SimulationConfig(
                num_episodes=5000, acp_strength=0.8, num_nodes=100, random_seed=12345
            )
            original_config.save(temp_path)

            # Verify file exists and has content
            assert os.path.exists(temp_path)
            with open(temp_path, "r") as f:
                saved_data = json.load(f)

            # Check saved data
            assert saved_data["num_episodes"] == 5000
            assert saved_data["acp_strength"] == 0.8
            assert saved_data["random_seed"] == 12345

            # Load config
            loaded_config = SimulationConfig.load(temp_path)

            # Verify loaded config matches original
            assert loaded_config.num_episodes == original_config.num_episodes
            assert loaded_config.acp_strength == original_config.acp_strength
            assert loaded_config.num_nodes == original_config.num_nodes
            assert loaded_config.random_seed == original_config.random_seed
            assert loaded_config.connectivity == original_config.connectivity

        finally:
            # Clean up
            if os.path.exists(temp_path):
                os.unlink(temp_path)

    def test_config_save_creates_directory(self):
        """Test that save() creates parent directories if needed."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a path with non-existent subdirectory
            config_path = Path(temp_dir) / "subdir" / "config.json"

            config = SimulationConfig()
            config.save(str(config_path))

            # Verify file was created
            assert config_path.exists()

            # Verify content
            loaded_config = SimulationConfig.load(str(config_path))
            assert loaded_config.num_episodes == config.num_episodes

    def test_config_to_dict(self):
        """Test converting config to dictionary."""
        config = SimulationConfig(num_episodes=3000, acp_strength=0.75, random_seed=999)

        config_dict = config.to_dict()

        assert isinstance(config_dict, dict)
        assert config_dict["num_episodes"] == 3000
        assert config_dict["acp_strength"] == 0.75
        assert config_dict["random_seed"] == 999
        assert config_dict["num_nodes"] == 50  # Default value

    def test_config_get_episode_seed(self):
        """Test episode seed generation."""
        config = SimulationConfig(random_seed=42)

        # Test deterministic seed generation
        assert config.get_episode_seed(0) == 42
        assert config.get_episode_seed(1) == 43
        assert config.get_episode_seed(100) == 142

        # Test consistency
        assert config.get_episode_seed(5) == config.get_episode_seed(5)

    def test_config_equality(self):
        """Test config equality comparison."""
        config1 = SimulationConfig(num_episodes=2000, acp_strength=0.7)
        config2 = SimulationConfig(num_episodes=2000, acp_strength=0.7)
        config3 = SimulationConfig(num_episodes=2000, acp_strength=0.8)

        assert config1 == config2
        assert config1 != config3

    def test_config_with_all_custom_values(self):
        """Test creating config with all custom values."""
        config = SimulationConfig(
            num_episodes=5000,
            num_nodes=200,
            connectivity=0.7,
            acp_strength=0.9,
            learning_rate=2.0,
            decay_rate=0.9,
            noise=0.2,
            confidence_level=0.99,
            bootstrap_samples=50000,
            vulnerability_distribution="bimodal",
            random_seed=777,
            n_cores=8,
            max_steps_per_episode=100,
        )

        # Verify all values
        assert config.num_episodes == 5000
        assert config.num_nodes == 200
        assert config.connectivity == 0.7
        assert config.acp_strength == 0.9
        assert config.learning_rate == 2.0
        assert config.decay_rate == 0.9
        assert config.noise == 0.2
        assert config.confidence_level == 0.99
        assert config.bootstrap_samples == 50000
        assert config.vulnerability_distribution == "bimodal"
        assert config.random_seed == 777
        assert config.n_cores == 8
        assert config.max_steps_per_episode == 100
