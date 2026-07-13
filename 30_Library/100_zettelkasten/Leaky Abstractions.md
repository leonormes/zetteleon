---
aliases: []
created: 2025-08-29T15:13:40+00:00
last_reviewed: ''
modified: 2026-07-13T08:52:28+00:00
permalink: llmeon/30-library/100-zettelkasten/leaky-abstractions
status: ''
tags: []
title: Leaky Abstractions
type: ''
updated: null
---

An abstraction in software is a simplified view of a complex system that hides the underlying implementation details (e.g., a file API hides the complexity of disk sectors).

An abstraction is "leaky" when the underlying complexity—the details it is supposed to hide—"leaks through" and must be understood to solve a problem. For example, a TCP connection modelled as a "reliable data pipe" leaks when you must debug packet loss or network congestion, forcing you to understand the underlying TCP protocol.

Mental models often function as personal abstractions that work until they leak.

Links: [[The Map is Not the Territory]]
