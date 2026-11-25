---
name: obsidian-bases
description: >-
  Create and edit Obsidian Bases (.base files in 02_bases/ and inline ```base code blocks)
  with views, filters, formulas, kanban boards, and summaries tailored to the LLMeon ProdOS
  schema. Use when working with .base files, building dynamic MoC/SoT tables, or creating
  table/cards/list/kanban views of notes.
---

# Obsidian Bases Skill (ProdOS Edition)

## ProdOS Vault Context

- All standalone `.base` files live in `02_bases/` (e.g., `Thinking.base`, `Zettelkasten.base`, `SoT.base`, `claim.base`, `concept.base`, `evidence.base`, `procedure.base`, `Question.base`, `MOCx.base`, `Inbox.base`, `LLM Prompts.base`).
- Every note is governed by `[[SoT - ProdOS Frontmatter Contract (Note Type Schemas)]]`:
  - Canonical `type` values: `claim`, `concept`, `evidence`, `question`, `procedure`, `protocol`, `map`, `journal`, `project`, `sot`, `link_report`, `equipment`, `source`, `prompt`, `tombstone`.
  - Base envelope fields: `title`, `type`, `tags`, `conformant` (boolean), `non_conformance_reason`, `status` (`seed`, `evergreen`, `stale`, `superseded`, or for HEAD notes `open`, `thinking`, `resolved`).
- Call `shale intent "<description>"` before editing any `.base` or `.md` file, and `shale done` when finished.

## Schema Overview

Base files use the `.base` extension and contain valid YAML:

```yaml
filters:
  and:
    - 'type == "claim"'
    - not:
        - 'file.hasTag("archive")'

formulas:
  days_stale: '(now() - file.mtime).days.round(0)'
  stale_flag: 'if((now() - file.mtime).days > 90 && status == "open", "⚠️ >90d Stale", "✅ Active")'

# Note properties MUST use the `note.` prefix in `properties:` or displayName is ignored!
properties:
  note.epistemic_status:
    displayName: "Epistemic Status"
  formula.days_stale:
    displayName: "Days Since Touch"
  formula.stale_flag:
    displayName: "Health"

summaries:
  avg_age: 'values.mean().round(1)'

views:
  - type: table | cards | list | kanban | map
    name: "View Name"
    limit: 50
    groupBy:
      property: note.status
      direction: ASC
    groupOrder:
      - open
      - thinking
      - resolved
    sort:
      - property: file.mtime
        direction: DESC
    filters:
      and:
        - 'conformant == true'
    order:
      - file.name
      - status
      - formula.days_stale
      - formula.stale_flag
    summaries:
      formula.days_stale: Average
```

## Key Rules & Pitfalls

1. **`properties:` Prefix Rule:** In `order`, `filters`, `groupBy`, and `sort`, a note property can be written bare (`status`) or prefixed (`note.status`). In the top-level `properties:` section, **always write `note.<property>`** (e.g. `note.status`), otherwise Obsidian ignores `displayName`.
2. **Duration Math:** Subtracting two dates (`now() - file.mtime`) returns a `Duration`, NOT a number. Access `.days` or `.hours` before calling `.round(0)`:
   - Correct: `'(now() - file.mtime).days.round(0)'`
   - Wrong: `'(now() - file.mtime).round(0)'`
3. **Null Guards in Formulas:** Guard optional date/number properties with `if()`:
   - `'if(due_date, (date(due_date) - today()).days.round(0), "")'`
4. **YAML Quoting:** Wrap formulas containing double quotes in single quotes (`'if(conformant, "✅", "❌")'`).
5. **Avoid `file.backlinks` in Large Bases:** `file.backlinks` is slow and does not auto-refresh when the vault changes; prefer reversing lookups with `file.links` or `file.hasLink(this.file)`.
6. **Sort Direction Must Be Uppercase:** `direction: ASC` or `direction: DESC` only; lowercase is silently ignored.

## Kanban Views (`type: kanban`, Obsidian 1.14+)

Cards are grouped into columns by `groupBy.property` (required). Dragging a card between columns updates that frontmatter property directly on the note (ideal for `Thinking.base` `open` → `thinking` → `resolved` or `claim.base` `seed` → `stable` → `evergreen`):

```yaml
  - type: kanban
    name: "Workbench Board"
    groupBy:
      property: note.status
      direction: ASC
    groupOrder:
      - open
      - thinking
      - resolved
    order:
      - file.name
      - AoL
      - tension
      - closing_condition
      - formula.days_stale
```

## Embedding Bases in MoCs & SoTs

1. **External `.base` embed:**
   ```markdown
   ![[Thinking.base#Think about this]]
   ```
2. **Inline ` ```base ` code block (per-note dynamic view using `this`):**
   Useful inside `MOC - *` or `SoT - *` notes to render a live table of notes linked from the current hub without creating a separate `.base` file:
   ````markdown
   ```base
   filters:
     and:
       - 'this.file.links.contains(file.asLink())'
   views:
     - type: table
       name: "Linked Notes"
       order:
         - file.name
         - type
         - status
         - conformant
   ```
   ````

## Functions Reference

See [references/FUNCTIONS_REFERENCE.md](references/FUNCTIONS_REFERENCE.md) for all Date, Duration, String, Number, List, File, Link, Object, and RegExp functions.
