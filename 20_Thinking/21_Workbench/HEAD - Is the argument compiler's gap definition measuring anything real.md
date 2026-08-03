---
title: HEAD - Is the argument compiler's gap definition measuring anything real?
type: question
tension: C1 reports 123 unsupported claims, but every one is a single-hop leaf, which
  is exactly the shape a too-generous definition would produce.
candidate_answers:
- Definition is too generous — require depth >1
- Definition is right, the graph is genuinely shallow
- Gaps should be weighted by how much rests on them
related_claims:
- '[[SoT - Knowledge Compiler (Argument Graph Spec)]]'
- '[[SoT - Typed Edge Vocabulary (Knowledge Graph Relations)]]'
sources:
- '[[SoT - Knowledge Compiler (Argument Graph Spec)]]'
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
permalink: llmeon/20-thinking/21-workbench/head-is-the-argument-compilers-gap-definition-measuring-anything-real
AoL: System
closing_condition: true
---

## The Question

`edge_lint.py --audit` reports 123 C1 gaps — claims that support something with nothing beneath them and no `axiom:` flag. Every gap is a leaf, and the graph is only two levels deep. Is C1 detecting a real epistemic problem, or is it just reporting the boundary of a shallow graph? Alongside this sit four deferred design decisions the spec parked: axiom representation, whether structural edges count in provenance, block-level versus note-level claims, and scan scope.

## Why It Matters

A metric that reports 123 problems is a metric nobody acts on. If C1 is over-reporting, it is worse than useless — it trains me to ignore the audit, which is the only quality gate the graph has. And the deferred decisions block C4 from being built at all.

## What I Currently Think

A shallow star is what a young graph looks like, so the shape alone does not prove the definition is wrong. But 123 is past the point of actionability. My lean is to weight gaps by in-degree — a leaf that three claims rest on matters; a leaf that one claim rests on is just the edge of the map — and to report only the top decile.

## What Would Settle It

Add an in-degree threshold flag to `edge_lint.py --audit` and see what the top decile looks like. If the top-10 gaps are ones I would actually want to close, the definition is fine and only the presentation was wrong. If they are still arbitrary, the definition needs changing. Either way this is a one-evening code change, not a design question.

## Sources

- [[SoT - Knowledge Compiler (Argument Graph Spec)]]