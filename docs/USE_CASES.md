# 🎯 ACP Simulation Use Cases - Version 3.0

Comprehensive practical examples for leveraging the fully configurable ACP simulation framework in research and real-world scenarios.

---

## 📋 Table of Contents

1. [Research Use Cases](#research-use-cases)
2. [Enterprise Security Planning](#enterprise-security-planning)
3. [Academic Publication Scenarios](#academic-publication-scenarios)
4. [Thesis and Dissertation Research](#thesis-and-dissertation-research)
5. [Comparative Analysis Studies](#comparative-analysis-studies)
6. [Performance and Scalability Testing](#performance-and-scalability-testing)
7. [Quick Reference Commands](#quick-reference-commands)

---

## 🔬 Research Use Cases

### Use Case 1: Optimal ACP Strength Determination

**Scenario**: Determine the optimal deception frequency for maximum effectiveness.

**Research Question**: What is the "sweet spot" for ACP deception strength?

**Methodology**:
```bash
# Sweep ACP strength from conservative to aggressive
python v3-Claude-Windows-Parameters-Scaled-agents-ACP-simulation/acp_fully_configurable.py --acp-strength 0.3 --num-episodes 5000 --output-prefix "acp_30"
python v3-Claude-Windows-Parameters-Scaled-agents-ACP-simulation/acp_fully_configurable.py --acp-strength 0.5 --num-episodes 5000 --output-prefix "acp_50"
python v3-Claude-Windows-Parameters-Scaled-agents-ACP-simulation/acp_fully_configurable.py --acp-strength 0.7 --num-episodes 5000 --output-prefix "acp_70"
python v3-Claude-Windows-Parameters-Scaled-agents-ACP-simulation/acp_fully_configurable.py --acp-strength 0.9 --num-episodes 5000 --output-prefix "acp_90"

# Automated sweep (recommended)
python v3-Claude-Windows-Parameters-Scaled-agents-ACP-simulation/parameter_sweep.py acp_strength
```

**Expected Insights**:
- Identify if excessive deception becomes counterproductive
- Find optimal balance between deception and reactive defense
- Understand diminishing returns of increased deception

**Analysis**:
```bash
# Compare all results
python explain_results.py acp_30_results.pkl
python explain_results.py acp_50_results.pkl
python explain_results.py acp_70_results.pkl
python explain_results.py acp_90_results.pkl
```

---

### Use Case 2: Network Scaling Validation

**Scenario**: Validate ACP effectiveness across different network sizes.

**Research Question**: Does ACP scale effectively from small to enterprise networks?

**Methodology**:
```bash
# Test across network sizes (adjust episodes for larger networks)
python v3-Claude-Windows-Parameters-Scaled-agents-ACP-simulation/acp_fully_configurable.py --num-nodes 50 --num-episodes 10000 --output-prefix "network_50"
python v3-Claude-Windows-Parameters-Scaled-agents-ACP-simulation/acp_fully_configurable.py --num-nodes 100 --num-episodes 5000 --output-prefix "network_100"
python v3-Claude-Windows-Parameters-Scaled-agents-ACP-simulation/acp_fully_configurable.py --num-nodes 200 --num-episodes 2000 --output-prefix "network_200"
python v3-Claude-Windows-Parameters-Scaled-agents-ACP-simulation/acp_fully_configurable.py --num-nodes 500 --num-episodes 1000 --output-prefix "network_500"
python v3-Claude-Windows-Parameters-Scaled-agents-ACP-simulation/acp_fully_configurable.py --num-nodes 1000 --num-episodes 500 --output-prefix "network_1000"

# Automated sweep
python v3-Claude-Windows-Parameters-Scaled-agents-ACP-simulation/parameter_sweep.py num_nodes
```

**Expected Insights**:
- Performance consistency across network scales
- Computational complexity vs. network size relationship
- ACP effectiveness in sparse vs. dense networks

---

### Use Case 3: Adaptive Attacker Analysis

**Scenario**: Test ACP robustness against attackers with different learning capabilities.

**Research Question**: Is ACP effective against sophisticated, fast-learning attackers?

**Methodology**:
```bash
# Test against various attacker learning speeds
python v3-Claude-Windows-Parameters-Scaled-agents-ACP-simulation/acp_fully_configurable.py --learning-rate 0.5 --num-episodes 5000 --output-prefix "slow_learner"
python v3-Claude-Windows-Parameters-Scaled-agents-ACP-simulation/acp_fully_configurable.py --learning-rate 1.0 --num-episodes 5000 --output-prefix "normal_learner"
python v3-Claude-Windows-Parameters-Scaled-agents-ACP-simulation/acp_fully_configurable.py --learning-rate 2.0 --num-episodes 5000 --output-prefix "fast_learner"
python v3-Claude-Windows-Parameters-Scaled-agents-ACP-simulation/acp_fully_configurable.py --learning-rate 3.0 --num-episodes 5000 --output-prefix "very_fast_learner"

# Test if stronger ACP compensates for faster attackers
python v3-Claude-Windows-Parameters-Scaled-agents-ACP-simulation/acp_fully_configurable.py --learning-rate 2.0 --acp-strength 0.9 --num-episodes 5000 --output-prefix "fast_vs_strong_acp"

# Automated sweep
python v3-Claude-Windows-Parameters-Scaled-agents-ACP-simulation/parameter_sweep.py learning_rate
```

**Expected Insights**:
- ACP effectiveness degradation with faster learners
- Compensation strategies for sophisticated attackers
- Learning rate thresholds where ACP remains effective

---

### Use Case 4: Vulnerability Distribution Impact

**Scenario**: Assess ACP performance across different network security postures.

**Research Question**: How does network vulnerability distribution affect ACP effectiveness?

**Methodology**:
```bash
# Test different vulnerability distributions
python v3-Claude-Windows-Parameters-Scaled-agents-ACP-simulation/acp_fully_configurable.py --vulnerability-distribution uniform --num-episodes 5000 --output-prefix "vuln_uniform"
python v3-Claude-Windows-Parameters-Scaled-agents-ACP-simulation/acp_fully_configurable.py --vulnerability-distribution normal --num-episodes 5000 --output-prefix "vuln_normal"
python v3-Claude-Windows-Parameters-Scaled-agents-ACP-simulation/acp_fully_configurable.py --vulnerability-distribution exponential --num-episodes 5000 --output-prefix "vuln_exponential"
python v3-Claude-Windows-Parameters-Scaled-agents-ACP-simulation/acp_fully_configurable.py --vulnerability-distribution bimodal --num-episodes 5000 --output-prefix "vuln_bimodal"

# Combine with network size for enterprise scenarios
python v3-Claude-Windows-Parameters-Scaled-agents-ACP-simulation/acp_fully_configurable.py --num-nodes 500 --vulnerability-distribution bimodal --connectivity 0.4 --num-episodes 2000 --output-prefix "enterprise_bimodal"
```

**Distribution Characteristics**:
- **Uniform**: All nodes equally vulnerable (controlled baseline)
- **Normal**: Most nodes moderately vulnerable (well-maintained networks)
- **Exponential**: Few highly vulnerable nodes (patched environments)
- **Bimodal**: Two distinct groups (enterprise with legacy systems)

**Expected Insights**:
- ACP effectiveness in heterogeneous environments
- Impact of security posture on optimal ACP configuration
- Enterprise network modeling accuracy

---

### Use Case 5: Comprehensive Sensitivity Analysis

**Scenario**: Systematically explore all parameter interactions.

**Research Question**: How do multiple parameters interact and which are most influential?

**Methodology**:
```bash
# Full automated sensitivity analysis
python v3-Claude-Windows-Parameters-Scaled-agents-ACP-simulation/parameter_sweep.py

# This automatically tests:
# - ACP strength: [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
# - Network size: [50, 100, 200]
# - Connectivity: [0.3, 0.5, 0.7]
# - Learning rate: [0.5, 1.0, 1.5, 2.0]
# - Vulnerability distributions: [uniform, normal, exponential, bimodal]

# Generates: sweep_{parameter}_visualization.png for each parameter
# Creates: sweep_{parameter}_summary.pkl with all results
```

**Expected Insights**:
- Parameter sensitivity rankings
- Interaction effects between parameters
- Robustness zones where ACP performs consistently well

---

## 🏢 Enterprise Security Planning

### Use Case 6: Enterprise Network Simulation

**Scenario**: Model a realistic enterprise environment with mixed legacy and modern systems.

**Enterprise Characteristics**:
- 500+ nodes
- Bimodal vulnerability distribution (secure + insecure groups)
- Moderate connectivity (0.4)
- Sophisticated attackers (learning rate 1.5-2.0)

**Methodology**:
```bash
# Enterprise baseline simulation
python v3-Claude-Windows-Parameters-Scaled-agents-ACP-simulation/acp_fully_configurable.py \
  --num-nodes 500 \
  --connectivity 0.4 \
  --vulnerability-distribution bimodal \
  --learning-rate 1.5 \
  --acp-strength 0.65 \
  --num-episodes 2000 \
  --confidence-level 0.95 \
  --bootstrap-samples 10000 \
  --output-prefix "enterprise_baseline" \
  --save-config

# Test stronger ACP for high-risk environments
python v3-Claude-Windows-Parameters-Scaled-agents-ACP-simulation/acp_fully_configurable.py \
  --num-nodes 500 \
  --connectivity 0.4 \
  --vulnerability-distribution bimodal \
  --learning-rate 2.0 \
  --acp-strength 0.85 \
  --num-episodes 2000 \
  --output-prefix "enterprise_high_security"
```

**Deliverables**:
- Enterprise-specific performance metrics
- Cost-benefit analysis of ACP implementation
- Risk assessment for different attacker capabilities

---

### Use Case 7: Cost-Benefit Analysis

**Scenario**: Quantify the economic benefits of ACP vs. traditional defense.

**Cost Model**:
- RESTORE_NODE: 6.0 points (expensive)
- PATCH: 1.5 points (moderate)
- ACP_DECEPTION: 1.0 points (cheap)
- MONITOR: 0.1 points (very cheap)

**Methodology**:
```bash
# Compare action distributions and costs
python v3-Claude-Windows-Parameters-Scaled-agents-ACP-simulation/acp_fully_configurable.py --num-episodes 5000 --output-prefix "cost_analysis"

# Analyze results
python explain_results.py cost_analysis_results.pkl
```

**Key Metrics**:
- Action frequency comparison (ACP vs. Traditional)
- Total cost per episode
- Cost savings from avoided RESTORE_NODE actions
- ROI of ACP implementation

---

## 🎓 Academic Publication Scenarios

### Use Case 8: Conference Paper Quality Analysis

**Scenario**: Generate results suitable for top-tier security conferences (IEEE S&P, USENIX Security, CCS).

**Conference Requirements**:
- 5,000-10,000 episodes per configuration
- 95% confidence intervals (standard)
- Multiple parameter variations
- Sensitivity analysis for key claims

**Methodology**:
```bash
# Baseline with high precision
python v3-Claude-Windows-Parameters-Scaled-agents-ACP-simulation/acp_fully_configurable.py \
  --num-episodes 10000 \
  --confidence-level 0.95 \
  --bootstrap-samples 10000 \
  --save-config \
  --output-prefix "conference_baseline"

# Sensitivity analysis (choose 2-3 most important parameters)
python v3-Claude-Windows-Parameters-Scaled-agents-ACP-simulation/acp_fully_configurable.py --acp-strength 0.5 --num-episodes 5000 --output-prefix "sens_acp_50"
python v3-Claude-Windows-Parameters-Scaled-agents-ACP-simulation/acp_fully_configurable.py --acp-strength 0.8 --num-episodes 5000 --output-prefix "sens_acp_80"

python v3-Claude-Windows-Parameters-Scaled-agents-ACP-simulation/acp_fully_configurable.py --learning-rate 1.5 --num-episodes 5000 --output-prefix "sens_learn_15"
python v3-Claude-Windows-Parameters-Scaled-agents-ACP-simulation/acp_fully_configurable.py --learning-rate 2.0 --num-episodes 5000 --output-prefix "sens_learn_20"
```

**Publication Package**:
- High-resolution figures (300 DPI)
- Complete statistical analysis
- Sensitivity analysis results
- Reproducible configuration files

---

### Use Case 9: Journal Paper Comprehensive Study

**Scenario**: Extensive analysis for journal submission (IEEE TDSC, ACM TOPS).

**Journal Requirements**:
- 10,000+ episodes per configuration
- 95% or 99% confidence intervals
- Comprehensive parameter sweeps
- Robustness testing across multiple conditions

**Methodology**:
```bash
# Maximum precision baseline
python v3-Claude-Windows-Parameters-Scaled-agents-ACP-simulation/acp_fully_configurable.py \
  --num-episodes 20000 \
  --confidence-level 0.99 \
  --bootstrap-samples 50000 \
  --save-config \
  --output-prefix "journal_baseline"

# Full parameter sweep (automated)
python v3-Claude-Windows-Parameters-Scaled-agents-ACP-simulation/parameter_sweep.py

# Additional robustness tests
python v3-Claude-Windows-Parameters-Scaled-agents-ACP-simulation/acp_fully_configurable.py --num-nodes 200 --vulnerability-distribution bimodal --num-episodes 10000 --output-prefix "robustness_1"
python v3-Claude-Windows-Parameters-Scaled-agents-ACP-simulation/acp_fully_configurable.py --connectivity 0.3 --learning-rate 2.0 --num-episodes 10000 --output-prefix "robustness_2"
```

**Expected Runtime**: Several hours for complete analysis
**Deliverables**: Comprehensive results package suitable for journal submission

---

## 🎓 Thesis and Dissertation Research

### Use Case 10: Thesis Defense-Ready Analysis

**Scenario**: Generate results for master's or PhD thesis defense.

**Thesis Requirements**:
- Current 10,000 episode run is excellent baseline
- 2-3 sensitivity analyses for comprehensive coverage
- Demonstration of ACP effectiveness across conditions
- At least one "worst case" scenario

**Methodology**:
```bash
# Primary result (already validated)
python v3-Claude-Windows-Parameters-Scaled-agents-ACP-simulation/acp_fully_configurable.py --num-episodes 10000 --output-prefix "thesis_primary"

# Sensitivity analysis 1: ACP strength
python v3-Claude-Windows-Parameters-Scaled-agents-ACP-simulation/acp_fully_configurable.py --acp-strength 0.4 --num-episodes 5000 --output-prefix "thesis_acp_sensitivity"

# Sensitivity analysis 2: Attacker learning
python v3-Claude-Windows-Parameters-Scaled-agents-ACP-simulation/acp_fully_configurable.py --learning-rate 2.0 --num-episodes 5000 --output-prefix "thesis_attacker_sensitivity"

# Worst case scenario
python v3-Claude-Windows-Parameters-Scaled-agents-ACP-simulation/acp_fully_configurable.py --connectivity 0.3 --learning-rate 2.0 --acp-strength 0.4 --num-episodes 5000 --output-prefix "thesis_worst_case"
```

**Thesis Package**:
- Primary results with high statistical power
- Sensitivity analysis showing robustness
- Worst-case scenario demonstrating boundaries
- Clear narrative of ACP effectiveness

---

## 📊 Comparative Analysis Studies

### Use Case 11: Traditional vs. ACP Head-to-Head

**Scenario**: Direct comparison focusing on action distribution differences.

**Methodology**:
```bash
# Standard comparison
python v3-Claude-Windows-Parameters-Scaled-agents-ACP-simulation/acp_fully_configurable.py --num-episodes 5000 --output-prefix "comparison"

# Analyze action distributions
python explain_results.py comparison_results.pkl
```

**Key Comparisons**:
- RESTORE_NODE usage: Traditional (41.85%) vs. ACP (near 0%)
- Cost efficiency: Total action costs per episode
- Response patterns: Reactive vs. strategic deception
- Attacker confidence degradation: 26.5% reduction with ACP

---

### Use Case 12: Multi-Parameter Interaction Study

**Scenario**: Explore how parameters interact and influence each other.

**Methodology**:
```bash
# 2x2 factorial design: ACP strength × Learning rate
python v3-Claude-Windows-Parameters-Scaled-agents-ACP-simulation/acp_fully_configurable.py --acp-strength 0.5 --learning-rate 1.0 --num-episodes 3000 --output-prefix "factorial_50_10"
python v3-Claude-Windows-Parameters-Scaled-agents-ACP-simulation/acp_fully_configurable.py --acp-strength 0.5 --learning-rate 2.0 --num-episodes 3000 --output-prefix "factorial_50_20"
python v3-Claude-Windows-Parameters-Scaled-agents-ACP-simulation/acp_fully_configurable.py --acp-strength 0.8 --learning-rate 1.0 --num-episodes 3000 --output-prefix "factorial_80_10"
python v3-Claude-Windows-Parameters-Scaled-agents-ACP-simulation/acp_fully_configurable.py --acp-strength 0.8 --learning-rate 2.0 --num-episodes 3000 --output-prefix "factorial_80_20"
```

**Analysis Focus**:
- Interaction effects between deception strength and attacker speed
- Optimal ACP configuration for different attacker types
- Synergistic or antagonistic parameter relationships

---

## ⚡ Performance and Scalability Testing

### Use Case 13: Computational Performance Benchmarking

**Scenario**: Measure simulation performance across different configurations.

**Methodology**:
```bash
# Test performance scaling
python v3-Claude-Windows-Parameters-Scaled-agents-ACP-simulation/acp_fully_configurable.py --num-episodes 100 --num-nodes 50 --output-prefix "perf_small"
python v3-Claude-Windows-Parameters-Scaled-agents-ACP-simulation/acp_fully_configurable.py --num-episodes 1000 --num-nodes 50 --output-prefix "perf_medium"
python v3-Claude-Windows-Parameters-Scaled-agents-ACP-simulation/acp_fully_configurable.py --num-episodes 10000 --num-nodes 50 --output-prefix "perf_large"

# Test network size impact
python v3-Claude-Windows-Parameters-Scaled-agents-ACP-simulation/acp_fully_configurable.py --num-nodes 100 --num-episodes 1000 --output-prefix "perf_nodes_100"
python v3-Claude-Windows-Parameters-Scaled-agents-ACP-simulation/acp_fully_configurable.py --num-nodes 200 --num-episodes 1000 --output-prefix "perf_nodes_200"
python v3-Claude-Windows-Parameters-Scaled-agents-ACP-simulation/acp_fully_configurable.py --num-nodes 500 --num-episodes 1000 --output-prefix "perf_nodes_500"
```

**Performance Metrics**:
- Episodes per second
- Memory usage
- Scaling efficiency
- Bottleneck identification

---

## 🚀 Quick Reference Commands

### Essential Commands by Goal

**Quick Testing**:
```bash
# 30-second test
python v3-Claude-Windows-Parameters-Scaled-agents-ACP-simulation/acp_fully_configurable.py --num-episodes 100

# 2-minute test
python v3-Claude-Windows-Parameters-Scaled-agents-ACP-simulation/acp_fully_configurable.py --num-episodes 1000
```

**Publication Quality**:
```bash
# Standard publication quality
python v3-Claude-Windows-Parameters-Scaled-agents-ACP-simulation/acp_fully_configurable.py --num-episodes 10000 --confidence-level 0.95 --bootstrap-samples 10000

# Maximum quality
python v3-Claude-Windows-Parameters-Scaled-agents-ACP-simulation/acp_fully_configurable.py --num-episodes 20000 --confidence-level 0.99 --bootstrap-samples 50000
```

**Sensitivity Analysis**:
```bash
# Full automated analysis
python v3-Claude-Windows-Parameters-Scaled-agents-ACP-simulation/parameter_sweep.py

# Quick single parameter
python v3-Claude-Windows-Parameters-Scaled-agents-ACP-simulation/parameter_sweep.py acp_strength
```

**Result Analysis**:
```bash
# Explain any result file
python explain_results.py your_results_file.pkl
```

---

## 📊 Decision Matrix

| Your Goal | Recommended Command | Episodes | Time | Output |
|-----------|-------------------|----------|------|--------|
| Quick test | `--num-episodes 100` | 100 | ~5s | Basic validation |
| Standard analysis | `--num-episodes 1000` | 1,000 | ~8s | Reliable results |
| **Thesis quality** | `--num-episodes 10000` | 10,000 | ~90s | **Recommended** |
| Conference paper | `--num-episodes 10000` | 10,000 | ~90s | Publication-ready |
| Journal paper | `--num-episodes 20000` | 20,000 | ~3min | Maximum precision |
| Enterprise test | `--num-nodes 500 --num-episodes 2000` | 2,000 | ~5min | Realistic scale |
| Full sensitivity | `parameter_sweep.py` | 15,000+ | ~30min | Comprehensive |

---

## 🎓 Best Practices

### For Research
1. **Always use `--save-config`** for reproducibility
2. **Use `--output-prefix`** to organize multiple runs
3. **Start with 1,000 episodes** for initial exploration
4. **Use 10,000+ episodes** for final results
5. **Run sensitivity analysis** on 2-3 key parameters

### For Enterprise
1. **Model your actual network size** with `--num-nodes`
2. **Use bimodal distribution** for mixed environments
3. **Test worst-case scenarios** with high learning rates
4. **Consider connectivity** based on your network architecture
5. **Analyze cost savings** from reduced RESTORE_NODE usage

### For Publication
1. **Use 95% confidence intervals** (standard)
2. **Include 10,000 bootstrap samples** minimum
3. **Show sensitivity analysis** for key claims
4. **Test robustness** across multiple conditions
5. **Document all parameters** for reproducibility

---

## 📞 Support and Resources

- **Comprehensive Guide**: See [`v3-Claude-Windows-Parameters-Scaled-agents-ACP-simulation/COMPREHENSIVE_GUIDE.md`](v3-Claude-Windows-Parameters-Scaled-agents-ACP-simulation/COMPREHENSIVE_GUIDE.md)
- **Quick Reference**: See [`v3-Claude-Windows-Parameters-Scaled-agents-ACP-simulation/QUICK_REFERENCE.md`](v3-Claude-Windows-Parameters-Scaled-agents-ACP-simulation/QUICK_REFERENCE.md)
- **Result Explanation**: Use `python explain_results.py your_results.pkl`
- **Installation Help**: See [`INSTALLATION_FIX.md`](INSTALLATION_FIX.md)

---

**Version**: 3.0  
**Author**: dyb  
**Date**: December 09, 2025  
**Status**: ✅ Production Ready