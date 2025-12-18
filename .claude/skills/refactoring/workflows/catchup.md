---
name: catchup
description: "Resume work after context reset - reads changes and progress"
---

# Resume Refactoring Session

This workflow restores context after running `/clear` so you can continue refactoring where you left off.

## Purpose

Use this workflow when:
- You've run `/clear` to reset context
- You're starting work after a break
- Your session was interrupted
- You need to refresh understanding of recent changes

**âš ï¸ IMPORTANT:** Always run `/clear` + `catchup` every 5-7 prompts to maintain optimal performance within Claude Pro budget limits.

## Step 1: Check Git Status

Understand the current state of the repository:

```bash
# Check current branch and status
git status

# Check for uncommitted changes
git diff --name-only

# Check for committed but unpushed changes
git log --oneline origin/main..HEAD 2>/dev/null || git log --oneline -5
```

**Report:**
```markdown
### Repository Status

**Branch:** {current-branch}
**Uncommitted changes:** {X files}
**Unpushed commits:** {Y commits}
**Last commit:** {hash} - {message}
```

## Step 2: Read Progress Tracking File

Check if there's a progress tracking file:

```bash
# Check for refactoring progress file
cat REFACTOR_PROGRESS.md 2>/dev/null || echo "No progress file found"
```

**If file exists:**
- Read the entire file
- Extract the goal, plan, and current progress
- Note any blockers or issues

**Report:**
```markdown
### Refactoring Progress

**Goal:** {from progress file}
**Started:** {date/time}
**Files completed:** {list}
**Files in progress:** {list}
**Files pending:** {list}
**Blockers:** {any issues noted}
```

**If no progress file:**
- Report that no formal progress tracking found
- Will rely on git history

## Step 3: Analyze Modified Files

For each modified file (up to 10 files max):

### 3a. Show File Diff Stats

```bash
git diff --stat {file}
```

### 3b. Read Current File Content

Read the modified file to understand current state.

### 3c. Summarize Changes

For each file, provide:
```markdown
**File:** {path/to/file.ts}
- **Changes:** {+X -Y lines}
- **Summary:** {one-sentence description of what changed}
- **Current state:** {what the file does now}
- **TODOs/FIXMEs:** {any found in comments}
```

**If > 10 files modified:**
Report file count and ask user which files to focus on.

## Step 4: Analyze Recent Commits

Look at commit history to understand what's been done:

```bash
# Get recent commits with stats
git log --oneline --stat -5
```

**Extract:**
- What was accomplished in recent commits
- Pattern of changes (extraction, modernization, etc.)
- Commit message themes

**Report:**
```markdown
### Recent Work

**Last 5 commits:**
1. {hash}: {message}
   - Files: {affected files}
   - Pattern: {what type of refactoring}

2. {hash}: {message}
   - Files: {affected files}
   - Pattern: {what type of refactoring}

...

**Work pattern identified:** {extraction / modernization / restructuring / etc.}
```

## Step 5: Check Validation Status

Verify if the codebase is in a good state:

```bash
# Check if tests pass (don't run if missing package.json)
[ -f package.json ] && echo "package.json exists" || echo "No package.json"

# Check git status for conflicts
git status --short
```

**Report:**
```markdown
### Codebase Health

**Tests:** {Unknown / Last run: result}
**Build status:** {Unknown / Last result}
**Git conflicts:** {None / {X} files}
**Uncommitted work:** {Clean / {Y} modified files}
```

## Step 6: Synthesize Current State

Combine all information into a comprehensive summary:

```markdown
## Session Resume Summary

### Where We Are

**Current branch:** {branch-name}
**Last activity:** {time since last commit}

**Refactoring Goal:** {from progress file or inferred from commits}

**Work Completed:**
- {summarize from commits and progress file}
- Modified {X} files
- Created {Y} new files
- {Z} commits made

**Current State:**
- {list modified but uncommitted files}
- Tests status: {pass/fail/unknown}
- Build status: {pass/fail/unknown}

**Files Changed:**

1. **{file1.ts}**: {summary of changes}
2. **{file2.ts}**: {summary of changes}
3. **{file3.ts}**: {summary of changes}

**Blockers/Issues:**
- {any TODOs or FIXMEs found}
- {any git conflicts}
- {any test failures noted}

### Inferred Next Steps

Based on the progress and patterns, the logical next steps appear to be:

1. **Immediate:** {what should happen next}
2. **Then:** {following step}
3. **Finally:** {completion step}

---

**Budget Status:**
- Tokens used in this catchup: ~{estimate}K
- Recommended: Check `/cost` before proceeding
```

## Step 7: Ask for Direction

Prompt the user:

```
âœ… Context restored!

I've caught up on your refactoring work. Here's what I understand:

{brief 2-3 sentence summary}

What would you like to do next?

Suggestions:
1. Continue with the next file in the plan
2. Validate current changes (run tests/type-check)
3. Commit current work before proceeding
4. Adjust the plan based on what we've learned
5. Something else?

Let me know!
```

---

## Budget Awareness

**Estimated token cost:** 1,000-2,000 tokens (depends on number of changed files)

**Recommendations:**
- Run this after EVERY `/clear`
- Don't try to resume without catchup (wastes tokens on confusion)
- If > 10 files changed, focus on most recent changes
- Keep REFACTOR_PROGRESS.md updated to make catchup faster

---

## Success Criteria

Catchup is successful when:
- âœ… Git status understood
- âœ… Recent commits analyzed
- âœ… Modified files read and summarized
- âœ… Progress file read (if exists)
- âœ… Next steps inferred
- âœ… User prompted for direction
- âœ… Context fully restored
