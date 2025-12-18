# ðŸ¤– AI-Assisted Development Guide

This document describes the AI-assisted development capabilities integrated into the ACP Simulation project using the Claude Code Playbook v3.0.0.

---

## Overview

The ACP Simulation project now includes a comprehensive AI-assisted development system that enables token-efficient collaboration with Claude Code for refactoring, code improvement, and maintenance tasks.

**Repository**: https://github.com/dyb5784/acp-simulation

---

## ðŸŽ¯ What is Claude Code Playbook?

The Claude Code Playbook is a token-efficient AI engineering system that reduces conversation turns by 67% through specialized workflows and systematic development protocols.

### Key Benefits
- **67% reduction** in conversation turns for refactoring tasks
- **Predictable token costs** per operation type
- **100% test pass rate** maintained throughout refactoring
- **Zero API breakage** with systematic validation gates
- **Budget-aware development** optimized for Claude Pro limits

---

## ðŸ“‚ Included Files

### Core Configuration
```
.claude/
â”œâ”€â”€ settings.local.json                 # Optional permissions
â””â”€â”€ skills/
    â””â”€â”€ refactoring/
        â”œâ”€â”€ SKILL.md                    # Complete skill overview (5,639 lines)
        â”œâ”€â”€ workflows/                  # 7 specialized workflows
        â”‚   â”œâ”€â”€ triage.md               # Tech debt analysis (6,211 lines)
        â”‚   â”œâ”€â”€ extract.md              # Function extraction (456 lines)
        â”‚   â”œâ”€â”€ modernize.md            # Pattern updates (481 lines)
        â”‚   â”œâ”€â”€ qnew.md                 # Session init (4,772 lines)
        â”‚   â”œâ”€â”€ qplan.md                # Plan validation (518 lines)
        â”‚   â”œâ”€â”€ qcode.md                # Batch implementation (740 lines)
        â”‚   â””â”€â”€ catchup.md              # Context restoration (5,639 lines)
        â””â”€â”€ knowledge/                  # Reference documentation
            â”œâ”€â”€ typescript-style.md     # Modern TS patterns (7,111 lines)
            â””â”€â”€ architecture-patterns.md # Architecture guides (10,792 lines)

CLAUDE.md                               # Project constitution (315 lines)
.cursorrules                           # Cursor IDE integration
```

---

## ðŸš€ Quick Start

### Initialize a Session

```bash
# Start fresh with context restoration
/clear
claude skills refactoring qnew

# Analyze your codebase for improvements
claude skills refactoring triage
```

### Common Workflows

**1. Find Technical Debt**
```bash
claude skills refactoring triage
```
Identifies the top 3 areas needing refactoring in your codebase.

**2. Extract a Function**
```bash
claude skills refactoring extract
```
Guides you through extracting a function to improve modularity.

**3. Modernize Code Patterns**
```bash
claude skills refactoring modernize
```
Updates code to use modern patterns and best practices.

**4. Batch Implementation**
```bash
claude skills refactoring qcode
```
Implements changes across multiple files (up to 15 files).

**5. Restore Context**
```bash
claude skills refactoring catchup
```
Restores context after using `/clear` (use every 5-7 prompts).

---

## ðŸ“Š Token Economics

### Claude Pro Limits
- **10-40 prompts** per 5-hour window
- **~44,000 tokens** total capacity

### Example Session (Within Budget)
```
qnew:        2K tokens
triage:      2K tokens
qplan:       3K tokens
extract #1:  5K tokens
/clear + catchup: 1K tokens
extract #2:  5K tokens
modernize:   4K tokens
â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
Total:      22K tokens (50% of budget)
```

### Session Management Protocol
**Every 5-7 prompts, execute:**
```bash
/cost                              # Check token usage
/clear                             # Reset context
claude skills refactoring catchup  # Restore context
```

**Why?** Prevents context degradation, optimizes token efficiency, maintains quality.

---

## ðŸ—ï¸ Modern Architecture Patterns

The playbook includes guidance for modernizing the ACP codebase:

### Feature-Based Modules
```
src/features/
  â””â”€â”€ acp-simulation/
      â”œâ”€â”€ manager.py      # Business logic
      â”œâ”€â”€ types.py        # Domain types
      â”œâ”€â”€ config.py       # Configuration
      â””â”€â”€ tests/
          â””â”€â”€ test_*.py   # Unit tests
```

### Functional Composition (Python)
```python
# Factory functions over classes
def create_acp_simulation(config: SimulationConfig):
    network = create_network(config.num_nodes, config.connectivity)
    attacker = create_cognitive_attacker(config.learning_rate)
    defender = create_acp_defender(config.acp_strength)
    
    return {
        'run': lambda episodes: run_simulation(network, attacker, defender, episodes),
        'analyze': lambda results: analyze_results(results)
    }
```

### Result Monad Pattern (Python)
```python
from typing import Union, Tuple

class Ok:
    def __init__(self, value):
        self.value = value
        self.ok = True

class Err:
    def __init__(self, error):
        self.error = error
        self.ok = False

Result = Union[Ok, Err]

def run_simulation(params) -> Result[SimulationResults, SimulationError]:
    try:
        results = validate_and_run(params)
        return Ok(results)
    except Exception as e:
        return Err(SimulationError(f"Simulation failed: {e}"))
```

---

## âœ… Validation Gates

**Before ANY commit, ALL checks must pass:**

1. **Type Check** (if using type hints)
   ```bash
   python -m mypy src/
   ```
   **Expected:** 0 errors

2. **Unit Tests**
   ```bash
   python -m pytest tests/
   ```
   **Expected:** All tests pass

