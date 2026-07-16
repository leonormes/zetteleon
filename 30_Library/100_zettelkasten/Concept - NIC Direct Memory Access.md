---
aliases: [NIC DMA]
created: 2025-11-22T15:00:06+00:00
modified: 2026-07-13T08:52:25+00:00
permalink: llmeon/30-library/100-zettelkasten/concept-nic-direct-memory-access
tags: [SoftwareEngineering/networking/hardware]
title: Concept - NIC Direct Memory Access
type: claim
conformant: false
non_conformance_reason: "Bulk inferred type. Needs review."
---

## NIC Direct Memory Access

Summary: NIC Direct Memory Access (DMA) is a technology that allows a Network Interface Card to read frame data directly from and write data directly to system RAM without involving the CPU for every byte.

Details:

DMA significantly reduces CPU overhead and packet processing latency. The NIC pulls data from the kernel's transmit rings in memory to the wire (transmit) and writes incoming wire signals directly into receive rings in memory (receive).
