---
aliases: [Typed Edges, Edge Vocabulary, Knowledge Graph Relations, Edge Syntax]
created: 2026-07-24T00:00:00+00:00
modified: 2026-07-27T11:50:15+00:00
permalink: llmeon/30-library/so-t/so-t-typed-edge-vocabulary-knowledge-graph-relations
see_also: ["[[SoT - ProdOS Frontmatter Contract (Note Type Schemas)]]", "[[Protocol - Typed Answer Contract (TAC) for Vault Agents]]", "[[SoT - PRODOS Core Specification]]"]
tags: [domain/pkm, prodos/sot, topic/knowledge-architecture, topic/knowledge-graph]
title: SoT - Typed Edge Vocabulary (Knowledge Graph Relations)
type: sot
conformant: true
prodos:
  kind: sot
  lifecycle: seedling
  trust: working
---
> Canonical status: this note is the authoritative spec for **typed edges** — inline, machine-checkable relationships between notes and blocks. It is the link/edge counterpart to [[SoT - ProdOS Frontmatter Contract (Note Type Schemas)]], which governs the *note-level* schema. Where the two overlap (e.g. `contradicts`, `supports`), the Frontmatter Contract's frontmatter fields are authoritative for note→note relations; typed edges extend the same vocabulary down to the *block* level and add optional weighting. New relationship types are added **here only**.

## Minimum Viable Understanding (MVU)

A **typed edge** is a one-line, reading-view-invisible annotation that records a *directed, named* relationship from the note (or block) it sits in to another note or block: `%%[relationship:: [[target]]]%%`. It replaces the flat `[[wikilink]]` — which says only "these two are related" — with a claim the machine can check: *this concept **implements** that one; this claim **contradicts** that one*. The point is not ontological richness for its own sake (that fails the Utility-over-Truth axiom); it is that a compiler can then resolve every target, flag dangling references, and let you ask graph questions — "what contradicts this?", "what does this depend on?" — without hand-maintaining a second index. One encoding only: the `%%[… :: …]%%` form is the single source of truth. No JSON-LD, no duplicated metadata blocks.

The interior is a **Dataview inline field**, which buys the encoding a second reader for free: Dataview indexes every edge as a queryable property, so single-hop questions (`LIST WHERE contradicts`) are answerable *inside Obsidian with zero code*, while the compiler (§6) handles everything DQL structurally cannot — validation, traversal, cycle detection.

## 1. Syntax

```
%%[<relationship>:: [[<target>]]]%%
%%[<relationship>:: [[<target>]], <attr>=<val>, <attr>=<val>]%%
%%[<relationship>:: <block-id>]%%
```

- Wrapped in Obsidian comment markers `%% … %%` → invisible in reading view and Live Preview, but plain text on disk and greppable. Dataview parses the inline field regardless of the comment wrapper (verified against `dataview.api.page()`).
- `<relationship>` — one value from the controlled vocabulary (§2), used as the *field name*. This is what makes the edge queryable: `WHERE supports` finds every note emitting a `supports` edge.
- `<target>` — a `[[wikilink]]` for a note, or a bare id for a content-block (§4).
- Attributes (§3) are **optional**, comma-separated after the target. The bare two-part form is always valid, keeping the common case cheap (Low-Maintenance axiom).

No `sourceType` prefix. The emitting node's type is already recorded in its own frontmatter `type:` (or its `content-block-start type=`), so repeating it in every edge was a second copy of a fact that could drift — and the compiler never read it.

One edge per marker. Multiple edges from the same block = multiple markers, one per line.

## 2. Relationship vocabulary (controlled)

Direction is always **source → target**, read "*source `relationship` target*".

| Relationship | Meaning (source → target) | Overlaps existing field |
|:---|:---|:---|
| `extends` | Source builds on / specialises the target. | — |
| `synthesizes` | Source combines several targets into a higher-order idea. | — |
| `implements` | Source is a concrete realisation of an abstract target. | — |
| `contradicts` | Source conflicts with / negates the target. | Claim `contradicts` |
| `supports` | Source provides evidence or argument *for* the target. | Evidence `supports_claims` |
| `depends_on` | Source requires the target to make sense or function. | — |

