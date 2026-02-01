---
aliases: [SDX, Software-Defined X]
created: 2026-01-08T08:40:29+00:00
last_reviewed: ""
modified: 2026-02-01T15:07:51+00:00
status: "stable"
tags: [architecture, concept, engineering, hardware, sdx]
title: SoT - Software-Defined X (SDX)
type: "SoT"
---

## SoT - Software-Defined X (SDX)

### 1. Definition

Software-Defined X (SDX) is a Systems Engineering methodology where software requirements dictate hardware architecture, rather than software being constrained by pre-selected generic hardware. It effectively applies CI/CD and Agile principles to physical hardware development via virtualization.

### 2. Core Problem: Integration Hell

In traditional "Hardware First" workflows, separate subsystems (IVI, ADAS, Chassis) are developed in isolation and integrated only when physical prototypes are available. This leads to:

- Late-Stage Failure: Discovery of fundamental incompatibilities ("Integration Hell") when change is most expensive.
- Suboptimal Hardware: Use of generic SoCs that are over-provisioned (wasteful) or under-provisioned (failure) for the specific software workload.

### 3. The SDX Solution Architecture

SDX inverts this process using a "Virtualization First" approach:

1. Virtual Hardware: Compute subsystems are virtualized in the cloud (e.g., PAVE360), creating a "Golden Model" accessible to all suppliers.
2. The Digital Twin: The system is modeled as a dual structure:
    - [[SoT - Digital Twin#A. The Executable Digital Twin (The Physics)|Executable Digital Twin]] (Physics/Code)
    - [[SoT - Digital Twin#B. The Declarative Digital Twin (The Rules)|Declarative Digital Twin]] (Requirements)
3. Continuous Verification: [[SoT - Verification Threading]] runs millions of scenarios to validate the Executable against the Declarative.

### 4. Operational Model

- Exploration: High-level scenario testing to identify failing requirements.
- Optimization: Iterative adjustment of hardware parameters (bus speed, sensor resolution) to meet software needs.
- Hybrid Verification: Gradual replacement of virtual components with physical ECUs as the design matures.

---

See Also:

- [[Video - What is Software-Defined]]
- [[SoT - Digital Twin]]
- [[SoT - Verification Threading]]
