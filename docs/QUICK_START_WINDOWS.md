# 🚀 Quick Start Guide - Windows

## Step-by-Step Instructions

### Step 1: Install Required Packages

Open **PowerShell** (or Command Prompt) in your project directory:

```powershell
cd "G:\My Drive\2026-bsi-vortrag\software"
```

Then install the required packages:

```powershell
pip install numpy scipy networkx matplotlib
```

**If you get an error "pip is not recognized"**, try:

```powershell
python -m pip install numpy scipy networkx matplotlib
```

### Step 2: Verify Installation

```powershell
python check_setup.py
```

You should see:
```
✅ numpy           1.24.3          (minimum: 1.20.0)
✅ scipy           1.11.3          (minimum: 1.7.0)
✅ networkx        3.1             (minimum: 2.6.0)
✅ matplotlib      3.8.0           (minimum: 3.4.0)

✅ ALL PACKAGES INSTALLED SUCCESSFULLY!
```

### Step 3: Run the Simulation

#### Quick Test (100 episodes, ~1 second):
```powershell
python acp_corrected_final.py
```

#### Power Analysis (1,000 episodes, ~3 seconds):
```powershell
python acp_parallel_power_analysis.py
```

#### Large Scale (10,000 episodes, ~30 seconds):
```powershell
python acp_parallel_power_analysis.py --num-episodes 10000
```

### Step 4: View Results

Two files will be created in your current directory:
1. `power_analysis_results.png` - Open with any image viewer
2. `power_analysis_results.pkl` - Python data file for further analysis

---

## Common Issues & Solutions

### ❌ Issue: "ModuleNotFoundError: No module named 'numpy'"

**Solution:**
```powershell
pip install numpy
```

If that doesn't work:
```powershell
python -m pip install numpy
```

### ❌ Issue: "pip is not recognized"

**Solution 1 - Use python -m pip:**
```powershell
python -m pip install numpy scipy networkx matplotlib
```

**Solution 2 - Add pip to PATH:**
1. Press Win+R, type `sysdm.cpl`, press Enter
2. Go to "Advanced" tab → "Environment Variables"
3. Under "User variables", find "Path" and click "Edit"
4. Click "New" and add: `C:\Users\YourUsername\AppData\Local\Programs\Python\Python311\Scripts`
5. Click OK, restart PowerShell

### ❌ Issue: "Permission denied" or "Access is denied"

**Solution - Install for user only:**
```powershell
pip install --user numpy scipy networkx matplotlib
```

### ❌ Issue: Multiple Python versions

**Solution - Use specific version:**
```powershell
python3 -m pip install numpy scipy networkx matplotlib
python3 acp_parallel_power_analysis.py
```

Or use `py` launcher:
```powershell
py -3.11 -m pip install numpy scipy networkx matplotlib
py -3.11 acp_parallel_power_analysis.py
```

---


---

## Expected Output

When successful, you should see:

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
Sample Size: 500 per strategy (1000 total)
Achieved Power: 1.0000 (100.0%)
Effect Size (Cohen's d): 5.447
p-value: 0.00e+00 (highly significant)

✅ All thesis claims validated with high statistical power
```

---

## Command-Line Options

### Basic Usage:
```powershell
python acp_parallel_power_analysis.py
```

### With Options:
```powershell
# Specify number of episodes
python acp_parallel_power_analysis.py --num-episodes 10000

# Specify number of CPU cores
python acp_parallel_power_analysis.py --cores 8

# Specify output directory
python acp_parallel_power_analysis.py --output "G:\My Drive\results"

# Combine options
python acp_parallel_power_analysis.py --num-episodes 5000 --cores 4 --output "./results"
```

---

## Files in Your Directory

After installation, you should have:

```
G:\My Drive\2026-bsi-vortrag\software\
├── acp_corrected_final.py              # Core implementation
├── acp_parallel_power_analysis.py      # Parallel scaling
├── requirements.txt                    # Package list
├── check_setup.py                      # Verify installation
├── SETUP_GUIDE.md                      # Full documentation
├── QUICK_START_WINDOWS.md             # This file
│
└── (After running):
    ├── power_analysis_results.png      # Visualization
    └── power_analysis_results.pkl      # Data package
```

---

## Performance Expectations

| Episodes | Expected Time | Use Case |
|----------|--------------|----------|
| 100 | ~1 second | Quick test |
| 1,000 | ~3 seconds | Standard analysis |
| 10,000 | ~30 seconds | Publication quality |
| 100,000 | ~5 minutes | Comprehensive validation |

*Times are approximate and depend on your CPU*

---

## Getting Help

### Check Python version:
```powershell
python --version
```
Should show Python 3.8 or higher

### Check pip version:
```powershell
pip --version
```

### Update pip:
```powershell
python -m pip install --upgrade pip
```

### Still having issues?

Try installing packages one at a time and note which one fails:
```powershell
python -m pip install numpy
python -m pip install scipy
python -m pip install networkx
python -m pip install matplotlib
```

Then search for the specific error message online.

---

## One-Line Install & Run

Copy and paste this entire block into PowerShell:

```powershell
python -m pip install numpy scipy networkx matplotlib && python check_setup.py && python acp_parallel_power_analysis.py
```

This will:
1. Install all packages
2. Verify installation
3. Run the simulation

---

## Success Checklist

- [ ] Python 3.8+ installed (`python --version`)
- [ ] Packages installed (`python check_setup.py`)
- [ ] Simulation runs without errors
- [ ] `power_analysis_results.png` file created
- [ ] Results show "✅ All thesis claims validated"

**If all checked, you're ready to go!** 🎉

---

**Date:** December 09, 2025  
**Author:** dyb  
**For:** Beyond Paralysis Thesis Validation
