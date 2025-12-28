---
aliases: ["NIC DMA"]
confidence: "1.0"
created: 2025-11-22T15:00:06Z
epistemic: "fact"
last_reviewed: "2025-11-22"
modified: 2025-12-28T09:56:32+00:00
purpose: "Explains how Network Interface Cards access system memory."
review_interval: "90"
see_also: []
source_of_truth: []
status: "seedling"
tags: ["topic/technology/networking/hardware"]
title: Concept - NIC Direct Memory Access
type: "concept"
uid: 
updated: 
---

## NIC Direct Memory Access

**Summary:** NIC Direct Memory Access (DMA) is a technology that allows a Network Interface Card to read frame data directly from and write data directly to system RAM without involving the CPU for every byte.

**Details:**
DMA significantly reduces CPU overhead and packet processing latency. The NIC pulls data from the kernel's transmit rings in memory to the wire (transmit) and writes incoming wire signals directly into receive rings in memory (receive).
