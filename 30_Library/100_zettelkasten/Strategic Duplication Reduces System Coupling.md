---
aliases: []
conformant: false
created: 2025-10-31T12:35:00+00:00
modified: 2026-09-19T15:44:43+00:00
non_conformance_reason: "missing schema field proposition for type claim (required when conformant - true); missing schema field contradicts for type claim (required when conformant - true); missing schema field evidence_links for type claim (required when conformant - true); missing schema field epistemic_status for type claim (required when conformant - true)"
permalink: llmeon/30-library/100-zettelkasten/strategic-duplication-reduces-system-coupling
tags: [coupling, SoftwareEngineering/Architecture]
title: Strategic Duplication Reduces System Coupling
type: claim
---

## Strategic Duplication Reduces System Coupling

Summary: Intentional code duplication can improve system independence when:

- Components must evolve separately
- Dependency chains create fragility
- Modularity outweighs DRY benefits

Examples:

- Isolated microservices with similar logic
- Avoiding shared libraries with version conflicts
- Temporary forks during migrations
