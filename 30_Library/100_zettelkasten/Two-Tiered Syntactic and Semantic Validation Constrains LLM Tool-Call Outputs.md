---
created: 2026-07-28T14:20:04+00:00
epistemic_status: medium
modified: 2026-08-08T10:29:26+00:00
permalink: llmeon/30-library/100-zettelkasten/two-tiered-syntactic-and-semantic-validation-constrains-llm-tool-call-outputs
tags: [domain/llm, topic/agent-architecture, topic/formal-methods]
title: Two-Tiered Syntactic and Semantic Validation Constrains LLM Tool-Call Outputs
type: claim
---

## Two-Tiered Syntactic and Semantic Validation Constrains LLM Tool-Call Outputs

A type checker and a business-rules engine catch different classes of error, and an LLM agent's tool calls need both. The first tier is syntactic: a library like Pydantic strictly enforces that the LLM's output actually has the shape it's supposed to—the right fields, the right types—before anything downstream even looks at what the values mean. This catches malformed output, but it can't catch output that's syntactically valid and semantically wrong.

That's the second tier's job. Semantic validation uses a formal ontology—OWL (Web Ontology Language) and RDFS (RDF Schema)—to encode business logic as logical constraints on a knowledge graph, and check the LLM's intended action against it. Two specific constraint types do most of the work: disjoint properties assert that two categories can never overlap, so an ontology can mechanically reject an agent trying to assign a payout property to something that's also typed as a support-representative entity, because "payout recipient" and "support representative" have been declared disjoint. Functional properties assert that a relationship can only take one value at a time, so an ontology can mechanically reject a second refund-issuance action once one refund relationship already holds for that transaction—not because a rule says "don't do this twice," but because the logic of the property itself makes a second value impossible to assert without contradiction.

### Scope & Conditions

Applies as the concrete implementation layer for the broader neuro-symbolic gate architecture—syntactic validation alone is necessary but not sufficient, since well-typed output can still violate business logic; semantic validation alone is impractical without syntactic validation first filtering out malformed requests before they reach the more expensive ontology check. Requires the domain's business rules to be expressible as disjointness and cardinality constraints in a formal ontology—not all business logic reduces cleanly to these forms.

### Evidence

Source: user-pasted summary of a presentation on neuro-symbolic AI architecture for agentic systems (title/channel/URL not provided in the summary). "Syntactic Validation: Utilising libraries like Pydantic (in Python) to strictly enforce data types before the LLM's output is processed. Semantic Validation: Utilising Web Ontology Language (OWL) and Resource Description Framework Schema (RDFS) to enforce business logic. For example, using 'disjoint properties' to ensure an LLM cannot assign a payout to a support representative instead of a customer, or using 'functional properties' to prevent an agent from issuing a second refund when only one is logically permissible."

### Implications

- It's the concrete mechanism behind the vault's neuro-symbolic gate architecture claim: [[Neuro-Symbolic Guardrails Intercept and Validate Tool-Call Requests Against a Formal Ontology Before Execution]] names the architectural pattern (intercept, then validate against a formal ontology); this note names the specific two-tier technical implementation that makes that interception actually enforceable.
- It depends on the vault's ontology-sourcing recommendation to be practical at scale: [[Ground New Agent Ontologies in Established Semantic Web Taxonomies Rather Than Building From Scratch]] argues for reusing existing taxonomies rather than authoring one from zero; this note's semantic tier is only as tractable as the ontology it validates against, so the two claims are directly complementary.
- It's a different validation substrate from the vault's existing structural/testing discipline notes: [[Classic Engineering Discipline Is More Necessary, Not Less, as a Countermeasure to AI-Generated Slop]] and [[Production-Stage Behavioral Testing and Fast Feedback Loops Are the Engineering Discipline AI-Generated Code Demands]] validate code structure and runtime behaviour respectively; this note validates a single tool-call request's logical permissibility against domain rules—a narrower, more immediate check than either.

### Related

- [[Neuro-Symbolic Guardrails Intercept and Validate Tool-Call Requests Against a Formal Ontology Before Execution]]—implements: this note's two-tier mechanism is the concrete technical realisation of that note's architectural pattern.
- [[Ground New Agent Ontologies in Established Semantic Web Taxonomies Rather Than Building From Scratch]]—depends_on: the semantic tier's practicality depends on having a usable ontology to validate against.

### See Also

- [[Agentic Loops Gain Turing-Complete Instability From Chained Reasoning and Tool Use]]

%%[implements:: [[Neuro-Symbolic Guardrails Intercept and Validate Tool-Call Requests Against a Formal Ontology Before Execution]], strength=3, confidence=medium]%%

%%[depends_on:: [[Ground New Agent Ontologies in Established Semantic Web Taxonomies Rather Than Building From Scratch]], strength=2, confidence=medium]%%
