---
aliases: []
conformant: true
contrasts_with:
- '[[Practice - Flat linking and tagging]]'
created: 2026-01-03T10:07:49+00:00
modified: 2026-11-15T10:17:00+00:00
permalink: llmeon/30-library/so-t/reference-file-structure
project_category: prodos
status: evergreen
tags:
- architecture
- prodos
- reference
- taxonomy
title: Reference - File Structure
type: sot
upstream:
- '[[SoT - PRODOS Core Specification]]'
---

## Reference - File Structure & Naming Conventions

### 1. The Core Structure

To maximize LLM context window efficiency and human retrieval speed, the vault follows the `AGENTS.md` §0 taxonomy (reconciled with the 2026-11-09 `30_Library/100_zettelkasten/` flattening):

| Directory | Component | Role | Cognitive Phase |
|:--- |:--- |:--- |:--- |
| `00_Inbox/` | The Stream | Frictionless Capture | Capture |
| `01_journals/` | The Log | Daily Notes & Time Logs | Capture / Reflect |
| `02_bases/` | The HUD | System Dashboards (`.base` files) | Orient |
| `10_System/` | The Kernel Tooling | Templates, Scripts, FileClasses, Prompts | Infrastructure |
| `20_Thinking/21_Workbench/` | The Workbench | Active Question Queue (`HEAD -` notes) | Refine (Thinking) |
| `30_Library/100_zettelkasten/` | The Canon | Flattened Knowledge Graph (`Claim`, `SoT`, `Protocol`, `MOC`, `Source`, `Q`) | Synthesize (Knowing) |
| `30_Library/200_projects/` | The Hangar | Project Anchor Notes | Engage (Doing) |
| `30_Library/ops/` | Operations | Operational References & Runbooks | Execute |

#### A. The Stream (`00_Inbox/` & `01_journals/`)

- `00_Inbox/`: Temporary capture entry point routed by `[[Prompt - Vault Ingest Router]]`.
- `01_journals/`: Daily Notes (`YYYY-MM-DD`) and chronological life logs. Existing notes here are protected human territory (`AGENTS.md` §6.1).

#### B. The HUD (`02_bases/`)

- Contents: Obsidian `.base` files (`Thinking.base`, `SoT.base`, `MOCx.base`, etc.) providing live structured views driven by `[[SoT - ProdOS Frontmatter Contract (Note Type Schemas)]]`.

#### C. System Tooling (`10_System/`)

- Contents: Templates, validators (`validate_note_frontmatter.py`, `validate_note_shape.py`, `edge_lint.py`), fileClasses, and `10_System/prompts/` governed by `[[SoT - Typed Answer Contract (TAC) for LLM Output]]`.

#### D. The Workbench (`20_Thinking/21_Workbench/`)

- Purpose: Flat queue of unresolved human questions (`HEAD - <question>?`) acting as active RAM.
- Rules: No sub-folders; protected human territory (`AGENTS.md` §6.1).
- Admission control (2026-08-03): governed by `[[SoT - HEAD Note Contract (The Workbench)]]` (Ownership, Origin, Convergence, Actionability). Captures (`source:`/`captured:`/`author:`) go to `00_Inbox/`, not here. Unresolved tensions from canonical notes are harvested into here by `[[Prompt - Tension Harvester]]`, leaving a `> Open threads:` pointer behind. Audited by `[[Protocol - Workbench Compliance Sweep]]`.

#### E. The Canon (`30_Library/100_zettelkasten/`, `200_projects/`, `ops/`)

- `30_Library/100_zettelkasten/` (flattened 2026-11-09): holds atomic claims (`Claim -` or full-sentence titles), questions (`Q —`), Sources (`Source -`), Maps of Content (`MOC -`), Sources of Truth (`SoT -`), and Protocols (`Protocol -`). Note type is set by frontmatter `type` and title prefix (`[[SoT - ProdOS Frontmatter Contract (Note Type Schemas)]]`), not subfolder path.
- `30_Library/200_projects/`: Project anchor and state notes linking to Todoist/Jira execution and `HEAD`/`SoT` thinking.
- `30_Library/ops/`: Operational runbooks and reference sheets.

#### F. The Archive (`99_Archive/`)

- Purpose: Retires resolved `HEAD` notes (with tombstones where cited; see HEAD Note Contract §3.1) and completed/deprecated material out of active working views.

---

### 2. Storage Protocols

#### The "No-Filing" Rule

We do not "file" notes by topic folder in ProdOS; we Type, Tag, and Link.

- Folders define _Lifecycle & Write Boundaries_ (Inbox, Journal, Workbench, Canon, System).
- Links and K-Plex typed edges define _Knowledge Architecture_ (`[[SoT - Typed Edge Vocabulary (Knowledge Graph Relations)]]`).

### Related

- [[SoT - PRODOS Core Specification]]—_Implements the directory and lifecycle boundary architecture of ProdOS._ [implements:: [[SoT - PRODOS Core Specification]], confidence=high]
- [[SoT - ProdOS Frontmatter Contract (Note Type Schemas)]]—_Type and schema rules that replace topic subfolders in 30_Library/100_zettelkasten/._ [depends_on:: [[SoT - ProdOS Frontmatter Contract (Note Type Schemas)]], confidence=high]
- [[SoT - HEAD Note Contract (The Workbench)]]—_Admission control and 99_Archive retirement rules for 20_Thinking/21_Workbench/._ [depends_on:: [[SoT - HEAD Note Contract (The Workbench)]], confidence=high]
- [[SoT - Execution Protocol (GTD & PARA)]]—_Aligns vault project anchors and archive boundaries with GTD execution._ [supports:: [[SoT - Execution Protocol (GTD & PARA)]], confidence=medium]
