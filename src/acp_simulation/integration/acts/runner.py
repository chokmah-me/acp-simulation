"""
ACTS Test Runner

Executes ACP simulations from ACTS-generated covering arrays.
"""

import pandas as pd
from pathlib import Path
from typing import Dict, List, Any, Optional
import time
import json

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
    parameters: Optional[List] = None,
    constraints: Optional[List] = None
) -> List[Dict[str, Any]]:
    """
    Run complete ACTS-based ACP experiment.
    
    One-stop function that generates covering array and runs all tests.
    """
    # Import here to avoid circular dependency
    from .generator import ACTSGenerator, ACP_PARAMETERS
    
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