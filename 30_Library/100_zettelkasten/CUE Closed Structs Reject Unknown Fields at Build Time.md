---
conformant: true
created: 2026-09-23T14:48:59+00:00
created_utc: '2026-09-23T00:00:00Z'
modified: 2026-09-26T08:45:27+00:00
permalink: llmeon/00-inbox/cue-closed-structs-reject-unknown-fields-at-build-time
source_title: Multi-customer Deployment Review, and an Assessment of CUE
source_url: N/A — internal engineering assessment
status: seed
tags: [cue, schema, validation]
title: CUE Closed Structs Reject Unknown Fields at Build Time
type: claim
upstream: '[[CUE-ASSESSMENT]]'
---

## CUE Closed Structs Reject Unknown Fields at Build Time

A CUE closed struct (`#Definition`) rejects a field it does not declare, producing a build-time error with file, line, and column, instead of silently accepting it the way Helm does.

### Scope & Conditions

Requires the struct to be declared closed; open structs (using `…`) do not gain this protection.

### Evidence

> "Closed structs (`#Definition`) reject unknown fields—this is what catches `replicaCnt`. Verified locally against `cue v0.17.1`: `w.mongodb.replicaCnt: field not allowed:./typo.cue:4:11`"

### Implications

- This is the specific mechanism that closes the typo-class failure documented for Helm.
- Any struct left open with `…` for convenience gives up this protection for that struct.

### Related

- [[Unvalidated Helm Values Accept Arbitrary Keys Silently]]—contradicts: this mechanism is the direct fix for that failure mode.
- [[SoT - Type-Driven Infrastructure Strategy]]—extends: a concrete instance of the "Shift Left" principle, moving validation from runtime to synthesis time.
