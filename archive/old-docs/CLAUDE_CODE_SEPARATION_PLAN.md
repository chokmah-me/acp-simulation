# 🔄 Claude Code Assistant Separation Plan

## Executive Summary

This plan details the separation of Claude Code assistant components from the ACP Simulation repository into a dedicated repository. The separation will create a clean, reusable Claude Code Playbook that can be applied to any project, while preserving all simulation functionality in the main repository.

**Key Benefits:**
- ✅ Reusable AI development toolkit across multiple projects
- ✅ Cleaner repository structure (separation of concerns)
- ✅ Independent versioning and maintenance of AI assistant tools
- ✅ Reduced repository size for simulation-only users
- ✅ Easier contribution to AI assistant tools

---

## 1. Current State Analysis

### Claude Code Components in ACP Repository

```
acp-simulation/
├── .claude/                          # Claude configuration
│   ├── settings.local.json
│   └── skills/                       # AI skills and workflows
│       ├── README.md
│       ├── python-scientific/
│       │   └── SKILL.md
│       └── refactoring/
│           ├── SKILL.md
│           ├── workflows/            # 7 workflow files
│           └── knowledge/            # 2 knowledge base files
├── CLAUDE.md                         # Project constitution
├── .cursorrules                      # IDE integration
├── LICENSE                           # Claude Code Playbook license
└── docs/
    └── AI_ASSISTED_DEVELOPMENT.md    # Integration guide
```

### Simulation Components (to remain)

```
acp-simulation/
├── src/acp_simulation/               # Core simulation package
├── tests/                            # Test suite
├── scripts/                          # Utility scripts
├── external/                         # Third-party tools (ACTS/CCM)
├── docs/                             # Simulation documentation
├── requirements.txt                  # Python dependencies
├── setup.py                          # Package setup
└── *.py                              # Main simulation scripts
```

**Zero Dependencies**: The simulation code has no dependencies on Claude Code components.

---

## 2. New Repository Structure

### Proposed: `claude-code-playbook` Repository

```
claude-code-playbook/
├── README.md                         # Main playbook documentation
├── LICENSE                           # MIT License
├── CONTRIBUTING.md                   # Contribution guidelines
├── .github/
│   ├── ISSUE_TEMPLATE/               # Issue templates
│   └── workflows/                    # CI/CD for playbook
├── docs/
│   ├── GETTING_STARTED.md            # Quick start guide
│   ├── WORKFLOW_GUIDE.md             # Workflow usage guide
│   ├── CREATING_SKILLS.md            # Skill development guide
│   └── EXAMPLES.md                   # Usage examples
├── skills/                           # Core skills directory
│   ├── README.md                     # Skills overview
│   ├── python-scientific/            # Python scientific computing
│   │   ├── SKILL.md                  # Main skill file
│   │   ├── examples/                 # Code examples
│   │   └── tests/                    # Skill validation tests
│   └── refactoring/                  # General refactoring
│       ├── SKILL.md                  # Skill overview
│       ├── workflows/                # Workflow definitions
│       │   ├── triage.md
│       │   ├── extract.md
│       │   ├── modernize.md
│       │   ├── qnew.md
│       │   ├── qplan.md
│       │   ├── qcode.md
│       │   └── catchup.md
│       ├── knowledge/                # Reference materials
│       │   ├── typescript-style.md
│       │   └── architecture-patterns.md
│       └── examples/                 # Refactoring examples
├── templates/                        # Project templates
│   ├── CLAUDE.md.template           # Project constitution template
│   ├── .cursorrules.template        # IDE rules template
│   └── python-project/              # Python project template
│       ├── structure/
│       └── setup-guide.md
└── examples/                         # Example projects
    ├── python-scientific-example/   # Example using python-scientific skill
    └── refactoring-example/         # Example using refactoring skill
```

---

## 3. Separation Strategy

### Phase 1: Create New Repository

**Actions:**
1. Create new GitHub repository: `dyb5784/claude-code-playbook`
2. Initialize with MIT license
3. Set up basic structure (README, docs, skills/)
4. Copy Claude Code components from ACP repository

**Files to Move:**
```
.claude/skills/          → claude-code-playbook/skills/
CLAUDE.md                → claude-code-playbook/templates/CLAUDE.md.template
.cursorrules             → claude-code-playbook/templates/.cursorrules.template
LICENSE                  → claude-code-playbook/LICENSE (update if needed)
docs/AI_ASSISTED_DEVELOPMENT.md → claude-code-playbook/docs/WORKFLOW_GUIDE.md
```

### Phase 2: Update ACP Repository

