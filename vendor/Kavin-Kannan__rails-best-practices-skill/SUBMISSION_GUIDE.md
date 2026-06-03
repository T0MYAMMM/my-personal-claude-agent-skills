# How to Submit Rails Best Practices Skill to Claude

This guide provides step-by-step instructions for submitting your skill to Claude.

## Current Status

✅ **Repository Created**: https://github.com/Kavin-Kannan/rails-best-practices-skill  
✅ **Code Pushed**: All files are on GitHub  
✅ **Skill Structure**: Complete and compliant  

## Next Steps

### Step 1: Enhance GitHub Repository

#### 1.1 Add Repository Topics/Tags

On your GitHub repository page:
1. Click on the gear icon (⚙️) next to "About"
2. Add these topics:
   - `claude`
   - `claude-skill`
   - `rails`
   - `ruby`
   - `best-practices`
   - `code-review`
   - `refactoring`
   - `ruby-on-rails`

#### 1.2 Update Repository Description

Set description to:
```
Claude Agent Skill for Rails Best Practices. Comprehensive collection of Rails best practices from rails-bestpractices.com. Helps Claude write, review, and refactor Rails code following community standards.
```

#### 1.3 Create First Release

```bash
cd /Users/kavinkannan/Documents/kipu_sources/rails_best_practices

# Create a release tag
git tag -a v1.0.0 -m "Initial release: Rails Best Practices Skill v1.0.0"
git push origin v1.0.0

# Or use GitHub CLI
gh release create v1.0.0 \
  --title "Rails Best Practices Skill v1.0.0" \
  --notes "Initial release of Rails Best Practices Skill for Claude. Comprehensive collection of Rails best practices from rails-bestpractices.com."
```

### Step 2: Submit to Claude

There are **three main ways** to submit/share your skill:

---

## Method 1: Upload to Claude.ai (Personal Use)

For using the skill yourself in Claude.ai:

### Steps:

1. **Package Your Skill**
   ```bash
   cd /Users/kavinkannan/Documents/kipu_sources/rails_best_practices
   zip -r rails-best-practices-skill.zip . \
     -x "*.git*" \
     -x ".DS_Store" \
     -x "*.swp"
   ```

