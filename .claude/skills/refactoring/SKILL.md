# Skill: Code Refactoring
> "The art of refactoring is leaving the codebase cleaner than you found it."

## Overview
This skill provides a comprehensive suite of workflows for surgical and safe modernization of legacy codebases. It works with your project's `CLAUDE.md` constitution, emphasizing iterative changes, budget awareness, and test-driven validation.

**Primary Goal:** Transform monolithic, tightly-coupled code into modular, maintainable, well-tested components following modern architectural patterns.

**Pro Subscription Awareness:** All workflows are designed to work within 10-40 prompts per 5-hour window. Use `/cost` every 3 prompts to track token burn.

---

## 📂 Skill Structure

```
.claude/skills/refactoring/
├── SKILL.md              # This file - overview and router
├── workflows/            # Executable task prompts
│   ├── triage.md         # Find technical debt hotspots
│   ├── extract.md        # Extract code into modules
│   ├── modernize.md      # Update to modern patterns
│   ├── catchup.md        # Resume after context reset
│   ├── qnew.md           # Start new session
│   ├── qplan.md          # Validate refactoring plan
│   └── qcode.md          # Full implementation with verification
└── knowledge/            # Reference documentation
    ├── typescript-style.md    # TypeScript patterns and style
    └── architecture-patterns.md   # Modern architecture patterns
```

---

## 🎯 Available Workflows

Run any workflow with: `claude skills refactoring <workflow-name>`

| Workflow | Purpose | Token Cost | When to Use |
|----------|---------|------------|-------------|
| **triage** | Find top 3 technical debt hotspots | ~2K | Start of refactoring project |
| **extract** | Extract code block to new module | ~5K | Targeted function decomposition |
| **modernize** | Update syntax and patterns | ~4K | Post-extraction cleanup |
| **catchup** | Resume after `/clear` | ~1-2K | Every 5-7 prompts |
| **qnew** | Fresh session initialization | ~2K | Start of work session |
| **qplan** | Validate refactoring plan | ~3K | Before implementation |
| **qcode** | Full implementation cycle | ~8-12K | Execute approved plan |

### Workflow Details

**triage** - Codebase Analysis
- Scans TypeScript files for complexity, LOC, dependencies
- Calculates technical debt scores
- Identifies top 3 refactoring priorities
- Provides effort estimates

**extract** - Function Extraction
- Analyzes code block for dependencies
- Creates new module with proper types
- Updates original file with imports
- Adds unit tests
- Validates with type-check/tests/lint

**modernize** - Pattern Modernization
- Converts `.then()` to `async/await`
- Adds Result<T,E> error handling
- Replaces classes with functions
- Improves type safety (removes `any`)
- Adds JSDoc documentation

**catchup** - Context Restoration
- Reads git diff and recent commits
- Summarizes changed files
- Reads REFACTOR_PROGRESS.md
- Infers next steps
- Restores work context

**qnew** - Session Initialization
- Reads CLAUDE.md and project structure
- Confirms understanding of constraints
- Checks for in-progress work
- Prompts for session goal

**qplan** - Plan Validation
- Checks alignment with modern patterns
- Searches for similar implementations
- Assesses minimalism and testability
- Identifies risks
- Provides go/no-go verdict

**qcode** - Full Implementation
- Executes approved plan file-by-file
- Validates after each file
- Tracks progress in REFACTOR_PROGRESS.md
- Generates UX test scenarios
- Commits incrementally

---

## 🔄 Refactoring Process (5-Step Cycle)

**1. Triage** → `claude skills refactoring triage`
- Identify top 3 debt hotspots
- Pick target file

**2. Plan** → `claude skills refactoring qplan`
- Design refactoring approach
- Validate against patterns
- Get approval

**3. Extract** → `claude skills refactoring extract`
- Break down code systematically
- One function at a time

**4. Modernize** → `claude skills refactoring modernize`
- Update patterns in extracted code
- Add documentation

**5. Reset** → `/clear` then `claude skills refactoring catchup`
- Continue with next target

**⚠️ Session Reset Protocol:** Execute `/clear` after every 5-7 prompts to avoid context degradation. Token budget is limited—resetting early saves tokens and maintains quality.

---

## 🧠 Knowledge Base

The `knowledge/` directory contains reference documentation that workflows automatically use:

**typescript-style.md**
- Async/await over promises
- Result<T,E> error handling
- Functional composition patterns
- Type safety guidelines
- Documentation standards

**architecture-patterns.md**
- Feature-based module structure
- Manager/Endpoint/Database layers
- Result monad implementation
- Dependency injection patterns
- Migration strategies

**How Workflows Use Knowledge:**
Workflows automatically reference these files when making decisions about code structure and patterns. You don't need to explicitly tell Claude to read them—they're part of the skill's context.

---

## 💡 Field-Tested Best Practices

### Session Management
- **Never** skip `/clear + catchup` protocol
- **Always** run `/cost` every 3 prompts
- **Stop** if TypeScript errors appear—fix before continuing
- **Batch** changes into 10-15 file increments max
- **Document** progress in `REFACTOR_PROGRESS.md`

### Workflow Selection
- Use **triage** once per project/sprint
- Use **qnew** at session start
- Use **qplan** before major changes
- Use **extract** for surgical extractions
- Use **modernize** for pattern updates
- Use **qcode** only after plan approval
- Use **catchup** after every `/clear`

### Budget Optimization
- Triage: Run once, save results
- Extract: 1-2 functions per session
- Modernize: 1-2 files per session
- qcode: Max 15 files per invocation
- catchup: Cheap insurance—use liberally

