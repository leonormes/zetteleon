---
created: 2026-06-15T14:03:00+00:00
modified: 2026-07-04T10:49:23+00:00
permalink: llmeon/raw/2026-06-15-pieces-ffnode-refinement-pre-tickets
pieces_ids: [1c6b6bf3-cf07-4e42-8a09-9ff4a4ae72fb, 918c44fc-34b4-43ae-a02e-a6533e884570, badc8227-e2a7-4321-89c0-84ee157b701b, c44e57d3-bddb-4f52-9f21-75e940db7325]
source: pieces
tags: [ffnode, pre-tickets, raw, refinement, stress-testing]
title: 2026-06-15-pieces-ffnode-refinement-pre-tickets
---

From the FFNode Stress Testing refinement meeting on 15 June 2026, Oliver Rushton proposed two new pre-tickets be added to the backlog:

1. Phase00—Node + Database Setup: A new phase to provision and configure the test nodes and their associated databases before Phase 0 (Asset Registration) can begin. This is a dependency for Phase 0.
2. Cohort Design Ticket: An extra ticket to design the test cohorts to match the permutation parameters (node count, database technology, dataset size). Dependency: the data must be available first.

The agent synthesised a full Hermes prompt for creating these Jira tickets, referencing the existing FFNode Stress Testing design document v5 and the validated backlog structure (Option A: FTFL-500 umbrella epic).

Key context from agent synthesis:

- "All three chains are now at sufficient."
- States: Phase00 (Node + database), Phase0c (cohort design), original Phases 0–4 per design doc
- Ollie (Oliver Rushton) authored chart releases via `gapv` and flagging Helm chart override friction
