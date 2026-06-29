---
title: Hermes Agent
wiki_type: dossier
entity_kind: project
created: 2026-05-12T22:07:54+0000
modified: 2026-05-16 09:13:00+01:00
tags:
- wiki
- dossier
- project
sources:
- raw/2026-05-12-pieces-hermes-agent
- raw/2026-05-16-pieces-hermes-session
permalink: llmeon/wiki/projects/hermes-agent
---

The **Hermes Agent** workstream was identified from Pieces LTM activity captured on 2026-05-12. This page tracks the project's scope, timeline, and key facts.

## Summary

Hermes Agent is the core orchestrator system managing LLM provider routing, skill-based task execution, and PKM vault synthesis. Recent activity (2026-05-15) focused on delegation logic inspection and session synthesis workflows involving multi-page cursor pagination.

## Key Facts

- Session activity on 2026-05-15 involved large-context orchestration with 1.1M+ input tokens and $8.05 cost for a single synthesis operation. > "meta_complete (1129028 input + 14248 output + 3081 reasoning tokens, $8.0493)" — [[raw/2026-05-16-pieces-hermes-session]] (Pieces: f5738669-223d-4c48-8c47-fe20cc869dae)
- Delegation logic inspection was performed on the Gemini skill file to understand multi-agent orchestration patterns. > "Now I have the full picture. Let me read the Gemini skill file to see the current delegation logic:" — [[raw/2026-05-16-pieces-hermes-session]] (Pieces: e45bca2a-528b-4a12-9b90-ceb0bc714bf6)
- Session synthesis workflows use cursor-based pagination (`fetchMore`) to handle large result sets. > "The evaluator says I have one remaining fetchMore cursor. Let me paginate it and then deliver the synthesis answer immediately after." — [[raw/2026-05-16-pieces-hermes-session]] (Pieces: ebe60ea4-157f-47de-b5f3-3d643eeace5d)

## Timeline

- **2026-05-12** — Project identified via Pieces LTM ingest; initial activity captured.
- **2026-05-15** — Large-context synthesis session executed (1.1M+ tokens); delegation logic review performed on Gemini skill file.


- **2026-05-28**: Comprehensive MCP proxy failure analysis completed — identified that Hermes does not use injected native MCP tools (`mcp_mcp-proxy_*`) and instead attempts raw HTTP to port 8000 which always fails. A 4-tier fallback chain was designed and documented.
  > "Hermes doesn't know that the mcp-proxy tools are already injected into its session as native tool calls" — [[raw/2026-05-28-pieces-hermes-mcp-proxy-fix]] (Pieces: 5b9878d5-de2e-4362-be83-88bf0e0daf32)

## Connections

- [[Hermes-Agent]] (skill system)
- [[PKM System]] (Obsidian vault integration)
- [[MCP Proxy Robustness and High Availability]] (MCP server management)
- [[Hermes-Multi-Model-Routing-Strategy]] _(architectural design for free-model-first routing matrix: Owl Alpha for planning, premium models for execution)_

## Contradictions

*None identified.*

## Open Questions

- What is the primary objective of this workstream?
- Who are the key stakeholders?
- What is the expected timeline for completion?

- **2026-05-12** — Project identified via Pieces LTM ingest; initial activity captured.

- **2026-05-28**: Comprehensive MCP proxy failure analysis completed — identified that Hermes does not use injected native MCP tools (`mcp_mcp-proxy_*`) and instead attempts raw HTTP to port 8000 which always fails. A 4-tier fallback chain was designed and documented.
  > "Hermes doesn't know that the mcp-proxy tools are already injected into its session as native tool calls" — [[raw/2026-05-28-pieces-hermes-mcp-proxy-fix]] (Pieces: 5b9878d5-de2e-4362-be83-88bf0e0daf32)

## Connections

- [[Hermes Agent]]
- [[PKM System]]
## Contradictions

*None identified.*
## Open Questions

- What is the primary objective of this workstream?
- Who are the key stakeholders?
- What is the expected timeline for completion?