**Actions:**
1. Remove `.claude/` directory
2. Remove `CLAUDE.md`
3. Remove `.cursorrules`
4. Update `LICENSE` to ACP-specific license
5. Update `docs/AI_ASSISTED_DEVELOPMENT.md` to reference new repository
6. Update main `README.md` to mention Claude Code Playbook as optional tool

**Files to Keep in ACP:**
```
All simulation code (src/, tests/, scripts/, external/)
All simulation documentation (docs/ except AI_ASSISTED_DEVELOPMENT.md)
requirements.txt, setup.py, *.py files
```

### Phase 3: Create Integration Bridge

**New File in ACP Repository:**
- `docs/CLAUDE_CODE_INTEGRATION.md` - Guide for using Claude Code Playbook with ACP

**Content:**
```markdown
# Claude Code Playbook Integration

This project can be enhanced with AI-assisted development using the Claude Code Playbook.

## Quick Start

1. Clone the Claude Code Playbook:
   ```bash
   git clone https://github.com/dyb5784/claude-code-playbook.git
   ```

2. Copy templates to your project:
   ```bash
   cp claude-code-playbook/templates/CLAUDE.md.template ./CLAUDE.md
   cp claude-code-playbook/templates/.cursorrules.template ./.cursorrules
   ```

3. Customize the templates for your project needs

4. Start using Claude Code with your project

## Available Skills

- **Python Scientific Computing**: For simulation development
- **General Refactoring**: For code improvement

See the [Claude Code Playbook repository](https://github.com/dyb5784/claude-code-playbook) for complete documentation.
```

---

## 4. File Mapping Details

### Complete File Transfer List

| Current Location | New Location | Purpose |
|------------------|--------------|---------|
| `.claude/skills/README.md` | `skills/README.md` | Skills overview |
| `.claude/skills/python-scientific/SKILL.md` | `skills/python-scientific/SKILL.md` | Python scientific patterns |
| `.claude/skills/refactoring/SKILL.md` | `skills/refactoring/SKILL.md` | Refactoring overview |
| `.claude/skills/refactoring/workflows/*.md` | `skills/refactoring/workflows/*.md` | Workflow definitions (7 files) |
| `.claude/skills/refactoring/knowledge/*.md` | `skills/refactoring/knowledge/*.md` | Knowledge base (2 files) |
| `CLAUDE.md` | `templates/CLAUDE.md.template` | Project constitution template |
| `.cursorrules` | `templates/.cursorrules.template` | IDE rules template |
| `docs/AI_ASSISTED_DEVELOPMENT.md` | `docs/WORKFLOW_GUIDE.md` | Workflow usage guide |
| `LICENSE` | `LICENSE` | Update to generic MIT |

### Files to Remove from ACP

```
.claude/ (entire directory)
CLAUDE.md
.cursorrules
LICENSE (replace with ACP-specific license)
docs/AI_ASSISTED_DEVELOPMENT.md
```

### Files to Modify in ACP

```
README.md - Add "Optional: Claude Code Playbook" section
docs/README.md - Update to reference external playbook
VERSION_CHANGELOG.md - Note the separation
```

---

## 5. Repository Independence Verification

### ACP Repository (Post-Separation)

**Must be able to:**
- ✅ Run all simulations without any Claude Code files
- ✅ Pass all tests without AI assistant components
- ✅ Build and install as Python package
- ✅ Generate publication-quality results
- ✅ Maintain statistical validation integrity

**Verification Commands:**
```bash
# Test simulation functionality
python acp_corrected_final.py
python acp_parallel_power_analysis.py
python src/acp_fully_configurable.py --num-episodes 100

# Run test suite
pytest tests/ -v

# Verify reproducibility
python scripts/verify_reproducibility.py

# Check package installation
pip install -e .
python -c "import acp_simulation; print('✅ Package works')"
```

### Claude Code Playbook Repository

**Must be able to:**
- ✅ Work as standalone documentation repository
- ✅ Provide clear integration instructions
- ✅ Serve as template for new projects
- ✅ Be versioned independently
- ✅ Accept community contributions

**Verification Steps:**
```bash
# Check all files are present
ls -la skills/
ls -la skills/refactoring/workflows/
ls -la templates/

# Verify documentation builds
# (if using docs generator)

# Test template functionality
# (copy templates to test project)
```

---

## 6. Git History Preservation

### Option A: Filter-branch (Recommended)

Preserve git history for moved files:

```bash
# In ACP repository
git filter-branch --subdirectory-filter .claude --prune-empty -- --all
# This creates new repo with only .claude history

# Then add other files manually
```

