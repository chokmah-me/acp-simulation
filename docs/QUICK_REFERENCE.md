# 🚀 Quick Reference Card - ACP Configurable Parameters

## One-Line Examples (Copy-Paste Ready)

```powershell
# ============================================================================
# BASIC USAGE
# ============================================================================

# Default run (1000 episodes)
python acp_fully_configurable.py

# Quick test (100 episodes)
python acp_fully_configurable.py --num-episodes 100

# Large scale (10,000 episodes)
python acp_fully_configurable.py --num-episodes 10000

# ============================================================================
# ACP STRENGTH VARIATIONS
# ============================================================================

# Low deception (30%)
python acp_fully_configurable.py --acp-strength 0.3 --output-prefix "acp_low"

# Medium deception (65% - default)
python acp_fully_configurable.py --acp-strength 0.65 --output-prefix "acp_med"

# High deception (90%)
python acp_fully_configurable.py --acp-strength 0.9 --output-prefix "acp_high"

# ============================================================================
# NETWORK SIZE VARIATIONS
# ============================================================================

# Small network (50 nodes - fast)
python acp_fully_configurable.py --num-nodes 50

# Medium network (100 nodes)
python acp_fully_configurable.py --num-nodes 100

# Large network (200 nodes)
python acp_fully_configurable.py --num-nodes 200

# Very large (500 nodes)
python acp_fully_configurable.py --num-nodes 500 --num-episodes 1000

# Enterprise scale (1000 nodes - slow!)
python acp_fully_configurable.py --num-nodes 1000 --num-episodes 500

# ============================================================================
# CONNECTIVITY VARIATIONS
# ============================================================================

# Sparse network (30% connectivity)
python acp_fully_configurable.py --connectivity 0.3

# Dense network (70% connectivity)
python acp_fully_configurable.py --connectivity 0.7

# ============================================================================
# CONFIDENCE INTERVAL OPTIONS
# ============================================================================

# 90% confidence intervals
python acp_fully_configurable.py --confidence-level 0.90

# 95% confidence intervals (default)
python acp_fully_configurable.py --confidence-level 0.95

# 99% confidence intervals (most conservative)
python acp_fully_configurable.py --confidence-level 0.99

# ============================================================================
# BOOTSTRAP PRECISION
# ============================================================================

# Fast (1,000 samples)
python acp_fully_configurable.py --bootstrap-samples 1000

# Standard (10,000 samples - default)
python acp_fully_configurable.py --bootstrap-samples 10000

# High precision (50,000 samples)
python acp_fully_configurable.py --bootstrap-samples 50000

# Maximum precision (100,000 samples - very slow!)
python acp_fully_configurable.py --bootstrap-samples 100000

# ============================================================================
# ATTACKER LEARNING RATE
# ============================================================================

# Slow learner (0.5x speed)
python acp_fully_configurable.py --learning-rate 0.5 --output-prefix "slow_attacker"

# Normal learner (1.0x speed - default)
python acp_fully_configurable.py --learning-rate 1.0

# Fast learner (2.0x speed)
python acp_fully_configurable.py --learning-rate 2.0 --output-prefix "fast_attacker"

# Very fast learner (3.0x speed)
python acp_fully_configurable.py --learning-rate 3.0 --output-prefix "very_fast_attacker"

# ============================================================================
# VULNERABILITY DISTRIBUTIONS
# ============================================================================

# Uniform (all nodes equal - default)
python acp_fully_configurable.py --vulnerability-distribution uniform

# Normal (bell curve)
python acp_fully_configurable.py --vulnerability-distribution normal

# Exponential (few vulnerable nodes)
python acp_fully_configurable.py --vulnerability-distribution exponential

# Bimodal (secure + insecure groups)
python acp_fully_configurable.py --vulnerability-distribution bimodal

# ============================================================================
# COMBINED CONFIGURATIONS
# ============================================================================

# Publication quality: high precision, 99% CI
python acp_fully_configurable.py --num-episodes 10000 --confidence-level 0.99 --bootstrap-samples 50000 --save-config --output-prefix "publication"

# Enterprise scenario: large network, bimodal vulnerabilities
python acp_fully_configurable.py --num-nodes 500 --connectivity 0.4 --vulnerability-distribution bimodal --num-episodes 2000 --output-prefix "enterprise"

# Worst case: fast attacker, sparse network, low ACP
python acp_fully_configurable.py --learning-rate 2.0 --connectivity 0.3 --acp-strength 0.4 --num-episodes 5000 --output-prefix "worst_case"

# Best case: slow attacker, dense network, high ACP
python acp_fully_configurable.py --learning-rate 0.5 --connectivity 0.7 --acp-strength 0.9 --num-episodes 5000 --output-prefix "best_case"

# Robustness test: smart attacker vs strong ACP
python acp_fully_configurable.py --learning-rate 2.5 --acp-strength 0.9 --num-episodes 5000 --output-prefix "robustness"

# ============================================================================
# SENSITIVITY ANALYSIS
# ============================================================================

# Automated full sensitivity analysis
python parameter_sweep.py

# Single parameter sweep (ACP strength)
python parameter_sweep.py acp_strength

# Single parameter sweep (network size)
python parameter_sweep.py num_nodes

# Single parameter sweep (connectivity)
python parameter_sweep.py connectivity

# Single parameter sweep (learning rate)
python parameter_sweep.py learning_rate

# ============================================================================
# RESULT ANALYSIS
# ============================================================================

# Explain any result file in plain English
python explain_results.py config_results.pkl
python explain_results.py publication_results.pkl
python explain_results.py enterprise_results.pkl

# ============================================================================
# USEFUL COMBINATIONS FOR RESEARCH
# ============================================================================

# Q: What's the optimal ACP strength?
python acp_fully_configurable.py --acp-strength 0.3 --output-prefix "acp_30"
python acp_fully_configurable.py --acp-strength 0.5 --output-prefix "acp_50"
python acp_fully_configurable.py --acp-strength 0.7 --output-prefix "acp_70"
python acp_fully_configurable.py --acp-strength 0.9 --output-prefix "acp_90"

# Q: Does ACP scale to large networks?
python acp_fully_configurable.py --num-nodes 50 --output-prefix "nodes_50"
python acp_fully_configurable.py --num-nodes 100 --output-prefix "nodes_100"
python acp_fully_configurable.py --num-nodes 200 --output-prefix "nodes_200"
python acp_fully_configurable.py --num-nodes 500 --num-episodes 1000 --output-prefix "nodes_500"

# Q: Is ACP effective against smart attackers?
python acp_fully_configurable.py --learning-rate 0.5 --output-prefix "learn_slow"
python acp_fully_configurable.py --learning-rate 1.0 --output-prefix "learn_normal"
python acp_fully_configurable.py --learning-rate 2.0 --output-prefix "learn_fast"
python acp_fully_configurable.py --learning-rate 3.0 --output-prefix "learn_veryfast"

# Q: Does vulnerability distribution matter?
python acp_fully_configurable.py --vulnerability-distribution uniform --output-prefix "vuln_uniform"
python acp_fully_configurable.py --vulnerability-distribution normal --output-prefix "vuln_normal"
python acp_fully_configurable.py --vulnerability-distribution exponential --output-prefix "vuln_exp"
python acp_fully_configurable.py --vulnerability-distribution bimodal --output-prefix "vuln_bimodal"

# ============================================================================
# PERFORMANCE TUNING
# ============================================================================

# Fast iteration (for testing)
python acp_fully_configurable.py --num-episodes 500 --bootstrap-samples 5000 --num-nodes 50

# Balanced (production quality)
python acp_fully_configurable.py --num-episodes 5000 --bootstrap-samples 10000 --num-nodes 50

# High quality (publication)
python acp_fully_configurable.py --num-episodes 10000 --bootstrap-samples 50000 --num-nodes 50 --confidence-level 0.99

# Maximum quality (critical research)
python acp_fully_configurable.py --num-episodes 20000 --bootstrap-samples 100000 --num-nodes 100 --confidence-level 0.99

```

