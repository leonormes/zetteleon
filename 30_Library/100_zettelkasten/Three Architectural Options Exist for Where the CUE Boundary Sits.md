---
conformant: true
created: 2026-09-23T14:50:15+00:00
created_utc: '2026-09-23T00:00:00Z'
modified: 2026-09-25T16:29:34+00:00
permalink: llmeon/00-inbox/three-architectural-options-exist-for-where-the-cue-boundary-sits
source_title: Multi-customer Deployment Review, and an Assessment of CUE
source_url: N/A — internal engineering assessment
status: seed
tags: [architecture, cue, decision-framework]
title: Three Architectural Options Exist for Where the CUE Boundary Sits
type: concept
upstream: '[[CUE-ASSESSMENT]]'
---

## Three Architectural Options Exist for Where the CUE Boundary Sits

There are three materially different positions for where CUE's boundary sits: a per-repo values generator (highest payoff and highest cost, already drifted, not recommended); a shared published module reading source data directly (deletes the worst relocated complexity, judged the right destination); and validation-only with no generation (cheapest real improvement, closes only the typo and CI-validation gaps).

### Scope & Conditions

This is a decision framework for scoping any CUE adoption on this platform, not a universal CUE taxonomy.

### Evidence

> "Option A … Not recommended as the next step. Option B … This is the right destination. Option C … Cheapest real improvement available."

### Implications

- Choosing Option A for its highest per-customer payoff ignores that it is also the option that has already visibly drifted.
- Option C can be adopted with zero architectural commitment and does not block a later move to Option B.

### Related

- [[Unversioned CUE Included Per-Repo Has Already Forked Between Two Copies]]—extends: the concrete drift evidence behind ruling out Option A.
- [[SoT - Generative Infrastructure Configuration Framework]]—extends: Option B corresponds to that SoT's "Level 2: CUE (Constraint-Based)" implementation pattern.
- [[SoT - Strategy - Helm to CUE Migration]]—shared mechanism: a related but distinct decision framework—that SoT's three phases are a sequence, not alternative end-states, to choose between.
