"""
Pytest configuration and fixtures for ACP simulation tests.
"""

import sys
import os
from pathlib import Path
import tempfile
import pytest

# Add src directory to Python path for testing
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))


@pytest.fixture
def temp_output_dir():
    """Create temporary output directory for tests"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


def pytest_addoption(parser):
    """Add command-line options for JAR file paths"""
    # Default to local JAR files in repository
    default_acts_jar = os.path.join(
        os.path.dirname(__file__),
        "..",
        "external",
        "acts",
        "acts_3.1.jar"
    )
    
    parser.addoption(
        "--acts-jar",
        action="store",
        default=os.environ.get("ACTS_JAR_PATH", default_acts_jar),
        help="Path to ACTS jar file"
    )
    parser.addoption(
        "--ccm-jar",
        action="store",
        default=os.environ.get("CCM_JAR_PATH", ""),
        help="Path to CCM jar file"
    )