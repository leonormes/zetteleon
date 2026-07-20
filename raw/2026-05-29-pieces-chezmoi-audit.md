---
created: 2026-05-29T13:44:28+00:00
modified: 2026-07-20T16:32:59+00:00
permalink: llmeon/raw/2026-05-29-pieces-chezmoi-audit
pieces_ids: [0564f203-1e28-4f6c-a485-5ab385382e8e, 49ca1f2c-5d47-4510-b40a-73c2011fa406, 913df5f6-aa3c-4c49-9914-dcf4b4df4c23, cf86f34c-82cc-426e-b81b-331d70267dfc, fa883503-057b-4ce2-a645-f7b59eed7e55]
source: pieces-ltm
tags: [pieces, raw]
title: 2026-05-29-pieces-chezmoi-audit
---

## Chezmoi Dotfiles Audit—2026-05-29

### Asset 1 (Pieces: 0564f203-1e28-4f6c-a485-5ab385382e8e)

> "I have been trying to build a chezmoi driven dotfiles and config system. I am not sure it is any good. It seems difficult to manage, which is the opposite of the goal. Give me a hermes prompt to investigate the repo and report on redundancy and code smells and suggest refactoring. Search the LTM for work done"

### Asset 2 (Pieces: 913df5f6-aa3c-4c49-9914-dcf4b4df4c23)

> "The user wants me to: 1. Search their LTM for work done on a chezmoi dotfiles/config system 2. Generate a Hermes prompt that will investigate the repo and report on redundancy, code smells, and suggest refactoring. Let me start by searching their LTM for chezmoi-related work, and also try to find the actual repo on their filesystem."

### Asset 3 (Pieces: cf86f34c-82cc-426e-b81b-331d70267dfc)

## Chezmoi Dotfiles Audit Report

Repository: `~/.local/share/chezmoi` (branch: `development`)

Date: 2026-05-29

Scope: Full structural audit—data pipeline, run scripts, templates, Hermes config, verification.

Constraint: Read-only. No changes applied.

---

### 1. Executive Summary

The dotfiles repository is well-architected with a clean CUE-data-driven pipeline and sensible chezmoi conventions. The `generated.json` is in sync with the CUE source, and no hardcoded hostnames or paths leak into templates. The three critical findings are: (1) `sentence-transformers` is listed in `inventory.common` but has no registry entry, which will cause silent resolution failures in any template that iterates inventory; (2) two packages (`cue`, `slack`) are duplicated across `common` and `work` inventories; (3) the `dot_hermes_custom_skills/custom/mcp-proxy/` directory is an empty directory in chezmoi source, yet the runtime `~/.hermes_custom_skops/custom/mcp-integration/SKILL.md` (v3.0.0) is not tracked—this skill would be lost on a fresh `chezmoi apply`. Additionally, four Linux-only `run_*` scripts execute on every macOS apply (harmless but noisy), and `dot_wezterm.lua` (119 lines) is vestigial since Ghostty is the active terminal. Overall health: good, with mechanical cleanups recommended.

### Asset 4 (Pieces: 49ca1f2c-5d47-4510-b40a-73c2011fa406)

> "The user wants me to create a Hermes `/goal` prompt based on the audit report they've shared. This is a COMPOSE scenario—they want me to generate a structured artifact (a Hermes goal prompt) that they can paste into their Hermes system. Let me look at what I know about Hermes from the audit report and what I might know from their memory about how Hermes goals work."

### Asset 5 (Pieces: fa883503-057b-4ce2-a645-f7b59eed7e55)

Generated `/goal` prompt: "CHEZMOI DOTFILES—RESILIENCE & SIMPLICITY REFACTOR"

The generated prompt covers:

- PHASE 1: Fix data pipeline integrity (CUE / packages.yaml)—add missing registry entry for `sentence-transformers`, deduplicate `cue` and `slack`, remove empty `personal: []`
- Written for pasting into `hermes --tui` as a `/goal` command
