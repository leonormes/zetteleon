---
aliases: []
confidence: ""
created: 2026-01-08T08:40:29+00:00
epistemic: ""
last_reviewed: ""
modified: 2026-01-23T18:09:20+00:00
purpose: ""
review_interval: ""
see_also: []
source_of_truth: []
status: "stable"
tags: [concept, engineering, sdx, simulation, testing]
title: SoT - Digital Twin
type: "SoT"
---

## SoT - Digital Twin

### 1. Definition

In the context of **Software-Defined X (SDX)**, a **Digital Twin** is a comprehensive, dual-natured virtual system that enables simultaneous hardware and software exploration. It transcends simple 3D visualization to become an executable specification.

### 2. The Dual-Nature Architecture

The Digital Twin is composed of two distinct but coupled layers:

#### A. The Executable Digital Twin (The Physics)

This layer represents the "Reality" of the system.

- **Core:** Runs actual production software binaries on virtualized compute hardware (e.g., Virtual SoCs like ARM Zena).
- **Environment:** Integrates physics-based models of sensors (cameras, LiDAR) and actuators (motors, brakes).
- **Function:** Validates _behavior_ and _performance_ in a deterministic, virtual environment before physical silicon exists.

#### B. The Declarative Digital Twin (The Rules)

This layer represents the "Ideal" of the system.

- **Core:** A machine-readable database of requirements, constraints, and success criteria.
- **Content:** Static definitions of what _must_ happen (e.g., "Latency < 10ms", "Stop distance < 30m").
- **Function:** Provides the static benchmark against which the Executable Twin is measured.

### 3. Integration

The synchronization between these two layers is managed by **[[SoT - Verification Threading]]**, which continuously runs the Executable Twin against the constraints of the Declarative Twin.

---

**See Also:**
- [[SoT - Verification Threading]]
- [[SoT - Software-Defined X (SDX)]]
