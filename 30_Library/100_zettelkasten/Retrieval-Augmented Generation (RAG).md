---
created: 2026-04-13T14:41:15+00:00
created_utc: 2026-04-13 11:20:00+00:00
kind: mechanism
modified: 2026-07-13T08:52:30+00:00
permalink: llmeon/30-library/100-zettelkasten/retrieval-augmented-generation-rag
source_title: AI Agent Architecture and the Modern Tech Stack
source_url: https://gemini.google.com/app/509937047bd0b955
status: seed
tags: [data-retrieval, grounding, llm, rag]
title: Retrieval-Augmented Generation (RAG)
type: atom
upstream: '[[HEAD The Failure of Human-Centric Design]]'
---

## Retrieval-Augmented Generation (RAG)

Retrieval-Augmented Generation (RAG) is an architectural pattern that dynamically injects relevant data from external sources into an LLM's prompt at inference time. This grounds the model's response in verifiable, current, or proprietary information without the need for expensive fine-tuning.

### Scope & Conditions

Used to connect static models to external knowledge bases. It requires a retrieval mechanism (often semantic search) and a prompt template that integrates retrieved data.

### Evidence

> "A pipeline that queries a vector database for relevant information and dynamically injects it into the LLM's prompt… without the need to fine-tune."

### Implications

- Connects static models to real-time or proprietary data.
- Reduces hallucinations by providing verifiable source material.

### Related

- [[Semantic Search via Embeddings]]—shared mechanism: RAG relies on embeddings for the retrieval phase.
- [[SoT - LLM Wiki Pattern]]—extends: the LLM Wiki is described as a stateful evolution of the RAG pattern.
- [[SoT - Agentic AI Design Patterns]]—direct concept match: RAG is identified as a core retrieval pattern for agents.
