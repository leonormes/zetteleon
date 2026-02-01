---
aliases: ["NIC DMA"]
created: 2025-11-22T15:00:06Z
last_reviewed: "2025-11-22"
modified: 2026-02-01T15:08:35+00:00
status: "seedling"
tags: ["SoftwareEngineering/networking/hardware"]
title: Concept - NIC Direct Memory Access
type: "concept"
updated: 
---

## NIC Direct Memory Access

Summary: NIC Direct Memory Access (DMA) is a technology that allows a Network Interface Card to read frame data directly from and write data directly to system RAM without involving the CPU for every byte.

Details:

DMA significantly reduces CPU overhead and packet processing latency. The NIC pulls data from the kernel's transmit rings in memory to the wire (transmit) and writes incoming wire signals directly into receive rings in memory (receive).
