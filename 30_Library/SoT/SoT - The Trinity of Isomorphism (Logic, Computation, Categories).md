---
alias: ["Category Theory for Hackers", "Curry-Howard-Lambek", "Duality of Sums and Products", "Wadler's Trinity"]
aliases: []
confidence: 5/5
confidence-gaps: []
created: 2025-12-18T12:40:00Z
decay-signals: []
epistemic: authoritative
last_reviewed: 2025-12-18
modified: 2025-12-18T21:31:55Z
purpose: Defines the architectural duality between Sums and Products using Category Theory.
quality-markers: ["Synthesized from Philip Wadler's Categories for the Working Hacker"]
related-soTs: ["[[SoT - The Algebra of Types (Cardinality and Isomorphism)]]", "[[SoT - The Curry-Howard Correspondence (Propositions as Types)]]"]
resonance-score: 10
review_interval: 1 year
see_also: []
source_of_truth: true
status: stable
tags: ["architecture", "category_theory", "duality", "logic", "mathematics"]
title: SoT - The Trinity of Isomorphism (Logic, Computation, Categories)
type: SoT
uid:
updated:
---

## 1. Working Knowledge (Stable Foundation)

- **The Trinity (Curry-Howard-Lambek):** Three fields describe the exact same structure:
    1. **Logic:** Propositions & Proofs (Gentzen).
    2. **Computation:** Types & Functions (Church).
    3. **Categories:** Objects & Arrows (Eilenberg/Mac Lane).
- **The Architectural Insight:** Data structures are defined by their **arrows** (relationships), not their contents.
  - **Products (AND):** Defined by arrows pointing **OUT** (Projections: `fst`, `snd`).
  - **Sums (OR):** Defined by arrows pointing **IN** (Injections: `Left`, `Right`).
- **Duality:** If you reverse the arrows of a Product, you get a Sum. The logic of construction is the mirror image of the logic of destruction.

## 2. Current Understanding (Coherent Narrative)

### The Category Abstraction

A Category is the simplest possible structure: Objects (Types) and Arrows (Functions).

- **Composition:** If $f: A \to B$ and $g: B \to C$, then $g \circ f: A \to C$.
- **Identity:** $id: A \to A$.

### Products vs. Sums (The Dual Shapes)

Wadler visualizes the "Shape" of data:

1. **Product ($A \times B$):** A "Source" object that can project to A and B. It is the essence of **Conjunction** ($A \land B$).
    - *Code:* `struct Point { x: Int, y: Int }`. You extract `x` and `y`.
2. **Sum ($A + B$):** A "Target" object that A and B can inject into. It is the essence of **Disjunction** ($A \lor B$).
    - *Code:* `enum Result { Ok(T), Err(E) }`. You construct it from `Ok` or `Err`.

### Functions as Exponentials

A function $A \to B$ is an object $B^A$.

- **Algebraic Proof:** $C^{A+B} \cong C^A \times C^B$.
- *Translation:* A function taking a Sum (`Either A B -> C`) is isomorphic to a Pair of functions (`(A -> C, B -> C)`).
- *Application:* This is the mathematical proof that a `case` statement (pattern match) must handle all branches to be valid.

## 3. Understanding Layers (Progressive Abstraction)

- **Layer 1 (The Hacker):** "Sums are Enums, Products are Structs."
- **Layer 2 (The Architect):** "Sums and Products are duals. If I design an API with inputs (Arrows In), I should consider the dual output structure (Arrows Out)."
- **Layer 3 (The Theorist):** "Logic, Code, and Categories are the same thing. I can use intuition from one to solve problems in the other."

## 4. Minimum Viable Understanding (MVU)

- **Trinity:** Logic = Code = Categories.
- **Duals:** Sums and Products are mirror images.
- **Candle in the Dark:** Using a language with Sum types (Rust/Haskell) gives you mathematical guidance. Using one without (Java/Go) leaves you "groping in the dark."

## 5. Tensions, Gaps, and Cross-SoT Coherence

- **Reinforcement:** This note provides the *Categorical* view of the concepts in [[SoT - The Algebra of Types (Cardinality and Isomorphism)]].
  - *Algebra:* $A + B$.
  - *Category:* Arrows pointing IN.
  - *Logic:* $A \lor B$.

## 6. Sources and Links

- **Source:** Philip Wadler, *Categories for the Working Hacker* (YouTube).
