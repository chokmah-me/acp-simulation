---
name: qnew
description: "Start new refactoring session with context loading"
---

# Start New Refactoring Session

This workflow initializes a new refactoring session by loading project context and confirming understanding.

## Purpose

Use this workflow at the start of:
- A new work session (morning, after break)
- After `/clear` when starting fresh
- When switching between projects
- When you want to verify Claude understands the project

## Step 1: Load Project Constitution

Read the project's CLAUDE.md file to understand constraints and goals.

```
Reading: CLAUDE.md
```

**Extract key information:**
- Budget constraints (Claude Pro: 10-40 prompts per 5 hours)
- Architectural goals (modern patterns, functional composition, Result monads)
- Non-negotiable rules (API surface preservation, test requirements)
- Diagnostic commands (type-check, test:unit, lint)
- Current refactoring objectives

## Step 2: Load Additional Context

Read supporting configuration files if they exist:

```
Reading: .cursorrules (if exists)
Reading: .claude/skills/refactoring/knowledge/typescript-style.md
Reading: .claude/skills/refactoring/knowledge/architecture-patterns.md
```

## Step 3: Scan Project Structure

Get a high-level view of the project:

```bash
# Check directory structure
ls -la

# Check for TypeScript project files
ls package.json tsconfig.json

# Scan source directory structure
ls src/
```

**Understand:**
- Project type (web app, API, library, etc.)
- Main source directories
- Test directory location
- Configuration files present

## Step 4: Check Available Commands

Verify the test/lint/build commands:

```
From package.json scripts:
- npm run test:unit â†’ Run unit tests
- npm run type-check â†’ TypeScript validation
- npm run lint â†’ Linting
- npm run dev â†’ Development server
- npm run build â†’ Production build
```

**Note:** If package.json is missing or commands differ from CLAUDE.md, report this discrepancy.

## Step 5: Confirm Understanding

Provide a summary of your understanding:

```markdown
## Session Initialization Complete

### Project Overview
**Type:** [Web app / API / Library]
**Language:** TypeScript
**Architecture:** [Current state description]

### Refactoring Goals
- Target: Modern patterns (feature modules, functional composition, Result monads)
- Current state: [Monolithic / Partially modularized / etc.]
- Priority: [From CLAUDE.md]

### Constraints
- Budget: Claude Pro (10-40 prompts per 5 hours)
- Model: Sonnet 4.5 only
- Batch size: 10-15 files per session max
- Testing: All changes must pass tests before commit

### Available Workflows
- `triage` - Find refactoring targets
- `extract` - Extract functions to modules
- `modernize` - Update to modern patterns
- `qplan` - Validate refactoring plan
- `qcode` - Execute with verification
- `catchup` - Resume after /clear

### Validation Commands
- Tests: `npm run test:unit`
- Types: `npm run type-check`
- Lint: `npm run lint`

### Session Protocol
- Run `/cost` every 3 prompts
- Run `/clear` + `catchup` every 5 prompts
- Commit after each logical unit of work
```

## Step 6: Check for In-Progress Work

Look for signs of ongoing refactoring:

```bash
# Check git status
git status

# Check for progress tracking file
cat REFACTOR_PROGRESS.md 2>/dev/null || echo "No progress file found"

# Check recent commits
git log --oneline -5
```

**If work is in progress:**
- Report uncommitted changes
- Read REFACTOR_PROGRESS.md if it exists
- Suggest running `catchup` instead of starting fresh

**If clean slate:**
- Confirm ready to start new work

## Step 7: Ask for Today's Goal

Prompt the user:

```
âœ… Context loaded and understood!

I'm ready to help with refactoring. What would you like to work on today?

Suggestions based on project state:
1. Run `triage` to identify technical debt hotspots
2. Continue existing refactoring work (if in progress)
3. Extract a specific function or module
4. Modernize a specific file's patterns
5. Something else?

What's your goal for this session?
```

---

## What This Workflow Does NOT Do

- Does NOT make any code changes
- Does NOT run tests or builds
- Does NOT create or modify files
- Does NOT commit anything

**This is purely a context-loading and confirmation workflow.**

---

## Budget Awareness

**Estimated token cost:** ~2,000 tokens

**Recommendations:**
- Run this at the start of every session
- Run this after `/clear` when resuming work
- If context hasn't changed much, you can skip this and dive right in

---

## Success Criteria

Session initialization is successful when:
- âœ… CLAUDE.md understood (or absence noted)
- âœ… Project type identified
- âœ… Test/lint commands known
- âœ… Architectural goals clear
- âœ… Budget constraints understood
- âœ… User prompted for goal
