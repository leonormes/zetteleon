---
conformant: true
created: 2026-07-16T00:00:00+00:00
description: "The canonical routing index for 10_System/prompts. Read this note first to decide which prompt to inject for a given task — defines the taxonomy, the routing table, and which prompts are historical task-logs rather than reusable prompts."
modified: 2026-11-17T10:12:44+00:00
permalink: llmeon/10-system/prompts/00-prompt-library-router
tags: [domain/pkm, moc, type/index]
title: 00 - Prompt Library Router
type: prompt
---

## Purpose

This note is the decision layer for the ProdOS Chief of Staff LLM. Every prompt in `10_System/prompts/` now carries a consistent `type/<category>` tag and a one-sentence `description` written for machine routing. Use this note to pick the right prompt; use [[LLM Prompts]] (the base) to browse by category.

> Cross-cutting requirement—Output Contract: every `type/system`, `type/protocol`, and `type/context`-driving-analysis prompt in this library is governed by [[Protocol - Typed Answer Contract (TAC) for Vault Agents]]: state confidence, cite evidence via `[[wikilink]]`, and flag insufficient context explicitly instead of guessing. This applies regardless of which prompt below you route to—it is not itself a routing choice.
>
> Cross-cutting requirement—Run Budget: every `type/system` and `type/protocol` run is bounded. Unless the prompt sets a tighter cap, stop and report as soon as any of these holds: the run has edited 10 notes; the same validator gate (`check_all.py`, `validate_note_frontmatter.py`, `validate_note_shape.py` or `edge_lint.py`) has failed 3 retries in a row on one note without the error count falling; or the same fix has been tried twice. The report names the note, the gate, the remaining errors and what was tried, then waits for Leon. A lower cap in the prompt itself, such as the 10 notes a day in [[Goal - Orphan Triage Sweep (Daily Cron)]], always wins.
>
> Cross-cutting requirement—K-Plex & Typed-Edge Architecture: every prompt that creates, edits, merges, or analyses notes operates on **K-Plex** by default alongside [[SoT - Typed Edge Vocabulary (Knowledge Graph Relations)]]:
> - **Idea Compass & 7-Predicate Typed Edges (`inferAllLinksAsFriends: false`):** Plain `[[wikilinks]]` are invisible in K-Plex. Pair meaningful relationships with a standalone `[<relationship>:: [[<target>]]]` line (`depends_on`, `extends`, `implements` → North; `synthesizes` → South from hubs only; `supports` → West; `contradicts` → East; `revises` → Sequence) or a mapped frontmatter property (`upstream`, `source`, `sources`, `entry_points`, `candidate_answers`, `supports_claims`, `evidence_links`, `distinguishes_from`, `tension`, `supersedes`, `superseded_by`, `merged_from`). Under `frontmatter-overrides-body-ontology`, never duplicate an inline typed-edge target in frontmatter `see_also`.
> - **K-Plex Views & Section Expansion:** Built-in views are Compass (`classic`), Mind Map (`mindmap`), and Facets (`wuxing`, with `LLMeon` presets `prodos-types` concentric by `type` and `prodos-status` horizontal by `status`). Long hubs (`sot`, `map`, `project`) expand by `##` headings in Compass and Mind Map—place inline edges under the specific `##` heading where the target belongs.
> - **Runtime Inspection (`window.kplexApi.v1`):** Inspect K-Plex neighbours, precedence evidence (`evidence({sourceId, targetId})`), ontology postings (`ontologyDocuments`, `inspectOntologyOccurrences`), and Mind Map exports via `obsidian vault="LLMeon" eval` using `.agents/skills/kplex-obsidian-cli/SKILL.md`.
## Taxonomy

| Category | Definition | Use it when… | Base view |
|---|---|---|---|
| `type/persona` | An identity/character the LLM adopts for the whole conversation. No fixed multi-phase algorithm. | You want an ongoing conversational partner (a coach, an architect mindset, an accountability loop). | Personas |
| `type/context` | Background/reference facts injected as system context. Not a task—no output format. | You want the LLM to _know_ something about Leon, a project, or a methodology before doing other work. | Contexts |
| `type/system` | A multi-phase autonomous agent workflow, usually operating over the vault via MCP tools, with defined phases and structured output. | The task requires search → classify → act across many notes. | Systems |
| `type/protocol` | A strict, imperative, repeatable procedure—minimal "why", built for recurring/cron execution. | A routine that should run the same way every time (e.g. a daily sweep). | Protocols |
| `type/utility` | A single-shot, input→output micro-task template. | You have one concrete artefact to transform (a diff, a CV, a ticket). | Utilities |
| `type/index` | This note: the routing index itself. Not a prompt to inject. | Deciding which prompt to use. | (n/a) |
| `type/task-log` | A one-off, dated, project-specific task that happened to be captured as a prompt. Not designed for reuse. | Never select these for a new task—they're historical record only. Read them only if reconstructing what was done. | (new—add to base) |

