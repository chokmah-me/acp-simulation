# 🕸️ Insight Mesh Network: ACP Simulation State
**Network Status:** Active
**Hub Node:** Kimi K2 Thinking (Architect)
**Current Objective:** Optimize and validate Asymmetric Cognitive Projection strategies.

## 🗺️ Architectural Map
* **Core Simulation Engine:** `/src`
    * `acp_corrected_final.py` - *Stable.* (Reference implementation).
    * `acp_fully_configurable.py` - *Active.* (Main CLI entry point).
    * `acp_parallel_power_analysis.py` - *Stable.* (Statistical engine).
* **Analysis Tools:** `/src`
    * `parameter_sweep.py` - *Volatile.* (Modify for new sensitivity tests).
    * `explain_results.py` - *Stable.* (Interpretation logic).
* **Documentation:** `/docs` - *Reference.* (Source of truth for installation/usage).

## 🛡️ Operational Constraints
1.  **Statistical Rigor:** All performance claims must report **Cohen's d** and **p-values**. Do not merge code that degrades statistical power < 80%.
2.  **Reproducibility:** All simulations must rely on explicit `random_seed` injection. Global random state is forbidden.
3.  **Vectorization:** Prefer `numpy` vector operations over Python loops for agent decision logic.
4.  **Cognitive Latency:** Maintain the "Latency Arbitrage" mechanism (Defender acts during Attacker processing window).

## 📡 Insight Log
* *Observation:* Project uses a hybrid of legacy fixed scripts (`corrected_final`) and new configurable CLI (`fully_configurable`).
* *Directive:* Prefer modification of `acp_fully_configurable.py` for new features to maintain CLI support.