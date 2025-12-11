# Post-Refactoring Implementation Plan

## Overview

**Timeline**: 2-3 weeks  
**5 Major Phases**: CLI → Tests → Performance → Docs → Release

This plan outlines the steps to transform the refactored ACP simulation codebase into a production-ready Python package suitable for PyPI distribution, research publication, and community use.

---

## Phase 6: CLI Scripts (2-3 days)

### Objective
Create command-line interfaces for easy execution of ACP simulations without writing Python code.

### Deliverables
- `scripts/run_acp.py` - Main CLI for running experiments
- `scripts/parameter_sweep.py` - CLI for parameter sensitivity analysis
- Updated `setup.py` with entry points
- Comprehensive help documentation and examples

### Key Features
- **Argument parsing**: Full argparse implementation with all configuration options
- **Progress reporting**: Real-time progress bars and status updates
- **Output formats**: Support for PNG, PKL, JSON output formats
- **Parallel execution**: Automatic parallelization for large experiments
- **Configuration files**: Load experiments from JSON/YAML config files

### Example Usage
```bash
# Basic experiment
acp-sim --episodes 1000 --acp-strength 0.8

# Parameter sweep
acp-sweep --parameter acp_strength --values 0.3,0.5,0.7,0.9

# Load from config
acp-sim --config experiments/standard.json
```

### Success Criteria
- ✅ All arguments properly validated
- ✅ Help text comprehensive with examples
- ✅ Exit codes appropriate for scripting
- ✅ Output files properly formatted and saved

---

## Phase 7: Comprehensive Testing (4-5 days)

### Objective
Expand test coverage to >90% and add integration tests for complete validation.

### Current State
- **29 tests** covering core modules (100% core coverage)
- All tests passing

### Target State
- **70+ tests** covering all modules
- **>90% overall coverage**
- Integration tests for end-to-end validation
- Performance benchmarks

### New Test Files

#### `tests/test_agents.py` (15-20 tests)
- **CognitiveAttacker**: IBLT activation, memory poisoning, learning
- **PessimisticDefender**: RESTORE_NODE usage, action selection
- **OptimisticACPDefender**: Deception deployment, information asymmetry
- **Configurable variants**: Parameter handling, inheritance

#### `tests/test_environment.py` (10-15 tests)
- **Network generation**: Erdős-Rényi, Barabási-Albert models
- **Action execution**: All action types (SCAN, EXPLOIT, PATCH, etc.)
- **Reward calculation**: Attacker and defender rewards
- **State transitions**: Node state changes, termination conditions
- **Cognitive latency**: Window implementation, exploitation

#### `tests/test_analysis.py` (12-18 tests)
- **Power analysis**: Statistical power calculation, effect sizes
- **Bootstrap CI**: Confidence interval accuracy, convergence
- **Visualization**: Figure generation, plot correctness
- **Result aggregation**: Episode collection, metric calculation

#### `tests/test_simulation_runner.py` (+8-10 tests)
- **Parallel execution**: Multi-processing, seed management
- **Edge cases**: Single episode, zero nodes, maximum steps
- **Error handling**: Invalid configurations, network failures
- **Reproducibility**: Deterministic results with same seed

#### `tests/test_integration.py` (5-8 tests)
- **End-to-end**: Full experiment execution and validation
- **Statistical validation**: p-values, effect sizes match expectations
- **Publication quality**: Figure generation, result packaging

### Infrastructure
- **pytest fixtures**: Common configurations, network setups
- **pytest-cov**: Coverage reporting and tracking
- **pytest-benchmark**: Performance regression testing
- **hypothesis**: Property-based testing for edge cases

### Success Criteria
- ✅ >90% code coverage (measured with pytest-cov)
- ✅ All integration tests pass
- ✅ Performance benchmarks established
- ✅ No flaky tests (100% reproducible)

---

## Phase 8: Performance Optimization (3-4 days)

### Objective
Achieve 500+ episodes/second throughput (currently ~200-300).

### Profiling Strategy
1. **Baseline measurement**: Profile current performance
2. **Identify bottlenecks**: Focus on hot loops and functions
3. **Optimize systematically**: Apply vectorization, caching, compilation
4. **Validate correctness**: Ensure results unchanged after optimization

