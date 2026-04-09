---
aliases: [Data-Centric Design Index, Engineering MOC, SDLC MOC, The Data-First Hub]
created: 2025-02-15T07:24:57Z
last_synthesis: 2026-04-02
modified: 2026-04-09T08:11:07+00:00
source_of_truth: true
status: evergreen
synthesis-count: 3
tags: [architecture, data-centric, engineering, prodos/moc, programming, sdlc]
title: MOC - Data-Centric Software Engineering
type: map
---

## 1. The Logical Thread: "Structure is Truth"

The philosophy of Data-First Programming follows an unbroken chain from the physical constraints of hardware to the high-level modeling of logic.

| Level | Role | Source of Truth | Core Principle |
|:--- |:--- |:--- |:--- |
| 1. The Axiom | Worldview | [[SoT - The Data-Centric Philosophy]] | "Data Dominates Code." Linus Torvalds: "Bad programmers worry about the code. Good programmers worry about data structures." |
| 2. The Theory | Mathematics | [[MOC - Type Theory]] | "Applied Category Theory." Modeling structure with Sum/Product types and mathematical invariants. |
| 3. The Physics | Performance | [[SoT - Data-Oriented Design]] | "Hardware is the Platform." Cache-aligned data layout (SoA vs. AoS) for massive performance gains. |
| 4. The Practice | Methodology | [[SoT - Type-Driven Development (The Torvalds Loop)]] | "The Torvalds Loop." A 4-phase protocol: Shape $\to$ Access $\to$ Invariants $\to$ Logic. |

---

## 2. The Development Curriculum: "Data-First" Mindset

- The Torvalds Loop: The strict protocol where Logic is the _last_ consideration.
- Parse, Don't Validate: Move validation to the boundary; transform raw input into "Trusted Types."
- Making Invalid States Unrepresentable: Using the type system to mathematically prove system integrity.
- Good Taste: [[SoT - The Data-Centric Philosophy#4. The Litmus Test: \"Good Taste\"|The Indirect Pointer Pattern]]—solving edge cases via structure rather than `if` statements.

---

## 3. Data Architectures & Systems (Lines of Thought)

### A. Infrastructure & Systems (Infrastructure as Data)

_Core Map: [[MOC - Data-Centric Infrastructure]]_

- GitOps: [[200_projects/10_Infrastructure/gitops/git index.md|The Git Data Perspective]]—Git as a Content-Addressable Merkle DAG.
- Secrets: [[SoT - Vault KV Data Structure]]—Vault as a Versioned Prefix Trie.
- Integrity: [[SoT - Vault KV Data Structure#6. The Integrity Model (Merkle Tree)|Merkle Trees]]—Recursive integrity proofs and binary identity.

### B. Networking & IAM (Networking as State Transport)

_Core Map: [[MOC - Data-Centric Networking]]_

- The Theory: [[SoT - The Data-Centric Theory of Networking]]—Routing as prefix-trie traversal.
- Encapsulation: [[SoT - The Architecture of Packet Encapsulation (TCP-IP)]]—The recursive nesting of data containers.
- Identity: [[SoT - Data-Centric IAM in Zero Trust]]—AuthZ as a data-processing operation on the PDP/PEP.

### C. Internals & High Performance

_Core Map: [[MOC - Data-Oriented Structures & Internals]]_

- The Structures: [[SoT - High-Performance Data Structures]]—Ring Buffers, Flattened Trees, CSR Graphs.
- The Safe Pointer: [[SoT - Slot Map (Generational Arena)]]—Referencing data without pointers.
- The Engine: [[SoT - Database Internals for Systems Programmers]]—Storage Pages, B-Trees, and MVCC.

---

## 4. Engineering Prompts

- [[Prompt - Data-Centric Coding Assistant]]—Enforcing the Data-First Design Loop.
- [[Prompt - Senior Systems Architect (Data-Centric Refactor)]]—Refactoring technical fragments into rigorous SoT.

---

## 5. Related Domains

- [[MOC - Interpretation of References]]—Mapping symbols (code) to memory/reality.
- [[SoT - Simple Made Easy (Rich Hickey)]]—Decomplecting state and logic.
