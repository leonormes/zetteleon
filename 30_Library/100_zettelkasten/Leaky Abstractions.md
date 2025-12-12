---
aliases: []
confidence: 
created: 2025-08-29T15:13:40Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T10:27:46Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: Leaky Abstractions
type:
uid: 
updated: 
version:
---

An abstraction in software is a simplified view of a complex system that hides the underlying implementation details (e.g., a file API hides the complexity of disk sectors).

An abstraction is "leaky" when the underlying complexity—the details it is supposed to hide—"leaks through" and must be understood to solve a problem. For example, a TCP connection modelled as a "reliable data pipe" leaks when you must debug packet loss or network congestion, forcing you to understand the underlying TCP protocol.

Mental models often function as personal abstractions that work until they leak.

Links: [[The Map is Not the Territory]]

[[Bug in the model]]