3. **Linting**
   ```bash
   python -m flake8 src/
   ```
   **Expected:** 0 errors, 0 warnings

**If ANY validation fails: DO NOT PROCEED. Fix the issue first.**

---

## ðŸŽ¯ Success Metrics

### Code Quality Targets
- **Lines per file**: < 500
- **Cyclomatic complexity**: < 10
- **Test coverage**: > 80%
- **Type hints**: 100% for public APIs

### Technical Debt Goals
- **God objects**: 0
- **Mixed concerns**: 0
- **Duplicate code**: Minimal

---

## ðŸŽ“ Learning Path

### Beginner (Sessions 1-2)
1. Run `qnew` to start
2. Use `triage` to understand the ACP codebase
3. Extract 1 simple function with `extract`
4. Practice `/clear` + `catchup` protocol

### Intermediate (Sessions 3-10)
1. Use `qplan` before extractions
2. Extract 2-3 functions per session
3. Apply `modernize` to update patterns
4. Track progress in `REFACTOR_PROGRESS.md`

### Advanced (Sessions 10+)
1. Use `qcode` for batch operations (10-15 files)
2. Design custom extraction strategies
3. Contribute patterns back to knowledge base
4. Mentor team members

---

## ðŸ”§ Workflow Details

### 1. Triage Workflow
**Purpose**: Find top 3 technical debt hotspots
**Cost**: ~2K tokens
**When to use**: Start of project or new session

**What it does:**
- Analyzes codebase structure
- Identifies god objects and mixed concerns
- Calculates cyclomatic complexity
- Reports top 3 refactoring priorities

### 2. QNew Workflow
**Purpose**: Initialize session with context
**Cost**: ~2K tokens
**When to use**: Start of work day

**What it does:**
- Loads project context
- Reviews CLAUDE.md guidelines
- Sets up session parameters
- Prepares for productive work

### 3. QPlan Workflow
**Purpose**: Validate refactoring plan
**Cost**: ~3K tokens
**When to use**: Before implementation

**What it does:**
- Reviews proposed changes
- Checks for API breakage
- Validates approach against patterns
- Provides improvement suggestions

### 4. Extract Workflow
**Purpose**: Extract function to new module
**Cost**: ~5K tokens
**When to use**: Targeted decomposition

**What it does:**
- Identifies extraction boundaries
- Creates new module/file
- Updates imports and references
- Adds unit tests

### 5. Modernize Workflow
**Purpose**: Update to modern patterns
**Cost**: ~4K tokens
**When to use**: Pattern upgrades

**What it does:**
- Identifies outdated patterns
- Applies modern equivalents
- Updates type hints
- Improves code quality

### 6. QCode Workflow
**Purpose**: Full implementation (max 15 files)
**Cost**: ~8-12K tokens
**When to use**: Execute approved plan

**What it does:**
- Implements across multiple files
- Runs validation checks
- Fixes issues iteratively
- Ensures all tests pass

### 7. Catchup Workflow
**Purpose**: Restore context after `/clear`
**Cost**: ~1-2K tokens
**When to use**: Every 5-7 prompts

**What it does:**
- Reloads project context
- Reviews recent changes
- Restores session state
- Continues work seamlessly

---

## ðŸ“– Reference Documentation

### Architecture Patterns
See [`.claude/skills/refactoring/knowledge/architecture-patterns.md`](.claude/skills/refactoring/knowledge/architecture-patterns.md) for:
- Feature-based module organization
- Result monad pattern implementation
- Functional composition strategies
- Dependency injection patterns

### TypeScript Style Guide
See [`.claude/skills/refactoring/knowledge/typescript-style.md`](.claude/skills/refactoring/knowledge/typescript-style.md) for:
- Modern TypeScript patterns
- Type safety best practices
- Functional programming approaches
- Error handling strategies

### Project Constitution
See [`CLAUDE.md`](CLAUDE.md) for:
- Budget constraints and token limits
- Commit guidelines and message format
- Validation requirements
- Session management protocols

---

## ðŸš€ Getting Started with ACP Development

### Step 1: Initial Setup
```bash
# Clone the repository
git clone https://github.com/dyb5784/acp-simulation.git
cd acp-simulation

# Verify installation
python check_setup.py
```

### Step 2: First AI-Assisted Session
```bash
# In Claude Code or Claude.ai Project
/clear
claude skills refactoring qnew

# Analyze the codebase
claude skills refactoring triage
```

### Step 3: Plan Improvements
```bash
# Review suggestions and plan
claude skills refactoring qplan

# Extract a function
claude skills refactoring extract
```

### Step 4: Modernize Patterns
```bash
# Update to modern patterns
claude skills refactoring modernize
```

---

## ðŸ“ž Support

For AI-assisted development questions:
1. Review this documentation
2. Check [`CLAUDE.md`](CLAUDE.md) for guidelines
3. Run `claude skills refactoring qnew` to refresh context
4. See [Claude Code Documentation](https://docs.claude.com/claude-code)

For ACP simulation questions:
1. See [`docs/README.md`](docs/README.md) for project overview
2. Check [`docs/SETUP_GUIDE.md`](docs/SETUP_GUIDE.md) for installation
3. Review [`v3-Claude-Windows-Parameters-Scaled-agents-ACP-simulation/COMPREHENSIVE_GUIDE.md`](v3-Claude-Windows-Parameters-Scaled-agents-ACP-simulation/COMPREHENSIVE_GUIDE.md) for parameters

---

**Version**: 3.1.0  
**Date**: December 11, 2025  
**Claude Code Playbook**: v3.0.0  
**Status**: âœ… Integrated and Ready