---

## Parameter Quick Reference Table

| Category | Parameter | Range | Default | Impact |
|----------|-----------|-------|---------|--------|
| **Episodes** | `--num-episodes` | 100-100000 | 1000 | Quality vs. Time |
| **Cores** | `--cores` | 1-32 | auto | Speed only |
| **ACP** | `--acp-strength` | 0.0-1.0 | 0.65 | Strategy behavior |
| **Network** | `--num-nodes` | 10-10000 | 50 | Scalability |
| **Network** | `--connectivity` | 0.0-1.0 | 0.6 | Topology |
| **Stats** | `--confidence-level` | 0.90/0.95/0.99 | 0.95 | CI width |
| **Stats** | `--bootstrap-samples` | 1000-100000 | 10000 | Precision |
| **Attacker** | `--learning-rate` | 0.1-5.0 | 1.0 | Adaptation speed |
| **Attacker** | `--decay-rate` | 0.1-0.99 | 0.8 | Memory retention |
| **Attacker** | `--noise` | 0.0-1.0 | 0.1 | Decision randomness |
| **Vuln** | `--vulnerability-distribution` | uniform/normal/exp/bimodal | uniform | Security posture |

---

## Runtime Estimates (8-core machine)

| Configuration | Episodes | Nodes | Bootstrap | Time |
|--------------|----------|-------|-----------|------|
| Quick test | 100 | 50 | 1,000 | ~5s |
| Standard | 1,000 | 50 | 10,000 | ~8s |
| **Your run** | **10,000** | **50** | **10,000** | **~90s** |
| High quality | 10,000 | 50 | 50,000 | ~120s |
| Large network | 1,000 | 500 | 10,000 | ~150s |
| Enterprise | 5,000 | 200 | 50,000 | ~600s |
| Maximum | 20,000 | 100 | 100,000 | ~1200s |

