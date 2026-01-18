---
aliases: ["Computing MOC", "CS MOC", "Software Engineering MOC", "Tech Stack MOC"]
confidence: "5/5"
created: 2025-12-13T09:15:00Z
epistemic: "null"
last-reviewed: "2025-12-13T00:00:00.000Z"
last_reviewed: "null"
modified: 2026-01-08T15:03:28+00:00
purpose: ""
review_interval: "6 months"
see_also: ["[[MOC - Linux Container Primitives]]", "[[MOC - Software Architecture Principles]]"]
source_of_truth: []
status: "stable"
tags: ["cloud", "computer-science", "SoftwareEngineering", "SoftwareEngineering/Architecture"]
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

- **[[SoT - The Functional Anatomy of a Computer]]**—_The Core._ IPOS model, I/O delegation (MMIO vs Port-Mapped), Interrupts, and the evolution of System-on-Chip (SoC) topology.
- **[[SoT - Mass vs Weight and the Kilogram]]**—_The Physics._ Foundational measurement concepts underpinning physical reality.

---

## 2. Software Architecture Principles (The Code)

How we structure logic to manage complexity.

- **[[SoT - Namespacing in Computing]]**—_The Boundaries._ Conflict avoidance and modularity across all domains (Kernel, DNS, Code).
- **[[SoT - Atomicity and Loose Coupling]]**—_The Component._ Defining "True Atomicity" as independence with a standardized interface.
- **[[SoT - Information Hiding (Parnas)]]**—_The Interface._ Encapsulating design decisions to allow independent evolution of modules.
- **[[SoT - Code Duplication and Refactoring]]**—_The Hygiene._ Kent Beck's taxonomy of duplication and the imperative to refactor.
- **[[SoT - Software Configuration Management Patterns]]**—_The Control._ Versioning everything as the foundation of reproducibility.

---

## 3. Functional Systems & Type Theory (The Logic)

Theoretical foundations for robust logic and effect management.

- **[[SoT - Fundamentals of Mathematical Logic]]**—_The Basics._ Propositional logic, connectives, and quantifiers.
- **[[SoT - Mathematical Proof Techniques]]**—_The Methods._ Direct, Contrapositive, and Contradiction proofs.
- **[[SoT - The Algebra of Types (Cardinality and Isomorphism)]]**—_The Math._ Types as sums, products, and exponents.
- **[[SoT - TypeScript as a Proof Engine (Set Theory and Distributivity)]]**—_The Verification._ Using structural typing and set theory to hoist invariants to compile-time.
- **[[SoT - The Monad Design Pattern (Pipeline Abstraction)]]**—_The Architecture._ Decoupling business logic from control flow complexity using wrappers and binders.
- **[[SoT - Functional Effects (Effects as Data)]]**—_The Action._ Using Tag Unions to decouple effect description from execution for simulation testing and observability.

---

## 4. Cloud & Infrastructure (The Network)

How we scale and connect systems.

- **[[SoT - Cloud Networking Core Components]]**—_The Pipe._ Gateways, Routing, and Addressing in AWS/Azure.
- **[[SoT - Automated Cloud Resource Hibernation]]**—_The Cost._ Strategies for managing cloud spend through scheduled dormancy.

---

## 5. Scripting & Automation (The Glue)

The languages and patterns used to orchestrate systems.

- **[[SoT - Bash Scripting]]**—_The Shell._ Core patterns for safe process orchestration and file manipulation (Quoting, Arrays, IFS).
- **[[SoT - Shell Automation and IPC]]**—_The Workflow._ Event-driven logic (Signals, Traps, FS Watching) for reactive terminal environments.
