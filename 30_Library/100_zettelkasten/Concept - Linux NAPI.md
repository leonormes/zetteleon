---
aliases: [NAPI]
conformant: false
created: 2025-11-22T15:00:07+00:00
modified: 2026-07-20T16:34:32+00:00
non_conformance_reason: "Bulk inferred type. Needs review."
permalink: llmeon/30-library/100-zettelkasten/concept-linux-napi
tags: [SoftwareEngineering/networking/kernel]
title: Concept - Linux NAPI
type: concept
---

## Linux NAPI

Summary: NAPI (New API) is a Linux kernel interface that improves network performance by switching between interrupt-driven and polling modes to handle high packet loads.

Details:

Standard interrupt handling can overwhelm the CPU if an interrupt is raised for every single incoming packet ("interrupt storm"). NAPI solves this by:

1. Accepting an initial interrupt to wake the driver.
2. Disabling further interrupts and switching to polling mode to process a batch of packets from the ring buffer.
3. Re-enabling interrupts once the queue is drained.
This mechanism increases throughput and reduces CPU usage under load.
