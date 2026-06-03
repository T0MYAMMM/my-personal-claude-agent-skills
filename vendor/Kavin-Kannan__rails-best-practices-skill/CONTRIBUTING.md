# Contributing to Rails Best Practices Skill

Thank you for your interest in contributing! This document outlines the contribution guidelines for this Claude Agent Skill.

## Code of Conduct

This project follows the Rails community's values of respect, collaboration, and constructive feedback. Be respectful, helpful, and professional in all interactions.

## Contribution Guidelines

### Disclosure of AI Involvement

If you use AI tools (including Claude) to assist with your contributions:

1. **Disclose AI Usage**: Clearly state in your pull request description if AI tools were used
2. **Human Ownership**: All contributions must be submitted under human accounts, not automated/bot accounts
3. **Verification**: Manually verify all AI-assisted contributions and provide evidence (tests, screenshots, logs)
4. **Responsibility**: As a contributor, you are personally responsible for the content you submit

### Contribution Process

1. **Fork the Repository**
   ```bash
   # Fork on GitHub, then clone
   git clone https://github.com/YOUR_USERNAME/rails-best-practices-skill.git
   cd rails-best-practices-skill
   ```

2. **Create a Feature Branch**
   ```bash
   git checkout -b feature/add-new-practice
   # or
   git checkout -b fix/update-documentation
   ```

3. **Make Your Changes**
   - Follow the existing structure and format
   - Add new practices to appropriate category directories
   - Update `INDEX.md` with new practices
   - Update `SKILL.md` if adding major capabilities
   - Follow existing markdown format

4. **Test Your Changes**
   - Verify the skill structure is correct
   - Test installation process
   - Ensure documentation is clear
   - Check that examples work

5. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "feat: Add practice for X"
   # Use conventional commit format:
   # feat: New feature
   # fix: Bug fix
   # docs: Documentation changes
   # refactor: Code refactoring
   ```

6. **Push and Create Pull Request**
   ```bash
   git push origin feature/add-new-practice
   # Then create PR on GitHub with clear description
   ```

### Pull Request Guidelines

Your pull request should include:

1. **Clear Description**
   - What changes were made
   - Why the changes were made
   - How to test/verify the changes
   - Any AI tool usage disclosure

2. **Evidence of Verification**
   - Screenshots of skill working (if applicable)
   - Test results
   - Installation verification

3. **Documentation Updates**
   - Update relevant documentation files
   - Add examples if introducing new practices
   - Update version if making significant changes

### Adding New Practices

When adding a new Rails best practice:

1. **Create Practice File**
   - Location: Appropriate category directory (e.g., `active_record/`, `controllers/`)
   - Format: Markdown file with clear structure
   - Name: Descriptive, kebab-case (e.g., `use_includes_for_associations.md`)

2. **Practice File Structure**
   ```markdown
   # Practice Title
   
   **Source**: [rails-bestpractices.com](link)
   **Date**: Date of practice
   **Author**: Author name (if known)
   
   ## Description
   Clear description of the practice
   
   ## Why
   Explanation of why this practice matters
   
   ## Bad Example
   ```ruby
   # Bad code example
   ```
   
   ## Good Example
   ```ruby
   # Good code example
   ```
   
   ## Related Practices
   Links to related practices
   
   ## Tags
   Relevant tags
   ```

3. **Update Index**
   - Add practice to `INDEX.md` in appropriate category
   - Maintain alphabetical or logical order

4. **Update SKILL.md** (if major capability)
   - Add to relevant capability section
   - Update examples if needed

### Code Style

- **Markdown**: Follow existing format and style
- **Code Examples**: Use Ruby syntax highlighting
- **File Naming**: Use kebab-case for files
- **Documentation**: Be clear, concise, and helpful

### Testing Requirements

Before submitting:

- [ ] Skill structure is correct
- [ ] `SKILL.md` is properly formatted
- [ ] All documentation is clear
- [ ] Examples are accurate
- [ ] Installation instructions work
- [ ] No broken links
- [ ] Version number is updated (if needed)

### Review Process

1. **Automated Checks**: Repository may have automated checks
2. **Human Review**: Maintainers will review your PR
3. **Feedback**: Address any feedback promptly
4. **Approval**: Once approved, your PR will be merged

### Commit Message Format

Use conventional commits:

```
feat: Add practice for using includes in queries
fix: Correct typo in timezone practice
docs: Update installation instructions
refactor: Reorganize security practices
```

### Types of Contributions

We welcome:

- ✅ New Rails best practices
- ✅ Improvements to existing practices
- ✅ Documentation improvements
- ✅ Bug fixes
- ✅ Examples and use cases
- ✅ Translation/localization
- ✅ Testing improvements

### Questions?

- Open an issue on GitHub
- Check existing issues for similar questions
- Review documentation in `README.md` and other guides

## Attribution

Contributors will be:
- Listed in the repository (if desired)
- Credited in release notes
- Acknowledged in documentation

## License

By contributing, you agree that your contributions will be licensed under the MIT License (see `LICENSE` file).

## Thank You!

Your contributions help make Rails development better for everyone. Thank you for taking the time to contribute!
