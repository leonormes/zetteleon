---
title: PKM Agent Audit — 2026-06-29
created: 2026-06-29 00:00:00+01:00
modified: 2026-06-29 00:00:00+01:00
tags:
- audit
- agents
- pkm
- inbox
type: audit
status: awaiting-review
permalink: llmeon/00-inbox/pkm-agent-audit-2026-06-29
---

# PKM Agent Audit — 2026-06-29

Read-only audit of all LLM agents configured to interact with this vault, their actual behaviour, and why no benefit is visible. Every finding is tagged `[source: <path>]` or `[inference]`. No existing file has been modified.

---

## Inventory

| Agent | Config path(s) | chezmoi-managed? | Trigger & cadence | Declared job | Writes to | Last activity (evidence) |
|---|---|---|---|---|---|---|
| **Hermes Gateway** | `~/.hermes/config.yaml` | Yes — source `private_dot_hermes/private_config.yaml` | launchd `ai.hermes.gateway.plist` RunAtLoad + KeepAlive on non-successful exit | LLM agent gateway + cron scheduler | delegates to skills | Today 08:19 [source: `~/.hermes/logs/gateway.log`] |
| **Hermes cron — Pieces LTM Project Check-In** | `~/.hermes/cron/jobs.json` (id: `529a6cc9`) | No — runtime state | Every 240 min; 345 completed runs since 2026-04-28 | Detect new projects from Pieces → create `wiki/projects/` dossiers | `raw/`, `wiki/projects/`, `log.md` | 2026-06-28 18:18, status: ok [source: `jobs.json`] |
| **Hermes cron — CoS Work Review (×3)** | `~/.hermes/cron/jobs.json` (ids: `bd2dc75f`, `ae0a6676`, `828f1027`) | No — runtime state | 08:15, 10:00/12:00/14:00/16:00, 17:30 weekdays; 142 combined runs | Jira/GitLab state → SoT note + daily journal | `200_projects/ProdOS/SoT - Work Open Loops.md`, `01_journals/Dailies/YYYY-MM-DD.md` | Today 08:19, status: ok [source: `jobs.json`] |
| **1MCP proxy** | `~/.config/1mcp/mcp.json` | Yes — source same path | launchd `com.user.1mcp.plist` RunAtLoad + KeepAlive | Aggregate MCP servers (obsidian-mcp-tools, basic-memory, atlassian, memory, sequential-thinking) | None directly | Permanent daemon [source: `com.user.1mcp.plist`] |
| **Basic Memory** | `~/.config/basic-memory/config.json` (chezmoi) + `~/.basic-memory/config.json` (runtime) | Partial — see §2 | Passive file watcher; no launchd plist; starts with 1MCP via `uvx basic-memory mcp` | Sync vault files → SQLite for semantic search via MCP | Adds/updates `permalink:` frontmatter on sync | Active; last scan 08:47 today, 43 files synced, 0 errors [source: `~/.basic-memory/watch-status.json`] |
| **Claude Desktop** | `~/Library/Application Support/Claude/claude_desktop_config.json` | No | Manual sessions only | General assistant; routes all tools through 1MCP at `?app=claude-desktop` | Session-only, no vault writes | N/A — manual [source: `claude_desktop_config.json`] |
| **Gemini (gemini-scribe)** | `GEMINI.md` (vault root); `~/.gemini/settings.json` (not inspected — not in scope of running agents) | Unknown | Manual sessions only; no launchd, no cron | ProdOS Operator via MCP proxy on port 8000 | Would write to vault on demand | No evidence of recent use; config references `http://127.0.0.1:8000/mcp/` which is **stale** — 1MCP now runs on port 3050 [inference from port mismatch] |
| **Pieces OS** | `com.pieces.os.launch.plist` | No | launchd, persistent | Ambient capture + LTM; surfaces activity to Hermes via REST `http://localhost:39300/messages` | Pieces internal DB only | 11,791 assets; last capture ~2026-06-23T08:42 per Hermes log [source: `log.md`] |

**Not found at:** Basic Memory does not have a launchd plist; it runs as a child process of the 1MCP server. MCPHub (`com.user.mcphub.plist`) has `RunAtLoad: false` and `KeepAlive: false` — effectively disabled [source: `com.user.mcphub.plist`].

---

## Intended Behaviour vs Actual

### Hermes

**Instructed to do** (verbatim from `AGENTS.md` §4 and `jobs.json`):

