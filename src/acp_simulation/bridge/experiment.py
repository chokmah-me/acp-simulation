"""Pricing validation experiment: fixed vs phase-contingent ADMM pricing.

Each episode simulates one host for ``--windows`` one-second windows. Both
pricing arms face the same episode seed: identical benign traces (common
random numbers) and an identically-initialized IBLT attacker whose subsequent
trajectory diverges only through the closed loop with the defender under test.

Metrics per episode per arm
---------------------------
- ``detected``: attacker price reached the kill threshold (150)
- ``delay``: windows from the attacker's first EXPLOIT to kill (None if the
  attacker was killed before exploiting, or never killed)
- ``fp_count`` / ``fp_max_price``: benign processes crossing the kill price

Analysis is paired by episode seed: bootstrap 95% CI on the paired mean
difference, paired Cohen's d, and Wilcoxon signed-rank p-values.

Usage
-----
python -m acp_simulation.bridge.experiment --episodes 200 --seed 42
"""

from __future__ import annotations

import argparse
import json
import os
import time
from dataclasses import asdict, dataclass
from typing import Dict, List, Optional

import numpy as np
from scipy import stats

from ..core.enums import ActionType
from .pricing import KILL_PRICE, THROTTLE_PRICE, FixedPricing, PhaseContingentPricing
from .workload import (
    ACTION_SIG,
    ATTACKER_PID,
    BENIGN_PIDS,
    attacker_outcome,
    generate_benign_traces,
    make_attacker,
)

ARMS = {"fixed": FixedPricing, "phase-contingent": PhaseContingentPricing}


@dataclass
class EpisodeMetrics:
    detected: bool
    kill_t: Optional[int]
    first_exploit_t: Optional[int]
    delay: Optional[float]
    fp_count: int
    fp_max_price: float
    scan_windows: int
    exploit_windows: int


def run_arm(seed: int, controller, benign, n_windows: int) -> EpisodeMetrics:
    np.random.seed(seed)  # attacker's np.random stream; identical start per arm
    rng = np.random.default_rng(seed + 1)  # signature draws
    attacker = make_attacker()

    kill_t = None
    first_exploit = None
    scan_n = exploit_n = 0
    benign_max = {pid: 0.0 for pid in BENIGN_PIDS}

    for t in range(n_windows):
        price = controller.prices.get(ATTACKER_PID, 0.0)
        alert = 0 if price < THROTTLE_PRICE else (1 if price < KILL_PRICE else 2)
        state = {"alert_level": alert, "time": t}
        situation = attacker._encode_situation(state)
        action = attacker.select_action(state, t)

        tbw, ufm = ACTION_SIG[action](rng)
        if action == ActionType.SCAN:
            scan_n += 1
        elif action == ActionType.EXPLOIT:
            exploit_n += 1
            if first_exploit is None:
                first_exploit = t

        _, new_price = controller.update(ATTACKER_PID, tbw, ufm)
        for pid in BENIGN_PIDS:
            _, bp = controller.update(pid, *benign[pid][t])
            benign_max[pid] = max(benign_max[pid], bp)

        if new_price >= KILL_PRICE:
            attacker.learn(situation, action, -2.0, t)
            kill_t = t
            break

        outcome = attacker_outcome(new_price, action)
        if action == ActionType.SCAN and outcome > 0:
            attacker.known_nodes.add(int(rng.integers(0, 64)))
        attacker.learn(situation, action, outcome, t)

    delay = (
        float(kill_t - first_exploit)
        if kill_t is not None and first_exploit is not None
        else None
    )
    fp = sum(1 for pid in BENIGN_PIDS if benign_max[pid] >= KILL_PRICE)
    return EpisodeMetrics(
        detected=kill_t is not None,
        kill_t=kill_t,
        first_exploit_t=first_exploit,
        delay=delay,
        fp_count=fp,
        fp_max_price=max(benign_max.values()),
        scan_windows=scan_n,
        exploit_windows=exploit_n,
    )


def run_episode(seed: int, n_windows: int) -> Dict[str, EpisodeMetrics]:
    benign = generate_benign_traces(np.random.default_rng(seed), n_windows)
    return {
        name: run_arm(seed, factory(), benign, n_windows)
        for name, factory in ARMS.items()
    }


# --- paired analysis --------------------------------------------------------


def bootstrap_paired_ci(
    diffs: np.ndarray, n_boot: int = 10000, ci: float = 0.95, seed: int = 0
):
    diffs = np.asarray(diffs, dtype=float)
    rng = np.random.default_rng(seed)
    boots = rng.choice(diffs, size=(n_boot, len(diffs)), replace=True).mean(axis=1)
    lo, hi = np.percentile(boots, [(1 - ci) / 2 * 100, (1 + ci) / 2 * 100])
    return float(lo), float(hi)


