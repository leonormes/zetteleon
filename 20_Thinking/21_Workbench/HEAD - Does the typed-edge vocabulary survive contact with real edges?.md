---
title: HEAD - Does the typed-edge vocabulary survive contact with real edges?
type: question
tension: The vocabulary is lifecycle:seedling, seeded from one POC, and two of its
  guarantees are assumptions rather than enforced properties.
candidate_answers:
- Vocabulary is sufficient — leave it
- Add relationship types once real gaps appear
- Namespace block ids by note to enforce uniqueness
related_claims:
- '[[SoT - Typed Edge Vocabulary (Knowledge Graph Relations)]]'
- '[[SoT - Knowledge Compiler (Argument Graph Spec)]]'
sources:
- '[[SoT - Typed Edge Vocabulary (Knowledge Graph Relations)]]'
tags:
- state/thinking
- prodos/head
conformant: true
status: open
prodos:
  kind: head
  lifecycle: active
created: 2026-08-03 13:20:30+01:00
modified: 2026-08-03 13:20:30+01:00
permalink: llmeon/20-thinking/21-workbench/head-does-the-typed-edge-vocabulary-survive-contact-with-real-edges
---

## The Question

Three things in the typed-edge spec are recorded as assumptions rather than guarantees: block ids are vault-unique *by assumption* with only an ambiguity warning as guard; the preference for frontmatter over inline edges for note-to-note relations is *a convention, not a gate*; and the six-relationship vocabulary is *seeded, not proven*. Do any of these need to become enforced, and is the vocabulary missing a type?

## Why It Matters

627 edges now exist across 291 notes. That is past the point where a vocabulary change is free — the spec itself notes a second syntax migration would not be cheap. If a seventh relationship is needed, the cost of adding it rises every week.

## What I Currently Think

Two live vault errors are the evidence: `related_to` in [[Canonical Schema V1]] and `solves` in [[Focus on the Process Not the Product in Daily Writing]]. Someone — me — reached for a relationship that did not exist, twice. `solves` in particular is not expressible as any of the six. That is weak evidence the vocabulary is under-specified rather than that those two notes are simply wrong.

## What Would Settle It

Decide the two lint errors properly rather than by rewriting them into the nearest existing type: either add `solves` to §2 or state why `implements` covers it. One decision, recorded in the vocabulary table, closes this and drops the vault to 0 lint errors.

## Sources

- [[SoT - Typed Edge Vocabulary (Knowledge Graph Relations)]]