### Quality Gates
Every change must pass:
1. `npm run test:unit` → All tests pass
2. `npm run type-check` → No TypeScript errors
3. `npm run lint` → No linting errors

If ANY fail: STOP and fix before proceeding.

---

## ⚠️ Common Pitfalls to Avoid

**Pitfall:** Trying to refactor too much at once
**Solution:** Stick to 1-2 functions per extract session

**Pitfall:** Not validating after each file
**Solution:** Run tests/type-check after EVERY modification

**Pitfall:** Forgetting to commit incrementally
**Solution:** Commit every 2-4 files, don't wait until end

**Pitfall:** Ignoring the `/clear + catchup` protocol
**Solution:** Set a timer, reset every 5-7 prompts religiously

**Pitfall:** Not tracking progress
**Solution:** Maintain REFACTOR_PROGRESS.md for complex refactorings

**Pitfall:** Skipping the qplan validation
**Solution:** Always validate plans before expensive qcode execution

---

## 📊 Budget Management

### Token Budget Guidelines

**Claude Pro Subscription:**
- 10-40 prompts per 5-hour window
- ~1,100 tokens average per prompt
- Total: ~44,000 tokens per window

**Workflow Costs:**
- triage: 2K tokens (run once)
- qnew: 2K tokens (per session)
- qplan: 3K tokens (per plan)
- extract: 5K tokens (per function)
- modernize: 4K tokens (per file)
- qcode: 8-12K tokens (per batch)
- catchup: 1-2K tokens (per reset)

**Example Budget Allocation:**
```
Session 1 (within 5-hour window):
- qnew: 2K
- triage: 2K
- qplan: 3K
- extract #1: 5K
- /clear + catchup: 1K
- extract #2: 5K
- /cost check
- modernize: 4K
Total: ~22K tokens (50% of budget)
```

### When to Stop and Reset

**Immediate stop if:**
- Tests fail unexpectedly
- TypeScript strict mode errors
- Token usage > 30K in session
- Confusion about next steps

**Planned resets:**
- After every 5-7 prompts
- Before starting new major task
- When switching between files
- After completing logical unit

---

## 🎓 Learning Curve

**Beginner** (First 2 sessions):
1. Start with qnew
2. Run triage to understand codebase
3. Pick the easiest target (smallest file)
4. Use extract for just 1 function
5. Practice /clear + catchup
6. Get comfortable with validation checks

**Intermediate** (Sessions 3-10):
1. Use qplan before extractions
2. Extract 2-3 functions per session
3. Add modernize to your workflow
4. Maintain REFACTOR_PROGRESS.md
5. Commit incrementally

**Advanced** (Sessions 10+):
1. Use qcode for batch operations
2. Refactor 10-15 files per session
3. Design custom extraction strategies
4. Contribute patterns to knowledge base
5. Mentor others on the team

---

## 🚀 Quick Start Guide

**Your First Refactoring Session:**

```bash
# 1. Start session
/clear
claude skills refactoring qnew

# 2. Identify targets
claude skills refactoring triage

# 3. Plan approach (for top priority file)
claude skills refactoring qplan

# 4. Extract first function
claude skills refactoring extract

# 5. Check budget
/cost

# 6. Reset context (if > 5 prompts)
/clear
claude skills refactoring catchup

# 7. Continue with next function or modernize
```

---

## 📈 Success Metrics

Track these to measure refactoring progress:

**Code Quality:**
- Lines of code per file (target: <500)
- Cyclomatic complexity (target: <10)
- Test coverage (target: >80%)
- TypeScript strict mode compliance (target: 100%)

**Technical Debt:**
- God object count (target: 0)
- Files with mixed concerns (target: 0)
- `any` type usage (target: 0)
- TODOs/FIXMEs (target: all tracked)

**Process:**
- Token efficiency (actual vs. estimated)
- Time to complete extraction (track and improve)
- Test failures per session (target: <2)
- Rework required (target: <10%)

---

## 🤝 Team Collaboration

**For Team Leads:**
- Share CLAUDE.md across the team
- Standardize on workflows
- Review progress files in standups
- Track token budget usage
- Celebrate successful extractions

**For Individual Contributors:**
- Follow the workflow order
- Document in REFACTOR_PROGRESS.md
- Write descriptive commit messages
- Share learnings in retrospectives
- Update knowledge base with new patterns

---

## 📚 Additional Resources

**In This Skill:**
- [knowledge/typescript-style.md](knowledge/typescript-style.md) - TypeScript patterns
- [knowledge/architecture-patterns.md](knowledge/architecture-patterns.md) - Modern architecture patterns
- [workflows/](workflows/) - All executable workflows

**External:**
- Claude Code Documentation: https://docs.claude.com/claude-code
- Refactoring Book: Martin Fowler's "Refactoring"
- TypeScript Handbook: https://www.typescriptlang.org/docs/

---

## 🆘 Getting Help

**If workflows aren't working:**
1. Check file paths are correct
2. Verify CLAUDE.md exists in project root
3. Ensure git is initialized
4. Confirm package.json has test/lint commands

**If results are poor quality:**
1. Are you using /clear + catchup protocol?
2. Are you running validations after each change?
3. Is your CLAUDE.md clear and specific?
4. Are you batching too many changes?

**If hitting budget limits:**
1. Run /cost more frequently
2. Use catchup more aggressively
3. Reduce batch sizes
4. Focus on one pattern at a time

---

**Last Updated:** 2025-12-01
**Version:** 3.0.0
**License:** MIT
**Author:** Public contribution to AI-assisted development