## Routing Table

### Vault / PKM Maintenance ("do Something to My Notes")

| Task | Prompt | Why |
|---|---|---|
| I have new vault content and don't know what to do with it | [[Prompt - Vault Ingest Router]] | Front door—runs locate→classify→test→route before any downstream prompt. Decides the route only: it does not merge, author or file, and stages new content through the atomic-capture pipeline in `00_Inbox/` |
| I pasted raw source text/notes and want atomic knowledge units extracted | [[Atomic Signal Extractor → Write TMP file]] | Step 1 of the atomic-capture pipeline |
| I have a tmp_atoms file ready to link into the vault | [[Atomic Linker → Promote & Connect]] | Step 2—always run after step 1 |
| I have a NEW note and need to find where it belongs | [[Knowledge Consolidation Agent]] | Discovery-first merge/dedupe |
| I have an established SoT/MOC and want scattered fragments folded into it | [[Knowledge Harvesting & Normalization Agent]] | Inverse of Consolidation Agent |
| I already know which notes to merge—just do it | [[sys_merger]] | Fast merge, no discovery phase |
| I want ONE note's links checked/expanded | [[Note Refresh & Link Auditor]] | Single-target deep refresh |
| I have a bare/orphan note with few or no links and want it positioned in the graph, then stress-tested | [[Orphan Note Positioning & Thread Audit]] | Single-note composition of the bootstrap→hygiene→epistemics pipeline below—discovers connections, applies typed edges/links/frontmatter, then thread-audits the note, all in one unattended run |
| I want a whole domain cluster surveyed for the first time—canonical candidates, duplicates, conflicts | [[LLM Graph Bootstrap Agent]] | Discovery/proposal only; writes report + stubs, never canonical notes. Run before the two graph prompts below |
| I want the whole justification graph audited for unsupported claims/foundations/conflicts, and gaps closed | [[Justification Graph Audit & Gap Closure]] | Runs `edge_lint.py --audit`; closes C1 gaps via edges or `axiom:` markers |
| I have a pile of unread/unprocessed notes to organise into MOCs | [[Principal Vault Triage Architect]] | Macro triage + navigation, not deep analysis |
| I want to know what I'm actually thinking about across the Zettelkasten | [[Zettelkasten Thinking-Pattern Analyst]] | Thematic/psychological analysis of the note graph |
| I want a new Map of Content built for a domain | [[Prompt - ProdOS MoC Cartographer]] | Builds annotated MOCs |
| I want a messy HEAD/working note turned into a stable SoT | [[Prompt - ProdOS Chronos Synthesizer]] | HEAD → SoT + Next Test |
| I want loose instructions turned into a strict Protocol note | [[Prompt - ProdOS Protocol Architect]] | Binary, imperative protocol output |
| My thinking workbench has filled up with clippings and finished documents | [[Protocol - Workbench Compliance Sweep]] | Runs the four HEAD-note tests over `20_Thinking/`, routes failures out, reports stale threads |
| Open problems are buried in `## Tensions` sections inside canonical notes where I never see them | [[Prompt - Tension Harvester]] | Harvests tensions into clustered HEAD notes, leaves a `> Open threads:` pointer in the source. Inverse of Chronos |
| Daily automated orphan cleanup | [[Goal - Orphan Triage Sweep (Daily Cron)]] | Recurring protocol, 10 notes/day |
| DevOps work log → reusable Atomic Command/Playbook | [[prompt - DevOps Knowledge Architect]] | Dedupes against existing commands first |
| I need the output-discipline rules every vault agent must follow (confidence, evidence, uncertainty flag) | [[Protocol - Typed Answer Contract (TAC) for Vault Agents]] | Cross-cutting contract, not a task-specific prompt—reference it, don't replace another prompt with it |
| An agent's output was wrong, unsafe, incomplete, or non-conformant and I need to fix the actual cause, not just the symptom | [[Protocol - Diagnose an Agent Failure]] | Cross-cutting protocol, not a task-specific prompt—classifies the root cause (retrieval/knowledge/routing/reasoning/TAC/permission/tool/ambiguity) before proposing a fix, and pairs every fix with a regression case in `10_System/evals/` |
| I want the atomic-note folder audited against the Allosso note-making rules (source layer, connectivity, keywords, review) and told which clusters are ready to write from | [[Prompt - Zettelkasten Audit (Allosso Rubric)]] | Read-only scorecard plus ranked findings and output-ready clusters. Health check on how you make notes, not on what you think ([[Zettelkasten Thinking-Pattern Analyst]]) or on argument soundness ([[Justification Graph Audit & Gap Closure]]) |
| I am working the Vault Graph programme one task per session (Todoist project Vault Graph) | [[Prompt - Vault Graph Programme (Session Driver)]] | Session driver: resume, confirm one task, execute, lint, log. Not for one-off note work |
| I have a new archery capture to fold into the 10-step shot process notes | [[Archery Shot Process - Knowledge Consolidation]] | Domain-specific Consolidation Agent; keeps contradictions as alternative views |
| I have a new family-chores capture to fold into the chores SoTs and plan | [[Family Chores - Knowledge Consolidation]] | Domain-specific Consolidation Agent; proposes full-note updates for you to apply |
| I pasted content about how we know things (knowledge, truth, evidence, science, belief) and want it folded into the epistemology graph | [[Epistemology Graph - Knowledge Consolidation]] | Domain-specific Consolidation Agent; reads the hub MoC and six SoTs, enhances existing notes or adds atomic notes with claim and counter-claim edges, reports gaps |
| I want the family and relationships notes triaged into their four buckets | [[Family Notes - Triage and Normalization]] | Domain-specific composition of Triage Architect, Consolidation Agent and Link Auditor |

