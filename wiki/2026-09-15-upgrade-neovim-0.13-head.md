---
tags:
- hermes
- solution
- neovim
- upgrade
- brew-head
source: owl-alpha
permalink: llmeon/wiki/2026-09-15-upgrade-neovim-0.13-head
---

# Upgrade Neovim to 0.13.0-dev via Brew HEAD

## Problem
Neovim 0.13.0 hasn't been released as stable yet (latest stable = 0.12.5). The user wanted to use the development version available via `brew install --HEAD`.

## What was done

1. **Added neovim/neovim tap** (migrated to homebrew-core already, so only for reference)
2. **Resolved SSL certificate issue** — system curl at `/usr/bin/curl` uses SecureTransport which failed to verify GitHub's SSL certs. Brew's own curl (`/opt/homebrew/bin/curl`, 8.22.0) works. Used `HOMEBREW_FORCE_BREWED_CURL=1` to force brew to use its own curl.
3. **Installed neovim --HEAD** — built in 1m16s. Installed to `/opt/homebrew/Cellar/neovim/HEAD-d0f5070_1`.
4. **Removed mise-managed neovim** — `mise rm neovim` and cleaned up stale install dir + shim to avoid conflicts.
5. **Verified** — `nvim --version` shows `NVIM v0.13.0-dev-1645+gd0f50703f0-Homebrew`, LazyVim loads cleanly.

## Files Changed
- `~/.config/mise/config.toml` — removed neovim from managed tools

## Key Commands
```bash
HOMEBREW_FORCE_BREWED_CURL=1 brew install --HEAD neovim
mise rm neovim
rm -rf ~/.local/share/mise/installs/neovim/latest
rm -f ~/.local/share/mise/shims/nvim
```