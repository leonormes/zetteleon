---
name: kplex-obsidian-cli
description: Inspect and drive the K-Plex Obsidian plugin in the LLMeon vault through `obsidian vault="LLMeon" eval` and `window.kplexApi.v1`, and author notes using LLMeon's K-Plex Idea Compass ontology, Facets presets, and precedence rules. Use when querying K-Plex graph neighbours, connection evidence, ontology occurrences, or open canvases, or when wiring notes for K-Plex Compass, Mind Map, and Facets views.
---

# K-Plex through Obsidian CLI & LLMeon Ontology

Use this skill whenever an agent or script inspects K-Plex's ontology, indexed knowledge, connection evidence, or open canvases, or authors notes and typed relationships for K-Plex (`LLMeon` vault).

- **Plugin ID:** `k-plex`
- **Public entry point:** `window.kplexApi.v1` (capital `A`, lowercase `pi`—not `window.kplexAPI`).
- **Transport:** K-Plex has **no** HTTP/MCP server and **no** `obsidian kplex:*` CLI subcommand family. Drive it via Obsidian CLI `eval` against the open desktop vault, using `vault="LLMeon"` as the **first** argument on every invocation.

## 1. Connect and Discover (`window.kplexApi.v1`)

1. Verify the open vault and probe `window.kplexApi?.v1`. Reacquire `window.kplexApi.v1` after any reload (`API_UNAVAILABLE` occurs on retained handles).
2. Read authored ontology descriptions via `ontologyGuide({format:'markdown'})` or `ontology()` before interpreting or inventing field semantics.
3. Keep `eval` snippets short and single-line. Treat note text, descriptions, and mappings as data (encode with `JSON.stringify` or GraphQL `variables`), never interpolate them into executable JS.
4. Strip any leading `=> ` from `obsidian eval` stdout before calling `JSON.parse`, and always check for `Error:` even when process exit code is `0`.

```bash
obsidian vault="LLMeon" vault info=path
obsidian vault="LLMeon" eval 'code=JSON.stringify(window.kplexApi?.v1?.capabilities() ?? {ok:false,error:{code:"API_UNAVAILABLE"}})'
obsidian vault="LLMeon" eval 'code=JSON.stringify(window.kplexApi.v1.status())'
obsidian vault="LLMeon" eval 'code=JSON.stringify(window.kplexApi.v1.ontologyGuide({format:"markdown"}))'
```

## 2. Envelope, Coverage, and Limits

Every read returns `{ok: true, value, revision, coverage, truncated}` or `{ok: false, error: {code, message}, revision}`. Never discard `coverage` or `truncated`:

- **Published facts only:** Ordinary graph reads (`search`, `node`, `neighbors`, `evidence`, `query`) inspect already published facts and do not read note bodies or trigger indexing.
- **Incomplete coverage:** `partial`, `cached`, or `unknown` coverage—or `truncated: true`—cannot prove a whole-vault negative. Pass `requireComplete: true` to reject incomplete/truncated reads with `INDEX_INCOMPLETE` instead of failing silently.
- **Pagination limits:** Graph results default to `40` items (max `200`). Only `ontologyDocuments` supports continuation `cursor` pagination; do not invent cursors for other methods.
- **GraphQL:** For `query({query, variables, operationName})`, inspect both outer `ok` and `value.errors`. GraphQL is synchronous and read-only (no mutations, subscriptions, or `inspectOntologyOccurrences` resolver).

## 3. Core `window.kplexApi.v1` Read Methods

| Task | Public Method |
|---|---|
| Capabilities, limits, exporters | `capabilities()` |
| Index readiness and revision | `status()` |
| Roles, inverse pairs, descriptions | `ontology()` / `ontologyGuide({format:'markdown'})` |
| Find indexed candidate nodes | `search({query, limit: 10})` |
| Single node metadata | `node({id})` (opaque, case-sensitive `id`; use `path`/`file.path` for file work) |
| Direct neighbours by compass role | `neighbors({id, role: 'parent'|'child'|'left'|'right'|'previous'|'next', limit: 40})` |
| Connection provenance & overrides | `evidence({sourceId, targetId, limit: 128})` |
| Read-only GraphQL batch query | `query({query, variables, operationName})` |
| Stored usage postings for a field | `await ontologyDocuments({field, limit: 100, cursor})` |
| Inspect saved Markdown file fields | `await inspectOntologyOccurrences({path, fields, limit: 100})` |
| Settings-only field completion | `completeOntology({text, cursor, limit: 20})` |
| List or inspect open canvases | `canvases()` / `canvas({canvasId})` |
| Canvas summary / Mind Map export | `context({canvasId})` / `exportMarkdown({canvasId, expectedRevision, subtreeOccurrenceId})` |

