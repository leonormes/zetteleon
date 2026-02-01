---
aliases: []
created: 2025-10-31T12:35:00Z
last_reviewed: ""
modified: 2026-02-01T15:08:27+00:00
status: "seedling"
tags: ["coupling", "SoftwareEngineering/Architecture"]
title: Strategic Duplication Reduces System Coupling
type: "concept"
updated: 
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
