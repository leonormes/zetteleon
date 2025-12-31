---
aliases: ["Action Management", "Atomic Action Protocol"]
confidence: "5/5"
created: 2025-12-20T20:01:29Z
epistemic: "strategy"
last_reviewed: "2025-12-23"
modified: 2025-12-30T17:49:08+00:00
purpose: "To provide a single, canonical Source of Truth for the principles, systems, and strategies for managing action, especially within an ADHD-aware context."
review_interval: "6 months"
see_also: ["[[SoT - Bridging the Intention-Action Gap]]", "[[SoT - PRODOS (System Architecture)]]", "[[SoT - Protocol - The Launch Sequence]]"]
source_of_truth: []
status: "stable"
tags: ["action", "adhd", "execution", "gtd", "prodos"]
title: SoT - Action Management Framework
type: "SoT"
uid: 
updated: 
---

> **Core Question:** How do we transform abstract intent into concrete reality?

## 1. The System: From Thought to Action

ProdOS strictly separates **Thinking** (Contextual/Exploratory) from **Doing** (Binary/Kinetic).

| Mode | Tool | Unit of Work | Characteristics |
|:--- |:--- |:--- |:--- |
| **Thinking** | **Obsidian** | `HEAD Note` | High-context, messy, exploratory, volatile. |
| **Doing** | **Todoist** | `MVA` | Low-context, binary, time-sensitive, mobile. |

### The 4-Phase ProdOS Workflow

1. **Capture (The Digital Dump):** Dump raw thoughts into `00_Inbox` or Daily Note. **Critical:** Decouple capture from organization. Do not tag, sort, or process during this phase. Just get it out of your head.
2. **Refine:** Use a `HEAD` note to identify the underlying Model and extract the first MVA.
3. **Bridge:** Use the *Todoist Context Bridge* to promote the MVA to the Todoist runtime with a link back to Obsidian.
4. **Engage:** Execute the single MVA when the reminder fires, restoring context via the deep link.

---

## 2. The Atomic Unit: The 'What' of Action

The fundamental building block of all productive work is the **Atomic Action**.

### 2.1 The Velocity Metric: Mean Time to First Action (MTTFA)

The primary KPI for ProdOS. It measures the time between identifying a task and executing the first micro-kinetic step.

- **The Rule:** Only "Compiled Binaries" (Executable MVAs) are permitted in the execution slot. No abstract intentions.

### 2.2 The Minimal Viable Action (MVA)

An MVA is a "momentum spark" designed to bypass initiation resistance.

1. **Micro-Temporal:** < 120 seconds.
2. **Kinetic:** Involves physical movement (e.g., "Open laptop").
3. **Binary:** Strictly True/False outcome.

### 2.3 Motion vs. Action: The Progress Diagnostic

A critical skill in ProdOS is distinguishing between **Motion** (preparatory activity) and **Action** (behavior that produces tangible results).

- **Motion:** Activities that create the *conditions* for action but do not directly move the project toward completion.
    *   *Includes:* Planning, strategizing, learning, brainstorming, and organizing.
    *   *The Trap:* Motion feels productive and safe, providing a false sense of accomplishment while avoiding the risk of failure inherent in action.
    *   *Deep Dive:* [[SoT - Motion vs Action (The Physics of Productivity)]]
- **Action:** Physical behavior that leads to a demonstrable outcome.
    - *The Test:* **"If I stopped this activity right now, would I be any closer to my goal?"**
    - *Example:* Outlining 20 ideas (Motion) vs. Writing one paragraph (Action).

---

## 3. The Atomic Standard: The Four Essential Properties

Every action promoted to the Todoist runtime must satisfy the **Atomic Standard**. If an action fails any of these tests, it must be refined.

### I. Indivisible (Atomic)

The smallest possible unit of work. It cannot be broken down further while remaining meaningful.

- **The Test:** Can this be completed in a single, uninterrupted session without waiting for external input?
- **Example:** "Open new document and title it 'Q4 Report'" (Correct) vs. "Write report" (Incorrect).

### II. Physical & Visible

A real-world activity that produces an observable change.

- **The Test:** Would an observer be able to *see* you doing this?
- **Example:** "Brainstorm strategy on whiteboard" (Correct) vs. "Decide on strategy" (Incorrect).

### III. Unambiguous Definition of Done

Completion is binary (0 or 1) and instantly verifiable.

- **The Test:** Can you definitively say "Yes, this is complete" without any uncertainty?
- **Example:** "Fill in revenue numbers in cells B15-B20" (Correct) vs. "Work on budget" (Incorrect).

### IV. Context-Specific

Tied to a specific tool, location, or person.

- **The Test:** What specific tool or location is required to complete this?
- **Example:** `@computer: Send status update email` (Correct) vs. "Send email" (Incorrect).

---

## 4. Maintenance & Strategy

### A. Re-entry Rituals

Combat the "always start fresh" loop with a 10-minute ritual: read the project anchor, run a dev command, and execute one small starter task.

### B. Capacity-Based Planning

- **High Gravity Days (20% Capacity):** Collapse the list to **one single MVA**. Hide all other tasks.
- **Utilization Capping:** Cap planned work at **60%** to allow for the "ADHD Tax."

### C. Violations and Fixes

| Violation | Example | Fix |
|:--- |:--- |:--- |
| **Too Large** | "Plan marketing campaign" | "List 10 potential themes in notebook" |
| **Not Physical** | "Consider options" | "Write pros/cons list for each option" |
| **Ambiguous** | "Improve documentation" | "Add code examples to endpoints 1-5" |
| **Missing Context** | "Call bank" | "@phone: Call Barclays to update address" |

---

## 5. Related Components

- [[SoT - PRODOS (System Architecture)]]
- [[SoT - Bridging the Intention-Action Gap]]
- [[SoT - Protocol - The Hemingway Bridge]]
