---
type: wiki
title: Maintenance Run — 2026-09-25
tags:
- hermes
- maintenance
- chezmoi
- topgrade
- brew
- tap-trust
actor: process/hermes
generated: '2026-09-25T08:43:00+01:00'
verified: '2026-09-25T09:00:00+01:00'
permalink: llmeon/wiki/2026-09-25-maintenance-run
---

# Maintenance Run — 2026-09-25

## chezmoi apply
- **Status:** ✅ **SYSTEM CONVERGED. All systems green.** (Exit 0)
- **Changes:**
  - 82 mise tools installed (74 cached, 8 new; 8 old versions pruned)
  - uv tools: basic-memory, cactus-needle, git-filter-repo, graphify, mcp-server-tree-sitter
  - Needle catalogue regenerated (283 tools across 16 servers)
  - 1MCP health: ✅ live on :3050
  - git state: clean, no changes

## topgrade
- **Status:** ⚠️ **Exited with errors** (Exit 1)
- **Duration:** 08:43 → 09:00 (17 min)
- **Exit code:** 1
- **Steps passed:** Brew (9 formulas), Brew Cask (13 casks), mise, rustup, zinit, npm, pnpm, pipx, uv, chezmoi, cargo, krew, helm, Hermes, agy, Claude Code, Claude Code Plugins, Cursor Extensions, Yazi, Munki, Antigravity CLI, Antigravity Extensions
- **Steps failed (known/ignored):** Containers (ACR auth — expected, in ignore_failures)
- **Steps reported FAILED (transient):** Brew Cask (ARM) — Microsoft Teams curl partial file download; recovered on retry

### Upgrades Applied
| Category | Count | Details |
|----------|-------|---------|
| **Brew formulas** | 9 | openexr 3.4.15→3.5.0, jpeg-xl 0.12.0→0.12.0_1, chafa 1.18.2→1.18.3, mise 2026.9.12→2026.9.13, ca-certificates, awscli 2.37.0→2.37.2, mole 1.55.0→1.56.0, drydock 1.1.4→1.2.1, sofka 0.28.5→0.29.2 |
| **Brew casks** | 13 | antigravity, antigravity-cli, claude, cursor, dbeaver-community, fantastical, microsoft-teams, ollama-app, raycast, slack, windows-app, wireshark-app, zoom |
| **mise** | 0 | 82 tools up to date; 3 min-age warnings (golangci-lint, @mermaid-js/mermaid-cli, uv) |
| **rustup** | 1 | nightly f7575a9da (2026-09-24) |
| **npm** | 8 added, 7 removed, 962 changed | uuid deprecation warnings |
| **uv tools** | 2 | jiratui v1.14.0→v1.15.0, semble v0.6.0→v0.6.1 |
| **Hermes agent** | 1 | v0.21.3→v0.21.5+2144 (main @ 7b761da2) |
| **Antigravity CLI** | 1 | v1.2.10→v1.2.11 |
| **zinit plugins** | 18 | All updated; compile-hook warnings on completion plugins (non-fatal) |
| **Yazi packages** | 3 | lazygit.yazi, smart-enter.yazi, git.yazi |

### Disk Freed
- Brew formula cleanup: ~400.7MB
- Brew cask cleanup: ~919.2MB
- Brew bundle cleanup: ~6.6MB
- **Total: ~1.33 GB**

## Fixes Applied
- **Tap trust reset** (GitHub #13): brew 6.0.0+ upgrade clears formula-level tap trust. 8 formulas + 1 cask needed re-trust. `brew bundle check --global` now returns exit 0.
- **Brewfile drift**: Brewfile now satisfied after tap trust re-applied.

## Unresolved Issues
- #13: Tap trust reset during brew upgrade — persistent pattern, need post-upgrade trust hook
- mise min-age warnings (golangci-lint 2.14.0, @mermaid-js/mermaid-cli 12.0.0, uv 0.12.19) — self-resolving
- Python 3.13.13→3.14.7 and vivid 0.10.1→0.11.1 need config bump

## Totals
- Issues tracked this run: 1 (GitHub #13 — tap trust reset)
- Issues still open: 1