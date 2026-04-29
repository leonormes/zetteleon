---
title: Unified LLM Router Cockpit
wiki_type: dossier
entity_kind: project
created: 2026-04-29T08:35:00+00:00
modified: 2026-04-29T08:35:00+00:00
tags: [wiki, dossier]
sources: [raw/2026-04-29-pieces-unified-llm-router-cockpit]
---

## Summary

An incremental build plan to unify Leon's diverse LLM tooling (Ollama, Hermes Agent, Claude, Gemini, Pieces, Cursor, iTerm, Zellij) into a single deterministic workflow with three layers: Cockpit (workspace layouts), Router (tiered model routing), and Memory (PKM compounding). The workspace is chezmoi-managed at `~/.local/share/chezmoi`.

## Key Facts

- Inspired by a structured prompt intended for Claude Code to implement the cockpit architecture inside a chezmoi dotfiles repo.
  > "Implement the Unified LLM Router Cockpit via Chezmoi" — [[raw/2026-04-29-pieces-unified-llm-router-cockpit]] (Pieces: a58e5c2f-bb9e-4d0c-9468-c4d4827fcb00)
- Uses Ollama (local plus cloud subscription), Hermes Agent (via Ollama), Claude (paid), Gemini (paid via MCP proxy), Pieces for Developers (LTM context), and Cursor.
  > "Ollama (local models + cloud subscription), Hermes Agent (autonomous agent with skills, cron, gateway, memory), Gemini CLI + MCP proxy, Cursor" — [[raw/2026-04-29-pieces-unified-llm-router-cockpit]] (Pieces: c29b18d3-c6a1-4d88-a4d5-9ad3f1a2b4e0)
- Includes three Zellij layout files (`llm-local.kdl`, `llm-dev.kdl`, `llm-research.kdl`) and shell aliases (`ll`, `ld`, `lr`).
  > "Create three Zellij layout files and add them to chezmoi" — [[raw/2026-04-29-pieces-unified-llm-router-cockpit]] (Pieces: 0cb1c751-9e4c-48ae-9d06-3c8c3116116f)
- Specifies a tiered model routing strategy in the Hermes config:
  - Tier 0 (Local): Ollama → `qwen3.5`
  - Tier 1 (Cheap Cloud): Ollama Cloud → `minimax-m2.7:cloud`
  - Tier 2 (Premium): Anthropic → `claude-sonnet`
  > "Tier 0 (Local): Ollama → qwen3.5 ... Tier 2 (Premium): Anthropic → claude-sonnet" — [[raw/2026-04-29-pieces-unified-llm-router-cockpit]] (Pieces: 76eec105-981b-4022-ac99-da5c663c1482)

## Connections

- [[raw/2026-04-29-pieces-unified-llm-router-cockpit]]
- [[wiki/concepts/Chezmoi Dotfiles Management]] (concept, to be created)

## Contradictions

_(none identified)_

## Open Questions

- What is the exact fallback order if the premium tier is rate-limited?
- How is cost attribution tracked per session / per tier?
