---
created: 2026-06-11 16:00:00+01:00
modified: 2026-06-11 14:36:04+00:00
tags:
- gtd
- operon
- prodos
title: README
permalink: llmeon/operon/readme
---

## Purpose

Operon holds actionable work inside the vault. Knowledge stays in `30_Library/200_Projects/`; this folder holds outcomes, deliverables, and task infrastructure.

| Path | Holds |
|------|-------|
| `Operon/Projects/` | Parent outcome file tasks (GTD projects) |
| `Operon/Tasks/` | Deliverable file tasks |
| `Operon/Templates/` | File-task templates for Operon Task Creator |
| `Operon/Filters/` | Human-readable filter specs (live filters live in plugin settings) |

## Syncing to Todoist (Context Bridge)

Operon inline tasks carry metadata after the title: `{{operonId:: …}} {{status:: …}}` etc. **Todoist Context Bridge** does not know Operon syntax by default.

**Fix (already in plugin settings):** Settings → Todoist Context Bridge → **Task text cleanup patterns**:

```regex
\{\{[^}]+\}\}
```

That strips all Operon `{{field:: value}}` blocks before the task title is sent to Todoist. Wikilinks and plain task text are preserved.

Operon dates/priority are **not** auto-mapped to Todoist fields (Operon uses `{{dateDue:: …}}`, not Dataview `[due:: …]`). Set due/priority in the sync modal, or clarify the line in plain language before syncing.

## GTD Boundaries

- Operon—project backlog, subtasks, planning, agent-addressable vault work
- Todoist—one next physical action per active thread (runway)
- Jira—work-team outcomes (`jiraKey` field links only)

## Troubleshooting embed blocks

If `Operon Dashboard` shows `Filter "…" not found`:

1. **Settings → Operon → Filters** — confirm the ProdOS filters appear in the list.
2. **Reload Obsidian** (`Cmd+R`) — Operon reads `data.json` at startup; edits made on disk need a reload.
3. If filters are missing from Settings, check `.obsidian/plugins/operon/data.json` under `views.filters.filterIds`.
4. Dashboard embeds use `filterId: "fs_…"` (stable IDs). Human specs: `Operon/Filters/`.

## First-time Setup (once)

1. Reload Obsidian (or wait for Operon index rebuild).
2. Open each file in `Operon/Projects/` → Command palette → Edit or convert to file task (registers `operonId` if missing).
3. On `Hermes Optimisation`, select the four backlog checkboxes → Convert Selection to Operon Tasks → set `parentTask` to the Hermes parent.
4. Open [[Operon Dashboard]] for live task views.
5. Pin one task from a filter row when ready to execute; copy the single next action to Todoist.

Templates are in `Operon/Templates/` (configured in Operon settings). Filter specs are in `Operon/Filters/`; live filters are in plugin settings.

## Quick Commands

| Command | When |
|---------|------|
| Create New Operon Task | Structured capture |
| Create or edit inline task | Upgrade `- []` at cursor |
| Create file task | New deliverable in `Operon/Tasks/` |
| Convert Selection to Operon Tasks | Bulk-upgrade checkbox lists |
| Operon: Task Finder | Search by memory, not path |

## See also

- [[Operon Dashboard]]
- [[gtd-action-system]]
- [[Projects Dashboard]]