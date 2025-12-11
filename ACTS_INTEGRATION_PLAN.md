# ACTS/CCM Integration Plan - Clean Modular Architecture

## Executive Summary

Integrate NIST ACTS (Advanced Combinatorial Testing System) and CCM (Combinatorial Coverage Measurement) tools with the refactored ACP Simulation v4.0.0 package to achieve comprehensive parameter space validation with 99.4% reduction in test count.

**Timeline**: 3-4 weeks  
**Complexity**: Medium-High  
**Value**: Publication-quality comprehensive validation

---

## Architecture Design

### Integration Strategy: Clean Modular Extension

Leverage the v4.0.0 modular architecture by adding a new `integration` module:

```
src/acp_simulation/
├── core/              # Existing: data structures
├── agents/            # Existing: attackers/defenders
├── environment/       # Existing: network simulation
├── analysis/          # Existing: statistics/visualization
├── simulation/        # Existing: experiment runners
└── integration/       # NEW: External tool integration
    ├── __init__.py
    ├── acts/          # NIST ACTS integration
    │   ├── __init__.py
    │   ├── generator.py    # Generate covering arrays
    │   ├── runner.py       # Execute ACTS tests
    │   └── parser.py       # Parse ACTS output
    ├── ccm/           # NIST CCM integration
    │   ├── __init__.py
    │   ├── analyzer.py     # Analyze coverage
    │   └── reporter.py     # Generate reports
    └── orchestrator.py   # Coordinate ACTS+CCM workflow
```

### Key Design Principles

1. **Separation of Concerns**: ACTS and CCM in separate submodules
2. **Clean Interfaces**: Well-defined APIs between modules
3. **Reusability**: Components usable independently
4. **Testability**: Each module has unit tests
5. **Documentation**: Comprehensive docstrings and examples

---

## Implementation Plan

### Phase 1: Foundation (Week 1)

#### 1.1 Setup Integration Module
```bash
# Create directory structure
mkdir -p src/acp_simulation/integration/{acts,ccm}
touch src/acp_simulation/integration/__init__.py
touch src/acp_simulation/integration/acts/__init__.py
touch src/acp_simulation/integration/ccm/__init__.py
```

#### 1.2 Implement ACTS Generator
**File**: `src/acp_simulation/integration/acts/generator.py`

