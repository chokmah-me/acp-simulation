# ACP Simulation - Claude Code Playbook

This project includes the Claude Code Playbook v4.0.0 for AI-assisted development.

## 🚀 Quick Start

### First Time Setup

```bash
# 1. Start a new session
/clear

# 2. Load the session initialization workflow
view .claude/skills/refactoring/workflows/qnew.md

# 3. Choose your skill based on work type:

# For simulation/numerical work:
view .claude/skills/python-scientific/SKILL.md

# For refactoring/architecture:
view .claude/skills/refactoring/SKILL.md
```

### Session Management Protocol

**Every 5-7 prompts, execute:**
```bash
/cost                                          # Check token usage
/clear                                         # Reset context
view .claude/skills/refactoring/workflows/catchup.md    # Restore context
```

## 📁 Directory Structure

```
.claude/
├── README.md                  # Playbook overview
├── GETTING_STARTED.md         # Detailed setup guide
├── WORKFLOW_GUIDE.md          # Comprehensive workflow documentation
└── skills/
    ├── README.md              # Skills navigation hub ⭐ START HERE
    ├── python-scientific/     # Scientific computing patterns
    │   └── SKILL.md          # NumPy, reproducibility, performance
    └── refactoring/          # Code refactoring workflows
        ├── SKILL.md          # Refactoring skill overview
        └── workflows/        # Executable workflows
            ├── triage.md     # Find technical debt hotspots
            ├── extract.md    # Extract components
            ├── qnew.md       # Start new session
            ├── qplan.md      # Validate plan
            ├── qcode.md      # Execute implementation
            └── catchup.md    # Resume after /clear
```

## 🎯 Common Workflows

### 1. Start New Session
```bash
/clear
view .claude/skills/refactoring/workflows/qnew.md
```

### 2. Find Technical Debt
```bash
view .claude/skills/refactoring/workflows/triage.md
```

### 3. Extract Component (e.g., from NetworkEnvironment)
```bash
view .claude/skills/refactoring/workflows/extract.md
```

### 4. Optimize Simulation Performance
```bash
view .claude/skills/python-scientific/SKILL.md
# Focus on vectorization and profiling sections
```

### 5. Resume After Context Clear
```bash
/clear
view .claude/skills/refactoring/workflows/catchup.md
```

## 🧪 Validation Requirements

**Before ANY commit, ALL checks must pass:**

```bash
# Type checking (if using mypy)
mypy src/ --strict

# Linting
flake8 src/ --max-line-length=100

# Tests
pytest tests/ -v

# Reproducibility (for ACP simulation)
python scripts/verify_reproducibility.py
```

**If ANY validation fails: STOP. Fix the issue first.**

## 📊 Token Budget Awareness

### Claude Pro Limits
- **10-40 prompts** per 5-hour window
- **~44,000 tokens** total capacity

### Typical Session (54% of budget)
```
Session start:           2K tokens
Load skill:              1K tokens
Triage:                  2K tokens
Plan:                    3K tokens
Extract #1:              5K tokens
/clear + catchup:        1K tokens
Extract #2:              5K tokens
Documentation:           3K tokens
Testing:                 2K tokens
──────────────────────────────────
Total:                  24K tokens
```

### Budget Tips
- Run `/cost` every 3 prompts
- Reset context (`/clear` + catchup) every 5-7 prompts
- Load skills once per session
- Batch related work together

## 🎓 Learning Path

### Beginner (Sessions 1-2)
1. Read `.claude/skills/README.md` to understand available skills
2. Run `qnew` workflow to start
3. Run `triage` to understand the codebase
4. Practice `/clear` + `catchup` protocol

### Intermediate (Sessions 3-10)
1. Use `extract` workflow to decompose components
2. Apply Python scientific patterns for vectorization
3. Use `qplan` before major changes
4. Track progress systematically

### Advanced (Sessions 10+)
1. Use `qcode` for batch operations
2. Design custom refactoring strategies
3. Optimize simulation performance
4. Contribute improvements to skills

## 📚 Key Documents

- **[Skills README](.claude/skills/README.md)** ⭐ Navigation hub for all skills
- **[Python Scientific Skill](.claude/skills/python-scientific/SKILL.md)** - NumPy, reproducibility, performance
- **[Refactoring Skill](.claude/skills/refactoring/SKILL.md)** - Code organization and workflows
- **[Getting Started](.claude/GETTING_STARTED.md)** - Detailed setup guide
- **[Workflow Guide](.claude/WORKFLOW_GUIDE.md)** - Comprehensive workflow docs

## 🎯 ACP Simulation Priorities

Based on technical debt analysis, focus on:

1. **NetworkEnvironment class** (330 lines)
   - God object with multiple responsibilities
   - Use: extract workflow + Python scientific patterns
   - Target: GraphTopology, NodeStateManager, ActionExecutor components

2. **run_corrected_experiment()** (186 lines)
   - Monolithic orchestration function
   - Use: extract workflow + configuration patterns
   - Target: Focused orchestration components

3. **Agent decision logic**
   - Performance bottleneck
   - Use: Python scientific patterns
   - Target: Vectorized batch processing

## ✅ Success Criteria

Your refactoring is successful when:
- ✅ All tests pass (100% pass rate maintained)
- ✅ Type hints added with numpy.typing
- ✅ Reproducibility verified (same seed = same results)
- ✅ Performance improved or maintained
- ✅ Code follows single-responsibility principle
- ✅ NumPy-style docstrings added
- ✅ Technical debt reduced

## 🆘 Troubleshooting

### "Workflow not found"
- Ensure you're viewing files with `.claude/skills/` prefix
- Check file paths: `ls .claude/skills/refactoring/workflows/`

### High token usage
- Use `/clear` + `catchup` more frequently (every 5-7 prompts)
- Don't reload skills unnecessarily
- Focus on one component at a time

### Tests failing after refactoring
- STOP immediately
- Identify the breaking change
- Fix before proceeding
- Never commit with failing tests

### Context seems lost
- Run: `/clear` then view `.claude/skills/refactoring/workflows/catchup.md`
- The catchup workflow will restore full context

## 📞 Support

1. Start with: `.claude/skills/README.md`
2. Check relevant skill documentation
3. Use `qnew` workflow to refresh context
4. Review `WORKFLOW_GUIDE.md` for detailed workflows

## 🔄 Version

- **Playbook Version**: 4.0.0
- **Date**: December 18, 2024
- **Project**: ACP Simulation
- **Status**: ✅ Configured and Ready

---

**Next Step:** Read [`.claude/skills/README.md`](.claude/skills/README.md) to understand available skills and choose your starting point.
