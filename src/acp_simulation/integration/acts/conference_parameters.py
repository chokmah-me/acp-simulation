"""
Enhanced ACTS parameters for conference validation.

Extends the base ACP parameters to include:
- Enterprise network topologies (hub-spoke, hierarchical)
- Topology-aware vulnerability distributions
- Topology-specific constraints

This configuration supports comprehensive validation of the conference abstract claims:
"Optimistic models trained against realistic variance outperform pessimistic models"
"""

try:
    from .generator import ACTSParameter, ACTSConstraint
except ImportError:
    # For direct execution
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
    from src.acp_simulation.integration.acts.generator import ACTSParameter, ACTSConstraint


# Enhanced parameter space for conference validation
CONFERENCE_ACP_PARAMETERS = [
    # Core ACP parameters
    ACTSParameter("acp_strength", "double", [0.3, 0.5, 0.7, 0.9]),
    ACTSParameter("learning_rate", "double", [0.5, 1.0, 1.5, 2.0]),
    # Network configuration
    ACTSParameter("num_nodes", "int", [50, 100, 200, 500]),
    ACTSParameter("connectivity", "double", [0.3, 0.5, 0.7]),
    # NEW: Enterprise network topologies for conference
    ACTSParameter(
        "topology_type", "enum", ["erdos_renyi", "barabasi_albert", "hub_spoke", "hierarchical"]
    ),
    # NEW: Topology-aware vulnerability distributions
    ACTSParameter(
        "vulnerability_dist", "enum", ["uniform", "normal", "exponential", "bimodal", "gradient"]
    ),
    # Experimental parameters
    ACTSParameter("confidence_level", "double", [0.90, 0.95, 0.99]),
    ACTSParameter("num_episodes", "int", [1000, 5000, 10000]),
]


# Enhanced constraints for realistic enterprise validation
CONFERENCE_ACP_CONSTRAINTS = [
    # Computational constraints
    ACTSConstraint("(num_nodes = 500) => (num_episodes <= 5000)"),
    ACTSConstraint("(confidence_level = 0.99) => (num_episodes >= 5000)"),
    # Topology-specific constraints for enterprise realism
    # Hub-spoke requires minimum connectivity to ensure hubs are connected
    ACTSConstraint('(topology_type = "hub_spoke") => (connectivity >= 0.3)'),
    # Hierarchical scales poorly above 200 nodes (tree depth issues)
    ACTSConstraint('(topology_type = "hierarchical") => (num_nodes <= 200)'),
    # Gradient vulnerability only makes sense for structured topologies
    ACTSConstraint(
        '(vulnerability_dist = "gradient") => '
        '((topology_type = "hub_spoke") || (topology_type = "hierarchical"))'
    ),
    # Bimodal distribution is most realistic for hub-spoke (secure servers, vulnerable endpoints)
    # This is a soft constraint - not enforced but recommended
    # ACTSConstraint("(topology_type = \"hub_spoke\") => (vulnerability_dist != \"uniform\")"),
]


# Expected coverage with 3-way interaction strength:
# - Base parameters (without topology): ~85 tests
# - Enhanced parameters (with topology): ~150-200 tests (estimated)
# - Still achieves >99% reduction vs exhaustive (4×4×4×5×4×3×3 = 11,520)


def get_conference_parameter_count() -> dict:
    """
    Get parameter space size for conference configuration.

    Returns
    -------
    dict
        Parameter statistics
    """
    total_combinations = 1
    param_info = {}

    for param in CONFERENCE_ACP_PARAMETERS:
        count = len(param.values)
        param_info[param.name] = count
        total_combinations *= count

    return {
        "parameters": param_info,
        "total_combinations": total_combinations,
        "estimated_3way_tests": 200,  # Conservative estimate
        "reduction_factor": total_combinations / 200,
    }


if __name__ == "__main__":
    # Print parameter space summary
    info = get_conference_parameter_count()
    print("Conference ACP Parameter Space Summary")
    print("=" * 50)
    print(f"\nParameters:")
    for name, count in info["parameters"].items():
        print(f"  {name}: {count} values")

    print(f"\nTotal exhaustive combinations: {info['total_combinations']:,}")
    print(f"Estimated 3-way covering array: ~{info['estimated_3way_tests']} tests")
    print(f"Reduction factor: {info['reduction_factor']:.1f}x")
    print(
        f"Coverage: {(1 - info['estimated_3way_tests']/info['total_combinations'])*100:.2f}% reduction"
    )
