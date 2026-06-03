# How to Share Rails Best Practices Skill with Claude Community

This guide explains the complete process of sharing your Rails Best Practices Skill with the Claude developer community.

## Overview

Based on [Claude's Agent Skills announcement](https://www.claude.com/blog/skills), there are several ways to share skills:

1. **Anthropic Skills Marketplace** (Official)
2. **GitHub Repository** (Community)
3. **Direct Sharing** (Team/Organization)

## Method 1: Anthropic Skills Marketplace (Recommended)

### Step 1: Prepare Your Skill

Ensure your skill follows Claude's format:

```
rails-best-practices/
├── SKILL.md              # Required: Skill description
├── README.md              # Recommended: Overview
├── .claude-skill         # Optional: Metadata
├── INSTALL.md            # Installation guide
├── CONTRIBUTING.md       # Contribution guide
├── INDEX.md              # Practices index
└── [category directories]/
```

### Step 2: Create GitHub Repository

1. **Initialize Repository**
   ```bash
   cd /path/to/rails_best_practices
   git init
   git add .
   git commit -m "Initial commit: Rails Best Practices Skill v1.0.0"
   ```

2. **Create on GitHub**
   - Go to GitHub and create a new repository
   - Name: `rails-best-practices-skill`
   - Make it public
   - Don't initialize with README (you already have one)

3. **Push to GitHub**
   ```bash
   git remote add origin https://github.com/yourusername/rails-best-practices-skill.git
   git branch -M main
   git push -u origin main
   ```

### Step 3: Submit to Anthropic

1. **Visit Anthropic Skills Repository**
   - Go to: `https://github.com/anthropics/skills` (if public)
   - Or check Anthropic's developer documentation for submission process

2. **Follow Submission Guidelines**
   - Review their contribution guidelines
   - Ensure your skill meets all requirements
   - Submit a pull request or follow their submission process

3. **Skill Requirements**
   - ✅ Clear `SKILL.md` file
   - ✅ Well-documented
   - ✅ Follows Claude's skill format
   - ✅ Includes examples
   - ✅ Tested and working

## Method 2: Share via GitHub (Community)

### Step 1: Create Public Repository

```bash
# Create repository on GitHub
# Name: rails-best-practices-skill
# Description: Claude Skill for Rails Best Practices
# Public repository
```

### Step 2: Add Installation Instructions

Update your README.md with:

```markdown
## Installation

### For Claude Code

```bash
cd ~/.claude/skills/
git clone https://github.com/yourusername/rails-best-practices-skill.git rails-best-practices
```

### For Claude Apps

[Instructions for Claude Apps users]
```

### Step 3: Share the Repository

- Share the GitHub URL: `https://github.com/yourusername/rails-best-practices-skill`
- Others can install via git clone
- Include in your project documentation
- Share on social media/forums

## Method 3: Direct Team Sharing

### For Your Organization

1. **Internal Repository**
   - Host on your organization's GitHub/GitLab
   - Share with team members
   - Install via git clone

2. **Team Installation**
   ```bash
   # Team members install:
   cd ~/.claude/skills/
   git clone <internal-repo-url> rails-best-practices
   ```

## Skill Metadata

Create a `.claude-skill` file (optional but recommended):

```json
{
  "name": "rails-best-practices",
  "version": "1.0.0",
  "description": "Comprehensive Rails best practices skill for Claude",
  "author": "Your Name",
  "repository": "https://github.com/yourusername/rails-best-practices-skill",
  "categories": ["coding", "rails", "ruby", "best-practices"],
  "tags": ["rails", "ruby", "best-practices", "code-review", "refactoring"]
}
```

## Promotion

Once shared:

1. **Documentation**
   - Clear README
   - Installation guide
   - Usage examples
   - Contribution guidelines

2. **Examples**
   - Show before/after code
   - Demonstrate skill capabilities
   - Include use cases

3. **Community**
   - Share on Rails forums
   - Post on social media
   - Write blog post
   - Present at meetups

## Maintenance

After sharing:

1. **Respond to Issues**
   - Monitor GitHub issues
   - Answer questions
   - Fix bugs

2. **Update Regularly**
   - Add new Rails practices
   - Update examples
   - Improve documentation
   - Version releases

3. **Community Engagement**
   - Accept contributions
   - Review pull requests
   - Collaborate with users

## Checklist Before Sharing

- [ ] `SKILL.md` is complete and accurate
- [ ] All documentation is clear
- [ ] Examples are tested
- [ ] Installation instructions work
- [ ] Repository is public (if sharing publicly)
- [ ] License is included
- [ ] Version number is set
- [ ] Skill has been tested with Claude Code
- [ ] README explains what the skill does
- [ ] CONTRIBUTING.md explains how others can help

## Resources

- **Claude Skills Blog**: https://www.claude.com/blog/skills
- **Claude Developer Docs**: https://docs.anthropic.com
- **Rails Best Practices**: https://rails-bestpractices.com/
- **GitHub Skills Examples**: Search for other Claude skills

## Next Steps

1. ✅ Complete skill development
2. ✅ Test with Claude Code
3. ✅ Prepare documentation
4. ⬜ Create GitHub repository
5. ⬜ Submit to Anthropic or share publicly
6. ⬜ Promote and maintain

Good luck sharing your skill with the Claude community!

