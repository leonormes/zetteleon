---
type: wiki
title: Dotfiles Maintenance — 2026-10-14
tags:
- chezmoi
- dotfiles-maintenance
- hermes
actor: agent/hermes
generated: 2026-10-14 08:45:00+01:00
verified: 2026-10-14 08:50:00+01:00
stale_after: 2026-11-14
permalink: llmeon/wiki/2026-10-14-dotfiles-maintenance
---

# Dotfiles Maintenance — 2026-10-14

Ran full dotfiles maintenance protocol on the chezmoi repo.

## Issues Found & Fixed

### 1. Stale .chezmoiignore (non-template) — REMOVED
- The non-template `.chezmoiignore` had a stale subset of rules from `.chezmoiignore.tmpl`
- Double-ignore files created confusing dual-rule system
- **Fix**: `git rm .chezmoiignore`, consolidated all rules into `.chezmoiignore.tmpl`

### 2. Missing .hermes/config.yaml ignore rule — ADDED
- `.hermes/config.yaml` (`_config_version` auto-incremented by Hermes) was not in `.chezmoiignore.tmpl`
- Only existed in the stale non-template `.chezmoiignore`
- **Fix**: Added with comment explaining app-tracked status

### 3. Skills dir ignore pattern — FIXED
- `.hermes/skills/*` only ignored contents, not the directory root
- Caused TTY conflict on `chezmoi apply --dry-run` when skills dir changed on disk
- **Fix**: Changed to `.hermes/skills` (proper directory-ignore pattern)

## State DB Notes
- `00-bootstrap.sh` and `99-verify.sh` have stale entries in chezmoi's state DB (shown as `R` in `chezmoi status`)
- `chezmoi forget` reports these as "not managed" despite appearing in `chezmoi managed` — likely run-script entries that can't be forgotten via the standard path
- Same issue with `verify_state.sh`
- These are cosmetic only — `chezmoi apply --dry-run` shows no pending changes

## Verification
- All 6 run scripts pass bash syntax validation
- `chezmoi apply --force --no-tty` → **SYSTEM CONVERGED. All systems green.**
- All 10 verification checks passed (binaries, Brewfile, mise, 1MCP, Topgrade, secrets)
- Committed and pushed: `8efa47d`
- Branch: `development` → `origin/development`