"""Episode workload for the pricing validation experiment.

One host, five processes, T one-second windows:

- pid 0: attacker, driven by a real IBLT ``CognitiveAttacker``. Each window it
  selects SCAN / EXPLOIT / PROPAGATE from its learned memory; the action maps
  to an I/O signature (tbw MB/s, ufm opens/s). The defender's price feeds back
  as the attacker's outcome (closed loop): actions taken while throttled fail
  (outcome -1), while killed the episode ends for the attacker (outcome -2).
- pids 1-4: benign processes with fixed behavior generators. Traces are
  pre-generated per episode so both pricing arms face identical benign load
  (common random numbers); only the attacker's RNG stream is re-seeded per arm.

Signatures are calibrated against the T2 budget (150) so the experiment is
discriminating: recon stays under budget, exploitation exceeds it, and the
ambient open-storm contaminant exceeds it badly -- reproducing the known
dwell-fiber contaminant at WIP ~476 vs budget 150.
"""

from __future__ import annotations

from typing import Callable, Dict, List, Tuple

import numpy as np

from ..agents.attacker import CognitiveAttacker
from ..core.enums import ActionType
from .pricing import THROTTLE_PRICE

ATTACKER_PID = 0
BENIGN_PIDS = (1, 2, 3, 4)

Sig = Tuple[float, float]  # (tbw MB/s, ufm opens/s)


def _scan_sig(rng: np.random.Generator) -> Sig:
    # Enumeration: many opens, ~zero bytes. WIP ~98 < budget.
    return (float(rng.uniform(0, 0.5)), float(rng.uniform(80, 200)))


def _exploit_sig(rng: np.random.Generator) -> Sig:
    # Intermittent encryption burst. WIP ~190 > budget.
    return (float(rng.uniform(350, 500)), float(rng.uniform(60, 120)))


def _propagate_sig(rng: np.random.Generator) -> Sig:
    # Lateral movement. WIP ~152, marginal vs budget.
    return (float(rng.uniform(5, 25)), float(rng.uniform(120, 300)))


ACTION_SIG: Dict[ActionType, Callable[[np.random.Generator], Sig]] = {
    ActionType.SCAN: _scan_sig,
    ActionType.EXPLOIT: _exploit_sig,
    ActionType.PROPAGATE: _propagate_sig,
}

ACTION_OUTCOME = {
    ActionType.SCAN: 0.3,
    ActionType.PROPAGATE: 0.5,
    ActionType.EXPLOIT: 1.0,
}


def make_attacker() -> CognitiveAttacker:
    """Fresh IBLT attacker with a small prior: a returning attacker that has
    successfully exploited twice before (documented modeling choice so episodes
    reach the exploitation phase within T windows)."""
    attacker = CognitiveAttacker(decay_rate=0.8, noise=0.1)
    for ts in (-4, -2):
        attacker.learn((0, 0, 0, -1), ActionType.EXPLOIT, 1.0, ts, 1.0)
    return attacker


def _idle_sig(rng: np.random.Generator) -> Sig:
    return (0.0, float(rng.uniform(0, 5)))


def _dev_sig(rng: np.random.Generator) -> Sig:
    return (float(rng.uniform(10, 40)), float(rng.uniform(20, 60)))


def _tar_sig(rng: np.random.Generator, bursting: bool) -> Sig:
    if bursting:
        return (float(rng.uniform(300, 500)), float(rng.uniform(30, 80)))
    return (float(rng.uniform(0, 5)), float(rng.uniform(5, 20)))


def _ambient_sig(rng: np.random.Generator, active: bool) -> Sig:
    if active:
        # The known contaminant: ~680 opens/s, zero bytes.
        return (0.0, float(rng.uniform(600, 760)))
    return (0.0, float(rng.uniform(0, 5)))


def generate_benign_traces(rng: np.random.Generator, n_windows: int) -> Dict[int, List[Sig]]:
    """Pre-generate identical benign traces for both pricing arms."""
    traces: Dict[int, List[Sig]] = {pid: [] for pid in BENIGN_PIDS}

    tar_burst_left = 0
    ambient_blocks = [rng.random() < 0.4 for _ in range((n_windows + 24) // 25)]

    for t in range(n_windows):
        traces[1].append(_idle_sig(rng))

        if tar_burst_left > 0:
            tar_burst_left -= 1
            traces[2].append(_tar_sig(rng, True))
        elif rng.random() < 0.05:
            tar_burst_left = int(rng.integers(2, 5))
            traces[2].append(_tar_sig(rng, True))
        else:
            traces[2].append(_tar_sig(rng, False))

        traces[3].append(_ambient_sig(rng, ambient_blocks[t // 25]))
        traces[4].append(_dev_sig(rng))

    return traces


def attacker_outcome(price: float, action: ActionType) -> float:
    """Closed-loop outcome: defender pressure punishes the attacker."""
    if price >= THROTTLE_PRICE:
        return -1.0  # action disrupted by throttling
    return ACTION_OUTCOME[action]
