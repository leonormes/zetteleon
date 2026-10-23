---
aliases: []
conformant: true
created: 2025-08-29T15:13:40+00:00
definition: An abstraction is leaky when the underlying complexity it is meant to hide leaks through and has to be understood to solve a problem
distinguishes_from: ["[[Maps as Simplified Abstractions]]"]
modified: 2026-10-22T15:11:16+00:00
non_conformance_reason: ""
permalink: llmeon/30-library/100-zettelkasten/leaky-abstractions
tags: [abstraction, devex]
title: Leaky Abstractions
type: concept
used_in_claims: ["[[Knowledge Applicability of Blub Studies]]"]
---

An abstraction in software is a simplified view of a complex system that hides the underlying implementation details (e.g., a file API hides the complexity of disk sectors).

An abstraction is "leaky" when the underlying complexity—the details it is supposed to hide—"leaks through" and must be understood to solve a problem. For example, a TCP connection modelled as a "reliable data pipe" leaks when you must debug packet loss or network congestion, forcing you to understand the underlying TCP protocol.

Mental models often function as personal abstractions that work until they leak.

Links: [[The Map is Not the Territory]]

## Related

- [[Blub Studies]]—_The practice that answers leakage: learning what sits under the tools you use._
- [[SoT - Mechanical Sympathy]]—_The same point at system level: abstractions work until you need to know how the machine behaves._
- [[SoT - Mental Models in Software Development]]—_Mental models are personal abstractions and leak in the same way._
- [[Flawed Mental Models Limit Mastery]]—_What a leak exposes when the model underneath is wrong._
- [[Maps as Simplified Abstractions]]—_The map analogy for abstraction, where detail is dropped on purpose._
- [[Higher Abstraction Levels Increase Breadth But Reduce Depth]]—_The trade-off that makes leaks possible: the detail given up at higher levels._