2. **Upload to Claude.ai**
   - Go to [claude.ai](https://claude.ai)
   - Navigate to **Settings** → **Capabilities**
   - Ensure "Code execution and file creation" is enabled
   - Scroll to **Skills** section
   - Click **"Upload skill"**
   - Select your `rails-best-practices-skill.zip` file
   - Wait for upload to complete

3. **Enable the Skill**
   - Toggle the skill **ON** in your Skills list
   - The skill is now active!

4. **Test the Skill**
   - Ask Claude: "Review this Rails code for best practices: [your code]"
   - Verify Claude uses the skill appropriately

---

## Method 2: Install for Claude Code (Local Development)

For using the skill with Claude Code (local development):

### Steps:

1. **Install the Skill**
   ```bash
   # Create skills directory if it doesn't exist
   mkdir -p ~/.claude/skills
   
   # Clone your repository
   cd ~/.claude/skills
   git clone https://github.com/Kavin-Kannan/rails-best-practices-skill.git rails-best-practices
   ```

2. **Verify Installation**
   ```bash
   ls -la ~/.claude/skills/rails-best-practices
   # Should show SKILL.md and other files
   ```

3. **Use with Claude Code**
   - Claude Code will automatically discover skills in `~/.claude/skills/`
   - The skill will be available when you use Claude Code

---

## Method 3: Submit to Anthropic Skills Marketplace (Community Sharing)

For sharing with the broader Claude community:

### Option A: Check for Official Marketplace

1. **Check Anthropic's Developer Resources**
   - Visit: https://docs.anthropic.com
   - Look for "Skills" or "Marketplace" section
   - Check for submission guidelines

2. **Check GitHub for Skills Repository**
   - Search for: `github.com/anthropics/skills`
   - If it exists and is public, follow their contribution guidelines
   - Submit a pull request with your skill

3. **Contact Anthropic**
   - Email: developer-relations@anthropic.com (if available)
   - Or check their support channels
   - Ask about skill submission process

### Option B: Share via GitHub (Community)

Since there may not be an official marketplace yet:

1. **Your Repository is Already Public** ✅
   - URL: https://github.com/Kavin-Kannan/rails-best-practices-skill

2. **Add Installation Instructions to README**
   - Already included in your README.md ✅

3. **Share with Community**
   - **Rails Forums**: Share in Ruby on Rails community forums
   - **Reddit**: Post on r/rails, r/ruby, r/claudeai
   - **Twitter/X**: Tweet with hashtags #Rails #Claude #AI #Ruby
   - **LinkedIn**: Post in Rails/Ruby groups
   - **Dev.to**: Write a blog post about the skill
   - **Rails Slack/Discord**: Share in relevant channels

4. **Create a Demo/Example**
   - Show before/after code examples
   - Create a short video demonstrating the skill
   - Add screenshots to README

---

## Method 4: Use Claude Skills API (For Developers)

If you're building applications that use Claude:

1. **Check Anthropic API Documentation**
   - Visit: https://docs.anthropic.com
   - Look for Skills API endpoints
   - Use API to upload/manage skills programmatically

2. **Integration Example** (if API available):
   ```bash
   curl -X POST https://api.anthropic.com/v1/skills \
     -H "Authorization: Bearer YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     -d @skill-metadata.json
   ```

---

## Quick Reference: Installation Commands

### For Others to Install Your Skill:

**Claude Code:**
```bash
mkdir -p ~/.claude/skills
cd ~/.claude/skills
git clone https://github.com/Kavin-Kannan/rails-best-practices-skill.git rails-best-practices
```

**Claude.ai (Upload ZIP):**
1. Download ZIP from GitHub: https://github.com/Kavin-Kannan/rails-best-practices-skill/archive/refs/heads/main.zip
2. Upload via Settings → Capabilities → Skills → Upload skill

---

## Verification Checklist

Before submitting/sharing:

- [x] Repository is public
- [x] All files are committed and pushed
- [x] SKILL.md is complete
- [x] README.md has installation instructions
- [x] License is included (MIT)
- [x] Copyright attribution is clear
- [ ] **Add GitHub topics** (do this now)
- [ ] **Create v1.0.0 release** (do this now)
- [ ] **Test skill upload** (try Method 1)
- [ ] **Share with community** (Method 3B)

---

## Immediate Actions

### Right Now (5 minutes):

1. **Add Topics to GitHub Repository**
   - Go to: https://github.com/Kavin-Kannan/rails-best-practices-skill
   - Click gear icon next to "About"
   - Add topics listed above

2. **Create Release**
   ```bash
   cd /Users/kavinkannan/Documents/kipu_sources/rails_best_practices
   gh release create v1.0.0 \
     --title "Rails Best Practices Skill v1.0.0" \
     --notes "Initial release of Rails Best Practices Skill for Claude. Comprehensive collection of Rails best practices from rails-bestpractices.com."
   ```

3. **Test Upload to Claude.ai**
   - Package and upload using Method 1 above
   - Verify it works

### This Week:

1. **Share with Rails Community**
   - Post on Rails forums
   - Share on social media
   - Write a blog post

2. **Monitor and Respond**
   - Watch for GitHub issues
   - Answer questions
   - Accept contributions

---

## Resources

- **Your Repository**: https://github.com/Kavin-Kannan/rails-best-practices-skill
- **Claude Skills Blog**: https://www.claude.com/blog/skills
- **Claude Help Center**: https://support.claude.com/en/articles/12512198-how-to-create-custom-skills
- **Anthropic Developer Docs**: https://docs.anthropic.com
- **Rails Best Practices**: https://rails-bestpractices.com/

---

## Success!

Your skill is ready to share! The repository is public and others can install it. 

**Next**: Add topics, create a release, and start sharing with the community!

