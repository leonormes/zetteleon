---
created: 2026-04-28T00:00:00+00:00
modified: 2026-07-30T00:00:00+01:00
permalink: llmeon/agents
tags: [agents, hermes, system]
title: AGENTS
---

## AGENTS.md—Agent Rulebook

Authoritative schema for all agent interactions with this vault. Single source of truth; no external spec supersedes this file.

**2026-07-30 — split notice:** the three-layer memory system (`raw/`, `wiki/`, `output/`, `log.md`) that used to live in this vault has moved to a standalone vault at `/Volumes/DAL/Zettelkasten/Hermes`, so this vault can stay human-authored territory everywhere except the one narrow exception in §9.3. If a task involves Hermes's own raw sources, dossiers, or generated output, work in the Hermes vault under its own `AGENTS.md` — not here. This vault's remaining agent surface is: read the taxonomy below, obey §6, and — only for typed-edge/`axiom:` bookkeeping — write into `30_Library/` per §9.

---

### 0. ProdOS Vault Taxonomy

Human-territory map. All agents must understand this structure to know what is off-limits and why.

#### Note Types

| Type | Location | Naming convention | Agent rule |
|------|----------|-------------------|-----------|
| HEAD | `20_Thinking/21_Workbench/` | `HEAD - <question>?` | **Constrained write (2026-08-03).** Governed by [[SoT - HEAD Note Contract (The Workbench)]]. An agent MAY create a new HEAD note and MAY move a non-compliant note out; it MUST NOT edit the body prose of a human-authored one. See §6a. |
| SoT | `30_Library/SoT/` | `SoT - Title.md` | Read-only, except typed-edge lines / `axiom:` (see §9.3). Canonical knowledge updated by human via Chronos Synthesis. |
| Protocol | `30_Library/SoT/` | `Protocol - Title.md` | Read-only. Binary imperative procedures. |
| Atomic / Claim | `30_Library/100_zettelkasten/` | Full-sentence title; `Claim - Title.md`; `Q — Title.md` | Read-only, except typed-edge lines / `axiom:` (see §9.3). To propose a claim, write a stub to the Hermes vault's `raw/proposed-claims/` — never write directly into the zettelkasten. |
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

### 6. Hard Constraints

| Rule | Reason |
|------|--------|
| Never write to `00_Inbox/`. | Human capture territory — the ingest router reads it, agents do not author into it. **Exception:** the Workbench Compliance Sweep MAY `git mv` a non-compliant note *into* `00_Inbox/`, because that is routing, not authoring. |
| Never edit the body prose of a human-authored note in `20_Thinking/`. | Superseded the blanket "never write to `20_Thinking/`" on 2026-08-03. Creating and routing HEAD notes is now sanctioned; rewriting the human's thinking is not. See §6a. |
| Never write or edit Claim/SoT content in `30_Library/`—stubs only, proposed in the Hermes vault's `raw/proposed-claims/`—except the §9.3 typed-edge/`axiom:` exception | The claim layer belongs to the human; agent crossing it erodes epistemic ownership. §9.3 is the one sanctioned, narrowly-scoped exception—no new claims, no proposition edits, no deletions under it |
| Every typed-edge or `axiom:` edit must leave `edge_lint.py` at 0 errors before being considered done | A report-only compiler is only trustworthy if the edges it reports on are kept valid (see §9.4) |
| Contradictions must be surfaced, not resolved | Resolution requires human judgement |
| ~~Query Pieces LTM before starting any new task~~ — **conditional as of 2026-08-01, see below** | — |

### 6a. Workbench write scope (2026-08-03)

`20_Thinking/21_Workbench/` moved from blanket read-only to **constrained write**. Canonical spec: [[SoT - HEAD Note Contract (The Workbench)]].

Agents MAY:

- create a new HEAD note conforming to the contract's §2 schema,
- `git mv` a note that fails the contract's §1 compliance tests to its correct home,
- backfill missing frontmatter on an existing HEAD note,
- append a `## What Would Settle It` stub where none exists.

Agents MUST NOT:

- edit or rewrite the body prose of a human-authored HEAD note,
- rename a legacy HEAD note (renaming rewrites backlinks — report the proposed title instead),
- delete anything. Every action is a move or an annotation.

**Why this changed.** The blanket ban made "help me keep my thinking queue clean" unfulfillable, so the workbench silently filled with Web Clipper captures — 22 of 44 notes at the time of the audit — until the folder's signal was gone. A rule that prevents the maintenance a folder needs does not protect the folder; it rots it. The narrow scope above is the smallest write surface that lets the sweep run.

