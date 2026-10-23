---
created: 2026-10-14T14:45:00+00:00
modified: 2026-10-22T15:11:05+00:00
permalink: llmeon/90-audits/2026-10-14-unexplained-underachievement
tags: [audit, TheHuman/Health/ADHD]
title: Audit - Unexplained Underachievement positioning
type: audit
---

## Positioning—[[Unexplained Underachievement]]—2026-10-14

Prompt used: [[Orphan Note Positioning & Thread Audit]] (thin note, one broken outbound link, no frontmatter conformance).

### Baseline

Thin: one outbound link (broken: `MoC - The Roots of Shame and Feeling Defective` does not exist; alias on [[MOC - Shame]]), four inbound (Misinterpretation as Character Flaws, MOC - Shame, SoT - ADHD Self-Compassion & Strengths, SoT - Belief Architecture & Cognitive Spaces). `type` empty. Graph state before: not grounded (`--why` showed no grounds), with one dependent.

### Patch A—Typed Edge

| Target file | Edge | Rationale | Resolved |
|---|---|---|---|
| Unexplained Underachievement | `[depends_on:: [[Misinterpretation as Character Flaws]], confidence=medium]` | Denial: without the misread-as-flaw criticism the note's mechanism loses its cause. Load: retracting it moves confidence. | Yes |

### Patch B—Plain Links

Added a `## Related` section with seven annotated links (Distorted Negative Self-Image, RSD, Shame-Procrastination Cycle, two SoTs, Executive Function Challenges). Broken MoC link repointed to [[MOC - Shame]] with the old display text.

### Patch C—Frontmatter

`type` blank to `claim`, `conformant: false` (no proposition card), `epistemic_status: medium`, tags added.

### Patch D—Personal Library

No matches. Best ARCHILLES hit scored 0.308 but the snippet did not bear on the claim.

### No Evidence / Needs Your Call

- Reverse edge `Distorted Negative Self-Image depends_on Unexplained Underachievement` is plausible but belongs in that note; not written.
- Note body is one paragraph with no source quote; a proposition card would make it conformant.

## Thread Audit

- Now grounded: `--why` traces through Misinterpretation as Character Flaws to the Interest-Based Nervous System SoT and dopamine evidence.
- Impact: [[SoT - Belief Architecture & Cognitive Spaces]] depends on it.
- Weakest link: Misinterpretation as Character Flaws is untyped (`[?]`) and itself rests on a journal note.

### Validation

- `edge_lint.py` (whole vault): 5 errors, none in this note (pre-existing, e.g. dangling `Mistaking the Map for the Territory`). 0 warnings.
- Confidence: medium.

Next action: write a proposition card for [[Unexplained Underachievement]] so it can be marked `conformant: true`.