### Capture / Triage

| Task | Prompt | Why |
|---|---|---|
| `"triage inbox"` / `"process 00_Inbox"` — process `00_Inbox/` items one-by-one into Projects (checkbox tasks), Problems, or the flat Todoist runway | [[Protocol - Action-First GTD (LLM Chief of Staff)]] | Interactive 7-type triage decision matrix enforcing Obsidian/Todoist control-plane separation, Todoist Bridge routing (`#todoist` checkboxes in `30_Library/200_Projects/`), and single-starter-verb Todoist pushes |

### Daily Execution (Todoist)

| Task | Prompt | Why |
|---|---|---|
| I want today planned: runway tasks timeboxed as dated, timed Todoist tasks (`/daily-plan`) | [[Protocol - Daily Plan (Todoist Timeboxing)]] | Reads Todoist, sets date, time and duration with Big Rocks first and a 25% buffer. Proposes the week's Big Rocks on Monday ([[Protocol - Big Rocks (Weekly Quadrant II Outcomes)]]). Draft and untested; shutdown clears the dates the CoS set |
| I have a planned block or task and need to start executing without overwhelm (`/engage-action`) | [[Protocol - Engage Action (Prosthetic Timebox & Somatic Switch)]] | Prosthetic timebox and somatic switch loop following `/daily-plan` macro blocking: picks one micro-starter, runs a bounded focus sprint, and handles friction/re-entry |

### Personal Context to Inject alongside other Prompts

| Context needed | Prompt |
|---|---|
| ADHD/communication style, "Chief of Staff" framing | [[leon-context-core-profile]] |
| Cloud/architecture expertise level | [[leon-context-cloud-architect]] |
| Dev environment (macOS/zsh/Neovim/chezmoi) | [[leon-context-dev-environment]] |
| Health/training profile | [[leon-context-health-profile]] |
| PKM/ProdOS philosophy (atomic notes, epistemics) | [[leon-context-pkm-philosophy]] |
| prodOS project vision | [[leon-context-project-prodos]] |
| Evaluating a new LLM tool/technique clip against actual stack, cost tiers, and goals | [[leon-context-llm-tool-evaluation]] |
| GTD methodology background | [[LLM GTD Context]] |
| FITFILE platform architecture (ArgoCD/Helm) | [[FITFILE Platform—ArgoCD + Helm Deployment Wiki]] |

### Conversational Personas

| Need | Prompt |
|---|---|
| Convergent partner to fight analysis-paralysis (A-C-T loop) | [[Thoughtful Action Partner]] |
| Data-structure-first coding philosophy for a whole session | [[Prompt - Data-Centric Coding Assistant]] |

