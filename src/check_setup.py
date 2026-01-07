"""
Dependency Checker for ACP Simulation
Checks if all required packages are installed
"""

import sys


def check_dependencies():
    """Check if all required packages are available"""

    print("=" * 70)
    print("ACP SIMULATION - DEPENDENCY CHECKER")
    print("=" * 70)
    print()

    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")
    print()

    packages = {"numpy": "1.20.0", "scipy": "1.7.0", "networkx": "2.6.0", "matplotlib": "3.4.0"}

    print("Checking required packages...")
    print("-" * 70)

    missing = []
    installed = []

    for package, min_version in packages.items():
        try:
            mod = __import__(package)
            version = getattr(mod, "__version__", "unknown")
            print(f"[OK] {package:15s} {version:15s} (minimum: {min_version})")
            installed.append(package)
        except ImportError:
            print(f"[MISSING] {package:15s} NOT INSTALLED")
            missing.append(package)

    print("-" * 70)
    print()

    if missing:
        print("[WARNING] MISSING PACKAGES DETECTED")
        print()
        print("To install missing packages, run:")
        print()
        print(f"    pip install {' '.join(missing)}")
        print()
        print("Or install all at once:")
        print()
        print("    pip install numpy scipy networkx matplotlib")
        print()
        print("If 'pip' is not recognized, try:")
        print()
        print("    python -m pip install numpy scipy networkx matplotlib")
        print()
        return False
    else:
        print("[SUCCESS] ALL PACKAGES INSTALLED SUCCESSFULLY!")
        print()
        print("You can now run:")
        print()
        print("    python acp_corrected_final.py           (100 episodes)")
        print("    python acp_parallel_power_analysis.py   (1,000 episodes)")
        print()
        return True


if __name__ == "__main__":
    success = check_dependencies()
    sys.exit(0 if success else 1)
