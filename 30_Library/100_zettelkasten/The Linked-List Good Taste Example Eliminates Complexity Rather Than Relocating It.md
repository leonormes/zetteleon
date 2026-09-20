---
conformant: true
created: 2026-09-19T15:24:32+00:00
created_utc: 2026-09-19 00:00:00+00:00
modified: 2026-09-19T15:44:44+00:00
permalink: llmeon/00-inbox/the-linked-list-good-taste-example-eliminates-complexity-rather-than-relocating-it
source_title: "The Conservation of Software Complexity: The Dichotomy of Data Structures and Control Flow (plus epistemic review/fact-check)"
source_url: unknown
status: seed
tags: [elimination-vs-relocation, epistemics, good-taste, linked-list, linus-torvalds]
title: "The Linked-List Good Taste Example Eliminates Complexity Rather Than Relocating It"
type: claim
upstream: '[[Data Structures vs Control Flow]]'
---

## The Linked-List Good Taste Example Eliminates Complexity Rather Than Relocating It

Torvalds' preferred implementation of singly-linked-list node removal—using a pointer-to-a-pointer instead of tracking a "previous node"—removes the special-case `if` branch for the list head entirely rather than moving that complexity somewhere else.

### Scope & Conditions

A 2016 TED-talk example of "good taste" in code; demonstrated for singly-linked-list deletion specifically.

### Evidence

> "Because the data structure has been conceptually generalized through indirection, the edge case completely vanishes. The if statement is entirely eliminated… The if didn't move anywhere. It stopped existing."

### Implications

- This is the source report's own headline "conservation" example, yet it is structurally a counterexample: total complexity went down, not sideways.
- Elimination (this case) and relocation (see [[Rob Pike's Rule 5 - Data Dominates]], [[Parse, Don't Validate - Validation Is Lossy, Parsing Is Constructive]]) are mechanistically different outcomes and should not be conflated.

### Related

- [[SoT - The Data-Centric Philosophy]]—corrects/refines: §4 "The Litmus Test: Good Taste" describes this exact linked-list example uncritically as an instance of the conservation law; this atom corrects that framing to elimination, not relocation.
- [[Elimination and Relocation Are Distinct Complexity-Management Mechanisms, Often Conflated as Conservation]]—extends: this worked example is the concrete instance of that general distinction.

### Tensions

- [[Software Complexity is Conserved Between Control Flow and Representation]]—contradicts: that note's own "Trade-off" section cites the same Torvalds/Pike "worry about data structures" framing as strict conservation ("it cannot be destroyed, only relocated"); this specific worked example is a counterexample, not a confirming instance.
