---
aliases: [qdisc]
created: 2025-11-22T15:00:04+00:00
modified: 2026-07-13T08:44:54+00:00
permalink: llmeon/30-library/100-zettelkasten/concept-linux-queuing-discipline
tags: [SoftwareEngineering/networking/kernel]
title: Concept - Linux Queuing Discipline
---

## Linux Queuing Discipline

Summary: A queuing discipline (qdisc) is a scheduler in the Linux networking stack that manages how packets are buffered and ordered before being handed to the network driver.

Details:

Qdiscs act as a buffer and traffic control system to smooth out bursts, share bandwidth across flows, and prevent bufferbloat. They can enforce rate limits and shaping rules. Common qdiscs include `fq_codel` (Fair Queueing Controlled Delay), which helps minimize latency under load.
