#!/usr/bin/env python3
"""
ACTS Combinatorial Testing CLI

Run ACP simulations with NIST ACTS-generated test suites.
"""

import argparse
import sys
from pathlib import Path

from acp_simulation.integration.orchestrator import CombinatorialTestingOrchestrator


def main():
    parser = argparse.ArgumentParser(
        description='Run ACP simulations with NIST ACTS combinatorial testing',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate and run 2-way covering array (quick test)
  python run_acts.py --strength 2 --acts-jar /path/to/acts.jar --ccm-jar /path/to/ccm.jar
  
  # Generate 3-way covering array without execution
  python run_acts.py --strength 3 --no-execute --acts-jar /path/to/acts.jar
  
  # Full workflow with custom output directory
  python run_acts.py --strength 3 --output-dir ./my_results --acts-jar /path/to/acts.jar --ccm-jar /path/to/ccm.jar
        """
    )
    
    parser.add_argument(
        '--strength',
        type=int,
        default=3,
        help='Interaction strength (2-way, 3-way, etc.) [default: 3]'
    )
    
    parser.add_argument(
        '--acts-jar',
        required=True,
        help='Path to ACTS jar file'
    )
    
    parser.add_argument(
        '--ccm-jar',
        required=True,
        help='Path to CCM jar file'
    )
    
    parser.add_argument(
        '--output-dir',
        default='./combinatorial_results',
        help='Output directory [default: ./combinatorial_results]'
    )
    
    parser.add_argument(
        '--no-execute',
        action='store_true',
        help='Generate covering array only, do not execute tests'
    )
    
    parser.add_argument(
        '--no-analyze',
        action='store_true',
        help='Execute tests only, do not analyze coverage with CCM'
    )
    
    args = parser.parse_args()
    
    # Validate jar files
    if not Path(args.acts_jar).exists():
        print(f"Error: ACTS jar not found: {args.acts_jar}", file=sys.stderr)
        sys.exit(1)
    
    if not Path(args.ccm_jar).exists():
        print(f"Error: CCM jar not found: {args.ccm_jar}", file=sys.stderr)
        sys.exit(1)
    
    # Run workflow
    print(f"\n{'='*70}")
    print(f"ACP Simulation + NIST ACTS/CCM Integration")
    print(f"{'='*70}")
    print(f"Strength: {args.strength}-way")
    print(f"ACTS: {args.acts_jar}")
    print(f"CCM: {args.ccm_jar}")
    print(f"Output: {args.output_dir}")
    print()
    
    orchestrator = CombinatorialTestingOrchestrator(
        acts_jar_path=args.acts_jar,
        ccm_jar_path=args.ccm_jar,
        output_dir=args.output_dir
    )
    
    results = orchestrator.run_full_workflow(
        strength=args.strength,
        execute_tests=not args.no_execute,
        analyze_coverage=not args.no_analyze
    )
    
    print(f"\n✅ Workflow complete!")
    print(f"Results: {args.output_dir}/combinatorial_testing_results.json")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())