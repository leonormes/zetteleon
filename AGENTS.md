---
created: 2026-04-28T00:00:00+00:00
modified: 2026-07-30T00:00:00+01:00
permalink: llmeon/agents
tags: [agents, hermes, system]
title: AGENTS
---

## AGENTS.md—Agent Rulebook

Authoritative schema for all agent interactions with this vault. Single source of truth; no external spec supersedes this file.

**2026-07-30 — split notice:** the three-layer memory system (`raw/`, `wiki/`, `output/`, `log.md`) that used to live in this vault has moved to a standalone vault at `/Volumes/DAL/Zettelkasten/Hermes`. If a task involves Hermes's own raw sources, dossiers, or generated output, work in the Hermes vault under its own `AGENTS.md` — not here. This vault is **full read-write territory**. Agents may create, edit, and move notes anywhere — the human curates via review, not prohibition.

---

### 0. ProdOS Vault Taxonomy

Human-territory map. Agents may read and write freely across all folders — the human curates through review, not prohibition.

#### Note Types

| Type | Location | Naming convention | Purpose |
|------|----------|-------------------|---------|
| HEAD | `20_Thinking/21_Workbench/` | `HEAD - <question>?` | In-progress thinking, open questions |
| SoT | `30_Library/SoT/` | `SoT - Title.md` | Canonical knowledge, protocols |
| Protocol | `30_Library/SoT/` | `Protocol - Title.md` | Binary imperative procedures |
| Atomic / Claim | `30_Library/100_zettelkasten/` | Full-sentence title; `Claim - Title.md`; `Q — Title.md` | Atomic claims and questions |
| MoC | `30_Library/MoC/` | `MOC - Title.md` | Hub notes, maps of content |

#### Folder Structure

```
00_Inbox/             ← capture entry point
01_journals/          ← daily notes
10_System/            ← templates, scripts, prompts
20_Thinking/          ← HEAD notes, workbench
30_Library/           ← knowledge base (claims, projects, MoC, SoT, ops)
  100_zettelkasten/   ← atomic, claim, and question notes
  200_projects/       ← project notes
  MoC/                ← maps of content
  ops/                ← operational references
  SoT/                ← source-of-truth and protocol documents
```

Agents may read and write freely across all folders. The human curates through review, not prohibition.

#### Frontmatter

Canonical spec: [[SoT - ProdOS Frontmatter Contract (Note Type Schemas)]]. New notes use `prodos.kind` and `prodos.lifecycle`. Do not add legacy keys (`type`, `status`, `updated`, `creation_date`) to new content.

---

### 9. Typed Edge / Justification Graph Workflow

Governs how agents interact with the vault's typed-edge system and argument-graph compiler. Canonical syntax: [[SoT - Typed Edge Vocabulary (Knowledge Graph Relations)]]. Canonical capabilities: [[SoT - Knowledge Compiler (Argument Graph Spec)]].

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

#### 9.3 Writing in `30_Library`

Agents may write freely in `30_Library/100_zettelkasten/`, `30_Library/SoT/`, `30_Library/MoC/`, and `30_Library/200_Projects/` — including typed-edge lines (`%%[relationship:: [[target]]]%%`), `axiom:` markers, new notes, and body content. The human curates through review.

#### 9.4 Validation recommendation

For typed-edge or `axiom:` edits, consider running before finalising:

```
uv run --with pyyaml python3 10_System/scripts/edge_lint.py --path "<file or vault root>"
```

This validates that typed edges are well-formed and catches structural issues before they compound.

#### 9.5 How to actually do the work

- One note's links/edges need fixing or expanding → [[Note Refresh & Link Auditor]].
- The whole graph needs auditing for gaps/foundations/conflicts, and gaps closed → [[Justification Graph Audit & Gap Closure]].

---

_This file is managed by the Hermes PKM workflow. Do not delete._
