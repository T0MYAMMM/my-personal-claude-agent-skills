# Rails Best Practices Skill

A Claude Agent Skill that provides comprehensive Rails best practices sourced from [rails-bestpractices.com](https://rails-bestpractices.com/).

## What is This?

This is a **Claude Agent Skill** - a specialized knowledge package that helps Claude review, analyze, and generate Ruby on Rails code following community best practices. **This skill is automatically invoked for both code review and code generation** when Claude is working with Ruby on Rails code.

## Quick Start

### Install for Claude Code

```bash
mkdir -p ~/.claude/skills
cp -r rails_best_practices ~/.claude/skills/rails-best-practices
```

See [QUICK_START.md](QUICK_START.md) for 3-step installation.

## Features

When enabled, Claude will automatically:
- ✅ Use `Time.zone.now` instead of `Time.now`
- ✅ Check `save` return values or use `save!`
- ✅ Avoid `default_scope` anti-patterns
- ✅ Prevent N+1 query problems
- ✅ Use strong parameters in controllers
- ✅ Follow Rails conventions
- ✅ Apply security best practices
- ✅ Optimize database queries
- ✅ And much more!

## Installation

- **Claude Code**: See [INSTALL.md](INSTALL.md)
- **Claude Apps**: Enable in Settings → Skills
- **API**: Include in Messages API requests

## Sharing with Community

Want to share this skill with other developers?

**See [HOW_TO_SHARE.md](HOW_TO_SHARE.md) for complete step-by-step instructions!**

Quick version:
1. Create GitHub repository
2. Submit to Anthropic Skills Marketplace (when available)
3. Share with Rails community

## Documentation

- **[SKILL.md](SKILL.md)** - Main skill description
- **[QUICK_START.md](QUICK_START.md)** - 3-step installation
- **[INSTALL.md](INSTALL.md)** - Detailed installation guide
- **[HOW_TO_SHARE.md](HOW_TO_SHARE.md)** - Complete sharing guide ⭐
- **[DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md)** - Developer contribution guide
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - How to contribute improvements
- **[INDEX.md](INDEX.md)** - Complete practices index
- **[USAGE.md](USAGE.md)** - Usage across projects
- **[COPYRIGHT.md](COPYRIGHT.md)** - Copyright and legal information ⚖️
- **[LEGAL_GUIDANCE.md](LEGAL_GUIDANCE.md)** - Legal guidance and recommendations ⚖️
- **[ATTRIBUTION_TEMPLATE.md](ATTRIBUTION_TEMPLATE.md)** - Template for practice file attribution

## Structure

```
rails-best-practices/
├── SKILL.md              # Main skill description (required)
├── README.md             # This file
├── INDEX.md              # Practices index
├── LICENSE               # MIT License
├── timezone/             # Time/timezone practices
├── active_record/        # ActiveRecord practices
├── controllers/          # Controller practices
├── error_handling/       # Error handling practices
├── code_organization/    # Code organization practices
├── views/                # View practices
├── migrations/           # Migration practices
├── security/             # Security practices
├── code_quality/         # Code quality practices
├── performance/          # Performance practices
├── testing/              # Testing practices
└── general/              # General Rails conventions
```

## Categories Covered

- **Timezone**: Time handling best practices
- **ActiveRecord**: Database and model patterns
- **Controllers**: Controller design patterns
- **Error Handling**: Exception handling
- **Code Organization**: Structure and patterns
- **Views**: View and partial patterns
- **Migrations**: Database migration practices
- **Security**: Security best practices
- **Code Quality**: DRY, SOLID, clean code
- **Performance**: Query optimization, caching
- **Testing**: Test coverage and quality
- **General**: Rails conventions and standards

## Source and Attribution

All practices are **based on concepts** from [rails-bestpractices.com](https://rails-bestpractices.com/), 
a community-driven collection of Rails best practices created by Richard Huang and contributors.

**Important**: This skill does NOT copy verbatim text from rails-bestpractices.com. All content 
is rewritten in our own words, organized for Claude Skill format, with proper attribution. 
See [COPYRIGHT.md](COPYRIGHT.md) for detailed copyright information.

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for:
- How to add new Rails practices
- Contribution guidelines (follows Claude's standards)
- AI usage disclosure requirements
- Pull request process
- Code of conduct

**Important**: All contributions must follow Claude's contribution guidelines, including disclosure of AI tool usage and human verification of all changes.

## License

MIT License - See [LICENSE](LICENSE) file for details.

## Version

Current version: **1.0.0**

## Support

- **Installation Issues**: See [INSTALL.md](INSTALL.md)
- **Sharing Questions**: See [HOW_TO_SHARE.md](HOW_TO_SHARE.md)
- **Contributing**: See [CONTRIBUTING.md](CONTRIBUTING.md)
- **General Questions**: Open an issue on GitHub

---

**Ready to share?** → See [HOW_TO_SHARE.md](HOW_TO_SHARE.md) for complete instructions!
