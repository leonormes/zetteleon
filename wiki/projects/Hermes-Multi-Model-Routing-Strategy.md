---
title: Hermes Multi-Model Routing Strategy
wiki_type: dossier
entity_kind: project
created: 2026-05-27T09:12:00+00:00
modified: 2026-05-27T09:18:00+00:00
tags: [wiki, dossier, project]
sources:
  - raw/2026-05-27-pieces-hermes-openrouter-claude
---

## Summary

Research and architectural design for Hermes's multi-model orchestration strategy. The goal is to use free/cheap models (Owl Alpha) for planning and lightweight tasks, reserving premium models (Claude Code CLI, cloud models) for complex execution. Work includes debugging Claude Code CLI timeouts, evaluating OpenRouter model tiers, and designing the optimal routing matrix.

## Key Facts

- **2026-05-27**: User identified a core problem: Claude Code CLI invoked by Hermes times out. Vision: Hermes uses free model (Owl Alpha) for planning, then routes complex expensive tasks to capable models. Current routing is not working as intended — [[raw/2026-05-27-pieces-hermes-openrouter-claude]] (Pieces: 78c22094-fd94-4479-af2a-b6b747ee689f)

- **Streamable-HTTP transport debugging**: Hermes today was debugging `smart-mcp-proxy`'s streamable-HTTP transport. The proxy runs in `CALL_TOOL` mode only (exposes `retrieve_tools` and `call_tool`), which constrains how Claude Code CLI can interact with MCP servers — [[raw/2026-05-27-pieces-hermes-openrouter-claude]] (Pieces: fad6006c-7e79-418f-8b41-d6480f0e18bc)

- **Multi-model affordability question**: User asked whether using OpenRouter for Hermes would remain affordable if Hermes primarily uses free models for planning and only escalates to premium models for complex tasks — [[raw/2026-05-27-pieces-hermes-openrouter-claude]] (Pieces: 78c22094-fd94-4479-af2a-b6b747ee689f)

- **LTM corpus relevance**: Memory search confirmed sufficient coverage of the Hermes + Claude Code timeout problem space. No additional material surfaced in tail pages (mostly FITFILE standup and Azure infra sessions) — [[raw/2026-05-27-pieces-hermes-openrouter-claude]] (Pieces: fad6006c-7e79-418f-8b41-d6480f0e18bc)

## Timeline

- **2026-05-27 (09:12 BST)** — User raised the core question about Hermes multi-model routing and Claude Code CLI timeouts.
- **2026-05-27 (09:15–09:18 BST)** — Memory search and synthesis completed; OpenRouter research scoped.

## Connections

- [[Hermes-Model-Configuration]] (related: past model ID resolution work)
- [[Hermes Config Production-Ready Audit]] (broader config audit)
- [[Hermes-Agent]] (parent project: Hermes orchestration agent)
- [[MCP Proxy Robustness and High Availability]] (streamable-HTTP transport debugging)

## Contradictions

_None identified._

## Open Questions

- What is the actual cost ceiling for OpenRouter usage with the proposed free-model-first routing?
- Does the streamable-HTTP transport timeout affect all MCP tool calls or only Claude Code CLI specifically?
- Should Hermes fall back to direct CLI invocation when MCP proxy transport fails?
