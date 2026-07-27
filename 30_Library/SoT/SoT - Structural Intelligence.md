---
aliases: [AST-Based Retrieval, Deterministic Code Graph, Structural Intelligence]
conformant: false
created: 2026-01-30T10:00:00+00:00
modified: 2026-07-27T16:01:00+00:00
non_conformance_reason: "Bulk inferred type. Needs review."
permalink: llmeon/30-library/so-t/so-t-structural-intelligence
tags: [architecture, ast, graph-theory, retrieval, tooling]
title: SoT - Structural Intelligence
type: sot
---

## Structural Intelligence

Structural Intelligence is the paradigm of treating code as a Deterministic Graph rather than a probabilistic bag of tokens. It relies on Abstract Syntax Trees (ASTs) and Control Flow Graphs (CFGs) to provide the "Ground Truth" schema that LLMs lack.

### The Retrieval Hierarchy

We define four tiers of code retrieval, moving from static text to dynamic causality:

| Tier | Mechanism | Strengths | Weaknesses |
|:--- |:--- |:--- |:--- |
| 1. The Bash Scout | `grep`, `find`, `ls` | Temporal Reality (Real-time), Negative Space (Proving absence). | "Stringly" typed. Misses semantic relationships. |
| 2. Vector RAG | Embeddings | Vibe Check (Concept matching), Natural Language queries. | Hallucination. Cannot prove "Who calls X?". Stale indexes. |
| 3. Structural (AST) | Tree-sitter, LSP | Deterministic Truth. 100% precision on "Call Graph" and "Type Hierarchy". | Static. Does not capture runtime execution flow. |
| 4. Causal (CFG) | Control Flow Graph | Reasoning. Simulates execution paths (If/Else, Loops). Tracks side effects. | Computationally expensive. Hard to serialize for prompts. |

### The "Cartographer" Protocol

To solve the "Context Window" bottleneck at Tier 4, we use The Cartographer.

- Role: Graph Pruner.
- Logic: instead of dumping the full CFG, it injects a Dependency Subgraph.
- Metric: Impact Radius. Only include nodes within 1-2 degrees of separation from the active code.

### The Mechanism: AST as Schema

The Abstract Syntax Tree transforms code from text into data:

- Program Node: The Root / Schema Definition.
- VariableDeclaration: A row in a table.
- CallExpression: An Edge in the graph.

> [!important] The Reliability Gap
> Benchmarks show that AST-derived graphs provide 100% node coverage and deterministic construction. LLM-based extraction is probabilistic, slow, and expensive (20x-45x cost).

### Implementation: The "RepoMap"

Tools like Aider and Tree-sitter use this to create RepoMaps: compressed skeletons of the codebase that fit into the context window.

- Context Slicing: Instead of reading a file, the agent reads the _Signature_ of the function.
- Refactoring Robustness: Tracking entities by structure, not line numbers.

### Why It Matters

For an LLM to possess [[SoT - Dimensions of Code Understanding|Structural Understanding]], it must be fed the Graph, not just the Text. This prevents [[SoT - Context Rot]] by grounding the model in the immutable reality of the compiler.

---
%%[synthesizes:: [[SoT - Context Rot]]]%%
%%[synthesizes:: [[SoT - Macro-Micro Unification]]]%%
%%[synthesizes:: [[SoT - The Context Engine]]]%%

See Also: [[SoT - Dimensions of Code Understanding]], [[SoT - Macro-Micro Unification]], [[SoT - Context Rot]], [[SoT - The Context Engine]]
