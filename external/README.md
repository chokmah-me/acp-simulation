# External Dependencies

This directory contains third-party JAR files and documentation required for integration tests.

## Files

### ACTS (Advanced Combinatorial Testing System)
- `acts/acts_3.1.jar` - NIST ACTS tool for combinatorial testing (version 3.1)
- `acts/acts_user_guide_3.1.pdf` - Official ACTS 3.1 user guide and documentation

### CCM (Combinatorial Coverage Measurement)
- `ccm/CCM17.jar` - Combinatorial Coverage Measurement tool (version 17)

## Setup

These files enable integration tests for combinatorial testing features. Both JAR files are now included in the repository.

### Included Files

- **ACTS 3.1**: Already included at `external/acts/acts_3.1.jar`
- **CCM 17**: Already included at `external/ccm/CCM17.jar`
- **Documentation**: ACTS user guide included

No additional downloads are required for running integration tests.

### Overriding JAR Paths

To use custom JAR locations:

```bash
# Using command-line options
python -m pytest tests/ --acts-jar="/path/to/acts.jar" --ccm-jar="/path/to/ccm.jar"

# Or set environment variables
export ACTS_JAR_PATH=/path/to/acts.jar
export CCM_JAR_PATH=/path/to/ccm.jar
python -m pytest tests/
```

## Test Integration

The pytest configuration in `tests/conftest.py` automatically detects these JAR files and configures tests to use them. Integration tests will skip gracefully if JAR files are not found.

## References

- ACTS User Guide: See `acts/acts_user_guide_3.1.pdf` for detailed usage instructions
- ACTS Official Site: https://csrc.nist.gov/Projects/automated-combinatorial-testing-for-software
- CCM Repository: https://github.com/dyb5784/combinatorial-testing-tools