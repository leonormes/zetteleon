---
aliases: [lo]
conformant: false
created: 2025-11-22T15:00:12+00:00
modified: 2026-09-19T15:44:33+00:00
non_conformance_reason: "missing schema field definition for type concept (required when conformant - true); missing schema field used_in_claims for type concept (required when conformant - true); missing schema field distinguishes_from for type concept (required when conformant - true)"
permalink: llmeon/30-library/100-zettelkasten/concept-loopback-interface
tags: [SoftwareEngineering/networking/kernel]
title: Concept - Loopback Interface
type: concept
---

## Loopback Interface

Summary: The loopback interface (commonly `lo` or `127.0.0.1`) is a virtual network interface that allows a computer to communicate with itself.

Details:

Traffic sent to the loopback interface never leaves the device and does not traverse a physical network card (NIC). Since the data remains entirely in software memory buffers, communication over loopback is extremely fast and has very low latency.
