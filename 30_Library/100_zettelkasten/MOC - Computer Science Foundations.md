---
aliases: [Computing MOC, CS MOC, Software Engineering MOC, Tech Stack MOC]
confidence: 5/5
created: 2025-12-13T09:15:00Z
epistemic:
last-reviewed: 2025-12-13
last_reviewed: 
modified: 2025-12-13T09:03:20Z
purpose: A unified Map of Content for the fundamental principles of Computer Science, Software Architecture, and Cloud Infrastructure.
review_interval: 6 months
see_also: ["[[MOC - Linux Container Primitives]]", "[[MOC - Software Architecture Principles]]"]
source_of_truth: []
status: stable
tags: [architecture, cloud, computer-science, moc, software-engineering]
title: MOC - Computer Science Foundations
type: map
uid:
updated:
---

## Overview

This map organizes the Source of Truth (SoT) notes covering the stack from physical hardware to abstract software architecture and cloud infrastructure.

---

## 1. The Hardware Layer (The Machine)

The physical reality of computation.

-   **[[SoT - The Functional Anatomy of a Computer]]** — *The Core.* The IPOS Model (Input, Processing, Output, Storage) and the shift to SoC architecture.
-   **[[SoT - Mass vs Weight and the Kilogram]]** — *The Physics.* Foundational measurement concepts underpinning physical reality.

---

## 2. Software Architecture Principles (The Code)

How we structure logic to manage complexity.

-   **[[SoT - Namespacing in Computing]]** — *The Boundaries.* Conflict avoidance and modularity across all domains (Kernel, DNS, Code).
-   **[[SoT - Atomicity and Loose Coupling]]** — *The Component.* Defining "True Atomicity" as independence with a standardized interface.
-   **[[SoT - Information Hiding (Parnas)]]** — *The Interface.* Encapsulating design decisions to allow independent evolution of modules.
-   **[[SoT - Code Duplication and Refactoring]]** — *The Hygiene.* Kent Beck's taxonomy of duplication and the imperative to refactor.
-   **[[SoT - Software Configuration Management Patterns]]** — *The Control.* Versioning everything as the foundation of reproducibility.

---

## 3. Cloud & Infrastructure (The Network)

How we scale and connect systems.

-   **[[SoT - Cloud Networking Core Components]]** — *The Pipe.* Gateways, Routing, and Addressing in AWS/Azure.
-   **[[SoT - Automated Cloud Resource Hibernation]]** — *The Cost.* Strategies for managing cloud spend through scheduled dormancy.
