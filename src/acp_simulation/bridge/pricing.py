"""Go-faithful ports of the dwell-fiber V3 pricing controllers.

Mirrors ``daemon/controller_v3.go`` (fixed ADMM update) and
``daemon/acp_policy.go`` (phase estimator + multiplier policy), with
thresholds from ``pkg/enforcement/config.go``:

- ``ALPHA=0.5``, ``LEAK=0.9``, T2 budget 150, T2 weights (0.3 TBW, 0.7 UFM)
- throttle price 50, kill price 150

Any behavioral divergence from the Go implementation is a bug in this file,
not a modeling choice.
"""

from __future__ import annotations

import math
from enum import IntEnum
from typing import Dict, Tuple

# --- V3 controller constants (daemon/controller_v3.go) ----------------------
ALPHA = 0.5
LEAK = 0.9
T2_BUDGET = 150.0
T2_OMEGA1 = 0.3  # TBW weight
T2_OMEGA2 = 0.7  # UFM weight

# --- Enforcement thresholds (pkg/enforcement/config.go) --------------------
THROTTLE_PRICE = 50.0
KILL_PRICE = 150.0

# --- ACP estimator constants (daemon/acp_policy.go) ------------------------
WINDOW_N = 8
MIN_WINDOWS = 3
RECON_OPENS = 50.0
RECON_TBW_CAP = 1.0
EXPLOIT_CV = 0.25
EXPLOIT_SUSTAIN = 4


class Phase(IntEnum):
    UNKNOWN = 0
    RECON = 1
    LEARNING = 2
    EXPLOITATION = 3


# (alpha_multiplier, budget_multiplier); UNKNOWN keeps the fixed update.
MULTIPLIERS: Dict[Phase, Tuple[float, float]] = {
    Phase.RECON: (0.4, 1.25),
    Phase.LEARNING: (0.8, 1.0),
    Phase.EXPLOITATION: (1.8, 0.85),
    Phase.UNKNOWN: (1.0, 1.0),
}


def wip_t2(tbw: float, ufm: float) -> float:
    """T2 work-in-progress: 0.3*TBW + 0.7*UFM."""
    return T2_OMEGA1 * tbw + T2_OMEGA2 * ufm


def _leak(price: float) -> float:
    p = price * LEAK
    return 0.0 if p < 0.5 else p


class ACPPhaseEstimator:
    """Port of daemon/acp_policy.go PhaseEstimator."""

    def __init__(self) -> None:
        self._states: Dict[int, Dict] = {}

    def observe(self, pid: int, tbw: float, ufm: float, wip: float, budget: float) -> Phase:
        st = self._states.setdefault(
            pid, {"wips": [], "prev_cv": 0.0, "has_prev": False, "streak": 0}
        )
        wips = st["wips"]
        wips.append(wip)
        if len(wips) > WINDOW_N:
            wips.pop(0)
        n = len(wips)

        st["streak"] = st["streak"] + 1 if wip > budget else 0

        recon_sig = ufm >= RECON_OPENS and tbw < RECON_TBW_CAP
        if n < MIN_WINDOWS:
            return Phase.RECON if recon_sig else Phase.UNKNOWN

        mean = sum(wips) / n
        if mean == 0:
            cv = math.inf
        else:
            var = sum((x - mean) ** 2 for x in wips) / n
            cv = math.sqrt(var) / mean

        if mean > budget and st["streak"] >= EXPLOIT_SUSTAIN and cv <= EXPLOIT_CV:
            st["prev_cv"], st["has_prev"] = cv, True
            return Phase.EXPLOITATION
        if mean > budget and st["has_prev"] and cv < st["prev_cv"]:
            st["prev_cv"] = cv
            return Phase.LEARNING

        st["prev_cv"], st["has_prev"] = cv, True
        return Phase.RECON if recon_sig else Phase.UNKNOWN


class FixedPricing:
    """Fixed ADMM update: price = leak(price) + alpha*(wip - budget)."""

    name = "fixed"

    def __init__(self) -> None:
        self.prices: Dict[int, float] = {}

    def update(self, pid: int, tbw: float, ufm: float) -> Tuple[float, float]:
        wip = wip_t2(tbw, ufm)
        price = max(0.0, _leak(self.prices.get(pid, 0.0)) + ALPHA * (wip - T2_BUDGET))
        self.prices[pid] = price
        return wip, price


class PhaseContingentPricing(FixedPricing):
    """ADMM update modulated by the inferred attacker phase (--acp-policy)."""

    name = "phase-contingent"

    def __init__(self) -> None:
        super().__init__()
        self.estimator = ACPPhaseEstimator()
        self.phases: Dict[int, Phase] = {}

    def update(self, pid: int, tbw: float, ufm: float) -> Tuple[float, float]:
        wip = wip_t2(tbw, ufm)
        phase = self.estimator.observe(pid, tbw, ufm, wip, T2_BUDGET)
        self.phases[pid] = phase
        alpha_mult, budget_mult = MULTIPLIERS[phase]
        price = max(
            0.0,
            _leak(self.prices.get(pid, 0.0))
            + (ALPHA * alpha_mult) * (wip - T2_BUDGET * budget_mult),
        )
        self.prices[pid] = price
        return wip, price
