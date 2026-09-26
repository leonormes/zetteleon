---
conformant: true
created: 2026-09-23T14:49:40+00:00
created_utc: '2026-09-23T00:00:00Z'
modified: 2026-09-25T16:29:35+00:00
permalink: llmeon/00-inbox/unversioned-cue-included-per-repo-has-already-forked-between-two-copies
source_title: Multi-customer Deployment Review, and an Assessment of CUE
source_url: N/A — internal engineering assessment
status: seed
tags: [cue, drift, versioning]
title: Unversioned CUE Included Per-Repo Has Already Forked Between Two Copies
type: claim
upstream: '[[CUE-ASSESSMENT]]'
---

## Unversioned CUE Included Per-Repo Has Already Forked Between Two Copies

With no `cue.mod` and no module versioning, the second proof-of-concept's CUE files exist as two separate directory copies that have already diverged in behaviour, including one copy gating a monitoring block on a condition the other copy does not apply.

### Scope & Conditions

Applies to any CUE code distributed by file-copy per repository rather than as a versioned, published module.

### Evidence

> "One copy gates the whole Grafana block on `if facts.deploy.monitoring`; the other does not … A platform rule has already forked between two copies of the platform's own rendering logic."

### Implications

- Putting CUE in each customer repo reproduces the original rsync-fork onboarding problem one layer up, and makes it worse because the forked thing is now logic, not just data.
- Publishing the module to an OCI registry and pinning it per customer prevents this specific fork.

### Related

- [[Two Parallel Customer-Onboarding Paths Coexist]]—shared mechanism: the same rsync-fork pattern this failure mode reproduces one layer up, now in logic instead of data.
- [[SoT - Strategy - Helm to CUE Migration]]—extends: the migration-risk consequence of skipping module versioning during adoption.
