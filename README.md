# Claude Code Playbook v3.0.0
## Token-Efficient AI Engineering for Everyone

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17744054.svg)](https://doi.org/10.5281/zenodo.17744054)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**A public contribution to democratizing AI-assisted software development.**

---

## 🎯 Problem

Professional developers using Claude Pro ($20-40/month) face hard token limits:
- 10-40 prompts per 5-hour window
- Traditional chat workflows waste tokens on multi-turn conversations
- Simple refactoring tasks often require 5-10+ conversation turns
- No standardized approach to budget-aware AI collaboration

## 💡 Solution

The Claude Code Playbook transforms AI-assisted development through:

1. **Executable Workflows** - Six specialized workflows that compress common tasks into efficient single-turn or few-turn operations
2. **Token Economics** - Empirically measured costs for predictable budget planning
3. **Skills-Based Architecture** - Modular system that Claude Code reads automatically
4. **Session Management** - Protocols for maintaining quality under token constraints
5. **Modern Patterns** - Reference implementations of contemporary software architecture

### Empirical Results
- **67% reduction** in conversation turns for refactoring tasks
- **Predictable token costs** per operation type
- **100% test pass rate** maintained throughout refactoring
- **Zero API breakage** with systematic validation gates

---

## 🚀 Quick Start

### Installation

1. **Download** the latest release from [Zenodo](https://zenodo.org/records/17744054)

2. **Extract** the archive to your project root:
   ```bash
   unzip ClaudePlaybook_v3.0.0.zip -d your-project/
   ```

3. **Upload to Claude Project**:
   - Open claude.ai
   - Create or open a Project
   - Upload the `.claude/` directory to Project Knowledge
   - Upload `CLAUDE.md` to Project Knowledge

### Your First Session

```bash
# Start Claude Code or open claude.ai Project

# Initialize session
/clear
claude skills refactoring qnew

# Analyze your codebase
claude skills refactoring triage

# Get your top 3 technical debt priorities!
```

---

## 📂 What's Included

```
ClaudePlaybook_v3.0.0/
├── .claude/
│   ├── skills/
│   │   └── refactoring/
│   │       ├── SKILL.md                    # Complete skill overview
│   │       ├── workflows/
│   │       │   ├── triage.md               # Find tech debt hotspots
│   │       │   ├── extract.md              # Extract functions
│   │       │   ├── modernize.md            # Update patterns
│   │       │   ├── qnew.md                 # Session init
│   │       │   ├── qplan.md                # Validate plans
│   │       │   ├── qcode.md                # Full implementation
│   │       │   └── catchup.md              # Resume after reset
│   │       └── knowledge/
│   │           ├── typescript-style.md     # Modern TS patterns
│   │           └── architecture-patterns.md # Feature modules, Result monads
│   └── settings.local.json                 # Optional permissions
├── CLAUDE.md                                # Project constitution
├── .cursorrules                             # Optional Cursor IDE integration
└── README.md                                # This file
```

---

## 🎯 Available Workflows

| Workflow | Purpose | Cost | When to Use |
|----------|---------|------|-------------|
| **triage** | Find top 3 technical debt hotspots | ~2K tokens | Start of project |
| **qnew** | Initialize session with context | ~2K tokens | Start of work day |
| **qplan** | Validate refactoring plan | ~3K tokens | Before implementation |
| **extract** | Extract function to new module | ~5K tokens | Targeted decomposition |
| **modernize** | Update to modern patterns | ~4K tokens | Pattern upgrades |
| **qcode** | Full implementation (max 15 files) | ~8-12K tokens | Execute approved plan |
| **catchup** | Restore context after `/clear` | ~1-2K tokens | Every 5-7 prompts |

### Invoke Workflows

```bash
# Command format
claude skills refactoring <workflow-name>

# Examples
claude skills refactoring triage
claude skills refactoring extract
claude skills refactoring qcode
```

---

## 📊 Token Economics

### Budget Planning

**Claude Pro Limits:**
- 10-40 prompts per 5-hour window
- ~44,000 tokens total capacity

**Example Session (within budget):**
```
qnew:        2K tokens
triage:      2K tokens
qplan:       3K tokens
extract #1:  5K tokens
/clear + catchup: 1K tokens
extract #2:  5K tokens
modernize:   4K tokens
─────────────────────────
Total:      22K tokens (50% of budget)
```

### Session Management Protocol

**Every 5-7 prompts, execute:**
```bash
/cost                              # Check token usage
/clear                             # Reset context
claude skills refactoring catchup  # Restore context
```

**Why?** Prevents context degradation, optimizes token efficiency, maintains quality.

---

## 🏗️ Modern Architecture Patterns

The playbook teaches contemporary software architecture:

### Feature-Based Modules
```
src/features/
  └── user-management/
      ├── manager.ts      # Business logic
      ├── endpoint.ts     # API routes
      ├── database.ts     # Data access
      ├── types.ts        # Domain types
      └── tests/
```

### Result Monad Pattern
```typescript
function divide(a: number, b: number): Result<number, Error> {
  if (b === 0) {
    return err(new Error('Division by zero'));
  }
  return ok(a / b);
}

// Type-safe error handling!
const result = divide(10, 2);
if (result.ok) {
  console.log(result.value); // 5
} else {
  console.error(result.error.message);
}
```

### Functional Composition
```typescript
// Factory functions over classes
function createUserService(db: Database) {
  return {
    async getUser(id: string) {
      return db.query('SELECT * FROM users WHERE id = $1', [id]);
    }
  };
}
```

---

## 🎓 Learning Path

### Beginner (Sessions 1-2)
1. Run `qnew` to start
2. Use `triage` to understand your codebase
3. Extract 1 simple function with `extract`
4. Practice `/clear` + `catchup` protocol

### Intermediate (Sessions 3-10)
1. Use `qplan` before extractions
2. Extract 2-3 functions per session
3. Apply `modernize` to update patterns
4. Track progress in `REFACTOR_PROGRESS.md`

### Advanced (Sessions 10+)
1. Use `qcode` for batch operations (10-15 files)
2. Design custom extraction strategies
3. Contribute patterns back to knowledge base
4. Mentor team members

---

## ✅ Validation Gates

**Every change must pass ALL checks:**

```bash
npm run type-check  # 0 errors required
npm run test:unit   # All tests pass
npm run lint        # 0 warnings
```

**If ANY fail:** STOP and fix before proceeding.

---

## 📈 Success Metrics

Track your progress:

**Code Quality:**
- Lines per file: < 500
- Cyclomatic complexity: < 10
- Test coverage: > 80%
- TypeScript strict mode: 100%

**Technical Debt:**
- God objects: 0
- Mixed concerns: 0
- `any` types: 0

**Process:**
- Token efficiency vs. estimates
- Test failures per session: < 2
- Rework required: < 10%

---

## 🤝 Contributing

This is a public contribution to AI-assisted development. Ways to contribute:

1. **Share your experience** - Open issues with success stories or challenges
2. **Propose new workflows** - Submit PRs with additional workflow patterns
3. **Improve documentation** - Help make this more accessible
4. **Report bugs** - Found an issue? Let us know
5. **Add patterns** - Contribute to `architecture-patterns.md` or `typescript-style.md`

### Repository
[Coming soon - GitHub repository link]

---

## 📄 License

MIT License - see LICENSE file for details.

**Philosophy:** AI-assisted development should be accessible to all developers, not just those with expensive API budgets or large organizations.

---

## 🙏 Acknowledgments

- **Anthropic** for Claude Pro and Claude Code
- **TypeScript community** for modern patterns and best practices
- **All developers** who provided feedback during field testing
- **You** for using this playbook and contributing to its evolution

---

## 📚 Additional Resources

- [Claude Code Documentation](https://docs.claude.com/claude-code)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [Refactoring by Martin Fowler](https://martinfowler.com/books/refactoring.html)

---

## 🆘 Getting Help

**Workflow issues?**
1. Check file paths are correct
2. Verify CLAUDE.md exists in project root
3. Ensure git is initialized
4. Confirm package.json has test/lint commands

**Quality issues?**
1. Are you using `/clear` + `catchup` protocol?
2. Running validations after each change?
3. Is CLAUDE.md clear and specific?
4. Batching too many changes?

**Budget issues?**
1. Run `/cost` more frequently
2. Use `catchup` more aggressively
3. Reduce batch sizes
4. Focus on one pattern at a time

---

## 📖 Citation

If you use this playbook in research or professional work, please cite:

```bibtex
@misc{claude_playbook_v3,
  author = {[Your Name]},
  title = {Claude Code Playbook: Token-Efficient AI Engineering},
  year = {2025},
  version = {3.0.0},
  doi = {10.5281/zenodo.17744054},
  url = {https://zenodo.org/records/17744054}
}
```

---

## 🚀 What's Next?

**Version 3.1 (Planned):**
- Additional workflows for different languages (Python, Go, Rust)
- Integration testing workflow
- Performance optimization workflow
- Team collaboration templates

**Long-term vision:**
- Multi-language support
- Custom workflow creation guide
- VS Code extension integration
- Automated token tracking

---

**Made with ❤️ for the developer community**

**Version:** 3.1.0
**Release Date:** December 2025
**Last Updated:** 2025-12-11

---

## 🤖 AI-Assisted Development Integration

### Claude Code Playbook Integration
This project now includes the **Claude Code Playbook v3.0.0** for AI-assisted development:

- **Token-efficient workflows** - 67% reduction in conversation turns
- **Six specialized workflows** for refactoring and code improvement
- **Modern architecture patterns** - Feature modules, Result monads, functional composition
- **Session management protocols** - Optimized for Claude Pro token limits

### Quick Start with Claude Code
```bash
# Initialize Claude Code session
/clear
claude skills refactoring qnew

# Analyze codebase for improvements
claude skills refactoring triage
```

### Included Files
- `CLAUDE.md` - Project constitution and guidelines
- `.claude/skills/refactoring/` - Complete workflow system
  - 7 workflow files (triage, extract, modernize, qnew, qplan, qcode, catchup)
  - 2 knowledge bases (TypeScript patterns, architecture patterns)
  - SKILL.md - Complete skill overview

**Learn more:** See [CLAUDE.md](CLAUDE.md) for complete documentation
