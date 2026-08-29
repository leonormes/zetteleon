---
created: 2026-07-28T00:00:00+00:00
epistemic_status: high
modified: 2026-08-29T09:36:00+00:00
permalink: llmeon/30-library/100-zettelkasten/doc-etl-framework-declarative-pipelines-with-agentic-optimization
proposition: DocETL is a framework that uses a declarative YAML interface to define
  LLM data pipelines combined with an agentic optimizer that searches for accurate,
  decomposed pipeline structures. Instead of fixing the prompt, DocETL restructures
  complex operations into sequences of simpler, more accurate steps, prioritizing
  accuracy over cost or latency.
tags: [domain/llm, topic/data-processing, topic/docetl, topic/optimization, topic/pipelines]
title: DocETL Framework - Declarative Pipelines with Agentic Optimization
type: claim
---

## DocETL Framework - Declarative Pipelines with Agentic Optimization

Rather than asking an LLM to solve a complex task in one pass, DocETL decomposes it into a pipeline of simpler operations: Map (extract from each document), Reduce (aggregate results), Filter (select), Resolve (canonicalize entities), Gather (repair context), Folding (sequential processing).

The framework uses a declarative YAML interface to specify the pipeline structure. Then an agentic optimizer explores alternative decompositions, measures output quality on real data, and selects the most accurate pipeline.

### Scope & Conditions

Effective for:

- Structured data extraction from document collections
- Tasks requiring aggregation or entity resolution
- Scenarios where accuracy is the primary metric (not cost or latency)

Requires:

- Ground truth labels or an LLM-based evaluator to measure quality
- Sufficient time for the optimizer to explore alternatives
- Decomposable tasks (not all problems decompose cleanly)

### Evidence

Source: "Paper Dives: MapReduce Is Back - And It Fixes Broken LLM Pipelines | DocETL" (Nerdy Dives). Quote: "Researchers from UC Berkeley and Columbia built DocETL to solve this. It's a declarative YAML interface for defining data pipelines combined with an agentic optimizer that focuses on maximizing accuracy instead of just minimizing cost or latency" [02:19].

### Core Contribution

The key insight is that pipeline structure matters more than model choice. By decomposing a 41-clause contract extraction into 21 independent focused maps, DocETL achieved 21.4% F1 improvement without changing the underlying LLM.

### Related

- [[LLM Pipeline Accuracy Degrades with Document Length and Task Complexity]]—solves: addresses naive pipeline failures.
- [[Task Decomposition and Iterative Refinement]]—implements: decomposes tasks into simpler steps.
- [[Evidence-Based Pipeline Optimization]]—implements: uses actual data to measure quality.
- [[Entity Canonicalization via LLM-Guided Resolution]]—implements: via Resolve operator.
- [[Context Repair via Document Chunking Augmentation]]—implements: via Gather operator.
- [[Sequential Processing with Working Memory (Folding)]]—implements: via Folding operator.

### See Also

- [[SoT - Declarative Data Pipeline Design]]
- [[Map-Reduce-Filter Patterns in LLM Systems]]

%%[supports:: [[LLM Pipeline Accuracy Degrades with Document Length and Task Complexity]], strength=5, confidence=high]%%
