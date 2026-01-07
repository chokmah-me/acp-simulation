"""
Statistical analysis functions for ACP simulation.

This module provides:
- Power analysis with configurable parameters
- Bootstrap confidence intervals
- Effect size calculations (Cohen's d)
- Statistical significance testing
"""

from typing import Any, Dict

import numpy as np
from numpy.typing import NDArray
from scipy import stats

from ..core.types import ConfidenceInterval


def calculate_power_analysis(
    acp_rewards: NDArray[np.float64], traditional_rewards: NDArray[np.float64], alpha: float = 0.05
) -> Dict[str, float]:
    """
    Calculate statistical power analysis for ACP vs Traditional comparison.

    Parameters
    ----------
    acp_rewards : NDArray[np.float64]
        Rewards from ACP defender episodes
    traditional_rewards : NDArray[np.float64]
        Rewards from Traditional defender episodes
    alpha : float, default=0.05
        Significance level

    Returns
    -------
    Dict[str, float]
        Power analysis results including:
        - mean_acp: Mean reward for ACP
        - mean_traditional: Mean reward for Traditional
        - cohen_d: Effect size (Cohen's d)
        - t_statistic: t-test statistic
        - p_value: Statistical significance
        - achieved_power: Statistical power (0-1)
        - confidence_level: 1 - alpha
    """
    # Calculate basic statistics
    mean_acp = np.mean(acp_rewards)
    mean_trad = np.mean(traditional_rewards)
    std_acp = np.std(acp_rewards, ddof=1)
    std_trad = np.std(traditional_rewards, ddof=1)

    # Pooled standard deviation for effect size
    pooled_std = np.sqrt((std_acp**2 + std_trad**2) / 2)
    cohen_d = (mean_acp - mean_trad) / pooled_std

    # Statistical significance test
    t_stat, p_value = stats.ttest_ind(acp_rewards, traditional_rewards)

    # Sample sizes
    n1 = len(acp_rewards)
    n2 = len(traditional_rewards)
    df = n1 + n2 - 2

    # Calculate achieved power
    ncp = np.abs(cohen_d) * np.sqrt(n1 * n2 / (n1 + n2))
    critical_t = stats.t.ppf(1 - alpha / 2, df)

    power = 1 - stats.nct.cdf(critical_t, df, ncp) + stats.nct.cdf(-critical_t, df, ncp)

    return {
        "mean_acp": float(mean_acp),
        "mean_traditional": float(mean_trad),
        "std_acp": float(std_acp),
        "std_traditional": float(std_trad),
        "cohen_d": float(cohen_d),
        "t_statistic": float(t_stat),
        "p_value": float(p_value),
        "degrees_freedom": float(df),
        "achieved_power": float(power),
        "alpha": float(alpha),
        "confidence_level": 1 - alpha,
    }


def bootstrap_confidence_intervals(
    acp_rewards: NDArray[np.float64],
    traditional_rewards: NDArray[np.float64],
    n_bootstrap: int = 10000,
    confidence_level: float = 0.95,
    random_seed: int = 42,
) -> Dict[str, ConfidenceInterval]:
    """
    Calculate bootstrap confidence intervals for ACP vs Traditional comparison.

    Uses bootstrap resampling to compute confidence intervals for:
    - Mean rewards (ACP and Traditional)
    - Reward difference (delta)
    - Effect size (Cohen's d)

    Parameters
    ----------
    acp_rewards : NDArray[np.float64]
        Rewards from ACP defender episodes
    traditional_rewards : NDArray[np.float64]
        Rewards from Traditional defender episodes
    n_bootstrap : int, default=10000
        Number of bootstrap samples
    confidence_level : float, default=0.95
        Confidence level (0.90, 0.95, or 0.99)
    random_seed : int, default=42
        Random seed for reproducibility

    Returns
    -------
    Dict[str, ConfidenceInterval]
        Confidence intervals for:
        - mean_acp_ci: CI for ACP mean reward
        - mean_traditional_ci: CI for Traditional mean reward
        - delta_ci: CI for reward difference
        - cohen_d_ci: CI for effect size
    """
    # Set random seed for reproducibility
    rng = np.random.default_rng(random_seed)

    # Initialize bootstrap results
    boot_mean_acp = []
    boot_mean_trad = []
    boot_delta = []
    boot_cohen_d = []

    # Get sample sizes
    n_acp = len(acp_rewards)
    n_trad = len(traditional_rewards)

    # Perform bootstrap resampling
    for _ in range(n_bootstrap):
        # Resample with replacement
        sample_acp = rng.choice(acp_rewards, size=n_acp, replace=True)
        sample_trad = rng.choice(traditional_rewards, size=n_trad, replace=True)

        # Calculate statistics for this sample
        mean_acp = np.mean(sample_acp)
        mean_trad = np.mean(sample_trad)
        delta = mean_acp - mean_trad

        # Effect size for this sample
        pooled_std = np.sqrt((np.var(sample_acp) + np.var(sample_trad)) / 2)
        cohen_d = delta / pooled_std if pooled_std > 0 else 0

        # Store results
        boot_mean_acp.append(mean_acp)
        boot_mean_trad.append(mean_trad)
        boot_delta.append(delta)
        boot_cohen_d.append(cohen_d)

    # Calculate percentiles for confidence intervals
    alpha = 1 - confidence_level
    lower_percentile = (alpha / 2) * 100
    upper_percentile = (1 - alpha / 2) * 100

    return {
        "mean_acp_ci": (
            float(np.percentile(boot_mean_acp, lower_percentile)),
            float(np.percentile(boot_mean_acp, upper_percentile)),
        ),
        "mean_traditional_ci": (
            float(np.percentile(boot_mean_trad, lower_percentile)),
            float(np.percentile(boot_mean_trad, upper_percentile)),
        ),
        "delta_ci": (
            float(np.percentile(boot_delta, lower_percentile)),
            float(np.percentile(boot_delta, upper_percentile)),
        ),
        "cohen_d_ci": (
            float(np.percentile(boot_cohen_d, lower_percentile)),
            float(np.percentile(boot_cohen_d, upper_percentile)),
        ),
        "confidence_level": confidence_level,
        "n_bootstrap": n_bootstrap,
        "random_seed": random_seed,
    }


