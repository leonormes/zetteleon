---
aliases: [Note Maturity, Status Progression]
conformant: true
created: 2025-10-31T08:20:00+00:00
definition: The lifecycle a note moves through, recorded in the status field as draft, seed, stable, evergreen, stale or superseded, which says how mature and how trustworthy the note is, separately from how confident its claim is.
distinguishes_from: ["[[Probabilistic Thinking Treats Beliefs as Hypotheses With Confidence Levels]]"]
modified: 2026-10-13T00:00:00+01:00
permalink: llmeon/30-library/100-zettelkasten/note-status-lifecycle
status: seed
tags: [quality, topic/knowledge-architecture, workflow, zettelkasten]
title: Note Status Lifecycle
type: concept
used_in_claims: ["[[Propositions Are the Only Thing That Can Be Wrong]]", "[[Reviewing Notes and Their Links Forces Re-engagement With the Ideas]]"]
---

## Note Status Lifecycle

A note's `status` field records how mature and trustworthy the note is, not whether its claim is true, which belongs to `epistemic_status`. The allowed values are `draft`, `seed`, `stable`, `evergreen`, `stale` and `superseded`, and they are fixed by [[SoT - ProdOS Frontmatter Contract (Note Type Schemas)]] and checked by `validate_note_frontmatter.py` and `validate_note_shape.py`.

[implements:: [[SoT - ProdOS Frontmatter Contract (Note Type Schemas)]], strength=3, confidence=medium]

### Scope & Conditions

- Applies to any note with a `type`. The field is optional, so a note with no `status` is simply unclassified, not invalid.
- Unlike `epistemic_status`, which says how sure the claim is, `status` says how finished and how current the note is. A well-evidenced claim can sit in a `seed` note, and a speculative one can be `stable` once it is complete and linked.
- Notes with `own_words: true`, and everything in `01_journals/` and `20_Thinking/`, are protected. An agent never edits their body, so it cannot promote them through the criteria below. It can only suggest a status in chat.
- Notes created before 2026-09-26 are frozen under the Atomic Note Standard. A status change is a frontmatter edit and does not oblige anyone to restructure the body.

### The six states

| Status | Meaning | Enters when |
|:-------|:--------|:------------|
| `draft` | Incomplete or in flux. | Work has started but the note does not yet state its point. |
| `seed` | Complete enough to read, not yet integrated or reviewed. | Default for new notes. LLM-generated notes always start here. By far the most common value, 399 notes against 43 `draft` when counted on 2026-09-22. |
| `stable` | Complete, reviewed and linked in. | The criteria below are met. |
| `evergreen` | Reliable backbone knowledge, used in several contexts. | The stricter criteria below are met. |
| `stale` | Possibly out of date. Needs reconsolidation or deprecation. | A note surfaces in search where it does not belong, or its sources or surrounding notes have moved on. |
| `superseded` | Replaced by another note. | Another note has absorbed it. `superseded_by` is then required. |

The older three-stage model called these seedling, growing and evergreen. Read seedling as `seed` and growing as `stable`. That mapping is an interpretation, since the contract migrated the old `owned` value to `stable` on the same reasoning that the note was complete. Treat it as a working convention, not a rule.

### Promotion criteria

A promotion needs evidence that can be checked in the vault, not a feeling of readiness.

- **`seed` to `stable`:**
  - the note states its point in one proposition or definition;
  - its frontmatter validates and its links are annotated;
  - it has at least one inbound link from a structural note (a MoC, SoT or another note that builds on it);
  - Leon has reviewed it for accuracy and framing. An agent cannot supply this step.
- **`stable` to `evergreen`:**
  - at least two inbound links from structural notes, showing it is useful in more than one context;
  - typed edges (`supports`, `depends_on` and the rest) that justify its place in the argument graph, run through `edge_lint.py`;
  - for claims, `epistemic_status` that the evidence links support.

The old criteria of a `purpose` field, a `confidence` score and a `review_interval` are retired for atomic notes. `purpose` and `last_reviewed` are listed as legacy keys in the Atomic Note Standard, and `confidence` is replaced by `epistemic_status` on claims. A review cadence is still available as `prodos.review` on SoTs, MoCs, protocols, HEAD notes and projects, but atomic notes no longer carry a `prodos` key.

### Demotion and retirement

- **To `stale`:** the vault treats a note that appears in search results where it does not belong as a prediction error. That is the signal to reconsolidate or deprecate it before it misleads retrieval, as set out in [[SoT - Evolutionary Note System]].
- **To `superseded`:** follow the deprecation rule in [[Knowledge Consolidation Agent]]. On the duplicate, change the frontmatter only: set `status: superseded`, set `superseded_by` to a list of quoted wikilinks, and add `archive` to `tags`. Replace the body with a one-line pointer to the surviving note. Set `supersedes` on the survivor.
- **HEAD notes are different.** A merged HEAD note needs a tombstone at its exact original title so inbound links still resolve.
- The contract notes that no pass has yet reconciled existing notes against the rule that `superseded_by` and `status: superseded` go together. `validate_note_frontmatter.py --audit` surfaces the mismatches.

### Evidence

- The enum is stated in the Frontmatter Contract §2 and mirrored in `VALID_STATUS` in `validate_note_shape.py` and in the `Note` fileClass. The three sources agree, and the contract records that `seed` was added to the document on 2026-09-22 because the other two already carried it.
- The retirement of `purpose` and `last_reviewed` for atomic notes is recorded in the Atomic Note Standard.
- The promotion thresholds (one and two inbound structural links, author review) come from this note's earlier version and have not been tested against the vault. No script currently computes inbound structural link counts or promotes anything.

### Implications

- A reader can use `status` to decide how much weight to give a note, and an agent can use it to decide how much to rely on one. Treat `seed` as a draft of an idea, not as settled knowledge.
- Agents create at `seed`, and moving to `stable` needs Leon's review, which keeps promotion a human decision.
- If the two-link evergreen threshold is worth keeping, a Dataview or script check would turn it from a convention into something enforced. That is not built.

### Related

- [[SoT - ProdOS Frontmatter Contract (Note Type Schemas)]]—_Defines the status enum, `supersedes` and `superseded_by`._
- [[SoT - Atomic Note Standard (The Proposition Card)]]—_Says which legacy keys atomic notes must drop and how older notes are frozen._
- [[SoT - Evolutionary Note System]]—_Source of stale-note detection and tombstoning._
- [[Knowledge Consolidation Agent]]—_The procedure for marking a note superseded._
- [[Propositions Are the Only Thing That Can Be Wrong]]—_Claim notes are the ones that carry an `epistemic_status` alongside `status`._
- [[Reviewing Notes and Their Links Forces Re-engagement With the Ideas]]—_Checking a note against these criteria is itself a form of review._
