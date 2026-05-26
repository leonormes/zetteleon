---
title: Hermes Agent — Discovery Report (Pieces LTM synthesis)
created: 2026-05-24T18:09:28+00:00
source: pieces-ltm
pieces_ids: [70503f11-16c7-4a75-9935-66516e96dfe6, dc22f99a-56a2-445b-8f7f-63d70699adef, d7b19381-e081-4ee1-ad1e-59e4785fc3ac, ee492eb2-78f3-49dc-8842-514461e3f794]
tags: [raw, pieces]
---

# Hermes Agent — Discovery Report

*Synthesised from LTM search results (terminal, editor, browser, chat), `ask_memory` digest (6-month window), and filesystem path scan. All claims are cited to specific tool results.*

## Source Assets

- **Pieces: 70503f11** (18:00:04 UTC) — User's original request for the discovery report
- **Pieces: dc22f99a** (18:00:11 UTC) — Agent initiating multi-wave LTM search
- **Pieces: d7b19381** (18:06:12 UTC) — Draft discovery report (intermediate version)
- **Pieces: ee492eb2** (18:09:28 UTC) — Final discovery report delivered

---

## Asset 1 — User Request (Pieces: 70503f11)

> Context: I've been building a configuration for an agent called "Hermes" using a coding assistant over the past several weeks/months. I now want to commission Hermes itself to review its current configuration and propose optimisations. Before I write that review brief, I need you to consolidate everything you've captured about this work into a structured discovery report.

The user requested 6 sections:
1. Project Identity
2. Current Architectural State
3. Design Decisions & Rationale
4. Incomplete or Pending Work
5. Known Issues & Friction Points
6. External References & Benchmarks

---

## Asset 2 — Agent Search Initiation (Pieces: dc22f99a)

The user wants a comprehensive discovery report about their "Hermes" agent configuration project. This is a COMPOSE scenario - I need to do extensive multi-wave searching across different sources (IDE, terminal, browser, chat) to build a thorough picture.

Search angles initiated:
1. Search for "Hermes" as a hint
2. Search for agent configuration work
3. Check browser activity for related documentation
4. Search for relevant file paths

---

## Asset 3 — Draft Discovery Report (Pieces: d7b19381)

*The circuit breaker fired after multiple duplicate queries. Substantial evidence accumulated across search rounds.*

### Key Findings — Project Identity
- Hermes Agent v0.14.0 (2026.5.16), Python 3.11.15
- Entry point: `/Users/leon.ormes/.local/bin/hermes`
- Source: `/Users/leon.ormes/.hermes/hermes-agent/`
- 14 personalities configured: catgirl, concise, creative, helpful, hype, kawaii, noir, philosopher, pirate, shakespeare, surfer, teacher, technical, uwu
- MCP servers: pieces (stdio), mcp-proxy (http), nop-proxy

### Key Findings — Architectural State
- `model.context_length: 128000`
- `model.default: qwen/qwen3.5-plus-20260420`
- `memory.provider: honcho`
- `max_turns: 30`
- `_config_version: 23`
- Profiles: ops.yaml, thin.yaml, research.yaml, pkm.yaml

### Key Findings — Design Decisions
- Ollama + qwen3.5 chosen over apfel (4K context wall)
- Cloud escalation via kimi-k2.6
- Context length raised to 128K (from 64K) for parallel delegation
- Honcho chosen for graph-based memory persistence
- SOUL.md = system prompt, loaded fresh each message
- Tiered routing: Tier 0 (cheap local) → Tier 1.5 (Owl Alpha) → Tier 1A (Claude Code CLI) → Tier 2 (cloud)

### Key Findings — Pending Work
- TUI startup performance (30-40s)
- brain-mcp cognitive layer upgrade (proposed, not implemented)
- Intelligent model routing policy (designed, not confirmed implemented)
- `hermes update` — 4 commits behind as of 23 May

### Key Findings — Known Issues
- `pieces (stdio) - failed` on every startup
- `mcp-proxy (http) - failed`
- `nop-proxy [failed]`
- TUI timeout: 30-40s to usable state
- Invalid model ID `qwen/qwen3.5:cloud` (fixed to `qwen/qwen3.5-plus-20260420`)

---

## Asset 4 — Final Discovery Report (Pieces: ee492eb2)

*The complete, grounded discovery report delivered after filesystem and ask_memory verification.*

### 1. Project Identity
- Local AI agent runtime built by Nous Research, "Messenger of the Digital Gods"
- Role: Personal AI OS / Mechanical Lead
- Installed v0.11.0 (23 Apr 2026), currently v0.14.0 (2026.5.16)

### 2. Current Architectural State
- Config version 23
- 14 personalities, active: technical
- Custom skills: code-delegate, terraform-sentinel, file-intelligence, api-key-security, library-indexer, pattern-recognition, daily-synthesis, debugging-hermes-tui-commands
- Structural map: chezmoi apply → config.yaml + SOUL.md + .env + skills + memories → hermes gateway → web UI :9119

### 3. Design Decisions
- Tiered routing (SOUL.md §1.6): Tier 0 local → Tier 1.5 Owl Alpha → Tier 1A Claude Code CLI → Tier 2 cloud
- Chezmoi as config management (skip auth files)
- 4-layer memory: built-in → session state → honcho → Obsidian vault
- Apfel rejected (4K context floor), Ollama interim, cloud default

### 4. Incomplete/Pending
- Voice Note Ingestion Skill (planned)
- Daily Digest /digest quick-command (planned)
- Infrastructure Wiki Directory (planned)
- Skill audit / continuous learning loop (planned)
- brain-mcp cognitive layer upgrade (proposed)
- Cost-optimising router (designed, not confirmed live)

### 5. Known Issues
- TUI slow startup (30-40s), connect_timeout: 8 applied
- Pieces MCP recurring failure (stdio vs SSE transport mismatch)
- HTTP 402 billing errors on paid models
- Kanban UI COLUMN_LABEL error (patched directly in dist/index.js)
- Iteration budget reached (10/10) mid-task

### 6. External References
- Hermes Agent Quickstart — Ollama Docs
- OpenRouter API docs / cookbook
- GitHub: NousResearch/hermes-agent
- Flue Agent Harness Framework (compared)
- lahfir/agent-desktop (evaluated)
- OpenClaw comparison: "Hermes Agent might have just killed OpenClaw"
