"""
NIST ACTS Integration Module

Integration with NIST Advanced Combinatorial Testing System (ACTS)
for generating minimal test suites that achieve t-way combinatorial coverage.
"""

from .generator import (
    ACTSGenerator,
    ACTSParameter,
    ACTSConstraint,
    ACP_PARAMETERS,
    ACP_CONSTRAINTS
)

from .runner import (
    ACTSRunner,
    run_acts_experiment
)

__all__ = [
    'ACTSGenerator',
    'ACTSParameter',
    'ACTSConstraint',
    'ACP_PARAMETERS',
    'ACP_CONSTRAINTS',
    'ACTSRunner',
    'run_acts_experiment'
]