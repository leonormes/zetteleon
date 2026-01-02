---
epistemic: ""
source_of_truth: []
aliases: ["My Productivity System", "ProdOS", "The PRODOS Architecture"]
confidence: "5/5"
created: 2025-11-13T00:00:00Z
last_reviewed: "2026-01-01"
modified: 2026-01-01T21:31:28+00:00
purpose: "The Master Index Note and System Specification for PRODOS, defining its architecture as an ADHD-centric cognitive augmentation system."
review_interval: "3 months"
see_also: ["[[SoT - PRODOS - Action Management (GTD)]]", "[[SoT - PRODOS - Knowledge Synthesis (Thinking)]]", "[[SoT - PRODOS - Structure & Storage (PARA/PKM)]]", "[[SoT - The Extended Mind Thesis]]", "[[SoT - ADHD and Motivation]]"]
status: "stable"
tags: ["architecture", "hansei", "prodos", "system_design", "topic/health/adhd"]
title: SoT - PRODOS (System Architecture)
type: "SoT"
uid: 
---

## 1. Definitive Statement

> [!definition] Definition
> PRODOS operates as a **Thinking Utility**, not a storage archive. Its sole purpose is to **reduce the friction of cognition**.
>
> **The Metric:** We do not measure "notes created." We measure **clarity achieved** and **actions taken**.

### 1.1 Theoretical Foundation

ProdOS is an operational implementation of the **[[SoT - The Extended Mind|Extended Mind Thesis]]**. It treats the vault as constitutive of the user's cognitive machinery, utilising **Epistemic Actions** (thinking via doing) to bypass executive function deficits.

### 1.2 Epistemic Stance: "Utility Over Truth"

* **The Map is Not the Territory:** The system is a simplified model. When the map disagrees with reality, we update the map.
* **Utility over Completeness:** If a note does not help you *think* or *act*, it is noise. We prioritise "Good Enough" over "Perfect."

---

## 2. The Core Constraint: Zero-Maintenance Baseline

Standard systems fail ADHD users due to high "Operational Overhead." PRODOS is engineered for **< 10% Maintenance Load** (`Time Organizing / Time Executing`).

* **The Mandate:** Decouple maintenance from execution.
* **Low Power Mode:** The system relies on capture-first workflows that function during low executive function states. Neglect must not cause system failure.

---

## 3. The Architecture: Dual-Axis Engagement Model

PRODOS functions as a cognitive control room balancing two axes:

| Engineering Axis | Cognitive Counterpart | ADHD Deficit | PRODOS Solution |
|:--- |:--- |:--- |:--- |
| **Horizontal (Azimuth)** | **Temporal (Time)** | *Time Blindness* | **Calendar/Blocking:** Visible temporal landscape. |
| **Vertical (Elevation)** | **Attentional (Focus)** | *Distraction* | **Depth Control:** Managing "Rabbit Holes" vs. "Flow". |

---

## 4. The Data Schema: Thinking vs. Storage

The system maintains a strict separation of concerns utilizing a **Git Version Control** metaphor to prevent "Version Control Failure" (treating draft notes as truth).

| Feature | HEAD Notes (Working Tree) | SoT Notes (Master Branch) |
|:--- |:--- |:--- |
| **Role** | **The Workbench.** Volatile state. | **The Canon.** Stable knowledge. |
| **Trust** | **Zero Trust.** Chaotic stream. | **High Trust.** System of Record. |
| **Protocol** | **Continuous Commit.** Log real-time. | **Squash & Merge.** Synthesise & Delete HEAD. |

### 4.1 Workflow Protocols

1. **HEAD Notes:** Create via hotkey (`YYYY-MM-DD-HHmm-HEAD`). Never resume old notes; start fresh. Output to **Action** (Todoist), **Fact** (SoT), or **Pointer** (Future Task).
2. **SoT Notes:** Updated only through formal synthesis. Must be atomic and durable.

---

## 5. Trust & Verifiability: The Acceptance Criteria

**The Output First Metric:** If using the system feels like a chore, it is failing.

1. **The 60-Second Context Restoration Test:** Can you recall the *Minimum Viable Understanding (MVU)* and *Next Action* in < 60s?
2. **The Reuse Score:** Did the system avoid at least 30 minutes of new research for a project?

---

## 6. Functional Specification

The logic is implemented through five integrated modules:

1. **Ubiquitous Capture:** Zero-friction entry (Voice/Keys) into a single `00_Inbox`.
2. **Logic Processor:** Filters inputs into **Actionable** (Project/Task) or **Non-Actionable** (Reference/Trash). Enforces the **2-Minute Rule**.
3. **Visual Flow Engine:** Uses Kanban with **WIP Limits** to prevent cognitive overload.
4. **Review Orchestrator:** Weekly Review ritual to "Get Clear, Get Current, Get Creative."
5. **Cognitive Support:** "Now" toggle for distraction-free focus and gamified feedback loops.

---

## 7. Execution Protocols

### 7.1 The Reality Unit Test

Thinking is only complete when it generates a **Query for Reality**.

* **Input:** Hypothesis (HEAD Note).
* **Function:** The Next Test (Action).
* **Return Value:** Data/Outcome (Update SoT).

### 7.2 The Ignition Protocol

Used to convert "Work" into "Inquiry" when motivation is low:

* **Mystery Hack:** Refactor chore into a bet/hypothesis.
* **Time Trial:** Refactor infinite task into a binary sprint.
* **Spite Hack:** Refactor compliance into rebellion/argument.

---

## 8. Maintenance: The Hansei Loop

**Philosophy:** "No problem is a problem."
1. **Identify Friction:** Analyse failure without judgment.
2. **Adjust Process (Kaizen):** Apply the 1% rule.
3. **Verify Alignment (Ikigai):** Check against "Reason for Being."

### 8.1 Retrieval Strategy

Search tools must exclude `HEAD` folders by default. Searching a topic must yield **one result**: The SoT.

---

**Files to Delete:**
- `Old ProdOS Product Description` (Redundant)
