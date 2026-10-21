---
conformant: true
contradicts: []
created: 2026-10-21 14:00:00+00:00
epistemic_status: medium
evidence_links: []
modified: 2026-10-21 14:00:00+00:00
proposition: In this vault the frontmatter schema is the note type and its epistemic
  status in the vault formal system and not a label added to a note that already has
  one, so frontmatter violations are type errors and not style errors.
status: seed
tags:
- formal-methods
- topic/pkm
- topic/knowledge-architecture
- prodos
title: Frontmatter Is the Type of a Note and Not a Label Attached to It
type: claim
permalink: llmeon/30-library/100-zettelkasten/frontmatter-is-the-type-of-a-note-and-not-a-label-attached-to-it
---

## Frontmatter Is the Type of a Note and Not a Label Attached to It

In this vault the frontmatter schema is the note's type and its status in the vault's formal system, not a label added to a note that already has one. A note of type `claim` belongs to the class governed by the claim schema, and without the schema the vault cannot route, query or validate it. Frontmatter violations are therefore type errors and not style errors.

### Scope & Conditions

- It is a design stance for this vault, and the SoT presents it as the recursive case of its own axiom. It is an instance of the constitutive reading, not independent evidence for it.
- The SoT's example uses the `prodos` block. For atomic notes in `100_zettelkasten` that key was dropped on 2026-09-26, and `type` and `status` carry the same information, so the example is stale for those notes and holds for SoTs and maps where `prodos` is still optional metadata.
- The vault tolerates non-conformant notes. A note can carry `conformant: false` with a reason and be reported as a warning, so the structure is authoritative by the vault's choice and not absolutely.

### Evidence

> "The `prodos` frontmatter block is not a label attached to a note that already has epistemic status. It IS the note's epistemic status in the vault's formal system."
> ([[SoT - Structure is Truth is a Unifying Axiom Across Formal Systems]], §4 The Recursive Case, emphasis markers omitted)

> "`type` is **required** on every note (§2), set to one of the contract's enum values. Fileclass's own class-detection (`fileClassAlias: type`) keys off this field — a note without it gets no schema, no validation, no editable Bases row, whatever its `prodos` object says."
> (the vault's AGENTS.md, Frontmatter section)

### Implications

- Fixing a missing `type` is a type repair. The note changes class and gains the schema, validation and editable views that class carries.
- A validator for frontmatter is the vault's type checker, which is what [[SoT - ProdOS Frontmatter Contract (Note Type Schemas)]] and the shape script enforce.

### Related

[implements:: [[Structure Constitutes the Domain of Valid Facts Rather Than Representing a Pre-Existing Truth]], strength=3, confidence=medium]

[depends_on:: [[SoT - ProdOS Frontmatter Contract (Note Type Schemas)]], strength=4, confidence=high]

- [[Structure Constitutes the Domain of Valid Facts Rather Than Representing a Pre-Existing Truth]]—implements: the vault is one more formal system the claim applies to.
- [[SoT - ProdOS Frontmatter Contract (Note Type Schemas)]]—depends on: the contract is the type system this claim describes.
- [[SoT - Atomic Note Standard (The Proposition Card)]]—shared mechanism: the body and link rules that complete the schema.

### Tensions

- [[SoT - Atomic Note Standard (The Proposition Card)]]—tension, not contradiction: its `conformant: false` escape hatch lets a note exist and be read without meeting the schema, so the structure is not what makes the note exist.