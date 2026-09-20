---
conformant: true
created: 2026-09-14T12:09:49+00:00
created_utc: '2026-09-14T00:00:00Z'
modified: 2026-09-19T15:44:36+00:00
permalink: llmeon/30-library/100-zettelkasten/graph-rag-offers-local-global-and-drift-search-modalities-over-a-knowledge-graph
source_title: PKM Meta-Graph System Research
source_url: https://microsoft.github.io/graphrag/
status: seed
tags: [domain/llm, domain/pkm, topic/agent-architecture, topic/knowledge-graph]
title: GraphRAG Offers Local, Global, and Drift Search Modalities Over a Knowledge Graph
type: concept
upstream: '[[PKM Meta-Graph System Research]]'
---

## GraphRAG Offers Local, Global, and Drift Search Modalities Over a Knowledge Graph

GraphRAG (Microsoft Research) answers different question types over a knowledge graph through three distinct search modes: local search, which fans out from specific entities to their immediate neighbours for a deep dive on a sub-topic; global search, which reasons across the whole corpus using pre-generated community summaries for broad thematic questions; and drift search, which fans out to neighbours while also drawing on global community context.

### Scope & Conditions

Contrasted with baseline RAG, which retrieves isolated text chunks by vector similarity alone and therefore struggles to "connect the dots" across disparate information.

### Evidence

> "Local Search | Reasons about specific entities by fanning out to their immediate neighbors… | Global Search | Reasons about holistic questions across the entire corpus by leveraging the pre-generated community summaries… | DRIFT Search | Fanning out to neighbors but with the added context of global community information."

### Implications

- Gives a vocabulary for choosing retrieval strategy by question type—a narrow factual question wants local search, a "what themes run across my notes" question wants global search—rather than using one retrieval mode for everything.

### Related

- [[Retrieval-Augmented Generation (RAG) Grounds LLM Outputs in External Knowledge]]—extends: GraphRAG's three search modes are a graph-structured refinement of baseline RAG's single vector-similarity retrieval.
- [[Text Network Analysis Reveals Community Structure and Structural Gaps in a Corpus]]—extends: GraphRAG's community summaries (used by global/drift search) are built from exactly the community-detection step this note describes.
