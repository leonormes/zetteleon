---
created: 2026-02-06T09:00:00+00:00
last-synthesis: 2026-02-06
modified: 2026-07-13T08:52:50+00:00
permalink: llmeon/30-library/so-t/so-t-llm-codebase-understanding-hierarchy
source_of_truth: true
tags: [concept/code-analysis, concept/code-representation, concept/context-management, domain/llm-architecture, llm, type/SoT]
title: SoT - LLM Codebase Understanding & Hierarchy
type: sot
conformant: false
non_conformance_reason: "Bulk inferred type. Needs review."
---

## Minimum Viable Understanding (MVU)

"Codebase Understanding" for an LLM is defined as the successful isomorphism between a repository's Static Analysis Graph (RIG) and the model's transient attention state. It is not a cognitive act but a probabilistic one: reducing the entropy of the prompt by encoding relationships as explicit structure (AST/RIG), thereby forcing token alignment with architectural constraints.

## Working Knowledge

### 1. The Hierarchy of Representations

To bridge the gap between "Code-as-Text" (Files) and "Code-as-System" (Logic), we layer representations:

- A. The Tree (AST): The structured schema for a single file. Transforms unstructured text into a local Knowledge Graph, enabling deterministic retrieval of grammatical structures.
- B. The Graph (CFG): Maps control flow (loops, branches) within a function. Essential for calculating cyclomatic complexity.
- C. The Network (RIG/CPG): The "God View" connecting ASTs via system-wide relationships (`calls`, `inherits_from`, `imports`). Represents the deterministic, evidence-backed architectural map.
- D. The Semantic Graph: Distorts "geography" (file location) to show "topology" (logic/data flow). Minimizes syntactic noise to maximize semantic signal.

### 2. Operational Strategies for Context

- The "Linker's View": LLMs operate most efficiently on flattened token streams. Treating the codebase as a continuous logic stream (imports as wires, files as arbitrary containers) minimizes symbol resolution overhead and optimizes Signal-to-Noise Ratio (SNR).
- Skeletonization (Symbol Tables): Separates the "Machine Contract" (Signatures/Types) from the "Human Description" (Docstrings). Feeding this skeleton reduces perplexity by defining the negotiation without implementation noise.
- Data Lineage: For stateful systems, static graphs are insufficient. We must track the data flow ("Path of the Mouse") to represent meaning through transformation rather than location.
- Literate Context: Ordering code by narrative intent (Literate Programming) rather than compilation order allows the model to process "Summary Chunks" first, establishing architectural priors before processing implementation details.
- Meta-Context (The Superego): Injecting a "Domain Manifesto" prevents "Perspective Drift" (regression to the mean of training data) by enforcing architecturally valid patterns and strict boundaries.
- Ubiquitous Language (Vector Anchoring): Using consistent, domain-specific terminology (e.g., `SkuVariant` vs `Item`) anchors the LLM's latent space to the correct conceptual region.

### 3. Mechanistic Rigor & Definitions

To prevent "hallucination" (statistical noise), we must define understanding mechanistically:

- Contextual Fidelity: An LLM "understands" only what fits in its context window. "Understanding" is a function of the probability distribution sharpness; standard patterns are sharp, "magic" (implicit) frameworks are entropic.
- Symbol Resolution: True understanding requires tracing definitions. If a symbol's definition is absent, the model hallucinates.
- The "Thinking" Fallacy: Models do not "think" or "prefer." A model "understands" a function signature not because it reflects, but because the signature's presence statistically constrains the set of probable next tokens to those matching the return type.

### 4. The Challenge of Context Rot & Recursive Exploration

Simply increasing context windows (e.g., 1M tokens) is insufficient due to Context Rot (Primacy/Recency Bias and Attention Dilution from distractors). The solution is Recursive Exploration:

- Recursive Language Models (RLMs): Move from linear reading to a recursive loop of `Graph Navigation` (Cheap) -> `Vector/Text Inspection` (Expensive).
- The Hybrid Loop: The agent queries the graph for structure first, then loads _only_ the specific node's text into the context window, minimizing noise. See [[SoT - Recursive Language Models]].

### 5. AI-Native Code Standards

Code should be written for agents (Model Parseability) to maximize correct inference:

1. Explicitness over Magic: Avoid implicit frameworks. Explicit imports anchor the model.
2. Strong Typing as Anchors: Types restrict the search space for the next token.
3. Atomic Context Units: Functions should fit in a single retrieval chunk (<40 lines).
4. Comments as System Prompts: Docstrings should define _Invariants_ and _Intent_.

### 6. The Cartographer Strategy

The Cartographer is an agent role that acts as a Graph Pruner to manage "Attention Dilution":

- Dependency Subgraphs: Instead of dumping the whole CFG, inject only nodes within 1-2 degrees of separation ("Impact Radius").
- Graph Integrity: Enforces checking of upstream/downstream edges before modification.

## Related Knowledge

- Foundational Physics: This hierarchy relies on [[SoT - Complexity Conservation]]. We move complexity from dynamic logic (code) to static representation (RIG) to lower the energy required for the LLM to reason correctly.
- Complexity Law: See [[SoT - LLM Reasoning Obeys the Complexity Conservation Law]].
- Failure Modes: See [[SoT - Parochial Code]] for why LLMs fail without global context.
