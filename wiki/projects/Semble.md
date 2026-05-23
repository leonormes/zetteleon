---
title: Semble Code Search
wiki_type: dossier
entity_kind: project
created: 2026-05-21T13:30:00+00:00
modified: 2026-05-21T13:30:00+00:00
tags: [wiki, dossier, project]
sources:
  - raw/2026-05-21-pieces-semble
  - raw/2026-05-21-pieces-general
connections:
  - [[Hermes-Agent]]
---

## Summary

**Semble Code Search** is a project to integrate the [Semble](https://github.com/MinishLab/semble) semantic code search library as the primary code-search mechanism for Hermes agents. It replaces the brute-force `grep` + `read` architecture with a highly optimised, localised semantic + BM25 code-aware search model, achieving ~84% token reduction on multi-file exploration.

## Key Facts

- Semble provides hybrid semantic + BM25 code-aware search with ~250ms cold-index speeds and NDCG@10 ~0.854 — [[raw/2026-05-21-pieces-semble]] (Pieces: 6c42a849-78d)
- Uses ~98% fewer tokens than grep+read for multi-file exploration — [[raw/2026-05-21-pieces-semble]] (Pieces: 6c42a849-78d)
- Migration completed on 2026-05-21: Semble installed, MCP interfaces added, chezmoi tracking configured, sub-agent templates created — [[raw/2026-05-21-pieces-general]] (Pieces: f9e677dc-35a)
- Token savings tracker shows 84% reduction on just 2 calls, validating the core value proposition — [[raw/2026-05-21-pieces-general]] (Pieces: f9e677dc-35a)
- The `<50ms` target from the spec applies to Semble's index traversal once the model is loaded; total wall time includes embedding generation — [[raw/2026-05-21-pieces-general]] (Pieces: f9e677dc-35a)
- Invoked via `semble search "<query>" ./` or `uvx --from "semble[mcp]" semble` if not on `$PATH` — [[raw/2026-05-21-pieces-semble]] (Pieces: 6c42a849-78d)

## Timeline

- **2026-05-21** — Project initiated; Hermes `/goal` mission template created for agent deployment
- **2026-05-21** — Migration completed (6 steps): install, MCP integration, chezmoi tracking, sub-agent templates, verification

## Connections

- [[Hermes-Agent]] — Semble is integrated as a Hermes agent tool
- [[Token-Usage]] — Primary motivation is token reduction

## Contradictions

*None identified.*

## Open Questions

- What is the long-term maintenance plan for Semble indexing as the codebase grows?
- Are there any edge cases where grep+read is still preferred over Semble?
