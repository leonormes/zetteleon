---
title: Token-Usage
wiki_type: dossier
entity_kind: project
created: 2026-05-18T13:40:46.635993+00:00
modified: 2026-05-18T13:40:46.635995+00:00
tags: [wiki, dossier, project]
sources: ["2026-05-18-pieces-cuh-rbac-permissions.md", "2026-05-18-pieces-worker-status-reflections.md", "2026-05-18-pieces-hermes-gitlab-research.md", "2026-05-18-pieces-brain-mcp-integration.md", "2026-05-18-pieces-hermes-diagnostic-session.md", "2026-05-18-pieces-llm-mcp-chezmoi-config.md"]
---

## Summary

Tracking and optimisation of LLM token consumption across sessions, including cost analysis and context compression strategies.

This project page was created during the Project Check-In on 2026-05-18, based on 10 Pieces LTM captures from the last 4 hours.

## Key Facts

> "meta_complete (1245650 input + 7913 output + 702 reasoning tokens, $8.8938)..." — [[raw/2026-05-18-pieces-cuh-rbac-permissions.md]]
> "Both pagination passes returned `sufficient` / no new material changing the ledger. The second cursor still has a `fetchMore` but the candidates are all repeats from the same backlog refinement meetin..." — [[raw/2026-05-18-pieces-cuh-rbac-permissions.md]]
> "Now I have a complete picture. Here is the current status:

---

## brain-mcp Integration — Current Status

### What has been confirmed from your filesystem and memory

**`.chezmoidata.toml` confirmed..." — [[raw/2026-05-18-pieces-cuh-rbac-permissions.md]]
> "The user has pasted a summary from Hermes about the brain-mcp integration status. The key findings are:

1. `brain-mcp` CLI doesn't have a "server" subcommand - its commands are: setup, add, remove, s..." — [[raw/2026-05-18-pieces-cuh-rbac-permissions.md]]
> "Summary: Brain-mcp Integration Status
     Root Cause Identified

     The brain-mcp package does not expose a server subcommand via its CLI. The --help output shows only these commands:
     - setup,..." — [[raw/2026-05-18-pieces-cuh-rbac-permissions.md]]
> "completed (37899 input + 759 output + 332 reasoning tokens, $0.2722)..." — [[raw/2026-05-18-pieces-cuh-rbac-permissions.md]]
> "meta_complete (359893 input + 1140 output + 216 reasoning tokens, $2.4501)..." — [[raw/2026-05-18-pieces-cuh-rbac-permissions.md]]
> "```
## MISSION: Fix brain-mcp proxy registration

## CONTEXT
brain-mcp was added to mcpproxy but its tools are not registering.
Root cause: `.chezmoidata.toml` has `command = "NPX"` — it must be `comm..." — [[raw/2026-05-18-pieces-cuh-rbac-permissions.md]]

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