- Operate exclusively in `raw/`, `wiki/`, `output/`. Never write to `00_Inbox/`, `20_Thinking/`, `30_Library/` [source: `AGENTS.md` §6].
- Ingest Pieces activity → create `raw/YYYY-MM-DD-pieces-<slug>.md` → upsert `wiki/` entity dossiers with inline citations → update `log.md` [source: `AGENTS.md` §4.1, `daily-synthesis/SKILL.md`].
- Query Jira via `gk` CLI → write `SoT - Work Open Loops.md` → append one-liner to daily journal [source: `jobs.json` prompt for CoS jobs].

**What it actually does:**

- Project Check-In: runs correctly per AGENTS.md schema. 139 `raw/` files created since April 2026. 15+ `wiki/projects/` dossiers maintained with verbatim Pieces citations and `pieces_id` backlinks [source: `raw/` ls, `wiki/projects/` ls, `log.md`].
- CoS Work Review: runs correctly. `SoT - Work Open Loops.md` is current as of today 08:18. Daily journal entries are appended on each run. Jira table and Top 3 Next Actions are well-formed [source: `SoT - Work Open Loops.md`, `01_journals/Dailies/2026-06-26.md`].
- Self-modification: gateway log shows repeated `Self-improvement review: Patched SKILL.md in skill 'pkm-obsidian'` and `cos-work-review` entries — Hermes is autonomously editing its own skill files [source: `gateway.log`]. This is not specified in any job prompt and is the mechanism behind the drifting skill definitions seen in git status.

**Overlaps and conflicts between agents:**

1. **Three competing schema documents with no mapping:**
   - `AGENTS.md` (vault root): raw/wiki/output three-layer, dossier/concept note types, Hermes-only.
   - `CLAUDE.md` (vault root): ProdOS HEAD/SoT/Atomic/Protocol/MoC types, different folder conventions.
   - `GEMINI.md` (vault root): same ProdOS vocabulary as CLAUDE.md but references stale MCP port 8000.
   - The user's stated ontology in this audit prompt (Claim/Concept/Practice/Source/Person/Question/Literature with typed links and steel-man structure) appears **nowhere** in any of these three documents. It is an intention that was never encoded [inference from full config read].

2. **Basic Memory config split:** Two config files with different `default_project` values: `~/.basic-memory/config.json` (runtime, updated today) has `"default_project": "main"` (→ `~/basic-memory`, not the vault); `~/.config/basic-memory/config.json` (chezmoi-managed) has `"default_project": "llmeon"` (→ the vault). The 1MCP server overrides this with `BASIC_MEMORY_MCP_PROJECT=llmeon` [source: `mcp.json`], so tool calls from Claude/agents correctly target the vault. But the runtime config is diverged from the chezmoi source, and no cron job prompt ever invokes a basic-memory tool — the index exists but nothing queries it [source: both config files, `jobs.json`].

3. **pkm profile is configured but no cron job uses it:** `~/.hermes/profiles/pkm.yaml` preloads `custom/pkm-obsidian` and `custom/mcp-integration` skills, constrains to vault directory, and sets model to `claude-sonnet-4-6`. None of the four active cron jobs specifies `"profile": "pkm"` — they all run on the default profile (`deepseek/deepseek-v4-flash`) [source: `jobs.json`, `pkm.yaml`]. The obsidian CLI tooling in `pkm-obsidian` skill is therefore never invoked by automation.

