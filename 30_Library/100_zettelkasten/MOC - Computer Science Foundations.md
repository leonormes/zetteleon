---
aliases: ["Computing MOC", "CS MOC", "Software Engineering MOC", "Tech Stack MOC"]
confidence: "5/5"
created: 2025-12-13T09:15:00Z
epistemic: "null"
last-reviewed: "2025-12-13T00:00:00.000Z"
last_reviewed: "null"
modified: 2025-12-27T20:41:18+00:00
purpose: ""
review_interval: "6 months"
see_also: ["[[MOC - Linux Container Primitives]]", "[[MOC - Software Architecture Principles]]"]
source_of_truth: []
status: "stable"
tags: ["architecture", "cloud", "computer-science", "software-engineering"]
title: MOC - Computer Science Foundations
type: "map"
uid: 
updated: 
---

## Overview

This map organizes the Source of Truth (SoT) notes covering the stack from physical hardware to abstract software architecture and cloud infrastructure.

---

## 1. The Hardware Layer (The Machine)

The physical reality of computation.

- **[[SoT - The Functional Anatomy of a Computer]]**—*The Core.* IPOS model, I/O delegation (MMIO vs Port-Mapped), Interrupts, and the evolution of System-on-Chip (SoC) topology.
- **[[SoT - Mass vs Weight and the Kilogram]]**—*The Physics.* Foundational measurement concepts underpinning physical reality.

---

## 2. Software Architecture Principles (The Code)

How we structure logic to manage complexity.

- **[[SoT - Namespacing in Computing]]**—*The Boundaries.* Conflict avoidance and modularity across all domains (Kernel, DNS, Code).
- **[[SoT - Atomicity and Loose Coupling]]**—*The Component.* Defining "True Atomicity" as independence with a standardized interface.
- **[[SoT - Information Hiding (Parnas)]]**—*The Interface.* Encapsulating design decisions to allow independent evolution of modules.
- **[[SoT - Code Duplication and Refactoring]]**—*The Hygiene.* Kent Beck's taxonomy of duplication and the imperative to refactor.
- **[[SoT - Software Configuration Management Patterns]]**—*The Control.* Versioning everything as the foundation of reproducibility.

---

## 3. Functional Systems & Type Theory (The Logic)

Theoretical foundations for robust logic and effect management.

- **[[SoT - The Algebra of Types (Cardinality and Isomorphism)]]**—*The Math.* Types as sums, products, and exponents.
- **[[SoT - TypeScript as a Proof Engine (Set Theory and Distributivity)]]**—*The Verification.* Using structural typing and set theory to hoist invariants to compile-time.
- **[[SoT - The Monad Design Pattern (Pipeline Abstraction)]]**—*The Architecture.* Decoupling business logic from control flow complexity using wrappers and binders.
- **[[SoT - Functional Effects (Effects as Data)]]**—*The Action.* Using Tag Unions to decouple effect description from execution for simulation testing and observability.

---

## 4. Cloud & Infrastructure (The Network)

How we scale and connect systems.

- **[[SoT - Cloud Networking Core Components]]**—*The Pipe.* Gateways, Routing, and Addressing in AWS/Azure.
- **[[SoT - Automated Cloud Resource Hibernation]]**—*The Cost.* Strategies for managing cloud spend through scheduled dormancy.

---

## 5. Scripting & Automation (The Glue)

The languages and patterns used to orchestrate systems.

- **[[SoT - Bash Scripting]]**—*The Shell.* Core patterns for safe process orchestration and file manipulation (Quoting, Arrays, IFS).
- **[[SoT - Shell Automation and IPC]]**—*The Workflow.* Event-driven logic (Signals, Traps, FS Watching) for reactive terminal environments.
