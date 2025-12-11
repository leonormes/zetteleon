---
aliases: [GTD Implementation, ProdOS Action System, Task Architecture]
confidence: 4/5
created: 2025-12-08T00:00:00Z
epistemic: 
last_reviewed: 2025-12-08
modified: 2025-12-11T10:10:43Z
purpose: "To define the unified workflow for Task Management within ProdOS, specifically detailing the integration between Obsidian Tasks and Todoist via the Context Bridge."
related-soTs: ["[[SoT - PKM Confidence and Acceptance Criteria]]", "[[SoT - PRODOS (System Architecture)]]"]
review_interval: 
see_also: []
source_of_truth: true
status: stable
tags: [gtd, obsidian, prodos, system_design, tasks, todoist]
title: SoT - PRODOS - Action Management (GTD)
type: 
uid: 
updated: 
---

## 1. The Core Philosophy: Separation of Thinking and Doing

ProdOS distinguishes between two distinct modes of operation, which require distinct tools:

| Mode         | Tool         | Unit of Work             | Characteristics                              |
| :----------- | :----------- | :----------------------- | :------------------------------------------- |
| **Thinking** | **Obsidian** | `HEAD Note`, `Checklist` | High-context, messy, exploratory, volatile.  |
| **Doing**    | **Todoist**  | `Task`                   | Low-context, binary, time-sensitive, mobile. |

**The Failure Mode:** Trying to "manage tasks" in Obsidian (lacks friction-free mobile capture/reminders) or "do thinking" in Todoist (lacks depth).

**The Solution:** A bridging protocol that allows context to be created in Obsidian and execution to be managed in Todoist.

### The Neurological "Why": TPN vs. DMN

This separation is not just organizational; it is neurological.

- **Obsidian (Thinking)** engages the **Default Mode Network (DMN)**—the imaginative, wandering, and sometimes ruminative part of the brain.
- **Todoist (Doing)** is designed to engage the **Task Positive Network (TPN)**—the "get it done" mode.
- **The Bridge** acts as the switch. Moving to Todoist is an *external* trigger that shuts down the DMN (rumination) and activates the TPN (action).

### The Mindset: Purpose Over Feelings

- **Old Way:** "What do I *feel* like doing?" (leads to procrastination).
- **ProdOS Way:** "What *needs* to be done?" (Purpose-centered). The system separates the decision (Thinking phase) from the execution (Doing phase), so you don't have to negotiate with your feelings in the moment.

---

## 2. Tool Specification

### A. Obsidian Tasks Plugin (`obsidian-tasks-plugin`)

**Role:** The "Micro-Manager" of thinking.

**Usage:**

- Used strictly for **internal checklists** within a `HEAD` note or `Project` note.
- Best for breaking down a complex problem into atomic steps (e.g., "Step 1: finding the error log", "Step 2: grepping for the ID").
- **Key Syntax:** `- [ ] Task Description 📅 2025-12-08 ⏫`
- **Constraint:** Do *not* use this for tasks that must happen "later" or "elsewhere". If the computer closes, these tasks disappear from awareness.

### B. Todoist Context Bridge (`todoist-context-bridge`)

**Role:** The "Teleporter" to the Runtime.

**Usage:**

- Used to promote a finalized **Next Action** from a note into the Todoist system.
- **Function:** Creates a task in Todoist that contains a deep link (`obsidian://open...`) back to the specific block or header in the Obsidian note.
- **Why:** When the Todoist notification fires (e.g., "Call Client"), one click restores the full "Mental State" (the Obsidian Note) needed to execute the task.

---

## 3. The LLM Interaction Layer

The LLM (Claude/Gemini) acts as the **Refinement Engine** between these tools. It does not "click the buttons," but it prepares the data.

### 1. The "Linter" Role

The LLM scans `HEAD` notes for vague language.

- *Input:* `- [ ] Work on the report` (Vague, likely to procrastinate)
- *Refinement:* `- [ ] Draft the 'Executive Summary' section of the Q3 Report ⏳ 25m` (Specific, actionable)

### 2. The "Bridge" Preparation

