# 🚀 ACP Simulation - Setup Guide

## Quick Setup (Windows)

### Step 1: Install Required Packages

Open PowerShell or Command Prompt and run:

```powershell
# Option 1: Using pip (recommended)
pip install numpy scipy networkx matplotlib

# Option 2: Using requirements.txt
pip install -r requirements.txt

# Option 3: If pip is not in PATH
python -m pip install numpy scipy networkx matplotlib
```

### Step 2: Verify Installation

```powershell
python -c "import numpy; import scipy; import networkx; import matplotlib; print('✅ All packages installed successfully!')"
```

### Step 3: Run the Simulation

```powershell
# Quick test (100 episodes)
python acp_corrected_final.py

# Power analysis (1,000 episodes)
python acp_parallel_power_analysis.py

# Large scale (10,000 episodes)
python acp_parallel_power_analysis.py --num-episodes 10000
```

---

## Detailed Setup Instructions

### For Windows:

1. **Check Python Installation:**
   ```powershell
   python --version
   ```
   Should show Python 3.8 or higher. If not, install from https://www.python.org/

2. **Install Packages:**
   ```powershell
   pip install numpy scipy networkx matplotlib
   ```

3. **If you get "pip is not recognized":**
   ```powershell
   python -m pip install --upgrade pip
   python -m pip install numpy scipy networkx matplotlib
   ```

4. **If you get permission errors:**
   ```powershell
   pip install --user numpy scipy networkx matplotlib
   ```

### For Linux/Mac:

```bash
# Using pip
pip3 install numpy scipy networkx matplotlib

# Or using requirements.txt
pip3 install -r requirements.txt

# If permission denied
pip3 install --user numpy scipy networkx matplotlib
```

---

## Common Issues and Solutions

### Issue 1: "ModuleNotFoundError: No module named 'numpy'"
**Solution:**
```powershell
pip install numpy
```

### Issue 2: "pip is not recognized as an internal or external command"
**Solution:**
```powershell
# Use python -m pip instead
python -m pip install numpy scipy networkx matplotlib

# Or add Python to PATH (Windows):
# 1. Search "Environment Variables" in Windows
# 2. Edit PATH
# 3. Add: C:\Users\YourUsername\AppData\Local\Programs\Python\Python3X\Scripts
```

### Issue 3: "Permission denied" or "Access is denied"
**Solution:**
```powershell
# Install for current user only
pip install --user numpy scipy networkx matplotlib
```

### Issue 4: Multiple Python versions installed
**Solution:**
```powershell
# Use specific Python version
python3 -m pip install numpy scipy networkx matplotlib
python3 acp_parallel_power_analysis.py
```

### Issue 5: "ImportError: DLL load failed" (Windows)
**Solution:**
```powershell
# Install Microsoft Visual C++ Redistributable
# Download from: https://aka.ms/vs/17/release/vc_redist.x64.exe

```

---


3. **Run simulation:**
   ```bash
   python acp_parallel_power_analysis.py
   ```

---

## Package Versions

These are the minimum versions required:

| Package | Minimum Version | Recommended |
|---------|----------------|-------------|
| Python | 3.8 | 3.11+ |
| numpy | 1.20.0 | 1.24+ |
| scipy | 1.7.0 | 1.11+ |
| networkx | 2.6.0 | 3.0+ |
| matplotlib | 3.4.0 | 3.8+ |

---

## Verification Script

Create a file called `check_setup.py`:

```python
import sys

print("Checking Python version...")
print(f"Python {sys.version}")

packages = {
    'numpy': '1.20.0',
    'scipy': '1.7.0', 
    'networkx': '2.6.0',
    'matplotlib': '3.4.0'
}

print("\nChecking packages...")
missing = []
for package, min_version in packages.items():
    try:
        mod = __import__(package)
        version = getattr(mod, '__version__', 'unknown')
        print(f"✅ {package} {version}")
    except ImportError:
        print(f"❌ {package} NOT INSTALLED")
        missing.append(package)

if missing:
    print(f"\n⚠️  Missing packages: {', '.join(missing)}")
    print("\nTo install, run:")
    print(f"pip install {' '.join(missing)}")
else:
    print("\n✅ All packages installed successfully!")
    print("You can now run: python acp_parallel_power_analysis.py")
```

Run it:
```powershell
python check_setup.py
```

---

## Running the Simulation

### Basic Usage:

```powershell
# 100 episodes (quick test, ~1 second)
python acp_corrected_final.py

# 1,000 episodes (power analysis, ~3 seconds)  
python acp_parallel_power_analysis.py

# 10,000 episodes (publication quality, ~30 seconds)
python acp_parallel_power_analysis.py --num-episodes 10000
```

### Expected Output:

```
╔════════════════════════════════════════════════════════════════════╗
║               PARALLEL ACP SIMULATION - POWER ANALYSIS             ║
║           1,000+ Episodes for Publication-Quality Results          ║
╚════════════════════════════════════════════════════════════════════╝

Configuration:
  • Total episodes: 1000
  • CPU cores: 4
  • Bootstrap samples: 10,000
  • Confidence level: 95%

Starting parallel execution...
✅ Completed 1000 episodes in 3.14 seconds

POWER ANALYSIS RESULTS
======================================================================
Achieved Power: 100.0%
Effect Size (Cohen's d): 5.447
p-value: 0.00e+00 (highly significant)
```

---

## Performance Tips

### 1. Use Multiple Cores
The script automatically uses available CPU cores:
```python
# Modify in acp_parallel_power_analysis.py
n_cores = 8  # Use 8 cores instead of auto-detect
```

### 2. Increase Episodes
```python
num_episodes = 10000  # More episodes = higher confidence
```

### 3. Save Results
Results are automatically saved to:
- `power_analysis_results.png` - Visualization
- `power_analysis_results.pkl` - Data for further analysis

---

## Getting Help

If you encounter other issues:

1. **Check Python version:**
   ```powershell
   python --version
   ```
   Should be 3.8 or higher

2. **Check pip version:**
   ```powershell
   pip --version
   ```

3. **Update pip:**
   ```powershell
   python -m pip install --upgrade pip
   ```

4. **Try installing one package at a time:**
   ```powershell
   pip install numpy
   pip install scipy
   pip install networkx
   pip install matplotlib
   ```

5. **If all else fails, try installing packages individually**

---

## File Checklist

Make sure you have these files in your directory:

```
G:\My Drive\2026-bsi-vortrag\software\
├── acp_corrected_final.py          (core implementation)
├── acp_parallel_power_analysis.py  (parallel scaling)
├── requirements.txt                (package list)
├── check_setup.py                  (verification script)
└── SETUP_GUIDE.md                  (this file)
```

---

## Quick Start (Copy-Paste)

```powershell
# Install packages
pip install numpy scipy networkx matplotlib

# Verify installation
python -c "import numpy, scipy, networkx, matplotlib; print('✅ Ready!')"

# Run simulation
python acp_parallel_power_analysis.py

# Done! Results saved to power_analysis_results.png
```

---

**Need help?** The error messages are usually clear about what's missing. Just install the missing package with `pip install <package-name>`.
