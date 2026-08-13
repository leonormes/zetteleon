---
aliases: []
conformant: true
created: 2025-10-31T12:37:00+00:00
epistemic_status: high
modified: 2026-08-13T10:56:51+00:00
permalink: llmeon/30-library/100-zettelkasten/dry-principle-vs-system-independence
prodos.kind: atomic
prodos.lifecycle: stable
proposition: "In software architecture, minimizing cross-component dependencies is often more valuable than eliminating code duplication, as premature abstraction creates fragile coupling."
tags: [principles, SoftwareEngineering/Architecture]
title: DRY Principle vs System Independence
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

%%[supports:: [[SoT - Pragmatism vs Rigour in Software]]]%%
