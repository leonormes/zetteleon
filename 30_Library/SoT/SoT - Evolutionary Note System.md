---
aliases: [Evolving Notes, Living Note System, NeuroStack Workflow, The Merge Protocol]
conformant: true
created: 2025-11-13T00:00:00+00:00
modified: 2026-10-17T15:02:56+00:00
non_conformance_reason: ''
permalink: llmeon/30-library/so-t/so-t-evolutionary-note-system
status: stable
tags: [ai, knowledge-management, pkm, synthesis, TheHuman/Cognition, thinking, topic/knowledge-architecture]
title: SoT - Evolutionary Note System
type: sot
---

> Slimmed 2026-10-17. The HEAD to SoT workflow this note introduced (the Merge Protocol) is now specified elsewhere. This note stays at its title because archived tombstones and several notes link here. Read the notes below for the current rules.

## 1. Minimum Viable Understanding (MVU)

Thinking and knowing are kept apart. Open questions live in disposable `HEAD` notes in the workbench, and settled answers are folded into durable `SoT` notes, so the vault does not accumulate maintenance debt.

## 2. Where Each Part Now Lives

| Idea from this note | Current home |
|:---|:---|
| What a HEAD note is (an open question you own, with a title ending in `?`) | [[SoT - HEAD Note Contract (The Workbench)]] §1–2 |
| The merge: HEAD resolved into SoT | [[Prompt - ProdOS Chronos Synthesizer]], with the exits in the HEAD Note Contract §3 |
| Supersession and staleness of old SoT content | `status` values in [[SoT - ProdOS Frontmatter Contract (Note Type Schemas)]] and the `Open threads:` pointer in HEAD Note Contract §4 |
| Tombstones for retired HEAD notes | HEAD Note Contract §3.1 |
| Why separating volatile and stable memory suits ADHD | [[SoT - Working Memory & Schema Theory]] and [[SoT - Processing IS the Work]] |

HEAD notes are protected from agent edits ([[AGENTS]] §6.1), so the old "move the HEAD to the archive" step is now done by Leon or the Workbench Sweep, not by an agent.

## 3. Ideas Not Yet Implemented

These came from the NeuroStack idea and have no script, prompt or note behind them. Treat them as candidates, not rules.

- Stale-note detection: a note that surfaces in search where it does not belong is a prediction error, and a signal to reconsolidate or deprecate it.
- Excitability decay: recently active notes rank higher in retrieval, and unused ones fade by exponential decay.
- Tiered retrieval: triples first, then summaries, then full content, to save tokens.
- Session briefs that rebuild context after an interruption.

## Related Source of Truth (SoT) & Maps

- [[MOC - ProdOS]]—_The central map for the Productivity Operating System._
- [[MOC - PKM as Process vs Product]]—_The shift from collecting information to active cognitive processing._
- [[SoT - Processing IS the Work]]—_Synthesis as the primary value-generator in knowledge work._
- [[SoT - The Extended Mind]]—_Theoretical basis for offloading working memory to an external system._
- [[SoT - PRODOS Core Specification]]—_The system kernel, including the Stage 5 Synthesis outcome layer._
- [[SoT - Working Memory & Schema Theory]]—_Why separating volatile and stable memory matters for neurodivergent brains._