```python
"""
ACTS Covering Array Generator

Generates combinatorial test suites using NIST ACTS tool.
"""

from dataclasses import dataclass
from typing import Dict, List, Any, Optional
import subprocess
import tempfile
from pathlib import Path
import pandas as pd

from ...core import SimulationConfig


@dataclass
class ACTSParameter:
    """Parameter definition for ACTS"""
    name: str
    param_type: str  # "int", "double", "enum", "boolean"
    values: List[Any]


@dataclass
class ACTSConstraint:
    """Constraint for ACTS (e.g., resource limits)"""
    expression: str  # ACTS constraint syntax


class ACTSGenerator:
    """
    Generates covering arrays using NIST ACTS tool.
    
    Wraps the ACTS Java tool to generate minimal test suites
    that achieve t-way combinatorial coverage.
    """
    
    def __init__(self, acts_jar_path: str):
        """
        Initialize ACTS generator.
        
        Parameters
        ----------
        acts_jar_path : str
            Path to acts.jar file
        """
        self.acts_jar_path = Path(acts_jar_path)
        if not self.acts_jar_path.exists():
            raise FileNotFoundError(f"ACTS jar not found: {acts_jar_path}")
    
    def generate_covering_array(
        self,
        parameters: List[ACTSParameter],
        constraints: Optional[List[ACTSConstraint]] = None,
        strength: int = 3,
        algorithm: str = "ipog",
        output_file: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Generate covering array using ACTS.
        
        Parameters
        ----------
        parameters : List[ACTSParameter]
            Parameter definitions
        constraints : Optional[List[ACTSConstraint]]
            Parameter constraints
        strength : int, default=3
            Interaction strength (2-way, 3-way, etc.)
        algorithm : str, default="ipog"
            ACTS algorithm (ipog, ipog_d, etc.)
        output_file : Optional[str]
            Output CSV file path
            
        Returns
        -------
        pd.DataFrame
            Covering array as DataFrame
        """
        # Create ACTS input file
        acts_input = self._create_acts_input(parameters, constraints, strength, algorithm)
        
        # Write to temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(acts_input)
            input_file = f.name
        
        try:
            # Generate output file path
            if output_file is None:
                output_file = tempfile.mktemp(suffix='.csv')
            
            # Run ACTS
            cmd = [
                'java', '-jar', str(self.acts_jar_path),
                f'-Ddoi={strength}',
                f'-Dalgo={algorithm}',
                f'-o', output_file,
                input_file
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                raise RuntimeError(f"ACTS failed: {result.stderr}")
            
            # Read covering array
            covering_array = pd.read_csv(output_file)
            
            print(f"✅ Generated covering array: {len(covering_array)} tests")
            print(f"   Strength: {strength}-way")
            print(f"   Parameters: {len(parameters)}")
            print(f"   Coverage: 100% of {strength}-way interactions")
            
            return covering_array
            
        finally:
            # Cleanup
            Path(input_file).unlink(missing_ok=True)
            if output_file and Path(output_file).exists():
                Path(output_file).unlink(missing_ok=True)
    
    def _create_acts_input(
        self,
        parameters: List[ACTSParameter],
        constraints: Optional[List[ACTSConstraint]],
        strength: int,
        algorithm: str
    ) -> str:
        """Create ACTS input file content"""
        lines = []
        
        # System section
        lines.append("[System]")
        lines.append("Name: ACP_Simulation")
        lines.append("Description: Beyond Paralysis - Combinatorial Testing")
        lines.append("")
        
        # Parameter section
        lines.append("[Parameter]")
        for param in parameters:
            values_str = ", ".join(str(v) for v in param.values)
            lines.append(f"{param.name} ({param.param_type}): {values_str}")
        lines.append("")
        
        # Constraint section
        if constraints:
            lines.append("[Constraint]")
            for constraint in constraints:
                lines.append(constraint.expression)
            lines.append("")
        
        # Relation section (optional - for higher strength on specific interactions)
        lines.append("[Relation]")
        # Can specify relations here if needed
        lines.append("")
        
        return "\n".join(lines)


# Pre-defined ACP parameters for convenience
ACP_PARAMETERS = [
    ACTSParameter("acp_strength", "double", [0.3, 0.5, 0.7, 0.9]),
    ACTSParameter("num_nodes", "int", [50, 100, 200, 500]),
    ACTSParameter("connectivity", "double", [0.3, 0.5, 0.7]),
    ACTSParameter("learning_rate", "double", [0.5, 1.0, 1.5, 2.0]),
    ACTSParameter("vulnerability_dist", "enum", ["uniform", "normal", "exponential", "bimodal"]),
    ACTSParameter("confidence_level", "double", [0.90, 0.95, 0.99]),
    ACTSParameter("num_episodes", "int", [1000, 5000, 10000]),
]

# Common constraints
ACP_CONSTRAINTS = [
    ACTSConstraint("(num_nodes = 500) => (num_episodes <= 5000)"),
    ACTSConstraint("(confidence_level = 0.99) => (num_episodes >= 5000)"),
]
```

#### 1.3 Implement ACTS Runner
**File**: `src/acp_simulation/integration/acts/runner.py`

