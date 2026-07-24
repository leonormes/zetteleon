---
aliases: [Typed Edges, Edge Vocabulary, Knowledge Graph Relations, Edge Syntax]
created: 2026-07-24T00:00:00+00:00
modified: 2026-07-24T00:00:00+00:00
permalink: llmeon/30-library/so-t/so-t-typed-edge-vocabulary-knowledge-graph-relations
see_also: ["[[SoT - ProdOS Frontmatter Contract (Note Type Schemas)]]", "[[Protocol - Typed Answer Contract (TAC) for Vault Agents]]", "[[SoT - PRODOS Core Specification]]"]
tags: [domain/pkm, prodos/sot, topic/knowledge-graph]
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

A **typed edge** is a one-line, reading-view-invisible annotation that records a *directed, named* relationship from the note (or block) it sits in to another note or block: `%%source-type.relationship{target-id}%%`. It replaces the flat `[[wikilink]]` — which says only "these two are related" — with a claim the machine can check: *this concept **implements** that one; this claim **contradicts** that one*. The point is not ontological richness for its own sake (that fails the Utility-over-Truth axiom); it is that a compiler can then resolve every target, flag dangling references, and let you ask graph questions — "what contradicts this?", "what does this depend on?" — without hand-maintaining a second index. One encoding only: the terse `%%…%%` form is the single source of truth. No JSON-LD, no duplicated metadata blocks.

## 1. Syntax

```
%%<sourceType>.<relationship>{<targetId>}%%
%%<sourceType>.<relationship>{<targetId>|<attr>=<val>,<attr>=<val>}%%
```

- Wrapped in Obsidian comment markers `%% … %%` → invisible in reading view and Live Preview, but plain text on disk and greppable.
- `<sourceType>` — the type of the *emitting* node: one of the canonical note types (`claim`, `concept`, `evidence`, `question`, `procedure`) or a block `type`.
- `<relationship>` — one value from the controlled vocabulary (§2).
- `<targetId>` — resolves per §4 (a note title/id or a block id).
- Attributes (§3) are **optional**; the bare three-part form is always valid. This keeps the common case cheap (Low-Maintenance axiom).

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

A `<targetId>` resolves, in priority order, to:

1. A **block id** — the `id` of a `<!--content-block-start … id="…"-->` block anywhere in the vault.
2. A **note** — by `prodos.id`, then by `title`/filename, then by alias.

The compiler (§6) fails an edge whose target resolves to nothing (a *dangling edge*) and warns on one that resolves ambiguously (same id in two places). Targets are ids, **not** `[[wikilinks]]` — an edge is metadata about a link, not the link itself. Keep the human-readable `[[wikilink]]` in the prose; the `%%…%%` edge types it.

## 5. Why one encoding (not JSON-LD)

The reverse-engineered POC (`30_Library/200_Projects/linux-namespaces.md`) encoded every edge **twice** — once as a JSON-LD `Relationship` block, once as `%%…%%` shorthand. Two sources of truth for one fact guarantee drift, and the note's own frontmatter had already been shredded by a YAML round-trip through Obsidian's tooling — direct evidence that hand-authored nested structures are fragile in this vault. The `%%…%%` form is chosen as sole authority because it is one line, invisible in reading view, survives YAML rewriters (it lives in the body, not frontmatter), and is trivially greppable.

## 6. Compiler contract

The typed-edge layer is only as good as the pass that checks it. A conformant compiler (`10_System/scripts/edge_lint.py`, to be written) MUST, over its scope:

1. Extract every `%%<type>.<rel>{<target>[|attrs]}%%`.
2. Reject any `<rel>` outside the §2 vocabulary.
3. Resolve every `<target>` per §4; report **dangling** (0 matches) and **ambiguous** (>1) as errors.
4. Validate attribute types per §3 (`strength` ∈ 1–5, `confidence` in enum).
5. Emit a report only — **propose, never auto-edit** (mirrors the `UNSURE`/dry-run discipline in [[Protocol - Typed Answer Contract (TAC) for Vault Agents]]).

This is the link/edge half of the validator [[SoT - ProdOS Frontmatter Contract (Note Type Schemas)]] §9 names but says does not yet exist; `fileclass validate` (CLI) covers the frontmatter half. Union of the two = the ProdOS knowledge compiler.

## Tensions & Gaps

- **Compiler not written.** This spec is a contract with no enforcer yet — identical to the Frontmatter Contract §9 gap. Until `edge_lint.py` exists, edges are self-reported, not checked.
- **Block ids are vault-unique by assumption.** §4 resolves block ids globally, but nothing yet *enforces* uniqueness of a `content-block` id across notes. The compiler's ambiguity warning is the only guard; a stronger scheme (namespacing ids by note) may be needed if collisions appear.
- **Overlap with frontmatter relations is a convention, not a gate.** §2 says "prefer the frontmatter field for note→note", but nothing stops an author recording the same fact both ways. If this drifts in practice, promote the rule to a compiler check that flags an inline edge duplicating a frontmatter relation.
- **Vocabulary is seeded, not proven.** The six relationships come from one POC plus the existing Claim/Evidence fields. Expect to add or merge types once real edges accumulate — treat `lifecycle: seedling` literally.
