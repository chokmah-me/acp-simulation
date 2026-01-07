# ACP Simulation Framework

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)](tests/)

Asymmetric Cognitive Projection (ACP) simulation framework for validating strategic cybersecurity defense mechanisms against instance-based learning attackers.

**Latest**: v4.1.0 - Enterprise Topology Edition (December 2025)

## 🎯 Overview

This framework models cognitive attacker-defender dynamics on enterprise network topologies, implementing:

- **Optimistic ACP Defense**: Exploits attacker cognitive latency windows
- **Pessimistic Traditional Defense**: Zero-trust worst-case modeling
- **Cognitive Attackers**: Instance-Based Learning Theory (IBLT)
- **Enterprise Networks**: Hub-spoke, hierarchical, scale-free topologies
- **Statistical Validation**: Variance reduction, power analysis, effect sizes

### Key Research Question

> "Do optimistic models trained against realistic variance outperform pessimistic models even in worst-case scenarios?"

**Research Focus**: Validating optimistic cognitive defense models against pessimistic worst-case approaches on realistic enterprise network topologies.

## 🚀 Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/chokmah-me/acp-simulation.git
cd acp-simulation

# Install dependencies
pip install -r requirements.txt

# Install package (development mode)
pip install -e .

# Verify installation
pytest tests/ -v
```

### Basic Usage

```python
from acp_simulation.environment import EnhancedNetworkEnvironment
from acp_simulation.agents import ConfigurableACPDefender, ConfigurableAttacker
from acp_simulation.core import NodeState, ActionType

# Create enterprise network (hub-spoke topology)
env = EnhancedNetworkEnvironment(
    num_nodes=50,
    topology_type='hub_spoke',  # Corporate server-client architecture
    vulnerability_distribution='gradient',  # Realistic security posture
    random_seed=42
)

# Get topology analysis
report = env.get_topology_report()
print(f"Network: {report['hub_count']} hubs, {report['peripheral_count']} peripheral")
print(f"Clustering: {report['metrics']['clustering_coefficient']:.3f}")

# Initialize agents
attacker = ConfigurableAttacker(learning_rate=1.0)
# Note: Defender requires network parameter - use standard workflow
```

### Enterprise Network Topologies (⭐ NEW in v4.1.0)

```python
# Hub-and-Spoke (Corporate Networks)
env_corporate = EnhancedNetworkEnvironment(
    num_nodes=50,
    topology_type='hub_spoke',  # 10% hubs (servers), 90% periphery (endpoints)
    vulnerability_distribution='gradient'  # Hubs secure (0.2), periphery vulnerable (0.7)
)

# Hierarchical (Security Zones)
env_enterprise = EnhancedNetworkEnvironment(
    num_nodes=50,
    topology_type='hierarchical',  # DMZ → Internal → Endpoints
    vulnerability_distribution='gradient'  # Outer layers vulnerable
)

# Scale-Free (Barabási-Albert)
env_scalefree = EnhancedNetworkEnvironment(
    num_nodes=100,
    topology_type='barabasi_albert',
    vulnerability_distribution='uniform'
)

# Random Baseline (Erdős-Rényi)
env_random = EnhancedNetworkEnvironment(
    num_nodes=50,
    topology_type='erdos_renyi',
    connectivity=0.6
)
```

## 📊 Running Experiments

### Enhanced Statistical Analysis (⭐ NEW in v4.1.0)

```python
from acp_simulation.simulation.enhanced_runner import run_enhanced_experiment

config = {
    'num_nodes': 50,
    'topology_type': 'hub_spoke',
    'vulnerability_dist': 'gradient',
    'acp_strength': 0.7,
    'learning_rate': 1.0,
    'max_steps': 50
}

# Run with variance reduction techniques
results = run_enhanced_experiment(
    config=config,
    num_episodes=100,
    num_trials=3,  # Multiple trials for aggregation
    warmup_steps=5,  # Reduce initialization bias
    use_crn=True  # Common Random Numbers for paired comparisons
)

# Analyze conference-specific metrics
stats = results['summary']
print(f"ACP Reward: {stats['acp_mean_reward']:.1f} ± {stats['acp_std_reward']:.1f}")
print(f"Traditional Reward: {stats['trad_mean_reward']:.1f} ± {stats['trad_std_reward']:.1f}")
print(f"Cohen's d: {stats['cohens_d']:.3f} ({stats['effect_size_interpretation']})")
print(f"p-value: {stats['p_value']:.4f}")
print(f"\n🎯 Conference Validation:")
print(f"  Restore Node Rate (ACP): {stats['acp_restore_rate']*100:.2f}%")
print(f"  Restore Node Rate (Trad): {stats['trad_restore_rate']*100:.2f}%")
print(f"  Overuse Ratio (Trad/ACP): {stats['restore_rate_ratio']:.2f}x")
```

### ACTS Combinatorial Testing

```python
from acp_simulation.integration.acts.conference_parameters import CONFERENCE_ACP_PARAMETERS, get_conference_parameter_count

# Check parameter space
info = get_conference_parameter_count()
print(f"Total combinations: {info['total_combinations']:,}")
print(f"ACTS 3-way tests: ~{info['estimated_3way_tests']}")
print(f"Reduction: {info['reduction_factor']:.1f}x")

