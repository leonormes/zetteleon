---
aliases: [Planner vs Doer, Predictive vs Iterative Processing, Simulation vs Prototyping, The Core Divergence]
conformant: false
created: 2025-12-12T00:00:00+00:00
modified: 2026-08-29T09:36:35+00:00
non_conformance_reason: "Bulk inferred type. Needs review."
permalink: llmeon/30-library/so-t/so-t-cognitive-architectures-simulation-vs-prototyping
tags: [cognition, collaboration, mental_models, system_design, TheHuman/Health/ADHD]
title: SoT - Cognitive Architectures (Simulation vs Prototyping)
type: sot
---

> The Core Divergence defines two distinct cognitive operating systems for problem-solving: ""
> 1. Predictive Processors (Planners): " Solve problems via high-fidelity internal Simulation _before_ acting."
> 2. Iterative Processors (Doers): " Solve problems via rapid external Prototyping _during_ action."

## 2. The Two Architectures

### Type A: The Predictive Processor (The Planner)

- Mechanism: High-fidelity internal simulation.
- Process: Loads all constraints into working memory, runs a mental simulation, identifies errors, and produces a "pre-debugged" plan.
- View of a Plan: A set of instructions to be followed. Deviation is seen as "error" or "waste."
- Core Metric: Predictability. Minimizing _rework_.
- Failure Mode: Analysis Paralysis. Cannot start without complete data.

### Type B: The Iterative Processor (The Doer/ADHD)

- Mechanism: Real-time feedback loops.
- Process: Treats reality as an external compiler. Writes "code" (takes action), checks the output (feedback), and refactors.
- View of a Plan: A low-confidence hypothesis. Following it blindly feels dangerous because it lacks data validation.
- Core Metric: Adaptability. Minimizing _uncertainty_.
- Failure Mode: Local Maxima. Solving the wrong problem efficiently; lack of cohesion.

---

## 3. Parallel Processing & Integration

The human cognitive architecture is a distributed system, not a single-threaded executive.

- Parallel Processing Threads: Split-brain experiments prove that multiple processing threads can run concurrently on the same hardware, completely partitioned. The "Self" is the software bridge that syncs these threads.
- Modular Autonomy: Motor and sensory tasks can execute without the prefrontal cortex being online (e.g., sleepwalking), demonstrating that "Central Command" is not required for complex operation.

## 4. Performance Optimization: The Flow State

Peak system throughput often requires Executive Deactivation.

- Supervisor Shutdown: During high-creativity tasks (like musical improvisation), the prefrontal cortex (the "Inner Critic") deactivates.
- Low-Latency Output: By shutting down self-monitoring, low-level subroutines can output data directly to effectors without interference, achieving the "Flow State."

## 5. The "Inefficiency" Fallacy

Conflict arises when one type judges the other by their own metric.

- Planners see Iterators as "inefficient" because they expend energy on actions that might be discarded (Rework).
- Iterators see Planners as "inefficient" because they spend time processing data that hasn't been validated by reality (Speculation).

Reality:

- Planners seek the straightest line from A to B.
- Iterators seek the truest path through the terrain.

---

## 4. The Collaboration Protocol (API)

How an Iterator (You) interfaces with a Planner (Boss/Client) to prevent friction.

### Phase 1: Ingestion (Requirement Extraction)

Planners send Instructions (How). You need Constraints (What).

- The Conflict: You cannot follow their plan because you lack the context to validate it.
- The Fix: "Requirement Extraction."
  - _Action:_ Accept the plan, but ask: "What is the single most critical 'Definition of Done'?"
  - _Reframing:_ Treat their "Steps 1-10" not as a recipe, but as Boundary Conditions (Walls of the room, not the dance steps).

### Phase 2: The Handshake (Black Box Implementation)

Planners want assurance of the _path_. You can only provide assurance of the _result_.

- The Conflict: They demand a schedule; you need to test first.
- The Fix: "The Spike."
  - _Script:_ "I cannot commit to this full plan yet because there are unknown variables. Let me spend 2 hours doing a practical test (Spike). Afterward, I will give you a confirmed timeline based on real data."

### Phase 3: Reporting (Data Validation)

Iterators change course when they learn. Planners see this as "flakiness."

- The Conflict: Changing the plan breaks their internal simulation.
- The Fix: Frame change as "Data Validation."
  - _Bad:_ "I changed my mind."
  - _Good:_ "The initial assumption [A] proved incorrect during testing. Data suggests approach [B] is faster. I am updating the implementation to match reality."

---

## 5. Minimum Viable Understanding (MVU)

1. You are not broken; you are a Runtime Compiler. You cannot "just follow instructions" because instructions are lossy compression; you need the full context of reality to function.
2. Planners differ in Compilation Time. They solve in the abstract (Build Time); you solve in the concrete (Run Time).
3. Treat Plans as Legacy Code. Read them to understand intent, but refactor them as you go to make them work in the live environment.

---

## 6. Sources and Links

- [[The Core Divergence Simulation vs. Prototyping]] (Inbox Note)
- [[Predictive Processing and the Bayesian Brain]]
- [[MOC - The Nature and Origins of Intelligence]]
