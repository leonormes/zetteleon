---
aliases: ["lo"]
confidence: "1.0"
created: 2025-11-22T15:00:12Z
epistemic: "fact"
last_reviewed: "2025-11-22"
modified: 2026-01-03T10:19:42+00:00
purpose: "Explains the virtual internal network interface."
review_interval: "90"
see_also: []
source_of_truth: []
status: "seedling"
tags: ["SoftwareEngineering/networking/kernel"]
title: Concept - Loopback Interface
type: "concept"
uid: 
updated: 
---

## Loopback Interface

**Summary:** The loopback interface (commonly `lo` or `127.0.0.1`) is a virtual network interface that allows a computer to communicate with itself.

**Details:**
Traffic sent to the loopback interface never leaves the device and does not traverse a physical network card (NIC). Since the data remains entirely in software memory buffers, communication over loopback is extremely fast and has very low latency.
