---
conformant: false
created: 2026-09-15T07:42:51+00:00
created_utc: '2026-09-14T00:00:00Z'
modified: 2026-09-26T08:45:25+00:00
non_conformance_reason: "missing schema field definition for type concept (required when conformant - true); missing schema field distinguishes_from for type concept (required when conformant - true); missing schema field used_in_claims for type concept (required when conformant - true)"
permalink: llmeon/30-library/100-zettelkasten/a-medallion-architecture-bronze-silver-gold-applied-to-agentic-knowledge-bases-stages-raw-capture-through-review-before-trusted-storage
prodos.kind: atomic
prodos.lifecycle: seed
source_title: Shared Memory Layer for Agentic AI
source_url: unknown — see [[tmp_atoms_shared-memory-agentic-ai]]
status: seed
tags: [domain/llm, domain/pkm, topic/agent-architecture, topic/knowledge-graph]
title: A Medallion Architecture (Bronze-Silver-Gold) Applied to Agentic Knowledge Bases Stages Raw Capture Through Review Before Trusted Storage
type: concept
upstream: '[[tmp_atoms_shared-memory-agentic-ai]]'
---

## A Medallion Architecture (Bronze/Silver/Gold) Applied to Agentic Knowledge Bases Stages Raw Capture Through Review Before Trusted Storage

Borrowed from enterprise data engineering, a medallion architecture applied to an agent-maintained knowledge base separates raw, immutable source capture (bronze—transcripts, articles, clippings) from agent-generated review proposals awaiting human approval (silver—suggested edits, link creations, extractions) from the approved, interlinked trusted knowledge base itself (gold—the wiki).

### Scope & Conditions

Specifically a response to the risk that an autonomous agent writing directly to a persistent knowledge base can introduce memory poisoning, hallucinations, and false contradictions.

### Evidence

> "Bronze (Raw): Ingestion of raw, immutable source materials… Silver (Review/Trust Layer): The agent parses the raw data and generates 'review proposals'… rather than modifying the wiki directly… Gold (Wiki): The approved, interlinked markdown files that form the trusted semantic knowledge base."

### Implications

- An agent that can write review proposals but never commit them directly to the gold layer cannot poison the trusted knowledge base, regardless of how confidently wrong a given proposal is.

[extends:: [[SoT - LLM Wiki Pattern]], strength=5, confidence=high]

### Resolves an Open Tension in This Vault's Own LLM Wiki Pattern

[[SoT - LLM Wiki Pattern]]—this vault's own canonical spec for exactly this kind of agent-maintained knowledge base—names the identical risk under its own "Tensions & Gaps" section, unresolved: _"Write authority: Giving the LLM full ownership of the wiki layer creates a risk of confident hallucinations being permanently encoded. The Schema/style-guide layer partially mitigates this but doesn't eliminate it. Human review gates on Ingest would add fidelity at the cost of friction."_ That SoT even links an open question—`[[HEAD - Should the LLM have write authority over the wiki layer?]]`—that appears never to have been written (the link is currently dangling).

The bronze/silver/gold split is close to a direct answer: it names the exact "human review gate on Ingest" that SoT gestures at without specifying, and reframes the friction/fidelity trade-off it worries about as a single design choice—friction is paid once, at the silver→gold promotion, not on every ingest. Since this vault's own `00_Inbox/ → 30_Library/` promotion workflow (raw capture → an agent's proposed atomic notes → this note, once reviewed) is already a lightweight, human-run instance of the same three-tier pattern, this atom is closer to a description of what this vault already does than a new proposal.

### Related

- [[SoT - Agentic AI Design Patterns]]—extends: a specific, named staging pattern for the knowledge-write case that SoT's general routing/chaining patterns don't cover.
- [[Transactional Belief Commit Prevents an Agent's Unverified Write From Immediately Becoming Actionable Truth]]—shared mechanism: the general staging principle this architecture is a concrete instance of.
- [[LLM Wiki Concept]]—extends: the atomic note for Karpathy's LLM Wiki pattern this vault already implements; this note supplies the write-authority safety mechanism that concept assumes but doesn't specify.
- [[SoT - Typed Answer Contract (TAC) for LLM Output]] and [[Protocol - Typed Answer Contract (TAC) for Vault Agents]]—shared mechanism: this vault's existing gate for trusting LLM _output_ (structure, confidence, citations) is the query-time twin of the silver-layer gate this note proposes for LLM _writes_.
- [[SoT - The RPI Workflow (Context Engineering)]]—extends: "Computed Truth" is this pattern's name for exactly what the gold layer is meant to contain—pre-synthesised, trusted knowledge rather than raw retrieval.
- [[Persistent Memory Layers Enable Multi-Session Agent Continuity]]—shared mechanism: the point of promoting anything to the gold layer is that it survives and compounds across sessions, which is what that note argues persistent memory is for.
