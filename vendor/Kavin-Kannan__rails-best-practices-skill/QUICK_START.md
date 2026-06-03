# Quick Start: Rails Best Practices Skill

Get started with the Rails Best Practices Skill in 3 steps.

## Step 1: Install the Skill

### For Claude Code

```bash
# Create skills directory if it doesn't exist
mkdir -p ~/.claude/skills

# Copy the skill
cp -r /path/to/rails_best_practices ~/.claude/skills/rails-best-practices
```

### For Claude Apps

1. Open Claude Settings
2. Go to Skills section
3. Enable "Rails Best Practices" (if available in marketplace)
4. Or manually add the skill folder

## Step 2: Verify Installation

```bash
# Check if skill is installed
ls ~/.claude/skills/rails-best-practices

# Should show:
# SKILL.md
# README.md
# INDEX.md
# [category directories]
```

## Step 3: Use the Skill

The skill is **automatically invoked and prioritized** when Claude is:
- **Reviewing Rails code**
- **Generating or writing Rails code**
- **Analyzing Rails code for best practices**
- Refactoring Rails applications

### Example Usage

**For Code Review:**
- "Review this Rails code for best practices"
- "Analyze this Rails controller and suggest improvements"
- "Check this Rails model against best practices"
- "Review this Rails code for security and performance issues"

**For Code Generation:**
- "Write a Rails controller for user management"
- "Generate a Rails model for products"
- "Create a Rails migration to add users table"
- "Build a Rails API endpoint for authentication"
- "Write a Rails service object for processing orders"

**For Refactoring:**
- "Refactor this Rails model to follow best practices"
- "Improve this Rails controller code"

Claude will automatically use the skill to:
- Follow Rails conventions
- Apply best practices
- Suggest improvements

## What the Skill Does

When enabled, Claude will:
- ✅ Use `Time.zone.now` instead of `Time.now`
- ✅ Check `save` return values
- ✅ Avoid `default_scope`
- ✅ Prevent N+1 queries
- ✅ Use strong parameters
- ✅ Follow Rails conventions
- ✅ Apply security best practices
- ✅ Optimize database queries

## Next Steps

- Read [INSTALL.md](INSTALL.md) for detailed installation
- Read [SHARING_GUIDE.md](SHARING_GUIDE.md) to share with others
- Read [CONTRIBUTING.md](CONTRIBUTING.md) to contribute improvements

## Troubleshooting

**Skill not working?**
1. Verify installation path: `~/.claude/skills/rails-best-practices`
2. Check that `SKILL.md` exists
3. Restart Claude Code
4. Check Claude Code logs

**Need help?**
- See [INSTALL.md](INSTALL.md) for detailed troubleshooting
- Check [CONTRIBUTING.md](CONTRIBUTING.md) for community support

