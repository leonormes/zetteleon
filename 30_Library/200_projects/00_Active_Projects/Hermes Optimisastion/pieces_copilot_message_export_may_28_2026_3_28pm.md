*Shared Message from Pieces (https://pieces.app) by Leon Ormes (leonormes@gmail.com) on Thursday May 28, 2026 - 3:28 PM*
---
## LLMeon — Repo Summary

**LLMeon** is your personal **AI-augmented knowledge vault**, built inside Obsidian at `/Volumes/DAL/Zettelkasten/LLMeon`. It is also a **git repository** (tracked via chezmoi conventions). Its primary purpose is to serve as the long-term memory and knowledge synthesis layer for Hermes — your primary AI agent — via a structured three-layer agent architecture backed by Pieces LTM as the upstream data source.

---

### Three-layer architecture

| Layer | Path | Role |
|---|---|---|
| **Raw** | `raw/` | Append-only immutable source dumps — Pieces LTM extracts, meeting transcripts, articles, pastes. Never edited after creation. |
| **Wiki** | `wiki/` | Agent-compiled knowledge: entity dossiers (people, projects, orgs, concepts), each with cited claims tracing back to `raw/`. |
| **Output** | `output/` | Synthesised deliverables — reports, briefs, scripts, plans. Sourced from `wiki/` only, never from `raw/` directly. |

The golden rule running through all three: every claim must be traceable to its source. `wiki/` → `raw/`, `output/` → `wiki/` → `raw/`. This creates a verifiable knowledge chain.

---

### Key files and components

- **`AGENTS.md`** — the authoritative Hermes rulebook. Defines note type schemas, frontmatter templates, linking conventions, and four core workflows: **Ingest**, **Sweep**, **Dossier Management**, and output generation. Hermes must not write directly into the human-authored `00_Inbox`/`20_Thinking`/`30_Library` directories.
- **`log.md`** — append-only vault operation log. Every Hermes ingest, sweep, or dossier update is recorded here with timestamps, raw sources created, wiki pages touched, and Pieces IDs ingested. Runs on a cron schedule (4-hourly project check-ins, daily synthesis).
- **`wiki/index.md`** — entry point for the agent knowledge layer. Tracks four entity subdirectories: `concepts/`, `orgs/`, `people/`, `projects/` (currently the only active one, with 13 project dossiers).
- **`30_Library/`** — human-authored territory: atomic Zettelkasten notes (`100_zettelkasten/`), project documentation (`200_projects/`), operational runbooks (`ops/` — GitLab CI, ArgoCD, kubectl, deployment safety), and Sources of Truth (`SoT/` — agentic AI design patterns, skill architecture, ML engineering).

---

### What it actually tracks

From `log.md`, the active projects being automatically ingested and dossier-managed are:

- **Azure AKS Backup — FTFL** (incl. Terraform IaC modules, NNU/MKUH backup instances)
- **12 Million Patient Synthetic NHS-OMOP Pipeline**
- **Unified LLM Router Cockpit** (the Hermes cost-routing architecture you've been building)
- **Security and Maintenance Roadmap**
- **Future Roadmap Planning**

---

### Notable patterns

- **Pieces LTM is the upstream feed.** Hermes runs a cron job every 4 hours querying `ask_pieces_ltm`, creating raw notes, and updating wiki dossiers. This is what powers the daily synthesis skill you configured.
- **Strict separation of concerns.** Human PKM (`30_Library/`) and agent memory (`raw/`, `wiki/`, `output/`) are intentionally kept in separate directory trees. The bridge is explicit and gated.
- **Orphan/stale detection baked in.** The Sweep workflow flags wiki pages with no inbound links, broken wikilinks, uncited claims, and stale pages — vault hygiene is automated.
- **`AGENTS.md` extends `CLAUDE.md`.** The vault has a dual-governance model — CLAUDE.md (not read yet, likely in the root) sets base rules; AGENTS.md adds Hermes-specific overrides. Where they conflict, CLAUDE.md wins.

---

### Note on `/skill route-task`

That command was a Hermes CLI slash-command — it doesn't work inside Pieces Copilot. Within Hermes itself you'd invoke it as a skill trigger; here the routing logic is embedded in my system context from the `route-task.md` skill file you already have in chezmoi.