def analyze_experiment_results(
    acp_results: NDArray[np.float64],
    traditional_results: NDArray[np.float64],
    acp_action_counts: Dict[str, int],
    traditional_action_counts: Dict[str, int],
    acp_confidence_scores: NDArray[np.float64],
    traditional_confidence_scores: NDArray[np.float64],
    config: Dict[str, float],
) -> Dict[str, Any]:
    """
    Comprehensive analysis of ACP experiment results.

    Parameters
    ----------
    acp_results : NDArray[np.float64]
        Rewards from ACP episodes
    traditional_results : NDArray[np.float64]
        Rewards from Traditional episodes
    acp_action_counts : Dict[str, int]
        Action frequency counts for ACP
    traditional_action_counts : Dict[str, int]
        Action frequency counts for Traditional
    acp_confidence_scores : NDArray[np.float64]
        Attacker confidence scores vs ACP
    traditional_confidence_scores : NDArray[np.float64]
        Attacker confidence scores vs Traditional
    config : Dict[str, float]
        Experiment configuration

    Returns
    -------
    Dict[str, Any]
        Comprehensive analysis results
    """
    # Basic statistics
    acp_mean = np.mean(acp_results)
    acp_std = np.std(acp_results, ddof=1)
    acp_median = np.median(acp_results)

    traditional_mean = np.mean(traditional_results)
    traditional_std = np.std(traditional_results, ddof=1)
    traditional_median = np.median(traditional_results)

    # Performance metrics
    delta = acp_mean - traditional_mean
    percent_improvement = (delta / abs(traditional_mean)) * 100

    # Power analysis
    power_results = calculate_power_analysis(
        acp_results, traditional_results, alpha=1 - config.get("confidence_level", 0.95)
    )

    # Bootstrap confidence intervals
    ci_results = bootstrap_confidence_intervals(
        acp_results,
        traditional_results,
        n_bootstrap=int(config.get("bootstrap_samples", 10000)),
        confidence_level=config.get("confidence_level", 0.95),
    )

    # Action distributions
    total_acp = sum(acp_action_counts.values())
    total_trad = sum(traditional_action_counts.values())

    acp_distribution = {k: v / total_acp for k, v in acp_action_counts.items()}
    traditional_distribution = {k: v / total_trad for k, v in traditional_action_counts.items()}

    # Confidence degradation
    acp_conf = np.mean(acp_confidence_scores) if len(acp_confidence_scores) > 0 else 0
    trad_conf = (
        np.mean(traditional_confidence_scores) if len(traditional_confidence_scores) > 0 else 1
    )

    confidence_degradation = (1 - acp_conf / trad_conf) * 100 if trad_conf > 0 else 0

    return {
        # Basic statistics
        "acp_mean": float(acp_mean),
        "acp_std": float(acp_std),
        "acp_median": float(acp_median),
        "traditional_mean": float(traditional_mean),
        "traditional_std": float(traditional_std),
        "traditional_median": float(traditional_median),
        # Performance metrics
        "delta": float(delta),
        "percent_improvement": float(percent_improvement),
        # Statistical analysis
        "power_analysis": power_results,
        "confidence_intervals": ci_results,
        # Action distributions
        "acp_action_distribution": acp_distribution,
        "traditional_action_distribution": traditional_distribution,
        # Confidence analysis
        "acp_attacker_confidence": float(acp_conf),
        "traditional_attacker_confidence": float(trad_conf),
        "confidence_degradation": float(confidence_degradation),
        # Configuration
        "config": config,
    }
