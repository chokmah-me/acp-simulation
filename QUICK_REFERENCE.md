# Claude Code Playbook - Quick Reference Card

## 🚀 Session Start
```bash
/clear
view .claude/skills/refactoring/workflows/qnew.md
```

## 📊 Check Token Budget (every 3 prompts)
```bash
/cost
```

## 🔄 Reset Context (every 5-7 prompts)
```bash
/cost
/clear
view .claude/skills/refactoring/workflows/catchup.md
```

## 🎯 Common Tasks

### Scientific Computing Work
```bash
view .claude/skills/python-scientific/SKILL.md
```

### Find Technical Debt
```bash
view .claude/skills/refactoring/workflows/triage.md
```

### Extract Component
```bash
view .claude/skills/refactoring/workflows/extract.md
```

### Validate Plan
```bash
view .claude/skills/refactoring/workflows/qplan.md
```

### Execute Implementation
```bash
view .claude/skills/refactoring/workflows/qcode.md
```

## ✅ Pre-Commit Validation
```bash
# All must pass before commit
mypy src/ --strict
flake8 src/ --max-line-length=100
pytest tests/ -v
python scripts/verify_reproducibility.py
```

## 📁 File Navigation

### Entry Points
- **Project overview**: `README.md`
- **Skills hub**: `.claude/skills/README.md` ⭐
- **Session start**: `.claude/skills/refactoring/workflows/qnew.md`

### Skills
- **Python scientific**: `.claude/skills/python-scientific/SKILL.md`
- **Refactoring**: `.claude/skills/refactoring/SKILL.md`

### Workflows (in `.claude/skills/refactoring/workflows/`)
- `triage.md` - Find debt
- `extract.md` - Extract code
- `qnew.md` - Start session
- `qplan.md` - Validate plan
- `qcode.md` - Implement
- `catchup.md` - Resume

## 💡 Token Budget

**Claude Pro**: 10-40 prompts per 5 hours (~44K tokens)

**Typical Session** (24K = 54%):
- Session start: 2K
- Load skill: 1K
- Triage: 2K
- Plan: 3K
- Extract: 5K
- Reset: 1K
- Extract: 5K
- Docs: 3K
- Test: 2K

## 🎯 ACP Priorities

1. **NetworkEnvironment** (330 lines) → extract + vectorize
2. **run_corrected_experiment()** (186 lines) → extract + config
3. **Agent logic** → vectorize

## 🆘 Troubleshooting

**High tokens?** → Reset more often (`/clear` + catchup)
**Tests fail?** → STOP, fix, then continue
**Lost context?** → `/clear` + catchup workflow
**Workflow not found?** → Check path: `.claude/skills/refactoring/workflows/`

---
**Print this card or keep it handy during development sessions!**
