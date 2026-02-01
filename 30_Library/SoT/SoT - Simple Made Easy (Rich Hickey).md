---
aliases: ["Rich Hickey", "Simple Made Easy", "Simplicity vs Complexity"]
created: 2026-01-07T00:00:00Z
last_reviewed: 
modified: 2026-02-01T15:07:52+00:00
status: "Stable"
tags: ["complexity", "design", "rich-hickey", "simplicity"]
title: SoT - Simple Made Easy (Rich Hickey)
type: "SoT"
updated: 
---

## SoT - Simple Made Easy (Rich Hickey)

> The Axiom: Simple!= Easy.
> -   Simple (Objective): One braid. Unentangled. A tool that does one thing.
> -   Easy (Subjective): Near at hand. Familiar. "I can type it fast."

### 1. The Cost of "Easy"

We choose "Easy" (ORMs, Frameworks) because it is fast to _start_. But "Easy" often braids concerns (Data + Logic + View).

- Result: The Complected System. You cannot change A without breaking B.

### 2. The Discipline of Simplicity

Simplicity requires Up-Front Design. You must mentally untangle the threads.

- Data: Just Data (Maps/Lists).
- State: Managed References.
- Logic: Pure Functions.

### 3. Complecting (Braid)

To "complect" is to weave together.

- Threading + Logic: Complected.
- Objects + State: Complected.
- Goal: Decomplect. Keep things separate so they can be composed.
