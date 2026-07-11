---
aliases: []
created: 2025-10-31 12:35:00+00:00
modified: 2026-07-04 10:51:45+00:00
permalink: llmeon/30-library/100-zettelkasten/strategic-duplication-reduces-system-coupling
tags:
- coupling
- SoftwareEngineering/Architecture
title: Strategic Duplication Reduces System Coupling
prodos:
  kind: atomic
  atomic:
    form: concept
  lifecycle: seedling
  review:
    last_reviewed: ''
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
