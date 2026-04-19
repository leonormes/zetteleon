---
aliases: []
created: 2025-08-29T15:13:40Z
last_reviewed: ""
modified: 2026-04-19T18:30:41+00:00
status: ""
tags: []
title: Leaky Abstractions
type: ""
updated: 
---

An abstraction in software is a simplified view of a complex system that hides the underlying implementation details (e.g., a file API hides the complexity of disk sectors).

An abstraction is "leaky" when the underlying complexity—the details it is supposed to hide—"leaks through" and must be understood to solve a problem. For example, a TCP connection modelled as a "reliable data pipe" leaks when you must debug packet loss or network congestion, forcing you to understand the underlying TCP protocol.

Mental models often function as personal abstractions that work until they leak.

Links: [[The Map is Not the Territory]]
