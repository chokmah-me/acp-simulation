"""
Setup script for ACP Simulation package.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="acp-simulation",
    version="4.0.0",
    author="dyb",
    description="Asymmetric Cognitive Projection (ACP) Simulation for cybersecurity defense validation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dyb5784/acp-simulation",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Security",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
            "mypy>=1.0",
            "flake8>=5.0",
            "black>=22.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "acp-sim=acp_simulation.scripts.run_acp:main",
        ],
    },
)