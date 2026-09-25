"""ACP bridge: sim-side validation package.

Validates the dwell-fiber ACP cognitive-phase price policy
(``daemon/acp_policy.go``, ``--acp-policy``) against IBLT-driven attackers:
fixed ADMM pricing vs phase-contingent pricing, paired by episode seed,
measuring detection delay and false-positive cost.

Modules
-------
pricing
    Go-faithful ports of the V3 pricing controllers (fixed + phase-contingent).
workload
    Episode workload: an IBLT ``CognitiveAttacker`` driving per-window I/O
    signatures, plus benign process traces (idle / tar-burst / ambient storm /
    dev) pre-generated per episode so both arms see identical benign behavior.
experiment
    Episode loop, metrics, paired statistical analysis, CLI runner.
"""

__all__ = ["pricing", "workload", "experiment"]
