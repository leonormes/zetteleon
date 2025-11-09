---
aliases: [Relation Fields, Semantic Links]
confidence: 0.92
created: 2025-10-31T08:19:00Z
epistemic: principle
last_reviewed: 2025-10-31
modified: 2025-11-01T09:43:59Z
purpose: "Explains how typed links add semantic meaning to wikilinks, transforming them from simple references into meaningful relationships."
review_interval: 90
see_also: []
source_of_truth: []
status: seedling
tags: [linking, semantics, zettelkasten]
title: Typed Links for Knowledge Context
type: concept
uid: 2025-10-31T08:19:00Z
updated: 2025-10-31T08:19:00Z
---

## Typed Links for Knowledge Context

**Summary:** Typed links use inline field syntax (e.g., `[[Note]] rel:: supports`) to label the relationship between a structural note and an atomic note, transforming bare links into meaningful, machine-readable connections.

**Details:**

A bare wikilink `[[Atomic Note]]` tells you that two notes are connected, but not *why* or *how*. A typed link answers that question by adding semantic metadata.

Common relation types include:

- `rel:: part-of`: Atomic note is a component of the larger structure
- `rel:: example-of`: Atomic note exemplifies the concept
- `rel:: supports`: Atomic note provides evidence for an argument
- `rel:: contradicts`: Atomic note challenges or opposes the point
- `rel:: mitigates`: Atomic note reduces risk or provides a solution

**Example:** Instead of `[[Error Budgets]]`, you write `[[Error Budgets]] rel:: mitigates strategy:: "Use bounded failure modes"`. This tells both humans and machines that the atomic note "Error Budgets" *mitigates* a risk mentioned in the structural note.

Typed links are placed inline within the narrative of a structural note (map, argument, comparison). They become queryable via Dataview, enabling you to ask questions like "show me all atomic notes that contradict this argument" or "find examples of X".

Without typed links, a MOC is just a list of links. With typed links, it becomes a semantic graph.
