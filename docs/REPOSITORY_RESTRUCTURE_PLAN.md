# 🏗️ ACP Simulation Repository Restructure Plan

## Current Status (Phase 1 Complete)
✅ **v2.0-stable branch created** - Legacy code preserved
✅ **Directory structure started** - src/, docs/, examples/ created
✅ **v3.0 code moved** - Python files consolidated in src/

## Phase 2: Clean Structure Implementation

### Step 2.1: Move Documentation to docs/
```bash
# Move all markdown documentation
move *.md docs\
move v3-Claude-Windows-Parameters-Scaled-agents-ACP-simulation\*.md docs\
```

### Step 2.2: Move Examples to examples/
```bash
# Create example configurations
mkdir examples\configs
mkdir examples\results

# Move any example files
# (Create sample config files here)
```

### Step 2.3: Clean Root Directory
```bash
# Remove zip archives (use GitHub releases instead)
del *.zip

# Remove binaries (use GitHub releases)
del mininet-vm.ova
del cdf_comparison.png

# Remove duplicate v2 directories (preserved in v2.0-stable branch)
rmdir /s /q v2-Claude-WindowsSetup-1000-scaled-agents-ACP-simulation
rmdir /s /q v2-Claude-WindowsSetup-1000-scaled-agents-ACP-simulation-branch
rmdir /s /q v3-Claude-Windows-Parameters-Scaled-agents-ACP-simulation
```

### Step 2.4: Update Imports and Paths
```python
# In src/acp_fully_configurable.py
# Change: sys.path.insert(0, '.')
# To: sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Update all file references to use relative paths
```

## Phase 3: GitHub Releases Setup

### Step 3.1: Create GitHub Releases for Binaries
1. Go to GitHub repository → Releases → Draft new release
2. Create releases:
   - **v2.0.0**: Include v2-Claude-WindowsSetup-1000-scaled-agents-ACP-simulation.zip
   - **v3.0.0**: Include v3-Claude-Windows-Parameters-Scaled-agents-ACP-simulation.zip
   - **Binaries**: Include mininet-vm.ova, cdf_comparison.png

### Step 3.2: Tag Current Versions
```bash
git tag -a v3.0.0 -m "Version 3.0: Fully configurable ACP simulation"
git push origin v3.0.0
```

## Phase 4: CI/CD Pipeline Setup

### Step 4.1: Create GitHub Actions Workflow
Create `.github/workflows/ci.yml`:

```yaml
name: CI

on:
  push:
    branches: [ master, develop ]
  pull_request:
    branches: [ master ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, 3.10, 3.11]

    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Run setup check
      run: python src/check_setup.py
    
    - name: Run quick test
      run: python src/acp_corrected_final.py
    
    - name: Run configurable test
      run: python src/acp_fully_configurable.py --num-episodes 100

  lint:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: 3.11
    - name: Install linting tools
      run: pip install flake8 black
    - name: Run flake8
      run: flake8 src/ --count --select=E9,F63,F7,F82 --show-source --statistics
    - name: Check black formatting
      run: black --check src/
```

### Step 4.2: Add Dependabot
Create `.github/dependabot.yml`:

```yaml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
```

## Phase 5: Repository Modernization

### Step 5.1: Add Contribution Guidelines
Create `CONTRIBUTING.md`:

```markdown
# Contributing to ACP Simulation

## Development Setup
1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/acp-simulation.git`
3. Install dependencies: `pip install -r requirements.txt`
4. Run tests: `python src/check_setup.py`

## Pull Request Process
1. Create feature branch: `git checkout -b feature/your-feature`
2. Make changes and test
3. Run linting: `flake8 src/`
4. Submit pull request with description

## Code Style
- Follow PEP 8
- Use black for formatting
- Add docstrings for new functions
- Update documentation for new features
```

### Step 5.2: Add Issue Templates
Create `.github/ISSUE_TEMPLATE/bug_report.md` and `.github/ISSUE_TEMPLATE/feature_request.md`

### Step 5.3: Update README with Badges
Add to README.md:
```markdown
[![CI](https://github.com/dyb5784/acp-simulation/actions/workflows/ci.yml/badge.svg)](https://github.com/dyb5784/acp-simulation/actions/workflows/ci.yml)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-3.0.0-brightgreen.svg)](https://github.com/dyb5784/acp-simulation/releases/tag/v3.0.0)
```

## Final Clean Structure

```
acp-simulation/
├── .github/
│   ├── workflows/
│   │   └── ci.yml
│   └── ISSUE_TEMPLATE/
├── docs/
│   ├── README.md
│   ├── CHANGELOG.md
│   ├── USE_CASES.md
│   ├── COMPREHENSIVE_GUIDE.md
│   ├── QUICK_REFERENCE.md
│   ├── SETUP_GUIDE.md
│   ├── QUICK_START_WINDOWS.md
│   └── INSTALLATION_FIX.md
├── examples/
│   ├── configs/
│   └── results/
├── src/
│   ├── __init__.py
│   ├── acp_corrected_final.py
│   ├── acp_parallel_power_analysis.py
│   ├── acp_fully_configurable.py
│   ├── parameter_sweep.py
│   ├── check_setup.py
│   └── explain_results.py
├── requirements.txt
├── CONTRIBUTING.md
└── LICENSE
```

## Implementation Commands

```bash
# Execute Phase 2
move *.md docs\
move v3-Claude-Windows-Parameters-Scaled-agents-ACP-simulation\*.md docs\
del *.zip
del mininet-vm.ova
del cdf_comparison.png
rmdir /s /q v2-Claude-WindowsSetup-1000-scaled-agents-ACP-simulation
rmdir /s /q v2-Claude-WindowsSetup-1000-scaled-agents-ACP-simulation-branch
rmdir /s /q v3-Claude-Windows-Parameters-Scaled-agents-ACP-simulation

# Update imports in src/*.py files
# (Use find/replace to update path references)

# Create GitHub Actions directory
mkdir .github\workflows
mkdir .github\ISSUE_TEMPLATE

# Create and push tag
git tag -a v3.0.0 -m "Version 3.0: Fully configurable ACP simulation"
git push origin v3.0.0
git push origin v2.0-stable
```

## Timeline Estimate
- **Phase 2**: 30 minutes (directory cleanup)
- **Phase 3**: 15 minutes (GitHub releases)
- **Phase 4**: 30 minutes (CI/CD setup)
- **Phase 5**: 45 minutes (modernization)
- **Total**: ~2 hours for complete restructure

## Benefits Achieved
✅ **Professional structure** - Standard open-source layout
✅ **Reduced repository size** - Remove duplicates and binaries
✅ **Better tooling** - CI/CD, linting, automated testing
✅ **Easier contributions** - Clear structure and guidelines
✅ **Proper versioning** - Git tags and GitHub releases
✅ **Modern development** - Automated dependency updates