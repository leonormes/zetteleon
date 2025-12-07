---
aliases: []
confidence: 5/5
created: 2025-12-06T03:00:00Z
epistemic: 
last_reviewed: 
modified: 2025-12-06T09:00:13Z
purpose: 
review_interval: "6 months"
see_also: []
source_of_truth: []
source_url: "[[SoT - PRODOS (System Architecture)]]"
status: stable
tags: [prodos, source/lib, system_design, workflow]
title: SoT - PRODOS - The Tri-State Router
type: lib-sot
uid: 
updated: 
---

## 1. Definitive Statement

> [!definition] Definition
> The **Tri-State Router** is the input processing logic used during the "Clarify" phase of PRODOS. It classifies every input based on its **Metabolic State** (Kinetic, Static, or Dynamic) rather than its topic, assigning it to the specific processing engine designed to handle that state.

## 2. Context & Scope
- **Problem Solved:** Prevents "To-Do List Rot" (where vague projects like "Plan holiday" sit stagnant because they are actually thinking problems) and "Note Graveyards" (where actionable tasks get buried in text files).
- **Application:** Applied immediately after **Capture**. Every item in the `00_Inbox` or Daily Note must pass through this router.
- **System Boundaries:** This logic replaces the standard GTD binary choice ("Is it actionable? Yes/No") with a trinary choice.

## 3. The Routing Logic (Reference Table)

| Input State | Definition | System Destination | Artifact Created | Primary Action |
| :--- | :--- | :--- | :--- | :--- |
| **1. Kinetic**<br>(Action) | Requires physical movement, coding, or communication. The steps are known. | **GTD Engine**<br>(Todoist) | **Task** | Execution |
| **2. Static**<br>(Storage) | Established fact, reference material, or completed specification. No action required. | **Library**<br>(Obsidian `30_Library`) | **SoT (LIB) Note** | Retrieval |
| **3. Dynamic**<br>(Thinking) | Unresolved problem, confusion, design requirement, or active learning. | **Workbench**<br>(Obsidian `20_Thinking`) | **HEAD Note** | Synthesis |

## 4. Detailed Decision Tree & Examples

### Path A: The Kinetic Path (Action)
*Test:* "Do I know exactly what the next physical action is?"
- **Yes:** It is Kinetic.
- **Implementation:**
    - **Micro-Task (<2 mins):** Do it immediately.
    - **Task:** Create Todoist entry (or Sync via Obsidian tag `#todoist`).
    - **Project:** Create Project Dashboard in `10_Actions` AND a recurring task to review it.
- **Example 1:** "Email Data Provider about API limits." $\rightarrow$ **Task** (I know how to email).
- **Example 2:** "Run the Terraform apply command." $\rightarrow$ **Task** (I know the command).

### Path B: The Static Path (Storage)
*Test:* "Is this information finished and created by someone else?"
- **Yes:** It is Static.
- **Implementation:**
    - Move file to `30_Library/31_Resources`.
    - Rename to `LIB - [Topic]`.
- **Example 1:** "Invoice for December." $\rightarrow$ **Reference**.
- **Example 2:** "The official Kubernetes v1.30 Changelog." $\rightarrow$ **LIB Note** (I didn't write it, I just store it).

### Path C: The Dynamic Path (Thinking)
*Test:* "Do I need to figure this out before I can do it?" or "Am I confused?"
- **Yes:** It is Dynamic.
- **Implementation:**
    - Instantiate **HEAD Note** in `20_Thinking`.
    - Apply functional tag (`#type/bug`, `#type/design`).
    - Create a "Pointer Task" in Todoist: "Process HEAD note on [Topic]."
- **Example 1:** "Why is the API latency spiking?" $\rightarrow$ **HEAD Note** (I can't "fix" it yet; I must diagnose it).
- **Example 2:** "Plan the Kubernetes Migration." $\rightarrow$ **HEAD Note** (I need to design the plan before I can assign tasks).
- **Example 3:** "Bessie is avoiding homework." $\rightarrow$ **HEAD Note** (I need to understand the root cause).

## 5. Edge Cases & Hybrid States

### The "Project" Hybrid

Projects often appear to be both Thinking and Action.

- **Rule:** The **Project Note** acts as the parent container.
- **Split:**
    - The *Plan* lives in a linked **HEAD Note** (`HEAD - Migration Strategy`).
    - The *Actions* live in **Todoist** (synced to the Project Note).
    - The *Specs* live in linked **LIB Notes** (`SoT - Azure Networking`).

### The "Stuck" Task

If a task in Todoist sits for >2 weeks without being done (procrastination):

- **Diagnosis:** It has been misclassified. It is likely a **Dynamic** problem disguised as a **Kinetic** task.
- **Correction:** Delete the Task. Create a **HEAD Note**: "Why am I resisting Task X?".

## 6. Verification & Maintenance

> [!check] Verification Log
> - **Primary Source:** Internal System Architecture Design ([[SoT - PRODOS (System Architecture)]]).
> - **Last Verified:** 2025-12-06
> - **Maintenance Action:** Audit `00_Inbox` weekly. If >10 items remain, the Router is blocked.
