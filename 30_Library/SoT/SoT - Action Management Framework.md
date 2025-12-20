---
aliases: [Action Management, Atomic Actions, Next Actions, GTD Framework, ProdOS Action, Task Architecture]
confidence: 5/5
created: 2025-12-20T12:00:00Z
epistemic: "framework"
last_reviewed: 2025-12-20
modified: 2025-12-20T12:30:00Z
purpose: "To provide a single, canonical Source of Truth for the principles, systems, and strategies for managing action, especially within an ADHD-aware context."
review_interval: 365
see_also:
- "[[SoT - The Cognitive Physiology of Task Execution]]"
- "[[SoT - Bridging the Intention-Action Gap]]"
- "[[MOC - Time Boxing for ADHD Brains]]"
- "[[SoT - Temporal Management (Blocking and Boxing)]]"
source_of_truth: true
status: "evergreen"
tags: [action, adhd, execution, gtd, prodos, productivity, framework, system_design, tasks, todoist]
title: SoT - Action Management Framework
type: "permanent"
uid: 20251220120000
updated: 
version: 2
---

## SoT - Action Management Framework

> **Core Question:** How do we transform abstract intent into concrete reality?

This Source of Truth (SoT) provides the complete framework for managing action within the ProdOS ecosystem. It is designed to counter **ADHD Task Initiation Deficits** by creating a robust system that separates thinking from doing and transforms vague intentions into executable steps.

---

### 1. The System: From Thought to Action

This section defines the canonical workflow for managing actions, based on Getting Things Done (GTD) principles adapted for ProdOS.

#### Core Philosophy: Separation of Thinking and Doing
ProdOS distinguishes between two modes of operation, which require distinct tools to prevent context collapse:

| Mode         | Tool         | Unit of Work             | Characteristics                              |
| :----------- | :----------- | :----------------------- | :------------------------------------------- |
| **Thinking** | **Obsidian** | `HEAD Note`, `Checklist` | High-context, messy, exploratory, volatile.  |
| **Doing**    | **Todoist**  | `Task`                   | Low-context, binary, time-sensitive, mobile. |

The primary failure mode is trying to "manage tasks" in Obsidian or "do thinking" in Todoist. The bridge protocol solves this.

#### The 4-Phase ProdOS Workflow
This pipeline converts "Cognitive Fog" into "Binary Action."

1.  **Phase 1: Capture (The Dump)**
    *   **Action:** User dumps raw thoughts, ideas, and worries into a trusted inbox (e.g., Daily Note, `00_Inbox`).
    *   **State:** `Messy`, `Emotional`, `Unstructured`.
    *   *Example:* "I need to fix the server patching, it's a mess."

2.  **Phase 2: Refine (The Thinking)**
    *   **Action:** The LLM or user refactors the messy thought into a structured `HEAD` note.
    *   **Activity:** The vague problem is broken down into a checklist of concrete, atomic steps using Obsidian Tasks. The *single* first physical action is identified.
    *   **State:** `Structured`, `Atomic`.

3.  **Phase 3: Bridge (The Commitment)**
    *   **Action:** The user invokes the `Todoist Context Bridge` on the primary Next Action.
    *   **Result:** A task is created in Todoist containing a deep link (`obsidian://...`) back to the `HEAD` note, preserving context.
    *   **State:** `Scheduled`, `Externalized`.

4.  **Phase 4: Engage (The Doing)**
    *   **Action:** A Todoist reminder fires. The user clicks the link, which restores the full context in Obsidian, and executes the single task.
    *   **State:** `Complete`.

#### System Tools
-   **Obsidian Tasks Plugin:** Used strictly for **internal checklists** within a `HEAD` note to break down a problem during the *Thinking* phase.
-   **Todoist Context Bridge:** The "teleporter" that promotes a finalized **Next Action** from Obsidian into the Todoist runtime, embedding a backlink to the source note.

---

### 2. The Atomic Unit: The 'What' of Action

The fundamental building block of all productive work is the **Atomic Action**. This is the answer to the question: "What is the very next physical thing I need to do?"

- **Core Principle:** [[The Action is the Atomic Unit of Productivity]]. It transforms vague intent into tangible progress.

