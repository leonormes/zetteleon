---
title: Hermes OpenRouter + Claude Code CLI Configuration Research
created: '2026-05-27T12:13:00+00:00'
source: pieces-ltm
pieces_ids:
- 78c22094-fd94-4479-af2a-b6b747ee689f
- fad6006c-7e79-418f-8b41-d6480f0e18bc
- 10a11651-64de-4c69-90a0-25f6f72ce0af
tags:
- raw
- pieces
- hermes
- openrouter
- claude-code
- mesh
permalink: llmeon/raw/2026-05-27-pieces-hermes-openrouter-claude
---

# Hermes OpenRouter + Claude Code CLI Configuration Research

## Asset 1 (Pieces: 78c22094-fd94-4479-af2a-b6b747ee689f)

**Captured:** 2026-05-27T09:12:09Z

User request:

> I am struggling to get hermes to use the claude code cli. It times out. If I were to use the openrouter so hermes could use the different models would it still be affordable? I am imaging the hermes using a free model (owl alpha) to plan what to do then use more capable models for the complex stuff. It is not working like that at the moment. reseach openrouter and offer a solution that is optimal

## Asset 2 (Pieces: fad6006c-7e79-418f-8b41-d6480f0e18bc)

**Captured:** 2026-05-27T09:18:15Z

Pagination confirmed sufficient. LTM corpus exhausted — no additional material relevant to Hermes + OpenRouter problem space.

## Hermes + OpenRouter: Complete Solution

The real problem: **Claude Code CLI timeouts**

- Today (27 May): debugging `smart-mcp-proxy`'s streamable-HTTP transport
- The proxy is in `CALL_TOOL` mode — only exposes `retrieve_tools` and `call_tool`
- Claude Code CLI timing out when invoked by Hermes

## Asset 3 (Pieces: 10a11651-64de-4c69-90a0-25f6f72ce0af)

**Captured:** 2026-05-27T09:16:35Z

Hermes + Claude Code CLI Timeouts + OpenRouter Multi-Model Solution

### What is actually happening right now

- **Today (27 May, ~09:45–09:53 BST):** debugging `smart-mcp-proxy`'s streamable-HTTP transport
- The proxy is in `CALL_TOOL` mode — it only exposes `retrieve_tools` and `call_tool`