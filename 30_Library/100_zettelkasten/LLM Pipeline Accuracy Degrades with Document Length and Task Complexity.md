---
created: 2026-07-28T00:00:00+00:00
epistemic_status: high
modified: 2026-08-29T09:36:02+00:00
permalink: llmeon/30-library/100-zettelkasten/llm-pipeline-accuracy-degrades-with-document-length-and-task-complexity
proposition: Naive LLM pipelines that apply a fixed prompt across documents fail as
  document length and task complexity increase. Transformers hallucinate details in
  long contexts and omit buried information. Aggregation of multiple extractions fails
  silently when the same entity is represented inconsistently across outputs.
tags: [domain/llm, topic/context-management, topic/data-processing, topic/pipelines, topic/reliability]
title: LLM Pipeline Accuracy Degrades with Document Length and Task Complexity
type: claim
---

## LLM Pipeline Accuracy Degrades with Document Length and Task Complexity

A simple LLM pipeline: "Extract [X] from document [D]." Apply it to a single document, and it works. Apply it to ten documents and aggregate the results, and structural failures emerge.

Problem 1: Context degradation in long documents. A transformer's attention mechanism becomes unreliable past a certain context length. Information buried in the middle or end of a long document is hallucinated, omitted, or contradicted.

Problem 2: Silent aggregation failures. An LLM extracts "Officer Smith," "J. Smith," and "Sergeant James Smith" from three documents. A naive aggregation treats them as three separate entities. The pipeline produces incomplete output without signaling that it failed.

### Scope & Conditions

Affects any data extraction pipeline where:

1. Documents exceed the LLM's reliable context window
2. Results from multiple document processes must be aggregated
3. The same entity may be referenced inconsistently across documents

### Evidence

Source: "Paper Dives: MapReduce Is Back - And It Fixes Broken LLM Pipelines | DocETL" (Nerdy Dives). Quote: "Many current frameworks for LLM-powered data processing treat a prompt as fixed and apply it across all documents to extract information. However, this approach fails as document length and task complexity increase" [00:13].

Example: "if an LLM extracts 'Officer Smith,' 'J. Smith,' and 'Sergeant James Smith,' a standard pipeline might treat them as three separate entities, resulting in incomplete outputs" [01:31].

### Implications

- Accuracy cliff: Performance doesn't degrade gracefully; it falls off suddenly past certain document lengths or task complexity thresholds.
- Silent failures: The pipeline completes without errors; the output is simply wrong or incomplete.
- Scaling penalty: Attempting to improve coverage (longer documents, more complex tasks) backfires.

### Related

- [[Context Window Limits Force Iterative Task Decomposition]]—related: context is one cause of the failure.
- [[LLM Hallucinations Arise from Probabilistic Prediction Without External Grounding]]—consequence: hallucinations emerge in long contexts.
- [[Entity Canonicalization via LLM-Guided Resolution]]—solution: formalized entity matching prevents aggregation failures.
- [[DocETL Framework - Declarative Pipelines with Agentic Optimization]]—solution: structured decomposition solves both problems.

### See Also

- [[SoT - LLM Pipeline Architecture]]

%%[depends_on:: [[Context Window Limits Force Iterative Task Decomposition]], strength=4, confidence=high]%%

%%[depends_on:: [[LLM Hallucinations Arise from Probabilistic Prediction Without External Grounding]], strength=4, confidence=high]%%
