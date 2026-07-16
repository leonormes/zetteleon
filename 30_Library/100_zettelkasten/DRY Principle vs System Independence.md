---
aliases: []
created: 2025-10-31T12:37:00+00:00
modified: 2026-07-13T08:52:25+00:00
permalink: llmeon/30-library/100-zettelkasten/dry-principle-vs-system-independence
tags: [principles, SoftwareEngineering/Architecture]
title: DRY Principle vs System Independence
type: claim
conformant: false
non_conformance_reason: "Bulk inferred type. Needs review."
---

## DRY Principle Vs System Independence

Summary: The tension between:

- DRY (Don't Repeat Yourself): Eliminate code duplication
- Independence: Minimize cross-component dependencies

Resolution Heuristics:

1. Duplicate when interfaces differ
2. Share when change patterns align
3. Prefer duplication over wrong abstraction

## Related

- [[Becoming System Agnostic]]
