---
aliases: [A-C-T Framework, Human-LLM-Human Sandwich, One-Note-Container, The Cognitive Loop, The Refinement Protocol]
confidence: 5/5
created: 2025-12-07T00:00:00Z
epistemic: 
last_reviewed: 
modified: 2025-12-08T11:11:32Z
purpose: "To define the standard operating procedure for converting amorphous thought into actionable outcomes using LLMs."
review_interval: 
see_also: []
source_of_truth: true
status: stable
supersedes: ["[[ADHD, LLMs, and PKM Balance]]"]
tags: [architecture, llm, prodos, sot, workflow]
title: SoT - PRODOS - The Cognitive Loop (A-C-T Framework)
type: SoT
uid: 
updated: 
---

## 1. Definitive Statement

> [!definition] Definition
> The **Cognitive Loop** (specifically the **A-C-T Framework**) is the standard ProdOS protocol for interacting with LLMs. It enforces a shift from "Information Collection" (divergent) to "Process Direction" (convergent).
>
> It mandates that **every** interaction with an LLM must be bounded by a pre-defined "Container" and must result in a specific, physical **Minimum Viable Action (MVA)**.

---

## 2. The Core Problem: The Collector's Fallacy

The ADHD brain is drawn to the dopamine hit of *acquiring* information, often mistaking this for *learning*. Combined with the infinite generation capabilities of LLMs, this leads to **Content Sprawl**: a vast library of unactioned text.

-   **The Failure Mode:** Using LLMs to "elaborate," "explore," or "tell me more," which generates infinite divergence.
-   **The Correction:** "Think like a man of action, act like a man of thought." Knowledge is inert until it is applied.

---

## 3. The Architecture: The Human-LLM-Human Sandwich

The workflow strictly enforces the user's role as the **Director**, not the Consumer.

1.  **Human (The Seed):** The user provides the raw, messy, amorphous input. This is the "Spark" or the "Struggle."
2.  **LLM (The Refiner/Converger):** The LLM processes the input *only* to structure it, filter it, or define the next step. It is banned from adding "fluff."
3.  **Human (The Artisan):** The user takes the output and performs the physical action (writing the note, running the command). The user *never* copy-pastes raw LLM output into the permanent Zettelkasten.

---

## 4. The Operational Workflow: The A-C-T Framework

To bypass analysis paralysis, all "thinking" sessions must follow this three-phase loop.

### Phase A: ACTION (Define the Goal)
-   **The Input:** Amorphous, vague anxiety or curiosity (e.g., "I need to fix my finances" or "I want to learn Kubernetes").
-   **The Question:** "What is the *single, specific action* this thinking is supposed to lead to?"
-   **The Role:** The LLM acts as a **Converger**.
-   **The Tool:** **Gemini Flash** (Fast, concise, decisive).
-   **The Output:** A **Minimum Viable Action (MVA)**. Not a plan, but the immediate next physical step (e.g., "List all income sources").

### Phase C: CONTAINER (Define the Boundary)
-   **The Constraint:** Before acting, the user must define the **One-Note-Container**.
-   **The Rule:** "I will create exactly *one* new atomic note, titled '[Title]', containing [Specific Data]."
-   **The Execution:** The user sets a timer (Time-Boxing) and performs the MVA. This is the "Act like a man of thought" phase—executing a deliberate, bounded task.

### Phase T: THOUGHT (Reflect & Synthesize)
-   **The Input:** The raw data or result generated in Phase C.
-   **The Role:** The LLM acts as a **Synthesizer**.
-   **The Tool:** **Gemini Pro** (Deep reasoning, complex analysis).
-   **The Prompt:** "Here is the data I generated. What is the single key insight? What is the logical next MVA?"
-   **The Output:** A validated **Atomic Note** for the Zettelkasten and the input for the next A-Phase.

---

## 5. Tactical Rules

### Model Selection Strategy
-   **Gemini Flash:** Use for **Phase A (Action)**. It prevents the "Encyclopedia Trap" by being too simple to generate sprawling essays. It forces binary choices and checklists.
-   **Gemini Pro:** Use for **Phase T (Thought)**. Use only when you have concrete data to analyze.

### The Zero-Toil Constraint
-   Never start an LLM chat without a defined **Container Goal** in Obsidian.
-   Never end a session without a **Next MVA**.
-   If the output is not actionable, it is waste.

---

## 6. Related Components
- [[SoT - PRODOS (System Architecture)]]
- [[SoT - PRODOS - Knowledge Synthesis (Thinking)]]
- [[HEAD - PKM as Version Control for Thinking]]
