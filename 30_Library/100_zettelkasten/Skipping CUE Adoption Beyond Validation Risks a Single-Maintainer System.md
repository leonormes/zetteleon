---
conformant: true
created: 2026-09-23T14:50:16+00:00
created_utc: '2026-09-23T00:00:00Z'
modified: 2026-09-25T16:29:31+00:00
permalink: llmeon/00-inbox/skipping-cue-adoption-beyond-validation-risks-a-single-maintainer-system
source_title: Multi-customer Deployment Review, and an Assessment of CUE
source_url: N/A — internal engineering assessment
status: seed
tags: [cue, risk, team-capability]
title: Skipping CUE Adoption Beyond Validation Risks a Single-Maintainer System
type: claim
upstream: '[[CUE-ASSESSMENT]]'
---

## Skipping CUE Adoption Beyond Validation Risks a Single-Maintainer System

If a team will not learn CUE's semantics, a validation-only schema is still worth adopting because a schema is readable even to non-CUE-fluent engineers, but generating and deep-merging values in CUE beyond that point produces a system only one person can maintain.

### Scope & Conditions

A condition for arguing against the fuller adoption path (the shared-module option and the deep-merge/generation steps) specifically, not against CUE in general.

### Evidence

> "If the team won't learn CUE, Step 0 is still worth it (a schema is readable even if the language isn't), but Steps 2–3 will produce a system one person maintains. That is worse than the status quo."

### Implications

- Team capability, not just technical merit, should gate how far the adoption sequence is taken.

### Related

- [[CUE Is a Second Language With Unusual Semantics]]—extends: the specific adoption cost this constraint says should gate scope.
- [[Recommended CUE Adoption Sequence Is Validate Publish Merge Then Generate]]—extends: names exactly which steps of that sequence (2–3) carry this risk.
