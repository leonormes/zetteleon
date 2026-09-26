---
conformant: true
contradicts: []
created: 2026-09-19T15:24:25+00:00
created_utc: 2026-09-19 00:00:00+00:00
epistemic_status: high
evidence_links: []
modified: 2026-09-25T16:29:31+00:00
non_conformance_reason: ''
permalink: llmeon/00-inbox/smart-data-structures-yield-trivial-code-torvalds-maxim-corrected-sourcing
proposition: Linus Torvalds argued that the difference between a bad and a good programmer is whether they prioritise their code or their data structures, and that well-chosen data structures make the algorithms operating on them self-evident.
source_title: "The Conservation of Software Complexity: The Dichotomy of Data Structures and Control Flow (plus epistemic review/fact-check)"
source_url: unknown
status: seed
tags: [data-structures, git, linus-torvalds, quote-provenance]
title: "Smart Data Structures Yield Trivial Code (Torvalds' Maxim, Corrected Sourcing)"
type: claim
upstream: '[[tmp_atoms_data-structures-vs-control-flow]]'
---

## Smart Data Structures Yield Trivial Code (Torvalds' Maxim, Corrected Sourcing)

Linus Torvalds argued that the difference between a bad and a good programmer is whether they prioritise their code or their data structures, and that well-chosen data structures make the algorithms operating on them self-evident.

### Scope & Conditions

Originates as a footnote in a 2006 git mailing-list reply about licensing and interoperability, not a general software essay or the 2016 TED talk (which supplies the separate linked-list example—see [[The Linked-List Good Taste Example Eliminates Complexity Rather Than Relocating It]]). Torvalds' actual point there is that a stable, well-documented data format is a durable interface while code built on it is disposable.

### Evidence

> "'Bad programmers worry about the code. Good programmers worry about data structures and their relationships.'"—footnote to Torvalds, "Re: Licensing and the library version of git", git mailing list, 27 Jul 2006.

### Implications

- The quote is frequently mis-cited as a standalone philosophical essay; its original context is a narrow point about interoperability via a stable data format.
- Citing this quote for a general "structure over control flow" thesis borrows context it wasn't made in.

### Related

- [[SoT - Conservation of Complexity]]—corrects/refines: quotes this exact line uncritically as "The Linus Torvalds Bridge" with no source or date; this atom supplies the missing provenance.
- [[SoT - Type-Driven Development (The Torvalds Loop)]]—corrects/refines: quotes the same line as "The Core Mandate" (§1) with no source; same correction applies.
- [[Corrected Quote Lineage - Brooks, Pike, Raymond, Torvalds (Fold Knowledge Into Data)]]—_this claim's own sourcing correction rests on that note's fuller attribution chain (Brooks → Pike → Raymond → Torvalds)._

[revises:: [[SoT - Conservation of Complexity]], confidence=high]

[revises:: [[SoT - Type-Driven Development (The Torvalds Loop)]], confidence=high]

[depends_on:: [[Corrected Quote Lineage - Brooks, Pike, Raymond, Torvalds (Fold Knowledge Into Data)]], confidence=high]
