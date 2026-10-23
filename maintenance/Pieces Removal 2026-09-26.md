---
created: 2026-09-26T07:38:23+00:00
modified: 2026-10-22T15:11:04+00:00
permalink: llmeon/maintenance/pieces-removal-2026-09-26
tags: [brew, chezmoi, cleanup, pieces]
title: Pieces Removal 2026-09-26
type: note
---

Pieces OS, Pieces app, and Pieces CLI completely removed from system.

Brew: Uninstalled casks `pieces` (v6.1.0), `pieces-os` (v12.6.2) + formula `pieces-cli` (v1.20.1, 2.6K files, 28.9MB). Brew auto-removed 3 orphaned formulae (certifi, pydantic, rpds-py).

System cleanup: Launch agents, app bundles, `~/Library/Application Support/com.pieces.*` + `pieces-cli`, preferences, caches, Caskroom backups.

Chezmoi: Removed from packages.yaml (registry + inventory) + deleted tracked zsh completion (402 lines). Committed as 4885c26.

Verification: brew casks/formulae, processes, apps, launch agents, support files, preferences, caches, chezmoi managed—all clean.
