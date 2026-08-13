---
aliases: [Model Theory, Proof Theory, Set Theory Basics, Subfields of Logic]
conformant: false
created: 2026-01-12T10:20:00+00:00
modified: 2026-08-13T10:53:41+00:00
non_conformance_reason: "Bulk inferred type. Needs review."
permalink: llmeon/30-library/so-t/so-t-core-fields-of-mathematical-logic
source_of_truth: true
tags: [foundation, math/logic, math/set-theory, prodos/sot]
title: SoT - Core Fields of Mathematical Logic
type: sot
---

## Minimum Viable Understanding (MVU)

Mathematical Logic is the study of formal systems, providing the "grammar" and "raw material" for all mathematics. It is subdivided into three core disciplines: Set Theory (The Objects), Proof Theory (The Deductive Machinery), and Model Theory (The Relationship between Language and Reality).

---

## 1. Set Theory (The "Raw Material")

Set theory is the foundational language of modern mathematics. Every mathematical object (numbers, functions, manifolds) can be constructed as a set.

- Foundational Framework: [[Axiomatic Set Theory Is a Foundational Framework for Mathematics]].
- The Standard: ZFC (Zermelo-Fraenkel with Choice). It provides the rules for set-forming operations to avoid contradictions.
- The Tension: [[Russell's Paradox in Naive Set Theory]] demonstrated that "the set of all sets that don't contain themselves" is a contradiction, necessitating the shift from naive grouping to axiomatic rigor.
- Key Axiom: [[Set Theory Requires Distinct Objects]]—the assumption that mathematical objects can be uniquely identified.

---

## 2. Proof Theory (The "Machinery")

Proof theory treats mathematical proofs as formal geometric or computational objects.

- Focus: Analyzes the structure of arguments, provability strength, and the consistency of systems.
- Computational Link: [[SoT - The Curry-Howard Correspondence (Propositions as Types)]] reveals that a mathematical proof is structurally identical to a computer program.
- Practical Application: [[SoT - Mathematical Proof Techniques]] (Direct, Induction, Contradiction).
- Philosophical Goal: Once the heart of Formalism (Hilbert's Programme), which aimed to prove the consistency of all mathematics using finitary methods.

---

## 3. Model Theory (Syntax vs. Semantics)

Model theory studies the relationship between Formal Languages (the formulas we write) and Mathematical Structures (the "worlds" where those formulas are true).

- The Inquiry: What structures satisfy a given set of axioms? (e.g., "Which sets of objects behave like a Group?").
- Syntax: The strings of symbols (e.g., $\forall x, y: x+y = y+x$).
- Semantics: The interpretation in a specific domain (e.g., Integers vs. Real Numbers).
- Core Result: Gödel's Completeness Theorem states that for first-order logic, a formula is provable if and only if it is true in every model.

---

## 4. Tensions & Gaps: The Incompleteness Barrier

The dream of a "perfectly closed" logical system was shattered by Kurt Gödel.

- The Limit: Gödel's Incompleteness Theorems prove that any consistent system powerful enough for arithmetic will contain true statements that cannot be proven within that system.
- History: See [[SoT - History of Mathematical Logic]] for the evolution from Aristotle to the Foundational Crisis.
- Grammar: For the basic symbols ($\forall, \exists, \implies$), see [[SoT - Fundamentals of Mathematical Logic]].

---

## Related Knowledge

- Mathematics MOC: [[MOC - What is Maths]].
- Computer Science: [[MOC - Computer Science Foundations]].
- Order Theory: [[SoT - Order Theory & Lattices]] (A bridge between Sets and Types).
- Type Theory: [[MOC - Type Theory]].
