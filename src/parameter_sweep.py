"""
PARAMETER SWEEP ANALYSIS
Automated sensitivity analysis across multiple parameter configurations

Enables systematic exploration of:
- ACP strength variations
- Network size scaling
- Connectivity effects  
- Learning rate impacts
- Vulnerability distribution comparisons

Author: dyb
Date: December 09, 2025
"""

import json
import pickle
import subprocess
import time
from pathlib import Path
from typing import Dict, List

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class ParameterSweep:
    """
    Automated parameter sweep for ACP sensitivity analysis
    """

    def __init__(self, base_config: Dict, output_dir: str = "./sweep_results"):
        self.base_config = base_config
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.results = []

    def sweep_single_parameter(
        self, param_name: str, param_values: List, episodes_per_config: int = 1000
    ):
        """
        Sweep a single parameter while keeping others constant
        """
        print(f"\n{'='*80}")
        print(f"PARAMETER SWEEP: {param_name}")
        print(f"{'='*80}")
        print(f"Values to test: {param_values}")
        print(f"Episodes per configuration: {episodes_per_config}")
        print(f"Total episodes: {len(param_values) * episodes_per_config}")
        print()

        sweep_results = []

        for i, value in enumerate(param_values):
            print(f"[{i+1}/{len(param_values)}] Testing {param_name} = {value}...")

            # Create configuration
            config = self.base_config.copy()
            config[param_name] = value
            config["num_episodes"] = episodes_per_config

            # Save config
            config_file = self.output_dir / f"sweep_{param_name}_{value}_config.json"
            with open(config_file, "w") as f:
                json.dump(config, f, indent=2)

            # Run simulation
            output_prefix = f"sweep_{param_name}_{value}"
            cmd = [
                "python",
                "acp_fully_configurable.py",
                f"--num-episodes={episodes_per_config}",
                f"--output-dir={self.output_dir}",
                f"--output-prefix={output_prefix}",
            ]

            # Add parameter-specific arguments
            if param_name == "acp_strength":
                cmd.append(f"--acp-strength={value}")
            elif param_name == "num_nodes":
                cmd.append(f"--num-nodes={value}")
            elif param_name == "connectivity":
                cmd.append(f"--connectivity={value}")
            elif param_name == "learning_rate":
                cmd.append(f"--learning-rate={value}")
            elif param_name == "vulnerability_distribution":
                cmd.append(f"--vulnerability-distribution={value}")
            elif param_name == "confidence_level":
                cmd.append(f"--confidence-level={value}")
            elif param_name == "bootstrap_samples":
                cmd.append(f"--bootstrap-samples={value}")
            elif param_name == "latency_window":
                # Handle tuple format (min, max)
                cmd.append(f"--latency-window-min={value[0]}")
                cmd.append(f"--latency-window-max={value[1]}")

            # Add base parameters
            for key, val in config.items():
                if key not in [param_name, "num_episodes", "n_cores"]:
                    if key == "acp_strength" and param_name != "acp_strength":
                        cmd.append(f"--acp-strength={val}")
                    elif key == "num_nodes" and param_name != "num_nodes":
                        cmd.append(f"--num-nodes={val}")
                    elif key == "connectivity" and param_name != "connectivity":
                        cmd.append(f"--connectivity={val}")
                    elif key == "learning_rate" and param_name != "learning_rate":
                        cmd.append(f"--learning-rate={val}")

            start_time = time.time()
            result = subprocess.run(cmd, capture_output=True, text=True)
            runtime = time.time() - start_time

            if result.returncode != 0:
                print(f"  ❌ Error running simulation")
                print(f"  {result.stderr}")
                continue

            # Load results
            result_file = self.output_dir / f"{output_prefix}_results.pkl"
            with open(result_file, "rb") as f:
                data = pickle.load(f)

            analysis = data["analysis"]

            sweep_results.append(
                {
                    "param_name": param_name,
                    "param_value": value,
                    "acp_mean": analysis["acp_mean"],
                    "traditional_mean": analysis["traditional_mean"],
                    "delta": analysis["delta"],
                    "percent_improvement": analysis["percent_improvement"],
                    "cohen_d": analysis["power_analysis"]["cohen_d"],
                    "p_value": analysis["power_analysis"]["p_value"],
                    "power": analysis["power_analysis"]["achieved_power"],
                    "runtime": runtime,
                    "config": config,
                    "full_analysis": analysis,
                }
            )

            print(
                f"  ✅ Complete: Δ={analysis['delta']:.1f}, d={analysis['power_analysis']['cohen_d']:.2f}, p={analysis['power_analysis']['p_value']:.2e}"
            )

        # Save sweep results
        sweep_file = self.output_dir / f"sweep_{param_name}_summary.pkl"
        with open(sweep_file, "wb") as f:
            pickle.dump(sweep_results, f)

        print(f"\n✅ Sweep complete: {len(sweep_results)} configurations tested")
        print(f"   Results saved to {sweep_file}")

        return sweep_results

    def create_sweep_visualization(self, sweep_results: List[Dict], output_file: str = None):
        """
        Create visualization of parameter sweep results
        """
        param_name = sweep_results[0]["param_name"]
        param_values = [r["param_value"] for r in sweep_results]

        fig, axes = plt.subplots(2, 3, figsize=(18, 10))
        fig.suptitle(f"Parameter Sweep: {param_name}", fontsize=16, fontweight="bold")

        # 1. Mean rewards
        ax = axes[0, 0]
        acp_means = [r["acp_mean"] for r in sweep_results]
        trad_means = [r["traditional_mean"] for r in sweep_results]

        ax.plot(param_values, acp_means, "o-", label="ACP", linewidth=2, markersize=8)
        ax.plot(param_values, trad_means, "s-", label="Traditional", linewidth=2, markersize=8)
        ax.set_xlabel(param_name, fontsize=11)
        ax.set_ylabel("Mean Reward", fontsize=11)
        ax.set_title("Performance vs Parameter", fontsize=12, fontweight="bold")
        ax.legend()
        ax.grid(True, alpha=0.3)

        # 2. Improvement percentage
        ax = axes[0, 1]
        improvements = [r["percent_improvement"] for r in sweep_results]
        ax.plot(param_values, improvements, "o-", color="green", linewidth=2, markersize=8)
        ax.axhline(y=100, color="gray", linestyle="--", alpha=0.5)
        ax.set_xlabel(param_name, fontsize=11)
        ax.set_ylabel("Improvement (%)", fontsize=11)
        ax.set_title("ACP Improvement vs Parameter", fontsize=12, fontweight="bold")
        ax.grid(True, alpha=0.3)

        # 3. Effect size
        ax = axes[0, 2]
        cohens_d = [r["cohen_d"] for r in sweep_results]
        ax.plot(param_values, cohens_d, "o-", color="purple", linewidth=2, markersize=8)
        ax.axhline(y=0.8, color="gray", linestyle="--", alpha=0.5, label="Large effect")
        ax.set_xlabel(param_name, fontsize=11)
        ax.set_ylabel("Cohen's d", fontsize=11)
        ax.set_title("Effect Size vs Parameter", fontsize=12, fontweight="bold")
        ax.legend()
        ax.grid(True, alpha=0.3)

        # 4. P-value (log scale)
        ax = axes[1, 0]
        p_values = [max(r["p_value"], 1e-300) for r in sweep_results]  # Avoid log(0)
        ax.semilogy(param_values, p_values, "o-", color="red", linewidth=2, markersize=8)
        ax.axhline(y=0.05, color="gray", linestyle="--", alpha=0.5, label="α=0.05")
        ax.axhline(y=0.001, color="gray", linestyle=":", alpha=0.5, label="α=0.001")
        ax.set_xlabel(param_name, fontsize=11)
        ax.set_ylabel("p-value (log scale)", fontsize=11)
        ax.set_title("Statistical Significance vs Parameter", fontsize=12, fontweight="bold")
        ax.legend()
        ax.grid(True, alpha=0.3, which="both")

        # 5. Statistical power
        ax = axes[1, 1]
        powers = [r["power"] for r in sweep_results]
        ax.plot(param_values, powers, "o-", color="blue", linewidth=2, markersize=8)
        ax.axhline(y=0.8, color="gray", linestyle="--", alpha=0.5, label="80% power")
        ax.axhline(y=0.95, color="gray", linestyle=":", alpha=0.5, label="95% power")
        ax.set_xlabel(param_name, fontsize=11)
        ax.set_ylabel("Statistical Power", fontsize=11)
        ax.set_title("Power Analysis vs Parameter", fontsize=12, fontweight="bold")
        ax.set_ylim([0, 1.05])
        ax.legend()
        ax.grid(True, alpha=0.3)

        # 6. Summary table
        ax = axes[1, 2]
        ax.axis("off")

        table_data = []
        for r in sweep_results:
            table_data.append(
                [
                    f"{r['param_value']:.3g}",
                    f"{r['delta']:.1f}",
                    f"{r['percent_improvement']:.0f}%",
                    f"{r['cohen_d']:.2f}",
                ]
            )

        table = ax.table(
            cellText=table_data,
            colLabels=[param_name, "Δ", "Improve", "d"],
            cellLoc="center",
            loc="center",
            bbox=[0, 0, 1, 1],
        )
        table.auto_set_font_size(False)
        table.set_fontsize(9)
        table.scale(1, 2)

        for i in range(len(table_data) + 1):
            for j in range(4):
                cell = table[(i, j)]
                if i == 0:
                    cell.set_facecolor("#4682B4")
                    cell.set_text_props(weight="bold", color="white")
                else:
                    cell.set_facecolor("#E8F4F8" if i % 2 == 0 else "white")

        ax.set_title("Summary Statistics", fontsize=12, fontweight="bold")

        plt.tight_layout()

        if output_file is None:
            output_file = self.output_dir / f"sweep_{param_name}_visualization.png"

        plt.savefig(output_file, dpi=300, bbox_inches="tight")
        print(f"✅ Visualization saved to {output_file}")

        return fig