**Related constraint — tensions.** Canonical notes MUST NOT carry `## Tensions & Gaps` / `## Open Questions` prose sections for *unresolved* problems; those become HEAD notes with a one-line `> **Open threads:**` pointer left in the source (contract §4). Rewriting an existing canonical note into that form is **outside** the §9.3 exception and needs explicit per-run human authorisation.

---

**Pieces LTM pre-task check — IF AVAILABLE (2026-08-01).** PiecesOS is currently
down, so this was being skipped on every session while still labelled mandatory.
A hard constraint that is routinely and legitimately skipped teaches agents that
the rest of this table is advisory too, so it has been demoted rather than left
to rot. **If** `mcp_pieces_*` tools are reachable, query them first per the Hermes
vault's `AGENTS.md` §7. **If not, proceed silently** — no log entry, no mention,
no treating it as a deviation. Restore this to the table above when PiecesOS works
again.

---

### 9. Typed Edge / Justification Graph Workflow

Governs how agents interact with the vault's typed-edge system and argument-graph compiler. Canonical syntax: [[SoT - Typed Edge Vocabulary (Knowledge Graph Relations)]]. Canonical capabilities: [[SoT - Knowledge Compiler (Argument Graph Spec)]]. Applies to any task touching a claim, concept, or SoT note that participates in the justification graph—not to general vault work.

#### 9.1 Tool preference for vault I/O

In order:

1. Obsidian tools exposed via 1MCP (`http://127.0.0.1:3050/mcp?app=claude-code`), server `obsidian-mcp-tools`—called **directly by name**, e.g. `obsidian-mcp-tools_1mcp_<tool>`. There is no discovery step: 1MCP replaced the old `retrieve_tools`/`call_tool` proxy pattern in June 2026 and exposes every upstream tool under its own name, same as any native tool. Never reintroduce a `retrieve_tools`/`call_tool` two-step. If a tool seems unavailable, run `curl -s http://127.0.0.1:3050/health | jq .servers` before assuming it doesn't exist—don't fall back silently.
2. The `obsidian` CLI when the MCP path isn't reachable: `read`, `create`, `append`, `property:set`, `search:context`, `backlinks`, `unresolved`, `eval`. Verified working whenever the Obsidian desktop app is running. **Since the 2026-07-30 vault split, always pass `vault=LLMeon` explicitly** — the CLI can now address more than one open vault by name, and this one is not the default.
3. Raw filesystem Read/Write only as a last resort, and never blind—`read` the file via one of the above first. A blind fs write bypasses Obsidian's `metadataCache`, so Dataview/backlinks/graph view can silently desync from disk until a reload.

`edge_lint.py`'s own full-vault batch scan is exempt from this—it reads files directly by design (`os.walk`), because a single-file-at-a-time CLI/MCP round trip does not scale to a whole-vault audit. This rule governs interactive single-note reads/writes, not the compiler's ingest step.

#### 9.2 Pre-task graph-state check

Before adding or editing a typed edge, an `axiom:` marker, or any note that participates in the argument graph, run:

```
uv run --with pyyaml python3 10_System/scripts/edge_lint.py --audit
```

and, if working a specific claim, `--why "<title>"` and/or `--impact "<title>"` on it. State what the graph currently looks like before changing it—don't add a duplicate edge or an `axiom:` flag onto a claim that's already grounded.

#### 9.3 Write scope in `30_Library` (the sanctioned exception to §0 / §6)

Agents MAY write directly into `30_Library/100_zettelkasten/`, `30_Library/SoT/`, `30_Library/MoC/`, and `30_Library/200_Projects/` notes, but ONLY to:

- add, edit, or remove a `%%[relationship:: [[target]]]%%` typed-edge line,
- set the `axiom: true` frontmatter boolean,
- maintain [[SoT - Typed Edge Vocabulary (Knowledge Graph Relations)]] and [[SoT - Knowledge Compiler (Argument Graph Spec)]] themselves.

Agents MUST NOT, under this exception: edit a claim's `proposition` or body prose, delete or rename a claim note, or author a brand-new claim note directly—new claims still go through the stub path (now in the Hermes vault, see its `AGENTS.md` §2.4). This exception exists because typed-edge/axiom bookkeeping is mechanical—recording a relationship the human already asserted in prose, not a judgement on the claim itself—and because without it, "help with the justification graph" cannot be fulfilled at all. Anything outside this narrow scope reverts to the general rule: propose, don't write.

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
