---
aliases: [Code Duplication, DRY Principle, Refactoring Duplication, Types of Duplication]
confidence: 5/5
confidence-gaps: []
created: 2025-12-12T17:30:00Z
epistemic: technical
last-synthesis: 2025-12-12
last_reviewed: 2025-12-12
modified: 2025-12-13T08:57:45Z
purpose: Canonical definition and analysis of code duplication, its types, and the principles of refactoring to improve software design.
quality-markers: []
related-soTs: ["[[SoT - Atomicity and Loose Coupling]]", "[[SoT - Information Hiding (Parnas)]]"]
resonance-score: 9
review_interval: 1 year
see_also: ["[[MOC - Software Architecture Principles]]", "[[SoT - The Functional Anatomy of a Computer]]"]
source_of_truth: true
status: stable
supersedes: ["[[kent beck lists multiple types of duplication that]]"]
tags: [code-quality, design-principles, refactoring, software-engineering, sot]
title: SoT - Code Duplication and Refactoring
type: SoT
uid:
updated:
---

## 1. Definitive Statement

> [!definition] Code Duplication
> **Code Duplication** refers to the presence of identical or very similar code segments in multiple places within a software system. While sometimes seemingly harmless, it is a primary indicator of poor design, leading to increased maintenance costs, reduced flexibility, and a higher probability of introducing bugs.
>
> **Refactoring** duplication is the process of restructuring code to eliminate these redundancies, thereby improving code clarity, maintainability, and overall design quality.

---

## 2. Kent Beck's Types of Duplication

Kent Beck, a pioneer in agile software development, identifies several categories of duplication that warrant refactoring:

### A. Duplicated Logic
-   **Description:** The same expression or logical sequence appears in multiple code locations.
-   **Example:** Identical `if/else` or `switch` blocks for the same conditional logic across different functions.

### B. Data Duplication
-   **Description:** The same literal values or data structures appear redundantly across code or tests.
-   **Example:** A `TAX_RATE` constant defined in multiple files, or a hard-coded URL used repeatedly.

### C. Structural Duplication
-   **Description:** Similar code structures are repeated, even if specific data or operations differ slightly. Often points to missing abstraction.
-   **Example:** Multiple classes with identical method signatures and similar internal logic, differing only in the data they operate on (e.g., `Rectangle` and `Circle` classes with `area()` methods having similar structure but different calculations).

### D. Algorithmic Duplication
-   **Description:** The same underlying algorithm is implemented in different ways or with minor variations.
-   **Example:** Two different functions calculating the sum of an array, one with a `for` loop and another with `reduce()`.

### E. Temporal Duplication
-   **Description:** Code whose meaning or correctness is highly dependent on the *order* or *timing* of operations, rather than clear logical flow. Often indicates a long, complex function where steps are implicitly linked in time.
-   **Indicators:** Long methods, code taking a long time to comprehend, unclear variable purposes.
-   **Refactoring:** Renaming, extracting methods, applying "Compose Method" pattern.

### F. Duplication Between Tests and Implementation
-   **Description:** When test code too closely mirrors implementation details, or uses hard-coded values also present in production code. A critical focus in Test-Driven Development (TDD).
-   **Problem:** Makes tests brittle and masks incomplete or overly simplistic implementations.
-   **Refactoring (TDD Cycle):** Start simple, replace constants with variables, then refactor to generalize.

---

## 3. The Rainsberger and Parnas Perspective

### J. B. Rainsberger on Mastery
-   **Core Claim:** "If you master removing duplication and fixing bad names, then I claim you master object-oriented design."
-   **Scope:** Duplication extends beyond lines of code to include duplicated logic, data, and design decisions.
-   **Benefit:** Removing duplication improves organization and reveals underlying design principles. It is the second of his "Elements of Simple Design."

### David Parnas: Information Hiding
-   **Core Principle:** Design modules to encapsulate and **hide** difficult or likely-to-change design decisions from other modules.
-   **Goal:** Create abstract interfaces that expose *only* necessary information.
-   **Impact:** Enables independent development, localizes impact of changes, and improves system comprehensibility.

---

## 4. Benefits of Eliminating Duplication

-   **Improved Maintainability:** Changes only need to be made in one place.
-   **Reduced Errors:** Fewer chances to introduce bugs due to inconsistent changes.
-   **Enhanced Readability:** Clearer, more concise code.
-   **Better Design:** Forces the creation of higher-level abstractions and more modular components.
-   **Increased Flexibility:** Easier to modify and extend the system.

---

## 5. ProdOS Integration

The principles of eliminating duplication directly map to effective knowledge management:

-   **[[SoT - Atomicity and Loose Coupling]]**: Each atomic note should contain a single idea, avoiding "duplicated logic" or "data duplication" across notes.
-   **[[SoT - Information Hiding (Parnas)]]**: SoTs act as "modules" that encapsulate complex topics, exposing their definitive statements and core mechanisms via clear structures and explicit links, hiding the underlying "design decisions" (original Zettels, research).
-   **"Don't Repeat Yourself" (DRY) for Knowledge:** Avoid summarizing the same concept in multiple places. Instead, link to the canonical SoT.
