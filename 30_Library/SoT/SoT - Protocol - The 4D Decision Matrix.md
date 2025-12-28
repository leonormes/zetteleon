---
aliases: ["4D System", "Delegate Delete Delay Do"]
confidence: "5/5"
created: 2025-12-23T22:44:23Z
epistemic: "strategy"
last_reviewed: "2025-12-23"
modified: 2025-12-28T18:49:16+00:00
purpose: "To provide a rapid, four-step decision filter for processing incoming tasks and reducing decision fatigue."
review_interval: "6 months"
see_also: ["[[SoT - Action Management Framework]]", "[[SoT - PRODOS - The Tri-State Router]]"]
source_of_truth: []
status: "stable"
tags: ["adhd", "decision-making", "gtd", "productivity", "protocol"]
title: SoT - Protocol - The 4D Decision Matrix
type: "Protocol"
uid: 
updated: 
---

## 1. Goal: Rapid Ingress Refinement

The **4D Matrix** is the tactical filter used during the **Refine** phase of the ProdOS workflow. It allows the operator to quickly clear an Inbox by assigning one of four "fates" to every item.

---

## 2. The Four Decisions (The 4 Ds)

### I. Do (Kinetic - Immediate)

- **Criteria:** The task takes < 2 minutes or is a critical "Right Now" priority.
- **Action:** Execute immediately. Do not record it.
- **ProdOS Path:** **Kinetic Path (Micro-Task).**

### II. Delegate (Kinetic - Assigned)

- **Criteria:** The task can be performed more effectively by someone else.
- **Action:** Hand off the task with clear expectations and deadlines.
- **Implementation:** Create a `@Waiting` task in Todoist to track the handoff.

### III. Defer / Delay (Dynamic or Scheduled)

- **Criteria:** The task is necessary but not for "Now."
- **Action:**
    - If it requires more clarity: Route to **Dynamic Path** (Create a HEAD note).
    - If it is a clear task for later: Route to **Kinetic Path** (Schedule in Todoist).
    - If it's a "Maybe": Move to **Someday/Maybe**.

### IV. Delete (Zero-Toil)

- **Criteria:** The task does not align with current goals, is redundant, or the cost of doing it exceeds the value.
- **Action:** Ruthlessly remove.
- **The ADHD Test:** "What happens if I *don't* do this?" If the answer is "Nothing critical," delete it to free up **Psychic RAM**.

---

## 3. The ADHD Advantage

The 4D System is particularly effective for the neurodivergent mind:

- **Predictability:** Provides a fixed algorithm for processing, reducing the cognitive load of "deciding what to decide."
- **Impulse Control:** Forces a moment of "Metacognitive Friction" before jumping into a new task.
- **Momentum:** The "Do" and "Delete" actions provide immediate "small wins" that generate dopamine for the remaining list.

---

## 4. Integration with Tri-State Router

The 4D Matrix acts as the **"Micro-Logic"** inside the **Ingress Controller**:

| 4D Decision | Tri-State Route | Outcome |
|:--- |:--- |:--- |
| **Do** | Kinetic | Done / Completed. |
| **Delegate** | Kinetic | `@Waiting` Task in Todoist. |
| **Defer** | Dynamic | `HEAD` Note or Pointer Task. |
| **Delete** | N/A | Purgatory / Removed. |

---

## 5. Summary

Use the 4D Matrix to maintain a **Zero Maintenance Baseline**. Every item in your Inbox is either done, delegated, deferred, or deleted. Nothing is allowed to "sit" and rot.
