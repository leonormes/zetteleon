---
aliases: []
created: 2025-10-31 12:37:00+00:00
last_reviewed: ''
modified: 2026-02-01 15:08:35+00:00
status: seedling
tags:
- principles
- SoftwareEngineering/Architecture
title: DRY Principle vs System Independence
type: concept
updated: null
permalink: llmeon/30-library/100-zettelkasten/dry-principle-vs-system-independence
---

## DRY Principle Vs System Independence

Summary: The tension between:

- DRY (Don't Repeat Yourself): Eliminate code duplication
- Independence: Minimize cross-component dependencies

Resolution Heuristics:

1. Duplicate when interfaces differ
2. Share when change patterns align
3. Prefer duplication over wrong abstraction