---
tags:
- hermes
- maintenance
- dotfiles
- issues-consolidation
source: owl-alpha
permalink: llmeon/wiki/2026-09-15-issues-consolidation
---

# Issues Consolidation — 2026-09-15

## Summary

Ran full issues consolidation on `leonormes/chezmoi` repo (`chezmoi-fault` label).

**Closed (9):** #3 #4 #6 #7 #8 #9 #10 #11 #12
**Still Open (1):** #5 — Docker ACR auth (infra-level, not a chezmoi issue)

## Issues Closed

| # | Title | Closed Reason |
|---|-------|--------------|
| 3 | pipx under topgrade — Python 3.9.6 | Resolved: PIPX_DEFAULT_PYTHON + pipx wrapper |
| 4 | chezmoi git HTTPS auth fails in non-interactive context | Resolved: credential helper in dot_gitconfig.tmpl |
| 6 | duplicate [env] key in mise config.toml | Resolved: template fix at time |
| 7 | chezmoi update fails — non-interactive git HTTPS auth | Superseded by #12; resolved by credential helper |
| 8 | pipx 'Python 3.10 or later' — repeat of #3 | Resolved: pipx wrapper prepends mise python bin |
| 9 | topgrade brew step hangs on msodbcsql18 | Resolved: `brew pin msodbcsql18` |
| 10 | pipx uv backend not found | Resolved: pipx wrapper includes uv bin dir |
| 11 | brew cask antigravity-cli upgrade — stale binary | Resolved: removed stale /opt/homebrew/bin/agy |
| 12 | chezmoi update fails in topgrade — git HTTPS auth (repeat) | Resolved: credential helper; removed from ignore_failures |

## New Skill Created

`custom/dotfiles-maintenance-run` — a proactive run+fix skill that:
1. Pre-flight: checks for stale brew locks/processes
2. Runs `chezmoi apply` with output capture
3. Runs `topgrade --verbose --disable ollama` with output capture
4. Parses output for 6 known failure patterns
5. Applies auto-fixes for each (stale binaries, msodbcsql18 pin, credential helper, etc.)
6. Generates a structured report

Pairs with `chezmoi-error-tracking` (retrospective issue capture) and `dotfiles-maintenance` (deep repair).

## Open Issue

**#5 — Docker ACR auth:** ACR token expiry blocks docker pull in automated contexts. Not a dotfiles issue. Mitigation: pre-topgrade ACR re-auth cron, or storing ACR creds in Docker config.json.