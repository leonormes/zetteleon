---
aliases: []
created: 2026-01-31T00:00:00+00:00
modified: 2026-07-13T08:52:50+00:00
permalink: llmeon/30-library/so-t/so-t-llm-reasoning-obeys-the-complexity-conservation-law
tags: [complexity, llm-understanding, prompt-engineering]
title: SoT - LLM Reasoning Obeys the Complexity Conservation Law
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
