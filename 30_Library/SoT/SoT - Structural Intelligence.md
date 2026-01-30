---
aliases: [Structural Intelligence, Deterministic Code Graph, AST-Based Retrieval]
tags: [architecture, retrieval, tooling, ast, graph-theory]
created: 2026-01-30T10:00:00+00:00
modified: 2026-01-30T10:45:00+00:00
---

# Structural Intelligence

**Structural Intelligence** is the paradigm of treating code as a **Deterministic Graph** rather than a probabilistic bag of tokens. It relies on Abstract Syntax Trees (ASTs) to provide the "Ground Truth" schema that LLMs lack.

## The Retrieval Hierarchy

We define three tiers of code retrieval, each with specific strengths and weaknesses:

| Tier | Mechanism | Strengths | Weaknesses |
| :--- | :--- | :--- | :--- |
| **1. The Bash Scout** | `grep`, `find`, `ls` | **Temporal Reality** (Real-time), **Negative Space** (Proving absence). | "Stringly" typed. Misses semantic relationships (e.g., `impl` blocks). |
| **2. Vector RAG** | Embeddings | **Vibe Check** (Concept matching), Natural Language queries. | **Hallucination.** Cannot prove "Who calls X?". Stale indexes. |
| **3. Structural (AST)** | Tree-sitter, LSP | **Deterministic Truth.** 100% precision on "Call Graph" and "Type Hierarchy". | Higher setup cost. Requires language support. |

## The Core Thesis: Graph > Vector

*   **Probabilistic Vector (RAG):** Code is a semantic cloud. Good for "How do I...?", bad for "Who calls X?".
*   **Deterministic Graph (AST):** Code is a precise schema. `Node A --calls--> Node B`. This is **Truth**.

## The Mechanism: AST as Schema

The Abstract Syntax Tree transforms code from text into data:
*   **Program Node:** The Root / Schema Definition.
*   **VariableDeclaration:** A row in a table.
*   **CallExpression:** An Edge in the graph.

> [!important] The Reliability Gap
> Benchmarks show that AST-derived graphs provide **100% node coverage** and deterministic construction. LLM-based extraction is probabilistic, slow, and expensive (20x-45x cost).

## Implementation: The "RepoMap"

Tools like **Aider** and **Tree-sitter** use this to create **RepoMaps**: compressed skeletons of the codebase that fit into the context window.
*   **Context Slicing:** Instead of reading a file, the agent reads the *Signature* of the function.
*   **Refactoring Robustness:** Tracking entities by structure, not line numbers.

## Why It Matters

For an LLM to possess [[SoT - Dimensions of Code Understanding|Structural Understanding]], it must be fed the **Graph**, not just the **Text**. This prevents [[SoT - Context Rot]] by grounding the model in the immutable reality of the compiler.

---
**See Also:** [[SoT - Dimensions of Code Understanding]], [[SoT - Macro-Micro Unification]]