Rules: the list is **closed** — an unknown relationship is a compiler error, not a silent pass (structure over discipline). To add a type, edit this table; that is the only sanctioned route. Where an edge duplicates a frontmatter relation already required by a note's fileClass (e.g. a `claim` note's `contradicts`), prefer the frontmatter field for note→note and reserve the inline edge for block→block or block→note precision.

## 3. Edge attributes (optional)

| Attribute | Type | Values | Default |
|:---|:---|:---|:---|
| `strength` | integer | 1–5 | unset (treated as 3) |
| `confidence` | enum | `high` \| `medium` \| `low` | unset |

Deliberately only two. The original POC also carried `evidence: empirical` and a JSON-LD `@context`; both are dropped — a fixed vocabulary plus these two weights is the ceiling before annotation cost outruns its value (see the schema-complexity trade-off in [[SoT - Typed Answer Contract (TAC) for LLM Output]]). Anything richer belongs in prose, not in the edge.

## 4. Targets & resolution

A target is written one of two ways, and the form determines how it resolves:

1. **A note — always a `[[wikilink]]`.** Resolves by `prodos.id`, then `title`/filename, then alias. `[[Note|Alias]]`, `[[Note#Heading]]` and `[[Note#^block]]` all resolve to `Note`.
2. **A content-block — a bare id.** The `id` of a `<!--content-block-start … id="…"-->` block anywhere in the vault. Blocks are not files, so they cannot be linked; this is the only case where a bare target is valid, and the compiler warns if a *note* target is written bare.

**Why notes are wikilinks.** An earlier revision of this spec required bare ids on the reasoning that "an edge is metadata about a link, not the link itself". That was the wrong trade. A bare id is a hand-maintained copy of a note's title: rename the note and every edge pointing at it silently dangles, and the author gets no signal until a lint run. A wikilink is rewritten automatically by Obsidian's own rename refactoring, so the edge survives; it also makes the target resolvable by Dataview and visible in the graph view. The cost — the target now appears in backlinks — is a feature, not the duplication the old rule feared.

The compiler (§6) fails an edge whose target resolves to nothing (a *dangling edge*) and warns on one that resolves ambiguously (same id in two places).

## 5. Why one encoding (not JSON-LD)

The reverse-engineered POC (`30_Library/200_Projects/linux-namespaces.md`) encoded every edge **twice** — once as a JSON-LD `Relationship` block, once as `%%…%%` shorthand. Two sources of truth for one fact guarantee drift, and the note's own frontmatter had already been shredded by a YAML round-trip through Obsidian's tooling — direct evidence that hand-authored nested structures are fragile in this vault. The `%%…%%` form is chosen as sole authority because it is one line, invisible in reading view, survives YAML rewriters (it lives in the body, not frontmatter), is trivially greppable, and — since the interior is a Dataview inline field — is queryable without any tooling of our own.

### 5.1 Ingest scope (what the compiler does *not* read)

Relationship information exists in this vault in four other shapes. `edge_lint.py` parses **only** the §1 encoding. This is a deliberate scope boundary, recorded here so it is a visible decision rather than a silent omission:

| Shape | Example | Count | Status |
|:---|:---|---:|:---|
| §1 typed edge | `%%[supports:: [[X]]]%%` | 69 | **parsed** — canonical |
| Visible inline field | `rel:: contradicts` in MoC prose | ~303 | not parsed — different grammar (relationship as *value*, not field name), and visible in reading view |
| Prose tension list | `[[X]]—contradicts: <explanation>` under `## Tensions` | ~133 | not parsed — free text, carries an explanation a typed edge cannot hold |
| Frontmatter relation | `contradicts:` in a `claim` fileClass | 2 | not parsed — `fileclass validate` owns the frontmatter half (§6) |

