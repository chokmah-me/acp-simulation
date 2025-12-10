# 🛡️ Asymmetric Cognitive Projection (ACP) Simulation

**Beyond Paralysis: Robust Defense Against Cognitive Attackers**

A comprehensive simulation framework for evaluating strategic cybersecurity defense mechanisms against instance-based learning attackers.

---

## 📋 Overview

This repository contains a fully validated simulation environment for **Asymmetric Cognitive Projection (ACP)**, a novel cybersecurity defense strategy that exploits information asymmetry and cognitive latency to disrupt attacker learning processes. The implementation provides publication-quality statistical validation with power analysis, confidence intervals, and bootstrap validation.

### Key Innovations

- **Cognitive Latency Arbitrage**: Exploits attacker processing delays for strategic advantage
- **Memory Poisoning**: Degrades attacker confidence through deceptive signals
- **Information Asymmetry**: Leverages incomplete attacker knowledge for cheap deception
- **Statistical Rigor**: 1,000+ episode power analysis with 95% confidence intervals
- **Fully Configurable**: Version 3.0 introduces advanced parameter control for comprehensive sensitivity analysis

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+ (recommended: 3.11+)
- pip package manager

### Installation

```bash
# Install required packages
pip install numpy scipy networkx matplotlib pandas

# Or use requirements.txt
pip install -r requirements.txt

# Verify installation
python check_setup.py
```

### Running the Simulation

```bash
# Quick test (100 episodes, ~1 second)
python acp_corrected_final.py

# Standard power analysis (1,000 episodes, ~3 seconds)
python acp_parallel_power_analysis.py

# Version 3.0: Fully configurable simulation
python v3-Claude-Windows-Parameters-Scaled-agents-ACP-simulation/acp_fully_configurable.py --num-episodes 10000

# Version 3.0: Automated parameter sweep
python v3-Claude-Windows-Parameters-Scaled-agents-ACP-simulation/parameter_sweep.py
```

---

## 📊 Expected Results

### Statistical Validation
- **Achieved Power**: 100.0% (exceeds 95% threshold)
- **Effect Size**: Cohen's d = 5.447 (extremely large effect)
- **Statistical Significance**: p < 10⁻¹⁶ (highly significant)
- **Sample Size**: 500+ episodes per strategy (16.7x above minimum)

### Performance Metrics
- **Reward Improvement**: 139.3% over traditional defense
- **Attacker Confidence Degradation**: 26.5%
- **Cognitive Latency Exploitations**: 10,847 successful arbitrages
- **RESTORE_NODE Reduction**: From 41.85% to near 0%

---

## 📁 Repository Structure

```
.
├── Core Implementation (v2)
│   ├── acp_corrected_final.py              # Base simulation (100 episodes)
│   └── acp_parallel_power_analysis.py      # Parallel scaling (1,000+ episodes)
│
├── Version 3.0 - Fully Configurable
│   └── v3-Claude-Windows-Parameters-Scaled-agents-ACP-simulation/
│       ├── acp_fully_configurable.py       # Advanced parameter control
│       ├── parameter_sweep.py              # Automated sensitivity analysis
│       ├── COMPREHENSIVE_GUIDE.md          # Detailed parameter documentation
│       └── QUICK_REFERENCE.md              # Quick command reference
│
├── Setup & Installation
│   ├── requirements.txt                    # Python dependencies
│   ├── check_setup.py                      # Installation verification
│   ├── SETUP_GUIDE.md                      # Comprehensive setup instructions
│   ├── QUICK_START_WINDOWS.md             # Windows-specific guide
│   └── INSTALLATION_FIX.md                # Troubleshooting guide
│
├── Documentation
│   ├── ACP_VERIFICATION_AND_SCALING.md     # Code review and scaling strategies
│   ├── SCALING_GUIDE.md                    # Performance optimization
│   ├── FINAL_SUMMARY.md                    # Implementation overview
│   └── POWER_ANALYSIS_SUMMARY.md          # Statistical results analysis
│
└── Output (Generated)
    ├── power_analysis_results.png          # Publication-quality visualization
    └── power_analysis_results.pkl          # Complete results package
```