4. **No single source of truth for agent behaviour:** Instructions are distributed across `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `daily-synthesis/SKILL.md`, `cos-work-review/SKILL.md`, `pkm-obsidian/private_SKILL.md`, `pkm.yaml`, and the `jobs.json` prompts themselves. Several contradict each other (e.g. `CLAUDE.md` is silent on raw/wiki/output; `AGENTS.md` is silent on HEAD/SoT/Atomic).

---

## Vault State

### Agent-written vs hand-written signal

Git commits are uniformly `vault backup` with no author attribution — git history cannot distinguish agent from human [source: `git log --oneline -30`]. Signal used: **path convention** per AGENTS.md §8:

- **Agent-written:** `raw/`, `wiki/`, `output/`, `log.md`, CoS run entries in `01_journals/Dailies/`, `200_projects/ProdOS/SoT - Work Open Loops.md`.
- **Human-written:** `00_Inbox/`, `20_Thinking/`, `30_Library/`, remainder of `01_journals/`.

### Counts

| Location | Count | Written by |
|---|---|---|
| `raw/` | 139 files | Agent |
| `wiki/projects/` | 15+ dossiers | Agent |
| `wiki/concepts/` | 3 files | Agent |
| `wiki/people/` | README.md only | Agent (stub) |
| `wiki/infrastructure/` | directory (not sampled) | Agent |
| `log.md` | Active, last entry 2026-06-23 | Agent |
| `SoT - Work Open Loops.md` | 1 file, updated today | Agent |
| `30_Library/100_zettelkasten/` | 1,075 notes | Human |
| `20_Thinking/21_Workbench/` (HEAD notes) | 32 notes | Human |
| `01_journals/Dailies/` | Daily files, agent-appended | Hybrid |

### Conformance sample

**Against the user's stated ontology** (Claim/typed links/steel-man/falsifiers/crux/`[source]`·`[inference]` tags):

**(a) 15 most-recently-modified notes:** All six checked were daily journal files containing CoS run summaries (e.g. `Jira open: 6 | Stale: 1`). Zero conformance to stated ontology. The remaining recently-modified files are `SoT - Work Open Loops.md` (Jira table, not an epistemic commitment) and wiki dossiers. 0/15 conform [source: `ls -lt`, journal files].

**(b) Random 12 Library notes sampled:**

| Note | `type` field | Typed links | Claim structure |
|---|---|---|---|
| A Next Action Must Be… | absent | none | none |
| Achieving a Goal… | `concept` | none | none |
| SoT - State Synchronisation Models | none (SoT format) | none | none |
| The Failure of No-Code Elimination | `kind: claim` + `type: atom` (conflicting fields) | `upstream:` (non-standard) | evidence + implications, no steel-man/falsifiers |
| Broader Understanding Enhances… | `type: ''` (empty) | none | none |
| Extrinsic rewards less effective… | `type: permanent` | none | none |
| An API Gateway is… | `type: permanent` | none | none |
| MOC - The Gap Between Thought… | MoC format | none | none |
| Timeboxing Combats Least Resistance | none | none | none |
| Visual Schedules Help Children… | none | none | none |
| MOC - Assertiveness Through System Design | `type/moc` tag | none | none |
| Claim - Over-capture plus deferred review | `type: claim` ✓ | `related_to:` ✓ | counter-positions + crux ✓ — **no steel-man sentence, no falsifiers, no confidence, no `[source]`/`[inference]` body tags** |

Summary: 1/12 (8%) partially conforms — the single `type: claim` note has crux and counter-positions but is missing steel-man, falsifiers, and confidence position. 0/12 have `[source]`/`[inference]` body tags. Type field usage: 4 distinct conventions (`type: permanent`, `type: concept`, `kind: claim`, absent) across 12 notes.

**(c) All agent-written notes examined:** 0% conform to stated ontology. Agent output uses AGENTS.md schema (dossier/raw/output) throughout. Zero Claim stubs proposed for user review. Zero Question notes created by any agent.

**Typed links across full vault:** 62 notes contain at least one key from `{related_to, contrasts_with, supports}` in frontmatter [source: `grep -rl`]. All are human-written. `prerequisite_of` and `instance_of` were not found. The 62 notes are concentrated in recent zettelkasten additions (~2026) — older notes (pre-2026) are mostly linkless.

**Drift markers:**

- **Type field chaos:** At least five naming conventions coexist: `type: permanent`, `type: concept`, `type: claim`, `kind: claim`, `type: atom`, `prodos.kind`, and absent. No single convention covers even 30% of the 1,075 zettelkasten notes [inference from 12-note sample + grep].
- **Q notes:** One found (`Q — What Am I Actually Struggling With.md`). The stated ontology expects `Q — [title].md` naming — the schema exists but is almost unused [source: `find`].
- **Claim notes:** ~10 found via filename/frontmatter (`Claim -` prefix or `type: claim`). All human-written. None produced by any agent [source: `grep -rl`, `find`].
- **Broken links:** `broken-links` plugin installed in Obsidian but not queried programmatically in this audit. Not quantified.
- **Orphans:** Not quantified; `pkm-obsidian` skill has `obsidian orphans vault=LLMeon` available but no cron job invokes it.
- **Last raw/ file:** `2026-06-24-pieces-ftfl-464-calico-cloud-cleanup.md` — 5 days ago. Last wiki update: `Chezmoi.md` modified 2026-06-22. Agent write cadence has slowed [source: `ls raw/`].
- **Stale GEMINI.md:** References `http://127.0.0.1:8000/mcp/` — 1MCP now runs on port 3050. Any Gemini session would fail to reach MCP tools without manual correction [source: `GEMINI.md`, `mcp.json`].

