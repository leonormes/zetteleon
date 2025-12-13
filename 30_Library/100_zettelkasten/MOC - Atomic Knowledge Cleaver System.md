---
aliases: []
confidence:
created: 2025-10-31T08:21:00Z
criteria: Only atomic and evergreen notes. Must be directly referenced in the core narrative of knowledge cleaving.
epistemic:
exclusions: Synthesis (consolidating many notes into one), advanced query techniques, dataview automation, or vault administration.
last_reviewed:
modified: 2025-12-13T17:55:12Z
purpose:
review_interval:
scope: The complete system of atomic knowledge cleaving—how to deconstruct long hybrid notes into pure atomic facts and contextual structural maps.
see_also: []
source_of_truth: []
status:
tags: [zettelkasten]
title: MOC - Atomic Knowledge Cleaver System
type: map
uid: 2025-10-31T08:21:00Z
updated: 2025-10-31T08:21:00Z
---

The Atomic Knowledge Cleaver is a process and philosophy for maintaining a high-integrity personal knowledge base. It rests on a fundamental principle: [[SoT - Atomicity and Loose Coupling]] rel:: part-of. This binary category invariant prevents knowledge bases from becoming either isolated facts with no coherence or narratives with no verifiable building blocks.

## The Core System

When you encounter a long note that mixes facts with reasoning, you have a hybrid note that needs cleaving. You follow [[SoT - The Unified Writing to Think Process]] rel:: example-of, which uses a rigorous three-phase approach: analysis (identify facts and context), deduplication (check for existing atomic notes), and generation (build new atoms and a MOC).

This process works because it honors the category invariant. Every extracted [[SoT - Atomicity and Loose Coupling]] rel:: part-of is a pure, context-free building block. Every structural note (the MOC) exists solely to create context by linking these atoms with [[Typed Links for Knowledge Context]] rel:: supports that add semantic meaning to each connection.

## Operationalizing Cleaving

Not every note needs cleaving. The system provides clear triggers: [[When to Cleave Notes]] rel:: part-of tells you that notes exceeding 250 words, containing 12+ outlinks, or having contextual sections (like "Use cases" or "Trade-offs") are candidates for deconstruction.

To implement cleaving systematically, all notes in the vault follow [[Canonical Schema V1]] rel:: part-of, which defines required YAML frontmatter fields, ensures machine readability, and enables dataview queries.

## Quality and Maturity

Every note starts as a seedling and matures over time. [[Note Status Lifecycle]] rel:: part-of ensures that only well-integrated, reviewed, and reliable notes become evergreen. This means that LLM-generated notes (which always start as seedlings) are subject to human review before being promoted, maintaining the integrity of your knowledge base.

The status progression—seedling → growing → evergreen—is not just metadata; it is a quality gate. An evergreen note has survived review, has multiple inbound links proving its utility, and has a justified confidence score.

## Why This Matters

Cleaving is labor-intensive upfront but pays dividends over time. By separating atoms from narrative, you create a vault where:

- Facts are atomic, reusable, and verifiable
- Context is explicit, linked, and discoverable
- The original reasoning is preserved (in MOCs) but not conflated with facts
- Queries and automation become possible (e.g., "show me all notes that support this argument")

The binary category invariant [[SoT - Atomicity and Loose Coupling]] rel:: defines means atomic notes never link to structural notes. This prevents "circular reasoning" in your knowledge base and keeps the architecture clean.

---

## Adjacent Areas (Not in This MOC)

- **Synthesis:** The inverse of cleaving—consolidating many notes into one. Requires a separate prompt.
- **Dataview Automation:** Using queries to maintain schema integrity and find orphaned notes.
- **Templating:** Creating reusable templates for specific note types (decisions, experiments, persons, etc.).
