---
aliases: ["MOC Pragmatism vs Rigour"]
confidence: ""
created: 2025-12-19T13:18:01Z
criteria: "Links to canonical SoT notes defining the core principles of this conflict."
epistemic: ""
exclusions: "Implementation details of specific projects."
last_reviewed: ""
modified: 2026-01-03T10:19:38+00:00
purpose: ""
review_interval: ""
scope: "The core conflict between building software quickly (pragmatism) and building it correctly (rigour)."
see_also: []
source_of_truth: []
status: ""
tags: ["map", "mental-model", "philosophy", "software-engineering"]
title: MOC - The Trade-off Between Pragmatism and Rigour in Software Engineering
type: "map"
uid: 
updated: 
---

> **Inclusion criteria:** Links must be to canonical, stable SoT notes that define a core aspect of the pragmatism-rigour spectrum.

This map organizes the core Source of Truth notes related to the fundamental conflict between developing software with speed and agility versus developing it with mathematical correctness and provable safety.

## 1. The Central Conflict

This defines the core trade-off and the two opposing philosophies.

- [[SoT - Pragmatism vs Rigour in Software]]

## 2. The Pragmatic Approach: Velocity and "Good Enough"

This branch explores the mindset and tools that prioritize shipping functional software quickly.

- **Core Philosophy:** SoT - The "Worse is Better" Philosophy explains why simple, imperfect systems often win in the marketplace.
- **Language Model:** [[SoT - Padded Cell vs Nanny Languages]] provides a framework for classifying languages based on their safety approach, with "Padded Cell" languages embodying pragmatism.
- **Case Study (Rust):**
  - [[SoT - Rust's Design Philosophy]] analyzes Rust as a major case study in pragmatic, engineering-led design.
  - [[SoT - Rust's Ownership Model]] details its novel, non-theoretical approach to memory safety.
- **Linking Strategy:** [[SoT - Static vs Dynamic Linking]] discusses the trade-offs, where the pragmatic choice of static linking prioritizes portability over long-term system security.

## 3. The Rigorous Approach: Correctness by Construction

This branch explores the mindset and tools that allow for building provably correct software, accepting a higher upfront cost for long-term stability.

- **Core Philosophy:** [[SoT - Dependent Types in Software]] defines the ultimate goal of rigour: encoding logic into types to make illegal states unrepresentable.
- **Formal Models:**
  - [[SoT - Quantitative Type Theory]] presents the formal theory for resource management that systems like Rust approximate.
  - [[SoT - Region-Based Memory Management]] is the formal concept that underpins systems like Rust's lifetimes.
- **Practical Implications:**
  - [[SoT - Runtime Guards vs Compile-Time Proofs]] directly contrasts the pragmatic and rigorous approaches to error handling.
  - [[SoT - Optimization via Function Fusion]] explains how theoretically-grounded languages can perform more powerful, algebraic optimizations than those that rely on low-level optimizers.
