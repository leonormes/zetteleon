---
aliases: [Software Complexity is Conserved Between Control Flow and Representation]
created: 2026-07-27T22:00:00+00:00
modified: 2026-07-28T09:12:53+00:00
permalink: llmeon/30-library/100-zettelkasten/evidence-torvalds-complexity-conservation-data-structures-vs-control-flow
source_reference: '[[Code vs Data Structures (Torvalds Essay)]]'
supports_claims:
- - Software Complexity is Conserved Between Control Flow and Representation
title: Evidence - Torvalds Complexity Conservation Data Structures vs Control Flow
type: evidence
---

%%[supports:: [[Software Complexity is Conserved Between Control Flow and Representation]], strength=4, confidence=high]%%

When a developer "worries about data structures" (Torvalds/Pike), they are moving complexity out of the procedural layer and into the structural layer. Smart Structures ⇒ Dumb Code: If the data model perfectly mirrors the problem domain's constraints, the algorithms required to manipulate that data become trivial, often reducing to simple traversals or lookups. Dumb Structures ⇒ Brittle Code: If the data model lacks internal constraints, the code must compensate with defensive null-checks, complex if/else ladders, and state-tracking flags.

Source: [[Code vs Data Structures (Torvalds Essay)]]