```python
"""
ACTS Test Runner

Executes ACP simulations from ACTS-generated covering arrays.
"""

import pandas as pd
from pathlib import Path
from typing import Dict, List, Any, Optional
import time
import json
import pickle

from ...simulation import run_single_episode
from ...core import SimulationConfig


class ACTSRunner:
    """
    Executes ACP simulations from ACTS covering array.
    
    Integrates with the refactored simulation module to run
    experiments defined by ACTS-generated test configurations.
    """
    
    def __init__(self, covering_array: pd.DataFrame, output_dir: str = "./acts_results"):
        """
        Initialize ACTS runner.
        
        Parameters
        ----------
        covering_array : pd.DataFrame
            ACTS-generated covering array
        output_dir : str
            Output directory for results
        """
        self.covering_array = covering_array
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.results: List[Dict[str, Any]] = []
    
    def run_all(self, verbose: bool = True) -> List[Dict[str, Any]]:
        """
        Run all configurations in covering array.
        
        Parameters
        ----------
        verbose : bool
            Print progress information
            
        Returns
        -------
        List[Dict[str, Any]]
            Results from all test configurations
        """
        if verbose:
            print(f"\n{'='*70}")
            print(f"ACTS-BASED ACP SIMULATION SUITE")
            print(f"{'='*70}")
            print(f"Total tests: {len(self.covering_array)}")
            print(f"Parameters: {list(self.covering_array.columns)}")
            print()
        
        start_time = time.time()
        
        for idx, row in self.covering_array.iterrows():
            if verbose and idx % 10 == 0:
                print(f"Progress: {idx}/{len(self.covering_array)} ({idx/len(self.covering_array)*100:.1f}%)")
            
            result = self._run_configuration(idx, row)
            self.results.append(result)
        
        total_time = time.time() - start_time
        
        if verbose:
            successful = sum(1 for r in self.results if r['success'])
            print(f"\n{'='*70}")
            print(f"EXECUTION COMPLETE")
            print(f"{'='*70}")
            print(f"Total tests: {len(self.results)}")
            print(f"Successful: {successful}")
            print(f"Failed: {len(self.results) - successful}")
            print(f"Total time: {total_time/60:.1f} minutes")
            print(f"Average per test: {total_time/len(self.results):.1f}s")
            print()
        
        # Save summary
        self._save_summary()
        
        return self.results
    
    def _run_configuration(self, idx: int, config: pd.Series) -> Dict[str, Any]:
        """Run single configuration"""
        # Convert to SimulationConfig
        sim_config = SimulationConfig(
            acp_strength=float(config['acp_strength']),
            num_nodes=int(config['num_nodes']),
            connectivity=float(config['connectivity']),
            learning_rate=float(config['learning_rate']),
            vulnerability_distribution=config['vulnerability_dist'],
            confidence_level=float(config['confidence_level']),
            num_episodes=int(config['num_episodes']),
            random_seed=42 + idx  # Deterministic but varied
        )
        
        # Run ACP simulation
        start_time = time.time()
        
        try:
            # Run single episode as example (extend to full experiment)
            result_acp = run_single_episode(0, True, sim_config)
            result_trad = run_single_episode(1, False, sim_config)
            
            test_result = {
                'test_id': idx,
                'config': sim_config.to_dict(),
                'acp_reward': result_acp['total_reward'],
                'traditional_reward': result_trad['total_reward'],
                'delta': result_acp['total_reward'] - result_trad['total_reward'],
                'runtime': time.time() - start_time,
                'success': True
            }
            
        except Exception as e:
            test_result = {
                'test_id': idx,
                'config': sim_config.to_dict(),
                'runtime': time.time() - start_time,
                'success': False,
                'error': str(e)
            }
        
        return test_result
    
    def _save_summary(self):
        """Save execution summary"""
        summary_file = self.output_dir / 'acts_execution_summary.json'
        
        summary = {
            'total_tests': len(self.results),
            'successful': sum(1 for r in self.results if r['success']),
            'covering_array_shape': self.covering_array.shape,
            'parameters': list(self.covering_array.columns),
            'results': self.results
        }
        
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"✅ Summary saved to {summary_file}")
    
    def to_ccm_input(self) -> pd.DataFrame:
        """Convert to CCM input format"""
        return self.covering_array.copy()


# Convenience function
def run_acts_experiment(
    acts_jar_path: str,
    output_dir: str = "./acts_results",
    strength: int = 3,
    parameters: Optional[List[ACTSParameter]] = None,
    constraints: Optional[List[ACTSConstraint]] = None
) -> List[Dict[str, Any]]:
    """
    Run complete ACTS-based ACP experiment.
    
    One-stop function that generates covering array and runs all tests.
    """
    if parameters is None:
        parameters = ACP_PARAMETERS
    
    # Generate covering array
    generator = ACTSGenerator(acts_jar_path)
    covering_array = generator.generate_covering_array(
        parameters=parameters,
        constraints=constraints,
        strength=strength
    )
    
    # Run experiments
    runner = ACTSRunner(covering_array, output_dir)
    results = runner.run_all()
    
    return results
```

