# Bridge validation: phase-contingent pricing vs IBLT attackers

Sim-side half of the dwell-fiber ACP bridge (`daemon/acp_policy.go`,
`--acp-policy`). Answers: does phase-contingent ADMM pricing beat fixed
pricing against an IBLT-driven attacker, and at what false-positive cost?

Run: `PYTHONPATH=src python -m acp_simulation.bridge.experiment
--episodes 200 --windows 150 --seed 42`

## Design

One host, 150 one-second windows per episode, five processes:

- **Attacker (pid 0)**: a real `CognitiveAttacker` (IBLT, decay 0.8, noise 0.1)
  with a two-instance EXPLOIT prior (returning attacker). Each window it
  selects SCAN / EXPLOIT / PROPAGATE from learned memory; the action maps to
  an I/O signature: SCAN = enumeration (ufm 80-200/s, tbw ~0; WIP ~98),
  EXPLOIT = encryption burst (tbw 350-500 MB/s; WIP ~190),
  PROPAGATE = lateral (WIP ~152). **Closed loop**: the defender's price is the
  attacker's outcome -- throttled actions fail (-1), kill ends the episode (-2),
  successful actions reward (+0.3/+0.5/+1.0). The attacker adapts its strategy
  to the defender under test.
- **Benign (pids 1-4)**: idle, tar (5%/window burst starts, 3-5 window bursts),
  ambient open-storm contaminant (~680 opens/s, zero bytes, active in 40% of
  25-window blocks), dev. Traces are pre-generated per episode (common random
  numbers) so both arms face identical benign load.

Arms: **fixed** pricing (`price = 0.9*price + 0.5*(wip-150)`, Go-faithful port
of `controller_v3.go`) vs **phase-contingent** (same update modulated by the
inferred phase -- recon x0.4/x1.25, learning x0.8/x1.0, exploitation x1.8/x0.85;
Go-faithful port of `acp_policy.go`). Kill price 150, throttle price 50
(`pkg/enforcement/config.go`). Paired by episode seed, n=200.

## Results (n=200, seed 42)

| metric | fixed | phase-contingent | paired diff (phase-fixed), 95% CI |
|---|---|---|---|
| detection rate | 0.155 | **0.620** | +0.465 [0.39, 0.54], d=0.88, p=9e-21 |
| detection delay, windows (n=28 both detected) | median 24.5 | **median 9.0** | -15.07 [-21.61, -9.36], d=-0.89, p<0.0001 |
| false positives / episode | 0.865 | **0.605** | -0.260 [-0.325, -0.195] |

Mechanism check (3 sample episodes): the attacker passes through
UNKNOWN -> RECON/LEARNING -> EXPLOITATION and is killed 2-4 windows after
exploitation is confirmed (kill at windows 4, 8, 17).

## Reading the results honestly

- **The win is real but has a specific mechanism.** Under fixed pricing the
  IBLT attacker learns the throttle boundary: EXPLOIT at price >= 50 fails, so
  it backs off to SCAN, the price leaks down, and it oscillates *under* the
  kill threshold indefinitely (hence the 15.5% detection rate). The
  phase-contingent policy escalates 1.8x once exploitation is confirmed, so the
  attacker cannot ride the boundary -- kill follows within a few windows.
- **The FP reduction is partly a misclassification artifact.** The ambient
  storm (680 opens/s, ~0 bytes) matches the recon signature, so it gets the
  dampened recon pricing (alpha x0.4) and crosses the kill price *slower* than
  under fixed pricing. The policy does not distinguish the contaminant from
  real enumeration -- it just prices both more leniently. Per-comm baselines or
  budget recalibration are still needed for the ambient problem.
- **Untested**: real workload traces (these are synthetic signatures), the
  actual Go estimator against live BPF data (needs the WSL host), and
  adversarial attackers that deliberately mimic benign phase patterns.

Raw results: `results/pricing_validation.json`.
