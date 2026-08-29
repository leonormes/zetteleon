---
created: 2026-07-28T00:00:00+00:00
epistemic_status: high
modified: 2026-08-29T09:36:05+00:00
permalink: llmeon/30-library/100-zettelkasten/sequential-processing-with-working-memory-folding-operator
proposition: The Folding operator processes batches of documents sequentially, carrying
  'a "scratchpad" of working memory forward between iterations. This enables the LLM'
  to build cumulative understanding and refer back to prior documents, improving consistency
  and accuracy across a corpus.
tags: [domain/llm, topic/data-processing, topic/memory, topic/pipelines, topic/sequential-processing]
title: Sequential Processing with Working Memory (Folding Operator)
type: claim
---

## Sequential Processing with Working Memory (Folding Operator)

Traditional map-reduce processes documents in isolation: "extract from document 1," "extract from document 2," etc. The LLM has no memory of prior documents.

Folding changes this: Process documents sequentially, carrying a working memory (scratchpad) forward. Document 2's extraction can refer to findings from Document 1. Document 3 can build on conclusions from Documents 1 and 2.

### Scope & Conditions

Effective for:

- Extracting information where patterns or coherence across documents matter
- Building cumulative understanding from a corpus
- Tasks requiring deduplication or consistency checking across multiple sources

Less useful for:

- Independent document processing where cross-document context adds noise
- Tasks where per-document isolation is required (e.g., privacy-sensitive extraction)

### Evidence

Source: "Paper Dives: MapReduce Is Back - And It Fixes Broken LLM Pipelines | DocETL" (Nerdy Dives). Quote: "Folding: Instead of purely splitting a document, folding feeds batches of documents sequentially, carrying a 'scratchpad' of working memory forward" [04:49].

### Implications

- Sequential processing cost: Documents must be processed in order; parallelization is limited.
- Memory management: The scratchpad must be maintained and updated; size management is critical.
- Cumulative context: Errors or hallucinations in early documents can propagate to later ones.

### Related

- [[Persistent Memory Layers Enable Multi-Session Agent Continuity]]—analogous: carries state forward across processing steps.
- [[Agent Feedback Loops Require Bidirectional Memory Writes]]—related: scratchpad enables feedback and learning across iterations.
- [[DocETL Framework - Declarative Pipelines with Agentic Optimization]]—implements: Folding is a core DocETL operator.
- [[Entity Canonicalization via LLM-Guided Resolution]]—related: folding enables consistent entity identification across documents.

### See Also

- [[SoT - Stateful Pipelines in LLM Systems]]

%%[implements:: [[Persistent Memory Layers Enable Multi-Session Agent Continuity]], strength=3, confidence=medium]%%
