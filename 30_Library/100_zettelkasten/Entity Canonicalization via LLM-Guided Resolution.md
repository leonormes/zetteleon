---
created: 2026-07-28T00:00:00+00:00
epistemic_status: high
modified: 2026-08-29T09:36:00+00:00
permalink: llmeon/30-library/100-zettelkasten/entity-canonicalization-via-llm-guided-resolution
proposition: Entity canonicalization solves the problem of the same entity being represented
  with different string keys across multiple LLM outputs. The Resolve operator uses
  two prompts—one to determine if values refer to the same entity, and another to
  generate the canonical form—before aggregation.
tags: [domain/llm, topic/aggregation, topic/data-processing, topic/entity-resolution]
title: Entity Canonicalization via LLM-Guided Resolution
type: claim
---

## Entity Canonicalization via LLM-Guided Resolution

When an LLM extracts "Officer Smith," "J. Smith," and "Sergeant James Smith" from different documents, a naive aggregation treats them as three entities. The correct answer is that they refer to the same person.

The Resolve operator formalizes entity matching: Given a set of extracted values, it uses two LLM calls:

1. Matching call: "Do these values refer to the same entity?"
2. Canonicalization call: "What is the canonical form of this entity?"

The result is a deduplicated, canonicalized entity set.

### Scope & Conditions

Essential for:

- Extracting entities (names, addresses, organizations) that may be written inconsistently
- Aggregating results from multiple documents where the same entity may appear in different forms
- Preventing downstream incorrect joins or counts due to string mismatch

Less useful for:

- Fully structured data where entities are already standardized
- Tasks where no entity aggregation is needed

### Evidence

Source: "Paper Dives: MapReduce Is Back - And It Fixes Broken LLM Pipelines | DocETL" (Nerdy Dives). Quote: "Resolve: Handles entity canonicalization. It uses two prompts—one to determine if values refer to the same entity, and another to generate the canonical form. This fixes the issue of LLMs generating slightly different string keys for the same entity before they are aggregated" [03:37].

### Implications

- Double token cost for entity matching: Two LLM calls per resolution operation increases token consumption.
- Scalability challenge: Pairwise comparison of entities is O(n²) in the number of extracted entities.
- Quality depends on prompt clarity: The LLM's ability to recognize entity matches depends on how clearly the prompt specifies matching criteria.

### Related

- [[LLM Pipeline Accuracy Degrades with Document Length and Task Complexity]]—solves: fixes aggregation failures.
- [[DocETL Framework - Declarative Pipelines with Agentic Optimization]]—implements: Resolve is a core DocETL operator.
- [[Structured Output Enforcement (JSON Schema and Function Calling)]]—related: canonicalization should produce structured output.

### See Also

- [[SoT - Entity Resolution at Scale]]

[supports:: [[LLM Pipeline Accuracy Degrades with Document Length and Task Complexity]], strength=5, confidence=high]