### One-shot Utilities

| Task | Prompt |
|---|---|
| Write a commit message from a git diff | `git commit prompt` (note not yet written) |
| Generate a Jira ticket JSON payload | `jira_ticket_prompt` (note not yet written) |
| Refine my CV for a UK infra role | [[CV Refinement Prompt]] |
| Merge specific notes I've already picked | [[sys_merger]] |

### Recovering Dropped Context

| Task | Prompt |
|---|---|
| Recover open loops from Pieces LTM after context-switching | [[Optimised GTD Context Auditor for Pieces LTM]] |

## Prompt Pairs & Pipelines (Avoid pIcking the wRong hAlf)

- Atomic-capture pipeline (sequential): [[Atomic Signal Extractor → Write TMP file]] → [[Atomic Linker → Promote & Connect]]. Never run step 2 without step 1's output.
- Consolidation vs Harvesting (inverse pair): [[Knowledge Consolidation Agent]] starts from a _new note_ and finds its home. [[Knowledge Harvesting & Normalization Agent]] starts from an _established home_ and hunts fragments. Pick based on which end you're holding.
- Graph bootstrap → hygiene → epistemics (three-stage pipeline): [[LLM Graph Bootstrap Agent]] surveys an unmapped domain cluster and _proposes_ canonical candidates, duplicates, conflicts, and edges—it writes a report and stubs, never canonical notes. Then [[Note Refresh & Link Auditor]] makes individual notes edge-conformant, and [[Justification Graph Audit & Gap Closure]] audits the resulting graph. Running Gap Closure on a cluster that was never bootstrapped will report a near-empty graph and look like there's nothing wrong.
- Same pipeline, one note: [[Orphan Note Positioning & Thread Audit]] is the above three-stage pipeline collapsed onto a single bare note instead of a whole cluster—discover/propose connections, apply the typed edges, then audit in one run. Use the three-stage version for a cluster; use this one when you're holding a single orphan.
- Link hygiene vs. graph epistemics (sequential pair): [[Note Refresh & Link Auditor]] makes ONE note's links/edges conformant to syntax (does it parse, do targets resolve). [[Justification Graph Audit & Gap Closure]] then audits the whole argument graph those edges form for semantic soundness (is it actually grounded, or just syntactically valid). Run the Auditor first if a claim isn't edge-conformant yet—the Gap Closure prompt's `--audit` will otherwise miss it.
- Chronos vs Tension Harvester (inverse pair, same axis): [[Prompt - ProdOS Chronos Synthesizer]] runs workbench → canon—a resolved HEAD note becomes an SoT. [[Prompt - Tension Harvester]] runs canon → workbench—an unresolved tension buried in an SoT becomes a HEAD note. Pick by which direction the thinking has moved. Both are governed by [[SoT - HEAD Note Contract (The Workbench)]], which defines what may live in `20_Thinking/` at all.
- Harvester vs Compliance Sweep: [[Prompt - Tension Harvester]] puts the _right_ things into the workbench. [[Protocol - Workbench Compliance Sweep]] takes the _wrong_ things out. Run the Sweep first if the workbench is already polluted—harvesting into a folder full of clippings just hides the new notes.
- Triage vs Thinking-Pattern Analysis: [[Principal Vault Triage Architect]] organises a backlog (breadth, navigation). [[Zettelkasten Thinking-Pattern Analyst]] analyses an already-connected graph (depth, insight). Don't use Triage when you want insight, or Analyst when you want a cleanup plan.
- Three lenses on the same folder: [[Prompt - Zettelkasten Audit (Allosso Rubric)]] judges _how the notes are made_ (source layer, link reasons, keywords, review, readiness to write from). [[Zettelkasten Thinking-Pattern Analyst]] analyses _what the notes say_ about your thinking. [[Justification Graph Audit & Gap Closure]] audits _whether the argument graph is grounded_. Run the Allosso audit first when the vault feels like a collection, because the other two assume connected, sourced notes.
- Three ProdOS Architects (distinct outputs, same family): [[Prompt - ProdOS Chronos Synthesizer]] outputs a SoT. [[Prompt - ProdOS MoC Cartographer]] outputs a MOC. [[Prompt - ProdOS Protocol Architect]] outputs a Protocol. Choose by desired artefact type, not by task description alone.

## Agent Skills in `.agents/skills/` (Mechanical & Tooling Layer)

Alongside the epistemic prompts above, five ProdOS-adapted agent skills live in `.agents/skills/` for tool and syntax execution:

