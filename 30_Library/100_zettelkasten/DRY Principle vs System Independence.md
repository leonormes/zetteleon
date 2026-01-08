---
aliases: []
confidence: "0.9"
created: 2025-10-31T12:37:00Z
epistemic: "principle"
last_reviewed: ""
modified: 2026-01-08T10:50:01+00:00
purpose: "Balance code reuse with modularity."
review_interval: "90"
see_also: ["Strategic Duplication Reduces System Coupling.md"]
source_of_truth: []
status: "seedling"
tags: ["principles", "SoftwareEngineering/Architecture"]
title: DRY Principle vs System Independence
type: "concept"
uid: 
updated: 
---

## DRY Principle Vs System Independence

**Summary:** The tension between:

- DRY (Don't Repeat Yourself): Eliminate code duplication
- Independence: Minimize cross-component dependencies

**Resolution Heuristics:**

1. Duplicate when interfaces differ
2. Share when change patterns align
3. Prefer duplication over wrong abstraction
