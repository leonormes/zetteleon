---
aliases: [A-C-T Framework, Action-Container-Thought, Kinetic Valve, The Cognitive Loop]
created: 2026-04-04T12:30:00+00:00
last-synthesis: 2026-04-04
modified: 2026-07-13T08:52:52+00:00
permalink: llmeon/30-library/so-t/so-t-prodos-the-cognitive-loop-a-c-t-framework
tags: [adhd, cognitive-loop, framework, prodos, protocol]
title: SoT - PRODOS - The Cognitive Loop (A-C-T Framework)
type: sot
conformant: false
non_conformance_reason: "Bulk inferred type. Needs review."
---

## 1. Minimum Viable Understanding (MVU)

The A-C-T Framework is a convergent cognitive loop—the "Kinetic Valve" of ProdOS—designed to defeat [[collectors fallacy|The Collector's Fallacy]] (hoarding information) and Analysis Paralysis (over-planning).

It forces a rapid transition from abstract thinking to physical execution by breaking the workflow into three distinct, non-overlapping phases, converting "Neural Potential" into "Kinetic Value" (see [[SoT - PRODOS Core Specification#1.1 The Definition|PRODOS Core Specification]]).

---

## 2. The Problem: The Intention-Action Gap

For ADHD brains, the "Research Rabbit Hole" and "Information Hoarding" provide immediate dopamine rewards, creating a "productive-feeling avoidance" of actual work. A-C-T acts as a Prosthetic Executive Function (see [[SoT - Prosthetic Executive Function]]) by imposing a boundary between _Thinking_ and _Doing_.

---

## 3. The Three Phases

### A = ACTION (Define the Goal)

- Objective: Convert an "amorphous input" into a single, physical [[SoT - PRODOS Core Specification#3.2 The Scope-Lock & Starter Task (MVA)|Minimal Viable Action (MVA)]].
- Constraint: Do not "solve" the problem; only define the absolute smallest next step.
- Unit Test: Is it a physical, binary task so small it is impossible to fail? Can success be verified in < 120 seconds? (e.g., "Open the code editor," "Create the file `test.py`").

### C = CONTAINER (Define the Boundary)

- Objective: Create a dedicated One-Note-Container (a single Obsidian note or Todoist task) for the MVA.
- Constraint: Time-box the effort (using the [[SoT - PRODOS Core Specification#2. The Dopamine Engine (The PINCH Model)|PINCH Model]] for urgency). Work ONLY within this container to prevent scope creep. This is a "One-Note-Workbench."

### T = THOUGHT (Define the Insight)

- Objective: Reflect on the raw data or results generated during the Action phase.
- Constraint: Answer only two questions to trigger the next loop:
    1. What is the single most obvious insight from this data?
    2. What is the logical Next MVA suggested by this insight?

---

## 4. ProdOS Roles & Tools

- The LLM (The Thoughtful Action Partner): Acts as the "Convergent Tool" during Phase A (Decomposition) and Phase T (Synthesis). Its goal is NOT to give comprehensive answers, but to help the human find the _smallest next step_.
- The Human (The Problem Definer): Provides the "Amorphous Input" and performs the physical execution during Phase C.
- Tools:
    - Obsidian: For Phase C (One-Note-Container) and Phase T (Synthesis into SoTs).
    - Todoist: For Phase C (Execution/Time-boxing).
    - LLM: For Phase A (Framing the MVA) using the [[Thoughtful Action Partner]] system prompt.

---

## 5. Related Concepts

- [[MOC - ProdOS]]
- [[SoT - Illusion of Explanatory Depth (IoED)|The Collector's Fallacy]] (The problem A-C-T solves)
- [[SoT - PRODOS Core Specification]] (The underlying engine)
- [[SoT - Prosthetic Executive Function]] (The theory of externalized EF)
- [[Protocol - Vague-to-Action]] (How to execute Phase A)