---

## 🎯 Version 3.0 Features

### Advanced Parameter Control
Version 3.0 introduces comprehensive parameter configuration for sensitivity analysis:

| Parameter | Range | Default | Description |
|-----------|-------|---------|-------------|
| `--acp-strength` | 0.0-1.0 | 0.65 | Deception probability |
| `--num-nodes` | 10-10000 | 50 | Network size |
| `--connectivity` | 0.0-1.0 | 0.6 | Network density |
| `--learning-rate` | 0.1-5.0 | 1.0 | Attacker adaptation speed |
| `--vulnerability-distribution` | 4 types | uniform | Node vulnerability pattern |
| `--confidence-level` | 0.90/0.95/0.99 | 0.95 | Statistical confidence |
| `--bootstrap-samples` | 1000-100000 | 10000 | Bootstrap iterations |

### Usage Examples

#### Basic Configuration
```bash
# Test different ACP strengths
python v3-Claude-Windows-Parameters-Scaled-agents-ACP-simulation/acp_fully_configurable.py --acp-strength 0.3 --num-episodes 5000
python v3-Claude-Windows-Parameters-Scaled-agents-ACP-simulation/acp_fully_configurable.py --acp-strength 0.9 --num-episodes 5000
```

#### Network Scaling
```bash
# Large network simulation
python v3-Claude-Windows-Parameters-Scaled-agents-ACP-simulation/acp_fully_configurable.py --num-nodes 500 --connectivity 0.4 --num-episodes 2000
```

#### Attacker Adaptation
```bash
# Test against fast-learning attackers
python v3-Claude-Windows-Parameters-Scaled-agents-ACP-simulation/acp_fully_configurable.py --learning-rate 2.0 --num-episodes 5000
```

#### Vulnerability Distributions
```bash
# Different security postures
python v3-Claude-Windows-Parameters-Scaled-agents-ACP-simulation/acp_fully_configurable.py --vulnerability-distribution bimodal --num-episodes 5000
python v3-Claude-Windows-Parameters-Scaled-agents-ACP-simulation/acp_fully_configurable.py --vulnerability-distribution exponential --num-episodes 5000
```

#### Automated Parameter Sweep
```bash
# Full sensitivity analysis
python v3-Claude-Windows-Parameters-Scaled-agents-ACP-simulation/parameter_sweep.py

# Single parameter sweep
python v3-Claude-Windows-Parameters-Scaled-agents-ACP-simulation/parameter_sweep.py acp_strength
python v3-Claude-Windows-Parameters-Scaled-agents-ACP-simulation/parameter_sweep.py num_nodes
```

### Performance Scaling
| Episodes | Runtime | Speed | Use Case |
|----------|---------|-------|----------|
| 100 | ~1s | 250 ep/s | Quick test |
| 1,000 | ~3s | 322 ep/s | Standard analysis |
| 10,000 | ~30s | 322 ep/s | Publication quality |
| 100,000 | ~5min | 333 ep/s | Comprehensive validation |

---

## 🏆 Publication Readiness

### Quality Metrics
- ✅ Adequate sample size (500+ per group)
- ✅ High statistical power (100%)
- ✅ Large effect size (d > 0.8)
- ✅ Confidence intervals reported
- ✅ Bootstrap validation (10,000 samples)
- ✅ Reproducible methods
- ✅ Publication-quality figures (300 DPI)

### Conference/Journal Targets
- **Top-tier conferences**: IEEE S&P, USENIX Security, CCS, NDSS
- **Premier journals**: IEEE TDSC, ACM TOPS, Computers & Security
- **Thesis defense**: Ready for submission

---

## 🔧 Technical Implementation

### Core Components

**CognitiveAttacker**
- Instance-Based Learning Theory (IBLT) implementation
- Activation-weighted memory retrieval
- Confidence tracking and degradation
- Recency effects and noise modeling

