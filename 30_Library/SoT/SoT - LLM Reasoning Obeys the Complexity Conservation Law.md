---
aliases: [LLM Reasoning Efficiency is Proportional to Structural Constraint]
conformant: false
created: 2026-01-31T00:00:00+00:00
modified: 2026-08-29T09:36:39+00:00
non_conformance_reason: "Bulk inferred type. Needs review."
permalink: llmeon/30-library/so-t/so-t-llm-reasoning-obeys-the-complexity-conservation-law
tags: [complexity, llm-understanding, prompt-engineering]
title: SoT - LLM Reasoning Obeys the Complexity Conservation Law
type: sot
---

## The Core Insight

> LLMs fail not because they lack intelligence, but because we force them to reason over Procedural Entropy instead of Structural Constraint.

## 1. The LLM Corollary to Tesler's Law

If software complexity is conserved, then an LLM must process that complexity to produce valid output.

- Procedural Processing: Forcing the LLM to read 1,000 lines of messy `if/else` code to "understand" a business rule. This leads to Attention Dilution and high Perplexity.
- Structural Processing: Providing the LLM with a 10-line Skeleton (Types + Signatures + Docstrings). The LLM processes the complexity via Topological Mapping.

## 2. Information Density vs. Entropy

- Raw Code (High Entropy): Low information density. The model must "compute" the intent from the syntax. Every semicolon is noise that distracts the attention mechanism.
- Information Structures (Low Entropy): High information density. The intent is explicit. By providing "Information" (context), we are narrowing the search space of the next likely token.

## 3. Mechanics of Constraint

Reliability is achieved by biasing the context to render invalid states statistically improbable using deterministic invariants:

1. Types & Signatures: Constrain the _mechanics_.
2. Ubiquitous Language: Anchors the _latent space_ (Vector Anchoring).
3. Negative Constraints: Prune entire branches of the probability tree (The "Sniper Shot").
4. Domain Manifesto: Sets the "Laws of Physics" for the task, preventing conceptual hallucinations.

## 4. Why "Context Stuffing" Fails

Context stuffing (linear reading) treats code as Geography. The LLM gets lost in the "streets" (lines of code).

Recursive exploration (RLM) treats code as Topology. The LLM follows the "lines" (data flow/edges) of the Semantic Graph.

Conclusion: To minimize tokens and maximize accuracy, we must perform the "Data -> Information" conversion _before_ sending the prompt. We provide the "Skeleton" so the model doesn't have to perform the "Surgery" of understanding on its own.

## 5. The Law in LLM Context

Large Language Models do not fail due to a lack of "intelligence" in the traditional sense; they fail when forced to reason over procedural entropy instead of structural constraint. LLMs are essentially statistical traversers of symbolic space—High-Performance at mapping structure to implication (e.g., traversing a graph or following a schema), but Low-Performance at simulating long execution traces or tracking hidden mutable state.

If [[Software Complexity is Conserved Between Control Flow and Representation|Complexity is Conserved]], providing an LLM with raw, unstructured code forces it to _reconstruct_ the underlying data model mentally while simultaneously trying to solve the problem. This "double burden" leads to:

1. Hallucination: The model fills in missing structural gaps with plausible but incorrect guesses.
2. Context Rot: High token counts of procedural detail dilute the model's attention on core constraints.

### Strategic Shift

To maximize LLM leverage, engineers must shift from Prompt Engineering (trying to explain the "how") to Structural Engineering (providing the "what").

- Context stuffing is a category error. Larger context windows often worsen reasoning if the contents are procedural rather than structural.
- MVC (Minimum Viable Context) is the required boundary to prevent these failures.
