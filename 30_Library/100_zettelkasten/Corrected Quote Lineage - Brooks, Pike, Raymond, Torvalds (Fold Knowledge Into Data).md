---
conformant: true
created: 2026-09-19T15:24:52+00:00
created_utc: 2026-09-19 00:00:00+00:00
definition: The smart data structures, dumb code phrasing commonly attributed to Torvalds is actually Eric Raymond phrasing, coined while Raymond was restructuring fetchmail protocol machines and credited by Raymond to a line in Brooks Mythical Man-Month, chapter 9; Raymond later formalised it as the Rule of Representation, fold knowledge into data so program logic can be stupid and robust.
distinguishes_from: []
modified: 2026-09-26T08:45:28+00:00
non_conformance_reason: ''
permalink: llmeon/00-inbox/corrected-quote-lineage-brooks-pike-raymond-torvalds-fold-knowledge-into-data
source_title: "The Conservation of Software Complexity: The Dichotomy of Data Structures and Control Flow (plus epistemic review/fact-check)"
source_url: unknown
status: seed
tags: [epistemics, eric-raymond, fred-brooks, quote-provenance]
title: Corrected Quote Lineage - Brooks, Pike, Raymond, Torvalds (Fold Knowledge Into Data)
type: concept
upstream: '[[tmp_atoms_data-structures-vs-control-flow]]'
used_in_claims: ["[[Smart Data Structures Yield Trivial Code (Torvalds' Maxim, Corrected Sourcing)]]"]
---

## Corrected Quote Lineage - Brooks, Pike, Raymond, Torvalds (Fold Knowledge Into Data)

The "smart data structures, dumb code" phrasing commonly attributed to Torvalds is actually Eric Raymond's, coined while restructuring fetchmail's protocol machines and credited by Raymond himself to Brooks's "Show me your tables" line in The Mythical Man-Month, chapter 9; Raymond later formalised it as the Rule of Representation: "Fold knowledge into data, so program logic can be stupid and robust."

### Scope & Conditions

A provenance correction establishing the actual attribution chain (Brooks 1975 → Pike 1989 → Raymond 1997/2003 → Torvalds 2006), not a new technical claim.

### Evidence

> "The 'smart structures / dumb code' phrasing is Raymond's. He drew it from reorganising fetchmail's protocol machines into a generic driver plus three method tables, and credited Brooks's Mythical Man-Month, chapter 9, as the same point."

### Implications

- Citations of this maxim should point to Raymond's Rule of Representation (or Brooks directly), not to Torvalds, unless specifically discussing Torvalds' independent restatement.

### Related

- [[SoT - The Data-Centric Philosophy]]—extends: its "Consensus of the Masters" table (§1) already lists Brooks, Pike, Raymond, and Torvalds as separate rows with separate quotes; this atom supplies the missing lineage connecting them (Raymond's phrasing derives from Brooks via Pike, not independently).

[extends:: [[SoT - The Data-Centric Philosophy]], confidence=high]

### Tensions

- [[SoT - Conservation of Complexity]]—contradicts: attributes the "data structures" maxim solely to Torvalds ("The Linus Torvalds Bridge") with no mention of the Brooks/Pike/Raymond lineage.
- [[SoT - Type-Driven Development (The Torvalds Loop)]]—contradicts: same single-attribution issue in its "Core Mandate" (§1).

[contradicts:: [[SoT - Conservation of Complexity]], confidence=medium]

[contradicts:: [[SoT - Type-Driven Development (The Torvalds Loop)]], confidence=medium]