The prose and frontmatter forms are **not** deprecated: §2 already prefers the frontmatter field for note→note relations, and a prose tension records *why* two notes conflict, which no edge attribute captures. They are complementary, not rivals. The visible `rel::` form in MoCs is the only genuine near-duplicate of §1, and migrating it is optional — a decision to make only if those MoCs start carrying argument weight.

## 6. Compiler contract

The typed-edge layer is only as good as the pass that checks it. A conformant compiler (`10_System/scripts/edge_lint.py`, **written and in use**) MUST, over its scope:

1. Extract every `%%[<rel>:: <target>[, attrs]]%%`, ignoring occurrences inside fenced or inline code so this spec's own examples are not linted as data.
2. Reject any `<rel>` outside the §2 vocabulary.
3. Resolve every `<target>` per §4; report **dangling** (0 matches) and **ambiguous** (>1) as errors, and a bare note target as a warning.
4. Validate attribute types per §3 (`strength` ∈ 1–5, `confidence` in enum).
5. Emit a report only — **propose, never auto-edit** (mirrors the `UNSURE`/dry-run discipline in [[Protocol - Typed Answer Contract (TAC) for Vault Agents]]).

`edge_lint.py` requires PyYAML and **refuses to run without it**. Frontmatter supplies both `title` (needed to resolve edge targets) and `type` (needed to identify claims); without it the tool silently reported false dangling errors and a false-empty gap audit. For a report-only tool, refusing to run beats printing confident wrong answers.

```bash
uv run --with pyyaml python3 10_System/scripts/edge_lint.py --audit
```

This is the link/edge half of the validator [[SoT - ProdOS Frontmatter Contract (Note Type Schemas)]] §9 names but says does not yet exist; `fileclass validate` (CLI) covers the frontmatter half. Union of the two = the ProdOS knowledge compiler.

## Tensions & Gaps

- **The two readers disagree about code blocks.** `edge_lint.py` masks fenced and inline code before parsing, so an edge written as a documentation *example* is ignored. Dataview does not: it indexes inline fields inside code spans as real properties. A note explaining the syntax therefore shows up in `LIST WHERE contradicts` but not in the compiler's graph — which is exactly how this vault's own handoff note became the single Dataview `contradicts` hit while the compiler correctly reported zero. Prefer prose over a live-looking example when documenting edges, and treat DQL counts as an upper bound on real edges.
- **Syntax migrated once already.** Edges were originally written `%%claim.supports{Target}%%` with bare-id targets. On 2026-07-25 all 69 live edges across 21 notes were migrated to the §1 Dataview form, the `sourceType` prefix was dropped as an unread duplicate of frontmatter `type:`, and note targets became wikilinks. The audit output was byte-identical before and after, so the migration was lossless — but a second syntax change would not be free, and the vocabulary is still `lifecycle: seedling`. Treat §1 as settled unless Dataview itself changes.
- **Block-id targets are the one un-linkable case.** 16 of the 69 edges target `content-block` ids and so must stay bare, because a block is not a file. They therefore keep the rename fragility that wikilinks solved for notes. If block-level claims become common, they need either real Obsidian `^block-refs` or a namespacing scheme — see the uniqueness gap below.
- **Block ids are vault-unique by assumption.** §4 resolves block ids globally, but nothing yet *enforces* uniqueness of a `content-block` id across notes. The compiler's ambiguity warning is the only guard; a stronger scheme (namespacing ids by note) may be needed if collisions appear.
- **Overlap with frontmatter relations is a convention, not a gate.** §2 says "prefer the frontmatter field for note→note", but nothing stops an author recording the same fact both ways. If this drifts in practice, promote the rule to a compiler check that flags an inline edge duplicating a frontmatter relation.
- **Vocabulary is seeded, not proven.** The six relationships come from one POC plus the existing Claim/Evidence fields. Expect to add or merge types once real edges accumulate — treat `lifecycle: seedling` literally.

%%[implements:: [[Claim - Domains relate through named relations, not undifferentiated association]], strength=4, confidence=high]%%
%%[implements:: [[Typed Links for Knowledge Context]], strength=5, confidence=high]%%
