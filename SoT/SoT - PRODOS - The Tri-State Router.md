---
alias: [Input Processing Logic, Metabolic States, Tri-State Router]
aliases: []
confidence: 5/5
created: 2025-12-06T03:00:00Z
epistemic: 
last-synthesis: 2025-12-07
last_reviewed: 2025-12-07
modified: 2025-12-10T12:00:00Z
purpose: "To define the routing logic that classifies both Inputs (Ingress) and Outputs (Egress) into Kinetic (Action), Static (Storage), or Dynamic (Thinking) states."
quality-markers: ["Addresses edge cases like Projects.", "Defines the three metabolic states.", "Provides clear routing logic table.", "Covers both Ingress (Inbox) and Egress (HEAD)."]
related-soTs: ["[[SoT - PRODOS - Problem-Solution Map]]", "[[SoT - PRODOS (System Architecture)]]"]
review_interval: "6 months"
see_also: []
source_of_truth: true
status: stable
supersedes: []
tags: [gtd, prodos, sot, source/lib, system_design, workflow]
title: SoT - PRODOS - The Tri-State Router
type: SoT
uid: 
updated: 
---

## 1. Definitive Statement

> [!definition] Definition
> The **Tri-State Router** is the core metabolic classification logic of PRODOS. It functions in two modes:
> 1.  **Ingress Controller:** Classifies raw inputs (Inbox) during the "Clarify" phase.
> 2.  **Build Pipeline:** Classifies the outputs of thinking (HEAD Notes) during the "Compile" phase.
>
> In both cases, it assigns the item to one of three states: **Kinetic (Action)**, **Static (Storage)**, or **Dynamic (Thinking)**.

## 2. Context & Scope
-   **Problem Solved:** Prevents "To-Do List Rot" (stagnant projects) and "Note Graveyards" (dead thoughts).
-   **Application:** 
    -   *Ingress:* Applied to `00_Inbox` items.
    -   *Egress:* Applied to the "Exit Block" of `HEAD` notes.
-   **System Boundaries:** Replaces binary "Actionable?" choices with trinary metabolic states.

## 3. The Routing Logic (Reference Table)

| Input State | Definition | System Destination | Artifact Created | Primary Action |
| :--- | :--- | :--- | :--- | :--- |
| **1. Kinetic**<br>(Action) | Requires physical movement, coding, or communication. The steps are known. | **GTD Engine**<br>(Todoist) | **Task** | Execution |
| **2. Static**<br>(Storage) | Established fact, reference material, or completed specification. No action required. | **Library**<br>(Obsidian `30_Library`) | **SoT (LIB) Note** | Retrieval |
| **3. Dynamic**<br>(Thinking) | Unresolved problem, confusion, design requirement, or active learning. | **Workbench**<br>(Obsidian `20_Thinking`) | **HEAD Note** | Synthesis |

## 4. Mode 1: The Input Router (Ingress)

*Applied to: Inbox, Emails, Slack Messages.*

### Path A: The Kinetic Path (Action)
*Test:* "Do I know exactly what the next physical action is?"
-   **Yes:** It is Kinetic.
-   **Implementation:**
    -   **Micro-Task (<2 mins):** Do it immediately.
    -   **Task:** Create Todoist entry (or Sync via Obsidian tag `#todoist`).
    -   **Project:** Create Project Dashboard in `10_Actions` AND a recurring task to review it.

### Path B: The Static Path (Storage)
*Test:* "Is this information finished and created by someone else?"
-   **Yes:** It is Static.
-   **Implementation:**
    -   Move file to `30_Library/31_Resources`.
    -   Rename to `LIB - [Topic]`.

### Path C: The Dynamic Path (Thinking)
*Test:* "Do I need to figure this out before I can do it?" or "Am I confused?"
-   **Yes:** It is Dynamic.
-   **Implementation:**
    -   Instantiate **HEAD Note** in `20_Thinking`.
    -   Create a "Pointer Task" in Todoist: "Process HEAD note on [Topic]."

---

## 5. Mode 2: The Output Router (Build Pipeline)

*Applied to: The bottom of a HEAD Note (Thinking Session).*

When you finish a thinking session, you must "Route" the note to close the loop.

### Path A: Kinetic (Action)
*Context:* "I figured it out. I just need to do it."
-   **Action:** Extract the verifiable Next Action to Todoist.
-   **Outcome:** **Archive/Delete** the HEAD note. (The value is now in the Task).

### Path B: Static (Storage)
*Context:* "I learned a fact or defined a spec."
-   **Action:** Merge the insight into the relevant `SoT` Note.
-   **Outcome:** **Archive/Delete** the HEAD note. (The value is now in the SoT).

### Path C: Dynamic (Still Thinking)
*Context:* "I am paused. I need to resume this later."
-   **Action:** 
    1.  **Serialize State:** Write a "Save State" sentence ("Stopped at X, need to check Y").
    2.  **Pointer Task:** Create a task in Todoist ("Thinking: Resume [[HEAD - Timestamp]]").
-   **Outcome:** **Keep Active.** The note remains in `20_Thinking`.

---

## 6. Edge Cases & Hybrid States

### The "Project" Hybrid

Projects often appear to be both Thinking and Action.

-   **Rule:** The **Project Note** acts as the parent container.
-   **Split:**
    -   The *Plan* lives in a linked **HEAD Note** (`HEAD - Migration Strategy`).
    -   The *Actions* live in **Todoist** (synced to the Project Note).
    -   The *Specs* live in linked **LIB Notes** (`SoT - Azure Networking`).

### The "Stuck" Task

If a task in Todoist sits for >2 weeks without being done (procrastination):

-   **Diagnosis:** It has been misclassified. It is likely a **Dynamic** problem disguised as a **Kinetic** task.
-   **Correction:** Delete the Task. Create a **HEAD Note**: "Why am I resisting Task X?".

## 6. Verification & Maintenance

> [!check] Verification Log
> -   **Primary Source:** Internal System Architecture Design ([[SoT - PRODOS (System Architecture)]]).
> -   **Last Verified:** 2025-12-08
> -   **Maintenance Action:** Audit `00_Inbox` weekly. If >10 items remain, the Router is blocked.
