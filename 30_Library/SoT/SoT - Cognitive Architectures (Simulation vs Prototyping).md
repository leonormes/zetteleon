---
aliases: [Planner vs Doer, Predictive vs Iterative Processing, Simulation vs Prototyping, The Core Divergence]
confidence: 
created: 2025-12-12T00:00:00Z
epistemic: 
last-synthesis: 2025-12-12
last_reviewed: 
modified: 2025-12-12T18:21:13Z
purpose: To define the fundamental divergence in cognitive architectures between "Predictive Processors" (Simulation-first) and "Iterative Processors" (Action-first), providing a framework for collaboration and self-understanding.
review_interval: 6 months
see_also: ["[[Predictive Processing and the Bayesian Brain]]", "[[SoT - Learning Mechanisms]]", "[[SoT - Myopic Understanding]]"]
source_of_truth: true
status: stable
tags: [adhd, cognition, collaboration, mental_models, system_design]
title: SoT - Cognitive Architectures (Simulation vs Prototyping)
type: SoT
uid: 
updated: 
---

## 1. Definitive Statement

> [!definition] Definition
> The **Core Divergence** defines two distinct cognitive operating systems for problem-solving:
> 1.  **Predictive Processors (Planners):** Solve problems via high-fidelity internal **Simulation** *before* acting.
> 2.  **Iterative Processors (Doers):** Solve problems via rapid external **Prototyping** *during* action.
> 
> Neither is "inefficient"; they simply compile at different times. Planners compile at **Build Time** (optimizing for predictability). Iterators compile at **Run Time** (optimizing for adaptability).

---

## 2. The Two Architectures

### Type A: The Predictive Processor (The Planner)
-   **Mechanism:** High-fidelity internal simulation.
-   **Process:** Loads all constraints into working memory, runs a mental simulation, identifies errors, and produces a "pre-debugged" plan.
-   **View of a Plan:** A set of instructions to be followed. Deviation is seen as "error" or "waste."
-   **Core Metric:** **Predictability**. Minimizing *rework*.
-   **Failure Mode:** **Analysis Paralysis**. Cannot start without complete data.

### Type B: The Iterative Processor (The Doer/ADHD)
-   **Mechanism:** Real-time feedback loops.
-   **Process:** Treats reality as an external compiler. Writes "code" (takes action), checks the output (feedback), and refactors.
-   **View of a Plan:** A low-confidence hypothesis. Following it blindly feels dangerous because it lacks data validation.
-   **Core Metric:** **Adaptability**. Minimizing *uncertainty*.
-   **Failure Mode:** **Local Maxima**. Solving the wrong problem efficiently; lack of cohesion.

---

## 3. The "Inefficiency" Fallacy

Conflict arises when one type judges the other by their own metric.

-   **Planners** see Iterators as "inefficient" because they expend energy on actions that might be discarded (Rework).
-   **Iterators** see Planners as "inefficient" because they spend time processing data that hasn't been validated by reality (Speculation).

**Reality:**
-   **Planners** seek the straightest line from A to B.
-   **Iterators** seek the truest path through the terrain.

---

## 4. The Collaboration Protocol (API)

How an **Iterator** (You) interfaces with a **Planner** (Boss/Client) to prevent friction.

### Phase 1: Ingestion (Requirement Extraction)

Planners send **Instructions** (How). You need **Constraints** (What).

-   **The Conflict:** You cannot follow their plan because you lack the context to validate it.
-   **The Fix:** **"Requirement Extraction."**
    -   *Action:* Accept the plan, but ask: "What is the single most critical 'Definition of Done'?"
    -   *Reframing:* Treat their "Steps 1-10" not as a recipe, but as **Boundary Conditions** (Walls of the room, not the dance steps).

### Phase 2: The Handshake (Black Box Implementation)

Planners want assurance of the *path*. You can only provide assurance of the *result*.

-   **The Conflict:** They demand a schedule; you need to test first.
-   **The Fix:** **"The Spike."**
    -   *Script:* "I cannot commit to this full plan yet because there are unknown variables. Let me spend 2 hours doing a practical test (Spike). Afterward, I will give you a confirmed timeline based on real data."

### Phase 3: Reporting (Data Validation)

Iterators change course when they learn. Planners see this as "flakiness."

-   **The Conflict:** Changing the plan breaks their internal simulation.
-   **The Fix:** Frame change as **"Data Validation."**
    -   *Bad:* "I changed my mind."
    -   *Good:* "The initial assumption [A] proved incorrect during testing. Data suggests approach [B] is faster. I am updating the implementation to match reality."

---

## 5. Minimum Viable Understanding (MVU)

1.  **You are not broken; you are a Runtime Compiler.** You cannot "just follow instructions" because instructions are lossy compression; you need the full context of reality to function.
2.  **Planners differ in Compilation Time.** They solve in the abstract (Build Time); you solve in the concrete (Run Time).
3.  **Treat Plans as Legacy Code.** Read them to understand intent, but refactor them as you go to make them work in the live environment.

---

## 6. Sources and Links
-   [[The Core Divergence Simulation vs. Prototyping]] (Inbox Note)
-   [[Predictive Processing and the Bayesian Brain]]