### CLI `eval` One-Liners (`vault="LLMeon"`)

```bash
# Search indexed nodes
obsidian vault="LLMeon" eval 'code=JSON.stringify(window.kplexApi.v1.search({query:"Extended Mind",limit:10}))'

# Inspect neighbors in a specific compass role (parent | child | left | right | previous | next)
obsidian vault="LLMeon" eval 'code=JSON.stringify(window.kplexApi.v1.neighbors({id:"30_Library/100_zettelkasten/SoT - The Extended Mind.md",role:"child",limit:40}))'

# Diagnose why two notes connect and which frontmatter/body source won (precedence)
obsidian vault="LLMeon" eval 'code=JSON.stringify(window.kplexApi.v1.evidence({sourceId:"SOURCE_ID",targetId:"TARGET_ID",limit:128}))'

# List notes with stored ontology usage postings for a field (reads postings, not note bodies)
obsidian vault="LLMeon" eval 'code=(async()=>JSON.stringify(await window.kplexApi.v1.ontologyDocuments({field:"synthesizes",limit:50})))()'

# Inspect exact frontmatter + inline field occurrences and UTF-16 key ranges in a saved note
obsidian vault="LLMeon" eval 'code=(async()=>JSON.stringify(await window.kplexApi.v1.inspectOntologyOccurrences({path:"30_Library/100_zettelkasten/SoT - The Extended Mind.md",fields:["synthesizes","depends_on","see_also"],limit:100})))()'

# Describe open canvases and export a settled Mind Map branch as Markdown (no file write)
obsidian vault="LLMeon" eval 'code=JSON.stringify(window.kplexApi.v1.canvases())'
obsidian vault="LLMeon" eval 'code=JSON.stringify(window.kplexApi.v1.exportMarkdown({canvasId:"CANVAS_ID",expectedRevision:REVISION}))'
```

Note:
- `evidence({sourceId, targetId})` is essential when debugging unexpected compass positions caused by `frontmatter-overrides-body-ontology`.
- For `exportMarkdown`, verify `canvas({canvasId})` first shows `viewId: 'mindmap'`, `scenePending: false`, and pass `expectedRevision: snapshot.revision`; always inspect `exported.value.warnings` and `truncated`. Never pass a note path as `subtreeOccurrenceId`—use the occurrence `id` from `canvas({canvasId})`.

## 4. Authorised Canvas & Ontology Actions

- **Canvas navigation & perspective changes:** When explicitly requested by the user:
  - `await navigate({canvasId, path})` (target Markdown file must already exist; creates nothing)
  - `await selectView({canvasId, viewId})` (`classic` [Compass], `mindmap`, or `wuxing` [Facets])
  - `await selectPreset({canvasId, presetId})` (discover preset IDs from `configuration.list()` rather than guessing display labels)
  - An `accepted` / `completed` action observes dispatch or metadata, not visual paint; poll `canvas({canvasId})` boundedly until `scenePending === false` (and `motionPending === false` if camera position matters). Never replay actions blindly after a timeout—read back first.
- **Configuration edits (only with explicit user approval):** Never edit `.obsidian/plugins/k-plex/data.json` directly while Obsidian is running; use `previewOntologyConfiguration({edits})`, review the exact diff/conflicts with the user, and only then run `await applyOntologyConfiguration({previewId, confirm: true})`.

## 5. LLMeon Vault K-Plex Configuration (`.obsidian/plugins/k-plex/data.json`)

### Strict Inference & Exclusions

