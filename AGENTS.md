---
created: 2026-04-28T00:00:00+00:00
modified: 2026-07-20T16:33:35+00:00
permalink: llmeon/agents
tags: [agents, hermes, system]
title: AGENTS
---

## AGENTS.md—Agent Rulebook

Authoritative schema for all agent interactions with this vault. Single source of truth; no external spec supersedes this file.

---

### 0. ProdOS Vault Taxonomy

Human-territory map. All agents must understand this structure to know what is off-limits and why.

#### Note Types

| Type | Location | Naming convention | Agent rule |
|------|----------|-------------------|-----------|
| HEAD | `20_Thinking/21_Workbench/` | `YYYY-MM-DD-HHmm-HEAD` | Read-only. Human-authored working memory; never write here. |
| SoT | `30_Library/SoT/` | `SoT - Title.md` | Read-only, except typed-edge lines / `axiom:` (see §9.3). Canonical knowledge updated by human via Chronos Synthesis. |
| Protocol | `30_Library/SoT/` | `Protocol - Title.md` | Read-only. Binary imperative procedures. |
| Atomic / Claim | `30_Library/100_zettelkasten/` | Full-sentence title; `Claim - Title.md`; `Q — Title.md` | Read-only, except typed-edge lines / `axiom:` (see §9.3). To propose a claim, write a stub to `raw/proposed-claims/` (§2.4)—never write directly into the zettelkasten. |
| MoC | `30_Library/MoC/` | `MOC - Title.md` | Read-only. Hub notes owned by human. |

#### Human-territory Folder Structure

```
00_Inbox/             ← capture entry point — read-only for agents
01_journals/          ← daily notes — CoS cron appends only, via explicit cron job prompt
10_System/            ← templates and prompts — read-only
20_Thinking/          ← HEAD notes — read-only
30_Library/           ← vetted knowledge base — read-only
  100_zettelkasten/   ← atomic, claim, and question notes
  200_projects/       ← project notes
  MoC/                ← maps of content
  ops/                ← operational references
  SoT/                ← source-of-truth and protocol documents
```

#### Frontmatter

Canonical spec: [[SoT - ProdOS Frontmatter Contract (Note Type Schemas)]]. New notes use `prodos.kind` and `prodos.lifecycle`. Do not add legacy keys (`type`, `status`, `updated`, `creation_date`) to new content.

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

#### 2.4 Claim Stubs

Proposed epistemic commitments surfaced by Hermes during Ingest, awaiting human completion. The agent proposes; the human owns.

- Naming: `raw/proposed-claims/YYYY-MM-DD-<slug>.md`
- Frontmatter:

  ```yaml
  ---
  title: <one-sentence falsifiable claim>
  type: claim-stub
  status: proposed
  created: <ISO 8601 with offset>
  source_raw: [[raw/source-note]]
  claim_statement: <single falsifiable sentence — the position being defended>
  steel_man: <strongest version of the opposing view, as Hermes understands it>
  tags: [claim-stub, agent-proposed]
  ---
  ```

- Body: one short paragraph of supporting context drawn verbatim or minimally paraphrased from the `source_raw` file. No synthesis. No inference beyond what the source directly supports. Tag any inferred statement `[inference]`; any quoted statement `[source: raw/filename]`.
- Fields left intentionally blank for the human to complete: `falsifiers`, `crux`, `confidence`, `counter_positions`.
- Rule: Hermes must not write to `30_Library/`—not even to create an atomic note. The stub goes to `raw/proposed-claims/` only. Promotion to `30_Library/` is a human action.

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
7. Propose a Claim stub if warranted—if the ingested source contains a position the user appears to be defending (a repeated assertion, a design decision, a trade-off with a clear winner), create one stub at `raw/proposed-claims/YYYY-MM-DD-<slug>.md` per §2.4. Populate `claim_statement`, `source_raw`, and `steel_man` only. Leave `falsifiers`, `crux`, `confidence`, and `counter_positions` blank. Append a flag line to the `log.md` entry: `- Claim stub proposed: [[raw/proposed-claims/…]]`. If no defensible position is evident, skip this step—do not fabricate a claim.

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
| Never write to `00_Inbox/`, or `20_Thinking/`. | Those are human ProdOS territory |
| Never write or edit Claim/SoT content in `30_Library/`—stubs only, to `raw/proposed-claims/`—except the §9.3 typed-edge/`axiom:` exception | The claim layer belongs to the human; agent crossing it erodes epistemic ownership. §9.3 is the one sanctioned, narrowly-scoped exception—no new claims, no proposition edits, no deletions under it |
| Every typed-edge or `axiom:` edit must leave `edge_lint.py` at 0 errors before being considered done | A report-only compiler is only trustworthy if the edges it reports on are kept valid (see §9.4) |
| Never edit a `raw/` file after creation — **except `raw/proposed-claims/`**, which is a working queue for stub completion | Immutability is the audit trail for ingested sources. Claim stubs (§2.4) are a working queue intentionally left incomplete for human action; their blank fields may be filled by the promoter |
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
├── raw/                    ← immutable ingested sources
│   └── proposed-claims/   ← claim stubs (§2.4) awaiting human review
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

