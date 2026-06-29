---
aliases:
- Evolving Notes
- Living Note System
- NeuroStack Workflow
- The Merge Protocol
created: 2025-11-13 00:00:00+00:00
last_reviewed: '2026-03-28'
modified: 2026-05-26 11:44:20+00:00
status: evergreen
tags:
- ai
- knowledge-management
- pkm
- synthesis
- TheHuman/Cognition
- thinking
title: SoT - Evolutionary Note System
trust-level: high
type: SoT
updated: null
permalink: llmeon/30-library/so-t/so-t-evolutionary-note-system
---

> The mechanism of growth is the Merge Protocol: "systematically squashing ephemeral thinking (`HEAD` notes) into durable answers (`SoT` notes)."

## 1. Minimum Viable Understanding (MVU)

- Stop creating "Permanent Notes" from scratch.
- Start by thinking in a disposable `HEAD` note (Low Friction).
- Finish by merging the answer into an `SoT` and deleting the draft (Closure).
- Maintain via automated "Stale Note" detection and tiered retrieval to save cognitive tokens.

## 2. The Core Workflow: HEAD -> SoT

The system separates "Thinking" (Volatile) from "Knowing" (Stable).

### Step 1: The Branch (HEAD Note)

- Context: You have a question, a problem, or a confusion.
- Action: Create a `HEAD` note. This is your "Dev Branch."
- ADHD Rule: Be messy. Argue with yourself. Paste logs. There are no rules here.

### Step 2: The Merge (Synthesis)

- Context: You have reached a conclusion or a "Working Knowledge."
- Action:
    1. Extract the core insight (The Answer).
    2. Open the relevant `SoT` note (The Master Branch).
    3. Update the "Minimum Viable Understanding" or "Working Knowledge" section.
    4. Deprecate: Move the `HEAD` note to the archive.

### Step 3: The Supersede

- Context: Your new insight contradicts an old one.
- Action: Overwrite the old SoT content. Do not hoard outdated facts. The goal is _Utility_, not _History_.

---

## 3. Maintenance Mechanics (The NeuroStack Paradigm)

To prevent the vault from becoming a "data graveyard," we adopt biological memory principles:

### A. Stale Note Detection (Prediction Errors)

Surface notes that appear in search results but don't belong there. This "prediction error" is the signal to reconsolidate or deprecate the note before it misleads the system.

### B. Excitability Decay (Hot Notes)

Recently active notes get priority in retrieval. Unused notes lose their "excitability" (hotness score) and fade into the background through exponential decay, reducing noise in the active workspace.

### C. Tiered Retrieval (Token Economy)

To minimize "cognitive load" (and LLM token costs), retrieval follows a three-stage escalation:

1. Triples: Quick factual lookups (Who/What/How).
2. Summaries: Contextual briefings.
3. Full Content: Deep dives only when necessary.

---

## 4. Why This Works for ADHD

- Low Friction Entry: You don't need to find the "perfect" place to write. You just dump into a `HEAD` note (Capture).
- No "Maintenance Debt": You don't keep the mess. Once the insight is extracted, the clutter is archived (Closure).
- Context Recovery: Biological replay mechanisms (session briefs) help rebuild task-specific context after an interruption.

---

## Related Source of Truth (SoT) & Maps

- [[MOC - ProdOS]]—_The central map for the Productivity Operating System, defining the full lifecycle from capture to synthesis._
- [[MOC - PKM as Process vs Product]]—_Explores the philosophical shift from collecting information to active cognitive processing._
- [[SoT - Processing IS the Work]]—_Foundational principle that identifies the act of synthesis as the primary value-generator in knowledge work._
- [[SoT - The Extended Mind]]—_The theoretical basis for offloading working memory to an external, evolutionary system._
- [[SoT - PRODOS Core Specification]]—_Unified specification for the system's kernel, including the Stage 5 Synthesis outcome layer._
- [[SoT - Knowledge Architecture (Associative Ontology)]]—_Deconstructs how the vault's structure supports non-linear discovery and growth._
- [[SoT - Working Memory & Schema Theory]]—_Scientific grounding for why separating volatile and stable memory is critical for neurodivergent brains._