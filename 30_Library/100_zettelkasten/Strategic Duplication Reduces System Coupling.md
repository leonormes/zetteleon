---
aliases: []
created: 2025-10-31T12:35:00+00:00
last_reviewed: ''
modified: 2026-07-04T10:51:45+00:00
permalink: llmeon/30-library/100-zettelkasten/strategic-duplication-reduces-system-coupling
status: seedling
tags: [coupling, SoftwareEngineering/Architecture]
title: Strategic Duplication Reduces System Coupling
type: concept
updated: null
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
