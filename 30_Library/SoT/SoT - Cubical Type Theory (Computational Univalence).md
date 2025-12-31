---
aliases: ["Computational Univalence", "Cubical Type Theory", "Higher Dimensional Types"]
confidence: "5/5"
created: 2025-12-18T00:00:00Z
epistemic: "authoritative"
last_reviewed: "2025-12-18"
modified: 2025-12-31T23:08:35+00:00
purpose: "Explains the architectural solution to the \\\"Computational Content of Univalence\\\" problem in Type Theory."
review_interval: "1 year"
see_also: ["[[SoT - Computational Type Theory (Meaning as Use)]]", "[[SoT - Equality in Type Theory (Intensional vs Extensional)]]"]
source_of_truth: []
status: "stable"
tags: ["architecture", "cubical", "hott", "mathematics", "type_theory"]
title: SoT - Cubical Type Theory (Computational Univalence)
type: "SoT"
uid: 
updated: 
---

## 1. Working Knowledge (Stable Foundation)

- **The Goal:** To make **Univalence** (treating isomorphic types as equal) *computable*.
- **The Problem it Solves:** In standard Homotopy Type Theory (HoTT), Univalence is an Axiom. Axioms don't compute; they act as "walls" that stop a program from reducing (breaking Canonicity).
- **The Solution:** **Cubical Type Theory**. It refactors the very environment of the logic to include **Dimensions** (Intervals), allowing the compiler to "trace" paths between types and execute them as programs.

## 2. Current Understanding (Coherent Narrative)

### The "Ninja Move": Changing the Environment

Instead of adding new rules for terms (which failed), Harper explains that we must generalize the context.

- **Standard Context:** $\Gamma \vdash M: A$ (Terms depend on Variables).
- **Cubical Context:** $\Gamma, i, j \vdash M: A$ (Terms depend on Variables AND **Dimension Variables**).

### The Geometry of Types

- **Point:** A term with 0 dimensions.
- **Line (Path):** A term depending on 1 dimension ($i$). This represents equality.
- **Square:** A term depending on 2 dimensions ($i, j$). This represents equality between equalities.
- **Cube:** 3 dimensions, and so on.

### The Mechanism: Coercion (`coe`)

This is the engine that makes Univalence run.

- **Definition:** `coe` moves a term from the "start" of a line to the "end".
- **Application:** If you have a Path between Type A and Type B (an isomorphism), `coe` effectively "runs" the transformation.
  - *Example:* If Path is `swap`, `coe` actually swaps the data.
  - *Result:* We no longer need an axiom. The path *is* the program.

### Kan Composition (`com`)

To ensure these 3D shapes hold together (e.g., that we can combine paths transitively), the system enforces the **Kan Condition**.

- **Algorithm:** It ensures that any "open box" of lines or squares can be strictly filled. This guarantees that all the groupoid laws (associativity, identity, inverse) hold computationally.

## 3. Understanding Layers (Progressive Abstraction)

- **Layer 1 (The Fix):** Cubical TT fixes the "bug" in HoTT where programs using Univalence would crash or hang.
- **Layer 2 (The Shift):** Equality is no longer a static "Fact" ($1=1$); it is a **dynamic process** (a line from A to B) that we can traverse.
- **Layer 3 (The Implementation):** We use Dimension Variables ($i \in [0,1]$) to implement this traversal.

## 4. Minimum Viable Understanding (MVU)

- **Axioms Break Code:** Adding "Univalence" as a rule without code behind it breaks the compiler.
- **Cubical Fixes Code:** It provides the "code" (Coercion & Dimensions) that runs underneath the Univalence principle.
- **Result:** You can write programs that treat Isomorphic structures as identical, and they will actually run.

## 5. Tensions, Gaps, and Cross-SoT Coherence

- **Complexity:** The "Cartesian" Cubical theory simplifies things, but the math is still incredibly dense compared to standard type theory.
- **Adoption:** This is cutting-edge (Agda supports it with `--cubical`), not yet in mainstream languages like Rust or Swift.

## 6. Sources and Links

- **Source:** Robert Harper, *Computational Type Theory* (Lecture 5).
