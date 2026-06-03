# How to Use Rails Best Practices Library

This library can be used across multiple Rails projects. Here's how to integrate it.

## Option 1: Copy to Your Project

1. Copy the entire `rails_best_practices/` directory to your Rails project root
2. Reference practices in your code review process
3. Use as guidelines for your development team

```bash
# From this project
cp -r rails_best_practices/ /path/to/your/rails/project/
```

## Option 2: Use as a Git Submodule

1. Add this repository as a submodule in your Rails project
2. Reference the practices from the submodule

```bash
cd /path/to/your/rails/project
git submodule add <this-repo-url> rails_best_practices
```

## Option 3: Reference from This Project

If you're using this multi-agent system:
- Practices are automatically used by Coding Agent and Code Review Agent
- See `prompts/rails_best_practices.txt` for the consolidated version

## Integration with Code Review

### Manual Review

Reference practices during code review:

```ruby
# Check against practices
# - Time.zone.now instead of Time.now
# - Check save return value
# - Avoid default_scope
# etc.
```

### Automated Review

Integrate into your CI/CD pipeline:

```yaml
# Example GitHub Actions
- name: Check Rails Best Practices
  run: |
    # Use a linter that checks against practices
    # Or reference the practices in your review process
```

## Integration with Linters

### RuboCop

Add custom cops based on practices:

```ruby
# .rubocop.yml
Rails/TimeZoneNow:
  Enabled: true
  Description: 'Use Time.zone.now instead of Time.now'
```

### Custom Scripts

Create scripts to check practices:

```ruby
# scripts/check_best_practices.rb
require_relative '../rails_best_practices/checker'

RailsBestPracticesChecker.new.check
```

## Team Guidelines

1. **Onboarding**: Share `rails_best_practices/README.md` with new team members
2. **Code Review**: Reference practices during PR reviews
3. **Documentation**: Link to practices in your project README
4. **CI/CD**: Integrate checks into your pipeline

## Updating Practices

When new practices are added:

1. Update the practice file in the appropriate category
2. Update `INDEX.md`
3. If using with agents, update `prompts/rails_best_practices.txt`
4. Commit and share with your team

## Examples

### Example 1: Code Review Checklist

```markdown
## Code Review Checklist

- [ ] Uses Time.zone.now instead of Time.now
- [ ] Checks save return value or uses save!
- [ ] Doesn't use default_scope
- [ ] Doesn't modify params hash directly
- [ ] Rescues StandardError, not Exception
- [ ] Follows "Tell, don't ask" principle
- [ ] Avoids N+1 queries
```

### Example 2: Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

# Check for Time.now usage
if git diff --cached | grep -q "Time\.now"; then
  echo "Warning: Consider using Time.zone.now instead of Time.now"
  echo "See: rails_best_practices/timezone/use_time_zone_now.md"
fi
```

### Example 3: Documentation Link

Add to your project README:

```markdown
## Code Standards

We follow Rails best practices. See [rails_best_practices/](rails_best_practices/) for guidelines.
```

## Best Practices for Using This Library

1. **Keep it updated**: Regularly check rails-bestpractices.com for new practices
2. **Customize for your team**: Add project-specific practices
3. **Make it accessible**: Ensure all team members can access the practices
4. **Integrate early**: Use from the start of your project
5. **Review regularly**: Periodically review practices with your team

## Support

For questions or contributions:
- Reference: [rails-bestpractices.com](https://rails-bestpractices.com/)
- See `INDEX.md` for complete list of practices
- See `README.md` for overview