### 9. Typed Edge / Justification Graph Workflow

Governs how agents interact with the vault's typed-edge system and argument-graph compiler. Canonical syntax: [[SoT - Typed Edge Vocabulary (Knowledge Graph Relations)]]. Canonical capabilities: [[SoT - Knowledge Compiler (Argument Graph Spec)]]. Applies to any task touching a claim, concept, or SoT note that participates in the justification graph—not to general vault work.

#### 9.1 Tool preference for vault I/O

In order:

1. Obsidian tools exposed via 1MCP (`http://127.0.0.1:3050/mcp?app=claude-code`), server `obsidian-mcp-tools`—called **directly by name**, e.g. `obsidian-mcp-tools_1mcp_<tool>`. There is no discovery step: 1MCP replaced the old `retrieve_tools`/`call_tool` proxy pattern in June 2026 and exposes every upstream tool under its own name, same as any native tool. Never reintroduce a `retrieve_tools`/`call_tool` two-step. If a tool seems unavailable, run `curl -s http://127.0.0.1:3050/health | jq .servers` before assuming it doesn't exist—don't fall back silently.
2. The `obsidian` CLI when the MCP path isn't reachable: `read`, `create`, `append`, `property:set`, `search:context`, `backlinks`, `unresolved`, `eval`. Verified working whenever the Obsidian desktop app is running.
3. Raw filesystem Read/Write only as a last resort, and never blind—`read` the file via one of the above first. A blind fs write bypasses Obsidian's `metadataCache`, so Dataview/backlinks/graph view can silently desync from disk until a reload.

`edge_lint.py`'s own full-vault batch scan is exempt from this—it reads files directly by design (`os.walk`), because a single-file-at-a-time CLI/MCP round trip does not scale to a whole-vault audit. This rule governs interactive single-note reads/writes, not the compiler's ingest step.

#### 9.2 Pre-task graph-state check

Mirrors §7's Pieces-context rule. Before adding or editing a typed edge, an `axiom:` marker, or any note that participates in the argument graph, run:

```
uv run --with pyyaml python3 10_System/scripts/edge_lint.py --audit
```

and, if working a specific claim, `--why "<title>"` and/or `--impact "<title>"` on it. State what the graph currently looks like before changing it—don't add a duplicate edge or an `axiom:` flag onto a claim that's already grounded.

#### 9.3 Write scope in `30_Library` (the sanctioned exception to §0 / §6)

Agents MAY write directly into `30_Library/100_zettelkasten/`, `30_Library/SoT/`, `30_Library/MoC/`, and `30_Library/200_Projects/` notes, but ONLY to:

- add, edit, or remove a `%%[relationship:: [[target]]]%%` typed-edge line,
- set the `axiom: true` frontmatter boolean,
- maintain [[SoT - Typed Edge Vocabulary (Knowledge Graph Relations)]] and [[SoT - Knowledge Compiler (Argument Graph Spec)]] themselves.

Agents MUST NOT, under this exception: edit a claim's `proposition` or body prose, delete or rename a claim note, or author a brand-new claim note directly—new claims still go through the stub path (§2.4). This exception exists because typed-edge/axiom bookkeeping is mechanical—recording a relationship the human already asserted in prose, not a judgement on the claim itself—and because without it, "help with the justification graph" cannot be fulfilled at all. Anything outside this narrow scope reverts to the general rule: propose, don't write.

#### 9.4 Mandatory validation gate

Before considering any typed-edge or `axiom:` edit complete:

```
uv run --with pyyaml python3 10_System/scripts/edge_lint.py --path "<file or vault root>"
```

must report `0 error(s)`. Do not report success with a residual ERROR. Fix warnings too where trivial (e.g. a note target written bare instead of as a wikilink)—they don't block completion, but leaving one is not "done."

#### 9.5 How to actually do the work

- One note's links/edges need fixing or expanding → [[Note Refresh & Link Auditor]].
- The whole graph needs auditing for gaps/foundations/conflicts, and gaps closed → [[Justification Graph Audit & Gap Closure]].

---

_This file is managed by the Hermes PKM workflow. Do not delete._
