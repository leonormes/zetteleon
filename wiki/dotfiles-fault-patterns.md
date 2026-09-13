---
tags:
- wiki
- dotfiles
- chezmoi
- error-patterns
title: Dotfiles Fault Patterns
permalink: llmeon/wiki/dotfiles-fault-patterns
---

# Dotfiles Fault Patterns

Living document for classifying and tracking chezmoi / topgrade failure patterns. Updated after each retrospective.

## Pitfall Categories

| Category | Description | Frequency | Mitigation |
|----------|-------------|-----------|------------|
| `whitespace-trim-bug` | Template whitespace control (`{{- end -}}`) eats syntax-critical newlines before `fi`, `done`, `else` | — | Render + `bash -n` before apply; document trim rules |
| `stale-data-file` | `.chezmoidata/` file exists on disk but removed from pipeline — chezmoi still loads it silently | — | Verify `rm` after `git rm`; check with `chezmoi execute-template` |
| `tty-requirement` | `chezmoi apply` blocks mid-sequence — no TTY for conflict prompts | — | Systematic scan + batch resolve per dotfiles-maintenance skill |
| `execution-order` | Script in wrong phase — runs before its dependencies exist | — | Verify phase docs in dotfiles-maintenance skill |
| `brew-bundle-hang` | `brew bundle` hangs on cask CDN TLS rejection | — | Remove from inventory; re-add when CDN fixed |
| `path-resolution` | Tool binary not found from within chezmoi context (keg-only, missing mise shim) | — | Add opt paths to `_.path` in mise config |
| `shebang-python-drift` | Python-script CLI (pipx, others) resolves `env python3` to system 3.9.6 because mise shims sit at END of PATH, after /usr/bin | Repeat (issues #3, #8) | Chezmoi-managed `~/.local/bin/pipx` wrapper that prepends `mise/installs/python/latest/bin` to PATH before exec; `PIPX_DEFAULT_PYTHON` alone is NOT enough — it only fixes target venv Python, not the launcher runtime |
| `wrapper-subtool-drift` | CLI wrapper fixes launcher Python but sub-tool (uv backend) still missing on PATH — pipx upgrade fails "uv executable could not be found" | New (issue #10) | Wrapper must prepend ALL mise bin dirs the tool depends on (python + uv for pipx); verify with `pipx environment \| grep BACKEND` |
| `stale-cask-binary` | Interrupted cask upgrade leaves orphan binary; next upgrade fails "It seems there is already a Binary at" | New (issue #11) | `sudo rm <orphan-binary>` then reinstall cask; watch for after killed brew bundle runs |
| `data-source-drift` | Hardcoded array diverged from packages.yaml source of truth | — | Eliminate hardcoded lists; source from data layer |
| `hash-header-drift` | SHA256 hash path in run_onchange script not updated for renamed/moved data file | — | Update hash path in every consumer when data source moves |
| `other` | New/unclassified | — | Add to this table after retrospective |

## Retrospective History

| Date | Total | Categories | Trend |
|------|-------|------------|-------|