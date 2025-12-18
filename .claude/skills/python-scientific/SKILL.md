# Python Scientific Computing Skill

## Overview

This skill provides best practices for scientific Python development, with emphasis on NumPy/SciPy-based simulations, reproducibility, and performance optimization for research-grade code.

**Specifically optimized for:** ACP (Asymmetric Cognitive Projection) simulation and agent-based modeling

## When to Use This Skill

Use this skill when working on:
- Scientific simulations (agent-based models, network simulations, statistical analysis)
- NumPy/SciPy-based computational code
- Research code requiring reproducibility
- Performance-critical Python applications
- Code generating statistical results or figures for publication

## Core Principles

### 1. Vectorization Over Loops

**Bad:**
```python
def calculate_rewards(states: list) -> list:
    rewards = []
    for state in states:
        reward = state['value'] * state['multiplier']
        rewards.append(reward)
    return rewards
```

**Good:**
```python
def calculate_rewards(values: np.ndarray, multipliers: np.ndarray) -> np.ndarray:
    """Calculate rewards using vectorized operations.
    
    Parameters
    ----------
    values : np.ndarray
        Array of state values
    multipliers : np.ndarray
        Array of multipliers
        
    Returns
    -------
    np.ndarray
        Computed rewards
    """
    return values * multipliers
```

### 2. Explicit Random Seeds for Reproducibility

**Bad:**
```python
def run_simulation():
    noise = np.random.randn(100)
    return noise.mean()
```

**Good:**
```python
def run_simulation(seed: int = 42) -> float:
    """Run simulation with reproducible randomness.
    
    Parameters
    ----------
    seed : int, default=42
        Random seed for reproducibility
        
    Returns
    -------
    float
        Mean of noise samples
    """
    rng = np.random.default_rng(seed)
    noise = rng.standard_normal(100)
    return float(noise.mean())
```

### 3. Type Hints with numpy.typing

**Bad:**
```python
def process_data(data, threshold):
    return data[data > threshold]
```

**Good:**
```python
from typing import Union
import numpy as np
from numpy.typing import NDArray

def process_data(
    data: NDArray[np.float64],
    threshold: float
) -> NDArray[np.float64]:
    """Filter data above threshold.
    
    Parameters
    ----------
    data : NDArray[np.float64]
        Input data array
    threshold : float
        Minimum value to retain
        
    Returns
    -------
    NDArray[np.float64]
        Filtered data
    """
    return data[data > threshold]
```

### 4. Configuration Management with Dataclasses

**Bad:**
```python
def run_experiment(num_agents=100, learning_rate=0.1, epochs=1000):
    # Configuration scattered across function parameters
    pass
```

**Good:**
```python
from dataclasses import dataclass, asdict
import json
from pathlib import Path

@dataclass(frozen=True)
class SimulationConfig:
    """Configuration for ACP simulation.
    
    Attributes
    ----------
    num_agents : int
        Number of agents in simulation
    learning_rate : float
        Attacker learning rate
    num_epochs : int
        Number of simulation epochs
    random_seed : int
        Seed for reproducibility
    """
    num_agents: int = 100
    learning_rate: float = 0.1
    num_epochs: int = 1000
    random_seed: int = 42
    
    def save(self, path: Path) -> None:
        """Save configuration to JSON file."""
        with open(path, 'w') as f:
            json.dump(asdict(self), f, indent=2)
    
    @classmethod
    def load(cls, path: Path) -> 'SimulationConfig':
        """Load configuration from JSON file."""
        with open(path, 'r') as f:
            return cls(**json.load(f))

def run_experiment(config: SimulationConfig) -> dict:
    """Run experiment with given configuration."""
    # Save config for reproducibility
    config.save(Path('outputs/experiment_config.json'))
    
    # Run experiment
    rng = np.random.default_rng(config.random_seed)
    # ... simulation code ...
    
    return results
```

### 5. Parallel Processing Patterns

**Bad:**
```python
def run_episodes(n: int):
    results = []
    for i in range(n):
        result = run_single_episode(i)
        results.append(result)
    return results
```

