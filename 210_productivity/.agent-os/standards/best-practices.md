# Development Best Practices

## Context

Global development guidelines for Agent OS projects.

<conditional-block context-check="core-principles">
IF this Core Principles section already read in current context:
  SKIP: Re-reading this section
  NOTE: "Using Core Principles already in context"
ELSE:
  READ: The following principles

## Core Principles

### Keep It Simple

- Implement code in the fewest lines possible
- Avoid over-engineering solutions
- Choose straightforward approaches over clever ones

### Optimize for Readability

- Prioritize code clarity over micro-optimizations
- Write self-documenting code with clear variable names
- Add comments for "why" not "what"

### DRY (Don't Repeat Yourself)

- Extract repeated business logic to private methods
- Extract repeated UI markup to reusable components
- Create utility functions for common operations

### File Structure

- Keep files focused on a single responsibility
- Group related functionality together
- Use consistent naming conventions
  </conditional-block>

<conditional-block context-check="dependencies" task-condition="choosing-external-library">
IF current task involves choosing an external library:
  IF Dependencies section already read in current context:
    SKIP: Re-reading this section
    NOTE: "Using Dependencies guidelines already in context"
  ELSE:
    READ: The following guidelines
ELSE:
  SKIP: Dependencies section not relevant to current task

## Dependencies

### Choose Libraries Wisely

When adding third-party dependencies:

- Select the most popular and actively maintained option
- Check the library's GitHub repository for:
  - Recent commits (within last 6 months)
  - Active issue resolution
  - Number of stars/downloads
  - Clear documentation
    </conditional-block>

## Configuration Management Practices

### Chezmoi Standards

- Use template files (`.tmpl`) for dynamic content
- Leverage chezmoi's data files for environment-specific configs
- Test configuration changes locally before commit
- Use `chezmoi diff` to preview changes
- Keep secrets in encrypted files or environment variables

### Shell Script Standards

- Always include shebang: `#!/usr/bin/env bash` or `#!/usr/bin/env zsh`
- Set strict error handling: `set -euo pipefail`
- Use local variables in functions
- Quote variables to prevent word splitting
- Use shellcheck for linting

## Test-Driven Development (TDD)

### Red → Green → Refactor Cycle

- **ALWAYS** follow Red → Green → Refactor cycle
- **DO NOT** generate both tests and implementation code in one step
- A new test must:
  1. Be minimal and independent
  2. Fail without new implementation
  3. Drive the shape of the API (not replicate implementation)
- After a failing test is confirmed, **ONLY THEN** write the smallest code to pass
- After passing, suggest safe, minimal refactor

### Testing for Configuration

- Test shell scripts with bats-core framework
- Validate configuration files with appropriate tools:
  - TOML: use `toml-test` or parsing validation
  - JSON: use `jq` validation
  - YAML: use `yq` validation
- Test chezmoi templates by running `chezmoi execute-template`
- Integration tests should verify actual tool functionality

## Git Workflow

### Commit Message Standards

- Format: `<Jira-ID>: <type>(<scope>): <subject>`
- Use Jira ticket ID from branch name or default to `FFAPP-5288`
- Types: feat, fix, docs, style, refactor, perf, test, build, ci, chore
- Subject: imperative, lowercase, no period
- Examples:
  - `FFAPP-4565: feat(config): add starship configuration`
  - `FFAPP-5288: fix(hammerspoon): correct window management script`

## MCP Server Integration

### Server Configuration

- Place MCP configurations in appropriate client directories
- Use environment variables for sensitive data (API keys)
- Test MCP server connections before deployment
- Document server capabilities and usage

### Available MCP Tools

- **Pieces**: Code snippets and memory management
- **Memory**: Persistent conversation memory
- **Sequential Thinking**: Enhanced reasoning
- **Context7**: Vector search and context
- **Obsidian**: Knowledge base integration
- **Filesystem**: File system operations
- **Git**: Version control operations
