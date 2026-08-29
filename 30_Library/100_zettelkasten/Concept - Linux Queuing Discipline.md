---
aliases: [qdisc]
conformant: false
created: 2025-11-22T15:00:04+00:00
modified: 2026-08-29T09:35:59+00:00
non_conformance_reason: "Bulk inferred type. Needs review."
permalink: llmeon/30-library/100-zettelkasten/concept-linux-queuing-discipline
tags: [SoftwareEngineering/networking/kernel]
title: Concept - Linux Queuing Discipline
type: claim
---

## Linux Queuing Discipline

Summary: A queuing discipline (qdisc) is a scheduler in the Linux networking stack that manages how packets are buffered and ordered before being handed to the network driver.

Details:

Qdiscs act as a buffer and traffic control system to smooth out bursts, share bandwidth across flows, and prevent bufferbloat. They can enforce rate limits and shaping rules. Common qdiscs include `fq_codel` (Fair Queueing Controlled Delay), which helps minimize latency under load.
