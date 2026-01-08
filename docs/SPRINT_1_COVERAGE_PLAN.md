# Sprint 1 Coverage Plan
**Target**: Increase test coverage from 55% to 70%+
**Date**: 2026-01-07
**Status**: Active

## Current Coverage Baseline (2026-01-07)

```
TOTAL: 1519 statements, 680 missed → 55% coverage
Tests: 89 passed, 3 skipped
```

### Coverage by Module

| Module | Stmts | Miss | Cover | Priority |
|--------|-------|------|-------|----------|
| **Priority 1: Core Gaps** | | | | |
| visualization.py | 203 | 195 | 4% | LOW (plotting logic) |
| network_enhanced.py | 90 | 90 | 0% | LOW (experimental) |
| enhanced_runner.py | 126 | 126 | 0% | LOW (experimental) |
| conference_parameters.py | 28 | 28 | 0% | LOW (config only) |
| **Priority 2: Critical Gaps** | | | | |
| agents/defender.py | 105 | 36 | 66% | **HIGH** |
| agents/base.py | 36 | 12 | 67% | **HIGH** |
| environment/network.py | 199 | 43 | 78% | **MEDIUM** |
| simulation/runner.py | 128 | 49 | 62% | **HIGH** |
| **Priority 3: Integration** | | | | |
| acts/runner.py | 68 | 27 | 60% | MEDIUM |
| ccm/analyzer.py | 28 | 15 | 46% | MEDIUM |
| orchestrator.py | 55 | 44 | 20% | LOW |
| **Already Strong** | | | | |
| agents/attacker.py | 72 | 6 | 92% | ✓ |
| topology_generators.py | 89 | 6 | 93% | ✓ |
| acts/generator.py | 96 | 3 | 97% | ✓ |
| core/* (all modules) | 110 | 0 | 100% | ✓ |
| statistics.py | 63 | 0 | 100% | ✓ |

## Sprint 1 Test Development Plan

### Phase 1: Core Agent Logic (Priority HIGH)
**Target**: Bring critical modules to 85%+ coverage

#### 1.1 `agents/base.py` (67% → 85%)
**Current gaps** (12 missing statements):
- Lines 56: BaseAttacker abstract method
- Line 83: BaseDefender abstract method
- Line 100: Agent state initialization edge case
- Lines 140, 162, 173-181: State transition logic

**Tests to write**:
```python
# tests/test_agents_base.py (NEW FILE)
class TestBaseAttacker:
    def test_abstract_instantiation_raises_error()
    def test_attacker_state_initialization()
    def test_attacker_state_transitions()
    def test_attacker_memory_management()

class TestBaseDefender:
    def test_abstract_instantiation_raises_error()
    def test_defender_state_initialization()
    def test_defender_observation_handling()
    def test_defender_action_selection_interface()
```

**Estimated coverage gain**: +18% (67% → 85%)

#### 1.2 `agents/defender.py` (66% → 85%)
**Current gaps** (36 missing statements):
- Lines 77-100: Pessimistic defender initialization
- Lines 223-243: ACP defender cognitive latency logic
- Lines 282-287: Action execution edge cases
- Line 377: Reward computation corner case

**Tests to write**:
```python
# tests/test_agents_defender.py (NEW FILE)
class TestPessimisticDefender:
    def test_initialization_with_default_params()
    def test_initialization_with_custom_params()
    def test_select_action_no_vulnerable_nodes()
    def test_select_action_with_vulnerable_nodes()
    def test_state_update_logic()

class TestACPDefender:
    def test_initialization_with_acp_strength()
    def test_cognitive_latency_window_detection()
    def test_action_selection_during_latency_window()
    def test_action_selection_outside_latency_window()
    def test_reward_calculation_edge_cases()
    def test_interaction_with_attacker_processing()
```

**Estimated coverage gain**: +19% (66% → 85%)

### Phase 2: Environment Logic (Priority MEDIUM-HIGH)

#### 2.1 `environment/network.py` (78% → 85%)
**Current gaps** (43 missing statements):
- Lines 70-102: Alternative initialization paths
- Lines 119-122: Graph generation edge cases
- Lines 361-365: Action execution error handling
- Lines 448, 552-553, 558-562: Metrics calculation
- Lines 602-622: State transition validation

**Tests to write**:
```python
# tests/test_environment_network.py (NEW FILE - expand existing)
class TestNetworkEnvironmentInitialization:
    def test_custom_graph_initialization()
    def test_invalid_topology_raises_error()
    def test_vulnerability_distribution_edge_cases()

class TestNetworkActionExecution:
    def test_action_on_invalid_node_raises_error()
    def test_action_on_already_patched_node()
    def test_action_on_compromised_node()
    def test_concurrent_defender_attacker_actions()

class TestNetworkMetrics:
    def test_get_observation_completeness()
    def test_get_reward_edge_cases()
    def test_state_transition_validation()
```

**Estimated coverage gain**: +7% (78% → 85%)

#### 2.2 `simulation/runner.py` (62% → 85%)
**Current gaps** (49 missing statements):
- Line 65: Episode initialization edge case
- Line 104: Configuration validation
- Lines 182-188, 196: Result aggregation logic
- Lines 211-212: Seed generation edge cases
- Lines 276-345: Parallel execution paths

**Tests to write**:
```python
# tests/test_simulation_runner_extended.py (NEW FILE)
class TestRunnerConfigValidation:
    def test_invalid_config_raises_error()
    def test_run_episode_with_zero_steps()
    def test_run_episode_with_custom_seed()

class TestRunnerResultAggregation:
    def test_aggregate_empty_results()
    def test_aggregate_single_episode()
    def test_aggregate_statistical_metrics()

class TestRunnerParallelExecution:
    def test_parallel_run_with_single_worker()
    def test_parallel_run_with_multiple_workers()
    def test_parallel_run_reproducibility_with_seeds()
    def test_parallel_run_error_handling()
```

**Estimated coverage gain**: +23% (62% → 85%)

### Phase 3: Integration Modules (Priority MEDIUM)

#### 3.1 `integration/acts/runner.py` (60% → 75%)
**Current gaps** (27 missing statements):
- Lines 57-62, 68: ACTSRunner configuration
- Lines 78-87: Run experiment orchestration
- Lines 126-127, 173-188: Result processing

**Tests to write**:
```python
# Extend tests/test_integration_acts_runner.py
class TestACTSRunnerOrchestration:
    def test_run_configuration_with_seed_injection()
    def test_save_summary_with_custom_path()
    def test_convert_results_to_ccm_format()
```

**Estimated coverage gain**: +15% (60% → 75%)

#### 3.2 `integration/ccm/analyzer.py` (46% → 70%)
**Current gaps** (15 missing statements):
- Lines 57-93: CCM integration logic (requires Java CCM tool)

**Tests to write**:
```python
# Extend tests/test_integration_ccm_analyzer.py
class TestCCMAnalyzerMockIntegration:
    def test_analyze_with_mocked_java_call()
    def test_parse_ccm_output_with_sample_data()
    def test_error_handling_missing_jar()
```

**Estimated coverage gain**: +24% (46% → 70%)

## Coverage Calculation

### Current State
- **Total statements**: 1519
- **Missed**: 680
- **Coverage**: 55%

### Targeted Improvements (Sprint 1)
| Module | Current | Target | Statements | Gain |
|--------|---------|--------|------------|------|
| agents/base.py | 67% | 85% | 36 | +6.5 stmts |
| agents/defender.py | 66% | 85% | 105 | +20 stmts |
| environment/network.py | 78% | 85% | 199 | +14 stmts |
| simulation/runner.py | 62% | 85% | 128 | +29 stmts |
| acts/runner.py | 60% | 75% | 68 | +10 stmts |
| ccm/analyzer.py | 46% | 70% | 28 | +7 stmts |

**Total new coverage**: ~87 statements
**Projected overall coverage**: 55% + (87/1519 × 100%) = **61%**

### Stretch Goals (Sprint 2+)
To reach 70% overall:
- Need to cover additional **135 statements** (680 - 87 = 593 remaining, target 455)
- Options:
  - Visualization tests (snapshot/baseline testing): +50 stmts
  - Enhanced runner integration tests: +40 stmts
  - Network enhanced topology tests: +30 stmts
  - Orchestrator integration tests: +15 stmts

## Test Writing Guidelines

### Reproducibility Requirements
All tests MUST follow ACP simulation constraints:
```python
def test_example(self):
    # ✓ CORRECT: Explicit seed injection
    config = SimulationConfig(random_seed=42)
    rng = np.random.default_rng(42)

    # ✗ FORBIDDEN: Global random state
    # np.random.rand()  # NEVER USE
    # random.random()   # NEVER USE
```

### Type Safety
```python
from numpy.typing import NDArray
import numpy as np

def test_with_type_hints():
    state: NDArray[np.float64] = np.array([0.1, 0.2, 0.3])
    assert state.dtype == np.float64
```

### Statistical Validation
For behavioral tests:
```python
def test_statistical_property():
    results = run_multiple_episodes(n=100, seed=42)
    effect_size = cohens_d(results['acp'], results['baseline'])
    p_value = ttest_ind(results['acp'], results['baseline']).pvalue

    assert effect_size > 0.3  # Minimum meaningful effect
    assert p_value < 0.05     # Statistical significance
```

## Sprint 1 Execution Plan

### Week 1: Core Agents
- [x] Baseline coverage analysis (DONE)
- [ ] Write `tests/test_agents_base.py` (18 tests)
- [ ] Write `tests/test_agents_defender.py` (12 tests)
- [ ] Run coverage, validate 65%+ reached
- [ ] Commit with message: "test: add comprehensive agent base and defender tests"

### Week 2: Environment & Runner
- [ ] Write `tests/test_environment_network.py` extensions (9 tests)
- [ ] Write `tests/test_simulation_runner_extended.py` (11 tests)
- [ ] Run coverage, validate 68%+ reached
- [ ] Commit with message: "test: add environment and runner edge case tests"

### Week 3: Integration & Validation
- [ ] Extend `tests/test_integration_acts_runner.py` (3 tests)
- [ ] Extend `tests/test_integration_ccm_analyzer.py` (3 tests)
- [ ] Run full coverage analysis, validate 70%+ reached
- [ ] Generate coverage report: `pytest --cov-report=html`
- [ ] Commit with message: "test: complete Sprint 1 coverage improvements (55% → 70%)"

## Success Criteria

- [ ] Overall coverage ≥ 70%
- [ ] All critical modules (agents, environment, runner) ≥ 85%
- [ ] All tests pass: `pytest tests/ -v` (100% pass rate)
- [ ] Reproducibility validated: `python scripts/verify_reproducibility.py`
- [ ] Type safety: `mypy src/ --strict` (0 errors)
- [ ] Linting: `flake8 src/ --max-line-length=100` (0 errors)

## Deferred Scope (Future Sprints)

### Low-Priority Modules (Keep as-is for now)
- `visualization.py` (4%): Requires snapshot testing infrastructure
- `network_enhanced.py` (0%): Experimental, unstable API
- `enhanced_runner.py` (0%): Experimental, conference validation only
- `conference_parameters.py` (0%): Configuration file, no logic to test
- `orchestrator.py` (20%): Integration layer, test after stabilization

### Rationale
These modules are either:
1. **Plotting code** (hard to test without visual regression framework)
2. **Experimental features** (API still in flux)
3. **Configuration data** (no executable logic)

Focus Sprint 1 on **core simulation logic** that directly impacts research validity.

## Notes

### Pre-commit Hook Integration
After Sprint 1, add coverage gate to `.pre-commit-config.yaml`:
```yaml
- repo: local
  hooks:
    - id: pytest-coverage
      name: pytest-coverage
      entry: pytest
      args: [--cov=src/acp_simulation, --cov-fail-under=70]
      language: system
      pass_filenames: false
```

### CI/CD Integration
Update `.github/workflows/ci.yml` to enforce coverage:
```yaml
- name: Run tests with coverage
  run: |
    pytest tests/ --cov=src/acp_simulation --cov-report=term-missing --cov-fail-under=70

- name: Upload coverage to Codecov
  uses: codecov/codecov-action@v4
  with:
    file: ./coverage.xml
    fail_ci_if_error: true
```

---
**Document Version**: 1.0
**Last Updated**: 2026-01-07
**Owner**: ACP Simulation Development Team
**Next Review**: After Sprint 1 completion
