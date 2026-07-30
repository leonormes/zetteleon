---
created: 2026-07-25 00:00:00+00:00
tags:
- agents
- gemini-cli
- system
title: GEMINI
permalink: llmeon/gemini-1
---

# Gemini CLI — Vault Entry Point

This file exists only because Gemini CLI auto-loads `GEMINI.md` hierarchically at session start (concatenated into every prompt); other agent tools auto-load `AGENTS.md` natively, and Claude Code auto-loads its own `CLAUDE.md`. **[[AGENTS.md]] is the single source of truth for agent behavior in this vault — read it in full before writing, editing, or deleting anything.** Nothing below this line supersedes it.

**2026-07-30:** Hermes's own raw/wiki/output memory system moved to a standalone vault (`/Volumes/DAL/Zettelkasten/Hermes`). This vault is now human ProdOS territory plus the narrow §9.3 typed-edge exception — nothing else.

Sections worth reading first:

- §0 — vault taxonomy: what's read-only, and why
- §6 — hard constraints: never violate without explicit instruction
- §9 — typed-edge / justification-graph workflow: read this before touching any claim, concept, or SoT note

If the task involves the typed-edge/justification-graph system specifically, also load the relevant workflow prompt from `10_System/prompts/`:

- One note's links/edges need fixing or expanding → [[Note Refresh & Link Auditor]]
- The whole graph needs auditing for gaps, and gaps closed → [[Justification Graph Audit & Gap Closure]]