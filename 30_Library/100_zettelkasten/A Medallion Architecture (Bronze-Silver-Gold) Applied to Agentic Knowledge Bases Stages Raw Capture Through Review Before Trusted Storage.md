---
title: A Medallion Architecture (Bronze-Silver-Gold) Applied to Agentic Knowledge Bases Stages Raw Capture Through Review Before Trusted Storage
type: concept
status: seed
prodos.kind: atomic
prodos.lifecycle: seed
source_title: Shared Memory Layer for Agentic AI
source_url: unknown — see [[tmp_atoms_shared-memory-agentic-ai]]
created_utc: '2026-09-14T00:00:00Z'
confidence: high
tags:
- domain/llm
- topic/agent-architecture
- topic/knowledge-graph
- domain/pkm
upstream: '[[tmp_atoms_shared-memory-agentic-ai]]'
conformant: true
permalink: llmeon/30-library/100-zettelkasten/a-medallion-architecture-bronze-silver-gold-applied-to-agentic-knowledge-bases-stages-raw-capture-through-review-before-trusted-storage
---

### A Medallion Architecture (Bronze/Silver/Gold) Applied to Agentic Knowledge Bases Stages Raw Capture Through Review Before Trusted Storage

Borrowed from enterprise data engineering, a medallion architecture applied to an agent-maintained knowledge base separates raw, immutable source capture (bronze — transcripts, articles, clippings) from agent-generated review proposals awaiting human approval (silver — suggested edits, link creations, extractions) from the approved, interlinked trusted knowledge base itself (gold — the wiki).

#### Scope & Conditions

Specifically a response to the risk that an autonomous agent writing directly to a persistent knowledge base can introduce memory poisoning, hallucinations, and false contradictions.

#### Evidence

> "Bronze (Raw): Ingestion of raw, immutable source materials... Silver (Review/Trust Layer): The agent parses the raw data and generates 'review proposals'... rather than modifying the wiki directly... Gold (Wiki): The approved, interlinked markdown files that form the trusted semantic knowledge base."

#### Implications

- An agent that can write review proposals but never commit them directly to the gold layer cannot poison the trusted knowledge base, regardless of how confidently wrong a given proposal is.

#### Related

- [[SoT - Agentic AI Design Patterns]]—extends: a specific, named staging pattern for the knowledge-write case that SoT's general routing/chaining patterns don't cover.
- [[Transactional Belief Commit Prevents an Agent's Unverified Write From Immediately Becoming Actionable Truth]]—shared mechanism: the general staging principle this architecture is a concrete instance of.