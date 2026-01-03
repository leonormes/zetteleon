---
aliases: []
confidence: "5/5"
created: 2025-12-18T00:00:00Z
epistemic: "authoritative"
last_reviewed: "2025-12-18"
modified: 2026-01-03T10:18:57+00:00
purpose: "Defines Robert Harper's Computational Type Theory, emphasizing that types are defined by program behavior (semantics) rather than syntax."
review_interval: "1 year"
see_also: ["[[SoT - Cubical Type Theory (Computational Univalence)]]", "[[SoT - The Curry-Howard Correspondence (Propositions as Types)]]"]
source_of_truth: []
status: "stable"
tags: ["architecture", "computational_logic", "semantics", "type_theory"]
title: SoT - Computational Type Theory (Meaning as Use)
type: "SoT"
uid: 
updated: 
---

## 1. Working Knowledge (Stable Foundation)

- **Core Thesis:** Types are defined by **program behavior** (how they run), not by static syntax rules.
- **Meaning is Use:** To understand a type is to understand:

    1. **Introduction:** What are its canonical values? (e.g., `true`, `false`)
    2. **Elimination:** How do we use them? (e.g., `if-then-else`)
    3. **Computation:** How do these interactions reduce? (e.g., `if true then A else B` reduces to `A`).

- **The Syntax Gap:** Formal syntax (what the compiler checks) is merely a "pale approximation" of semantic truth. We use it because semantic truth is often undecidable.

## 2. Current Understanding (Coherent Narrative)

### Core Framework: Computational Semantics

Harper argues that truth is primary. A type is a **Partial Equivalence Relation (PER)** over computations.

- **Membership:** To say $M

in au$ is to say "M evaluates to a canonical value of type $ au$."

- **Equality:** Two terms are equal if they evaluate to equal values.

### The Standard Library of Logic

- **Booleans:** Defined by the `if` construct (binary decision). The branches "know" the path taken ($x=true$ in the 'then' branch).
- **Natural Numbers:** Defined as the **strongest** (smallest) predicate satisfying `Zero` and `Successor`. This ensures **induction** works. If it were weaker, it might include infinite recursion (stacks of successors that never end).
- **Function Types ($ o$):** Defined by **Extensionality**. Two functions are equal if they produce equal outputs for all equal inputs.

### The Fact of Choice

In this constructive setting, the **Axiom of Choice** is not an axiom but a theorem.

- **Logic:** $orall x

exists y. R(x, y)

implies

exists f orall x. R(x, f(x))$.

- **Proof:** Because the existential quantifier $

Sigma$ contains the witness ($y$) in its data structure, a proof of "For all x there exists y" *is* a program that computes y from x. The function $f$ is simply extracting that witness.

## 3. Understanding Layers (Progressive Abstraction)

- **Layer 1 (The Mantra):** "Types are defined by their introduction and elimination rules."
- **Layer 2 (The mechanism):** Verification is working backwards from values ("Head Expansion").
- **Layer 3 (The Philosophy):** Logic is not the foundation of math; computation is the foundation of logic.

## 4. Minimum Viable Understanding (MVU)

- **Type = Behavior:** A type is a contract about how a program executes.
- **Syntax < Semantics:** The rules we write down (syntax) are just an imperfect attempt to capture the reality of how code runs (semantics).
- **Constructive Choice:** If you prove something exists, you have computed it.

## 5. Tensions, Gaps, and Cross-SoT Coherence

- **Tension:** **Decidability vs. Expressiveness.**
  - **Semantic View:** "If they run the same, they are the same." (True, but hard to check).
  - **Formal View:** "I need to check this in milliseconds." (Fast, but rejects some valid programs).
  - *See [[SoT - Equality in Type Theory (Intensional vs Extensional)]] for the deep dive on this conflict.*

## 6. Sources and Links

- **Source:** Robert Harper, *Computational Type Theory* (Lectures 1-4).
- **Source:** Robert Harper, *OPLSS 2018: Computational Type Theory* (Lecture 1) - Establishes "Types as Specifications of Program Behavior" vs. Formalism.
