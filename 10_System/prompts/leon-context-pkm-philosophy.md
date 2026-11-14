---
aliases: []
created: 2026-02-02T07:05:00+00:00
description: "The PKM/ProdOS philosophy and mechanics (binary architecture, epistemics, anti-hoarding goal)."
modified: 2026-10-22T15:11:07+00:00
permalink: llmeon/10-system/prompts/leon-context-pkm-philosophy
tags: [domain/pkm, system/prompt, type/context]
title: leon-context-pkm-philosophy
type: prompt
---

## Knowledge Management Context (The Librarian)

### System Architecture

My Obsidian vault uses a Binary Architecture:

1. Atomic Notes ("Bricks"): Context-free, reusable units (Concepts, Definitions, Quotes).
2. Structural Notes ("Architecture"): Frameworks that link bricks (Maps, Sequences, Arguments).

### Advanced Mechanics

- Epistemic Layer: I track _certainty_ and _confidence_ in my notes.
- Cleaving: The process of breaking hybrid notes into atomic components.
- PDU Analogy: I treat knowledge like network packets (Protocol Data Units)—metadata layers wrapping atomic content.

### Evolutionary Mechanics

- Git-Model: HEAD (current view), STAGING (raw capture), THREAD (history).
- Resonance Scoring: A metric to counter recency bias by rating genuine insight quality over time.

### K-Plex Knowledge Architecture & Idea Compass

- Visual Knowledge Compiler: **K-Plex** (`.obsidian/plugins/k-plex/`) renders the graph with `inferAllLinksAsFriends: false` and `showInferredNodes: false`—plain `[[wikilinks]]` remain hidden unless typed via `[<relationship>:: [[Target]]]` or mapped relational frontmatter.
- Idea Compass Axes:
  - **North (`parents` — Origin/Governance):** `depends_on`, `extends`, `implements`, `upstream`, `source`, `uses_concept`
  - **South (`children` — Synthesis/Generative):** `synthesizes`, `entry_points`, `candidate_answers`
  - **West (`leftFriends` — Support):** `supports`, `supports_claims`, `evidence_links`, `see_also`
  - **East (`rightFriends` — Challenge):** `contradicts`, `distinguishes_from`, `contrasts_with`, `tension`
  - **Sequence (`previous` / `next` — Lineage):** `revises`, `supersedes`, `superseded_by`, `merged_from`
- Facets & Precedence: Preset views organise neighbourhoods by `type` (`prodos-types`) and lifecycle `status` (`prodos-status`). Under `frontmatter-overrides-body-ontology`, frontmatter takes precedence over body edges—never duplicate an inline typed-edge target in `see_also`.

### Goal

To prevent "Digital Hoarding." All knowledge must eventually serve an output or an action.
