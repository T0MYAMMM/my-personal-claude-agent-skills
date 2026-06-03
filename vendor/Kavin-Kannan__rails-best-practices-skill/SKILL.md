# Rails Best Practices Skill

A comprehensive skill that helps Claude review, analyze, and generate Ruby on Rails code according to established best practices.

## Purpose

This skill provides Claude with expert knowledge of Rails best practices sourced from [rails-bestpractices.com](https://rails-bestpractices.com/). **This skill is automatically invoked for both code review and code generation** - when enabled, Claude will:

- **Review code against established Rails conventions**
- **Generate code following Rails best practices**
- **Identify Rails anti-patterns and suggest improvements**
- **Flag security vulnerabilities and performance issues**
- **Ensure code follows Rails community standards**
- **Provide detailed code review feedback with specific recommendations**
- **Apply best practices automatically when writing new Rails code**

## When to Use

This skill is **automatically invoked and prioritized** when Claude is:
- **Reviewing Ruby on Rails code**
- **Generating or writing Ruby on Rails code**
- **Analyzing Rails code for best practices**
- **Performing code reviews on Rails applications**
- Refactoring Rails applications
- Debugging Rails issues
- Explaining Rails concepts

## Capabilities

### Time and Timezone
- Enforces use of `Time.zone.now` instead of `Time.now`
- Recommends client-side time display instead of `time_ago_in_words`

### ActiveRecord
- Ensures `save` return values are checked or `save!` is used
- Warns against `default_scope` usage
- Recommends batched finders for large datasets
- Identifies and fixes N+1 query problems

### Controllers
- Prevents modification of params hash
- Recommends route restrictions
- Enforces strong parameters usage

### Error Handling
- Ensures `StandardError` is rescued, not `Exception`
- Recommends specific exception handling

### Code Organization
- Applies "Tell, don't ask" principle
- Recommends namespaced models
- Identifies empty helpers

### Views
- Recommends local variables in partials
- Avoids instance variable dependencies

### Migrations
- Recommends `say` and `say_with_time` for logging

### Security
- Checks for SQL injection risks
- Identifies XSS vulnerabilities
- Ensures CSRF protection
- Validates authentication/authorization

### Code Quality
- Enforces DRY principle
- Ensures single responsibility
- Removes trailing whitespace

### Performance
- Optimizes database queries
- Recommends appropriate eager loading
- Suggests caching strategies

## Resources

This skill includes:
- Comprehensive best practices documentation organized by category
- Code examples for each practice
- Common anti-patterns to avoid
- Reference links to source material

## Usage Examples

### Code Review
When reviewing Rails code, Claude will:
- **Comprehensively analyze code against Rails best practices**
- **Identify N+1 query problems and suggest optimizations**
- **Flag params hash modifications and security issues**
- **Suggest eager loading opportunities**
- **Recommend security improvements**
- **Check for proper error handling patterns**
- **Verify adherence to Rails conventions**
- **Provide actionable feedback with code examples**

### Code Generation
When generating Rails code, Claude will automatically:
- **Follow Rails best practices from the start**
- **Use `Time.zone.now` instead of `Time.now`**
- **Check `save` return values or use `save!`**
- **Avoid `default_scope` anti-patterns**
- **Use strong parameters in controllers**
- **Prevent N+1 queries with proper eager loading**
- **Apply proper error handling patterns**
- **Follow Rails naming conventions and structure**
- **Implement security best practices**

### Refactoring
When refactoring, Claude will:
- Extract repeated code
- Apply "Tell, don't ask" principle
- Improve query performance
- Enhance code organization

## Categories

The skill covers practices in:
- Timezone handling
- ActiveRecord patterns
- Controller design
- Error handling
- Code organization
- View patterns
- Migrations
- Security
- Code quality
- Performance optimization
- Testing
- General Rails conventions

## Source and Attribution

This skill is **based on concepts** from [rails-bestpractices.com](https://rails-bestpractices.com/), 
a community-driven collection of Rails best practices. 

**Important**: Content is rewritten in our own words, not copied verbatim. We provide 
attribution and source links throughout. See [COPYRIGHT.md](COPYRIGHT.md) for copyright 
information and legal considerations.

## Version

Current version: 1.0.0

## Maintenance

This skill is maintained and updated as new Rails best practices emerge. Categories are organized for easy reference and extension.

## Attribution

This skill is based on publicly available best practices from [rails-bestpractices.com](https://rails-bestpractices.com/). The practices themselves are community knowledge. This skill structure, organization, and documentation are original work.

## License

MIT License - See [LICENSE](LICENSE) file for details.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to contribute improvements, new practices, or documentation updates.

