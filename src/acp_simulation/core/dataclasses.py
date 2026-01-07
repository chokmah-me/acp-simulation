"""
Data classes for ACP simulation data structures.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Tuple

from .enums import ActionType


@dataclass(frozen=True)
class Instance:
    """
    Cognitive memory instance for Instance-Based Learning Theory (IBLT).

    Represents one past experience stored in the attacker's memory,
    including the situation, action taken, outcome, and confidence level.

    Attributes
    ----------
    situation : Tuple
        Encoded representation of the situation/context
    action : ActionType
        Action taken in this situation
    outcome : float
        Reward or outcome from the action
    timestamp : int
        Time step when this instance was created
    confidence : float
        Confidence level of this memory (degraded by ACP deception)

    Notes
    -----
    The confidence parameter is critical for ACP's memory poisoning mechanism.
    Normal learning uses confidence = 1.0, while ACP-poisoned learning
    uses confidence = 0.3-0.5 to degrade the attacker's memory.
    """

    situation: Tuple
    action: ActionType
    outcome: float
    timestamp: int
    confidence: float = 1.0


@dataclass(frozen=True)
class SimulationConfig:
    """
    Configuration for ACP simulation experiments.

    This immutable configuration class ensures reproducibility and
    provides a single source of truth for all simulation parameters.

    Attributes
    ----------
    num_episodes : int
        Total number of episodes to run (default: 1000)
    num_nodes : int
        Number of nodes in the network (default: 50)
    connectivity : float
        Network connectivity between 0.0 and 1.0 (default: 0.6)
    acp_strength : float
        ACP deception probability between 0.0 and 1.0 (default: 0.65)
    learning_rate : float
        Attacker learning rate multiplier (default: 1.0)
    decay_rate : float
        Memory decay rate for IBLT (default: 0.8)
    noise : float
        Decision noise level (default: 0.1)
    confidence_level : float
        Statistical confidence level: 0.90, 0.95, or 0.99 (default: 0.95)
    bootstrap_samples : int
        Number of bootstrap samples for CI calculation (default: 10000)
    vulnerability_distribution : str
        Vulnerability distribution type: 'uniform', 'normal',
        'exponential', or 'bimodal' (default: 'uniform')
    random_seed : int
        Master random seed for reproducibility (default: 42)
    n_cores : int, optional
        Number of CPU cores for parallel processing. If None,
        uses min(cpu_count(), 16) (default: None)
    max_steps_per_episode : int
        Maximum steps per episode (default: 60)

    Examples
    --------
    >>> # Default configuration
    >>> config = SimulationConfig()
    >>>
    >>> # Custom configuration
    >>> config = SimulationConfig(
    ...     num_episodes=5000,
    ...     acp_strength=0.8,
    ...     num_nodes=100
    ... )
    >>>
    >>> # Save configuration
    >>> config.save(Path('configs/experiment.json'))
    >>>
    >>> # Load configuration
    >>> loaded_config = SimulationConfig.load(Path('configs/experiment.json'))
    """

    num_episodes: int = 1000
    num_nodes: int = 50
    connectivity: float = 0.6
    acp_strength: float = 0.65
    learning_rate: float = 1.0
    decay_rate: float = 0.8
    noise: float = 0.1
    confidence_level: float = 0.95
    bootstrap_samples: int = 10000
    vulnerability_distribution: str = "uniform"
    random_seed: int = 42
    n_cores: int = None
    max_steps_per_episode: int = 60

    def __post_init__(self):
        """Validate configuration parameters after initialization."""
        # Validate ranges
        if not 0.0 <= self.acp_strength <= 1.0:
            raise ValueError("acp_strength must be between 0.0 and 1.0")
        if not 0.0 <= self.connectivity <= 1.0:
            raise ValueError("connectivity must be between 0.0 and 1.0")
        if self.confidence_level not in [0.90, 0.95, 0.99]:
            raise ValueError("confidence_level must be 0.90, 0.95, or 0.99")
        if self.num_nodes < 10:
            raise ValueError("num_nodes must be at least 10")
        if self.num_episodes < 1:
            raise ValueError("num_episodes must be at least 1")
        if self.bootstrap_samples < 100:
            raise ValueError("bootstrap_samples must be at least 100")

    def save(self, path: str) -> None:
        """
        Save configuration to JSON file.

        Parameters
        ----------
        path : str
            Path to save the configuration file
        """
        import json
        from dataclasses import asdict
        from pathlib import Path

        # Create directory if it doesn't exist
        Path(path).parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w") as f:
            json.dump(asdict(self), f, indent=2)

    @classmethod
    def load(cls, path: str) -> "SimulationConfig":
        """
        Load configuration from JSON file.

        Parameters
        ----------
        path : str
            Path to the configuration file

        Returns
        -------
        SimulationConfig
            Loaded configuration instance
        """
        import json

        with open(path, "r") as f:
            data = json.load(f)

        return cls(**data)

    def to_dict(self) -> dict:
        """
        Convert configuration to dictionary.

        Returns
        -------
        dict
            Configuration as dictionary
        """
        from dataclasses import asdict

        return asdict(self)

    def get_episode_seed(self, episode_id: int) -> int:
        """
        Get deterministic seed for a specific episode.

        Parameters
        ----------
        episode_id : int
            Episode identifier

        Returns
        -------
        int
            Seed for this episode
        """
        return self.random_seed + episode_id
