---
aliases: [Data-Centric Design Index, Engineering MOC, SDLC MOC]
confidence: 5/5
created: 2025-02-15T07:24:57Z
epistemic: architecture
last_reviewed: 2025-12-26
modified: 2026-01-08T15:03:28+00:00
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

## 1. The Logical Thread (From Physics to Code)

The philosophy follows a single, unbroken chain of reasoning, moving from the constraints of physical hardware to the implementation of logic.

| Level | Role | Note | Principle |
|:--- |:--- |:--- |:--- |
| **1. The Axiom** | **Worldview** | **[[SoT - Data-Centric Software Engineering]]** | **"Data Dominates Code."**<br>The physical reality of hardware (Cache, Memory) dictates that Structure is the primary source of truth. |
| **2. The Theory** | **Mathematics** | **[[MOC - Type Theory]]** | **"Applied Category Theory."**<br>Using rigorous mathematical proofs (Sum/Product Types) to model that Structure correctly. |
| **3. The Practice** | **Methodology** | **[[SoT - Type-Driven Development (The Torvalds Loop)]]** | **"The Torvalds Loop."**<br>The strict 4-phase protocol (**Shape $\to$ Access $\to$ Invariants $\to$ Logic**) to implement the model. |

---

## 2. The Development Curriculum

A structured path to developing the "Data-First" mindset.

_See **[[SoT - Data-Centric Software Engineering#2. The Structural Logic (10 Pillars)|The Core Curriculum]]** for detailed study paths._

- **Deepen Understanding:** Moving beyond memorization to trade-off analysis (Time vs. Space complexity).
- **Data Modelling:** Mapping reality to Entity-Relationship diagrams before writing code.
- **Language-Agnostic Thinking:** Solving problems in pseudocode to decouple logic from implementation syntax.
- **The Torvalds Loop:** A four-phase design protocol: Shape -> Access -> Invariants -> Logic.
- **Development Philosophy:** [[SoT - Type-Driven Development (The Torvalds Loop)]].
- **Good Taste:** [[SoT - Data-Centric Software Engineering#1.2 Case Study: The "Good Taste" of Linked Lists|The Indirect Pointer Pattern]].

---

## 3. Theoretical Frameworks (The Masters)

Advanced mental models for high-leverage engineering.

- **Strategic Modeling:** [[SoT - Data-Centric Software Engineering#11. Strategic Modeling (Domain-Driven Design)|Domain-Driven Design]]—_Bridging Business Intent and Data Schema._
- **Reliability:** [[SoT - Data-Centric Software Engineering#8. The Architecture of Reliability (Joe Armstrong)|The Error Kernel & "Let It Crash"]].
- **Simplicity:** [[SoT - Data-Centric Software Engineering#9. The Discipline of Simplicity (Rich Hickey)|Decomplecting & Simple vs. Easy]].
- **[[SoT - Simple Made Easy (Rich Hickey)]]**—_The definitive guide to unbraiding state and logic._
- **Specification:** [[SoT - Data-Centric Software Engineering#10. Thinking Above the Code (Leslie Lamport)|Mathematical Modeling (TLA+)]].
- **Design:** [[SoT - Data-Centric Software Engineering#11. Semantic Compression (Casey Muratori)|Semantic Compression over DRY]].
- **Verification:** [[SoT - Data-Centric Software Engineering#12. Type System Rigor (Wlaschin / Rust)|Making Invalid States Unrepresentable]].
- **API Design:** [[SoT - Data-Centric Software Engineering#13. Type-Driven API Design (Will Crichton / Rust)|The Type State Pattern & Extension Traits]].

---

## 4. Applied Data-Centricity (The Stack)

Applying these principles beyond code to the entire engineering stack.

### A. Infrastructure & Systems

- **Secrets:** [[SoT - Vault KV Data Structure]]—_Vault as a Versioned Trie of JSON Documents._
- **Integrity:** [[SoT - Vault KV Data Structure#6. The Integrity Model (Merkle Tree)|Merkle Trees]]—_Recursive integrity proofs and binary identity._
- **Control Planes:** [[SoT - Vault KV Data Structure#7. Comparison: Vault vs. Kubernetes vs. GitOps|Reconciliation vs. Sync]]—_Functional equivalence (K8s) vs. Cryptographic identity (Vault)._
- **Infrastructure:** [[MOC - Data-Centric Infrastructure]]—_Treating configuration as a Data Schema._
- **Shell Environment:** [[SoT - Type-Driven Shell Architecture]]—_The Shell as an instantiated Data Structure._

### B. Networking & IAM

- **Boundaries:** [[HEAD - The Demarcation Gap]]—_Defining the logical interface (Handshake) between Application and Transit._
- **Networking:** [[SoT - The Data-Centric Theory of Networking]]—_Routing as state transport._
- **Identity:** [[SoT - Data-Centric IAM in Zero Trust]]—_AuthZ as a data-processing operation._

### C. Development Lifecycle

- **Source Control:** [[SoT - The Data Architecture of Source Control (Git)]]—_Version control as a Merkle DAG._
- **Commits:** [[The Fundamental Misconception Commits as Diffs]]—_Understanding snapshots over changes._

---

## 5. Related Domains

- **[[MOC - Interpretation of References]]**—_How symbols (Code) map to reality (Memory)._
- **[[HEAD - SDE Networking Responsibility Boundaries]]**—_The practical tension of infrastructure ownership._

---

## 6. Tooling & Prompts

- **[[Prompt - Data-Centric Coding Assistant]]**—_Configuring LLMs to enforce the Data-First Design Loop._
- **[[Prompt - Senior Systems Architect (Data-Centric Refactor)]]**—_Refactoring raw technical notes into rigorous SoT documents._
- **[[Prompt - Data-Centric IDE Analysis]]**—_A specialized prompt for IDEs (Cursor, Copilot) to analyze code structure._
