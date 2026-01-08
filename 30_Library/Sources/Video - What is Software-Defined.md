---
aliases: []
author: David Fritz
confidence: ""
created: 2026-01-08T08:33:31+00:00
epistemic: ""
last_reviewed: ""
modified: 2026-01-08T10:49:39+00:00
purpose: ""
review_interval: ""
see_also: []
source_of_truth: []
status: ""
tags: [engineering, hardware, sdx, source/video]
title: Video - What is Software-Defined
type: ""
---

## Video - What is Software-Defined?

### Summary

Based on the video "What is Software-Defined?" featuring David Fritz from Siemens, here is the conceptual framework and operational model discussed.

#### Core Concept: Software-Defined (SDX)

The term "Software-Defined" (encompassing Software-Defined Products, Vehicles, etc.) refers to a development methodology where hardware and software exploration occurs simultaneously. Unlike traditional workflows where software is constrained by pre-selected generic hardware, SDX allows the software requirements to dictate hardware architecture [01:27].

#### The Problem: Integration Hell

In complex systems like modern vehicles, separate subsystems (IVI, ADAS, chassis control) are often developed by different suppliers using isolated workflows. When these components are finally integrated, incompatibilities arise ("integration hell"), leading to massive recalls and failure to meet requirements [03:58]. Generic System-on-Chips (SoCs) are increasingly insufficient for these specialised workloads [01:47].

#### The Solution Framework: PAVE360 & Digital Twins

The proposed solution moves from physical validation to a virtualised, iterative CI/CD model.

**Virtualisation First:** Compute subsystems (e.g., ARM’s Zena) are virtualised in the cloud, allowing software development to begin long before the physical silicon exists. This creates a "golden model" accessible to all suppliers [02:18], [04:58].

**The Dual-Nature Digital Twin:** The Digital Twin is conceptualised as having two distinct components [06:59]:
1. **Executable Digital Twin:** Runs the actual software and physics-based models of sensors and actuators.
2. **Declarative Digital Twin:** Represents the static requirements and documentation of what should happen.

**Verification Threading:** This is the bridge that validates the Executable against the Declarative. It allows engineers to quantify the probability of meeting a requirement (e.g., stopping for an obstacle) based on current design parameters (sensor resolution, processing speed, data throughput) [07:36].

#### Operational Model

1. **Exploration:** Run millions of high-level scenarios in the cloud to identify failing requirements [05:51].
2. **Optimisation:** Adjust hardware parameters (e.g., camera resolution, NPU selection) to meet software needs iteratively [08:42].
3. **Hybrid Verification:** As the design matures, virtual pieces are swapped for physical hardware (ECUs) for final validation, ensuring the system works before physical production begins [06:07].