def paired_stats(diffs: np.ndarray) -> Dict[str, float]:
    diffs = np.asarray(diffs, dtype=float)
    out = {
        "n": int(len(diffs)),
        "mean_diff": float(np.mean(diffs)),
        "ci_lo": float("nan"),
        "ci_hi": float("nan"),
        "cohen_d_paired": float("nan"),
        "wilcoxon_p": 1.0,
    }
    if len(diffs) == 0:
        return out
    out["ci_lo"], out["ci_hi"] = bootstrap_paired_ci(diffs)
    sd = float(np.std(diffs, ddof=1))
    if sd > 0:
        out["cohen_d_paired"] = float(np.mean(diffs) / sd)
    nz = diffs[diffs != 0]
    if len(nz) > 0:
        try:
            out["wilcoxon_p"] = float(stats.wilcoxon(nz).pvalue)
        except ValueError:
            pass
    return out


def analyze(fixed: List[EpisodeMetrics], phase: List[EpisodeMetrics]) -> Dict:
    det_f = np.array([m.detected for m in fixed], dtype=float)
    det_p = np.array([m.detected for m in phase], dtype=float)

    both = [
        (a.delay, b.delay)
        for a, b in zip(fixed, phase)
        if a.delay is not None and b.delay is not None
    ]
    delay_diffs = np.array([b - a for a, b in both])

    fp_f = np.array([m.fp_count for m in fixed], dtype=float)
    fp_p = np.array([m.fp_count for m in phase], dtype=float)

    return {
        "episodes": len(fixed),
        "detection_rate": {
            "fixed": float(det_f.mean()),
            "phase_contingent": float(det_p.mean()),
            "paired_diff": paired_stats(det_p - det_f),
        },
        "detection_delay_windows": {
            "n_both_detected": len(both),
            "median_fixed": float(np.median([a for a, _ in both])) if both else None,
            "median_phase": float(np.median([b for _, b in both])) if both else None,
            # negative diff = phase-contingent detects faster
            "paired_diff_phase_minus_fixed": paired_stats(delay_diffs),
        },
        "false_positives_per_episode": {
            "mean_fixed": float(fp_f.mean()),
            "mean_phase": float(fp_p.mean()),
            "paired_diff_phase_minus_fixed": paired_stats(fp_p - fp_f),
        },
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--episodes", type=int, default=200)
    ap.add_argument("--windows", type=int, default=150)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--out", type=str, default="results")
    args = ap.parse_args()

    t0 = time.time()
    fixed, phase = [], []
    for i in range(args.episodes):
        ep = run_episode(args.seed + i, args.windows)
        fixed.append(ep["fixed"])
        phase.append(ep["phase-contingent"])
        if (i + 1) % 50 == 0:
            print(f"  ... {i + 1}/{args.episodes} episodes", flush=True)

    report = analyze(fixed, phase)
    report["config"] = {
        "episodes": args.episodes,
        "windows": args.windows,
        "seed": args.seed,
        "runtime_s": round(time.time() - t0, 1),
    }

    os.makedirs(args.out, exist_ok=True)
    path = os.path.join(args.out, "pricing_validation.json")
    with open(path, "w") as f:
        json.dump(report, f, indent=2)

    d = report["detection_rate"]
    dl = report["detection_delay_windows"]
    fp = report["false_positives_per_episode"]
    pd = dl["paired_diff_phase_minus_fixed"]
    print("\n=== Pricing validation: fixed vs phase-contingent (paired, n=%d) ==="
          % report["episodes"])
    print(f"detection rate      fixed={d['fixed']:.3f}  phase={d['phase_contingent']:.3f}")
    print(f"detection delay     n_both={dl['n_both_detected']}  "
          f"median fixed={dl['median_fixed']}  median phase={dl['median_phase']}")
    print(f"  paired diff (phase-fixed): mean={pd['mean_diff']:.2f} windows  "
          f"95% CI [{pd['ci_lo']:.2f}, {pd['ci_hi']:.2f}]  "
          f"d={pd['cohen_d_paired']:.2f}  wilcoxon p={pd['wilcoxon_p']:.4f}")
    pf = fp["paired_diff_phase_minus_fixed"]
    print(f"false positives/ep  fixed={fp['mean_fixed']:.3f}  phase={fp['mean_phase']:.3f}  "
          f"paired diff mean={pf['mean_diff']:.3f}  95% CI [{pf['ci_lo']:.3f}, {pf['ci_hi']:.3f}]")
    print(f"results -> {path}")


if __name__ == "__main__":
    main()
