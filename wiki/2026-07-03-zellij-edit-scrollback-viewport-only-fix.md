---
tags:
- hermes
- solution
- zellij
- nvim
source: deepseek/deepseek-v4-flash
permalink: llmeon/wiki/2026-07-03-zellij-edit-scrollback-viewport-only-fix
---

# Zellij `EditScrollback` viewport-only capture fix

**Date:** 2026-07-03
**Problem:** Zellij 0.44.3 `EditScrollback` (key `e` in scroll mode) was only capturing the visible viewport content in the temp file passed to nvim, not the full scrollback buffer.

**Root cause:** Zellij's internal `EditScrollback` action appears to write only the visible viewport range to the temp file, despite `scroll_buffer_size` being set to 10000. The `dump-screen --full` CLI command captures the complete buffer correctly.

**Fix:** Created `~/.local/bin/zellij-scrollback.sh` — a wrapper script that:
1. Calls `zellij action dump-screen --full --path <tmpfile>` to capture the full scrollback buffer
2. Opens the result in `nvim -u minimal.lua` for clipboard-aware editing
3. Falls back to Zellij's internal temp file if `dump-screen` fails

**Files changed:**
- `~/.local/bin/zellij-scrollback.sh` (new, chezmoi-tracked)
- `~/.config/zellij/config.kdl` — `scrollback_editor` → wrapper path
- `~/.local/share/chezmoi/dot_config/zellij/config.kdl.tmpl` — same update

**Related config:** `minimal.lua` at `~/.config/nvim/minimal.lua` sets `clipboard=unnamedplus` + explicit pbcopy/pbpaste bindings for Zellij scrollback editing.