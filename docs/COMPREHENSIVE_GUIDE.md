# 📚 Comprehensive Guide - Fully Configurable ACP Simulation

## Table of Contents
1. [Quick Start Examples](#quick-start-examples)
2. [All Available Parameters](#all-available-parameters)
3. [Parameter Descriptions](#parameter-descriptions)
4. [Usage Examples](#usage-examples)
5. [Sensitivity Analysis](#sensitivity-analysis)
6. [Interpreting Results](#interpreting-results)

---

## Quick Start Examples

### Example 1: Basic Run with Default Settings
```powershell
python acp_fully_configurable.py --num-episodes 1000
```

### Example 2: Test Different ACP Strengths
```powershell
# Weak ACP (30% deception)
python acp_fully_configurable.py --acp-strength 0.3 --num-episodes 5000

# Strong ACP (90% deception)
python acp_fully_configurable.py --acp-strength 0.9 --num-episodes 5000
```

### Example 3: Large Network Simulation
```powershell
# 500-node network with lower connectivity
python acp_fully_configurable.py --num-nodes 500 --connectivity 0.4 --num-episodes 2000
```

### Example 4: High Precision Analysis
```powershell
# 99% confidence intervals with 50,000 bootstrap samples
python acp_fully_configurable.py --confidence-level 0.99 --bootstrap-samples 50000 --num-episodes 5000
```

### Example 5: Fast Learner Attacker
```powershell
# Attacker learns 2x faster
python acp_fully_configurable.py --learning-rate 2.0 --num-episodes 5000
```

### Example 6: Bimodal Vulnerability Distribution
```powershell
# Network with secure and insecure nodes
python acp_fully_configurable.py --vulnerability-distribution bimodal --num-episodes 5000
```

---

## All Available Parameters

### Episode Configuration
| Parameter | Type | Default | Range | Description |
|-----------|------|---------|-------|-------------|
| `--num-episodes` | int | 1000 | 100+ | Total episodes to run |
| `--cores` | int | auto | 1-32 | CPU cores to use |

### ACP Strategy
| Parameter | Type | Default | Range | Description |
|-----------|------|---------|-------|-------------|
| `--acp-strength` | float | 0.65 | 0.0-1.0 | Probability of using deception |

### Network Configuration
| Parameter | Type | Default | Range | Description |
|-----------|------|---------|-------|-------------|
| `--num-nodes` | int | 50 | 10-10000 | Number of network nodes |
| `--connectivity` | float | 0.6 | 0.0-1.0 | Edge probability |

### Statistical Analysis
| Parameter | Type | Default | Range | Description |
|-----------|------|---------|-------|-------------|
| `--confidence-level` | float | 0.95 | 0.90/0.95/0.99 | CI confidence level |
| `--bootstrap-samples` | int | 10000 | 1000-100000 | Bootstrap iterations |

### Attacker Configuration
| Parameter | Type | Default | Range | Description |
|-----------|------|---------|-------|-------------|
| `--learning-rate` | float | 1.0 | 0.1-5.0 | Learning speed multiplier |
| `--decay-rate` | float | 0.8 | 0.1-0.99 | Memory decay rate |
| `--noise` | float | 0.1 | 0.0-1.0 | Decision noise level |

### Vulnerability Configuration
| Parameter | Type | Default | Options | Description |
|-----------|------|---------|---------|-------------|
| `--vulnerability-distribution` | str | uniform | uniform/normal/exponential/bimodal | Node vulnerability pattern |

### Output Configuration
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `--output-dir` | str | . | Output directory path |
| `--output-prefix` | str | config | Output filename prefix |
| `--save-config` | flag | False | Save configuration to JSON |

---

## Parameter Descriptions

### 🎯 ACP Strength (`--acp-strength`)

**What it controls:** How often ACP uses deception tactics vs. reactive defense

**Values:**
- `0.3` = Low deception (30% of time)
- `0.5` = Moderate deception
- `0.65` = Default (balanced)
- `0.8` = High deception
- `0.9` = Maximum deception (90% of time)

**Use cases:**
- Test if "too much" deception is counterproductive
- Find optimal deception level for different scenarios
- Compare aggressive vs. conservative strategies

**Example:**
```powershell
# Compare three levels
python acp_fully_configurable.py --acp-strength 0.3 --output-prefix "acp_low"
python acp_fully_configurable.py --acp-strength 0.65 --output-prefix "acp_med"
python acp_fully_configurable.py --acp-strength 0.9 --output-prefix "acp_high"
```

---

### 🌐 Network Size (`--num-nodes`)

**What it controls:** Number of nodes in the network

**Values:**
- `50` = Small network (default, fast)
- `100` = Medium network
- `200` = Large network
- `500` = Very large network
- `1000`+ = Enterprise-scale (slow)

**Use cases:**
- Test scalability of ACP approach
- Validate results hold for different network sizes
- Model real-world network topologies

**Performance:**
- 50 nodes: ~3ms per episode
- 100 nodes: ~8ms per episode
- 200 nodes: ~25ms per episode
- 500 nodes: ~150ms per episode
- 1000 nodes: ~600ms per episode

**Example:**
```powershell
# Small, fast test
python acp_fully_configurable.py --num-nodes 50 --num-episodes 10000

# Enterprise scale
python acp_fully_configurable.py --num-nodes 500 --num-episodes 1000
```

---

### 🔗 Network Connectivity (`--connectivity`)

**What it controls:** How densely connected the network is

**Values:**
- `0.3` = Sparse (30% of possible edges)
- `0.5` = Moderate
- `0.6` = Default (balanced)
- `0.7` = Dense

**Use cases:**
- Test in isolated vs. highly-connected environments
- Model different network architectures
- Evaluate ACP effectiveness vs. topology

**Example:**
```powershell
# Isolated networks (harder for attacker)
python acp_fully_configurable.py --connectivity 0.3

# Dense networks (easier for attacker)
python acp_fully_configurable.py --connectivity 0.7
```

---

### 📊 Confidence Level (`--confidence-level`)

**What it controls:** Width of confidence intervals

**Values:**
- `0.90` = 90% CI (narrower, less conservative)
- `0.95` = 95% CI (default, standard)
- `0.99` = 99% CI (wider, more conservative)

**Use cases:**
- Publication requirements (usually 95%)
- High-stakes decisions (use 99%)
- Exploratory analysis (90% okay)

**Example:**
```powershell
# Standard publication quality
python acp_fully_configurable.py --confidence-level 0.95

# Extra conservative for critical claims
python acp_fully_configurable.py --confidence-level 0.99
```

---

### 🔄 Bootstrap Samples (`--bootstrap-samples`)

**What it controls:** Precision of confidence intervals

**Values:**
- `1000` = Fast, less precise
- `10000` = Default (balanced)
- `50000` = Slow, very precise
- `100000` = Very slow, maximum precision

**Use cases:**
- Quick tests: 1,000 samples
- Standard analysis: 10,000 samples
- Publication: 10,000-50,000 samples
- Critical decisions: 100,000 samples

**Performance:**
- 1,000 samples: +1 second
- 10,000 samples: +5 seconds
- 50,000 samples: +25 seconds
- 100,000 samples: +50 seconds

**Example:**
```powershell
# Quick exploratory analysis
python acp_fully_configurable.py --bootstrap-samples 1000

# Publication quality
python acp_fully_configurable.py --bootstrap-samples 50000
```

---

### 🧠 Attacker Learning Rate (`--learning-rate`)

**What it controls:** How quickly attacker learns from experience

**Values:**
- `0.5` = Slow learner (half speed)
- `1.0` = Default (normal speed)
- `1.5` = Fast learner
- `2.0` = Very fast learner (double speed)
- `3.0` = Extremely fast learner

**Use cases:**
- Model different attacker sophistication levels
- Test ACP robustness against adaptive attackers
- Worst-case scenario analysis (fast learners)

**Example:**
```powershell
# Naive attacker (learns slowly)
python acp_fully_configurable.py --learning-rate 0.5

# Sophisticated attacker (learns quickly)
python acp_fully_configurable.py --learning-rate 2.0

# Is ACP still effective against fast learners?
python acp_fully_configurable.py --learning-rate 3.0 --acp-strength 0.9
```

---

### 🎲 Vulnerability Distribution (`--vulnerability-distribution`)

**What it controls:** How vulnerabilities are distributed across nodes

**Options:**

#### `uniform` (Default)
- All nodes equally vulnerable
- Baseline scenario
- Good for controlled experiments

#### `normal`
- Most nodes have medium vulnerability
- Bell curve distribution
- Realistic for well-maintained networks

#### `exponential`
- Few highly vulnerable nodes
- Most nodes relatively secure
- Models patching programs

#### `bimodal`
- Two groups: secure (10-30%) and vulnerable (70-90%)
- Models mixed environments (old + new systems)
- Realistic for enterprise networks

**Use cases:**
- Test ACP effectiveness across different environments
- Model realistic network security postures
- Understand impact of patch management

**Example:**
```powershell
# Homogeneous environment
python acp_fully_configurable.py --vulnerability-distribution uniform

# Enterprise with legacy systems
python acp_fully_configurable.py --vulnerability-distribution bimodal

# Well-patched network
python acp_fully_configurable.py --vulnerability-distribution exponential
```

---

## Usage Examples

### Scenario 1: Thesis Validation (Current Setup)
```powershell
# Your current successful run
python acp_fully_configurable.py \
  --num-episodes 10000 \
  --num-nodes 50 \
  --acp-strength 0.65 \
  --connectivity 0.6 \
  --confidence-level 0.95 \
  --bootstrap-samples 10000
```

**Expected result:**
- 141% improvement
- Cohen's d ≈ 6.1
- Power = 100%
- Runtime: ~90 seconds

---

### Scenario 2: Testing ACP Robustness Against Smart Attackers
```powershell
# Does ACP work against attackers that learn quickly?
python acp_fully_configurable.py \
  --learning-rate 2.0 \
  --acp-strength 0.65 \
  --num-episodes 5000 \
  --output-prefix "smart_attacker"
```

**Research question:** Is ACP still effective when attackers adapt faster?

---

### Scenario 3: Enterprise-Scale Validation
```powershell
# Large network with realistic vulnerability distribution
python acp_fully_configurable.py \
  --num-nodes 500 \
  --connectivity 0.4 \
  --vulnerability-distribution bimodal \
  --num-episodes 1000 \
  --output-prefix "enterprise"
```

**Research question:** Does ACP scale to enterprise networks?

---

### Scenario 4: Optimal ACP Strength Analysis
```powershell
# Find the "sweet spot" for deception
python acp_fully_configurable.py --acp-strength 0.3 --output-prefix "acp_30"
python acp_fully_configurable.py --acp-strength 0.5 --output-prefix "acp_50"
python acp_fully_configurable.py --acp-strength 0.7 --output-prefix "acp_70"
python acp_fully_configurable.py --acp-strength 0.9 --output-prefix "acp_90"

# Then compare results
python explain_results.py acp_30_results.pkl
python explain_results.py acp_50_results.pkl
python explain_results.py acp_70_results.pkl
python explain_results.py acp_90_results.pkl
```

**Research question:** What's the optimal deception frequency?

---

### Scenario 5: Publication-Quality Sensitivity Analysis
```powershell
# High precision across multiple parameters
python acp_fully_configurable.py \
  --num-episodes 5000 \
  --confidence-level 0.99 \
  --bootstrap-samples 50000 \
  --save-config \
  --output-prefix "publication_baseline"

# Then vary one parameter at a time...
# (See Sensitivity Analysis section)
```

---

## Sensitivity Analysis

### Manual Sensitivity Analysis

Test one parameter while keeping others constant:

```powershell
# 1. Vary ACP Strength (keep rest default)
python acp_fully_configurable.py --acp-strength 0.3 --output-prefix "sens_acp_30"
python acp_fully_configurable.py --acp-strength 0.5 --output-prefix "sens_acp_50"
python acp_fully_configurable.py --acp-strength 0.7 --output-prefix "sens_acp_70"
python acp_fully_configurable.py --acp-strength 0.9 --output-prefix "sens_acp_90"

# 2. Vary Network Size (keep rest default)
python acp_fully_configurable.py --num-nodes 50 --output-prefix "sens_nodes_50"
python acp_fully_configurable.py --num-nodes 100 --output-prefix "sens_nodes_100"
python acp_fully_configurable.py --num-nodes 200 --output-prefix "sens_nodes_200"

# 3. Vary Connectivity (keep rest default)
python acp_fully_configurable.py --connectivity 0.3 --output-prefix "sens_conn_30"
python acp_fully_configurable.py --connectivity 0.5 --output-prefix "sens_conn_50"
python acp_fully_configurable.py --connectivity 0.7 --output-prefix "sens_conn_70"
```

### Automated Sensitivity Analysis

Use the parameter sweep script:

```powershell
# Full sensitivity analysis (all parameters)
python parameter_sweep.py

# Single parameter sweep
python parameter_sweep.py acp_strength
python parameter_sweep.py num_nodes
python parameter_sweep.py connectivity
python parameter_sweep.py learning_rate
```

This automatically:
1. Runs multiple configurations
2. Generates comparison visualizations
3. Creates summary statistics
4. Identifies parameter sensitivities

---

## Interpreting Results

### Understanding Output Files

After running simulation, you get:

1. **`{prefix}_results.pkl`** - Complete data package
   - Load with: `pickle.load(open('file.pkl', 'rb'))`
   - Contains: raw results, analysis, configuration

2. **Configuration JSON** (if `--save-config` used)
   - Documents exact parameters used
   - Enables perfect reproducibility

### Key Metrics to Look For

#### 1. **Percent Improvement**
- **Good:** > 100% (ACP more than doubles traditional)
- **Acceptable:** 50-100%
- **Concerning:** < 50%

#### 2. **Cohen's d (Effect Size)**
- **Small:** 0.2-0.5
- **Medium:** 0.5-0.8
- **Large:** 0.8-1.2
- **Very Large:** 1.2+ (yours is 6.1!)

#### 3. **P-value**
- **Highly Significant:** < 0.001
- **Significant:** < 0.05
- **Not Significant:** ≥ 0.05

#### 4. **Statistical Power**
- **Inadequate:** < 0.80
- **Adequate:** 0.80-0.95
- **Excellent:** > 0.95 (yours is 1.00!)

### Getting Detailed Explanations

```powershell
# Load and explain any result file
python explain_results.py {prefix}_results.pkl

# Examples:
python explain_results.py config_results.pkl
python explain_results.py enterprise_results.pkl
python explain_results.py smart_attacker_results.pkl
```

---

## Common Research Questions

### Q1: "Is ACP effective across different network sizes?"
```powershell
python acp_fully_configurable.py --num-nodes 50 --output-prefix "size_50"
python acp_fully_configurable.py --num-nodes 100 --output-prefix "size_100"
python acp_fully_configurable.py --num-nodes 200 --output-prefix "size_200"
python acp_fully_configurable.py --num-nodes 500 --output-prefix "size_500"
```

### Q2: "What's the optimal ACP strength?"
```powershell
python parameter_sweep.py acp_strength
# Automatically tests [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
```

### Q3: "Does vulnerability distribution matter?"
```powershell
python acp_fully_configurable.py --vulnerability-distribution uniform --output-prefix "vuln_uniform"
python acp_fully_configurable.py --vulnerability-distribution normal --output-prefix "vuln_normal"
python acp_fully_configurable.py --vulnerability-distribution exponential --output-prefix "vuln_exp"
python acp_fully_configurable.py --vulnerability-distribution bimodal --output-prefix "vuln_bimodal"
```

### Q4: "Is ACP robust to adaptive attackers?"
```powershell
python acp_fully_configurable.py --learning-rate 0.5 --output-prefix "slow_learner"
python acp_fully_configurable.py --learning-rate 1.0 --output-prefix "normal_learner"
python acp_fully_configurable.py --learning-rate 2.0 --output-prefix "fast_learner"
python acp_fully_configurable.py --learning-rate 3.0 --output-prefix "very_fast_learner"
```

### Q5: "How precise are my estimates?"
```powershell
# Increase bootstrap samples for tighter CIs
python acp_fully_configurable.py \
  --bootstrap-samples 50000 \
  --confidence-level 0.99 \
  --num-episodes 10000 \
  --output-prefix "high_precision"
```

---

## Tips for Publication

### For Conference Papers:
- Use 5,000-10,000 episodes per configuration
- 95% confidence intervals (standard)
- Test 3-5 parameter values per dimension
- Include sensitivity analysis for key parameters

### For Journal Papers:
- Use 10,000+ episodes per configuration
- 95% or 99% confidence intervals
- Comprehensive parameter sweeps
- Test robustness across multiple conditions

### For Thesis:
- Current 10,000 episode run is excellent
- Add 2-3 sensitivity analyses (pick most interesting)
- Show ACP works across conditions
- Include at least one "worst case" scenario

---

## Performance Optimization

### For Speed:
```powershell
# Use fewer episodes for initial tests
--num-episodes 1000

# Use fewer bootstrap samples
--bootstrap-samples 5000

# Smaller networks
--num-nodes 50

# More cores
--cores 16
```

### For Precision:
```powershell
# More episodes
--num-episodes 20000

# More bootstrap samples
--bootstrap-samples 50000

# Higher confidence level
--confidence-level 0.99
```

---

## Troubleshooting

### "Taking too long!"
- Reduce `--num-nodes` (biggest impact)
- Reduce `--num-episodes`
- Reduce `--bootstrap-samples`
- Increase `--cores`

### "Results seem noisy"
- Increase `--num-episodes`
- Increase `--bootstrap-samples`
- Check if network is too small

### "Effect size decreased"
- Check if parameter values are extreme
- May be genuine finding (ACP less effective in that regime)
- Verify with multiple runs

---

## Getting Help

```powershell
# See all options
python acp_fully_configurable.py --help

# See examples
python acp_fully_configurable.py --help | more
```

---

**Author:** dyb  
**Date:** December 09, 2025  
**Version:** 1.0.0 - Fully Configurable Edition
