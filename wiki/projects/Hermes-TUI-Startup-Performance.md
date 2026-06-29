---
title: Hermes TUI Startup Performance
wiki_type: dossier
entity_kind: project
created: 2026-05-23 20:15:00+01:00
modified: 2026-05-23 20:15:00+01:00
tags:
- wiki
- dossier
sources:
- raw/2026-05-23-pieces-hermes-tui-slow.md
permalink: llmeon/wiki/projects/hermes-tui-startup-performance
---

# Hermes TUI Startup Performance

## Summary

Investigation into slow `hermes --tui` startup times (30–40+ seconds to reach a usable state). A `/goal` prompt was composed for Hermes to self-diagnose and fix the slow startup configuration.

## Key Facts

- `hermes --tui` takes 30–40+ seconds to reach a usable state — [[raw/2026-05-23-pieces-hermes-tui-slow.md]] (Pieces: f79dcc22)
- A `/goal` prompt was created for self-diagnosis, grounded in the specific config: chezmoi-managed, 81 skills, MCP servers (mcp-proxy/graphify/pieces SSE), multiple profiles, recent migration to v0.13.0 — [[raw/2026-05-23-pieces-hermes-tui-slow.md]] (Pieces: 17a5978e)
- The fix must be persisted via chezmoi at `~/.local/share/chezmoi/` — [[raw/2026-05-23-pieces-hermes-tui-slow.md]] (Pieces: 17a5978e)
- The same session also encountered the `qwen/qwen3.5:cloud` model ID error (see related project) — [[raw/2026-05-23-pieces-hermes-tui-slow.md]] (Pieces: 17a5978e)

## Connections

- [[Hermes Model Configuration]] — related model config error discovered in same session
- [[Hermes Config Production-Ready Audit]] — broader config audit project
- [[Hermes-Agent]] — Hermes agent project page
- [[Chezmoi]] — Hermes config is chezmoi-managed

## Contradictions

_(none)_

## Open Questions

- What is the root cause of the slow startup? (MCP server timeouts? too many skills? model resolution delay?)
- Has the `/goal` prompt been executed yet and produced a diagnosis?
- Are there specific MCP servers or profile configs causing the delay?