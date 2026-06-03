# Security Review Skill for Claude Code

A comprehensive security review skill that enables Claude Code to perform systematic security audits with **working proof-of-concept exploits for every finding**.

## The Iron Law

```
NO FINDING WITHOUT A WORKING EXPLOIT
```

Suspecting a vulnerability is worthless. This skill requires proving exploitation.

## What It Does

- **Automated Scanning**: Runs SAST, SCA, secret detection, and infrastructure scanning tools
- **Manual Code Review**: Systematic review for injection, auth, and data exposure vulnerabilities
- **Exploit Development**: Creates working PoC exploits for every vulnerability found
- **Severity Classification**: CVSS-aligned severity ratings with business impact
- **Structured Reporting**: Professional security reports with remediation guidance

## Installation

### Option 1: Clone to skills directory

```bash
git clone https://github.com/dilaz/security-review-skill.git ~/.claude/skills/security-review
```

### Option 2: Copy the skill file

```bash
mkdir -p ~/.claude/skills/security-review
curl -o ~/.claude/skills/security-review/SKILL.md https://raw.githubusercontent.com/dilaz/security-review-skill/main/SKILL.md
```

## Usage

The skill activates automatically when you:
- Ask Claude Code to perform a security audit
- Request vulnerability assessment or penetration testing
- Ask it to find security issues in code
- Review code that handles user input, executes commands, reads files, or makes network requests

Example prompts:
- "Review this codebase for security vulnerabilities"
- "Find security issues in the authentication system"
- "Perform a security audit of this API"

## Required Tools

The skill uses these security tools (install as needed):

### Static Analysis (SAST)
```bash
pip install opengrep bandit
npm install -g eslint eslint-plugin-security
go install github.com/securego/gosec/v2/cmd/gosec@latest
npm install -g @ast-grep/cli
```

### Dependency Scanning (SCA)
```bash
brew install trivy grype  # macOS
pip install pip-audit
go install golang.org/x/vuln/cmd/govulncheck@latest
```

### Secret Detection
```bash
brew install gitleaks  # macOS
# trufflehog: https://github.com/trufflesecurity/trufflehog
```

## Workflow

```
Start Review
    ↓
Run Automated Scanners (SAST, SCA, secrets)
    ↓
Manual Code Review (injection, auth, data exposure)
    ↓
Vulnerability Found? → Write Exploit PoC
    ↓
Exploit Works? → Document with Severity
    ↓
Generate Report
```

## License

MIT
