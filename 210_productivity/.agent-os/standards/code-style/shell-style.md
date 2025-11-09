# Shell Script Code Style

## General Principles

### Shebang and Settings

```bash
#!/usr/bin/env bash
set -euo pipefail  # Exit on error, undefined vars, pipe failures
```

### Formatting

- Use 2 spaces for indentation
- Maximum line length: 80 characters
- Use `$()` for command substitution instead of backticks
- Quote variables to prevent word splitting: `"${variable}"`

### Variables and Constants

```bash
# Constants in UPPERCASE
readonly CONFIG_DIR="${HOME}/.config"

# Local variables in functions
function example_function() {
  local input_file="${1}"
  local output_file="${2}"
  # ...
}
```

### Functions

```bash
# Function definition format
function descriptive_name() {
  local param1="${1:-default_value}"

  # Function body
  echo "Processing: ${param1}"
}

# Or alternative syntax for simple functions
descriptive_name() {
  # Function body
}
```

### Error Handling

```bash
# Check command success
if ! command -v git >/dev/null 2>&1; then
  echo "Error: git is not installed" >&2
  exit 1
fi

# Check file existence
if [[ ! -f "${config_file}" ]]; then
  echo "Error: Configuration file not found: ${config_file}" >&2
  exit 1
fi
```

### Conditional Logic

```bash
# Use [[ ]] for tests
if [[ -n "${variable}" ]]; then
  echo "Variable is not empty"
fi

# Multiple conditions
if [[ -f "${file}" && -r "${file}" ]]; then
  echo "File exists and is readable"
fi
```

## Chezmoi-Specific Standards

### Template Files

```bash
# Use chezmoi template syntax for dynamic content
{{- if eq .chezmoi.os "darwin" }}
export HOMEBREW_PREFIX="/opt/homebrew"
{{- else if eq .chezmoi.os "linux" }}
export HOMEBREW_PREFIX="/home/linuxbrew/.linuxbrew"
{{- end }}

# Access chezmoi data
export PROJECT_ROOT="{{ .chezmoi.sourceDir }}"
```

### Configuration Management

```bash
# Check for chezmoi presence
if command -v chezmoi >/dev/null 2>&1; then
  alias cm='chezmoi'
  alias cma='chezmoi apply'
  alias cmd='chezmoi diff'
fi
```

## Best Practices

### Documentation

```bash
#!/usr/bin/env bash
# Purpose: Configure development environment
# Usage: ./setup.sh [--dry-run]
# Dependencies: git, curl, homebrew

set -euo pipefail

# Global constants
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly LOG_FILE="${SCRIPT_DIR}/setup.log"
```

### Logging

```bash
# Logging functions
log_info() {
  echo "[INFO] $*" | tee -a "${LOG_FILE}"
}

log_error() {
  echo "[ERROR] $*" >&2 | tee -a "${LOG_FILE}"
}

log_debug() {
  [[ "${DEBUG:-}" == "true" ]] && echo "[DEBUG] $*" >&2
}
```

### Platform Detection

```bash
# Detect operating system
detect_os() {
  case "${OSTYPE}" in
    darwin*)  echo "macos" ;;
    linux*)   echo "linux" ;;
    *)        echo "unknown" ;;
  esac
}

readonly OS="$(detect_os)"
```

### Safe Operations

```bash
# Safe directory operations
change_directory() {
  local target_dir="${1}"

  if [[ ! -d "${target_dir}" ]]; then
    log_error "Directory does not exist: ${target_dir}"
    return 1
  fi

  cd "${target_dir}" || {
    log_error "Failed to change to directory: ${target_dir}"
    return 1
  }
}

# Safe file operations
backup_file() {
  local file="${1}"

  if [[ -f "${file}" ]]; then
    cp "${file}" "${file}.backup.$(date +%Y%m%d_%H%M%S)"
    log_info "Backed up: ${file}"
  fi
}
```

## Testing

### Use ShellCheck

```bash
# Install shellcheck via homebrew
brew install shellcheck

# Run on all shell scripts
find . -name "*.sh" -exec shellcheck {} \;
```

### BATS Testing Framework

```bash
#!/usr/bin/env bats

# Test file: test_config.bats

@test "config directory exists" {
  run test -d "${HOME}/.config"
  [ "$status" -eq 0 ]
}

@test "git configuration is valid" {
  run git config --get user.name
  [ "$status" -eq 0 ]
  [ -n "$output" ]
}
```
