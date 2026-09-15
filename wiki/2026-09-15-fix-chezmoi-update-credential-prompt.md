---
tags:
- hermes
- solution
- topgrade
- chezmoi
- git-auth
source: owl-alpha
permalink: llmeon/wiki/2026-09-15-fix-chezmoi-update-credential-prompt
---

# Fix: chezmoi update prompts for HTTPS credentials in non-interactive shells

## Problem
`chezmoi update` (used by topgrade) prompted for GitHub HTTPS credentials with:
```
fatal: could not read Username for 'https://github.com': Device not configured
```
This blocked topgrade in non-interactive sessions. Was previously worked around via `ignore_failures = ["chezmoi"]`.

## Root Cause
- `chezmoi` repo remote was HTTPS (`https://github.com/leonormes/chezmoi.git`)
- `gh auth status` showed `Git operations protocol: ssh`
- No git credential helper was configured — git fell back to interactive TTY prompt
- `gh auth git-credential get` works for HTTPS with the OAuth token, but `fill` is unsupported when gh is configured for SSH protocol

## Fix
1. Added `[credential]\n\thelper = !gh auth git-credential` to `dot_gitconfig.tmpl` (chezmoi-managed)
2. Ran `chezmoi apply` to deploy the new `.gitconfig`
3. Removed `"chezmoi"` from `ignore_failures` in `topgrade.toml.tmpl`
4. Updated `brew-topgrade-macos` skill with the new pitfall entry

## Verification
- `chezmoi update` now completes cleanly with exit 0
- No TTY prompt for credentials
- `git fetch --dry-run` succeeds non-interactively

## Files Changed
- `~/.local/share/chezmoi/dot_gitconfig.tmpl` — added `[credential]` section
- `~/.local/share/chezmoi/dot_config/topgrade.d/topgrade.toml.tmpl` — removed `"chezmoi"` from `ignore_failures`
- `~/.hermes/skills/devops/brew-topgrade-macos/SKILL.md` — updated docs + new pitfall