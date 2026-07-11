---
aliases:
- Data-Centric Design Index
- Engineering MOC
- SDLC MOC
- The Data-First Hub
created: 2025-02-15 07:24:57+00:00
modified: 2026-07-04 10:51:11+00:00
permalink: llmeon/30-library/mo-c/moc-data-centric-software-engineering
source_of_truth: true
tags:
- architecture
- data-centric
- engineering
- prodos/moc
- programming
- sdlc
title: MOC - Data-Centric Software Engineering
prodos:
  kind: moc
  lifecycle: evergreen
  chronos:
    synthesis_count: 4
---


## 1. The Logical Thread: "Structure is Truth"

The philosophy of Data-First Programming follows an unbroken chain from the physical constraints of hardware to the high-level modeling of logic.

| Level | Role | Source of Truth | Core Principle |
|:--- |:--- |:--- |:--- |
| 1. The Axiom | Worldview | [[SoT - The Data-Centric Philosophy]] | "Data Dominates Code." Linus Torvalds: "Bad programmers worry about the code. Good programmers worry about data structures." |
| 2. The Constraint | Physics | [[SoT - Conservation of Complexity]] | "Tesler's Law." Complexity is conserved; it must be moved into Data/Schema to simplify Logic. |
| 3. The Theory | Mathematics | [[MOC - Type Theory]] | "Applied Category Theory." Modeling structure with Sum/Product types and mathematical invariants. |
| 4. The Physics | Performance | [[SoT - Data-Oriented Design]] | "Hardware is the Platform." Cache-aligned data layout (SoA vs. AoS) for massive performance gains. |
| 5. The Practice | Methodology | [[SoT - Type-Driven Development (The Torvalds Loop)]] | "The Torvalds Loop." A 4-phase protocol: Shape $\to$ Access $\to$ Invariants $\to$ Logic. |
| 6. The Audit | Behavioral | [[SoT - Dimensions of Code Understanding]] | "Behavioral Signal." Measuring understanding via structural adherence and coupling awareness. |

---

## 2. The Development Curriculum: "Data-First" Mindset

- The Torvalds Loop: The strict protocol where Logic is the _last_ consideration.
- Parse, Don't Validate: Move validation to the boundary; transform raw input into "Trusted Types."
- Making Invalid States Unrepresentable: Using the type system to mathematically prove system integrity.
- Information Hiding: [[SoT - Information Hiding (Parnas)]]—Encapsulating design decisions via abstract interfaces.
- Good Taste: [[SoT - The Data-Centric Philosophy#4. The Litmus Test: \"Good Taste\"|The Indirect Pointer Pattern]]—solving edge cases via structure rather than `if` statements.

---

## 3. Data Architectures & Systems (Lines of Thought)

### A. Infrastructure & Systems (Infrastructure as Data)

_Core Map: [[MOC - Data-Centric Infrastructure]]_

- GitOps: [[30_Library/200_projects/10_Infrastructure/gitops/git index.md|The Git Data Perspective]]—Git as a Content-Addressable Merkle DAG.
- Secrets: [[SoT - Vault KV Data Structure]]—Vault as a Versioned Prefix Trie.
- Integrity: [[SoT - Vault KV Data Structure#6. The Integrity Model (Merkle Tree)|Merkle Trees]]—Recursive integrity proofs and binary identity.

### B. Networking & IAM (Networking as State Transport)

_Core Map: [[MOC - Networking]]_

- The Theory: [[SoT - The Data-Centric Theory of Networking]]—Routing as prefix-trie traversal.
- Encapsulation: [[SoT - The Architecture of Packet Encapsulation (TCP-IP)]]—The recursive nesting of data containers.
- Identity: [[SoT - Data-Centric IAM in Zero Trust]]—AuthZ as a data-processing operation on the PDP/PEP.

### C. Internals & High Performance

_Core Map: [[MOC - Data-Oriented Structures & Internals]]_

- The Structures: [[SoT - High-Performance Data Structures]]—Ring Buffers, Flattened Trees, CSR Graphs.
- Type Mechanics: [[SoT - Rust Type Mechanics]]—Enums (Sum Types) and Structs (Product Types).
- The Safe Pointer: [[SoT - Slot Map (Generational Arena)]]—Referencing data without pointers.
- The Engine: [[SoT - Database Internals for Systems Programmers]]—Storage Pages, B-Trees, and MVCC.

---

## 4. Engineering Prompts

- [[Prompt - Data-Centric Coding Assistant]]—Enforcing the Data-First Design Loop.
- [[Knowledge Harvesting & Normalization Agent]]—Refactoring technical fragments into rigorous SoT.
- [[SoT - LLM Reasoning Obeys the Complexity Conservation Law]]—The LLM corollary to Tesler's Law.

---

## 5. Related Domains

- [[MOC - Interpretation of References]]—Mapping symbols (code) to memory/reality.
- [[SoT - Simple Made Easy (Rich Hickey)]]—Decomplecting state and logic.
- [[SoT - Parochial Code]]—_The failure mode resulting from a lack of architectural boundaries._
- [[SoT - Context Rot]]—_The entropy of high-level awareness in long sessions._