**Good:**
```python
from multiprocessing import Pool, cpu_count
from functools import partial

def run_single_episode(episode_id: int, config: SimulationConfig) -> dict:
    """Run single episode with unique seed."""
    # Use episode_id to create unique but reproducible seed
    episode_seed = config.random_seed + episode_id
    rng = np.random.default_rng(episode_seed)
    # ... simulation code ...
    return result

def run_episodes_parallel(
    num_episodes: int,
    config: SimulationConfig,
    num_workers: int = None
) -> list[dict]:
    """Run episodes in parallel using multiprocessing.
    
    Parameters
    ----------
    num_episodes : int
        Number of episodes to run
    config : SimulationConfig
        Simulation configuration
    num_workers : int, optional
        Number of parallel workers (default: cpu_count())
        
    Returns
    -------
    list[dict]
        Results from all episodes
    """
    if num_workers is None:
        num_workers = cpu_count()
    
    run_func = partial(run_single_episode, config=config)
    
    with Pool(num_workers) as pool:
        results = pool.map(run_func, range(num_episodes))
    
    return results
```

### 6. Testing Numerical Code

**Bad:**
```python
def test_reward_calculation():
    result = calculate_reward(1.0, 2.0)
    assert result == 2.0  # Exact equality can fail due to floating point
```

**Good:**
```python
import pytest
import numpy as np
from numpy.testing import assert_allclose, assert_array_equal

def test_reward_calculation():
    """Test reward calculation with floating point tolerance."""
    result = calculate_reward(1.0, 2.0)
    expected = 2.0
    assert_allclose(result, expected, rtol=1e-7)

def test_reward_vectorized():
    """Test vectorized reward calculation."""
    values = np.array([1.0, 2.0, 3.0])
    multipliers = np.array([2.0, 3.0, 4.0])
    expected = np.array([2.0, 6.0, 12.0])
    
    result = calculate_rewards(values, multipliers)
    assert_array_equal(result, expected)

def test_reward_reproducibility():
    """Test that results are reproducible with same seed."""
    config = SimulationConfig(random_seed=42)
    result1 = run_experiment(config)
    result2 = run_experiment(config)
    
    assert_allclose(result1['rewards'], result2['rewards'])
```

### 7. Performance Profiling

**Profile before optimizing:**

```python
import cProfile
import pstats
from pstats import SortKey

def profile_simulation():
    """Profile simulation to identify bottlenecks."""
    profiler = cProfile.Profile()
    profiler.enable()
    
    # Run code to profile
    config = SimulationConfig(num_epochs=1000)
    results = run_experiment(config)
    
    profiler.disable()
    
    # Print stats
    stats = pstats.Stats(profiler)
    stats.sort_stats(SortKey.CUMULATIVE)
    stats.print_stats(20)  # Top 20 functions
    
    return results

# Or use line_profiler for line-by-line analysis:
# @profile  # Uncomment when using kernprof
def expensive_function():
    """Function to profile line-by-line."""
    # ... code ...
    pass

# Run with: kernprof -l -v script.py
```

### 8. Memory-Efficient Array Operations

**Bad:**
```python
def process_large_dataset(data: np.ndarray) -> np.ndarray:
    # Creates many intermediate arrays
    step1 = data * 2
    step2 = step1 + 5
    step3 = step2 / 3
    return step3
```

**Good:**
```python
def process_large_dataset(data: np.ndarray) -> np.ndarray:
    """Process data in-place to minimize memory usage.
    
    Parameters
    ----------
    data : np.ndarray
        Input data (will be modified in-place)
        
    Returns
    -------
    np.ndarray
        Processed data
    """
    # Single expression minimizes temporaries
    return (data * 2 + 5) / 3

def process_large_dataset_batched(
    data: np.ndarray,
    batch_size: int = 10000
) -> np.ndarray:
    """Process large dataset in batches to control memory.
    
    Parameters
    ----------
    data : np.ndarray
        Input data
    batch_size : int
        Number of elements per batch
        
    Returns
    -------
    np.ndarray
        Processed data
    """
    n = len(data)
    result = np.empty_like(data)
    
    for i in range(0, n, batch_size):
        end = min(i + batch_size, n)
        result[i:end] = (data[i:end] * 2 + 5) / 3
    
    return result
```

