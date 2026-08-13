---
aliases: ["Russell's Paradox"]
conformant: false
created: 2025-11-01T11:22:13+00:00
modified: 2026-08-13T10:54:52+00:00
non_conformance_reason: "Bulk inferred type. Needs review."
permalink: llmeon/30-library/100-zettelkasten/russells-paradox-in-naive-set-theory
tags: [foundations, paradox, set-theory, topic/maths]
title: "Russell's Paradox in Naive Set Theory"
type: claim
---

Summary: Russell's Paradox (1901) exposed a fundamental contradiction in naive set theory by constructing the set of all sets that do not contain themselves, demonstrating that unrestricted set comprehension leads to logical inconsistency.

The Paradox:

Consider the set R = {x | x ∉ x}, the set of all sets that do not contain themselves as members. Does R contain itself?

- If R ∈ R, then by definition R ∉ R (contradiction)
- If R ∉ R, then by definition R ∈ R (contradiction)

Consequence:

This paradox revealed that the naive comprehension principle—that any definable collection forms a set—is logically flawed. It forced a complete reconstruction of set theory with explicit axioms that avoid such contradictions, leading to modern axiomatic set theories like ZF and ZFC.

Impact: The paradox was particularly devastating to Frege's logicist program, as it was discovered just as Frege was completing his foundational work.
