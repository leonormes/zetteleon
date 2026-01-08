---
aliases: ["Rich Hickey", "Simple Made Easy", "Simplicity vs Complexity"]
confidence: "5/5"
created: 2026-01-07T00:00:00Z
epistemic: "Design Philosophy"
last_reviewed: 
modified: 2026-01-08T10:49:41+00:00
purpose: "To define Rich Hickey's distinction between Simple (Unentangled) and Easy (Familiar), and why Simplicity is the objective of Engineering."
review_interval: "1 year"
see_also:
  - "[[SoT - The Data-Centric Philosophy]]"
source_of_truth: []
status: "Stable"
tags: ["complexity", "design", "rich-hickey", "simplicity"]
title: SoT - Simple Made Easy (Rich Hickey)
type: "SoT"
uid: 
updated: 
---

## SoT - Simple Made Easy (Rich Hickey)

> **The Axiom:** **Simple!= Easy.**
> -   **Simple (Objective):** One braid. Unentangled. A tool that does one thing.
> -   **Easy (Subjective):** Near at hand. Familiar. "I can type it fast."

### 1. The Cost of "Easy"

We choose "Easy" (ORMs, Frameworks) because it is fast to _start_. But "Easy" often braids concerns (Data + Logic + View).

- **Result:** The Complected System. You cannot change A without breaking B.

### 2. The Discipline of Simplicity

Simplicity requires **Up-Front Design**. You must mentally untangle the threads.

- **Data:** Just Data (Maps/Lists).
- **State:** Managed References.
- **Logic:** Pure Functions.

### 3. Complecting (Braid)

To "complect" is to weave together.

- **Threading + Logic:** Complected.
- **Objects + State:** Complected.
- **Goal:** Decomplect. Keep things separate so they can be composed.