| Skill | Path | When to use |
|---|---|---|
| `kplex-obsidian-cli` | `.agents/skills/kplex-obsidian-cli/SKILL.md` | Inspect and drive `window.kplexApi.v1` via `obsidian vault="LLMeon" eval` (`neighbors`, `evidence`, `ontologyGuide`, `ontologyDocuments`, `inspectOntologyOccurrences`, `canvases`, `exportMarkdown`, canvas view/preset switching) and reference LLMeon's K-Plex ontology pairs and precedence rules. |
| `obsidian-bases` | `.agents/skills/obsidian-bases/SKILL.md` | Creating or editing `.base` files in `02_bases/` (formulas, `days_stale`, summaries, `type: kanban` boards) or embedding inline ` ```base ` dynamic tables (`this.file.links`) inside MoCs/SoTs. |
| `obsidian-cli` | `.agents/skills/obsidian-cli/SKILL.md` | Tier 2 fallback when `obsidian-llmeon` 1MCP is unreachable (`vault="LLMeon"` first-arg rule, `--json` last-arg rule, `content=` backslash guard) and hot-reloading K-Plex (`plugin:reload id=k-plex`, `dev:errors`). |
| `defuddle-knap` | `.agents/skills/defuddle-knap/SKILL.md` | Stage 0 web capture (`defuddle parse <url> --md --json`) and safe YAML frontmatter templating (`knap render` with `yaml_property`) into `00_Inbox/` before [[Prompt - Vault Ingest Router]] or [[Atomic Signal Extractor → Write TMP file]]. |
| `archery-consolidation` | `.agents/skills/archery-consolidation/SKILL.md` | Skill wrapper for [[Archery Shot Process - Knowledge Consolidation]]. |
## Task-logs (historical—do not Route to These)

These were captured as prompt notes but are one-off, dated, project-specific tasks. Keep for record-keeping; the CoS should never select them for a _new_ task:

- [[configure-basic-memory.prompt]]—2026-06-22, Basic Memory infra setup
- [[Goal - Frontmatter Bulk Migration (Phase 3)]]—2026-07-11, checkpointed vault migration
- [[You are an infrastructure-as-code and Azure backup expert]]—2026-04-30, FITFILE Azure backup Terraform task (FTFL-596/599/615)

## Maintenance Rule

When adding a new prompt note to this folder:

1. Set exactly one `type/<category>` tag from the taxonomy above.
2. Write a one-sentence `description` in the frontmatter that states what it does _and_ when to use it—this is what the CoS matches against.
3. If it overlaps with an existing prompt, add a one-line `> Trigger:` callout under the heading (see the four link-auditing prompts for the pattern) instead of leaving the ambiguity implicit.
4. If it's a one-off dated task rather than a reusable prompt, tag `type/task-log` and list it in the Task-logs section above.
5. TAC compliance is non-negotiable—both halves. Every prompt that creates or edits any vault note's frontmatter MUST embed a `## TAC FRONTMATTER COMPLIANCE (MANDATORY)` block, verbatim in spirit, requiring `title`, `type` (canonical lowercase value only, as listed under `type` in `10_System/schema/enums.yaml`), `tags`, `conformant`, and `non_conformance_reason` on every write. Any YAML template shown in the prompt's `OUTPUT FORMAT` must itself include these fields, not just describe them in prose—LLMs pattern-match off the example, so an example missing `conformant` reliably produces notes missing `conformant`. This is how we stop LLM sessions from re-inventing frontmatter conventions and drifting from the schema (~30% of the vault's `type` values are currently non-canonical drift from exactly this failure mode). This is the _frontmatter_ half of the Typed Answer Contract principle; every system/protocol prompt that produces prose, analysis, or synthesis (not just frontmatter) MUST separately carry an `> Output Contract:` callout pointing at [[Protocol - Typed Answer Contract (TAC) for Vault Agents]]—see that protocol and [[SoT - Typed Answer Contract (TAC) for LLM Output]] for the full rationale on both halves.
6. Own-words guard. Any prompt that can edit, merge into, rename, move or delete an existing note MUST carry the `> [!warning] Own-words guard` callout at the top of its body, pointing at [[AGENTS]] §6. Protected notes (any note with `own_words: true`, and every existing note in `01_journals/` and `20_Thinking/`) are never write targets for any prompt in this library, except the approved moves the Workbench Compliance Sweep is allowed under [[AGENTS]] §6.1.