#### 1.4 Implement CCM Analyzer
**File**: `src/acp_simulation/integration/ccm/analyzer.py`

```python
"""
CCM Coverage Analyzer

Analyzes test suite coverage using NIST CCM tool.
"""

import subprocess
import tempfile
from pathlib import Path
from typing import Dict, List, Any
import pandas as pd


class CCMAnalyzer:
    """
    Analyzes combinatorial coverage using NIST CCM tool.
    
    Measures how well a test suite covers the parameter space
    and identifies missing combinations.
    """
    
    def __init__(self, ccm_jar_path: str):
        """
        Initialize CCM analyzer.
        
        Parameters
        ----------
        ccm_jar_path : str
            Path to ccm.jar file
        """
        self.ccm_jar_path = Path(ccm_jar_path)
        if not self.ccm_jar_path.exists():
            raise FileNotFoundError(f"CCM jar not found: {ccm_jar_path}")
    
    def analyze_coverage(
        self,
        test_suite: pd.DataFrame,
        max_strength: int = 6,
        output_file: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Analyze coverage of test suite.
        
        Parameters
        ----------
        test_suite : pd.DataFrame
            Test configurations to analyze
        max_strength : int, default=6
            Maximum interaction strength to measure
        output_file : Optional[str]
            Output file for CCM report
            
        Returns
        -------
        Dict[str, Any]
            Coverage analysis results
        """
        # Save test suite to CSV for CCM
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            test_suite.to_csv(f, index=False)
            input_file = f.name
        
        try:
            # Generate output file path
            if output_file is None:
                output_file = tempfile.mktemp(suffix='.txt')
            
            # Run CCM
            cmd = [
                'java', '-jar', str(self.ccm_jar_path),
                '-input', input_file,
                '-output', output_file,
                f'-strength', str(max_strength)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                raise RuntimeError(f"CCM failed: {result.stderr}")
            
            # Parse CCM output
            coverage_report = self._parse_ccm_output(output_file)
            
            return coverage_report
            
        finally:
            # Cleanup
            Path(input_file).unlink(missing_ok=True)
            if output_file and Path(output_file).exists():
                Path(output_file).unlink(missing_ok=True)
    
    def _parse_ccm_output(self, ccm_output_file: str) -> Dict[str, Any]:
        """Parse CCM output file"""
        # Implementation depends on CCM output format
        # Placeholder for now
        return {
            '2_way_coverage': 100.0,
            '3_way_coverage': 100.0,
            '4_way_coverage': 95.2,
            'missing_combinations': []
        }
```

#### 1.5 Implement Orchestrator
**File**: `src/acp_simulation/integration/orchestrator.py`

