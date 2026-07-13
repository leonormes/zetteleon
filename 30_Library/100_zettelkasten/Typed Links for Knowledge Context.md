---
aliases: [Relation Fields, Semantic Links]
created: 2025-10-31T08:19:00+00:00
modified: 2026-07-13T08:52:33+00:00
permalink: llmeon/30-library/100-zettelkasten/typed-links-for-knowledge-context
tags: [linking, semantics, zettelkasten]
title: Typed Links for Knowledge Context
---

## Typed Links for Knowledge Context

Summary: Typed links use inline field syntax (e.g., `[[Note]] rel:: supports`) to label the relationship between a structural note and an atomic note, transforming bare links into meaningful, machine-readable connections.

Details:

A bare wikilink `[[Atomic Note]]` tells you that two notes are connected, but not _why_ or _how_. A typed link answers that question by adding semantic metadata.

Common relation types include:

- `rel:: part-of`: Atomic note is a component of the larger structure
- `rel:: example-of`: Atomic note exemplifies the concept
- `rel:: supports`: Atomic note provides evidence for an argument
- `rel:: contradicts`: Atomic note challenges or opposes the point
- `rel:: mitigates`: Atomic note reduces risk or provides a solution

Example: Instead of `[[Error Budgets]]`, you write `[[Error Budgets]] rel:: mitigates strategy:: "Use bounded failure modes"`. This tells both humans and machines that the atomic note "Error Budgets" _mitigates_ a risk mentioned in the structural note.

Typed links are placed inline within the narrative of a structural note (map, argument, comparison). They become queryable via Dataview, enabling you to ask questions like "show me all atomic notes that contradict this argument" or "find examples of X".

Without typed links, a MOC is just a list of links. With typed links, it becomes a semantic graph.
