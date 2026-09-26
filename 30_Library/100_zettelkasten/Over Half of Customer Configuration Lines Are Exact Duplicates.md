---
conformant: true
created: 2026-09-23T14:48:29+00:00
created_utc: '2026-09-23T00:00:00Z'
modified: 2026-09-26T08:45:34+00:00
permalink: llmeon/00-inbox/over-half-of-customer-configuration-lines-are-exact-duplicates
source_title: Multi-customer Deployment Review, and an Assessment of CUE
source_url: N/A — internal engineering assessment
status: seed
tags: [configuration-management, duplication, technical-debt]
title: Over Half of Customer Configuration Lines Are Exact Duplicates
type: claim
upstream: '[[CUE-ASSESSMENT]]'
---

## Over Half of Customer Configuration Lines Are Exact Duplicates

Across 29 primary customer values files, 57.8% of substantive lines are exact duplicates of a line appearing in another customer's file.

### Scope & Conditions

Measured by counting only substantive lines (longer than 30 characters). The most-repeated lines are values that should be platform-wide defaults, such as a shared TLS secret name or a shared auth0 base URL.

### Evidence

> "1,317 substantive lines, 556 distinct → 57.8% are exact duplicates of a line in another file."

### Implications

- A platform-default value that needs to change requires editing dozens of near-identical files by hand.
- The duplication is direct evidence that these values belong in a shared default layer, not per-customer overrides.

### Related

- [[SoT - Generative Infrastructure Configuration Framework]]—contradicts: directly violates that SoT's "Data Has One Home" principle, that every value must trace to exactly one authoritative source.

[supports:: [[SoT - Infrastructure Complexity]], confidence=medium]
