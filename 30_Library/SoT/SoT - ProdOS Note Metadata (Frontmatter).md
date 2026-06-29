---
aliases:
- Note metadata schema
- ProdOS frontmatter specification
created: 2026-04-08 18:00:00+00:00
modified: 2026-05-26 11:44:18+00:00
see_also:
- '[[CLAUDE.md]]'
tags:
- prodos/schema
- topic/pkm
title: SoT - ProdOS Note Metadata (Frontmatter)
permalink: llmeon/30-library/so-t/so-t-prod-os-note-metadata-frontmatter
---

## 1. Minimum Viable Understanding (MVU)

- Every new or substantially revised library note SHOULD expose a top-level YAML object `prodos` that states kind, lifecycle, and optional trust and review metadata.
- `title`, `created`, `modified`, and `tags` remain required at the top level for Obsidian, Dataview, and agent tooling.
- Legacy top-level keys (`type`, `status`, `trust-level`, `source_of_truth`, `last_reviewed`, `review_interval`, `updated`, `creation_date`, `id` / `ID` / `uid`) are deprecated for new content; map them into `prodos` (see §5).
- Hypotheses and experiments in `100_zettelkasten`: use `prodos.kind: atomic` and `prodos.atomic.form: hypothesis`. Keep tag `#hypothesis` where Dataview boards rely on it.

---

## 2. Layer A—Core (all First-class notes)

| Field | Required | Type | Rule |
|:------|:---------|:-----|:-----|
| `title` | Yes | string | Matches filename / H1 convention for the note kind. |
| `created` | Yes | string | ISO 8601 datetime with offset (e.g. `2026-04-08T18:00:00+00:00`). |
| `modified` | Yes | string | Same format as `created`; update when body or frontmatter meaningfully changes. |
| `tags` | Yes | list | Prefer hierarchical tags (`topic/…`, `prodos/…`, `type/…`). |
| `aliases` | No | list | Obsidian aliases; omit or `[]` if none. |
| `prodos` | Yes | mapping | See §3. |

Do not add `updated` or `creation_date` on new notes; use only `created` / `modified`.

---

## 3. The `prodos` Object

### 3.1 Universal Subkeys

| Key | Required | Type | Allowed values / notes |
|:----|:---------|:-----|:----------------------|
| `prodos.kind` | Yes | string | `head`, `sot`, `protocol`, `moc`, `atomic`, `project`, `ops`, `prompt`, `journal` |
| `prodos.lifecycle` | Yes | string | `seedling`, `active`, `stable`, `evergreen`, `archived` |
| `prodos.trust` | No | string | `low`, `working`, `stable`, `authoritative`—epistemic confidence, distinct from workflow lifecycle |
| `prodos.review` | No | mapping | Optional cadence; see below |
| `prodos.id` | No | string | Canonical stable id for the note (replaces `id`, `ID`, `uid`). Lowercase, `kebab-case` or alphanumeric slug. |

`prodos.review` (optional)

| Key | Type | Example |
|:----|:-----|:--------|
| `interval` | string | `6 months` (free text) or later ISO 8601 duration |
| `last_reviewed` | string (date) | `2026-04-08` |

### 3.2 Enumerations (normative)

`prodos.kind`—where the note lives in ProdOS routing (folder is normative; kind must agree):

| Value | Typical path |
|:------|:-------------|
| `head` | `20_Thinking/21_Workbench/` |
| `sot` | `30_Library/SoT/` (excludes `Protocol -` prefix; those are `protocol`) |
| `protocol` | `30_Library/SoT/` or `30_Library/ops/` when named `Protocol - …` |
| `moc` | `30_Library/MoC/` |
| `atomic` | `30_Library/100_zettelkasten/` |
| `project` | `30_Library/200_projects/` |
| `ops` | `30_Library/ops/` |
| `prompt` | `10_System/prompts/` |
| `journal` | `01_journals/` |

`prodos.lifecycle`

