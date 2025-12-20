---
aliases: [Deforestation, Fusion, Stream Fusion]
confidence: 4/5
confidence-gaps: [build/foldr) are highly technical., The specific compiler transformations (e.g.]
created: 2025-12-19T13:14:01Z
decay-signals: []
epistemic: concept
last_reviewed: 2025-12-19
modified: 2025-12-20T09:54:05Z
purpose: "To define Function Fusion as a high-level, algebraic optimization technique that eliminates intermediate data structures."
quality-markers: [Contrasts high-level fusion with low-level LLVM optimization., Provides a clear map/filter example]
related-soTs: []
resonance-score: 7
review_interval: 24 months
see_also: []
source_of_truth: true
status: stable
supersedes: []
tags: ["compilers", "functional-programming", "optimization"]
title: SoT - Optimization via Function Fusion
type: SoT
uid: 
updated:
---

## 1. Definitive Statement

> [!definition] Definition
> **Function Fusion** (also known as *deforestation* or *stream fusion*) is a compile-time optimization technique used in functional programming that transforms a sequence of operations on a data structure into a single, unified operation. It eliminates the need to create and populate intermediate data structures, drastically reducing memory allocation and improving performance.

---

## 2. The Core Problem: The Waste of Intermediate Collections

In modern data processing, it is common to chain together operations like `map`, `filter`, and `reduce`. While this approach is highly readable and declarative, a naive implementation is incredibly inefficient.

**The Naive (Un-fused) Process:**
Consider the operation: `numbers.map(x => x * 2).filter(x => x > 10)`

1. `map(x => x * 2)` runs. It iterates through the original `numbers` list and allocates a **new, intermediate list** to store the results.
2. `filter(x => x > 10)` runs. It iterates through the **intermediate list** and allocates a **second new list** to store the final filtered results.

| Failure Mode | The Problem | The Fusion Solution |
| :--- | :--- | :--- |
| **Memory Bloat** | Each step in the chain allocates a full intermediate collection. For large datasets, this can lead to massive, temporary memory usage. | **No Intermediate Allocation:** Fusion combines the operations so that only a single, final collection is ever created. |
| **Cache Inefficiency** | Iterating over multiple, separate collections one after another leads to poor data locality and frequent CPU cache misses. | **Single-Pass Processing:** The fused operation processes each element through the entire chain of logic in a single pass, maximizing data locality. |
| **Redundant Iteration** | The program iterates N times for N operations in the chain, doing far more work than necessary. | **One Loop to Rule Them All:** The compiler rewrites the chain of high-level functions into a single, optimized `for` loop under the hood. |

---

## 3. The Architecture: Algebraic Transformation

Fusion works because of the strong mathematical (algebraic) properties of functional constructs. The compiler can "look at" the chain of functions and, instead of executing them one by one, rewrite them based on proven rules.

**Conceptual Transformation:**

- **Original Code:** `collection.map(f).filter(g)`
- **Compiler's Thought Process:**
    1. The `map` produces a list. The `filter` consumes a list.
    2. I can combine these. Instead of building the whole list from `map`, I can compute one element, immediately pass it to `filter`'s logic, and only then decide if it should go into the final list.
- **Fused (Rewritten) Code:**

    ```sh
    let results = [];
    for item in collection {
        let mapped_item = f(item); // Perform map's logic
        if g(mapped_item) {       // Perform filter's logic
            results.push(mapped_item);
        }
    }
    ```

### The Critique of LLVM-Based Optimization

Languages like Rust, which lack the powerful higher-kinded abstractions needed for true fusion, often rely on the LLVM compiler backend to perform similar optimizations.

- **The Rust Deficit:** Rust's iterators are a pragmatic solution, but they are just "syntax sugar" over loops. The compiler doesn't perform high-level algebraic fusion.
- **The LLVM "Hope":** The Rust compiler generates a large amount of complex, un-optimized code from the iterator chain and "hopes" that the LLVM optimizer is smart enough to see the pattern and boil it down to a single loop.
- **The Argument:** Critics argue this is less reliable and less efficient than the guaranteed, high-level transformations of a language designed for fusion (like Haskell with its `build/foldr` rules). It's cleaning up a mess at a low level rather than avoiding the mess at a high level.

---

## 5. Minimum Viable Understanding (MVU)

1. **Chaining functions like `map` and `filter` is clean but naively slow because it creates temporary lists at each step.**
2. **Fusion is a compiler trick that combines the entire chain into one single, efficient loop.**
3. **This avoids creating the temporary lists, saving memory and speeding up execution.**
4. **True functional languages do this at a high, algebraic level, which is considered more powerful than relying on a low-level optimizer like LLVM to clean up the mess afterwards.**

---

## 6. Open Questions & Tensions

- **Tension:** **Compiler Complexity.** Implementing a robust fusion system in a compiler is extremely complex and depends on the language having a very regular, mathematical structure (e.g., everything being an expression, strong referential transparency).
- **Tension:** **Predictability.** While powerful, the exact conditions under which fusion will trigger can sometimes feel like a "black box" to the developer, making performance analysis less predictable than in a more explicit, low-level model.

## 7. Related Components

- [[SoT - Pragmatism vs Rigour in Software]]
