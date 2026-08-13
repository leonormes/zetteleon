---
conformant: true
created: 2026-07-28T00:00:00+00:00
epistemic_status: high
modified: 2026-08-13T10:54:47+00:00
permalink: llmeon/30-library/100-zettelkasten/gleaning-secondary-validation-to-catch-silent-omissions
prodos.kind: atomic
prodos.lifecycle: stable
proposition: Gleaning is a verification technique where a secondary "validator" prompt checks the LLM's initial output for quiet omissions. If something is missed, the validator flags it and the system refines the extraction without starting from scratch, preventing silent failures in LLM pipelines.
tags: [domain/llm, topic/hallucination-mitigation, topic/pipelines, topic/quality-gates, topic/verification]
title: Gleaning - Secondary Validation to Catch Silent Omissions
type: claim
---

## Gleaning - Secondary Validation to Catch Silent Omissions

An LLM extracts clauses from a contract. It outputs 35 clauses. The real document has 41 clauses; the LLM silently omitted 6. The pipeline completes without error. The output is incomplete.

Gleaning addresses this with a validator prompt: "Given the document and the initial extraction, are there any clauses that should have been extracted but weren't?"

If the validator finds omissions, it refines the extraction, re-querying the LLM or expanding the search space. The pipeline catches the miss before output is finalized.

### Scope & Conditions

Effective for:

- Extraction tasks where completeness is critical (contracts, regulations, specifications)
- Scenarios where an LLM might miss outliers or edge cases (rare clause types, unusual formatting)
- Tasks with clear criteria for inclusion/exclusion

Less useful for:

- Open-ended tasks where "completeness" is undefined
- Domains where false positives (over-inclusion) are worse than false negatives (omission)

### Evidence

Source: "Paper Dives: MapReduce Is Back - And It Fixes Broken LLM Pipelines | DocETL" (Nerdy Dives). Quote: "LLM-Specific Behaviors (Gleaning): The system uses a secondary 'validator' prompt to check the LLM's initial output for quiet omissions. If something is missed, it refines the extraction without starting from scratch" [07:54].

### Implications

- Double-pass cost: Gleaning adds a second LLM call (validator prompt) to every extraction.
- Risk of over-inclusion: An aggressive validator might flag false positives, requiring manual review.
- Modest gains: In benchmarks, gleaning often produces 5–15% recall improvements, depending on the domain.

### Related

- [[Model Self-Verification as a Secondary Quality Gate]]—analogous: verification pattern at the operator level.
- [[LLM Pipeline Accuracy Degrades with Document Length and Task Complexity]]—solves: catches silent failures.
- [[Error Handling and Retry Pipelines for LLM Failures]]—related: retry on validator feedback.
- [[DocETL Framework - Declarative Pipelines with Agentic Optimization]]—context: gleaning is an optimization directive in DocETL.

### See Also

- [[Precision-Recall Trade-offs in LLM Extraction]]

%%[supports:: [[LLM Pipeline Accuracy Degrades with Document Length and Task Complexity]]]%%

%%[supports:: [[Model Self-Verification as a Secondary Quality Gate]]]%%