# Output:
# Total combinations: 34,560
# ACTS 3-way tests: ~200
# Reduction: 172.8x
```

## 🏗️ Architecture

### Network Topologies

| Topology | Use Case | V Characteristics | NEW |
|----------|----------|-----------------|-----|
| **Hub-Spoke** | Corporate networks | Servers (10%) highly connected, endpoints (90%) connect to servers | ⭐ |
| **Hierarchical** | Security zones | DMZ → Internal → Endpoints, defense-in-depth | ⭐ |
| **Barabási-Albert** | Scale-free | Power-law degree distribution, hubs emerge naturally | |
| **Erdős-Rényi** | Baseline/random | Uniform connectivity, no structure | |

### Vulnerability Distributions

| Distribution | Description | Works With | NEW |
|--------------|-------------|------------|-----|
| **Gradient** | Topology-aware: hubs/core secure, periphery vulnerable | Hub-spoke, Hierarchical | ⭐ |
| **Inverse** | Insider threat model: hubs/core vulnerable | Hub-spoke, Hierarchical | ⭐ |
| **Uniform** | All nodes equal (0.5) | Any topology | |
| **Normal** | Bell curve around 0.5 | Any topology | |
| **Exponential** | Skewed distribution | Any topology | |
| **Bimodal** | Mixed secure/insecure | Any topology | |

## 🧪 Testing

```bash
# Run all tests (including new topology tests)
pytest tests/ -v  # 29 total tests

# Run only new topology tests (v4.1.0)
pytest tests/test_topology_generators.py -v  # 19 tests

# Run with coverage
pytest tests/ --cov=src/acp_simulation --cov-report=html

# Verify reproducibility
python scripts/verify_reproducibility.py
```

## 📈 Performance

### Benchmarks (16-core machine, v4.1.0)

- **Single episode** (50 nodes, 50 steps): ~100-200ms
- **100 episodes** (parallel): ~2-3 seconds
- **1,000 episodes** (parallel): ~15-20 seconds
- **ACTS suite** (200 tests × 1,000 episodes): ~15-20 minutes

### Variance Reduction Impact

| Technique | Benefit |
|-----------|---------|
| Common Random Numbers (CRN) | 20-30% reduction in standard error |
| Warmup Periods (5 steps) | 10-15% more stable estimates |
| Multi-Trial Aggregation (3 trials) | 15-25% improved confidence intervals |
| **Combined** | **40-50% improved statistical power** |

## 📚 Documentation

- **[CLAUDE.md](CLAUDE.md)**: Developer guide for AI-assisted development
- **[ENHANCEMENTS_SUMMARY.md](ENHANCEMENTS_SUMMARY.md)**: Technical details of v4.1.0 features
- **[SESSION_SUMMARY_2025-12-24.md](SESSION_SUMMARY_2025-12-24.md)**: Development session notes
- **[CHANGELOG.md](CHANGELOG.md)**: Complete version history
- **[PLAYBOOK_README.md](PLAYBOOK_README.md)**: Claude Code AI playbook instructions

## 🔬 Conference Validation

### Claims to Validate

1. **Pessimistic Overreaction**: Restore node action rate 41.85% (pessimistic) vs 33.4% (optimistic)
2. **Reward Superiority**: ACP reward 790 vs Traditional -124
3. **Generalization**: ACP >990 vs Pessimistic 959 against unknown threats

### Validation Code

See [ENHANCEMENTS_SUMMARY.md](ENHANCEMENTS_SUMMARY.md) for complete validation procedures.

## 🛠️ Development

### Project Structure

```
acp-simulation/
├── src/acp_simulation/          # Main package
│   ├── core/                    # Data structures
│   ├── agents/                  # Attacker/Defender agents
│   ├── environment/             # Network simulation
│   │   ├── topology_generators.py  # ⭐ NEW: Enterprise topologies
│   │   └── network_enhanced.py     # ⭐ NEW: Enhanced environment
│   ├── simulation/              # Experiment runners
│   │   └── enhanced_runner.py      # ⭐ NEW: Variance reduction
│   ├── analysis/                # Statistical analysis
│   └── integration/             # External frameworks
│       └── acts/
│           └── conference_parameters.py   # ⭐ NEW: conference parameter space
├── tests/                       # Test suite
│   └── test_topology_generators.py  # ⭐ NEW: 19 topology tests
├── scripts/                     # Utility scripts
├── docs/                        # Documentation
└── .claude/                     # AI playbooks (optional)
```

### Code Quality Standards

Before committing:
- ✅ All tests pass: `pytest tests/ -v`
- ✅ Type checking: `mypy src/ --strict`
- ✅ Linting: `flake8 src/ --max-line-length=100`
- ✅ Reproducibility: `python scripts/verify_reproducibility.py`

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 📞 Contact

- **Repository**: https://github.com/chokmah-me/acp-simulation
- **Issues**: https://github.com/chokmah-me/acp-simulation/issues

## 🔖 Citation

```bibtex
@software{acp_simulation_2025,
  author = {dyb},
  title = {ACP Simulation Framework: Enterprise Network Topologies for Cognitive Defense Validation},
  year = {2025},
  version = {4.1.0},
  url = {https://github.com/chokmah-me/acp-simulation}
}
```

## 📝 Version History

**v4.1.0 (December 2025)** - Enterprise Topology Edition ⭐
- Enterprise network topologies (hub-spoke, hierarchical)
- Topology-aware vulnerability distributions (gradient, inverse)
- Variance reduction framework (CRN, warmup, multi-trial)
- ACTS parameter space expansion (34,560 combinations → ~200 tests)
- Enhanced statistical analysis with conference-specific metrics
- 19 new tests (100% passing)
- 2,327 lines of code added

**v4.0.0 (December 2024)** - Production Release
- Modular package structure
- Comprehensive test suite
- ACTS integration
- Statistical power analysis

See [CHANGELOG.md](CHANGELOG.md) for complete history.

---

**Status**: ✅ Production Ready | **Last Updated**: December 24, 2025