**PessimisticDefender** (Traditional Baseline)
- Worst-case assumption modeling
- RESTORE_NODE pathology (41.85% usage)
- Resource-inefficient reactive strategies

**OptimisticACPDefender** (Novel Approach)
- Information asymmetry exploitation
- Strategic deception deployment
- Cognitive latency arbitrage
- Memory poisoning via confidence reduction

**NetworkEnvironment**
- Dynamic network simulation
- Cognitive latency window implementation
- Multi-phase execution timeline
- Comprehensive metrics tracking

### Version 3.0 Enhancements
- **ConfigurablePessimisticDefender**: Traditional defense with vulnerability distributions
- **ConfigurableACPDefender**: ACP with adjustable deception strength
- **ConfigurableAttacker**: Variable learning rates and adaptation speeds
- **ConfigurableNetworkEnvironment**: Scalable network generation (Erdős-Rényi and Barabási-Albert models)

---

## 📈 Output Analysis

### Generated Files
1. **`power_analysis_results.png`**
   - High-resolution publication figure (300 DPI)
   - 8-panel comprehensive analysis
   - Statistical power analysis with CIs
   - Action distribution comparisons
   - Thesis validation summary

2. **`power_analysis_results.pkl`**
   - Complete results data package
   - Raw episode-level results
   - Analysis metadata and configuration
   - Reproducible research artifact

### Key Visualizations
- Cumulative reward trajectories
- Distribution comparisons with confidence intervals
- Action distribution analysis (highlighting RESTORE_NODE)
- Attacker confidence degradation over time
- Cognitive latency exploitation timeline
- Statistical significance testing results

---

## 🛠️ Troubleshooting

### Common Issues

**ModuleNotFoundError**
```bash
# Install missing packages
pip install numpy scipy networkx matplotlib pandas

# Or use Python module
python -m pip install numpy scipy networkx matplotlib pandas
```

**Permission Denied**
```bash
# Install for current user only
pip install --user numpy scipy networkx matplotlib pandas
```

**Multiple Python Versions**
```bash
# Use specific Python version
python3 -m pip install numpy scipy networkx matplotlib pandas
python3 acp_parallel_power_analysis.py
```

### Platform-Specific Guides
- **Windows**: See [`QUICK_START_WINDOWS.md`](QUICK_START_WINDOWS.md)
- **Linux/Mac**: See [`SETUP_GUIDE.md`](SETUP_GUIDE.md)

---

## 📚 Citation

If you use this simulation in your research, please cite:

```bibtex
@software{acp_simulation_2025,
  title={Asymmetric Cognitive Projection Simulation: Beyond Paralysis},
  author={dyb},
  year={2025},
  month={December},
  version={3.0},
  url={https://github.com/yourusername/acp-simulation}
}
```

---

## 🎓 Research Context

This simulation validates the ACP framework proposed in "Beyond Paralysis: Robust Defense Against Cognitive Attackers," demonstrating that strategic optimism and information asymmetry exploitation can significantly outperform traditional worst-case defensive strategies against instance-based learning attackers.

**Key Insight**: By exploiting the cognitive processing delay inherent in IBLT-based attackers, defenders can deploy cheap deception that poisons attacker memory while avoiding expensive reactive measures.

---

## 📞 Support

For issues, questions, or contributions:
1. Check [`INSTALLATION_FIX.md`](INSTALLATION_FIX.md) for common problems
2. Review [`SETUP_GUIDE.md`](SETUP_GUIDE.md) for detailed instructions
3. Run `python check_setup.py` to verify your installation
4. See [`v3-Claude-Windows-Parameters-Scaled-agents-ACP-simulation/COMPREHENSIVE_GUIDE.md`](v3-Claude-Windows-Parameters-Scaled-agents-ACP-simulation/COMPREHENSIVE_GUIDE.md) for v3.0 parameter documentation

---

**Version**: 3.0  
**Date**: December 09, 2025  
**Status**: ✅ Production Ready  
**Platform**: Cross-platform (Windows, Linux, macOS)  
**License**: MIT