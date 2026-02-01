---
aliases: ["Declarative Intent", "Intent vs Implementation"]
created: 2025-01-15T10:06:00Z
last_reviewed: "2025-01-15"
modified: 2026-02-01T15:08:32+00:00
status: "seedling"
tags: ["declarative", "design-principle", "infrastructure"]
title: Intent-Implementation Separation
type: "concept"
updated: 
---

## Intent-Implementation Separation

Summary: A design principle that separates declarative intent (what to deploy) from implementation details (how to deploy it), enabling automation and reducing cognitive load.

Details: Intent-Implementation Separation distinguishes between essential deployment parameters that express business intent (application name, environment, region) and derived implementation details (specific DNS names, bucket names, IAM role ARNs). By capturing only intent in a Configuration Kernel and deriving implementation through a Configuration Generator, this principle reduces the cognitive burden on operators and enables consistent automation. The separation allows implementation details to evolve (e.g., changing naming conventions) without requiring operators to understand or modify those details across all deployments.