## NumPy-Style Docstrings

Always use NumPy-style docstrings for scientific code:

```python
def compute_statistics(
    data: NDArray[np.float64],
    confidence_level: float = 0.95
) -> dict[str, float]:
    """Compute descriptive statistics with confidence intervals.
    
    Parameters
    ----------
    data : NDArray[np.float64]
        Input data array
    confidence_level : float, default=0.95
        Confidence level for intervals (0 < confidence_level < 1)
        
    Returns
    -------
    dict[str, float]
        Dictionary containing:
        - 'mean': Sample mean
        - 'std': Sample standard deviation
        - 'ci_lower': Lower confidence bound
        - 'ci_upper': Upper confidence bound
        
    Raises
    ------
    ValueError
        If confidence_level not in (0, 1)
        
    Examples
    --------
    >>> data = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    >>> stats = compute_statistics(data)
    >>> print(f"Mean: {stats['mean']:.2f}")
    Mean: 3.00
    
    Notes
    -----
    Confidence intervals computed using t-distribution for small samples.
    
    References
    ----------
    .. [1] Student. "The probable error of a mean." Biometrika (1908).
    """
    if not 0 < confidence_level < 1:
        raise ValueError("confidence_level must be in (0, 1)")
    
    from scipy import stats as sp_stats
    
    mean = np.mean(data)
    std = np.std(data, ddof=1)
    n = len(data)
    
    # Compute confidence interval
    t_value = sp_stats.t.ppf((1 + confidence_level) / 2, n - 1)
    margin = t_value * std / np.sqrt(n)
    
    return {
        'mean': float(mean),
        'std': float(std),
        'ci_lower': float(mean - margin),
        'ci_upper': float(mean + margin)
    }
```

## Reproducibility Checklist

Every research script should include:

1. **Explicit seeds everywhere**
   ```python
   RANDOM_SEED = 42
   rng = np.random.default_rng(RANDOM_SEED)
   ```

2. **Version logging**
   ```python
   import sys
   import numpy as np
   import scipy
   
   print(f"Python: {sys.version}")
   print(f"NumPy: {np.__version__}")
   print(f"SciPy: {scipy.__version__}")
   ```

3. **Configuration saving**
   ```python
   config.save(Path('outputs/config.json'))
   ```

4. **Timestamp logging**
   ```python
   from datetime import datetime
   
   timestamp = datetime.now().isoformat()
   results['timestamp'] = timestamp
   ```

5. **Git commit hash** (if available)
   ```python
   import subprocess
   
   try:
       git_hash = subprocess.check_output(
           ['git', 'rev-parse', 'HEAD']
       ).decode('ascii').strip()
       results['git_commit'] = git_hash
   except:
       results['git_commit'] = 'unknown'
   ```

## Common Refactoring Patterns for Research Code

### Pattern 1: Extract Magic Numbers

**Before:**
```python
def update_confidence(confidence, success):
    if success:
        return min(1.0, confidence * 1.05)
    else:
        return max(0.0, confidence * 0.95)
```

**After:**
```python
CONFIDENCE_INCREASE_FACTOR = 1.05
CONFIDENCE_DECREASE_FACTOR = 0.95
MIN_CONFIDENCE = 0.0
MAX_CONFIDENCE = 1.0

def update_confidence(confidence: float, success: bool) -> float:
    """Update confidence based on outcome.
    
    Parameters
    ----------
    confidence : float
        Current confidence level [0, 1]
    success : bool
        Whether action was successful
        
    Returns
    -------
    float
        Updated confidence level [0, 1]
    """
    if success:
        return min(MAX_CONFIDENCE, confidence * CONFIDENCE_INCREASE_FACTOR)
    else:
        return max(MIN_CONFIDENCE, confidence * CONFIDENCE_DECREASE_FACTOR)
```

### Pattern 2: Vectorize Loops