def run_sensitivity_analysis():
    """
    Run comprehensive sensitivity analysis
    """
    print("\n" + "╔" + "=" * 78 + "╗")
    print("║" + " " * 78 + "║")
    print("║" + "COMPREHENSIVE SENSITIVITY ANALYSIS".center(78) + "║")
    print("║" + " " * 78 + "║")
    print("╚" + "=" * 78 + "╝")
    print()

    # Base configuration
    base_config = {
        "acp_strength": 0.65,
        "num_nodes": 50,
        "connectivity": 0.6,
        "latency_window": (0.3, 0.8),
        "learning_rate": 1.0,
        "decay_rate": 0.8,
        "noise": 0.1,
        "confidence_level": 0.95,
        "bootstrap_samples": 10000,
        "vulnerability_distribution": "uniform",
    }

    sweeper = ParameterSweep(base_config, output_dir="./sensitivity_analysis")

    # Define sweeps
    sweeps_to_run = [
        ("acp_strength", [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]),
        ("num_nodes", [50, 100, 200]),
        ("connectivity", [0.3, 0.5, 0.7]),
        ("learning_rate", [0.5, 1.0, 1.5, 2.0]),
        ("vulnerability_distribution", ["uniform", "normal", "exponential", "bimodal"]),
    ]

    all_results = {}

    for param_name, param_values in sweeps_to_run:
        print(f"\n{'#'*80}")
        print(f"# Sweep {param_name}")
        print(f"{'#'*80}\n")

        results = sweeper.sweep_single_parameter(param_name, param_values, episodes_per_config=1000)
        all_results[param_name] = results

        # Create visualization
        sweeper.create_sweep_visualization(results)

    # Create summary report
    print("\n" + "=" * 80)
    print("SENSITIVITY ANALYSIS COMPLETE")
    print("=" * 80)
    print()

    print("Summary of Results:")
    print()

    for param_name, results in all_results.items():
        print(f"{param_name}:")
        print(f"  • Configurations tested: {len(results)}")
        print(
            f"  • Improvement range: {min(r['percent_improvement'] for r in results):.1f}% to {max(r['percent_improvement'] for r in results):.1f}%"
        )
        print(
            f"  • Effect size range: {min(r['cohen_d'] for r in results):.2f} to {max(r['cohen_d'] for r in results):.2f}"
        )
        print()


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        # Quick single parameter sweep
        param_name = sys.argv[1]

        if param_name == "acp_strength":
            values = [0.3, 0.5, 0.7, 0.9]
        elif param_name == "num_nodes":
            values = [50, 100, 200, 500]
        elif param_name == "connectivity":
            values = [0.3, 0.5, 0.7]
        elif param_name == "learning_rate":
            values = [0.5, 1.0, 2.0]
        else:
            print(f"Unknown parameter: {param_name}")
            print("Available: acp_strength, num_nodes, connectivity, learning_rate")
            sys.exit(1)

        base_config = {
            "acp_strength": 0.65,
            "num_nodes": 50,
            "connectivity": 0.6,
            "learning_rate": 1.0,
            "decay_rate": 0.8,
            "noise": 0.1,
            "confidence_level": 0.95,
            "bootstrap_samples": 10000,
            "vulnerability_distribution": "uniform",
        }

        sweeper = ParameterSweep(base_config)
        results = sweeper.sweep_single_parameter(param_name, values, episodes_per_config=1000)
        sweeper.create_sweep_visualization(results)
    else:
        # Full sensitivity analysis
        run_sensitivity_analysis()