---

## Decision Guide

### "I want to..."

**...run a quick test**
```powershell
python acp_fully_configurable.py --num-episodes 100
```

**...match my successful 10K run**
```powershell
python acp_fully_configurable.py --num-episodes 10000
```

**...test if ACP works with strong deception**
```powershell
python acp_fully_configurable.py --acp-strength 0.9 --num-episodes 5000
```

**...see if ACP scales to 500 nodes**
```powershell
python acp_fully_configurable.py --num-nodes 500 --num-episodes 1000
```

**...test against smart attackers**
```powershell
python acp_fully_configurable.py --learning-rate 2.0 --num-episodes 5000
```

**...get 99% confidence intervals**
```powershell
python acp_fully_configurable.py --confidence-level 0.99 --bootstrap-samples 50000
```

**...model an enterprise network**
```powershell
python acp_fully_configurable.py --num-nodes 500 --vulnerability-distribution bimodal --connectivity 0.4
```

**...do a complete sensitivity analysis**
```powershell
python parameter_sweep.py
```

**...understand my results in plain English**
```powershell
python explain_results.py config_results.pkl
```

---

## Getting Help

```powershell
# Show all options with descriptions
python acp_fully_configurable.py --help

# Show usage examples
python acp_fully_configurable.py --help | more

# Read comprehensive guide
# See: COMPREHENSIVE_GUIDE.md
```

---

**Pro Tip:** Always use `--output-prefix` to keep track of different configurations!

```powershell
python acp_fully_configurable.py --acp-strength 0.5 --output-prefix "test_acp_50"
python acp_fully_configurable.py --acp-strength 0.9 --output-prefix "test_acp_90"

# Then compare:
python explain_results.py test_acp_50_results.pkl
python explain_results.py test_acp_90_results.pkl
```

---

**Date:** December 09, 2025  
**Version:** 1.0.0
