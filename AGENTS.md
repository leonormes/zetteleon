---
created: 2026-04-28T00:00:00+00:00
modified: 2026-05-26T11:43:57+00:00
tags: [agents, hermes, system]
title: AGENTS
---

## AGENTS.md—Hermes Vault Rulebook

Authoritative schema for all Hermes interactions with this vault.

This extends the ProdOS architecture defined in `CLAUDE.md`. Read that first.

When a rule here conflicts with `CLAUDE.md`, `CLAUDE.md` takes precedence.

---

### 1. Three-Layer Memory Architecture

Hermes operates exclusively within these three directories. Do not write directly

into the ProdOS folders (`00_Inbox`, `20_Thinking`, `30_Library`)—those are

human-authored territory. Bridge content into ProdOS only when explicitly instructed.

| Layer | Path | Purpose | Mutability |
|-------|------|---------|-----------|
| Raw | `raw/` | Immutable source material: transcripts, clipped articles, raw data dumps | Append-only. Never edit after ingest. |
| Wiki | `wiki/` | Structured agent-compiled knowledge: entity dossiers, concept pages, relationship maps | Updated by Hermes on each relevant ingest. |
| Output | `output/` | Final deliverables: reports, briefs, scripts, summaries generated from wiki | Created on demand; never used as a source. |

---

### 2. Note Types & Metadata

#### 2.1 Raw Notes

- Naming: `raw/YYYY-MM-DD-<slug>.md` (e.g. `raw/2026-04-28-meeting-product-sync.md`)
- Frontmatter required:

  ```yaml
  ---
  title: <descriptive title>
  created: <ISO 8601 with offset>
  source: <origin — "transcript", "article", "paste", "file">
  source_url: <URL if applicable>
  tags: [raw]
  ---
  ```

- Body: Verbatim or minimally cleaned source content. Add no commentary.
- Rule: After creation, the file is sealed. Hermes must not modify it.

#### 2.2 Wiki Pages

Two sub-types:

##### Dossier (Entity)

People, projects, organisations, tools.

- Naming: `wiki/<Type>/<Entity Name>.md` where Type is `people/`, `projects/`, `orgs/`, or `concepts/`
- Frontmatter:

  ```yaml
  ---
  title: <Entity Name>
  wiki_type: dossier
  entity_kind: person | project | org | concept
  created: <ISO 8601>
  modified: <ISO 8601>
  tags: [wiki, dossier]
  sources: [<list of raw/ filenames that support this page>]
  ---
  ```

- Mandatory sections:
  - `## Summary`—one-paragraph overview
  - `## Key Facts`—bulleted claims, each with an inline citation: `> "verbatim quote" — [[raw/source-note]]`
  - `## Connections`—`[[Wikilinks]]` to related dossiers and concept pages
  - `## Contradictions`—any claims that conflict across sources (flag, do not resolve)
  - `## Open Questions`—gaps Hermes cannot fill from existing raw material

##### Concept Page

Ideas, frameworks, processes, domain knowledge.

- Naming: `wiki/concepts/<Concept Name>.md`
- Same frontmatter structure as Dossier but `entity_kind: concept`.

#### 2.3 Output Documents

- Naming: `output/YYYY-MM-DD-<type>-<slug>.md`
  Types: `report`, `brief`, `script`, `summary`, `plan`
- Frontmatter:

  ```yaml
  ---
  title: <document title>
  output_type: report | brief | script | summary | plan
  created: <ISO 8601>
  wiki_sources: [<list of wiki/ pages used>]
  tags: [output]
  ---
  ```

- Outputs are synthesised from wiki pages only—never written from raw alone.

---

### 3. Linking Conventions

- All cross-references use `[[Wikilinks]]`—Obsidian-compatible, always relative.
- Every claim in a wiki page must trace back to at least one `raw/` source via `[[Wikilinks]]`.
- Use `[[wiki/people/Jane Doe]]` style paths in links to prevent ambiguity.
- Orphan wiki pages (no inbound or outbound links) should be flagged during Sweep.

---

### 4. Core Workflows

#### 4.1 Ingest

Trigger: User drops a file or text into `raw/`, or instructs Hermes to ingest a URL/paste.

Steps (execute in order):

1. Create raw note—write verbatim content to `raw/YYYY-MM-DD-<slug>.md` with correct frontmatter.
2. Identify entities—scan raw content for: people, projects, organisations, concepts.
3. For each entity:
   - If a wiki page already exists: open it, add new facts as bulleted claims with the raw source citation, and update `modified` timestamp.
   - If no wiki page exists: create one from the appropriate template (§2.2).
4. Check for contradictions—compare new facts against existing `## Key Facts`. If a conflict is found, add it to `## Contradictions` on the wiki page. Do not silently overwrite existing facts.
5. Update `index.md`—add or update the one-line entry for each touched wiki page.
6. Append to `log.md`—record the ingest event (§5 format).

