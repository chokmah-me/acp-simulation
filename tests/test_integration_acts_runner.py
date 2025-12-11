"""
Tests for ACTS Runner Module
"""

import pytest
import pandas as pd
from pathlib import Path
import tempfile
import json

from acp_simulation.integration.acts.runner import ACTSRunner
from acp_simulation.core import SimulationConfig


class TestACTSRunner:
    """Test ACTSRunner class"""
    
    @pytest.fixture
    def sample_covering_array(self):
        """Create sample covering array for testing"""
        return pd.DataFrame({
            'acp_strength': [0.5, 0.7],
            'num_nodes': [50, 100],
            'connectivity': [0.5, 0.7],
            'learning_rate': [1.0, 1.5],
            'vulnerability_dist': ['uniform', 'normal'],
            'confidence_level': [0.95, 0.99],
            'num_episodes': [1000, 5000]
        })
    
    @pytest.fixture
    def temp_output_dir(self):
        """Create temporary output directory"""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)
    
    def test_runner_initialization(self, sample_covering_array, temp_output_dir):
        """Test runner initialization"""
        runner = ACTSRunner(sample_covering_array, str(temp_output_dir))
        
        assert runner.covering_array.equals(sample_covering_array)
        assert runner.output_dir.exists()
        assert runner.output_dir == temp_output_dir
        assert runner.results == []
    
    def test_run_configuration_conversion(self, sample_covering_array, temp_output_dir):
        """Test configuration conversion from DataFrame to SimulationConfig"""
        runner = ACTSRunner(sample_covering_array, str(temp_output_dir))
        
        # Test first configuration
        config_series = sample_covering_array.iloc[0]
        result = runner._run_configuration(0, config_series)
        
        assert 'test_id' in result
        assert result['test_id'] == 0
        assert 'config' in result
        assert 'runtime' in result
        assert 'success' in result
        
        # Check config was properly converted
        config_dict = result['config']
        assert config_dict['acp_strength'] == 0.5
        assert config_dict['num_nodes'] == 50
        assert config_dict['connectivity'] == 0.5
        assert config_dict['learning_rate'] == 1.0
        assert config_dict['vulnerability_distribution'] == 'uniform'
        assert config_dict['confidence_level'] == 0.95
        assert config_dict['num_episodes'] == 1000
    
    def test_run_configuration_types(self, sample_covering_array, temp_output_dir):
        """Test that configuration values have correct types"""
        runner = ACTSRunner(sample_covering_array, str(temp_output_dir))
        
        config_series = sample_covering_array.iloc[0]
        result = runner._run_configuration(0, config_series)
        
        config_dict = result['config']
        
        # Check types
        assert isinstance(config_dict['acp_strength'], float)
        assert isinstance(config_dict['num_nodes'], int)
        assert isinstance(config_dict['connectivity'], float)
        assert isinstance(config_dict['learning_rate'], float)
        assert isinstance(config_dict['vulnerability_distribution'], str)
        assert isinstance(config_dict['confidence_level'], float)
        assert isinstance(config_dict['num_episodes'], int)
    
    def test_save_summary_creates_file(self, sample_covering_array, temp_output_dir):
        """Test that summary file is created"""
        runner = ACTSRunner(sample_covering_array, str(temp_output_dir))
        
        # Add some mock results
        runner.results = [
            {
                'test_id': 0,
                'config': {'acp_strength': 0.5},
                'runtime': 1.5,
                'success': True
            },
            {
                'test_id': 1,
                'config': {'acp_strength': 0.7},
                'runtime': 1.8,
                'success': False,
                'error': 'Simulation failed'
            }
        ]
        
        runner._save_summary()
        
        summary_file = temp_output_dir / 'acts_execution_summary.json'
        assert summary_file.exists()
        
        # Check file content
        with open(summary_file, 'r') as f:
            summary = json.load(f)
        
        assert summary['total_tests'] == 2
        assert summary['successful'] == 1
        assert summary['covering_array_shape'] == [2, 7]  # 2 rows, 7 columns
        assert len(summary['results']) == 2
    
    def test_to_ccm_input(self, sample_covering_array, temp_output_dir):
        """Test conversion to CCM input format"""
        runner = ACTSRunner(sample_covering_array, str(temp_output_dir))
        
        ccm_input = runner.to_ccm_input()
        
        assert isinstance(ccm_input, pd.DataFrame)
        assert ccm_input.equals(sample_covering_array)
        assert list(ccm_input.columns) == list(sample_covering_array.columns)


class TestACTSRunnerEdgeCases:
    """Test edge cases and error handling"""
    
    def test_empty_covering_array(self, temp_output_dir):
        """Test with empty covering array"""
        empty_array = pd.DataFrame(columns=[
            'acp_strength', 'num_nodes', 'connectivity', 'learning_rate',
            'vulnerability_dist', 'confidence_level', 'num_episodes'
        ])
        
        runner = ACTSRunner(empty_array, str(temp_output_dir))
        results = runner.run_all(verbose=False)
        
        assert results == []
        assert runner.results == []
    
    def test_single_configuration(self, temp_output_dir):
        """Test with single configuration"""
        single_array = pd.DataFrame({
            'acp_strength': [0.5],
            'num_nodes': [50],
            'connectivity': [0.5],
            'learning_rate': [1.0],
            'vulnerability_dist': ['uniform'],
            'confidence_level': [0.95],
            'num_episodes': [1000]
        })
        
        runner = ACTSRunner(single_array, str(temp_output_dir))
        
        # Mock the run_configuration to avoid actual simulation
        original_run_config = runner._run_configuration
        runner._run_configuration = lambda idx, row: {
            'test_id': idx,
            'config': {'mock': True},
            'runtime': 1.0,
            'success': True
        }
        
        results = runner.run_all(verbose=False)
        
        assert len(results) == 1
        assert results[0]['test_id'] == 0
        assert results[0]['success'] is True
    
    def test_missing_columns_in_covering_array(self, temp_output_dir):
        """Test handling of covering array with missing columns"""
        incomplete_array = pd.DataFrame({
            'acp_strength': [0.5],
            'num_nodes': [50]
            # Missing other required columns
        })
        
        runner = ACTSRunner(incomplete_array, str(temp_output_dir))
        
        # Should handle missing columns gracefully (may raise KeyError during execution)
        with pytest.raises((KeyError, AttributeError)):
            config_series = incomplete_array.iloc[0]
            runner._run_configuration(0, config_series)


class TestRunACTSExperiment:
    """Test the convenience function run_acts_experiment"""
    
    def test_function_signature(self):
        """Test function exists with correct signature"""
        from acp_simulation.integration.acts.runner import run_acts_experiment
        
        # Should be callable
        assert callable(run_acts_experiment)
        
        # Should have required parameters
        import inspect
        sig = inspect.signature(run_acts_experiment)
        params = list(sig.parameters.keys())
        
        assert 'acts_jar_path' in params
        assert 'output_dir' in params
        assert 'strength' in params
    
    @pytest.mark.integration
    def test_run_experiment_integration(self):
        """Integration test for run_acts_experiment (requires ACTS jar)"""
        # This would require actual ACTS jar and would be slow
        # Marked as integration test to be skipped by default
        pytest.skip("Integration test requiring ACTS jar")