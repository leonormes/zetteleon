---
aliases: [Schema V1]
confidence: 0.95
created: 2025-10-31T08:17:00Z
epistemic: principle
last_reviewed: 2025-10-31
modified: 2025-11-01T09:43:55Z
purpose: "Reference definition of the required YAML frontmatter structure for all zettelkasten notes."
review_interval: 180
see_also: []
source_of_truth: []
status: seedling
tags: [metadata, schema, zettelkasten]
title: Canonical Schema V1
type: definition
uid: 2025-10-31T08:17:00Z
updated: 2025-10-31T08:17:00Z
---

## Canonical Schema V1

**Summary:** A standardized YAML frontmatter template and field specification that ensures all notes in the vault are machine-readable, queryable, and adhere to the atomic/structural category invariant.

**Details:**

All notes must include the following global fields:

- `uid`: ISO 8601 UTC timestamp (YYYY-MM-DDTHH:MM:SSZ) serving as a unique identifier
- `created`: ISO timestamp of note creation
- `updated`: ISO timestamp of last modification
- `type`: Note category (atomic subtypes: concept, strategy, definition, instructional, question, quote, person; structural subtypes: map, comparison, sequence, argument, project, timeline, source, experiment, decision)
- `aliases`: Array of alternative names
- `tags`: Array of categorical tags

Atomic notes additionally require:

- `status`: seedling | growing | evergreen
- `epistemic`: fact | axiom | principle | opinion | hypothesis | NA
- `purpose`: One-line description of what the note is for
- `confidence`: Decimal 0–1 indicating epistemic confidence
- `last_reviewed`: YYYY-MM-DD of last review
- `review_interval`: Integer days between reviews
- `see_also`: Array of related atomic notes only
- `source_of_truth`: Optional array of canonical sources

Structural notes additionally require:

- `scope`: What belongs in this note
- `exclusions`: What does not belong
- `criteria`: Inclusion criteria for adding links

This schema enables dataview queries, automation, and linting.
