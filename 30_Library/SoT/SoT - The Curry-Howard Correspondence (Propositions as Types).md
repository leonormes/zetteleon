---
aliases: []
confidence: "5/5"
created: 2025-12-18T00:00:00Z
epistemic: "authoritative"
last_reviewed: "2025-12-18"
modified: 2025-12-28T09:56:09+00:00
purpose: "Defines the foundational isomorphism between mathematical logic and computer programming."
review_interval: "1 year"
see_also: ["[[SoT - Proof-Carrying Code via Simulated Dependent Types]]"]
source_of_truth: []
status: "stable"
tags: ["computer_science", "formal_methods", "logic", "type_theory"]
title: SoT - The Curry-Howard Correspondence (Propositions as Types)
type: "SoT"
uid: 
updated: 
---

## 1. Working Knowledge (Stable Foundation)

- **Definition:** The Curry-Howard Correspondence is the observation that **mathematical logic** and **computational types** are structurally identical. A program is a proof, and the type it satisfies is the proposition it proves.
- **The Isomorphism:**
  - **Proposition** $\iff$ **Type**
  - **Proof** $\iff$ **Program** (Inhabitant of the Type)
  - **Simplification of Proof** $\iff$ **Execution of Program** (Beta-reduction)
- **Logical Mapping:**
  - **Implication ($A \implies B$)** $\iff$ **Function ($A \to B$)**
  - **Conjunction ($A \land B$)** $\iff$ **Product Type (Tuple/Struct)**
  - **Disjunction ($A \lor B$)** $\iff$ **Sum Type (Enum/Union)**
  - **False ($\bot$)** $\iff$ **Empty Type (Void/Never)**
  - **Negation ($\neg A$)** $\iff$ **Function to Empty Type ($A \to \bot$)**

## 2. Current Understanding (Coherent Narrative)

### The Foundational Link

The Curry-Howard correspondence reveals that software architecture is not merely an engineering task but a logical one. When a developer defines a type, they are stating a mathematical proposition. When they write a function that satisfies that type, they are providing a constructive proof that the proposition is true.

### Constructive (Intuitionistic) Logic

Unlike classical logic, Curry-Howard relies on **Constructive Logic**. In this framework, you cannot claim a statement is true simply by showing its negation is impossible. You must provide a **construction** (a program).

- **Rejection of the Law of Excluded Middle:** In classical logic, $P \lor \neg P$ is always true. In computation, $P \lor \neg P$ is only "true" if you have a program that can *decide* which branch holds for any given input.
- **The Halting Problem:** The inability to assume every program returns a value directly mirrors the logical limit that not every proposition is provable/decidable.

### Architectural Consequence

This framework transforms the compiler from a syntax checker into a **Theorem Prover**. A program that type-checks is a logically consistent proof. Robust type systems (like those in Rust, Haskell, or Swift) allow architects to encode business rules as types, ensuring that any code that compiles is logically "sound" relative to those rules.

## 3. Understanding Layers (Progressive Abstraction)

- **Layer 1 (Basic Model):** Writing code is the same as proving math.
- **Layer 2 (Mapping):** Every common programming construct has a logical twin (e.g., an `if/else` on an Enum is a proof of a Disjunction).
- **Layer 3 (Deep Theory):** Type systems are formal languages for expressing Intuitionistic Logic. Proof simplification (computation) is the process of removing unnecessary steps from a proof.

## 4. Minimum Viable Understanding (MVU)

- **Proposition = Type**: A statement we want to prove.
- **Proof = Program**: The code that demonstrates the statement is true.
- **Computation = Proof Checking**: The compiler verifying that your code actually satisfies the requirements of the type.
- **Constructive Requirement**: To prove something, you must build it. You cannot assume $A \lor \neg A$ without a way to compute the result.

## 5. Tensions, Gaps, and Cross-SoT Coherence

- **Conflict with Classical Intuition:** Most developers think in classical logic ($A$ is either true or false). Learning to think constructively (can I *calculate* the truth of $A$?) is a significant cognitive shift.
- **Connection to Formal Verification:** This SoT provides the "Why" for [[SoT - Proof-Carrying Code via Simulated Dependent Types]]. If types are propositions, then encoding sizes into types is encoding a proof about memory safety.

## 6. Sources and Links

- **Source:** Computerphile - "Propositions as Types" (Thorsten Altenkirch).
- **Related:** [[Logicism (Mathematics as Extension of Logic)]], [[Intuitionism Rejects the Law of Excluded Middle]].
