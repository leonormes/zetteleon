---
aliases: [K2A Framework, PRODOS, Productivity Operating System]
created: 2026-01-03T09:45:08+00:00
last_reviewed: 2026-01-12
modified: 2026-02-10T23:07:08+00:00
status: stable
tags: [adhd-optimization, execution, prodos, system-architecture]
tier: 1-Foundation
title: SoT - PRODOS Core Specification
type: SoT
---

## PRODOS Unified Specification

### 1. The Core Kernel

#### 1.1 The Definition

PRODOS is a Thinking Utility designed to convert Neural Potential into Kinetic Value. It treats the human as the Problem Definer and the system as the Executor.

- The Logic-Dopamine Mismatch: Logic provides direction (steering), but only Dopamine provides movement (fuel).
- The Metric: We measure Actions Taken. Motivation is a _result_ of action, not the cause.

#### 1.2 The Five Axioms

1. Utility Over Truth: If a note doesn't help you act, it is noise.
2. Throughput Over Storage: The system is for Compute, not a database.
3. Low Maintenance: Operates with < 10% Maintenance Load.
4. Context is Scarcity: Aggressively compact context to protect attention.
5. The 70% Rule: A 70% "perfect" action that is Done is superior to a 99% "perfect" action that is Active.

---

### 2. The Dopamine Engine (The PINCH Model)

When a task lacks intrinsic motivation, the Problem Definer must "gamify" the execution using one of these five drivers:

- Play / Passion: Can I make this fun?
- Interest: Can I learn something new?
- Novelty: Can I do this in a weird way?
- Challenge / Competition: Can I beat my high score/the clock?
- Hurry: Can I beat the alarm?

---

### 3. Execution Protocols

#### 3.1 The Scope-Lock & Starter Task

Before any action, you must define the Starter Task (Momentum Generator).

- Rule: The MVA must be so small it is impossible to fail (e.g., "Open the code editor").
- The Unit Test: The minimum verifiable criteria for success.

#### 3.2 The Ignition Protocol ("Heat")

If you are stuck in "Logic Mode," use one of these to generate movement:

1. Mystery: "I wonder if I can do this without using [Tool]?"
2. Urgency: "I have 5 minutes. How much can I get done?"
3. Spite: "I'm going to finish this to prove [Idea] wrong."

#### 3.3 The Checklist Protocol (The Firmware)

Use Instruction SoTs to offload working memory for complex tasks.

---

### 4. State Management (Cryosleep)

#### The Save State Syntax (#SAVESTATE)

- Timestamp: `YYYY-MM-DD-HHmm`.
- The Conflict: What perfectionist block did we hit?
- The Current State: The new hypothesis.
- The Next Test: The immediate next Starter Task.

---

### 5. Data Schema

- HEAD Notes: Active thinking and Decision Tracing.
- SoT Notes: Canonical Truth and Instruction SoTs (Checklists).
- The Context Cache (.ai/): Machine-readable memory for the AI Executor.