#### The Four Essential Properties of an Atomic Action
An atomic action (or "Next Action" in GTD) must satisfy four properties to be valid:
1.  **Indivisible (Atomic):** It cannot be broken down further. "Write report" is not atomic; "Open Google Docs and create a new document titled 'Q4 Report'" is.
2.  **Physical & Visible:** It must be a real-world activity that produces an observable change.
3.  **Unambiguous Definition of Done:** [[Atomic Action Completion Must Be Binary and Instantly Verifiable|Completion is binary (0 or 1)]]. You either did it or you didn't.
4.  **Context-Specific:** [[Atomic Actions Are Context-Specific|It is tied to a specific tool, location, or person]] (e.g., `@computer`, `@phone`). Context tags are crucial for filtering and batching.

#### Composing Actions into Projects
Individual actions are composed into larger projects, which can be modeled as [[Action Sequences Form Directed Acyclic Graphs|Directed Acyclic Graphs (DAGs)]].

---

### 3. The Neurology: The 'Why' of Action

Understanding the neurological barriers to action, especially in ADHD, is key to designing a system that works.

- **Dopamine Dysregulation:** [[ADHD Causes Task Initiation Deficits Due to Dopamine Hyposensitivity|ADHD is characterized by dopamine hyposensitivity]], meaning the brain requires higher stimulation (novelty, urgency, interest) to initiate tasks.
- **Network Switching (TPN vs. DMN):** The brain struggles to switch from the wandering "thinking" state (Default Mode Network, DMN) to the focused "doing" state (Task Positive Network, TPN). Using an external tool like Todoist acts as a hard switch.
-   **Activation Energy:** [[Activation Energy is the Primary Barrier to ADHD Task Initiation|Activation Energy is the primary bottleneck]]. The entire system is designed to lower this barrier.
-   **Purpose Over Feelings:** The system separates the *decision* to do something (made during the calm, reflective "Thinking" phase) from the *execution*. This prevents in-the-moment negotiation with your feelings.

---

### 4. The Strategies: The 'Fix' for Inertia

These are techniques to lower activation energy and trigger action.

#### For Initiating Difficult Tasks (The Momentum Method)
- **[[SoT - Starter Tasks|Starter Tasks]]:** A special class of atomic action designed *only* to build momentum, not to make progress. They are a direct counter to high activation energy.
- **Artificial Ignition (Activation Fuel):** As detailed in [[SoT - Bridging the Intention-Action Gap]], this involves manufacturing dopamine by framing tasks with **Novelty, Urgency, Challenge, or Immersion (Pairing)**. These can be represented by `@Fuel_` tags in Todoist.

#### For Converting Thoughts into Actions (The Clarification Process)
- **[[Clarifying Stuff Into Actions Follows a Four-Step Process|The Four-Step Clarification Process]]** converts vague thoughts ("Stuff") into clear, atomic actions, externalizing decision-making.
- **Motion vs. Action:** It is critical to [[The Skill in Productivity is Not Confusing Motion for Action|distinguish preparatory "motion" from productive "action"]]. Motion can be a form of productive procrastination if not managed.

#### For Maintaining Project Momentum
- **Re-entry Rituals:** To combat the "always start fresh" loop, use a 10-minute ritual: read the project anchor note, run a dev environment command, and execute one small starter task.
- **Minimal Path to Demo (MPD):** For large projects, define the smallest set of features that delivers a demonstrable outcome. This provides a concrete "done" state and prevents scope creep.

---

### 5. Temporal Integration (The 'When')
A task list (inventory) without a sense of time (capacity) leads to overwhelm. All tasks bridged to Todoist must be assigned a temporal fate, as defined in **[[SoT - Temporal Management (Blocking and Boxing)]]**.
- **P1 (Critical):** Must be **Time Blocked** on the Calendar immediately.
- **P2 (Important):** Must have a defined **Time Box** (e.g., `[25m]`).
- **P3 (Routine):** Batched into a "Shallow Work" block.

---

### 6. Acceptance Criteria (Definition of Done)

A task is properly processed and ready for action *only when*:
1.  **It starts with a Verb.** (e.g., Call, Write, Run, Buy).
2.  **It has a defined Context.** (e.g., @computer, @shop).
3.  **It exists in Todoist** if it cannot be done *right now*.
4.  **It links back** to the Obsidian note that generated it.
5.  **It is Real Work, not Meta-Work.** (It must "move the ball" in the real world).