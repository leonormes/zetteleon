---
conformant: true
created: 2026-09-23T14:48:58+00:00
created_utc: '2026-09-23T00:00:00Z'
modified: 2026-09-25T16:29:16+00:00
permalink: llmeon/00-inbox/a-tenth-of-customer-config-commits-are-repairs-to-earlier-commits
source_title: Multi-customer Deployment Review, and an Assessment of CUE
source_url: N/A — internal engineering assessment
status: seed
tags: [configuration-management, git-history, technical-debt]
title: A Tenth of Customer-Config Commits Are Repairs to Earlier Commits
type: claim
upstream: '[[CUE-ASSESSMENT]]'
---

## A Tenth of Customer-Config Commits Are Repairs to Earlier Commits

Of 337 commits touching customer node configuration in twelve months, 35 (about 10%) have corrective commit subjects such as "fix", "revert", "hotfix", or "typo".

### Scope & Conditions

Measured over the twelve months preceding the assessment; includes six consecutive commits titled "Hotfix/grafana perms".

### Evidence

> "1,307 commits total; 337 (26%) touch `ffnodes/` … Of the 337, 35 (~10%) have corrective subjects."

### Implications

- A visible fraction of engineering time on customer configuration is spent correcting earlier configuration mistakes rather than making new changes.

### Related

- [[SoT - Infrastructure Complexity]]—shared mechanism: string-fragility producing recurring runtime errors is the general pattern this specific commit-rate measures.

[supports:: [[SoT - Infrastructure Complexity]], confidence=medium]
