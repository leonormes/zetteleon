---
title: LLMeon
wiki_type: dossier
entity_kind: project
created: 2026-05-18 13:40:46.778995+00:00
modified: 2026-05-18 13:40:46.779042+00:00
tags:
- wiki
- dossier
- project
sources:
- 2026-05-18-pieces-cuh-rbac-permissions.md
- 2026-05-18-pieces-worker-status-reflections.md
- 2026-05-18-pieces-hermes-gitlab-research.md
- 2026-05-18-pieces-brain-mcp-integration.md
- 2026-05-18-pieces-hermes-diagnostic-session.md
- 2026-05-18-pieces-llm-mcp-chezmoi-config.md
permalink: llmeon/wiki/projects/llmeon
---

## Summary

LLMeon is the name of the Obsidian vault instance located at /Volumes/DAL/Zettelkasten/LLMeon, serving as the personal knowledge base.

This project page was created during the Project Check-In on 2026-05-18, based on 8 Pieces LTM captures from the last 4 hours.

## Key Facts

> "Now I have a complete picture. Here is the current status:

---

## brain-mcp Integration — Current Status

### What has been confirmed from your filesystem and memory

**`.chezmoidata.toml` confirmed..." — [[raw/2026-05-18-pieces-cuh-rbac-permissions.md]]
> "The user has pasted a summary from Hermes about the brain-mcp integration status. The key findings are:

1. `brain-mcp` CLI doesn't have a "server" subcommand - its commands are: setup, add, remove, s..." — [[raw/2026-05-18-pieces-cuh-rbac-permissions.md]]
> "```
## MISSION: Fix brain-mcp proxy registration

## CONTEXT
brain-mcp was added to mcpproxy but its tools are not registering.
Root cause: `.chezmoidata.toml` has `command = "NPX"` — it must be `comm..." — [[raw/2026-05-18-pieces-cuh-rbac-permissions.md]]
> "The root cause is visible in Hermes' own summary. Here is the diagnosis and fix.

---

## What Happened

Hermes hit its 30-iteration budget mid-debug. The infrastructure is legitimately in place, but ..." — [[raw/2026-05-18-pieces-cuh-rbac-permissions.md]]
> "╭─ ⚕ Hermes ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────..." — [[raw/2026-05-18-pieces-cuh-rbac-permissions.md]]
> "Both grounding checks confirm the architectural claims. Here is the full deliverable.

---

## Review of Your `brain-mcp` Prompt — Fixes Based on Your Actual chezmoi Setup

Your prompt has good bones ..." — [[raw/2026-05-18-pieces-cuh-rbac-permissions.md]]
> "Now I have everything needed to deliver a thorough, grounded review. Here is the full analysis:

---

## Review of Your `brain-mcp` chezmoi Prompt

### What I've established from your memory and files..." — [[raw/2026-05-18-pieces-cuh-rbac-permissions.md]]
> "I want to update my llm mcp config. Here is a prompt I am going to use. Review previous chezmoi changes and offer fixes to this
# MISSION: EXPAND COGNITIVE LAYER VIA MCP-PROXY (CHEZMOI PROTOCOL)

## C..." — [[raw/2026-05-18-pieces-cuh-rbac-permissions.md]]

## Connections

- [[Hermes-Agent]] — Agent orchestration framework that captures activity to Pieces LTM
- [[General]] — Catch-all project for uncategorised work

## Timeline

- **2026-05-18** — Project page created from Pieces LTM ingests

## Contradictions

None identified.

## Open Questions

- What is the long-term scope and ownership of this workstream?
- Should this be merged with an existing project or remain separate?