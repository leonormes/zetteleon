---
aliases: [Adaptive Routines, Energy-Based Tiered Routines, The Honeyman Method]
confidence: 5/5
created: 2025-12-10T12:00:00Z
epistemic:
last_reviewed: 2025-12-10
modified: 2025-12-10T19:59:40Z
purpose: To define the adaptive routine protocol used in ProdOS to manage energy fluctuations and prevent system abandonment.
related-soTs: ["[[SoT - Bridging the Intention-Action Gap]]", "[[SoT - Process Primacy (Systems Over Goals)]]", "[[SoT - PRODOS - Action Management (GTD)]]"]
review_interval: 6 months
see_also: ["[[MOC - The Honeyman Method]]"]
source_of_truth: true
status: stable
tags: ["adhd", "energy-management", "prodos", "routines"]
title: SoT - The Honeyman Method (Adaptive Routines)
type: SoT
uid:
updated:
---

## 1. Definition

The **Honeyman Method** is an adaptive, three-tiered framework for managing routines. It replaces binary "Success/Failure" models with a dynamic scope that scales based on available executive function.

> [!definition] Core Principle
> Consistency is not achieved by performing the *same action* every day, but by maintaining the *same habit loop* at varying intensities.
>
> **The Goal:** To prevent the "All-or-Nothing" collapse where a single missed "Ideal" day leads to total system abandonment.

---

## 2. The Three Tiers (Scope Definition)

### Tier 1: The Ideal (High Energy / Flow)
-   **Context:** High dopamine, low stress, ample time.
-   **Scope:** The "Pinterest Perfect" version of the routine. Includes stretch goals and optimisation tasks.
-   **ProdOS Role:** **Expansion.** This is when we process the "Someday/Maybe" list or do deep architectural work.
-   **Trap:** Do not treat this as the "Standard." It is a bonus state.

### Tier 2: The Most Likely (Baseline / Maintenance)
-   **Context:** Average day. Normal energy, some friction.
-   **Scope:** The core essential tasks needed to maintain status quo. No frills.
-   **ProdOS Role:** **Maintenance.** Clearing the Inbox, checking the Daily Note, moving the critical needle.
-   **Metric:** "Did I keep the system running?"

### Tier 3: The Minimum (Low Energy / Survival)
-   **Context:** Executive dysfunction, burnout, illness, or crisis.
-   **Scope:** The absolute "Minimum Viable Action" (MVA) required to keep the lights on.
    -   *Example:* "Brush teeth" (instead of 10-step skincare).
    -   *Example:* "Open Obsidian Daily Note" (instead of writing 500 words).
-   **ProdOS Role:** **Survival.** The goal is purely **Continuity**. Keeping the chain unbroken prevents the "Wall of Awful" from rebuilding.
-   **Critical Rule:** Doing the Minimum counts as 100% Success. **No Guilt.**

---

## 3. Integration into ProdOS (System Usage)

In the context of [[SoT - PRODOS (System Architecture)]], the Honeyman Method serves as the **Variable Scope Controller** for the Action Loop.

### The Problem: Static Systems vs. Dynamic Biology

Standard productivity systems (GTD) assume a constant level of agentic capacity. ADHD brains fluctuate wildly. When a rigid system meets a low-energy day, the system breaks.

### The Solution: Dynamic Acceptance Criteria

We integrate the Honeyman Method into the **Daily Plan** and **Hansei** phases.

#### A. The Morning Handshake (Capacity Check)

When engaging with the system (via [[SoT - PRODOS - Knowledge Synthesis (Thinking)|Daily Note]]), the user explicitly declares their **Energy Tier**:

1.  **Assess:** "My battery is at 20%." (Tier 3).
2.  **Adjust Scope:** The LLM (or user) filters the specific Todoist view:
    -   *Tier 1:* Show all `@Next` tasks + `@Project` work.
    -   *Tier 2:* Show only `P1` (Critical) tasks.
    -   *Tier 3:* Show only `P1` + `@Quick` (MVA).

#### B. The "Next Test" Definition

When defining a "Next Test" in a [[HEAD Note]], the scope of the test must match the current tier.

-   *Idea:* "I need to fix the server architecture."
-   *Tier 1 Action:* "Draft full schema diagram."
-   *Tier 3 Action:* "Open the repo and read the README." (Micro-Stepping).

#### C. Preventing the "Shame Spiral"

The Honeyman Method provides a **Pre-Approved Fallback**. When you switch to Tier 3, you are not "failing" to do Tier 1; you are "successfully executing" Tier 3. This semantic shift preserves dopamine and prevents the shame-based avoidance that kills systems.

---

## 4. Implementation Example (The Daily Ritual)

| Routine Phase | Tier 1 (Ideal) | Tier 2 (Standard) | Tier 3 (Minimum) |
| :--- | :--- | :--- | :--- |
| **Capture** | Process all Inboxes (Email, Slack, Todoist) to Zero. | Clear only Todoist Inbox. Check Email for fires. | Dump brain to Daily Note. Ignore others. |
| **Plan** | Time-block entire day. Set 3 Major Outcomes. | List top 3 priorities. No time-blocking. | Pick **ONE** thing. Do it. |
| **Synthesis** | Process `HEAD` notes. Merge insights to `SoT`. | Review one `HEAD` note. | Skip. |
| **Review** | Full Hansei Reflection (Journaling). | Bullet point log of day. | "I survived." (Checkmark). |

---

## 5. Related Concepts
-   **[[200_projects/ProdOS/lower energy capacity|Lower Energy Capacity Principles]]:** The foundational principles that this method operationalizes.
-   **[[SoT - Bridging the Intention-Action Gap]]:** Uses Tier 3 to overcome Activation Energy.