### Optimization Targets

#### 1. IBLT Activation (High Priority)
**Current**: Loop over memory instances for each decision
**Optimization**: Vectorize activation calculation using NumPy
**Expected gain**: 3-5x speedup in attacker decision-making

```python
# Before: Loop-based
activations = [self.activation(inst, time) for inst in memories]

# After: Vectorized
time_diffs = time - np.array([inst.timestamp for inst in memories])
activations = np.log(np.maximum(time_diffs ** (-self.decay_rate), 1e-10))
```

#### 2. Network Operations (Medium Priority)
**Current**: Repeated NetworkX queries during episode execution
**Optimization**: Cache neighbor lookups and network properties
**Expected gain**: 2-3x speedup in action execution

#### 3. Batch Episode Processing (Medium Priority)
**Current**: Each episode has Python overhead
**Optimization**: Process multiple episodes in vectorized batches
**Expected gain**: 1.5-2x speedup for large experiments

#### 4. Numba JIT Compilation (Low Priority)
**Current**: Pure Python execution
**Optimization**: Compile hotspots with `@numba.jit`
**Expected gain**: 5-10x speedup in compiled functions

### Profiling Tools
- **cProfile**: Function-level timing analysis
- **line_profiler**: Line-by-line execution time
- **memory_profiler**: Memory usage tracking
- **py-spy**: Sampling profiler for production

### Success Criteria
- ✅ 500+ episodes/second on standard hardware
- ✅ <5% overhead for parallel execution
- ✅ Memory usage <1GB for 10,000 episodes
- ✅ Results identical to unoptimized version (validated with fixed seeds)

---

## Phase 9: Documentation (3-4 days)

### Objective
Create comprehensive documentation for researchers, developers, and users.

### Deliverables

#### 1. README.md Updates
- **Quick start**: Installation and first experiment
- **Python API**: Code examples using new package structure
- **CLI usage**: Command-line examples
- **Migration guide**: From v3.x to v4.0

#### 2. docs/API_REFERENCE.md
- **Auto-generated**: From NumPy-style docstrings
- **Class hierarchy**: Inheritance diagrams (using pyreverse)
- **Parameter tables**: All configuration options
- **Example code**: For each major class/function

#### 3. docs/EXAMPLES.md
- **10+ complete examples**:
  - Basic experiment
  - Parameter sensitivity analysis
  - Large-scale simulation (100,000 episodes)
  - Custom agent implementation
  - Visualization customization
  - Parallel execution
  - Statistical validation workflow
  - Publication figure generation
  - Reproducibility checklist
  - Performance optimization

#### 4. CHANGELOG.md
- **v4.0.0 release notes**: Breaking changes, new features, bug fixes
- **Migration guide**: Step-by-step upgrade instructions
- **Acknowledgments**: Contributors, references

#### 5. Jupyter Notebooks
- **Tutorial notebook**: Interactive introduction
- **Research notebook**: Complete analysis workflow
- **Validation notebook**: Reproducibility demonstration

### Documentation Quality
- **Sphinx**: Professional documentation generation
- **Read the Docs**: Hosted documentation
- **Type hints**: Leveraged for API documentation
- **Examples**: All code tested and runnable

### Success Criteria
- ✅ README provides clear quick start
- ✅ API reference complete and accurate
- ✅ All examples tested and working
- ✅ Hosted documentation live

---

## Phase 10: Release (1-2 days)

### Objective
Release v4.0.0 to PyPI and GitHub for public distribution.

### Release Checklist

#### Pre-Release Validation
- [ ] All tests pass (pytest)
- [ ] Type checking clean (mypy --strict)
- [ ] Linting passes (flake8)
- [ ] Documentation builds (sphinx)
- [ ] Version numbers consistent
- [ ] CHANGELOG.md updated
- [ ] README.md updated

#### Build and Upload
```bash
# Build distribution packages
python setup.py sdist bdist_wheel

# Upload to Test PyPI
twine upload --repository testpypi dist/*

# Test installation
pip install --index-url https://test.pypi.org/simple/ acp-simulation

# Upload to Production PyPI
twine upload dist/*
```

