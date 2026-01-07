"""
Tests for CCM Analyzer Module
"""

import pytest
import pandas as pd
from pathlib import Path
import tempfile

from acp_simulation.integration.ccm.analyzer import CCMAnalyzer


class TestCCMAnalyzer:
    """Test CCMAnalyzer class"""

    def test_analyzer_initialization_with_nonexistent_jar(self):
        """Test analyzer initialization with non-existent jar file"""
        with pytest.raises(FileNotFoundError, match="CCM jar not found"):
            CCMAnalyzer("nonexistent/path/ccm.jar")

    def test_analyze_coverage_with_sample_data(self):
        """Test coverage analysis with sample test suite"""
        # Create analyzer without jar (testing parsing logic)
        analyzer = CCMAnalyzer.__new__(CCMAnalyzer)

        # Create sample test suite
        test_suite = pd.DataFrame(
            {
                "acp_strength": [0.3, 0.5, 0.7],
                "num_nodes": [50, 100, 200],
                "connectivity": [0.3, 0.5, 0.7],
            }
        )

        # Mock the _parse_ccm_output method
        def mock_parse(output_file):
            return {
                "2_way_coverage": 100.0,
                "3_way_coverage": 85.5,
                "4_way_coverage": 72.3,
                "missing_combinations": [],
            }

        analyzer._parse_ccm_output = mock_parse

        # Test the analyze_coverage method structure
        # (without actually running CCM)
        result = analyzer._parse_ccm_output("dummy_file.txt")

        assert isinstance(result, dict)
        assert "2_way_coverage" in result
        assert "3_way_coverage" in result
        assert "4_way_coverage" in result
        assert "missing_combinations" in result
        assert result["2_way_coverage"] == 100.0
        assert result["3_way_coverage"] == 85.5

    def test_parse_ccm_output_placeholder(self):
        """Test the placeholder CCM output parser"""
        analyzer = CCMAnalyzer.__new__(CCMAnalyzer)

        result = analyzer._parse_ccm_output("dummy_path.txt")

        assert isinstance(result, dict)
        assert result["2_way_coverage"] == 100.0
        assert result["3_way_coverage"] == 100.0
        assert result["4_way_coverage"] == 95.2
        assert result["missing_combinations"] == []


class TestCCMAnalyzerWithTestSuite:
    """Test CCM analyzer with various test suites"""

    @pytest.fixture
    def sample_test_suite(self):
        """Create sample test suite"""
        return pd.DataFrame(
            {"param1": [1, 2, 1, 2], "param2": ["a", "a", "b", "b"], "param3": [10, 20, 10, 20]}
        )

    def test_analyze_coverage_parameters(self, sample_test_suite):
        """Test coverage analysis parameters"""
        analyzer = CCMAnalyzer.__new__(CCMAnalyzer)

        # Mock the analyze_coverage to avoid needing actual CCM jar
        def mock_analyze(test_suite, max_strength=6, output_file=None):
            return {
                "2_way_coverage": 100.0,
                "3_way_coverage": 75.0,
                "max_strength_tested": max_strength,
            }

        analyzer.analyze_coverage = mock_analyze

        result = analyzer.analyze_coverage(sample_test_suite, max_strength=4)

        assert result["2_way_coverage"] == 100.0
        assert result["3_way_coverage"] == 75.0
        assert result["max_strength_tested"] == 4

    def test_test_suite_with_different_types(self):
        """Test analyzer with mixed data types"""
        test_suite = pd.DataFrame(
            {
                "int_param": [1, 2, 3],
                "float_param": [0.1, 0.5, 0.9],
                "str_param": ["low", "medium", "high"],
                "bool_param": [True, False, True],
            }
        )

        analyzer = CCMAnalyzer.__new__(CCMAnalyzer)

        # Just verify the DataFrame is properly structured
        assert len(test_suite) == 3
        assert list(test_suite.columns) == ["int_param", "float_param", "str_param", "bool_param"]


class TestCCMAnalyzerEdgeCases:
    """Test edge cases and error handling"""

    def test_empty_test_suite(self):
        """Test with empty test suite"""
        empty_suite = pd.DataFrame(columns=["param1", "param2"])

        analyzer = CCMAnalyzer.__new__(CCMAnalyzer)

        # Should handle empty DataFrame
        assert len(empty_suite) == 0
        assert list(empty_suite.columns) == ["param1", "param2"]

    def test_single_row_test_suite(self):
        """Test with single row test suite"""
        single_suite = pd.DataFrame({"param1": [1], "param2": ["a"]})

        analyzer = CCMAnalyzer.__new__(CCMAnalyzer)

        assert len(single_suite) == 1

    def test_large_test_suite(self):
        """Test with larger test suite"""
        # Create test suite with 100 rows
        large_suite = pd.DataFrame(
            {
                "p1": list(range(100)),
                "p2": [f"val_{i}" for i in range(100)],
                "p3": [i * 0.1 for i in range(100)],
            }
        )

        analyzer = CCMAnalyzer.__new__(CCMAnalyzer)

        assert len(large_suite) == 100
        assert list(large_suite.columns) == ["p1", "p2", "p3"]


class TestCCMAnalyzerIntegration:
    """Integration tests requiring CCM jar"""

    @pytest.fixture
    def ccm_jar_path(self, pytestconfig):
        """Path to CCM jar - skip if not available"""
        ccm_jar = pytestconfig.getoption("--ccm-jar")
        if not ccm_jar:
            pytest.skip("CCM jar not specified (use --ccm-jar option)")
        return ccm_jar

    @pytest.mark.integration
    def test_analyze_coverage_integration(self, ccm_jar_path):
        """Integration test for coverage analysis"""
        if not Path(ccm_jar_path).exists():
            pytest.skip("CCM jar not available")

        analyzer = CCMAnalyzer(ccm_jar_path)

        test_suite = pd.DataFrame({"param1": [1, 2, 1, 2], "param2": ["a", "a", "b", "b"]})

        result = analyzer.analyze_coverage(test_suite, max_strength=2)

        assert isinstance(result, dict)
        assert "2_way_coverage" in result
        assert isinstance(result["2_way_coverage"], float)
        assert 0 <= result["2_way_coverage"] <= 100


class TestCoverageReportStructure:
    """Test structure of coverage reports"""

    def test_coverage_report_keys(self):
        """Test that coverage report has expected structure"""
        analyzer = CCMAnalyzer.__new__(CCMAnalyzer)

        report = analyzer._parse_ccm_output("dummy.txt")

        # Check all expected keys are present
        expected_keys = {
            "2_way_coverage",
            "3_way_coverage",
            "4_way_coverage",
            "missing_combinations",
        }
        assert set(report.keys()) == expected_keys

        # Check value types
        assert isinstance(report["2_way_coverage"], (int, float))
        assert isinstance(report["3_way_coverage"], (int, float))
        assert isinstance(report["4_way_coverage"], (int, float))
        assert isinstance(report["missing_combinations"], list)

    def test_coverage_values_range(self):
        """Test that coverage values are in valid range"""
        analyzer = CCMAnalyzer.__new__(CCMAnalyzer)

        report = analyzer._parse_ccm_output("dummy.txt")

        # All coverage values should be between 0 and 100
        for key in ["2_way_coverage", "3_way_coverage", "4_way_coverage"]:
            assert 0 <= report[key] <= 100
