---
aliases: [Russell's Paradox]
confidence: 0.9
created: 2025-11-01T11:22:13Z
epistemic: fact
last_reviewed: 2025-11-01
modified: 2025-11-01T11:35:54Z
purpose: "Explain Russell's Paradox and its consequences for set theory foundations."
review_interval: 90
see_also: ["[[Axiomatic Set Theory Is a Foundational Framework for Mathematics]]", "[[Logicism (Mathematics as Extension of Logic)]]"]
source_of_truth: ["/Volumes/DAL/Zettelkasten/LLMeon/200_projects/Maths/What is maths.md"]
status: seedling
tags: [foundations, paradox, set-theory, topic/maths]
title: "Russell's Paradox in Naive Set Theory"
type: concept
uid: 2025-11-01T11:22:13Z
updated: 2025-11-01T11:22:13Z
version: 1
---

**Summary:** Russell's Paradox (1901) exposed a fundamental contradiction in naive set theory by constructing the set of all sets that do not contain themselves, demonstrating that unrestricted set comprehension leads to logical inconsistency.

**The Paradox:**

Consider the set R = {x | x ∉ x}, the set of all sets that do not contain themselves as members. Does R contain itself?

- If R ∈ R, then by definition R ∉ R (contradiction)
- If R ∉ R, then by definition R ∈ R (contradiction)

**Consequence:**

This paradox revealed that the naive comprehension principle—that any definable collection forms a set—is logically flawed. It forced a complete reconstruction of set theory with explicit axioms that avoid such contradictions, leading to modern axiomatic set theories like ZF and ZFC.

**Impact:** The paradox was particularly devastating to Frege's logicist program, as it was discovered just as Frege was completing his foundational work.