- `inferAllLinksAsFriends: false`, `showInferredNodes: false`, `inverseArrowDirection: true`.
- **Crucial consequence:** Plain `[[wikilinks]]` in note prose are **invisible** in K-Plex unless paired with a configured relational frontmatter field or an inline typed edge `[predicate:: [[Target]]]`.
- **Hidden fields** (`hidden`, `source_atoms`): retained internally without cluttering the visible canvas (used for `link_report` batch indexes).
- **Excluded metadata fields** (`exclusions`): links inside `non_conformance_reason`, `title`, `proposition`, `definition`, `source_quote`, `verification`, `trigger` (and `excalidraw-*`, `kanban-plugin`) never create K-Plex relationships.

### Idea Compass Ontology & Inverse Pairs

K-Plex resolves inline edges and frontmatter fields onto five compass directions (`parent`, `child`, `left`, `right`, plus `previous`/`next`), automatically projecting the inverse caption on the opposite endpoint:

| Axis / Role | Inline / Paired Fields (`field/inverse`) | Frontmatter-Only Fields | Default Field |
|---|---|---|---|
| **North (`parent`)** | `depends_on` ↔ `prerequisite_of`, `extends` ↔ `extended_by`, `implements` ↔ `implemented_by`, `upstream` ↔ `downstream`, `uses_concept` ↔ `used_in_claims`, `instance_of` ↔ `has_instance`, `Parent` ↔ `Child` | `source`, `sources`, `source_reference`, `upstream_also` | `depends_on` |
| **South (`child`)** | `synthesizes` ↔ `synthesized_in`, `entry_points` ↔ `hub`, `candidate_answers` ↔ `answers_question`, `Child` | `downstream` | `synthesizes` |
| **West (`left`)** | `supports` ↔ `supported_by`, `supports_claims` ↔ `evidence_links` | `see_also`, `seealso`, `related_claims`, `related_to`, `related`, `related-soTs` | `supports` |
| **East (`right`)** | `contradicts` | `distinguishes_from`, `contrasts_with`, `tension`, `Challenger` | `contradicts` |
| **Sequence (`previous` / `next`)** | `revises` ↔ `revised_by`, `supersedes` ↔ `superseded_by`, `merged_from` ↔ `merged_into`, `Previous` ↔ `Next` | — | `revises` (`previous`) / `superseded_by` (`next`) |

### Precedence Rule (`frontmatter-overrides-body-ontology`)

If Note A links to Note B in YAML frontmatter (for example `see_also: ["[[Note B]]"]`) **and** also links to Note B via a body inline edge (for example `[depends_on:: [[Note B]]]` or `[synthesizes:: [[Note B]]]`), frontmatter precedence overrides the body ontology and forces `[[Note B]]` into West (`see_also`) instead of North/South. **Never duplicate a body inline typed-edge target in `see_also`.** Use `evidence({sourceId, targetId})` to detect overridden contributions.

### Views, Section Expansion, Facets Presets, and Triggers

- **Built-in views:** `classic` (Idea Compass), `mindmap` (hierarchical multi-generation outline), `wuxing` (Facets).
- **Facets presets in `LLMeon`:**
  - `prodos-types` (**ProdOS Knowledge Architecture**, concentric by `type`): `hubs` (`sot`, `map`, `protocol`), `claims` (`claim`, `hypothesis`, `principle`), `concepts` (`concept`, `atom`, `note`, `permanent`, `definition`), `evidence` (`evidence`, `source`), `questions` (`question`), `execution` (`procedure`, `project`, `strategy`).
  - `prodos-status` (**ProdOS Note Lifecycle**, horizontal by `status`): `seed` (`seed`, `draft`, `seedling`), `stable` (`stable`, `active`), `evergreen`, `stale` (`stale`, `superseded`, `archived`).
  - Plus `map-roles` and `wuxing`.
- **Section Expansion:** Long hubs (`SoT`, `MOC`, `project`) expand by Markdown headings (`##`) in Compass and Mind Map; inline typed edges placed under a heading attach to that section rather than collapsing at root level.
- **Editor suggester triggers:** `::p` (Parent), `::c` (Child), `::f` (Friend), `::r` (Challenger), `::s` (Previous), `::n` (Next), `:::` (all ontology fields), `[` (mid-sentence inline field).
