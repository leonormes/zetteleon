---
created: 2026-04-06 17:20:35+00:00
modified: 2026-05-26 11:43:57+00:00
title: CLAUDE
permalink: llmeon/claude
---

## CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

### What This Repo Is

This is an Obsidian-based Personal Knowledge Management (PKM) vault—not a software project. There are no build, lint, or test commands. The primary "code" is in `gemini-scribe/`, which contains AI agent tooling and prompt infrastructure for working with vault content.

### User Context

Leon is a 52-year-old Software Engineer with ADHD. Interaction conventions:

- Micro-steps mandatory: Break tasks into the smallest physical actions; never say "set up X", say "create file X".
- British English: Use British spelling (colour, optimise, programme, etc.).
- Structure over prose: Use Markdown, hierarchies, and bullets. Avoid walls of text.
- Action bias: Theoretical explanations must end with a concrete next action.
- Depth over brevity: Explain the _why_ and the _principle_, not just the _how_.

### Vault Architecture (ProdOS)

The vault implements a two-state binary architecture:

#### Note Types

| Type | Location | Purpose | Voice |
|------|----------|---------|-------|
| HEAD | `20_Thinking/21_Workbench/` | Active thinking; volatile working memory | Human writes, LLM reads/refines only |
| SoT (Source of Truth) | `30_Library/SoT/` | Canonical, stable knowledge | Third-person, objective |
| Protocol | `30_Library/SoT/` | Repeatable procedures; imperative logic | `Protocol - Title.md` naming |
| Atomic | `30_Library/100_zettelkasten/` | Context-free declarative notes | Full-sentence titles |
| MoC | `30_Library/MoC/` | Maps of Content; topical hub notes | |

#### Folder Structure

- `00_Inbox/`—raw capture entry point
- `01_journals/`—daily notes
- `10_System/templates/`—Obsidian templates (Templater syntax)
- `10_System/prompts/`—reusable LLM context prompts (leon-context-*.md)
- `20_Thinking/21_Workbench/`—HEAD notes (ephemeral, one-problem lifespan)
- `30_Library/`—vetted knowledge base
  - `100_zettelkasten/`—atomic notes
  - `200_projects/`—project notes (Infrastructure, Dev, Maths, Personal)
  - `ops/`—operational command references
  - `SoT/`—source-of-truth and protocol documents
- `gemini-scribe/`—AI agent infrastructure (prompts, templates, RAG cache)

### Key Conventions

- Before creating new content, check `30_Library/SoT/` and `30_Library/ops/` for existing protocols or SoT notes on that topic.
- HEAD notes: Named `YYYY-MM-DD-HHmm-HEAD`. LLMs must NOT write substantive content here—only refine raw human input into structure.
- SoT notes: Updated via "Chronos Synthesis" (merging HEAD note insights). Key sections: `Working Knowledge`, `Current Understanding`, `Minimum Viable Understanding (MVU)`, `Tensions & Gaps`.
- Protocol notes: All steps must be binary (Done / Not Done). No ambiguity. Named `Protocol - Title.md`.
- Atomic notes: Use declarative, full-sentence titles that capture the core insight (e.g., _"A Goals-First Mentality Restricts Happiness"_).
- Frontmatter: Authoritative spec: [[Typed-Answer-Contract-RAG]]. For new and revised notes, use the top-level `prodos` object (`prodos.kind`, `prodos.lifecycle`, optional `prodos.trust`, `prodos.review`, and kind-specific extensions). Required top-level keys remain `title`, `created`, `modified`, `tags`; optional `aliases`; optional `see_also` / `supersedes` / `superseded_by` as per that SoT. Use ISO 8601 datetimes with offset for `created` / `modified`. Legacy keys (`type`, `status`, `trust-level`, `source_of_truth`, `updated`, `creation_date`, bare `last_reviewed` / `review_interval`) still appear in older notes; do not add them on new content—map semantics into `prodos` instead. Templates live in `10_System/templates/` (`HEAD_note template`, `Template - SoT`, `Template - Protocol`, `Template - Atomic Zettel`, `Template - MoC`). Adoption is forward-only until bulk migration.
- Machine validation (optional): JSON Schema `gemini-scribe/schemas/prodos-note-frontmatter.schema.json`; CUE `gemini-scribe/cue/prodos_frontmatter.cue`; vault scan `gemini-scribe/scripts/validate_note_frontmatter.py` (see `gemini-scribe/cue/README.md`).

### Gemini-scribe Agent Infrastructure

`gemini-scribe/` contains tooling for Gemini-based agents operating on this vault:

- `AGENTS.md`—vault overview for agent context
- `Prompts/`—agent prompt library
- `skills/`—agent skill definitions
- `Agent-Sessions/`—saved agent conversation sessions
- `rag-index-cache.json`—RAG index for vault content

The `GEMINI.md` (root) defines the ProdOS Operator role and MCP Proxy tool protocol for Gemini agents. These patterns apply equally to Claude: always prefer searching existing vault content over generating new content from scratch.