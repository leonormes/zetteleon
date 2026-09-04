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
| `data-source-drift` | Hardcoded array diverged from packages.yaml source of truth | — | Eliminate hardcoded lists; source from data layer |
| `hash-header-drift` | SHA256 hash path in run_onchange script not updated for renamed/moved data file | — | Update hash path in every consumer when data source moves |
| `other` | New/unclassified | — | Add to this table after retrospective |

## Retrospective History

| Date | Total | Categories | Trend |
|------|-------|------------|-------|