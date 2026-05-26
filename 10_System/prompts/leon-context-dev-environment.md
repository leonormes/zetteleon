---
aliases: []
created: 2026-02-02T07:05:00+00:00
description: Leon’s dev environment constraints (macOS, zsh, WezTerm, Neovim/VS Code, CLI-first workflow).
modified: 2026-05-26T11:44:37+00:00
tags: [domain/dev-environment, system/prompt, type/context]
title: leon-context-dev-environment
type: prompt
---

## Technical Environment (The Rig)

### Core Stack

- OS: macOS
- Shell: Zsh + zinit
- Terminal: WezTerm
- Editor: Neovim (LazyVim distro). _I am keyboard-driven and think in layers._ And Google Antigravity IDE (VS-Code clone)
- Keyboards: Keyboardio Atreus (QMK firmware).

### Workflow Management

- Dotfiles: Managed via `chezmoi` (single source of truth).
- Package Manager: Homebrew, mise
- Launcher: Raycast (global keymaps).
- Shortcuts: I use Hyper (Hold Esc) and Meh (Hold Space) modifiers.

### Constraint

Any code or configuration suggestions must be compatible with this specific CLI-first, keyboard-centric workflow. Do not suggest GUI-based solutions unless unavoidable.