---

## Diagnosis

**Hermes is running.** 345 Project Check-In completions and 142 CoS Work Review completions are evidence of sustained execution, not a broken trigger. The dominant failure mode is therefore not (a). It is a combination of three:

**Primary — (c) Non-conforming output:** Hermes is producing well-structured work in a schema (`AGENTS.md` dossier/raw/output) that is entirely orthogonal to the schema the user actually wants (Claim/typed-links/steel-man). The raw/ and wiki/ layers capture *what happened at work*; the stated ontology is designed to capture *what you believe and why*. These are different epistemological categories. The agent was never instructed to produce Claim stubs, Question notes, or anything requiring the user to take a falsifiable position. Because the output doesn't match the ontology, it never integrates with the 30_Library/ layer and generates no visible cognitive benefit. [Evidence: 0% of agent output has `type: claim`, 0 Claim stubs found in `raw/` or `wiki/`, user's ontology absent from every agent config file read.]

**Secondary — (f) Too generic:** Both active cron jobs are optimised for *status tracking* (Jira state, Pieces project detection), not *epistemic forcing*. The CoS Work Review is a functional work-management tool — it reduces toil around Jira — but produces no commitment the user must defend. The Project Check-In produces entity dossiers about things that happened; these are recognition-mode outputs (you recognise the summary as accurate) rather than generation-mode outputs (you are forced to state a position). This directly worsens the known failure mode of drifting toward recognition over generation. [Evidence: `SoT - Work Open Loops.md` is a Jira mirror; wiki dossiers contain factual summaries with Pieces citations; neither format contains a falsifiable claim.]

**Contributing — (d) Never surfaced:** Even the work-tracking output that is useful (CoS SoT, daily journal CoS runs) is only surfaced by opening specific files. There is no query, index, or dashboard that presents agent-proposed content for review at the natural moment of doing. The wiki/ tree exists in a folder the user rarely opens (it is excluded from human-territory per AGENTS.md §6). The basic-memory index is built but never queried by any agent or surfaced to the user. [Evidence: `00_Inbox/` contains no agent-generated review queue; no Dataview query for agent output found; `jobs.json` has no basic-memory tool calls.]

