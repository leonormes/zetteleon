---
title: Zsh Config — Vim Command-Line Editing
wiki_type: dossier
entity_kind: project
created: 2026-05-21T13:30:00+00:00
modified: 2026-05-22T07:29:00+00:00
tags: [wiki, dossier, project]
sources:
  - raw/2026-05-21-pieces-zsh-config
  - raw/2026-05-21-pieces-zsh-edit-command-line-response
connections:
  - [[Chezmoi]]
---

## Summary

**Zsh Config** project to enable opening the current zsh command line in Vim for editing, using the `edit-command-line` ZLE widget. The user works extensively in the command line with zsh and frequently needs to edit long pasted commands. Configuration is managed via chezmoi.

## Key Facts

- The native zsh mechanism is `edit-command-line` — a ZLE widget that opens the current command buffer in `$VISUAL` / `$EDITOR` — [[raw/2026-05-21-pieces-zsh-config]] (Pieces: 5c936938-42d)
- The user requested a Hermes prompt to fix their chezmoi-managed zsh config for this — [[raw/2026-05-21-pieces-zsh-config]] (Pieces: 833ddbc0-008)
- The user's zsh aliases file is managed by chezmoi — [[raw/2026-05-21-pieces-zsh-config]] (Pieces: f0db2f13-c50)
- The `edit-command-line` ZLE widget must be registered via `zvm_after_init_commands` (not just `bindkey`) because zsh-vi-mode overwrites ZLE keymaps after initialisation — [[raw/2026-05-21-pieces-zsh-edit-command-line-response]] (Pieces: 5c936938-42d)
- The recommended bindings are: `bindkey -M vicmd v edit-command-line` (vim normal mode) and `bindkey "^X^E" edit-command-line` (insert mode fallback) — [[raw/2026-05-21-pieces-zsh-edit-command-line-response]] (Pieces: 5c936938-42d)
- `VISUAL` must be set to `nvim` if not already configured; belongs in the preflight/runtime zsh module (`00-preflight.zsh.tmpl` or `05-runtime.zsh`) — [[raw/2026-05-21-pieces-zsh-edit-command-line-response]] (Pieces: 5c936938-42d)

## Timeline

- **2026-05-21** — User requested vim command-line editing setup for zsh; Hermes prompt generated

## Connections

- [[Chezmoi]] — Zsh config is chezmoi-managed

## Contradictions

*None identified.*

## Open Questions

- Has the `edit-command-line` binding been applied to the chezmoi-managed zsh config yet?
- What key binding does the user prefer (e.g., `^X^E`, `v`, etc.)?