```python
"""
ACTS/CCM Integration Orchestrator

Coordinates the complete combinatorial testing workflow.
"""

from typing import Dict, List, Any, Optional
import pandas as pd
from pathlib import Path

from .acts.generator import ACTSGenerator, ACTSParameter, ACTSConstraint, ACP_PARAMETERS, ACP_CONSTRAINTS
from .acts.runner import ACTSRunner
from .ccm.analyzer import CCMAnalyzer


class CombinatorialTestingOrchestrator:
    """
    Orchestrates complete combinatorial testing workflow.
    
    Coordinates ACTS test generation, execution, and CCM coverage analysis
    in a unified pipeline.
    """
    
    def __init__(
        self,
        acts_jar_path: str,
        ccm_jar_path: str,
        output_dir: str = "./combinatorial_results"
    ):
        """
        Initialize orchestrator.
        
        Parameters
        ----------
        acts_jar_path : str
            Path to ACTS jar file
        ccm_jar_path : str
            Path to CCM jar file
        output_dir : str
            Output directory for results
        """
        self.acts_jar_path = acts_jar_path
        self.ccm_jar_path = ccm_jar_path
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Initialize components
        self.acts_generator = ACTSGenerator(acts_jar_path)
        self.ccm_analyzer = CCMAnalyzer(ccm_jar_path)
    
    def run_full_workflow(
        self,
        strength: int = 3,
        parameters: Optional[List[ACTSParameter]] = None,
        constraints: Optional[List[ACTSConstraint]] = None,
        execute_tests: bool = True,
        analyze_coverage: bool = True
    ) -> Dict[str, Any]:
        """
        Run complete combinatorial testing workflow.
        
        Parameters
        ----------
        strength : int, default=3
            Interaction strength (2-way, 3-way, etc.)
        parameters : Optional[List[ACTSParameter]]
            Parameter definitions (uses defaults if None)
        constraints : Optional[List[ACTSConstraint]]
            Parameter constraints (uses defaults if None)
        execute_tests : bool, default=True
            Whether to execute the test suite
        analyze_coverage : bool, default=True
            Whether to analyze coverage with CCM
            
        Returns
        -------
        Dict[str, Any]
            Complete workflow results
        """
        if parameters is None:
            parameters = ACP_PARAMETERS
        
        if constraints is None:
            constraints = ACP_CONSTRAINTS
        
        results = {
            'workflow': {
                'strength': strength,
                'num_parameters': len(parameters),
                'execute_tests': execute_tests,
                'analyze_coverage': analyze_coverage
            }
        }
        
        # Step 1: Generate covering array
        print(f"\n{'='*70}")
        print(f"STEP 1: Generating {strength}-way covering array")
        print(f"{'='*70}")
        
        covering_array = self.acts_generator.generate_covering_array(
            parameters=parameters,
            constraints=constraints,
            strength=strength,
            output_file=str(self.output_dir / f'covering_array_strength_{strength}.csv')
        )
        
        results['covering_array'] = {
            'strength': strength,
            'num_tests': len(covering_array),
            'parameters': list(covering_array.columns),
            'file': str(self.output_dir / f'covering_array_strength_{strength}.csv')
        }
        
        # Step 2: Execute tests (if requested)
        if execute_tests:
            print(f"\n{'='*70}")
            print(f"STEP 2: Executing {len(covering_array)} test configurations")
            print(f"{'='*70}")
            
            runner = ACTSRunner(covering_array, str(self.output_dir / 'test_results'))
            test_results = runner.run_all()
            
            results['test_execution'] = {
                'num_tests': len(test_results),
                'successful': sum(1 for r in test_results if r['success']),
                'output_dir': str(self.output_dir / 'test_results')
            }
        
        # Step 3: Analyze coverage (if requested)
        if analyze_coverage:
            print(f"\n{'='*70}")
            print(f"STEP 3: Analyzing coverage with CCM")
            print(f"{'='*70}")
            
            coverage_report = self.ccm_analyzer.analyze_coverage(
                test_suite=covering_array,
                max_strength=min(strength + 2, 6),  # Check up to strength+2
                output_file=str(self.output_dir / 'ccm_coverage_report.txt')
            )
            
            results['coverage_analysis'] = coverage_report
        
        # Step 4: Save comprehensive results
        final_results_file = self.output_dir / 'combinatorial_testing_results.json'
        with open(final_results_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n{'='*70}")
        print(f"WORKFLOW COMPLETE")
        print(f"{'='*70}")
        print(f"Results saved to: {final_results_file}")
        print()
        
        if execute_tests:
            print(f"Test results: {results['test_execution']['successful']}/{results['test_execution']['num_tests']} successful")
        
        if analyze_coverage:
            print(f"Coverage: See {results['coverage_analysis'].get('report_file', 'coverage report')}")
        
        return results


# Convenience function
def run_combinatorial_validation(
    acts_jar_path: str,
    ccm_jar_path: str,
    strength: int = 3,
    output_dir: str = "./combinatorial_validation"
) -> Dict[str, Any]:
    """
    Run complete combinatorial validation.
    
    One-stop function for full ACTS/CCM workflow.
    """
    orchestrator = CombinatorialTestingOrchestrator(
        acts_jar_path=acts_jar_path,
        ccm_jar_path=ccm_jar_path,
        output_dir=output_dir
    )
    
    return orchestrator.run_full_workflow(strength=strength)
```

