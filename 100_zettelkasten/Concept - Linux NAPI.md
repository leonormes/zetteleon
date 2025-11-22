---
aliases: [NAPI]
confidence: 1.0
created: 2025-11-22T15:00:07Z
epistemic: fact
last_reviewed: 2025-11-22
modified: 2025-11-22T14:41:28Z
purpose: "Explains the Linux kernel's efficient packet processing mechanism."
review_interval: 90
see_also: []
source_of_truth: []
status: seedling
tags: [networking/kernel]
title: Concept - Linux NAPI
type: concept
uid: 2025-11-22T15:00:07Z
updated: 2025-11-22T15:00:07Z
---

## Linux NAPI

**Summary:** NAPI (New API) is a Linux kernel interface that improves network performance by switching between interrupt-driven and polling modes to handle high packet loads.

**Details:**
Standard interrupt handling can overwhelm the CPU if an interrupt is raised for every single incoming packet ("interrupt storm"). NAPI solves this by:
1.  Accepting an initial interrupt to wake the driver.
2.  Disabling further interrupts and switching to polling mode to process a batch of packets from the ring buffer.
3.  Re-enabling interrupts once the queue is drained.
This mechanism increases throughput and reduces CPU usage under load.
