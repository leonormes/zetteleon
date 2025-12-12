---
aliases: [Declarative Intent, Intent vs Implementation]
confidence: 0.8
created: 2025-01-15T10:06:00Z
epistemic: principle
last_reviewed: 2025-01-15
modified: 2025-11-12T14:24:42Z
purpose: Design principle that separates what to deploy from how to deploy it
review_interval: 90
see_also: []
source_of_truth: []
status: seedling
tags: [declarative, design-principle, infrastructure]
title: Intent-Implementation Separation
type: concept
uid: 2025-01-15T10:06:00Z
updated: 2025-01-15T10:06:00Z
---

## Intent-Implementation Separation

**Summary:** A design principle that separates declarative intent (what to deploy) from implementation details (how to deploy it), enabling automation and reducing cognitive load.

**Details:** Intent-Implementation Separation distinguishes between essential deployment parameters that express business intent (application name, environment, region) and derived implementation details (specific DNS names, bucket names, IAM role ARNs). By capturing only intent in a Configuration Kernel and deriving implementation through a Configuration Generator, this principle reduces the cognitive burden on operators and enables consistent automation. The separation allows implementation details to evolve (e.g., changing naming conventions) without requiring operators to understand or modify those details across all deployments.
