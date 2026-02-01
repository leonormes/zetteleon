---
aliases: ["NAPI"]
created: 2025-11-22T15:00:07Z
last_reviewed: "2025-11-22"
modified: 2026-02-01T15:08:35+00:00
status: "seedling"
tags: ["SoftwareEngineering/networking/kernel"]
title: Concept - Linux NAPI
type: "concept"
updated: 
---

## Linux NAPI

Summary: NAPI (New API) is a Linux kernel interface that improves network performance by switching between interrupt-driven and polling modes to handle high packet loads.

Details:

Standard interrupt handling can overwhelm the CPU if an interrupt is raised for every single incoming packet ("interrupt storm"). NAPI solves this by:

1. Accepting an initial interrupt to wake the driver.
2. Disabling further interrupts and switching to polling mode to process a batch of packets from the ring buffer.
3. Re-enabling interrupts once the queue is drained.
This mechanism increases throughput and reduces CPU usage under load.