**Before:**
```python
def apply_decay(values: np.ndarray, decay_rate: float) -> np.ndarray:
    result = np.zeros_like(values)
    for i in range(len(values)):
        result[i] = values[i] * (1 - decay_rate)
    return result
```

**After:**
```python
def apply_decay(values: np.ndarray, decay_rate: float) -> np.ndarray:
    """Apply exponential decay to values.
    
    Parameters
    ----------
    values : np.ndarray
        Input values
    decay_rate : float
        Decay rate in [0, 1]
        
    Returns
    -------
    np.ndarray
        Decayed values
    """
    return values * (1 - decay_rate)
```

### Pattern 3: Replace Dicts with Dataclasses

**Before:**
```python
def create_agent(agent_id, learning_rate=0.1, memory_size=100):
    return {
        'id': agent_id,
        'learning_rate': learning_rate,
        'memory_size': memory_size,
        'memory': []
    }
```

**After:**
```python
from dataclasses import dataclass, field

@dataclass
class Agent:
    """Agent with learning capabilities.
    
    Attributes
    ----------
    agent_id : int
        Unique agent identifier
    learning_rate : float
        Learning rate for updates
    memory_size : int
        Maximum memory capacity
    memory : list
        Agent memory (initialized empty)
    """
    agent_id: int
    learning_rate: float = 0.1
    memory_size: int = 100
    memory: list = field(default_factory=list)
    
    def add_to_memory(self, experience: dict) -> None:
        """Add experience to memory, removing oldest if full."""
        self.memory.append(experience)
        if len(self.memory) > self.memory_size:
            self.memory.pop(0)
```

## Integration with ACP Simulation

For the ACP simulation specifically, apply these patterns:

1. **Configuration Management**
   - Create `SimulationConfig` dataclass
   - Save config before each run
   - Load config for reproducibility

2. **Vectorization Opportunities**
   - Batch process agent decisions
   - Vectorize network operations
   - Use NumPy for state updates

3. **Reproducibility**
   - Set seed at simulation start
   - Use episode-specific seeds
   - Log all configuration

4. **Performance**
   - Profile episode execution
   - Vectorize bottlenecks
   - Use multiprocessing for independent episodes

5. **Testing**
   - Test with fixed seeds
   - Verify statistical properties
   - Test edge cases (single agent, large networks)

## Quick Reference Commands

```bash
# Profile simulation
python -m cProfile -o profile.stats script.py
python -c "import pstats; p = pstats.Stats('profile.stats'); p.sort_stats('cumulative'); p.print_stats(20)"

# Line-by-line profiling
pip install line_profiler
kernprof -l -v script.py

# Memory profiling
pip install memory_profiler
python -m memory_profiler script.py

# Run tests with coverage
pytest --cov=src --cov-report=html

# Type checking
mypy src/ --strict
```

## ACP-Specific Patterns

### Network State Vectorization

**Before:**
```python
for node in network.nodes():
    if network.nodes[node]['compromised']:
        # Process compromised node
        pass
```

**After:**
```python
# Store state as NumPy arrays
compromised_mask = network_state['compromised']  # boolean array
compromised_nodes = np.where(compromised_mask)[0]
# Process in batch
```

### Cognitive Processing with Seeds

**Before:**
```python
def cognitive_decision(state):
    return np.random.choice(['attack', 'defend'])
```

**After:**
```python
def cognitive_decision(
    state: dict,
    rng: np.random.Generator
) -> str:
    """Make cognitive decision with explicit RNG.
    
    Parameters
    ----------
    state : dict
        Current game state
    rng : np.random.Generator
        Random number generator for reproducibility
        
    Returns
    -------
    str
        Decision ('attack' or 'defend')
    """
    return rng.choice(['attack', 'defend'])
```

## Additional Resources

- NumPy User Guide: https://numpy.org/doc/stable/user/index.html
- SciPy Lecture Notes: https://scipy-lectures.org/
- Python Scientific Lecture Series: https://github.com/jrjohansson/scientific-python-lectures
- Best Practices for Scientific Computing: https://journals.plos.org/plosbiology/article?id=10.1371/journal.pbio.1001745