| Value | Meaning |
|:------|:--------|
| `seedling` | Capture or draft; structure incomplete. |
| `active` | In use; may change frequently (HEAD, experiments, live protocols). |
| `stable` | Reviewed; suitable as dependency for other notes. |
| `evergreen` | Hub or canonical; intentionally maintained over long horizons (many MoCs / core SoTs). |
| `archived` | Superseded or retired; see `superseded_by` / `supersedes` if applicable. |

`prodos.trust` (optional; maps legacy "how sure are we")

| Value | Typical legacy sources |
|:------|:----------------------|
| `low` | Early draft, single anecdote. |
| `working` | `trust-level: working-knowledge` |
| `stable` | `trust-level: stable`, many `status: stable` |
| `authoritative` | Policy-grade, audit-relevant, or formally reviewed. |

---

## 4. Layer B—Kind Extensions

Only include the block that matches `prodos.kind`. Nested under `prodos` keeps one namespace; agents and Dataview read `prodos.chronos`, `prodos.ops`, etc.

### 4.1 `sot`

```yaml
prodos:
  kind: sot
  chronos:
    last_synthesis: 2026-04-08
    synthesis_count: 1
```

| Key | Type | Notes |
|:----|:-----|:------|
| `prodos.chronos.last_synthesis` | date | Replaces top-level `last_synthesis`. |
| `prodos.chronos.synthesis_count` | integer | Replaces `synthesis-count`. |

`see_also` MAY remain top-level as a list of wikilinks for backward compatibility with existing SoTs.

### 4.2 `protocol`

```yaml
prodos:
  kind: protocol
  protocol:
    applies_to:
      - "[[FITFILE Platform]]"
    binary_checklist: true
```

Steps in the body remain binary (Done / Not Done). Filename: `Protocol - Title.md`.

### 4.3 `moc`

```yaml
prodos:
  kind: moc
  moc:
    hub_for:
      - prodos/moc
      - topic/adhd
    entry_points: []
```

`entry_points` may be empty; links usually live in the body.

### 4.4 `atomic`

```yaml
prodos:
  kind: atomic
  atomic:
    form: concept
```

`prodos.atomic.form`: `concept`, `claim`, `definition`, `metaphor`, `hypothesis`, `strategy`, `insight` (extend only via PR to this SoT).

For hypothesis / experiment atomics, set `form: hypothesis` and keep `tags` including `hypothesis` if existing Dataview queries use `#hypothesis`.

### 4.5 `ops`

```yaml
prodos:
  kind: ops
  ops:
    tool: kubectl
    target_service: argocd
    hop_level: local
    requires_tunnel: true
    prerequisites:
      - "[[cmd-ssh-bastion-tunnel]]"
```

Maps legacy top-level `tool`, `target_service`, `hop_level`, `requires_tunnel`, `prerequisites`.

### 4.6 `prompt`

```yaml
prodos:
  kind: prompt
  prompt:
    description: One-line purpose for routing and RAG.
    inject_as: system_context
```

### 4.7 `project` (optional)

```yaml
prodos:
  kind: project
  project:
    area: 10_Infrastructure
    owner: self
```

---

## 5. Layer C—Supersession

Optional top-level keys (wikilink or path string):

| Key | Use |
|:----|:----|
| `supersedes` | This note replaces the linked note. |
| `superseded_by` | This note is replaced by the linked note. |

---

## 6. Legacy Mapping (Phase 1—document only)

| Legacy key | New location |
|:-----------|:-------------|
| `type: head` / `SoT` / `map` / … | `prodos.kind` (use lowercase enum; `SoT` → `sot`, `map` → `moc`) |
| `type: concept` / `hypothesis` / … on atomics | `prodos.kind: atomic` + `prodos.atomic.form` |
| `type: atomic_command` / `command` / `playbook` | `prodos.kind: ops` (retain disambiguation in `tags`) |
| `status: stable` / `evergreen` / … | `prodos.lifecycle` (align semantics; `evergreen` stays `evergreen`) |
| `trust-level` | `prodos.trust` |
| `source_of_truth: true` | `prodos.lifecycle: evergreen` or `prodos.trust: authoritative` (context-dependent) |
| `last_reviewed`, `review_interval` | `prodos.review.last_reviewed`, `prodos.review.interval` |
| `last_synthesis`, `synthesis-count` | `prodos.chronos.*` |
| `updated`, `creation_date` | remove; use `modified` / `created` |
| `id`, `ID`, `uid` | `prodos.id` |

