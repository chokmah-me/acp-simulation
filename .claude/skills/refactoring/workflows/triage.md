---
name: triage
description: "Analyze codebase to find top 3 technical debt hotspots"
---

# Codebase Triage for Refactoring

This workflow analyzes your TypeScript codebase to identify the top 3 files with the most significant technical debt.

## Purpose

Use this workflow to:
- Identify where to start refactoring
- Find "god objects" and monolithic files
- Prioritize refactoring efforts
- Understand codebase complexity

## Step 1: Scan TypeScript Files

Find all TypeScript files in the project:

```bash
# Scan for .ts files (excluding .d.ts and test files)
find . -name "*.ts" ! -name "*.d.ts" ! -name "*.test.ts" ! -name "*.spec.ts" | head -50
```

Present the list to the user:

```markdown
### TypeScript Files Found

Found {X} TypeScript files in the project:

**Source files** (showing first 50):
- {file1.ts}
- {file2.ts}
- ...

Would you like me to analyze all files, or focus on a specific directory?
```

## Step 2: Analyze Each File

For each TypeScript file, calculate a "technical debt score" based on:

### 2a. Lines of Code (LOC)
```bash
# Count lines in file
wc -l {file.ts}
```

**Scoring:**
- < 200 lines: 0 points
- 200-500 lines: 10 points
- 500-1000 lines: 30 points
- 1000-2000 lines: 60 points
- > 2000 lines: 100 points

### 2b. Cyclomatic Complexity

Count complexity indicators by reading the file:
- Nested conditionals (if/else, switch, ternary)
- Loops (for, while, forEach)
- Logical operators (&&, ||)
- Try/catch blocks

**Scoring:**
- < 10 complexity points: 0 points
- 10-20 complexity: 10 points
- 20-40 complexity: 30 points
- > 40 complexity: 50 points

### 2c. Dependency Count

Count imports/exports:
```bash
# Count import statements
grep -c "^import " {file.ts}

# Count from statements
grep -c "from " {file.ts}
```

**Scoring:**
- < 10 dependencies: 0 points
- 10-20 dependencies: 5 points
- 20-30 dependencies: 15 points
- > 30 dependencies: 30 points

### 2d. God Object Indicators

Check for mixed concerns by searching for keywords:
```bash
# Database keywords
grep -c "query\|select\|insert\|update\|delete" {file.ts}

# API/HTTP keywords
grep -c "get\|post\|put\|delete\|router\|endpoint" {file.ts}

# Business logic keywords
grep -c "calculate\|validate\|process\|transform" {file.ts}
```

**If 2+ concern types found:** +30 points

### 2e. Code Smell Indicators

```bash
# Any types
grep -c ": any" {file.ts}

# Console logs (debug code left behind)
grep -c "console.log" {file.ts}

# TODO comments
grep -c "TODO\|FIXME\|HACK" {file.ts}
```

**Scoring:**
- Each any type: +2 points
- Each console.log: +1 point
- Each TODO: +1 point

### Total Debt Score

**Debt Score = LOC score + Complexity score + Dependency score + God Object points + Code Smell points**

## Step 3: Rank Files

Sort all files by debt score (highest first).

Create a summary table:

```markdown
### Technical Debt Analysis

| Rank | File | LOC | Complexity | Dependencies | Debt Score |
|------|------|-----|------------|--------------|------------|
| 1 | file1.ts | 1500 | High | 25 | 145 |
| 2 | file2.ts | 1200 | Medium | 32 | 128 |
| 3 | file3.ts | 800 | High | 18 | 95 |
...
```

## Step 4: Generate Triage Report

Create the final report:

```markdown
### Codebase Triage Report

**ðŸŽ¯ Top 3 Refactoring Priorities:**

1. **File:** `{file1.ts}`
   - **Debt Score:** {score}/200
   - **LOC:** {lines} lines
   - **Diagnosis:** {specific issue - God Object / High Complexity / etc.}
   - **Impact:** {why this is a problem}
   - **Specific Issues:**
     - {issue 1}
     - {issue 2}
     - {issue 3}

2. **File:** `{file2.ts}`
   - **Debt Score:** {score}/200
   - **LOC:** {lines} lines
   - **Diagnosis:** {specific issue}
   - **Impact:** {why this is a problem}
   - **Specific Issues:**
     - {issue 1}
     - {issue 2}

3. **File:** `{file3.ts}`
   - **Debt Score:** {score}/200
   - **LOC:** {lines} lines
   - **Diagnosis:** {specific issue}
   - **Impact:** {why this is a problem}
   - **Specific Issues:**
     - {issue 1}
     - {issue 2}

**ðŸ“ˆ Overall Codebase Health:**
- Total files analyzed: {X}
- Average debt score: {Y}
- Files with high debt (>80): {Z}
- Recommended focus areas: {list}

**ðŸ“ˆ Next Recommended Action:**
Focus on #{ranking} priority: `{filename}`

Suggested approach:
1. Run `qplan` to design extraction strategy
2. Use `extract` workflow to decompose 1-2 functions
3. Use `modernize` workflow to update patterns
4. Iterate until file debt score < 50

**Budget Estimate:**
- High priority files: 8-12 prompts each
- Medium priority files: 5-8 prompts each
- Low priority files: 3-5 prompts each
```

## Step 5: Provide Detailed Recommendations

For the #1 priority file, provide specific recommendations:

```markdown
### Detailed Recommendations for {#1 File}

**Current State:**
- {lines} lines of code
- {complexity} cyclomatic complexity
- {dependencies} dependencies

**Quick Wins** (low effort, high impact):
1. Extract {specific function} to new module
2. Remove {X} console.log statements
3. Replace {Y} any types with specific types

**Medium Effort:**
1. Split into {X} feature modules
2. Extract database logic to separate layer
3. Convert to Result<T,E> error handling

**Long Term:**
1. Decompose into Manager/Endpoint/Database pattern
2. Move to src/features/{domain}/
3. Add comprehensive test coverage

**Estimated Effort:**
- Quick wins: 1-2 sessions (4-8 prompts)
- Medium: 3-4 sessions (12-16 prompts)
- Long term: 6-8 sessions (24-32 prompts)
```

---

## Budget Awareness

**Estimated token cost:** ~2,000 tokens

**Recommendations:**
- Run this once at the start of a refactoring project
- Re-run after major changes to track progress
- Don't run this every session (expensive)
- Save the report for reference

---

## Success Criteria

Triage is successful when:
- âœ… All .ts files analyzed
- âœ… Debt scores calculated for each file
- âœ… Top 3 priorities identified with specific issues
- âœ… Next actions recommended
- âœ… Effort estimates provided

---

## Next Steps

After triage:
1. Review top 3 files identified
2. Pick the #1 priority (or user's preference)
3. Run `qplan` to design refactoring approach
4. Use `extract` or `modernize` workflows to execute
5. Track progress in REFACTOR_PROGRESS.md
