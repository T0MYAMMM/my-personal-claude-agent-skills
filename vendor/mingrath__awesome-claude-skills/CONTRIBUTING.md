# Contribution Guidelines

Thank you for your interest in contributing to Awesome Claude Code Skills. This resource is community-driven, and your contributions help developers discover and adopt powerful skills for Claude Code.

## Adding a Skill

Please ensure your pull request adheres to the following guidelines:

### Requirements

- The skill must be a Claude Code skill (a `SKILL.md` file or directory following the [Agent Skills specification](https://agentskills.io)).
- The skill must be publicly available (open-source repository, gist, or similar).
- The skill should be tested and functional with Claude Code.
- The skill should do something useful that is not already well-covered by an existing entry.

### Formatting

- Use the following format: `- [skill-name](link) - Description starting with a capital letter and ending with a period.`
- Keep the description concise -- one sentence, no more than 150 characters.
- Do not use promotional language ("best", "amazing", "ultimate").
- Add the skill to the appropriate existing category. If no category fits, propose a new one.
- Maintain alphabetical order within categories.
- Check your spelling and grammar.

### Pull Request

- Make an individual pull request for each skill addition.
- Use the [pull request template](.github/pull_request_template.md).
- Include a brief explanation of why the skill is awesome -- what problem does it solve, and why would other developers want it?
- The pull request title should follow the format: `Add skill-name`.

### Quality Standards

Before submitting, check that the skill:

- [ ] Has a clear and specific `description` in its frontmatter.
- [ ] Follows single responsibility -- it does one thing well.
- [ ] Contains actionable, specific instructions (not vague guidance).
- [ ] Has a `SKILL.md` file under 500 lines (with supporting files for detailed content).
- [ ] Has been tested with real-world use cases.
- [ ] Does not contain hardcoded secrets, API keys, or credentials.
- [ ] Includes examples of expected input/output where applicable.

## Updating an Existing Entry

- If a link is broken, submit a PR to fix or remove it.
- If a description is inaccurate, submit a PR with a corrected description.
- If a skill has been deprecated or archived, submit a PR to remove it.

## Creating a New Category

- If you believe a new category is needed, open an issue first to discuss it.
- New categories should contain at least three skills.
- Category names should be clear and follow the existing naming conventions.

## Reporting Issues

- Use GitHub issues to report broken links, inaccurate descriptions, or other problems.
- Include the skill name and a brief description of the issue.

Thank you for helping make this list awesome.
