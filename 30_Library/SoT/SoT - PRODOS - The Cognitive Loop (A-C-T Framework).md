---
aliases: ["A-C-T Framework", "Human-LLM-Human Sandwich", "One-Note-Container", "The Cognitive Loop", "The Refinement Protocol"]
confidence: "5/5"
created: 2025-12-07T00:00:00Z
epistemic: ""
last_reviewed: ""
modified: 2025-12-26T14:56:21+00:00
purpose: "To define the standard operating procedure for converting amorphous thought into actionable outcomes using LLMs."
review_interval: "3 months"
see_also: ["[[ADHD", "and PKM Balance]]", "LLMs"]
source_of_truth: []
status: "stable"
tags: ["architecture", "llm", "prodos", "workflow"]
title: SoT - PRODOS - The Cognitive Loop (A-C-T Framework)
type: "SoT"
uid: 
updated: 
---

## 2. The Core Problem: The Collector's Fallacy

The ADHD brain is drawn to the dopamine hit of *acquiring* information, often mistaking this for *learning*. Combined with the infinite generation capabilities of LLMs, this leads to **Content Sprawl**: a vast library of unactioned text.

- **The Failure Mode:** Using LLMs to "elaborate," "explore," or "tell me more," which generates infinite divergence.
- **The Correction:** "Think like a man of action, act like a man of thought." Knowledge is inert until it is applied.

---

## 3. The Bergson Architecture (Theoretical Framework)

*Based on: "Think like a Man of Action, Act like a Man of Thought" (Henri Bergson).*

We reject the dichotomy between strategy and execution, viewing them as a continuous **CI/CD Cycle**.

### A. Thinking like a Man of Action (Compile-Time Optimisation)

*Goal: Reduce latency between idea and execution.*

- **The Interface Adapter:** Treat abstract ideals (e.g., "Justice", "Health") as *Interfaces*. You must write the **Implementation Class** (binary, concrete actions).
- **The Compute Budget (TTL):** Apply a strict **Time-To-Live** to decision-making to prevent infinite analysis loops.
- **The Sandbox (Unit Tests):** Use intellect to run "Unit Tests"—simulating specific execution paths and exception handling—rather than vague worrying.

### B. Acting like a Man of Thought (Runtime Monitoring)

*Goal: Maintain system stability during execution.*

- **The Daemon Process:** Run a lightweight background thread during action to monitor internal state (tone, pacing, distraction) without blocking the main execution thread.
- **The Control Loop (PID Controller):** Treat action as a closed-loop system. Constantly measure *Current State* vs. *Target State* and apply steering impulses in real-time.
- **Signal-to-Noise Ratio:** Every output must change the system state. Remove all "bloat" (hesitation, qualifiers).

---

## 4. The Architecture: The Human-LLM-Human Sandwich

The workflow strictly enforces the user's role as the **Director**, not the Consumer.

1. **Human (The Seed):** The user provides the raw, messy, amorphous input. This is the "Spark" or the "Struggle."
2. **LLM (The Refiner/Converger):** The LLM processes the input *only* to structure it, filter it, or define the next step. It is banned from adding "fluff."
3. **Human (The Artisan):** The user takes the output and performs the physical action (writing the note, running the command). The user *never* copy-pastes raw LLM output into the permanent System.

---

## 5. The Operational Workflow: The A-C-T Framework

To bypass analysis paralysis, all "thinking" sessions must follow this three-phase loop.

### Phase A: ACTION (Define the Goal)

- **The Input:** Amorphous, vague anxiety or curiosity (e.g., "I need to fix my finances" or "I want to learn Kubernetes").
- **The Question:** "What is the *single, specific action* this thinking is supposed to lead to?"
- **The Role:** The LLM acts as a **Converger**.
- **The Tool:** **Gemini Flash** (Fast, concise, decisive).
- **The Output:** A **Minimum Viable Action (MVA)**. Not a plan, but the immediate next physical step (e.g., "List all income sources").

#### The Momentum Loop Trigger (120-Second Commitment)

If Phase A is stalled due to "Task Size Anxiety":

- **The Rule:** You are only authorized to work for **2 minutes**.
- **Constraint:** Remove the threat of a "long, boring task."
- **Output:** After 120 seconds, you must choose: *Continue* (Dopamine high) or *Stop* (Save state via Tri-State Router).

### Phase C: CONTAINER (Define the Boundary)

- **The Constraint:** Before acting, the user must define the **One-Note-Container**.
- **The Rule:** "I will create exactly *one* new atomic note, titled '[Title]', containing [Specific Data]."
- **The Execution:** The user sets a timer (Time-Boxing) and performs the MVA. This is the "Act like a man of thought" phase—executing a deliberate, bounded task.

### Phase T: THOUGHT (Reflect & Synthesize)

- **The Input:** The raw data or result generated in Phase C.
- **The Role:** The LLM acts as a **Synthesizer**.
- **The Tool:** **Gemini Pro** (Deep reasoning, complex analysis).
- **The Prompt:** "Here is the data I generated. What is the single key insight? What is the logical next MVA?"
- **The Output:** A validated **SoT Note** for the Library and the input for the next A-Phase.

---

## 6. Tactical Rules

### Model Selection Strategy

- **Gemini Flash:** Use for **Phase A (Action)**. It prevents the "Encyclopedia Trap" by being too simple to generate sprawling essays. It forces binary choices and checklists.
- **Gemini Pro:** Use for **Phase T (Thought)**. Use only when you have concrete data to analyze.

### The Zero-Toil Constraint

- Never start an LLM chat without a defined **Container Goal** in Obsidian.
- Never end a session without a **Next MVA**.
- If the output is not actionable, it is waste.

---

## 7. Related Components

- [[SoT - PRODOS (System Architecture)]]
- [[SoT - PRODOS - Knowledge Synthesis (Thinking)]]
- [[HEAD - PKM as Version Control for Thinking]]