---

## 7. Copy-paste Examples

### HEAD (workbench)

```yaml
---
title: 2026-04-08-1430-HEAD Short topic label
created: 2026-04-08T14:30:00+00:00
modified: 2026-04-08T14:30:00+00:00
tags: [state/thinking, prodos/head]
aliases: []
prodos:
  kind: head
  lifecycle: active
---
```

### SoT (canonical)

```yaml
---
title: SoT - Example Topic
created: 2026-04-08T18:00:00+00:00
modified: 2026-04-08T18:00:00+00:00
tags: [prodos/sot, topic/example]
aliases: []
prodos:
  kind: sot
  lifecycle: stable
  trust: stable
  review:
    interval: 6 months
    last_reviewed: 2026-04-08
  chronos:
    last_synthesis: 2026-04-08
    synthesis_count: 0
see_also: []
---
```

### Protocol

```yaml
---
title: Protocol - Example Runbook
created: 2026-04-08T18:00:00+00:00
modified: 2026-04-08T18:00:00+00:00
tags: [prodos/protocol, topic/ops]
aliases: []
prodos:
  kind: protocol
  lifecycle: active
  protocol:
    applies_to: []
    binary_checklist: true
---
```

### MoC

```yaml
---
title: MOC - Example Hub
created: 2026-04-08T18:00:00+00:00
modified: 2026-04-08T18:00:00+00:00
tags: [prodos/moc, topic/example]
aliases: []
prodos:
  kind: moc
  lifecycle: evergreen
  moc:
    hub_for: [topic/example]
---
```

### Atomic (hypothesis)

```yaml
---
title: Example Hypothesis Stated as a Full Sentence
created: 2026-04-08T18:00:00+00:00
modified: 2026-04-08T18:00:00+00:00
tags: [hypothesis, topic/productivity, prodos/atomic]
aliases: []
prodos:
  kind: atomic
  lifecycle: active
  atomic:
    form: hypothesis
---
```

---

## 8. Migration Stance

1. Forward-only: new and heavily edited notes adopt `prodos` first.
2. High-traffic next: MoCs, core SoTs, ops commands.
3. Bulk normalisation only after enums are stable and any tooling (Dataview dashboards) is updated.

---

## 9. Machine-readable Schema

1. JSON Schema (many tools / IDEs): `gemini-scribe/schemas/prodos-note-frontmatter.schema.json`.
2. CUE (sum-type friendly; recommended for `prodos.kind`-specific rules): `gemini-scribe/cue/prodos_frontmatter.cue`. Validate one extracted frontmatter object as JSON:
   - `cue vet -d '#Frontmatter' path/to/frontmatter.json gemini-scribe/cue/prodos_frontmatter.cue`
3. Vault scan: `gemini-scribe/scripts/validate_note_frontmatter.py` (requires [PyYAML](https://pypi.org/project/PyYAML/); expects `cue` on `PATH` for full checks). See `gemini-scribe/cue/README.md`.

Why keep CUE and JSON Schema? CUE expresses "`atomic` implies `atomic.form`" without brittle `if`/`then`. JSON Schema remains the lowest-friction option for tools that do not install CUE. Update both when this spec changes.

---

## 10. Tensions & Gaps

- Obsidian community plugins may expect legacy top-level keys; keep one legacy read path in scripts until Phase 3.
- Deeply nested YAML is harder to hand-edit; prefer shallow `prodos` for atomics and ops.
- `00_Inbox` / quick captures: minimal frontmatter acceptable (`title`, `created`, `modified`, `tags`) until triaged; then add full `prodos`.