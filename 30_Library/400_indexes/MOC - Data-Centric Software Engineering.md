---
aliases: [Data-Centric Design Index, Engineering MOC, SDLC MOC]
confidence: 5/5
created: 2025-02-15T07:24:57Z
epistemic: architecture
last_reviewed: 2025-12-26
modified: 2025-12-26T20:47:04+00:00
purpose: The central index for cultivating Data-Centric Software Engineering skills and methodology.
review_interval: 6 months
see_also: ["[[SoT - Data-Centric Software Engineering]]"]
source_of_truth: true
status: stable
tags: [data-centric, programming, sdlc]
title: MOC - Data-Centric Software Engineering
type: map
uid:
updated:
---

## Core Principles (The SoT)

> [!definition] The Paradigm Shift
> Moving beyond syntax-specific details to focus on the shape, flow, and transformation of data.

- **[[SoT - Data-Centric Software Engineering]]**—*The definitive guide to the mindset: State over Logic, Structure over Syntax.*
- **The Conservation Law of Complexity**—*Complexity must reside somewhere; shifting it from procedural logic to structural schema makes systems robust.*
- **Structure as Epistemology**—*How you represent the data defines how you view the problem (e.g., Trie for routing, DAG for history).*

---

## 1. The Development Curriculum

A structured path to developing the "Data-First" mindset.

*See **[[SoT - Data-Centric Software Engineering#2. The Core Curriculum|The Core Curriculum]]** for detailed study paths.*

- **Deepen Understanding:** Moving beyond memorization to trade-off analysis (Time vs. Space complexity).
- **Data Modelling:** Mapping reality to Entity-Relationship diagrams before writing code.
- **Language-Agnostic Thinking:** Solving problems in pseudocode to decouple logic from implementation syntax.
- **The Torvalds Loop:** A four-phase design protocol: Shape -> Access -> Invariants -> Logic.

---

## 2. Applied Data-Centricity (The Stack)

Applying these principles beyond code to the entire engineering stack.

### A. Infrastructure & Systems

- **Secrets:** [[Vault KV Data Structure First Principles]]—*Vault as a Versioned Trie of JSON Documents.*
- **Integrity:** [[Vault KV Data Structure First Principles#What is a Merkel tree|Merkle Trees]]—*Recursive integrity proofs and binary identity.*
- **Control Planes:** [[Vault KV Data Structure First Principles#Do k8s controllers utilise Merkel tree|Reconciliation vs. Sync]]—*Functional equivalence (K8s) vs. Cryptographic identity (Vault).*
- **Infrastructure:** [[SoT - Data-Centric Infrastructure (Terraform)]]—*Treating configuration as a Data Schema.*

### B. Networking & IAM

- **Boundaries:** [[HEAD - The Demarcation Gap]]—*Defining the logical interface (Handshake) between Application and Transit.*
- **Networking:** [[SoT - The Data-Centric Theory of Networking]]—*Routing as state transport.*
- **Identity:** [[SoT - Data-Centric IAM in Zero Trust]]—*AuthZ as a data-processing operation.*

### C. Development Lifecycle

- **Source Control:** [[SoT - The Data Architecture of Source Control (Git)]]—*Version control as a Merkle DAG.*
- **Commits:** [[The Fundamental Misconception Commits as Diffs]]—*Understanding snapshots over changes.*

---

## 3. Related Domains

- **[[MOC - Interpretation of References]]**—*How symbols (Code) map to reality (Memory).*
- **[[HEAD - SDE Networking Responsibility Boundaries]]**—*The practical tension of infrastructure ownership.*

---

## 4. Tooling & Prompts

- **[[Prompt - Data-Centric Coding Assistant]]**—*Configuring LLMs to enforce the Data-First Design Loop.*
- **[[Prompt - Senior Systems Architect (Data-Centric Refactor)]]**—*Refactoring raw technical notes into rigorous SoT documents.*
- **[[Prompt - Data-Centric IDE Analysis]]**—*A specialized prompt for IDEs (Cursor, Copilot) to analyze code structure.*
