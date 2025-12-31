---
aliases: ["Simple Made Easy", "Complecting", "Rich Hickey Simplicity"]
confidence: 5/5
created: 2025-12-31T00:00:00Z
epistemic: architecture
last_reviewed: 2025-12-31
modified: 2025-12-31T12:20:46+00:00
purpose: "To define the rigorous distinction between Simple and Easy in software architecture."
review_interval: 1 year
see_also: ["[[SoT - Data-Centric Software Engineering]]", "[[SoT - Information Hiding (Parnas)]]"]
source_of_truth: true
status: stable
tags: [architecture, simplicity, clojure, rich-hickey, design-patterns]
title: SoT - Simple Made Easy (Rich Hickey)
type: SoT
uid:
updated:
---

## 1. Definitive Statement

> [!definition] The Core Philosophy
> **Simplicity is an objective property of a system, describing a lack of interleaving.**
>
> Developers systematically conflate **Simple** (unentangled) with **Easy** (familiar/near-at-hand). We must prioritize Simplicity (the artifact's maintainability) over Ease (the developer's immediate convenience), or we will build "complected" systems that are impossible to reason about.

---

## 2. Core Conceptual Framework

### 2.1 Simple vs. Easy

Hickey draws a sharp etymological and practical distinction:

| Term | Etymology | Definition | Nature |
|:--- |:--- |:--- |:--- |
| **Simple** | *Simplex* (One fold) | A lack of interleaving. A component has one role, one task, or one concept. | **Objective.** You can observe if two things are tied together. |
| **Easy** | *Adjacent* (Lying near) | "Near to hand" (familiar tool) or "Near to grasp" (familiar concept). | **Relative.** Depends on the observer's skill and context. |

**The Architect's Trap:** We prioritize *Easy* (fast compile loops, magic frameworks, familiar syntax) at the cost of *Simple*. This creates systems that are quick to start but eventually collapse under their own complexity.

### 2.2 Complecting (The Mechanism of Complexity)

**Complect** (v): To braid or weave together.

* **Complexity** is defined by the number of **interconnections**, not the number of components.
* When you complect two concepts (e.g., *Logic* and *Time*), you cannot change one without analyzing the other.
* This creates a **Combinatorial Burden**. Since human working memory is limited (the "juggling" analogy), complected systems rapidly exceed our ability to reason about them.

---

## 3. Architectural Strategy: Disentanglement

To architect robust systems, replace "Complex" (Braided) constructs with "Simple" (Orthogonal) ones.

| Complex (Braided) | Simple (Disentangled) | The Complexity (Why?) |
|:--- |:--- |:--- |
| **State / Objects** | **Values** | Objects complect **Value** with **Time** (mutation). Values are immutable facts. |
| **Methods** | **Functions** | Methods complect **Behavior** with **State/Class Taxonomy**. |
| **Inheritance** | **Polymorphism (Protocols)** | Inheritance complects **Type Definition** with **Implementation Details**. |
| **Syntax** | **Data** | Syntax is opaque and specific; Data is generic and manipulatable. |
| **Loops** | **Set Functions / Declarative** | Loops complect **What** is done with **How** (iteration mechanics). |
| **Actors** | **Queues** | Actors complect **What** happens with **Who** does it. |
| **ORM** | **Declarative Data (SQL)** | ORMs complect **Domain Logic** with **Database Representation**. |
| **Conditionals** | **Rules** | Hardcoded `if/else` complects **Logic** with **Program Flow**. |

---

## 4. The "How-To" of Simplicity

1. **Abstract Correctly:** Abstraction is not "hiding details"; it is "drawing away" from physical implementation.
2. **Separate Concerns:** Rigorously separate the **Who, What, When, Where, Why,** and **How**.
    * *Example:* If Module A calls Module B directly, you have complected *What* (logic) with *When* (now) and *Where* (Module B's location). Introducing a Queue separates these concerns.
3. **Data First:** Prefer generic data structures (maps, sets, vectors) over specialized classes. Data is transparent; objects are opaque.
4. **Value Immutability:** State (mutation) is the primary source of complexity. Isolate it rigidly.

> **Summary:** Simplicity is a choice. It often looks "harder" (less Easy) initially because it requires understanding underlying components rather than relying on "magic" frameworks. But it is the only path to long-term velocity.
