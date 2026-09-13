---
conformant: true
created: 2026-09-13T09:35:26+00:00
created_utc: '2026-09-13T00:00:00Z'
modified: 2026-09-13T09:36:16+00:00
permalink: llmeon/00-inbox/equating-semantic-similarity-with-knowledge-is-a-pkm-anti-pattern
source_title: A Portable Interest and PKM Knowledge Graph
source_url: UNKNOWN
status: seed
tags: [anti-pattern, epistemics, pkm, semantic-search]
title: Equating Semantic Similarity with Knowledge Is a PKM Anti-Pattern
type: claim
upstream: '[[PKM Meta-Graph System Research]]'
---

## Equating Semantic Similarity with Knowledge Is a PKM Anti-Pattern

Treating embedding-based semantic similarity between notes as if it were an authored, meaningful relationship is an anti-pattern; similarity search can retrieve candidate connections, but only an authored predicate plus rationale creates a durable assertion about how two ideas actually relate.

### Scope & Conditions

Applies specifically to systems that use vector/semantic search (e.g. RAG-style retrieval) as an input to graph construction.

### Evidence

> "Equating semantic similarity with knowledge: Similarity retrieves candidates; an authored predicate plus rationale creates a durable assertion."

### Implications

- Semantic search should nominate candidate links for human (or LLM-with-review) confirmation, never write a link directly on the basis of similarity alone.
- An LLM agent proposing edges should be required to state confidence and rationale, and a human/reviewer must confirm before the edge is committed.

### Related

- [[SoT - Canonical Interest Tags]]—applies to: Archilles' `search_annotations`/`search_books_with_citations` tools (documented there) are exactly this kind of similarity-based retrieval; this note is the caution for how their results should be used—as candidates, not as committed edges.
