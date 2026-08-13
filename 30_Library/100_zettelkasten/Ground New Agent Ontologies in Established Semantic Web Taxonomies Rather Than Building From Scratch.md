---
created: 2026-07-28T14:20:04+00:00
epistemic_status: medium
modified: 2026-08-13T10:54:47+00:00
permalink: llmeon/30-library/100-zettelkasten/ground-new-agent-ontologies-in-established-semantic-web-taxonomies-rather-than-building-from-scratch
tags: [domain/llm, topic/agent-architecture, topic/formal-methods]
title: Ground New Agent Ontologies in Established Semantic Web Taxonomies Rather Than Building From Scratch
type: claim
---

## Ground New Agent Ontologies in Established Semantic Web Taxonomies Rather Than Building From Scratch

Building an ontology from a blank page is slow and easy to get wrong—the categories and relationships that seem obvious at design time rarely survive contact with real data. The alternative is to start from a semantic framework that already exists and has already been battle-tested across many domains: Schema.org, FOAF (Friend of a Friend), Dublin Core, and similar established taxonomies encode a large amount of general-purpose structure (people, organisations, relationships, documents, transactions) that most domains need in some form. Starting there means an organisation is only responsible for the genuinely domain-specific extensions, not for reinventing general semantic structure that's already been solved.

Two paths for extending the base taxonomy are named: top-down, where domain experts deliberately design the additional classes, properties, and constraints the business actually needs; and bottom-up, where structure is derived from ingesting the organisation's existing data and observing what relationships and categories are actually present. Neither is presented as strictly superior—they're complementary starting points depending on whether the domain knowledge or the raw data is more readily available.

### Scope & Conditions

Applies specifically to sourcing the ontology that a neuro-symbolic validation gate would check tool-call requests against. Doesn't address how to choose between top-down and bottom-up extension in a given case, or how to reconcile the two if used together—the source treats them as two available options without a decision procedure for picking one.

### Evidence

Source: user-pasted summary of a presentation on neuro-symbolic AI architecture for agentic systems (title/channel/URL not provided in the summary). "The speaker advises against building ontologies from scratch. Organisations should utilise established semantic frameworks (e.g., Schema.org, FOAF, Dublin Core) as foundational schemas for their knowledge graphs, either building upon them top-down via domain experts, or bottom-up via data ingestion." The source's own assessment notes this is "standard practice in traditional data engineering and knowledge management," not a novel recommendation.

### Implications

- It's a practical precondition for the vault's neuro-symbolic gate architecture to be adoptable at reasonable cost: [[Neuro-Symbolic Guardrails Intercept and Validate Tool-Call Requests Against a Formal Ontology Before Execution]] depends on having a formal ontology to validate against; this note lowers the practical barrier to having one by pointing at reusable starting points instead of a from-scratch build.
- It's the concrete resourcing strategy behind the vault's two-tier validation mechanism: [[Two-Tiered Syntactic and Semantic Validation Constrains LLM Tool-Call Outputs]]'s semantic tier needs an actual ontology encoding disjoint and functional properties; this note describes where that ontology should come from.

### Related

- [[Neuro-Symbolic Guardrails Intercept and Validate Tool-Call Requests Against a Formal Ontology Before Execution]]—supports: lowers the practical cost of adopting that note's architecture.
- [[Two-Tiered Syntactic and Semantic Validation Constrains LLM Tool-Call Outputs]]—related: names where the ontology that note's semantic tier validates against should be sourced from.

### See Also

- [[Agentic Loops Gain Turing-Complete Instability From Chained Reasoning and Tool Use]]

%%[supports:: [[Neuro-Symbolic Guardrails Intercept and Validate Tool-Call Requests Against a Formal Ontology Before Execution]], strength=2, confidence=medium]%%
