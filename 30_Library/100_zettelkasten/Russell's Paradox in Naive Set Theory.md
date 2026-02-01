---
aliases: ["Russell's Paradox"]
created: 2025-11-01T11:22:13Z
last_reviewed: "2025-11-01"
modified: 2026-02-01T15:08:27+00:00
status: "seedling"
tags: ["foundations", "paradox", "set-theory", "topic/maths"]
title: "Russell's Paradox in Naive Set Theory"
type: "concept"
updated: 
---

Summary: Russell's Paradox (1901) exposed a fundamental contradiction in naive set theory by constructing the set of all sets that do not contain themselves, demonstrating that unrestricted set comprehension leads to logical inconsistency.

The Paradox:

Consider the set R = {x | x ∉ x}, the set of all sets that do not contain themselves as members. Does R contain itself?

- If R ∈ R, then by definition R ∉ R (contradiction)
- If R ∉ R, then by definition R ∈ R (contradiction)

Consequence:

This paradox revealed that the naive comprehension principle—that any definable collection forms a set—is logically flawed. It forced a complete reconstruction of set theory with explicit axioms that avoid such contradictions, leading to modern axiomatic set theories like ZF and ZFC.

Impact: The paradox was particularly devastating to Frege's logicist program, as it was discovered just as Frege was completing his foundational work.