The LLM identifies which tasks are "Blockers" or "External" and flags them for the Bridge.

- *Instruction:* "This task involves emailing X, push to Todoist."
- *Output:* The LLM formats the text to ensure the "Context Bridge" plugin captures the right summary.

---

## 4. The Process: From Vague Idea to ADHD-Friendly Action

This pipeline converts "Cognitive Fog" into "Binary Action."

### Phase 1: Capture (The Dump)

- **Action:** User dumps raw thought into `Daily Note` or `Inbox`.
- **State:** `Messy`, `Emotional`, `Unstructured`.
- *Example:* "I need to fix the server patching, it's a mess."

### Phase 2: Refine (The Thinking)

- **Action:** LLM (Command: `/refine`) extracts this to a `HEAD` note (`HEAD - Server Patching.md`).
- **Activity:**

1.  **Explode:** Break the vague fear into concrete steps using **Obsidian Tasks**.

    - `- [ ] Check current uptime`
    - `- [ ] List failed patches`

2.  **Isolate:** Identify the *single* first physical action.

- **State:** `Structured`, `Atomic`.

### Phase 3: Bridge (The Commitment)

- **Action:** User invokes `Todoist Context Bridge` on the primary Next Action.
- **Result:**
    - Obsidian: Task marked with `[Todoist Synced]` (or icon).
    - Todoist: New task "List failed patches" with link `[[HEAD - Server Patching]]`.
- **State:** `Scheduled`, `Externalized`.

### Phase 4: Engage (The Doing)

- **Action:** Todoist reminds user. User clicks link.
- **Protocol:**

    1.  **Environment Check:** Before starting, remove temptations (phone, tabs).
    2.  **Context Restore:** Click link -> Obsidian opens `HEAD - Server Patching`.
    3.  **The "Just Start" Heuristic:** If resistance hits ("I'll do it later"), use the **Implementation Intention**:

        > *"IF I say 'I'll do it later', THEN I will just do 30 seconds of this task."*

    4.  **Pomodoro:** Set timer for 25m. Focus only on the "Next Small Action."

- **Execution:** User performs the task, checks off in Obsidian (for record) and Todoist (for dopamine).

---

## 5. Temporal Integration

GTD manages **Inventory** (What to do), but it does not manage **Capacity** (When to do it). To prevent "List Overwhelm," ProdOS integrates strict Temporal Management.

-   **See Canonical Protocol:** **[[SoT - Temporal Management (Blocking and Boxing)]]**

### The Integration Point
-   **The Bridge:** When moving a task to Todoist, you must decide its temporal fate:
    -   **P1 (Critical):** Must be **Time Blocked** on the Calendar immediately.
    -   **P2 (Important):** Must have a defined **Time Box** (Duration) attached (e.g., `[25m]`).
    -   **P3 (Routine):** Batched into a "Shallow Work" block.

---

## 6. Dashboards & Views (Obsidian)

To support this workflow, the following Dataview dashboards are critical:

### A. The "Incubation" Dashboard

*Shows potential projects that lack a defined Next Action.*

```dataview

TABLE without id file.link as "Project", file.cday as "Created"

FROM "003_workbench"

WHERE !contains(file.tasks.status, " ") AND file.name != "HEAD - Template"

SORT file.cday desc

```

### B. The "Active Loops" Dashboard

*Shows open loops that are currently in progress (Obsidian Tasks).*

```dataview

TASK

FROM "003_workbench"

WHERE !completed

GROUP BY file.link

```

### C. The "Resistance" Monitor

*Highlights tasks that have been rolled over or are vague (High Risk of ADHD Paralysis).*

```dataview

TASK

WHERE !completed AND created < (date(today) - dur(7 days))



```

## 7. Acceptance Criteria (Definition of Done)

A task is properly processed only when:

1.  **It starts with a Verb.** (Call, Write, Run, Buy)
2.  **It has a defined Context.** (At Computer, At Shop)
3.  **It exists in Todoist** IF it cannot be done *right now*.
4.  **It links back** to the thinking that generated it.
5.  **It is Real Work, not Meta-Work.** (Planning about planning is forbidden. The task must "move the ball" in the real world.)
