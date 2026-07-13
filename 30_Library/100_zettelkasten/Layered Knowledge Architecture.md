---
created: 2026-04-14T20:38:44+00:00
created_utc: '2026-04-14T14:00:00Z'
kind: distinction
modified: 2026-07-13T08:52:28+00:00
permalink: llmeon/30-library/100-zettelkasten/layered-knowledge-architecture
source_title: Hermes Agent and Karpathy’s LLM Wiki
source_url: https://youtu.be/Mb5N08xcxtg
status: seed
tags: [data-integrity, design-patterns, system-architecture]
title: Layered Knowledge Architecture
type: atom
upstream: '[[SoT - LLM Wiki Pattern]]'
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

- [[SoT - LLM Wiki Pattern]]—direct concept match: defines the three-layer architecture.
- [[SoT - ProdOS Note Metadata (Frontmatter)]]—shared mechanism: metadata (frontmatter) is a component of the schema layer.

### See Also

- [[Harness Engineering]]