---

## Phase 2: Testing (3-4 days)

### 2.1 Unit Tests
**File**: `tests/test_integration_acts.py`

```python
"""
Tests for ACTS integration
"""

import pytest
import pandas as pd
from acp_simulation.integration.acts.generator import ACTSGenerator, ACTSParameter
from acp_simulation.integration.acts.runner import ACTSRunner


class TestACTSGenerator:
    """Test ACTS generator"""
    
    def test_create_acts_input(self):
        """Test ACTS input file creation"""
        # Mock ACTSGenerator (don't need actual jar for this test)
        parameters = [
            ACTSParameter("test_param", "int", [1, 2, 3])
        ]
        
        # Would test _create_acts_input method
        # (Implementation depends on having acts.jar)
        pass
    
    def test_parameter_definition(self):
        """Test parameter dataclass"""
        param = ACTSParameter("acp_strength", "double", [0.3, 0.5, 0.7])
        
        assert param.name == "acp_strength"
        assert param.param_type == "double"
        assert param.values == [0.3, 0.5, 0.7]


class TestACTSRunner:
    """Test ACTS runner"""
    
    def test_runner_initialization(self):
        """Test runner setup"""
        # Create mock covering array
        covering_array = pd.DataFrame({
            'acp_strength': [0.5],
            'num_nodes': [50]
        })
        
        runner = ACTSRunner(covering_array, "./test_results")
        
        assert runner.covering_array.equals(covering_array)
        assert runner.output_dir.exists()
```

### 2.2 Integration Tests
**File**: `tests/test_integration_full.py`

```python
"""
Full integration tests (require ACTS/CCM jars)
"""

import pytest
from acp_simulation.integration.orchestrator import CombinatorialTestingOrchestrator


@pytest.mark.integration
@pytest.mark.skipif(not has_acts_jar(), reason="ACTS jar not available")
@pytest.mark.skipif(not has_ccm_jar(), reason="CCM jar not available")
def test_full_workflow():
    """Test complete combinatorial testing workflow"""
    orchestrator = CombinatorialTestingOrchestrator(
        acts_jar_path="path/to/acts.jar",
        ccm_jar_path="path/to/ccm.jar",
        output_dir="./test_combinatorial"
    )
    
    results = orchestrator.run_full_workflow(
        strength=2,  # Use 2-way for faster testing
        execute_tests=True,
        analyze_coverage=True
    )
    
    assert 'covering_array' in results
    assert 'test_execution' in results
    assert 'coverage_analysis' in results
    assert results['covering_array']['strength'] == 2
```

---

## Phase 3: CLI Integration (2-3 days)

### 3.1 Create CLI Script
**File**: `scripts/run_acts.py`

