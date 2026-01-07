"""
LEARNING RATE PARAMETER SWEEP ANALYSIS
Investigating how attacker learning speed affects ACP deception effectiveness

Key Research Question: How does attacker learning rate impact the effectiveness 
of ACP deception strategies in degrading attacker confidence and improving defense?

Tested learning_rate values: [0.2, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0]
- 1000 episodes per configuration
- Default parameters: acp_strength=0.65, num_nodes=50, connectivity=0.6
- Analysis focuses on: reward delta, attacker confidence degradation, action distributions

Author: dyb
Date: December 12, 2025
"""

import subprocess
import json
import pickle
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import time
from typing import List, Dict, Tuple
import pandas as pd
from scipy import stats
import sys

# Set style for publication-quality plots
plt.style.use("seaborn-v0_8-whitegrid")
sns.set_palette("husl")


class LearningRateSweep:
    """
    Specialized parameter sweep for learning_rate analysis
    """

    def __init__(self, output_dir: str = "./learning_rate_sweep"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.results = []

        # Base configuration with default parameters
        self.base_config = {
            "acp_strength": 0.65,
            "num_nodes": 50,
            "connectivity": 0.6,
            "learning_rate": 1.0,  # Will be overridden during sweep
            "decay_rate": 0.8,
            "noise": 0.1,
            "confidence_level": 0.95,
            "bootstrap_samples": 10000,
            "vulnerability_distribution": "uniform",
        }

    def run_learning_rate_sweep(
        self, learning_rates: List[float] = None, episodes_per_config: int = 1000
    ) -> List[Dict]:
        """
        Execute learning rate sweep with comprehensive analysis

        Parameters
        ----------
        learning_rates : List[float]
            Learning rate values to test
        episodes_per_config : int
            Number of episodes per configuration

        Returns
        -------
        List[Dict]
            Sweep results with detailed analysis
        """
        if learning_rates is None:
            learning_rates = [0.2, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0]

        print("\n" + "=" * 80)
        print("LEARNING RATE PARAMETER SWEEP ANALYSIS".center(80))
        print("=" * 80)
        print()
        print(f"Testing learning rates: {learning_rates}")
        print(f"Episodes per configuration: {episodes_per_config}")
        print(f"Total episodes: {len(learning_rates) * episodes_per_config}")
        print(f"Output directory: {self.output_dir}")
        print()

        sweep_results = []

        for i, lr in enumerate(learning_rates):
            print(f"[{i+1}/{len(learning_rates)}] Testing learning_rate = {lr}...")

            # Create configuration
            config = self.base_config.copy()
            config["learning_rate"] = lr
            config["num_episodes"] = episodes_per_config

            # Save configuration
            config_file = self.output_dir / f"lr_{lr:.1f}_config.json"
            with open(config_file, "w") as f:
                json.dump(config, f, indent=2)

            # Run simulation
            output_prefix = f"lr_{lr:.1f}"
            cmd = [
                "python",
                "acp_fully_configurable.py",
                f"--num-episodes={episodes_per_config}",
                f"--output-dir={self.output_dir}",
                f"--output-prefix={output_prefix}",
                f"--learning-rate={lr}",
                f'--acp-strength={config["acp_strength"]}',
                f'--num-nodes={config["num_nodes"]}',
                f'--connectivity={config["connectivity"]}',
                f'--confidence-level={config["confidence_level"]}',
                f'--bootstrap-samples={config["bootstrap_samples"]}',
                f'--vulnerability-distribution={config["vulnerability_distribution"]}',
            ]

            start_time = time.time()
            result = subprocess.run(cmd, capture_output=True, text=True)
            runtime = time.time() - start_time

            if result.returncode != 0:
                print(f"  [ERROR] Error running simulation for learning_rate={lr}")
                print(f"  Error: {result.stderr}")
                continue

            # Load results
            result_file = self.output_dir / f"{output_prefix}_results.pkl"
            with open(result_file, "rb") as f:
                data = pickle.load(f)

            analysis = data["analysis"]

            # Extract detailed metrics
            result_entry = {
                "learning_rate": lr,
                "acp_mean_reward": analysis["acp_mean"],
                "traditional_mean_reward": analysis["traditional_mean"],
                "reward_delta": analysis["delta"],
                "percent_improvement": analysis["percent_improvement"],
                "cohen_d": analysis["power_analysis"]["cohen_d"],
                "p_value": analysis["power_analysis"]["p_value"],
                "statistical_power": analysis["power_analysis"]["achieved_power"],
                "acp_attacker_confidence": analysis["acp_attacker_confidence"],
                "traditional_attacker_confidence": analysis["traditional_attacker_confidence"],
                "confidence_degradation": analysis["confidence_degradation"],
                "acp_action_distribution": analysis["acp_action_distribution"],
                "traditional_action_distribution": analysis["traditional_action_distribution"],
                "total_acp_deceptions": analysis["total_acp_deceptions"],
                "deceptions_per_episode": analysis["deceptions_per_episode"],
                "runtime": runtime,
                "config": config,
                "full_analysis": analysis,
                "raw_data": data,
            }

            sweep_results.append(result_entry)

            print(f"  [SUCCESS] Complete:")
            print(f"     Reward Δ: {analysis['delta']:.2f}")
            print(f"     Improvement: {analysis['percent_improvement']:.1f}%")
            print(f"     Confidence degradation: {analysis['confidence_degradation']:.1f}%")
            print(f"     Cohen's d: {analysis['power_analysis']['cohen_d']:.3f}")
            print(f"     Runtime: {runtime:.1f}s")
            print()

        # Save comprehensive sweep results
        sweep_file = self.output_dir / "learning_rate_sweep_summary.pkl"
        with open(sweep_file, "wb") as f:
            pickle.dump(sweep_results, f)

        # Save as CSV for easy analysis
        csv_file = self.output_dir / "learning_rate_sweep_summary.csv"
        df = pd.DataFrame(
            [
                {
                    "learning_rate": r["learning_rate"],
                    "acp_mean_reward": r["acp_mean_reward"],
                    "traditional_mean_reward": r["traditional_mean_reward"],
                    "reward_delta": r["reward_delta"],
                    "percent_improvement": r["percent_improvement"],
                    "cohen_d": r["cohen_d"],
                    "p_value": r["p_value"],
                    "statistical_power": r["statistical_power"],
                    "acp_attacker_confidence": r["acp_attacker_confidence"],
                    "traditional_attacker_confidence": r["traditional_attacker_confidence"],
                    "confidence_degradation": r["confidence_degradation"],
                    "total_acp_deceptions": r["total_acp_deceptions"],
                    "deceptions_per_episode": r["deceptions_per_episode"],
                    "runtime": r["runtime"],
                }
                for r in sweep_results
            ]
        )
        df.to_csv(csv_file, index=False)

        print(f"[SUCCESS] Sweep complete: {len(sweep_results)} configurations tested")
        print(f"   Detailed results saved to {sweep_file}")
        print(f"   Summary CSV saved to {csv_file}")

        self.results = sweep_results
        return sweep_results

    def create_comprehensive_visualizations(
        self, sweep_results: List[Dict] = None, output_prefix: str = None
    ):
        """
        Create publication-quality visualizations for learning rate analysis

        Parameters
        ----------
        sweep_results : List[Dict]
            Sweep results to visualize
        output_prefix : str
            Prefix for output files
        """
        if sweep_results is None:
            sweep_results = self.results

        if not sweep_results:
            print("No results to visualize")
            return

        if output_prefix is None:
            output_prefix = self.output_dir / "learning_rate_analysis"

        learning_rates = [r["learning_rate"] for r in sweep_results]

        # Create figure with subplots
        fig = plt.figure(figsize=(20, 16))
        gs = fig.add_gridspec(4, 3, hspace=0.3, wspace=0.3)

        # Main title
        fig.suptitle(
            "Impact of Attacker Learning Rate on ACP Effectiveness",
            fontsize=16,
            fontweight="bold",
            y=0.98,
        )

        # 1. Reward Analysis
        ax1 = fig.add_subplot(gs[0, 0])
        acp_rewards = [r["acp_mean_reward"] for r in sweep_results]
        trad_rewards = [r["traditional_mean_reward"] for r in sweep_results]

        ax1.plot(
            learning_rates,
            acp_rewards,
            "o-",
            label="ACP",
            linewidth=2.5,
            markersize=8,
            color="#2E86AB",
        )
        ax1.plot(
            learning_rates,
            trad_rewards,
            "s-",
            label="Traditional",
            linewidth=2.5,
            markersize=8,
            color="#A23B72",
        )
        ax1.set_xlabel("Learning Rate", fontsize=11, fontweight="bold")
        ax1.set_ylabel("Mean Reward", fontsize=11, fontweight="bold")
        ax1.set_title("Defense Performance vs Learning Rate", fontsize=12, fontweight="bold")
        ax1.legend(fontsize=10)
        ax1.grid(True, alpha=0.3)

        # 2. Improvement Percentage
        ax2 = fig.add_subplot(gs[0, 1])
        improvements = [r["percent_improvement"] for r in sweep_results]
        ax2.plot(learning_rates, improvements, "o-", color="#28A745", linewidth=2.5, markersize=8)
        ax2.axhline(y=100, color="gray", linestyle="--", alpha=0.5, label="No improvement")
        ax2.set_xlabel("Learning Rate", fontsize=11, fontweight="bold")
        ax2.set_ylabel("Improvement (%)", fontsize=11, fontweight="bold")
        ax2.set_title("ACP Improvement vs Learning Rate", fontsize=12, fontweight="bold")
        ax2.legend(fontsize=10)
        ax2.grid(True, alpha=0.3)

        # 3. Effect Size (Cohen's d)
        ax3 = fig.add_subplot(gs[0, 2])
        cohens_d = [r["cohen_d"] for r in sweep_results]
        ax3.plot(learning_rates, cohens_d, "o-", color="#6F42C1", linewidth=2.5, markersize=8)
        ax3.axhline(y=0.8, color="gray", linestyle="--", alpha=0.5, label="Large effect")
        ax3.axhline(y=0.5, color="gray", linestyle=":", alpha=0.5, label="Medium effect")
        ax3.set_xlabel("Learning Rate", fontsize=11, fontweight="bold")
        ax3.set_ylabel("Cohen's d", fontsize=11, fontweight="bold")
        ax3.set_title("Effect Size vs Learning Rate", fontsize=12, fontweight="bold")
        ax3.legend(fontsize=10)
        ax3.grid(True, alpha=0.3)

        # 4. Statistical Significance
        ax4 = fig.add_subplot(gs[1, 0])
        p_values = [max(r["p_value"], 1e-300) for r in sweep_results]
        ax4.semilogy(learning_rates, p_values, "o-", color="#DC3545", linewidth=2.5, markersize=8)
        ax4.axhline(y=0.05, color="gray", linestyle="--", alpha=0.5, label="α=0.05")
        ax4.axhline(y=0.001, color="gray", linestyle=":", alpha=0.5, label="α=0.001")
        ax4.set_xlabel("Learning Rate", fontsize=11, fontweight="bold")
        ax4.set_ylabel("p-value (log scale)", fontsize=11, fontweight="bold")
        ax4.set_title("Statistical Significance", fontsize=12, fontweight="bold")
        ax4.legend(fontsize=10)
        ax4.grid(True, alpha=0.3, which="both")

        # 5. Statistical Power
        ax5 = fig.add_subplot(gs[1, 1])
        powers = [r["statistical_power"] for r in sweep_results]
        ax5.plot(learning_rates, powers, "o-", color="#17A2B8", linewidth=2.5, markersize=8)
        ax5.axhline(y=0.8, color="gray", linestyle="--", alpha=0.5, label="80% power")
        ax5.axhline(y=0.95, color="gray", linestyle=":", alpha=0.5, label="95% power")
        ax5.set_xlabel("Learning Rate", fontsize=11, fontweight="bold")
        ax5.set_ylabel("Statistical Power", fontsize=11, fontweight="bold")
        ax5.set_title("Power Analysis", fontsize=12, fontweight="bold")
        ax5.set_ylim([0, 1.05])
        ax5.legend(fontsize=10)
        ax5.grid(True, alpha=0.3)

        # 6. Attacker Confidence Degradation
        ax6 = fig.add_subplot(gs[1, 2])
        conf_degrad = [r["confidence_degradation"] for r in sweep_results]
        ax6.plot(learning_rates, conf_degrad, "o-", color="#E83E8C", linewidth=2.5, markersize=8)
        ax6.axhline(y=0, color="gray", linestyle="--", alpha=0.5, label="No degradation")
        ax6.set_xlabel("Learning Rate", fontsize=11, fontweight="bold")
        ax6.set_ylabel("Confidence Degradation (%)", fontsize=11, fontweight="bold")
        ax6.set_title("Attacker Confidence Impact", fontsize=12, fontweight="bold")
        ax6.legend(fontsize=10)
        ax6.grid(True, alpha=0.3)

        # 7. Action Distribution - ACP
        ax7 = fig.add_subplot(gs[2, :2])
        self._plot_action_distribution(ax7, sweep_results, "acp", learning_rates)
        ax7.set_title("ACP Action Distribution by Learning Rate", fontsize=12, fontweight="bold")

        # 8. Action Distribution - Traditional
        ax8 = fig.add_subplot(gs[2, 2])
        self._plot_action_distribution(ax8, sweep_results, "traditional", learning_rates)
        ax8.set_title("Traditional Action Distribution", fontsize=12, fontweight="bold")

        # 9. ACP Deception Usage
        ax9 = fig.add_subplot(gs[3, 0])
        deceptions = [r["deceptions_per_episode"] for r in sweep_results]
        ax9.plot(learning_rates, deceptions, "o-", color="#FD7E14", linewidth=2.5, markersize=8)
        ax9.set_xlabel("Learning Rate", fontsize=11, fontweight="bold")
        ax9.set_ylabel("Deceptions/Episode", fontsize=11, fontweight="bold")
        ax9.set_title("ACP Deception Usage", fontsize=12, fontweight="bold")
        ax9.grid(True, alpha=0.3)

        # 10. Summary Statistics Table
        ax10 = fig.add_subplot(gs[3, 1:])
        ax10.axis("off")

        table_data = []
        for r in sweep_results:
            table_data.append(
                [
                    f"{r['learning_rate']:.1f}",
                    f"{r['reward_delta']:.2f}",
                    f"{r['percent_improvement']:.1f}%",
                    f"{r['cohen_d']:.3f}",
                    f"{r['confidence_degradation']:.1f}%",
                ]
            )

        table = ax10.table(
            cellText=table_data,
            colLabels=["LR", "Δ Reward", "Improve", "Cohen's d", "Conf. Deg."],
            cellLoc="center",
            loc="center",
            bbox=[0, 0, 1, 1],
        )
        table.auto_set_font_size(False)
        table.set_fontsize(9)
        table.scale(1, 2.5)

        for i in range(len(table_data) + 1):
            for j in range(5):
                cell = table[(i, j)]
                if i == 0:
                    cell.set_facecolor("#2C3E50")
                    cell.set_text_props(weight="bold", color="white")
                else:
                    cell.set_facecolor("#ECF0F1" if i % 2 == 0 else "white")

        ax10.set_title("Summary Statistics by Learning Rate", fontsize=12, fontweight="bold")

        plt.savefig(f"{output_prefix}_comprehensive.png", dpi=300, bbox_inches="tight")
        plt.close()

        print(f"[SUCCESS] Comprehensive visualization saved to {output_prefix}_comprehensive.png")

        # Create individual focused plots
        self._create_focused_plots(sweep_results, output_prefix)

    def _plot_action_distribution(self, ax, sweep_results, defender_type, learning_rates):
        """Plot action distribution heatmap"""
        action_types = ["MONITOR", "PATCH", "ISOLATE", "DEPLOY_HONEYPOT", "ACP_DECEPTION"]

        distribution_data = []
        for lr in learning_rates:
            result = next(r for r in sweep_results if r["learning_rate"] == lr)
            distribution = result[f"{defender_type}_action_distribution"]
            row = [distribution.get(action, 0) for action in action_types]
            distribution_data.append(row)

        im = ax.imshow(np.array(distribution_data).T, cmap="YlOrRd", aspect="auto")
        ax.set_xticks(range(len(learning_rates)))
        ax.set_xticklabels([f"{lr:.1f}" for lr in learning_rates])
        ax.set_yticks(range(len(action_types)))
        ax.set_yticklabels(action_types, fontsize=9)
        ax.set_xlabel("Learning Rate", fontsize=10, fontweight="bold")
        ax.set_ylabel("Action Type", fontsize=10, fontweight="bold")

        # Add colorbar
        cbar = plt.colorbar(im, ax=ax, shrink=0.8)
        cbar.set_label("Frequency", fontsize=9)

    def _create_focused_plots(self, sweep_results: List[Dict], output_prefix: str):
        """Create focused analysis plots"""
        learning_rates = [r["learning_rate"] for r in sweep_results]

        # Plot 1: Learning Rate vs Effectiveness Metrics
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle("Learning Rate Impact on ACP Effectiveness", fontsize=14, fontweight="bold")

        # Reward delta
        deltas = [r["reward_delta"] for r in sweep_results]
        ax1.plot(learning_rates, deltas, "o-", linewidth=2.5, markersize=8, color="#2E86AB")
        ax1.set_xlabel("Learning Rate", fontweight="bold")
        ax1.set_ylabel("Reward Delta (ACP - Traditional)", fontweight="bold")
        ax1.set_title("Reward Improvement by Learning Rate", fontweight="bold")
        ax1.grid(True, alpha=0.3)

        # Confidence degradation
        conf_deg = [r["confidence_degradation"] for r in sweep_results]
        ax2.plot(learning_rates, conf_deg, "o-", linewidth=2.5, markersize=8, color="#E83E8C")
        ax2.set_xlabel("Learning Rate", fontweight="bold")
        ax2.set_ylabel("Attacker Confidence Degradation (%)", fontweight="bold")
        ax2.set_title("Attacker Confidence Impact", fontweight="bold")
        ax2.grid(True, alpha=0.3)

        # Statistical significance
        p_vals = [r["p_value"] for r in sweep_results]
        ax3.semilogy(learning_rates, p_vals, "o-", linewidth=2.5, markersize=8, color="#DC3545")
        ax3.axhline(y=0.05, color="gray", linestyle="--", alpha=0.5, label="α=0.05")
        ax3.set_xlabel("Learning Rate", fontweight="bold")
        ax3.set_ylabel("p-value", fontweight="bold")
        ax3.set_title("Statistical Significance", fontweight="bold")
        ax3.legend()
        ax3.grid(True, alpha=0.3, which="both")

        # Effect size with interpretation
        cohens_d = [r["cohen_d"] for r in sweep_results]
        ax4.plot(learning_rates, cohens_d, "o-", linewidth=2.5, markersize=8, color="#6F42C1")
        ax4.axhline(y=0.2, color="gray", linestyle=":", alpha=0.5, label="Small")
        ax4.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5, label="Medium")
        ax4.axhline(y=0.8, color="gray", linestyle="-", alpha=0.5, label="Large")
        ax4.set_xlabel("Learning Rate", fontweight="bold")
        ax4.set_ylabel("Cohen's d", fontweight="bold")
        ax4.set_title("Effect Size Interpretation", fontweight="bold")
        ax4.legend(title="Effect Size", fontsize=9)
        ax4.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig(f"{output_prefix}_effectiveness.png", dpi=300, bbox_inches="tight")
        plt.close()

        print(f"[SUCCESS] Effectiveness analysis plot saved to {output_prefix}_effectiveness.png")

    def generate_summary_report(self, sweep_results: List[Dict] = None) -> str:
        """
        Generate comprehensive summary report

        Parameters
        ----------
        sweep_results : List[Dict]
            Sweep results to analyze

        Returns
        -------
        str
            Formatted summary report
        """
        if sweep_results is None:
            sweep_results = self.results

        if not sweep_results:
            return "No results available for report generation"

        report = []
        report.append("=" * 80)
        report.append("LEARNING RATE SWEEP ANALYSIS - SUMMARY REPORT".center(80))
        report.append("=" * 80)
        report.append("")

        # Configuration summary
        report.append("EXPERIMENT CONFIGURATION")
        report.append("-" * 40)
        base_config = sweep_results[0]["config"]
        report.append(f"• ACP Strength: {base_config['acp_strength']:.2f}")
        report.append(f"• Network Size: {base_config['num_nodes']} nodes")
        report.append(f"• Connectivity: {base_config['connectivity']:.2f}")
        report.append(f"• Episodes per configuration: {base_config['num_episodes']:,}")
        report.append(f"• Vulnerability Distribution: {base_config['vulnerability_distribution']}")
        report.append(f"• Confidence Level: {base_config['confidence_level']*100:.0f}%")
        report.append("")

        # Tested learning rates
        learning_rates = [r["learning_rate"] for r in sweep_results]
        report.append(f"Tested Learning Rates: {learning_rates}")
        report.append("")

        # Key findings
        report.append("KEY FINDINGS")
        report.append("-" * 40)

        # Best performing learning rate
        best_improvement = max(sweep_results, key=lambda x: x["percent_improvement"])
        report.append(
            f"• Best Performance: learning_rate = {best_improvement['learning_rate']:.1f}"
        )
        report.append(f"  - Reward improvement: {best_improvement['percent_improvement']:.1f}%")
        report.append(
            f"  - Attacker confidence degradation: {best_improvement['confidence_degradation']:.1f}%"
        )
        report.append(f"  - Effect size (Cohen's d): {best_improvement['cohen_d']:.3f}")
        report.append("")

        # Statistical significance
        significant_results = [r for r in sweep_results if r["p_value"] < 0.05]
        report.append(
            f"• Statistically Significant Results: {len(significant_results)}/{len(sweep_results)}"
        )
        if significant_results:
            best_sig = min(significant_results, key=lambda x: x["p_value"])
            report.append(
                f"  - Most significant: learning_rate = {best_sig['learning_rate']:.1f} (p={best_sig['p_value']:.2e})"
            )
        report.append("")

        # Effect size interpretation
        large_effects = [r for r in sweep_results if r["cohen_d"] >= 0.8]
        medium_effects = [r for r in sweep_results if 0.5 <= r["cohen_d"] < 0.8]
        report.append(f"• Effect Sizes:")
        report.append(f"  - Large effects (d ≥ 0.8): {len(large_effects)} configurations")
        report.append(f"  - Medium effects (0.5 ≤ d < 0.8): {len(medium_effects)} configurations")
        report.append("")

        # Learning rate impact analysis
        report.append("LEARNING RATE IMPACT ANALYSIS")
        report.append("-" * 40)

        # Correlation analysis
        lrs = np.array([r["learning_rate"] for r in sweep_results])
        improvements = np.array([r["percent_improvement"] for r in sweep_results])
        conf_degrad = np.array([r["confidence_degradation"] for r in sweep_results])

        corr_improvement = np.corrcoef(lrs, improvements)[0, 1]
        corr_confidence = np.corrcoef(lrs, conf_degrad)[0, 1]

        report.append(f"• Correlation with Learning Rate:")
        report.append(f"  - Improvement correlation: {corr_improvement:.3f}")
        report.append(f"  - Confidence degradation correlation: {corr_confidence:.3f}")
        report.append("")

        # Trend analysis
        if corr_improvement > 0.5:
            trend = "positive"
        elif corr_improvement < -0.5:
            trend = "negative"
        else:
            trend = "no clear"
        report.append(
            f"• Trend Analysis: {trend.capitalize()} relationship between learning rate and ACP effectiveness"
        )
        report.append("")

        # Detailed results table
        report.append("DETAILED RESULTS BY LEARNING RATE")
        report.append("-" * 40)
        report.append(
            f"{'LR':>4} {'ΔReward':>8} {'Improve%':>9} {'Cohen-d':>8} {'P-val':>8} {'Power':>7} {'ConfDeg%':>9}"
        )
        report.append("-" * 80)

        for r in sweep_results:
            report.append(
                f"{r['learning_rate']:4.1f} {r['reward_delta']:8.2f} {r['percent_improvement']:8.1f}% "
                f"{r['cohen_d']:7.3f} {r['p_value']:7.2e} {r['statistical_power']:6.3f} "
                f"{r['confidence_degradation']:8.1f}%"
            )

        report.append("")
        report.append("=" * 80)
        report.append("ANALYSIS COMPLETE")
        report.append("=" * 80)

        # Save report
        report_file = self.output_dir / "learning_rate_sweep_report.txt"
        with open(report_file, "w") as f:
            f.write("\n".join(report))

        print(f"[SUCCESS] Summary report saved to {report_file}")

        return "\n".join(report)


def main():
    """Main execution function"""
    # Create sweep analyzer
    sweep = LearningRateSweep(output_dir="./learning_rate_sweep_results")

    # Define learning rates to test
    learning_rates = [0.2, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0]

    # Run sweep
    results = sweep.run_learning_rate_sweep(learning_rates=learning_rates, episodes_per_config=1000)

    # Create visualizations
    sweep.create_comprehensive_visualizations(
        sweep_results=results, output_prefix="./learning_rate_sweep_results/learning_rate_analysis"
    )

    # Generate report
    report = sweep.generate_summary_report(results)
    print("\n" + report)


if __name__ == "__main__":
    main()
