# Claude Skills Directory

This directory contains skills for AI-assisted development with Claude Code for the ACP Simulation project.

## Directory Structure

```
.claude/skills/
├── README.md (this file)
├── python-scientific/         # Python scientific computing patterns
│   └── SKILL.md              # NumPy, reproducibility, performance
└── refactoring/              # General code refactoring
    ├── SKILL.md              # Skill overview
    └── workflows/            # Development workflows
        ├── triage.md         # Find technical debt hotspots
        ├── extract.md        # Extract code to modules
        ├── qnew.md           # Start new session
        ├── qplan.md          # Validate refactoring plan
        ├── qcode.md          # Full implementation
        └── catchup.md        # Resume after context clear
```

## Available Skills

### 1. Python Scientific Computing

**Location**: `.claude/skills/python-scientific/SKILL.md`

**Purpose**: Best practices for research-grade Python development with NumPy/SciPy

**Key Topics**:
- Vectorization over loops
- Random seed management for reproducibility  
- Type hints with `numpy.typing`
- Configuration management with dataclasses
- Parallel processing patterns
- Testing numerical code
- Performance profiling
- Memory-efficient operations
- NumPy-style docstrings
- ACP-specific patterns

**When to Use**:
- Working on simulation code
- Numerical analysis and statistical validation
- Performance optimization
- Ensuring reproducibility
- Writing research code for publication
- Refactoring NetworkEnvironment or agent logic

**Quick Start**:
```bash
# Load skill at session start
view .claude/skills/python-scientific/SKILL.md

# Then work on your code with patterns in mind
```

### 2. General Refactoring

**Location**: `.claude/skills/refactoring/SKILL.md`

**Purpose**: Structured workflows for code quality improvement and architecture

**Available Workflows**:
- **triage**: Identify technical debt hotspots in codebase
- **extract**: Extract reusable components (e.g., from NetworkEnvironment)
- **qnew**: Start new refactoring session with context
- **qplan**: Validate refactoring plan before implementation
- **qcode**: Execute approved plan with validation
- **catchup**: Resume after context clear

**When to Use**:
- Breaking down god objects (NetworkEnvironment class)
- Extracting specialized components (GraphTopology, NodeStateManager)
- Architectural decisions
- Code organization and structure
- Technical debt reduction
- Feature development

**Quick Start**:
```bash
# Start session
/clear
view .claude/skills/refactoring/workflows/qnew.md

# Identify debt hotspots
view .claude/skills/refactoring/workflows/triage.md

# Extract a component
view .claude/skills/refactoring/workflows/extract.md
```

## Skill Selection Guide for ACP Simulation

| Task Type | Primary Skill | Secondary Skill | Notes |
|-----------|---------------|-----------------|-------|
| Optimize simulation loop | Python Scientific | - | Focus on vectorization |
| Extract NetworkEnvironment components | Refactoring | Python Scientific | Combine both for best results |
| Add type hints to modules | Python Scientific | - | Use numpy.typing |
| Fix numerical reproducibility | Python Scientific | - | Check seed management |
| Decompose monolithic functions | Refactoring | - | Use extract workflow |
| Add new defense strategy | Python Scientific | Refactoring | Design pattern, then implement |
| Performance tuning | Python Scientific | - | Profile first, optimize second |
| Code review before PR | Both | - | Check patterns from both |

## Usage Patterns

### Starting a Session

1. **Clear context** if needed: `/clear`
2. **Load appropriate skill**:
   - For simulation work: `view .claude/skills/python-scientific/SKILL.md`
   - For refactoring: `view .claude/skills/refactoring/workflows/qnew.md`
3. **Work with patterns**: Apply skill guidelines to your code

### During Development

- **Check cost**: `/cost` every ~3 prompts
- **Reference skills**: View specific sections as needed
- **Follow patterns**: Use examples from SKILL.md files
- **Validate frequently**: Run tests after each change

### Session Reset Protocol

Execute `/clear` + load catchup workflow every 5-7 prompts:

```bash
/clear
view .claude/skills/refactoring/workflows/catchup.md
```

### Before Committing

Verify your changes follow skill patterns:

```bash
# For Python scientific code
- [ ] Vectorized operations used where possible
- [ ] Type hints added with numpy.typing
- [ ] Reproducibility verified with fixed seeds
- [ ] NumPy-style docstrings added
- [ ] Tests pass: pytest tests/ -v
- [ ] Type check passes: mypy src/ --strict
- [ ] Linting passes: flake8 src/

# For refactoring work
- [ ] Code well-organized into focused modules
- [ ] Single-responsibility components
- [ ] Technical debt reduced
- [ ] Architecture improved
- [ ] Tests maintain 100% pass rate
```

## Integration with Project

The skills in this directory support the development guidelines in project documentation:

- **Python Scientific**: Implements patterns for ACP simulation code quality
- **Refactoring**: Provides workflows for NetworkEnvironment decomposition
- Together they ensure code quality and research reproducibility

## ACP Simulation Specific Guidelines

### Priority Refactoring Targets

Based on technical debt analysis:

1. **NetworkEnvironment class** (330 lines, god object)
   - Use: Refactoring extract workflow
   - Apply: Python scientific patterns for vectorization
   - Target: Single-responsibility components

2. **run_corrected_experiment()** (186 lines, monolithic)
   - Use: Refactoring extract workflow
   - Apply: Configuration management patterns
   - Target: Focused orchestration components

3. **Agent decision logic**
   - Use: Python scientific skill
   - Apply: Vectorization patterns
   - Target: Batch processing for performance

### Validation Requirements

**Before ANY commit to ACP simulation:**

```bash
# Type checking (if using mypy)
mypy src/ --strict

# Linting
flake8 src/ --max-line-length=100

# Tests
pytest tests/ -v

# Reproducibility
python scripts/verify_reproducibility.py
```

All must pass with zero errors.

## Token Budget Awareness

### Claude Pro Limits
- **10-40 prompts** per 5-hour window
- **~44,000 tokens** total capacity

### Typical Session Allocation
```
Session Start (qnew):           2K tokens
Load Python Scientific skill:   1K tokens
Triage analysis:                2K tokens
Plan refactoring (qplan):       3K tokens
Extract component #1:           5K tokens
/clear + catchup:               1K tokens
Extract component #2:           5K tokens
Type hints & docs:              3K tokens
Testing & validation:           2K tokens
────────────────────────────────────────
Total:                         24K tokens (54% of budget)
```

### Budget Optimization Tips

1. **Load skills once per session** - Don't re-read unless needed
2. **Use workflows efficiently** - triage once, extract multiple times
3. **Reset context regularly** - Every 5-7 prompts: `/clear` + catchup
4. **Batch related work** - Multiple extractions in one session
5. **Validate incrementally** - Catch errors early

## Version History

- **v1.1** (2024-12-18): Added Python Scientific skill, improved organization
- **v1.0** (2024-12-11): Initial skills directory with refactoring workflows

## See Also

- `../../CONTEXT.md` - Project-specific context and operational constraints
- `../../GETTING_STARTED.md` - Quick start guide for playbook
- `../../WORKFLOW_GUIDE.md` - Detailed workflow documentation