#### 4.2 Sweep

Trigger: User instructs Hermes to run a vault health check (periodic or on demand).

Steps:

1. Orphan detection—find all `wiki/` pages with no inbound `[[links]]`. List them.
2. Stale detection—find wiki pages whose `modified` date is more than 90 days old and have no `## Open Questions`. Flag for review.
3. Broken links—scan all `[[Wikilinks]]` across `wiki/` and `output/`. List any that point to non-existent files.
4. Uncited claims—scan `## Key Facts` sections for bullet points that lack a `[[raw/…]]` citation.
5. Missing `index.md` entries—compare `wiki//*.md` against `index.md`. List missing.
6. Report—write a dated sweep report to `output/YYYY-MM-DD-report-sweep.md` and append a summary line to `log.md`.

#### 4.3 Dossier Management

Trigger: User asks about a person or project, or Ingest identifies a new entity.

Rules:

- All claims must be traceable to `raw/` sources via direct quotes. No speculative synthesis.
- If two sources contradict (e.g. different job titles for a person), preserve both in `## Contradictions` with citations.
- Dossiers for projects must include a `## Timeline` section with dated milestones sourced from raw notes.
- Hermes must not merge or delete a dossier without explicit user instruction.

---

### 5. `log.md` Entry Format

Append one entry per operation. Never edit past entries.

```
## YYYY-MM-DD HH:MM — <operation>

- Action: Ingest | Sweep | Dossier-update | Output-created
- Raw source: [[raw/filename]] (if applicable)
- Wiki pages touched: [[wiki/…]], [[wiki/…]]
- Flags: <any contradictions or orphans found, or "none">
```

---

### 5b. Daily Synthesis Workflow (Pieces LTM Integration)

Hermes uses the `daily-synthesis` skill (`~/.hermes/skills/daily-synthesis/SKILL.md`)

to ingest activity from Pieces LTM as the primary sensory input for this vault.

The pipeline runs in three phases:

| Phase | Action |
|-------|--------|
| Capture | Query Pieces LTM MCP (`mcp_pieces_*` tools) for today's snippets, screenshots, clipboard, and terminal activity |
| Distil | Write grouped source material to `raw/YYYY-MM-DD-pieces-<slug>.md` with `pieces_ids` in frontmatter |
| Compound | Upsert wiki entity pages, citing each claim with both the `raw/` backlink AND the specific Pieces memory ID |

Pieces backlink format (mandatory in all wiki claims sourced from Pieces):

```
> "verbatim excerpt" — [[raw/YYYY-MM-DD-pieces-slug]] (Pieces: <pieces_id>)
```

---

### 6. Hard Constraints

| Rule | Reason |
|------|--------|
| Never write to `00_Inbox/`, `20_Thinking/`, or `30_Library/` | Those are human ProdOS territory |
| Never edit a `raw/` file after creation | Immutability is the audit trail |
| Every wiki claim needs a `raw/` citation | Prevents hallucination compounding |
| Contradictions must be surfaced, not resolved | Resolution requires human judgement |
| `log.md` is append-only | Operational audit trail |
| Use `OBSIDIAN_VAULT_PATH` from `.env` for all file paths | Portability |
| Query Pieces LTM before starting any new task | Real-time context may modify requirements |

---

### 7. Pre-Task Context Rule (MANDATORY)

> Before starting any new task, Hermes must first query Pieces LTM to verify if
> there is any real-time context (current files open, recent searches, or terminal
> commands) that modifies the task requirements.

Procedure:

1. Use available `mcp_pieces_*` tools to retrieve recent activity (last 30 minutes
   or since last interaction).
2. Scan for: currently open files, active terminal working directories, recent
   clipboard contents, and any Pieces annotations tagged as "in-progress".
3. If relevant context is found:
   - Adjust the task scope accordingly.
   - State explicitly what Pieces context influenced the approach.
   - Cite the `pieces_id` in the session response.
4. If no relevant context is found: proceed with the original task.
5. This step must be logged if it modifies the task—append a `## Context-Override`
   subsection to the relevant `log.md` entry.

Skip condition: If Pieces MCP is unavailable, log the skip with reason and proceed.

---

### 8. Vault Path Reference

The vault root is resolved from `$OBSIDIAN_VAULT_PATH` (set in `~/.hermes/.env`).

```
$OBSIDIAN_VAULT_PATH/
├── raw/          ← immutable ingested sources
├── wiki/
│   ├── people/   ← person dossiers
│   ├── projects/ ← project dossiers
│   ├── orgs/     ← organisation dossiers
│   └── concepts/ ← concept pages
├── output/       ← final deliverables
├── AGENTS.md     ← this file
├── index.md      ← one-line catalog of all wiki pages
└── log.md        ← chronological operation history
```

---

_This file is managed by the Hermes PKM workflow. Do not delete._