### Option B: Clean Break

Start fresh without history (simpler):

```bash
# In new repository
git init
# Copy files without history
# Add initial commit with message:
# "Initial commit: Claude Code Playbook v3.0.0
# Extracted from acp-simulation repository"
```

### Option C: Hybrid Approach

Keep history in ACP, start fresh in new repo but reference original commits:

```bash
# In new repo's README.md, add:
# "This playbook was originally developed for the ACP Simulation project.
# Original development history available at:
# https://github.com/chokmah-me/acp-simulation (commits up to 2025-12-11)"
```

**Recommendation**: Option B (Clean Break) for simplicity, as the playbook will evolve independently.

---

## 7. Post-Separation Maintenance

### ACP Repository

**Ongoing tasks:**
- Maintain simulation code and documentation
- Update `docs/CLAUDE_CODE_INTEGRATION.md` if playbook API changes
- No maintenance of AI assistant components

**Release versioning:** Continue ACP versioning (v4.0, v4.1, etc.)

### Claude Code Playbook Repository

**Ongoing tasks:**
- Add new skills and workflows
- Improve existing documentation
- Add examples and templates
- Accept community contributions
- Maintain integration guides

**Release versioning:** Start fresh (v1.0.0, v1.1.0, etc.)

### Synchronization Strategy

**When to update integration docs:**
- New major version of playbook
- New skills added
- Workflow API changes
- Template structure changes

**Update process:**
1. Update playbook repository
2. Test with ACP simulation
3. Update ACP integration docs
4. Notify users of changes

---

## 8. Migration Timeline

### Week 1: Preparation
- [ ] Create `claude-code-playbook` repository
- [ ] Copy all Claude Code components
- [ ] Set up basic documentation structure
- [ ] Create project templates

### Week 2: ACP Cleanup
- [ ] Remove `.claude/` directory from ACP
- [ ] Remove `CLAUDE.md` and `.cursorrules`
- [ ] Update `LICENSE` file
- [ ] Create `docs/CLAUDE_CODE_INTEGRATION.md`
- [ ] Update main `README.md`

### Week 3: Documentation & Testing
- [ ] Complete playbook documentation
- [ ] Add usage examples
- [ ] Test integration with ACP
- [ ] Verify both repositories work independently
- [ ] Create migration guide

### Week 4: Release & Announcement
- [ ] Tag playbook v1.0.0 release
- [ ] Tag ACP v4.1.0 release (post-separation)
- [ ] Update GitHub repository descriptions
- [ ] Announce to users (if any)
- [ ] Archive old branches if needed

---

## 9. Risk Mitigation

### Risk 1: Loss of Development Context
**Mitigation:**
- Keep detailed migration commit messages
- Document original purpose of each component
- Preserve cross-references in documentation

### Risk 2: Integration Breakage
**Mitigation:**
- Test integration thoroughly before finalizing
- Provide clear version compatibility matrix
- Maintain backward compatibility in playbook

### Risk 3: Community Confusion
**Mitigation:**
- Clear README in both repositories explaining separation
- Cross-link between repositories
- Update all external documentation
- Use descriptive commit messages

### Risk 4: Duplicate Maintenance
**Mitigation:**
- Establish clear ownership boundaries
- Create automation for template updates
- Document when to update integration docs

---

## 10. Success Metrics

### Separation Success
- [ ] Zero Claude Code files remain in ACP repository
- [ ] All simulation functionality preserved
- [ ] ACP can run without any AI assistant components
- [ ] Playbook repository is self-contained
- [ ] Clear integration path documented

### Quality Metrics
- [ ] All tests pass in ACP repository
- [ ] Simulation results unchanged (reproducibility verified)
- [ ] Playbook documentation is complete
- [ ] Integration guide is clear and tested
- [ ] No broken links or references

### Maintenance Metrics
- [ ] Both repositories have clear contribution guidelines
- [ ] Versioning strategy is documented
- [ ] Release process is defined
- [ ] Issue templates are in place
- [ ] CI/CD is configured (optional but recommended)

---

## 11. Next Steps

1. **Review and approve** this separation plan
2. **Create new repository** `dyb5784/claude-code-playbook`
3. **Execute Phase 1**: Copy Claude Code components
4. **Execute Phase 2**: Clean ACP repository
5. **Test thoroughly**: Verify both repositories work independently
6. **Document**: Complete integration guides
7. **Release**: Tag v1.0.0 of playbook, update ACP to v4.1.0

---

**Plan Version**: 1.0  
**Date**: December 11, 2025  
**Status**: Ready for Review