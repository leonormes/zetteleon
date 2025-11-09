---
aliases: []
confidence: 0.9
created: 2025-10-31T12:35:00Z
epistemic: principle
last_reviewed: 
modified: 2025-10-31T12:35:00Z
purpose: "Explain when duplication benefits system design."
review_interval: 90
see_also: []
source_of_truth: []
status: seedling
tags: [architecture, coupling]
title: Strategic Duplication Reduces System Coupling
type: concept
uid: 
updated: 
---

## Strategic Duplication Reduces System Coupling

**Summary:** Intentional code duplication can improve system independence when:
- Components must evolve separately
- Dependency chains create fragility
- Modularity outweighs DRY benefits

**Examples:**
- Isolated microservices with similar logic
- Avoiding shared libraries with version conflicts
- Temporary forks during migrations
