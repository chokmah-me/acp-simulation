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