---
created: 2026-05-28T18:05:42+00:00
modified: 2026-07-20T16:32:59+00:00
permalink: llmeon/raw/2026-05-28-pieces-llmeon-repo-summary
pieces_ids: [48c402f1-3561-426c-bcb9-110e8aeb514c, 90e86161-028b-4ece-a7a2-a16b1f3f7366, dcdee514-a007-46a7-a6e9-3a8c66439711]
source: pieces-ltm
tags: [pieces, raw]
title: 2026-05-28-pieces-llmeon-repo-summary
---

## Asset 1 (Pieces: dcdee514-a007-46a7-a6e9-3a8c66439711)

Captured: 2026-05-28T14:21:47.299698Z

## LLMeon—Repo Summary

LLMeon is your personal AI-augmented knowledge vault, built inside Obsidian at `/Volumes/DAL/Zettelkasten/LLMeon`. It is also a git repository (tracked via chezmoi conventions). Its primary purpose is to serve as the long-term memory and knowledge synthesis layer for Hermes—your primary AI agent—via a structured three-layer agent architecture backed by Pieces LTM as the upstream data source.

---

### Three-layer Architecture

| Layer | Path | Role |
|---|---|---|
| Raw | `raw/` | Append-only immutable source dumps—Pieces LTM extracts, meeting transcripts, articles, pastes. Never edited after creation. |
| Wiki | `wiki/` | Agent-compiled knowledge: entity dossiers (people, projects, orgs, concepts), each with cited claims tracing back to `raw/`. |
| Output | `output/` | Synthesised deliverables—reports, briefs, scripts, plans. Sourced from `wiki/` only, never from `raw/` directly. |

The golden rule running through all three: every claim must be traceable to its source. `wiki/` → `raw/`, `output/` → `wiki/` → `raw/`. This creates a verifiable knowledge chain.

---

### Key Files and Components

- `AGENTS.md`—the authoritative Hermes rulebook. Defines note type schemas, frontmatter templates, linking conventions, and four core workflows: Ingest, Sweep, Dossier Management, and output generation. Hermes must not write directly into the human-authored `00_Inbox`/`20_Thinking`/`30_Library` directories.
- `log.md`—append-only vault operation log. Every Hermes ingest, sweep, or dossier update is recorded here with timestamps, raw sources created, wiki pages touched, and Pieces IDs ingested. Runs on a cron schedule (4-hourly project check-ins, daily synthesis).
- `wiki/index.md`—entry point for the agent knowledge layer. Tracks four entity subdirectories: `concepts/`, `orgs/`, `people/`, `projects/` (currently the only active one, with 13 project dossiers).
- `30_Library/`—human-authored territory: atomic Zettelkasten notes (`100_zettelkasten/`), project documentation (`200_projects/`), operational runbooks (`ops/`—GitLab CI, ArgoCD, kubectl, deployment safety), and Sources of Truth (`SoT/`—agentic AI design patterns, skill architecture, ML engineering).

---

### What it Actually Tracks

From `log.md`, the active projects being automatically ingested and dossier-managed are:

- Azure AKS Backup—FTFL (incl. Terraform IaC modules, NNU/MKUH backup instances)
- 12 Million Patient Synthetic NHS-OMOP Pipeline
- Unified LLM Router Cockpit (the Hermes cost-routing architecture you've been building)
- Security and Maintenance Roadmap
- Future Roadmap Planning

---

### Notable Patterns

- Pieces LTM is the upstream feed. Hermes runs a cron job every 4 hours querying `ask_pieces_ltm`, creating raw notes, and updating wiki dossiers. This is what powers the daily synthesis skill you configured.
- Strict separation of concerns. Human PKM (`30_Library/`) and agent memory (`raw/`, `wiki/`, `output/`) are intentionally kept in separate directory trees. The bridge is explicit and gated.
- Orphan/stale detection baked in. The Sweep workflow flags wiki pages with no inbound links, broken wikilinks, uncited claims, and stale pages—vault hygiene is automated.
- `AGENTS.md` extends `CLAUDE.md`. The vault has a dual-governance model—CLAUDE.md (not read yet, likely in the root) sets base rules; AGENTS.md adds Hermes-specific overrides. Where they conflict, CLAUDE.md wins.

---

### Note on `/skill route-task`

That command was a Hermes CLI slash-command—it doesn't work inside Pieces Copilot. Within Hermes itself you'd invoke it as a skill trigger; here the routing logic is embedded in my system context from the `route-task.md` skill file you already have in chezmoi.

## Asset 2 (Pieces: 48c402f1-3561-426c-bcb9-110e8aeb514c)

Captured: 2026-05-28T14:21:11.315588Z

The evaluator wants me to synthesize from the files I've read and deliver the summary. Let me do that now based on what I've read from:

1. `/Volumes/DAL/Zettelkasten/LLMeon/output/README.md` - Three-layer agent architecture (raw/wiki/output), deliverable types
2. `/Volumes/DAL/Zettelkasten/LLMeon/wiki/index.md` - Wiki layer details, entity types (concepts, orgs, people, projects)
3. `/Volumes/DAL/Zettelkasten/LLMeon/log.md` - Operation log showing ingests from Pieces LTM, project types (NHS OMOP, Azure AKS Backup, LLM Router Cockpit, etc.)
4. `/Volumes/DAL/Zettelkasten/LLMeon/AGENTS.md` - The Hermes agent rulebook covering the three-layer memory system, note types, and core workflows like ingestion, sweeping, and dossier management with its logging format

From the earlier memory and LTM searches, I can see this Obsidian vault at `/Volumes/DAL/Zettelkasten/LLMeon` is orchestrated by the Hermes agent, tracking work across FITFILE projects, NHS infrastructure, Kubernetes backups, and LLM orchestration with daily synthesis jobs pulling from Pieces LTM.

The vault also contains a 30_Library folder with human-authored zettelkasten notes, project documentation, sources of truth, and operational runbooks, plus graphify integration for knowledge graph visualization and 13 active project dossiers. I realize the `/skill route-task` command was a Hermes CLI thing, not available in this Pieces copilot context, so I'm ready to synthesize the full repository summary now.

## Asset 3 (Pieces: 90e86161-028b-4ece-a7a2-a16b1f3f7366)

Captured: 2026-05-28T14:20:42.294455Z

The reviewer wants me to read actual file contents. From the search results, I can see:

1. `/Volumes/DAL/Zettelkasten/LLMeon/output/README.md` - exists
2. `/Volumes/DAL/Zettelkasten/LLMeon/wiki/index.md` - exists
3. `/Volumes/DAL/Zettelkasten/LLMeon/wiki/log.md` - exists
4. `/Volumes/DAL/Zettelkasten/LLMeon/log.md` - exists (24076 bytes)

Let me also search for key top-level files like AGENTS.md, index.md, etc.

Now I need to pull the actual content from the README and wiki/index.md to see what's in there.
