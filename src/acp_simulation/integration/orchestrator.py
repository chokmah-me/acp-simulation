"""
ACTS/CCM Integration Orchestrator

Coordinates the complete combinatorial testing workflow.
"""

from typing import Dict, List, Any, Optional
import pandas as pd
from pathlib import Path
import json

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