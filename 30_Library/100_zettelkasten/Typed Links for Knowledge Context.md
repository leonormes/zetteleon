---
aliases: [Relation Fields, Semantic Links]
conformant: true
contradicts: []
created: 2025-10-31T08:19:00+00:00
epistemic_status: high
evidence_links: []
modified: 2026-11-14T16:49:00+00:00
permalink: llmeon/30-library/100-zettelkasten/typed-links-for-knowledge-context
proposition: Typed links use inline relationship syntax to label how two notes relate, transforming bare wikilinks into a machine-readable semantic graph that supports directional navigation and argument compilation.
status: evergreen
tags: [linking, semantics, topic/knowledge-architecture, zettelkasten]
title: Typed Links for Knowledge Context
type: claim
---

## Typed Links for Knowledge Context

Typed links use inline relationship syntax (`[<relationship>:: [[Target]]]`) to label the relationship between notes, transforming bare `[[wikilinks]]` into meaningful, machine-readable connections.

### Mechanism & ProdOS Evolution

A bare wikilink `[[Atomic Note]]` records only that two notes are associated, not _why_ or _how_. A typed link answers that question by attaching a controlled relationship predicate:

- **Canonical ProdOS Syntax ([[SoT - Typed Edge Vocabulary (Knowledge Graph Relations)]]):** `[<relationship>:: [[Target]]]` using the closed 7-predicate vocabulary (`extends`, `synthesizes`, `implements`, `contradicts`, `supports`, `depends_on`, `revises`).
- **Legacy MoC Syntax (Deprecated for Compilation):** Earlier notes used visible inline fields such as `[[Note]] rel:: supports`, `rel:: part-of`, or `rel:: mitigates`. Neither `edge_lint.py` nor K-Plex parses `rel::`; canonical notes use `[<relationship>:: [[Target]]]` plus natural prose explanation on the bullet line.

### Why It Matters (Human + Computer Division)

1. **Human Elaboration:** Choosing a predicate and writing a one-sentence prose annotation forces the author to articulate the exact conceptual bridge rather than hoarding unexamined links ([[Creating Meaningful Links]], [[Eufriction - Productive Friction Strengthens Thinking]]).
2. **Three-Reader Execution:** Once written by the human, the same `[<relationship>:: [[Target]]]` line is read by Dataview (single-hop queries), **K-Plex** (directional Idea Compass, Mind Map, and Facets), and `edge_lint.py` ([[SoT - Knowledge Compiler (Argument Graph Spec)]] C1–C5 gap, foundation, conflict, and provenance checks).

## Related

- [[SoT - Typed Edge Vocabulary (Knowledge Graph Relations)]]—_The authoritative 7-predicate syntax and K-Plex Idea Compass specification implementing this claim._
- [[SoT - Knowledge Compiler (Argument Graph Spec)]]—_Specifies how the argument compiler interrogates `supports`, `depends_on`, and `contradicts` edges across the vault._ [implements:: [[SoT - Knowledge Compiler (Argument Graph Spec)]], strength=4, confidence=high]
- [[Claim - Domains relate through named relations, not undifferentiated association]]—_Establishes that named relations carry load-bearing epistemic structure that bare links discard._ [extends:: [[Claim - Domains relate through named relations, not undifferentiated association]], strength=4, confidence=high]
- [[Creating Meaningful Links]]—_Explains why explicit link context is essential for human sense-making._ [extends:: [[Creating Meaningful Links]], strength=4, confidence=high]
- [[Personal Context and Relevance are Key to Knowledge Formation]]—_Grounds why the human author must supply the relational context._