**Contributing — (e) Config sprawl:** Three schema documents (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`) define overlapping but divergent agent behaviours with no cross-referencing. Hermes is autonomously patching its own skill files (evidenced in gateway.log), which means the chezmoi source and live config are drifting — the skills in chezmoi (`dot_hermes_custom_skills/`) are marked as modified in `git status` and the mechanism is unclear. The pkm-obsidian skill (which has the `obsidian orphans`, backlinks, and unresolved-link tooling) is never invoked by automation. [Evidence: `git status`, `gateway.log` self-improvement entries, `jobs.json` showing no `profile: pkm` on any job.]

---

## Improvement Plan

**Principle:** Remove and consolidate before adding. Every action below is one concrete physical change to one specific file, ordered by impact. Nothing is added until the redundant layer is removed.

---

### Step 1 — Retire GEMINI.md from agent-instruction role (do first)

**Action:** Move `GEMINI.md` to `99_Archive/GEMINI-archived-2026-06-29.md`.

**Why:** It references a stale MCP port (8000 vs 3050), duplicates ProdOS vocabulary already in `CLAUDE.md`, and there is no evidence of a running Gemini agent. It is dead config creating maintenance surface. The `gemini-scribe/` directory can stay — it contains templates and RAG infrastructure that may still be referenced in manual sessions.

**Risk:** Low. Any future Gemini session would need GEMINI.md updated anyway due to the port mismatch.

---

### Step 2 — Add the missing ontology to AGENTS.md (highest leverage change)

**Action:** Open `AGENTS.md` and add a new §2.4 "Claim Stubs" and extend §4.1 "Ingest" with a Step 7.

**§2.4 — Claim Stub (new note type):**

```yaml
---
title: <one sentence claim>
type: claim-stub
status: proposed
created: <ISO 8601>
source_raw: [[raw/source-note]]
claim_statement: <single falsifiable sentence in first person>
steel_man: <strongest version of the opposing view>
falsifiers: <what evidence would make this wrong>
crux: <the single load-bearing assumption>
tags: [claim-stub, agent-proposed]
---
```

Stubs go to `raw/proposed-claims/YYYY-MM-DD-<slug>.md`. Hermes may **propose** stubs; it may **never** write or edit notes in `30_Library/` directly.

**§4.1 Ingest, Step 7 (new):**

> If the ingested source contains a position the user appears to be defending (a repeated assertion, a trade-off decision, a design choice), propose one Claim stub to `raw/proposed-claims/YYYY-MM-DD-<slug>.md`. Populate `claim_statement`, `source_raw`, and `steel_man` only. Leave `falsifiers`, `crux`, and `confidence` blank for the user to complete. Append a one-line flag to `log.md`: `Claim stub proposed: [[raw/proposed-claims/…]]`.

**Why this step specifically:** The source-digest/claim boundary is currently undefined in all agent configs. This is the single encoding that makes the boundary concrete. It does not require a new agent, a new cron job, or a new tool — it adds a behaviour to an existing run. The stub is minimal and explicitly incomplete, forcing the user to generate rather than recognise.

---

### Step 3 — Add one surfacing mechanism (Dataview query)

**Action:** Create `00_Inbox/Agent Review Queue.md` containing:

````markdown
---
title: Agent Review Queue
type: index
---

## Claim Stubs awaiting review

```dataview
TABLE file.mtime AS "Proposed", source_raw AS "Source", claim_statement AS "Statement"
FROM "raw/proposed-claims"
WHERE type = "claim-stub" AND status = "proposed"
SORT file.mtime DESC
```

## Recent wiki updates (last 7 days)

```dataview
TABLE file.mtime AS "Modified", wiki_type AS "Type"
FROM "wiki"
WHERE file.mtime >= date(today) - dur(7 days)
SORT file.mtime DESC
```
````

**Why:** Without a surfacing mechanism, output that doesn't enter a regular workflow generates no benefit. This single file, opened at the start of a thinking session, answers "what has the agent proposed since I last looked?" It requires Dataview (already installed [source: `.obsidian/plugins/dataview/`]).

---

### Step 4 — Fix Basic Memory config divergence

**Action:** Run `chezmoi diff dot_config/basic-memory/config.json` to verify the chezmoi source has `"default_project": "llmeon"`. If the live `~/.basic-memory/config.json` has drifted to `"main"`, run `chezmoi apply dot_config/basic-memory/config.json` to re-sync. Do not edit `~/.basic-memory/config.json` directly.

**Why:** Two configs with different defaults is confusing. The 1MCP env var (`BASIC_MEMORY_MCP_PROJECT=llmeon`) correctly overrides for agent use, but a direct `uvx basic-memory` CLI call would target the wrong project.

**Note:** Basic Memory's current value is passive — it indexes the vault but nothing calls it. Do not invest further in it until Step 2 is generating Claim stubs worth searching semantically.

---

### Step 5 — Consolidate CLAUDE.md and AGENTS.md (later)

**Action:** After Steps 1–4 are stable, merge `CLAUDE.md` into `AGENTS.md`: add a §0 "Note taxonomy" section that names the ProdOS types (HEAD, SoT, Atomic, MoC, Claim) with their locations and the constraint that Hermes touches only `raw/`, `wiki/`, `output/`, and `raw/proposed-claims/`. Then delete `CLAUDE.md`.

**Why this is deferred:** Steps 1–3 are the minimum viable change set. Merging the spec documents is consolidation that reduces maintenance burden but does not directly produce benefit. Do it once the new Claim stub workflow has been validated (i.e., one week after Step 2).

---

### What NOT to do

- Do not add a new agent, a new cron job, or a new MCP server. The existing infra is over-specified relative to the vault's current conformance state.
- Do not migrate the 1,075 zettelkasten notes to the stated ontology in bulk. The type field chaos is real but the cost of bulk migration is higher than the cost of forward-only adoption on new notes.
- Do not enable the pkm profile on cron jobs until the Claim stub workflow is validated — adding the obsidian CLI tooling to the cron context before the schema is stable will produce more self-modification churn.

---

## Single next physical action

**Open `AGENTS.md`, add §2.4 "Claim Stubs" and the Step 7 extension to §4.1 "Ingest."** This is one file edit, no new infrastructure, and it is the only change that directly encodes the source-digest/claim boundary — the missing mechanism between "Hermes ingests Pieces activity" and "I hold a position I can defend."

Everything else in the improvement plan depends on first having a defined stub format.

---

*Audit conducted: 2026-06-29. Read-only. No existing files modified. This file created as the sole output.*