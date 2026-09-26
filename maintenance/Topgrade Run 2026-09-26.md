---
title: Topgrade Run 2026-09-26
type: note
permalink: llmeon/maintenance/topgrade-run-2026-09-26
tags:
- maintenance
- topgrade
- brew
---

Topgrade run 2026-09-26 (09:42-09:53). Exit code 1.

**chezmoi apply**: SYSTEM CONVERGED (exit 0). Clean apply, no changes.

**Upgrades**: mise 2026.9.14, awscli 2.37.4, aws-c-s3 1.2.0 (formulae). google-gemini 1.119.2, raycast 2.5.2, windows-app 11.4.2, antigravity-cli 1.2.11 (casks). Hermes v0.21.5+2453 (309 new commits). rustup nightly updated. uv python versions installed (3.11.16, 3.12.14, 3.13.15).

**Issues:**
1. **Stale agy binary** (Pattern 1) — brews cask upgrade failed on antigravity-cli because a stale binary at /opt/homebrew/bin/agy wasn't cleaned by the upgrade. Fixed with `sudo rm -f /opt/homebrew/bin/agy; brew reinstall --cask antigravity-cli`.
2. **Tap trust reset** — 3rd occurrence (logged to GitHub #13). All 8 taps + 1 cask needed re-trust after brew cask upgrade cycle.

**Disk freed**: ~63.5MB from brew bundle cleanup.