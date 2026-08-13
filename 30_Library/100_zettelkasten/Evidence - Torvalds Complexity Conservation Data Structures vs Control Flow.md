---
aliases: [Software Complexity is Conserved Between Control Flow and Representation]
conformant: true
created: 2026-07-27T22:00:00+00:00
epistemic_status: high
modified: 2026-08-13T10:54:46+00:00
permalink: llmeon/30-library/100-zettelkasten/evidence-torvalds-complexity-conservation-data-structures-vs-control-flow
prodos.kind: evidence
prodos.lifecycle: stable
proposition: "When data structures perfectly model domain constraints, procedural complexity can be shifted into the structural layer, simplifying the resulting code."
title: Evidence - Torvalds Complexity Conservation Data Structures vs Control Flow
---

%%[supports:: [[Software Complexity is Conserved Between Control Flow and Representation]]]%%

When a developer "worries about data structures" (Torvalds/Pike), they are moving complexity out of the procedural layer and into the structural layer. Smart Structures ⇒ Dumb Code: If the data model perfectly mirrors the problem domain's constraints, the algorithms required to manipulate that data become trivial, often reducing to simple traversals or lookups. Dumb Structures ⇒ Brittle Code: If the data model lacks internal constraints, the code must compensate with defensive null-checks, complex if/else ladders, and state-tracking flags.

Source: [[Code vs Data Structures (Torvalds Essay)]]
