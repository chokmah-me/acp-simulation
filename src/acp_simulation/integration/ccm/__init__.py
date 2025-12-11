"""
NIST CCM Integration Module

Integration with NIST Combinatorial Coverage Measurement (CCM)
for analyzing test suite coverage and identifying missing combinations.
"""

from .analyzer import CCMAnalyzer

__all__ = [
    'CCMAnalyzer'
]