---
created: 2026-04-14T19:58:03+00:00
created_utc: "2026-04-14T12:40:00Z"
kind: mechanism
modified: 2026-04-19T18:30:43+00:00
source_title: "CUE — A Type System for the Cloud"
source_url: "https://youtube.com/watch?v=qgNuOjSZL9Y"
status: seed
tags: [computer-science, cue, lattice-theory, type-systems]
title: CUE Lattice Model
type: atom
upstream: "[[SoT - CUE Configuration]]"
---

## CUE Lattice Model

CUE treats types and values as a mathematical lattice, effectively merging the two concepts. In this model, a "type" is a set of all possible valid values, and a specific "value" is simply a set containing a single, concrete element. This unified representation allows for consistent reasoning across all levels of configuration.

### Scope & Conditions

The core conceptual and mathematical model of the CUE configuration language.

### Evidence

> "Unlike traditional languages that distinguish between types and values, CUE treats everything as a set (a mathematical lattice). A 'type' is simply a set of possible values, and a value is a set containing a single element."

### Implications

- Simplifies the conceptual model of configuration by removing the artificial boundary between schema and data.
- Enables types to act as functional filters and constraints within the unification process.

### Related

- [[SoT - Order Theory & Lattices]]—shared mechanism: provides the formal mathematical foundation for the CUE model.
- [[Calculus (Definition)]]—See Also.

### See Also

- [[SoT - CUE Configuration]]
