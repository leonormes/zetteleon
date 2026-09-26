---
title: Pieces Removal 2026-09-26
type: note
permalink: llmeon/maintenance/pieces-removal-2026-09-26
tags:
- pieces
- cleanup
- brew
- chezmoi
---

Pieces OS, Pieces app, and Pieces CLI completely removed from system.

**Brew:** Uninstalled casks `pieces` (v6.1.0), `pieces-os` (v12.6.2) + formula `pieces-cli` (v1.20.1, 2.6K files, 28.9MB). Brew auto-removed 3 orphaned formulae (certifi, pydantic, rpds-py).

**System cleanup:** Launch agents, app bundles, `~/Library/Application Support/com.pieces.*` + `pieces-cli`, preferences, caches, Caskroom backups.

**Chezmoi:** Removed from packages.yaml (registry + inventory) + deleted tracked zsh completion (402 lines). Committed as 4885c26.

**Verification:** brew casks/formulae, processes, apps, launch agents, support files, preferences, caches, chezmoi managed — all clean.