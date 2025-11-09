# Makefile for Modern Markdown Formatting and Linting in Zettelkasten Vault

# Shell configuration
SHELL := bash

# Directory where markdown files are located
TARGET_DIR := 100_zettelkasten

# Prettier config file (located at root)
PRETTIER_CONFIG := .prettierrc.json

# Modern markdownlint-cli2 config file (located at root)
LINT_CONFIG := .markdownlint-cli2.jsonc

# Detect local binaries if present; fallback to npx
ifeq ($(shell command -v markdownlint-cli2 2>/dev/null),)
  MLC2 := npx -y markdownlint-cli2
else
  MLC2 := markdownlint-cli2
endif

ifeq ($(shell command -v prettier 2>/dev/null),)
  PRETTIER := npx -y prettier
else
  PRETTIER := prettier
endif

.PHONY: format lint check format-all lint-all md.lint md.fix md.format md.check md.all help

# Modern CLI2 targets - recommended approach
# Lint using markdownlint-cli2 (respects .markdownlint-cli2.jsonc config automatically)
md.lint:
	@echo "Linting markdown files with markdownlint-cli2..."
	$(MLC2)
	@echo "Linting complete."

# Auto-fix using markdownlint-cli2 --fix (safe, non-destructive fixes)
md.fix:
	@echo "Auto-fixing markdown files with markdownlint-cli2..."
	$(MLC2) --fix
	@echo "Auto-fixing complete."

# Format using Prettier for advanced formatting (tables, etc.)
md.format:
	@echo "Formatting markdown files with Prettier..."
	$(PRETTIER) --config $(PRETTIER_CONFIG) --write "**/*.md"
	@echo "Formatting complete."

# Comprehensive workflow: fix, then lint
md.all: md.fix md.lint
	@echo "Complete markdown processing finished."

# Check alias for linting
md.check: md.lint

# Legacy targets (backwards compatibility) - use fd with specific directory
# Format markdown files using Prettier in TARGET_DIR
format:
	@echo "Formatting markdown files in $(TARGET_DIR)..."
	cd $(TARGET_DIR) && fd -e md --exclude "Question for Bessie about her learning.md" --exec $(PRETTIER) --config ../$(PRETTIER_CONFIG) --write
	@echo "Formatting complete."

# Lint markdown files in TARGET_DIR (legacy - less efficient than CLI2 approach)
lint:
	@echo "Linting markdown files in $(TARGET_DIR) (legacy mode)..."
	cd $(TARGET_DIR) && fd -e md --exclude "Question for Bessie about her learning.md" --exec $(MLC2) --config ../$(LINT_CONFIG)
	@echo "Linting complete."

# Format all markdown files in the vault (legacy)
format-all:
	@echo "Formatting all markdown files in the vault (legacy mode)..."
	fd -e md --exclude "assets" --exclude "000_inbox/journals" --exclude "templates" --exclude "210_productivity/ProdOS" --exclude "Excalidraw" --exclude "Readwise" --exclude "100_zettelkasten/Question for Bessie about her learning.md" --exec $(PRETTIER) --config $(PRETTIER_CONFIG) --write
	@echo "Formatting complete."

# Lint all markdown files in the vault (legacy - use md.lint instead)
lint-all:
	@echo "Linting all markdown files in the vault (legacy mode)..."
	fd -e md --exclude "assets" --exclude "000_inbox/journals" --exclude "templates" --exclude "210_productivity/ProdOS" --exclude "Excalidraw" --exclude "Readwise" --exclude "100_zettelkasten/Question for Bessie about her learning.md" --exec $(MLC2) --config $(LINT_CONFIG)
	@echo "Linting complete."

# Check (alias for lint) - outputs errors without fixing
check: lint

# Display help information
help:
	@echo "Modern Markdown Tooling Commands (RECOMMENDED):"
	@echo "  make md.lint    - Lint all markdown files using markdownlint-cli2"
	@echo "  make md.fix     - Auto-fix markdown issues using markdownlint-cli2 --fix"
	@echo "  make md.format  - Format markdown files using Prettier (tables, etc.)"
	@echo "  make md.all     - Complete workflow: fix + lint"
	@echo "  make md.check   - Alias for md.lint"
	@echo ""
	@echo "Legacy Commands (backwards compatibility):"
	@echo "  make format     - Format markdown files in $(TARGET_DIR) using Prettier"
	@echo "  make lint       - Lint markdown files in $(TARGET_DIR)"
	@echo "  make format-all - Format all markdown files in the vault (with exclusions)"
	@echo "  make lint-all   - Lint all markdown files in the vault (with exclusions)"
	@echo "  make check      - Alias for 'make lint'"
	@echo ""
	@echo "Configuration Files:"
	@echo "  .markdownlint-cli2.jsonc - Modern linting rules (CLI2)"
	@echo "  .prettierrc.json        - Prettier formatting rules"
	@echo ""
	@echo "  make help       - Show this help message"