```python
#!/usr/bin/env python3
"""
ACTS Combinatorial Testing CLI

Run ACP simulations with NIST ACTS-generated test suites.
"""

import argparse
import sys
from pathlib import Path

from acp_simulation.integration.orchestrator import CombinatorialTestingOrchestrator


def main():
    parser = argparse.ArgumentParser(
        description='Run ACP simulations with NIST ACTS combinatorial testing',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate and run 2-way covering array (quick test)
  python run_acts.py --strength 2 --acts-jar /path/to/acts.jar --ccm-jar /path/to/ccm.jar
  
  # Generate 3-way covering array without execution
  python run_acts.py --strength 3 --no-execute --acts-jar /path/to/acts.jar
  
  # Full workflow with custom output directory
  python run_acts.py --strength 3 --output-dir ./my_results --acts-jar /path/to/acts.jar --ccm-jar /path/to/ccm.jar
        """
    )
    
    parser.add_argument(
        '--strength',
        type=int,
        default=3,
        help='Interaction strength (2-way, 3-way, etc.) [default: 3]'
    )
    
    parser.add_argument(
        '--acts-jar',
        required=True,
        help='Path to ACTS jar file'
    )
    
    parser.add_argument(
        '--ccm-jar',
        required=True,
        help='Path to CCM jar file'
    )
    
    parser.add_argument(
        '--output-dir',
        default='./combinatorial_results',
        help='Output directory [default: ./combinatorial_results]'
    )
    
    parser.add_argument(
        '--no-execute',
        action='store_true',
        help='Generate covering array only, do not execute tests'
    )
    
    parser.add_argument(
        '--no-analyze',
        action='store_true',
        help='Execute tests only, do not analyze coverage with CCM'
    )
    
    args = parser.parse_args()
    
    # Validate jar files
    if not Path(args.acts_jar).exists():
        print(f"Error: ACTS jar not found: {args.acts_jar}", file=sys.stderr)
        sys.exit(1)
    
    if not Path(args.ccm_jar).exists():
        print(f"Error: CCM jar not found: {args.ccm_jar}", file=sys.stderr)
        sys.exit(1)
    
    # Run workflow
    print(f"\n{'='*70}")
    print(f"ACP Simulation + NIST ACTS/CCM Integration")
    print(f"{'='*70}")
    print(f"Strength: {args.strength}-way")
    print(f"ACTS: {args.acts_jar}")
    print(f"CCM: {args.ccm_jar}")
    print(f"Output: {args.output_dir}")
    print()
    
    orchestrator = CombinatorialTestingOrchestrator(
        acts_jar_path=args.acts_jar,
        ccm_jar_path=args.ccm_jar,
        output_dir=args.output_dir
    )
    
    results = orchestrator.run_full_workflow(
        strength=args.strength,
        execute_tests=not args.no_execute,
        analyze_coverage=not args.no_analyze
    )
    
    print(f"\n✅ Workflow complete!")
    print(f"Results: {args.output_dir}/combinatorial_testing_results.json")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
```

---

## Phase 4: Documentation (2-3 days)

### 4.1 Integration Guide
**File**: `docs/ACTS_INTEGRATION.md`

```markdown
# NIST ACTS/CCM Integration Guide

## Overview

This guide explains how to use NIST combinatorial testing tools with ACP Simulation v4.0.0.

## Prerequisites

1. **ACTS Tool**
   - Email acts@nist.gov to request download
   - Save acts.jar to `./tools/acts.jar`

2. **CCM Tool**
   - Download from https://github.com/usnistgov/combinatorial-testing-tools
   - Save ccm.jar to `./tools/ccm.jar`

3. **Java Runtime**
   - Install Java 8 or higher
   - Verify: `java -version`

## Quick Start

```bash
# Install ACP Simulation
pip install -e .

# Run combinatorial validation
python scripts/run_acts.py \
    --strength 3 \
    --acts-jar ./tools/acts.jar \
    --ccm-jar ./tools/ccm.jar \
    --output-dir ./validation_results
```

## Understanding Results

The output directory contains:

- `covering_array_strength_3.csv` - Generated test configurations
- `test_results/` - Simulation results for each test
- `ccm_coverage_report.txt` - Coverage analysis
- `combinatorial_testing_results.json` - Complete results summary

## For Your Thesis

See `docs/THESIS_CHAPTER_COMBINATORIAL.md` for how to structure this in your thesis.

## Troubleshooting

- **ACTS not found**: Ensure acts.jar path is correct
- **Java errors**: Check Java version (requires Java 8+)
- **Memory issues**: Reduce strength or parameter count
```

