# Installing Rails Best Practices Skill

This guide explains how to install and use the Rails Best Practices Skill for Claude.

## Installation Methods

### Method 1: Manual Installation (Claude Code)

1. **Locate Claude Skills Directory**
   ```bash
   # Default location
   ~/.claude/skills/
   ```

2. **Copy the Skill**
   ```bash
   # Copy the entire rails_best_practices directory
   cp -r /path/to/rails_best_practices ~/.claude/skills/rails-best-practices
   ```

3. **Verify Installation**
   ```bash
   ls ~/.claude/skills/rails-best-practices
   # Should show: SKILL.md, README.md, INDEX.md, and category directories
   ```

### Method 2: Git Clone (Recommended)

1. **Clone to Skills Directory**
   ```bash
   cd ~/.claude/skills/
   git clone <repository-url> rails-best-practices
   ```

2. **Update When Needed**
   ```bash
   cd ~/.claude/skills/rails-best-practices
   git pull
   ```

### Method 3: Symlink (For Development)

If you're developing the skill:

```bash
ln -s /path/to/rails_best_practices ~/.claude/skills/rails-best-practices
```

## Verification

After installation, Claude should automatically detect the skill. You can verify by:

1. Asking Claude to write Rails code
2. Checking if Claude follows Rails best practices
3. Reviewing code and seeing Rails-specific suggestions

## Usage

Once installed, the skill is automatically invoked when:
- Writing Ruby on Rails code
- Reviewing Rails code
- Refactoring Rails applications

No manual activation needed - Claude detects when Rails code is being worked on.

## Updating

To update the skill:

```bash
cd ~/.claude/skills/rails-best-practices
git pull  # If using git
# Or copy new files if using manual installation
```

## Troubleshooting

### Skill Not Detected

1. Check the directory name matches exactly: `rails-best-practices`
2. Verify `SKILL.md` exists in the root
3. Ensure Claude Code has access to the skills directory
4. Restart Claude Code if needed

### Skill Not Working

1. Verify the skill structure is correct
2. Check that `SKILL.md` is properly formatted
3. Ensure all category directories are present
4. Review Claude Code logs for errors

## Uninstallation

To remove the skill:

```bash
rm -rf ~/.claude/skills/rails-best-practices
```

