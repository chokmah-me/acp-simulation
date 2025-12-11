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
            
            # Run ACTS - ACTS 3.1 syntax: java [options] -jar jarName <inputFileName> [outputFileName]
            cmd = [
                'java',
                f'-Ddoi={strength}',
                f'-Dalgo={algorithm}',
                '-Doutput=csv',  # Output in CSV format for easy parsing
                '-jar', str(self.acts_jar_path),
                input_file,
                output_file
            ]
            
            # Debug: print command
            print(f"Running ACTS command: {' '.join(cmd)}")
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                raise RuntimeError(f"ACTS failed: {result.stderr}")
            
            # Read covering array - ACTS CSV format
            try:
                # Try reading as CSV first
                covering_array = pd.read_csv(output_file)
            except pd.errors.ParserError:
                # If that fails, try reading as plain text and split
                with open(output_file, 'r') as f:
                    lines = f.readlines()
                
                # Find the header line (starts with "Test Case" or similar)
                header_line = None
                data_start = 0
                for i, line in enumerate(lines):
                    if 'Test Case' in line or 'p1' in line:
                        header_line = line.strip()
                        data_start = i + 1
                        break
                
                if header_line is None:
                    # Try to parse as simple CSV without header
                    data = []
                    for line in lines:
                        if line.strip() and not line.startswith('#'):
                            data.append(line.strip().split(','))
                    
                    if data:
                        covering_array = pd.DataFrame(data[1:], columns=data[0])
                    else:
                        raise RuntimeError("Could not parse ACTS output")
                else:
                    # Parse with header
                    data = []
                    for line in lines[data_start:]:
                        if line.strip() and not line.startswith('#'):
                            data.append(line.strip().split(','))
                    
                    covering_array = pd.DataFrame(data, columns=header_line.split(','))
            
            # Clean up the DataFrame (remove any empty rows/columns)
            covering_array = covering_array.dropna(how='all')
            if len(covering_array) == 0:
                raise RuntimeError("ACTS produced empty covering array")
            
            # Convert column names to match parameter names
            covering_array.columns = [param.name for param in parameters]
            
            # Convert data types based on parameter types
            for param in parameters:
                if param.param_type == "int":
                    covering_array[param.name] = pd.to_numeric(covering_array[param.name], errors='coerce').astype('Int64')
                elif param.param_type == "double":
                    covering_array[param.name] = pd.to_numeric(covering_array[param.name], errors='coerce').astype(float)
                # enum and boolean stay as strings
            
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