"""
CCM Coverage Analyzer

Analyzes test suite coverage using NIST CCM tool.
"""

import subprocess
import tempfile
from pathlib import Path
from typing import Dict, List, Any, Optional
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
        # Placeholder for now - will need to adapt based on actual CCM output
        return {
            '2_way_coverage': 100.0,
            '3_way_coverage': 100.0,
            '4_way_coverage': 95.2,
            'missing_combinations': []
        }