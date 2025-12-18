# Getting Started with Claude Code Playbook

This guide will help you quickly integrate the Claude Code Playbook into your project.

## Prerequisites

- [Claude Code](https://docs.claude.com/claude-code) installed and configured
- A project with git initialized
- Basic familiarity with Claude Code commands

## Quick Start (5 minutes)

### Step 1: Clone the Playbook

```bash
git clone https://github.com/dyb5784/claude-code-playbook.git
cd claude-code-playbook
```

### Step 2: Copy Templates to Your Project

```bash
# Copy templates to your project root
cp templates/CLAUDE.md.template /path/to/your/project/CLAUDE.md
cp templates/.cursorrules.template /path/to/your/project/.cursorrules
```

### Step 3: Customize for Your Project

Edit the copied files to match your project's needs:

**CLAUDE.md:**
- Update project name and description
- Set your token budget constraints
- Define validation requirements
- Specify coding standards

**.cursorrules:**
- Adjust for your programming language
- Update architectural preferences
- Set documentation standards

### Step 4: Start Using Claude Code

In your project directory:

```bash
# Initialize a session
/clear
claude skills refactoring qnew

# Analyze your codebase
claude skills refactoring triage
```

## Choosing the Right Skill

### For Python Scientific Computing

Use when working on:
- Numerical simulations
- Statistical analysis
- Data processing
- Research code
- Performance optimization

**How to load:**
```bash
view skills/python-scientific/SKILL.md
```

### For General Refactoring

Use when:
- Restructuring code
- Adding new features
- Reducing technical debt
- Modernizing patterns

**How to use:**
```bash
claude skills refactoring <workflow-name>
```

## Session Management Best Practices

### The 5-7 Prompt Rule

**Every 5-7 prompts, reset:**
```bash
/cost                              # Check usage
/clear                             # Reset context
claude skills refactoring catchup  # Restore context
```

**Why?** Prevents context degradation and optimizes token usage.

### Budget Tracking

Check cost every 3 prompts:
```bash
/cost
```

**Typical session:** 22K tokens (50% of Claude Pro budget)

## Your First Refactoring Session

### 1. Start Fresh
```bash
/clear
claude skills refactoring qnew
```

### 2. Identify Targets
```bash
claude skills refactoring triage
```

### 3. Plan Your Approach
```bash
claude skills refactoring qplan
```

### 4. Extract a Function
```bash
claude skills refactoring extract
```

### 5. Check Budget
```bash
/cost
```

### 6. Reset and Continue
```bash
/clear
claude skills refactoring catchup
```

## Common Workflows

### Find Technical Debt
```bash
claude skills refactoring triage
```

### Extract a Function
```bash
claude skills refactoring extract
```

### Modernize Code
```bash
claude skills refactoring modernize
```

### Batch Implementation
```bash
claude skills refactoring qcode
```

## Tips for Success

1. **Start small**: Extract 1-2 functions per session
2. **Validate constantly**: Run tests after each change
3. **Track progress**: Document in REFACTOR_PROGRESS.md
4. **Commit often**: Every 2-4 files
5. **Follow patterns**: Use examples from SKILL.md files

## Troubleshooting

### "Workflow not found"
- Check you're in the correct directory
- Verify the playbook is cloned
- Ensure skills directory structure is intact

### High token usage
- Use `/clear` + `catchup` more frequently
- Reduce batch sizes
- Focus on one pattern at a time

### Poor quality suggestions
- Verify CLAUDE.md is customized for your project
- Ensure you're following the session reset protocol
- Check that you're loading the appropriate skill

## Next Steps

- Read [WORKFLOW_GUIDE.md](WORKFLOW_GUIDE.md) for detailed workflow documentation
- Explore [skills/README.md](../skills/README.md) for skill selection guidance
- Check out the examples in `examples/` directory
- Consider contributing your own skills!

---

**Need help?** Open an issue on GitHub or check the [Claude Code Documentation](https://docs.claude.com/claude-code).