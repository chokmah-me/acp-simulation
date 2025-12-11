# Project Refactoring Constitution

> Systematic transformation from monolithic architecture to modern modular patterns

---

## ⚠️ BUDGET CONSTRAINTS

**Claude Pro Subscription Limits:**
- 10-40 prompts per 5-hour window
- ~44,000 tokens total per window
- Always use Sonnet 4.5 (NOT Opus)

**Session Management:**
- Run `/cost` every 3 prompts to track token usage
- Run `/clear` + `catchup` every 5-7 prompts
- Batch work into 10-15 file increments maximum
- Stop if token usage exceeds 30K in a session

---

## ARCHITECTURAL GOALS

**Target State:** Modern modular architecture with feature-based organization

**Current State → Future State:**

| Current | Target |
|---------|--------|
| Monolithic files | Feature modules under `/src/features/` |
| Class inheritance | Functional composition with factory functions |
| Throw/catch error handling | Result<T,E> monads |
| Hardcoded business logic | Configuration-driven logic |
| Mixed concerns (god objects) | Manager/Endpoint/Database layers |
| Flat file structure | Domain-organized features |

**Key Modern Patterns:**
1. **Feature-based modules:** `src/features/{domain}/{manager,endpoint,database,types}.ts`
2. **Result monads:** All fallible operations return `Result<T, Error>`
3. **Functional composition:** Factory functions instead of classes
4. **Dependency injection:** Pass dependencies as parameters
5. **Configuration-driven:** Extract rules to config objects

**Reference:** See [.claude/skills/refactoring/knowledge/architecture-patterns.md](.claude/skills/refactoring/knowledge/architecture-patterns.md)

---

## REFACTORING WORKFLOWS

Use the refactoring skills system for all work:

**Start Every Session:**
```bash
/clear
claude skills refactoring qnew
```

**Find What to Refactor:**
```bash
claude skills refactoring triage
```

**Plan Before Implementing:**
```bash
claude skills refactoring qplan
```

**Execute Refactoring:**
```bash
# For single function extraction
claude skills refactoring extract

# For pattern modernization
claude skills refactoring modernize

# For batch operations (after plan approval)
claude skills refactoring qcode
```

**Resume After Context Reset:**
```bash
/clear
claude skills refactoring catchup
```

**See:** [.claude/skills/refactoring/SKILL.md](.claude/skills/refactoring/SKILL.md) for complete workflow documentation.

---

## VALIDATION RULES

**Before ANY commit, ALL checks must pass:**

1. **Type Check:**
   ```bash
   npm run type-check
   ```
   **Expected:** 0 errors
   **If fails:** STOP and fix TypeScript errors before proceeding

2. **Unit Tests:**
   ```bash
   npm run test:unit
   ```
   **Expected:** All tests pass
   **If fails:** STOP and fix failing tests before proceeding

3. **Linting:**
   ```bash
   npm run lint
   ```
   **Expected:** 0 errors, 0 warnings
   **If fails:** Try `npm run lint -- --fix`, then manually fix remaining

**If ANY validation fails: DO NOT PROCEED. Fix the issue first.**

---

## API SURFACE PROTECTION

**Before modifying any exported function, class, or module:**

1. Search for all usages:
   ```bash
   grep -r "functionName" src/
   ```

2. Analyze impact of changes

3. Propose migration plan if breaking changes needed

4. Get explicit user approval before modifying

**Backwards compatibility is critical. When in doubt, ask.**

---

## COMMIT GUIDELINES

**Commit Frequency:**
- Commit after every 2-4 files modified
- Don't accumulate large changesets
- Atomic commits: one logical change per commit

**Commit Message Format:**
```
refactor: {brief description}

{detailed description of changes}

Changes:
- {specific change 1}
- {specific change 2}
- {specific change 3}

Tests: {passing/fixed}
Types: {passing}
Lint: {clean}

{context about why this change was made}
```

**Example:**
```
refactor: extract validateUserInput from main module

Extracted user validation logic to improve modularity and testability.

Changes:
- Created src/features/user/validate.ts with validation functions
- Updated main module to import and use new validation module
- Added 10 unit tests for validation logic
- All tests passing, type-check clean

Tests: 10 new tests, all passing
Types: No errors
Lint: Clean

Part of decomposing monolithic module (1200 LOC → target 500 LOC).
```

---

## PROGRESS TRACKING

**For multi-session refactorings, maintain `REFACTOR_PROGRESS.md`:**

```markdown
# Refactoring Progress

## Current Goal
Decompose monolithic module

## Session Info
- Started: 2025-12-01
- Token budget used: 18K / 44K
- Prompts used: 14 / 40

## Completed
- [x] Extracted validateUserInput (lines 145-230)
  - Created src/features/user/validate.ts
  - Added 10 tests, all passing
- [x] Extracted formatMessage (lines 350-420)
  - Created src/features/messages/format.ts
  - Added 8 tests, all passing

## In Progress
- [ ] Extract command parsing logic

## Pending
- [ ] Extract event handlers
- [ ] Modernize error handling to Result<T,E>
- [ ] Move to src/features/

## Blockers
None currently

## Notes
- Main module: 1200 LOC → 950 LOC (target: <500)
- All validations passing
- Need to check for circular dependencies before next extraction
```

---

## SESSION RESET PROTOCOL

**Every 5-7 prompts, execute this protocol:**

1. Check token usage:
   ```bash
   /cost
   ```

2. If > 5 prompts or > 12K tokens:
   ```bash
   /clear
   claude skills refactoring catchup
   ```

3. Continue work with restored context

**Why:** Prevents context degradation, saves tokens, maintains quality.

---

## ERROR HANDLING STRATEGY

**When TypeScript strict mode errors appear:**

1. **STOP immediately** - Do not proceed with other work
2. Read the error message carefully
3. Understand the root cause
4. Fix the error
5. Re-run type-check
6. Only proceed once type-check passes

**When tests fail:**

1. **STOP immediately**
2. Read test failure output
3. Determine if issue is:
   - Test needs updating (behavior intentionally changed)
   - Implementation is broken (unintentional behavior change)
4. Fix appropriately
5. Re-run tests
6. Only proceed once all tests pass

**When you're unsure:**
- Ask the user for guidance
- Don't guess or make assumptions
- Better to ask than to break things

---

## MINIMUM VIABLE REFACTOR

**Immediate Goal:** Keep application operational while refactoring

**Non-Negotiable:**
- Application must start without errors
- All features must continue working
- Events must be handled
- No user-facing behavior changes (unless explicitly requested)

---

## LEARNING AND IMPROVEMENT

**After Each Session:**
- Update REFACTOR_PROGRESS.md
- Note what worked well
- Note what was challenging
- Adjust approach for next session

**After Each Milestone:**
- Review overall progress
- Update this CLAUDE.md if needed
- Share learnings with team
- Celebrate progress!

---

## USEFUL REFERENCES

**In This Project:**
- [.claude/skills/refactoring/SKILL.md](.claude/skills/refactoring/SKILL.md) - Workflow documentation
- [.claude/skills/refactoring/knowledge/typescript-style.md](.claude/skills/refactoring/knowledge/typescript-style.md) - TypeScript patterns
- [.claude/skills/refactoring/knowledge/architecture-patterns.md](.claude/skills/refactoring/knowledge/architecture-patterns.md) - Modern architecture patterns

---

**Last Updated:** 2025-12-01
**Version:** 3.0.0
**License:** MIT
