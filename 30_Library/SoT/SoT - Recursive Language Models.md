---
created: 2026-07-27T17:29:18+00:00
modified: 2026-08-29T09:36:42+00:00
permalink: llmeon/30-library/so-t/so-t-recursive-language-models
title: SoT - Recursive Language Models
type: note
---

## SoT - Recursive Language Models

A Source of Truth note on Recursive Language Models—models that apply language model inference recursively, either over their own outputs or over structured intermediate representations, to handle tasks requiring multi-hop reasoning.

Recursive language models are distinguished from single-pass inference by their ability to chain reasoning steps, revisit intermediate conclusions, and integrate outputs across multiple inference passes. This makes them better suited for tasks requiring logical composition, multi-step deduction, or reasoning over structured knowledge graphs, where flat semantic similarity retrieval is insufficient.

Key claim: RAG is "brittle for multi-hop reasoning because it relies on semantic similarity rather than logical relationships." Querying raw retrieval is structurally flawed for tasks where the answer depends on a chain of inferences rather than a single nearest-neighbour lookup.

### Tensions

#### Long Context Vs Retrieval

This note argues that RAG is "brittle for multi-hop reasoning because it relies on semantic similarity rather than logical relationships" and that querying raw retrieval is structurally flawed. [[Retrieval-Augmented Generation (RAG)]] and the Qdrant notes treat retrieval as a working mechanism.

This is a scope tension, not a disagreement: single-hop factual lookup vs multi-hop reasoning have different optimal strategies. The RAG notes are definitional rather than advocacy, so the tension is about which regime applies to a given task, not which is correct.
