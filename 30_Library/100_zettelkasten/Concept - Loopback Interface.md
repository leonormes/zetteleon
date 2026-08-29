---
aliases: [lo]
conformant: false
created: 2025-11-22T15:00:12+00:00
modified: 2026-08-29T09:35:59+00:00
non_conformance_reason: "Bulk inferred type. Needs review."
permalink: llmeon/30-library/100-zettelkasten/concept-loopback-interface
tags: [SoftwareEngineering/networking/kernel]
title: Concept - Loopback Interface
type: concept
---

## Loopback Interface

Summary: The loopback interface (commonly `lo` or `127.0.0.1`) is a virtual network interface that allows a computer to communicate with itself.

Details:

Traffic sent to the loopback interface never leaves the device and does not traverse a physical network card (NIC). Since the data remains entirely in software memory buffers, communication over loopback is extremely fast and has very low latency.
