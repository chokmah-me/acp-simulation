# Claude Skills Directory

This directory contains skills for AI-assisted development with Claude Code.

## Directory Structure

```
.claude/skills/
├── README.md (this file)
├── python-scientific/         # Python scientific computing patterns
│   └── SKILL.md              # NumPy, reproducibility, performance
└── refactoring/              # General code refactoring
    ├── SKILL.md              # Skill overview
    ├── workflows/            # Development workflows
    │   ├── triage.md
    │   ├── extract.md
    │   ├── modernize.md
    │   ├── qnew.md
    │   ├── qplan.md
    │   ├── qcode.md
    │   └── catchup.md
    └── knowledge/            # Reference materials
        ├── typescript-patterns.md
        └── architecture-patterns.md
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

**When to Use**:
- Working on simulation code
- Numerical analysis and statistical validation
- Performance optimization
- Ensuring reproducibility
- Writing research code for publication

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
- **triage**: Identify issues in codebase
- **extract**: Extract reusable components
- **modernize**: Update to modern patterns
- **qnew**: Quick new feature development
- **qplan**: Quick planning session
- **qcode**: Quick coding session  
- **catchup**: Resume after context clear

**When to Use**:
- Architectural decisions
- Code organization and structure
- Feature development
- Technical debt reduction

**Quick Start**:
```bash
# Use a specific workflow
claude skills refactoring triage
claude skills refactoring qnew
```

## Skill Selection Guide

| Task Type | Primary Skill | Notes |
|-----------|---------------|-------|
| Optimize simulation | Python Scientific | Focus on vectorization |
| Add type hints | Python Scientific | Use numpy.typing |
| Fix numerical bug | Python Scientific | Check reproducibility |
| Restructure modules | General Refactoring | Use extract workflow |
| Add new feature | Python Scientific + Refactoring | Combine both |
| Performance tuning | Python Scientific | Profile first |
| Code review | Both | Check patterns from both |

## Usage Patterns

### Starting a Session

1. **Clear context** if needed: `/clear`
2. **Load appropriate skill**: `view .claude/skills/<skill>/SKILL.md`
3. **Work with patterns**: Apply skill guidelines to your code

### During Development

- **Check cost**: `/cost` every ~3 prompts
- **Reference skills**: View specific sections as needed
- **Follow patterns**: Use examples from SKILL.md files

### Before Committing

Verify your changes follow skill patterns:

```bash
# For Python scientific code
- [ ] Vectorized operations used
- [ ] Type hints added  
- [ ] Reproducibility verified
- [ ] NumPy-style docstrings
- [ ] Tests pass

# For refactoring work
- [ ] Code well-organized
- [ ] Modern patterns used
- [ ] Technical debt reduced
- [ ] Architecture improved
```

## Integration with CLAUDE.md

The skills in this directory support the development guidelines in `CLAUDE.md`:

- `CLAUDE.md` defines **project-level standards** and **validation requirements**
- Skills provide **implementation patterns** and **best practices**
- Together they ensure code quality and research reproducibility

## Adding New Skills

To add a new skill:

1. Create directory: `.claude/skills/<skill-name>/`
2. Add `SKILL.md` with:
   - Overview and purpose
   - When to use the skill
   - Key patterns with examples
   - Quick reference
3. Update this `README.md`
4. Reference in `CLAUDE.md` if needed

## Version History

- **v1.0** (2025-12-11): Initial skills directory with Python Scientific Computing
- **v0.9** (2025-12-10): General Refactoring skill added

## See Also

- `../../CLAUDE.md` - Project development guidelines
- `../../docs/AI_ASSISTED_DEVELOPMENT.md` - AI integration documentation
- `../../VERSION_CHANGELOG.md` - Project version history