#### GitHub Release
- [ ] Create release from tag v4.0.0
- [ ] Upload distribution packages
- [ ] Write release notes with highlights
- [ ] Link to documentation
- [ ] Add example code snippets

#### Post-Release
- [ ] Monitor PyPI download statistics
- [ ] Respond to initial issues
- [ ] Update project status badge
- [ ] Announce on relevant channels (Twitter, LinkedIn, research groups)

### Success Metrics
- ✅ Package installable from PyPI
- ✅ All examples work with installed package
- ✅ Documentation accessible
- ✅ No critical issues in first week

---

## Timeline Summary

| Phase | Duration | Key Activities | Deliverables |
|-------|----------|----------------|--------------|
| **Phase 6: CLI** | 2-3 days | Argument parsing, progress reporting, output formats | 2 CLI scripts, entry points |
| **Phase 7: Tests** | 4-5 days | Write 40+ tests, integration tests, coverage tracking | >90% coverage, no flaky tests |
| **Phase 8: Performance** | 3-4 days | Profile, vectorize, cache, compile | 500+ ep/s throughput |
| **Phase 9: Docs** | 3-4 days | API docs, examples, notebooks, changelog | Complete documentation |
| **Phase 10: Release** | 1-2 days | Build, upload, GitHub release, monitoring | v4.0.0 on PyPI |

**Total Timeline**: 2-3 weeks (13-18 working days)

---

## Resource Requirements

### Personnel
- **1 developer** for CLI, testing, performance (Phases 6-8)
- **1 technical writer** for documentation (Phase 9)
- **1 release manager** for PyPI and GitHub (Phase 10)

### Tools and Services
- **pytest-cov**: Coverage tracking
- **Sphinx**: Documentation generation
- **Read the Docs**: Documentation hosting
- **GitHub Actions**: CI/CD pipeline
- **PyPI**: Package distribution
- **line_profiler**: Performance profiling

### Budget Considerations
- **Time**: 2-3 weeks of focused development
- **Compute**: Profiling and benchmarking resources
- **Services**: Read the Docs hosting (free for open source)

---

## Risk Mitigation

### Risk 1: Performance targets not met
**Mitigation**: 
- Set intermediate goals (300, 400, 500 ep/s)
- Focus on highest-impact optimizations first
- Consider alternative approaches (Cython, JAX) if needed

### Risk 2: Test coverage takes longer than expected
**Mitigation**:
- Prioritize critical paths first
- Use property-based testing to reduce manual test writing
- Accept 85% coverage if 90% proves too time-consuming

### Risk 3: Documentation incomplete at release
**Mitigation**:
- Start documentation early (parallel with Phase 8)
- Focus on API reference first (auto-generated)
- Release with "beta" documentation status if needed

### Risk 4: PyPI release issues
**Mitigation**:
- Test with Test PyPI first
- Have backup maintainer with PyPI access
- Prepare offline installation instructions

---

## Success Metrics

### Code Quality
- **Test Coverage**: >90%
- **Type Coverage**: 100%
- **Cyclomatic Complexity**: <10 per function
- **Lines per File**: <500 (most files)

### Performance
- **Throughput**: 500+ episodes/second
- **Memory**: <1GB for 10,000 episodes
- **Parallel Efficiency**: >85% scaling

### Documentation
- **API Coverage**: 100% public APIs documented
- **Examples**: 10+ working examples
- **User Guide**: Complete quick start

### Release
- **PyPI Downloads**: >100 in first month
- **GitHub Stars**: +50
- **Issues**: <5 critical in first week

---

## Conclusion

This plan provides a clear, actionable roadmap to transform the refactored ACP simulation codebase into a production-ready Python package. Each phase builds on the previous work, ensuring systematic progress toward the goal of a maintainable, well-documented, high-performance package suitable for research, publication, and community use.

The modular architecture established in Phases 1-5 provides a solid foundation for these implementation phases, with clear separation of concerns making each phase relatively independent and testable.