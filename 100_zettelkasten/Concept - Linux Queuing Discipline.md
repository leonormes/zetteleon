---
aliases: [qdisc]
confidence: 1.0
created: 2025-11-22T15:00:04Z
epistemic: fact
last_reviewed: 2025-11-22
modified: 2025-11-22T14:41:38Z
purpose: "Explains the traffic control layer in the Linux kernel."
review_interval: 90
see_also: []
source_of_truth: []
status: seedling
tags: [networking/kernel]
title: Concept - Linux Queuing Discipline
type: concept
uid: 2025-11-22T15:00:04Z
updated: 2025-11-22T15:00:04Z
---

## Linux Queuing Discipline

**Summary:** A queuing discipline (qdisc) is a scheduler in the Linux networking stack that manages how packets are buffered and ordered before being handed to the network driver.

**Details:**
Qdiscs act as a buffer and traffic control system to smooth out bursts, share bandwidth across flows, and prevent bufferbloat. They can enforce rate limits and shaping rules. Common qdiscs include `fq_codel` (Fair Queueing Controlled Delay), which helps minimize latency under load.
