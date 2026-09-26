---
conformant: true
created: 2026-04-14T20:38:44+00:00
created_utc: '2026-04-14T14:00:00Z'
definition: A structured AI memory system is divided into three distinct layers, namely immutable raw sources, the AI-synthesised wiki and the governing schema configuration, so that every synthesised insight can be traced back to unalterable evidence and the structure can be changed by updating the schema layer alone.
distinguishes_from: []
kind: distinction
modified: 2026-09-25T16:29:26+00:00
non_conformance_reason: ""
permalink: llmeon/30-library/100-zettelkasten/layered-knowledge-architecture
source_title: Hermes Agent and Karpathy’s LLM Wiki
source_url: https://youtu.be/Mb5N08xcxtg
status: seed
tags: [data-integrity, design-patterns, system-architecture, topic/knowledge-architecture]
title: Layered Knowledge Architecture
type: concept
upstream: '[[SoT - LLM Wiki Pattern]]'
used_in_claims: []
---

## Layered Knowledge Architecture

A structured AI memory system is divided into three distinct layers: immutable Raw Sources, the AI-synthesised Wiki, and the governing Schema configuration. This separation ensures that every synthesised insight can be traced back to unalterable evidence while allowing the overall knowledge structure to be modified by updating the schema layer alone.

### Scope & Conditions

Essential for maintaining data integrity and structural flexibility in persistent AI memory systems.

### Evidence

> "The workflow is divided into three distinct layers… Raw Sources (Immutable)… The Wiki (AI-generated markdown)… The Schema (rulebook/configuration)."

### Implications

- Ensures that AI synthesis remains grounded in verifiable source material.
- Allows for global changes to the wiki's structure and conventions without the need to re-process individual source documents.

### Related

- [[SoT - LLM Wiki Pattern]]—direct concept match: defines the three-layer architecture. [extends:: [[SoT - LLM Wiki Pattern]]]
- [[SoT - ProdOS Frontmatter Contract (Note Type Schemas)]]—shared mechanism: metadata (frontmatter) is a component of the schema layer.
- [[LLM Wiki Concept]]—shared mechanism: defines the persistent, agent-maintained wiki whose layer structure this note describes.
- [[Immutability Principle - Preserve Original Notes]]—shared mechanism: the same rule at note level, where originals stay as written and changes go into new linked notes, just as raw sources stay unaltered beneath the wiki.
- [[A Medallion Architecture (Bronze-Silver-Gold) Applied to Agentic Knowledge Bases Stages Raw Capture Through Review Before Trusted Storage]]—shared mechanism: another layered design with an immutable raw base and a trusted top layer, adding a human-review stage between them.
- [[Persistent Memory Layers Enable Multi-Session Agent Continuity]]—extends: the agent-continuity case for keeping a persistent layer that outlives any one session.
- [[Agent Feedback Loops Require Bidirectional Memory Writes]]—shared mechanism: agents need write access to memory, which fits a design where the AI writes to the wiki layer while the raw layer stays immutable.
- [[Canonical Schema V1]]—shared mechanism: a concrete frontmatter template, one instance of a schema layer.
- [[Knowledge Linting]]—extends: periodic health checks over the wiki layer for stale information, orphan pages and contradictions.
- [[Multi-Page Ingestion Impact]]—extends: how a single source ingestion propagates through several pages of the wiki layer.

### See Also

- [[Harness Engineering]]

### Update (2026-09-21)

- Per [[AGENTS]], the three-layer memory system (raw, wiki, output and a log) that was once embedded in this vault moved to a standalone Hermes vault on 2026-07-30. This vault is now the human zettelkasten.

### Maps

- [[MOC - AI Software Engineering]]—_Lists the parent SoT under "The LLM Wiki Pattern"; it does not yet list this note._