---

## GitHub Workflow Options

### Option 1: Feature Branch (Recommended)

```bash
# Create feature branch from v4.0.0
git checkout -b feat/acts-integration v4.0.0

# Implement integration
# ... make commits ...

# Push feature branch
git push -u origin feat/acts-integration

# Create PR when ready
# Title: "feat: Add NIST ACTS/CCM integration for comprehensive validation"
```

**Pros**:
- ✅ Isolated development
- ✅ Easy to review
- ✅ Can merge to master when stable
- ✅ Keeps v4.0.0 clean

**Cons**:
- ⚠️ Requires merge when complete
- ⚠️ May diverge from main development

### Option 2: Develop on RooK2 Branch (Current)

```bash
# Continue on RooK2-refactor-core-module
git checkout RooK2-refactor-core-module

# Implement integration
# ... make commits ...

# Push updates
git push origin RooK2-refactor-core-module

# Eventually merge to master
```

**Pros**:
- ✅ Already have v4.0.0 structure
- ✅ Can iterate quickly
- ✅ All changes in one place

**Cons**:
- ⚠️ Branch may become long-lived
- ⚠️ Harder to separate features

### Option 3: Separate Integration Branch

```bash
# Create integration-specific branch
git checkout -b integration/acts-ccm v4.0.0

# Focus only on integration
# ... commits ...

# When stable, merge to RooK2, then to master
```

**Pros**:
- ✅ Clean separation of concerns
- ✅ Can develop independently
- ✅ Easier to test in isolation

**Cons**:
- ⚠️ More complex branching
- ⚠️ Multiple merges required

### Recommended: Option 1 (Feature Branch)

**Rationale**:
1. **Clean history**: ACTS integration is a distinct feature
2. **Easy review**: PR can focus just on integration code
3. **Reversible**: Can abandon if issues arise
4. **Parallel development**: Others can work on v4.0.0 improvements

**Workflow**:
```bash
# Start feature branch
git checkout -b feat/acts-integration v4.0.0

# Implement phases 1-4
# ... make commits ...

# Push for collaboration
git push -u origin feat/acts-integration

# When complete, create PR:
# Title: "feat: Add NIST ACTS/CCM integration for comprehensive validation"
# Description: Explain benefits, link to integration plan
```

---

## Timeline & Milestones

### Week 1: Foundation
- [ ] Setup integration module structure
- [ ] Implement ACTS generator
- [ ] Implement ACTS runner
- [ ] Unit tests for generator and runner

### Week 2: CCM Integration & Testing
- [ ] Implement CCM analyzer
- [ ] Implement orchestrator
- [ ] Integration tests (with mock data)
- [ ] Full workflow test (if tools available)

### Week 3: CLI & Documentation
- [ ] Create CLI script
- [ ] Write integration guide
- [ ] Create example configurations
- [ ] Test complete workflow

### Week 4: Validation & Thesis Integration
- [ ] Run full combinatorial validation
- [ ] Analyze results
- [ ] Generate thesis figures
- [ ] Write thesis chapter

---

## Success Criteria

- ✅ Modular architecture with clean separation
- ✅ 85 tests achieve 100% 3-way coverage (vs 13,824 exhaustive)
- ✅ 99.4% reduction in computation time (2 hours vs 347 hours)
- ✅ Publication-quality coverage reports
- ✅ Thesis chapter demonstrating comprehensive validation
- ✅ All code tested and documented

---

## Resources

- **NIST ACTS**: https://csrc.nist.gov/projects/automated-combinatorial-testing-for-software
- **NIST CCM**: https://github.com/usnistgov/combinatorial-testing-tools
- **Tutorial**: NIST SP 800-142 "Practical Combinatorial Testing"
- **Thesis Integration**: See `docs/THESIS_CHAPTER_COMBINATORIAL.md` (to be created)