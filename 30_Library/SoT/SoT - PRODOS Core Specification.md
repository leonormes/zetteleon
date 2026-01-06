---
aliases: []
tags: []
title: PRODOS Core Specification (v2.0)
type: ""
status: ""
confidence: ""
epistemic: ""
purpose: ""
created: 2026-01-03T09:45:08+00:00
modified: 2026-01-05T19:50:17+00:00
last_reviewed: ""
review_interval: ""
see_also: []
source_of_truth: []
---

# PRODOS Core Specification (v2.0)

## 1. The Kernel

### 1.1 The Definition

PRODOS operates as a **Thinking Utility**, not a storage archive. Its sole purpose is to **reduce the friction of cognition**.

* **The Metric:** We do not measure "notes created." We measure **clarity achieved** and **actions taken**.

### 1.2 The Three Axioms

1. **Utility Over Truth:** The map is not the territory. If a note does not help you *think* or *act*, it is noise. We prioritize "Good Enough" over "Perfect."
2. **Throughput Over Storage:** The system is a runtime environment (Compute), not a database. Focus on the *flow* of information into action, not its static preservation.
3. **Low Maintenance:** The system must operate with **< 10% Maintenance Load**. Decouple maintenance from execution to survive low-energy states.

### 1.3 Data Schema (Thinking vs. Knowing)

* **HEAD Notes (The Workbench):** Volatile, chaotic, "Continuous Commit." Used for active thinking. `YYYY-MM-DD-HHmm-HEAD`.
* **SoT Notes (The Canon):** Stable, atomic, "Squash & Merge." The System of Record. Updated only via synthesis.

### 1.4 Problem Architecture

A problem exists **if and only if** there is a distinct gap between the **Current State** ($S_c$) and the **Desired State** ($S_d$), and the method to bridge that gap is **unknown**.

| Type | Definition | PRODOS Strategy |
|:--- |:--- |:--- |
| **Problem** | Gap + Unknown Path. | **HEAD Note**. Structure the gap, hypothesize the path. |
| **Task** | Gap + Known Path. | **Kinetic Action**. Execute immediately. |
| **Constraint** | Unchangeable Variable. | **Boundary Condition**. Optimize *around* it. |

---

## 2. The Core Loop (Workflow)

```d2
direction: down
classes: {
  process: {
    style: {
      fill: "#e1f5fe"
      stroke: "#01579b"
      stroke-width: 2
    }
  }
  decision: {
    shape: diamond
    style: {
      fill: "#fff9c4"
      stroke: "#fbc02d"
    }
  }
  storage: {
    shape: cylinder
    style: {
      fill: "#e0e0e0"
      stroke: "#616161"
    }
  }
  terminator: {
    shape: oval
    style: {
      fill: "#ffebee"
      stroke: "#c62828"
    }
  }
}

# --- NODES ---
INPUT: "Spark / Input" {class: process}
HEAD: "HEAD Note\n(Capture Context)" {class: storage}
GATE: "The Gate\n(Is it actionable?)" {class: decision}

# Outcomes
TRASH: "Garbage Collection\n(Delete)" {class: terminator}
ACTION: "Quick Action\n(< 2 mins)" {class: process}
SOT: "SoT / Fact\n(Reference)" {class: storage}

# Project Flow
HANGAR: "The Hangar\n(Charter Project)" {class: process}
COCKPIT: "The Cockpit\n(Execute)" {class: process}
UNIT_TEST: "Unit Test\n(Attempt -> Fail -> Learn)" {class: decision}
BRIDGE: "Bridge Note\n(Save State)" {class: storage}

# --- EDGES ---
INPUT -> HEAD: "Capture"
HEAD -> GATE: "Review"

# Gate Logic
GATE -> TRASH: "Delete"
GATE -> ACTION: "Do / Delegate"
GATE -> SOT: "Defer (Ref)"
GATE -> HANGAR: "Defer (Proj)"

# Execution Logic
HANGAR -> COCKPIT: "Initialize"
COCKPIT -> UNIT_TEST: "Attempt"
UNIT_TEST -> COCKPIT: "Fail (Fetch Info)"
UNIT_TEST -> BRIDGE: "Pass (Timebox End)"
BRIDGE -> COCKPIT: "Resume (Next Session)"

# Styling connections
ACTION -> TRASH: "Done"
```

### Phase Definitions

1. **Phase 1: Ingestion (The Stream):** Capture trigger in a **HEAD Note**. Do not process; capture context only.
2. **Phase 2: The Gate (4D Filter):**
    * **Do:** Actionable in < 2 mins? Execute immediately.
    * **Delegate:** Can someone else do it? Assign (`@Waiting`).
    * **Defer:** Needs time? Move to **Hangar** (Project) or **SoT** (Reference).
    * **Delete:** No value? Ruthlessly remove.
3. **Phase 3: The Hangar (Chartering):** Define the **Capstone** ("I will build X") and the **First Unit Test** ("I will make function Y work").
4. **Phase 4: The Cockpit (Execution Loop):** Load context, attempt Unit Test, fail, fetch info, fix, verify. **Rule:** No Input without Output.
5. **Phase 5: Cryosleep (State Preservation):** Write Bridge Note (Save State) and disengage.

---

## 3. Execution Rules (The Constraints)

### 3.1 The Minimal Viable Action (MVA)

To bypass initiation resistance, every task must be reduced to an MVA:

* **Micro-Temporal:** Takes < 120 seconds.
* **Kinetic:** Involves physical movement (e.g., "Open laptop," "Type command").
* **Binary:** Strictly True/False outcome.
* **Atomic Standard:** Indivisible, Physical & Visible, Unambiguous Definition of Done, Context-Specific.

### 3.2 The Golden Rule of Learning

**"We do not 'study' topics. We attack them."**
* **No Input without Output:** You cannot consume information without producing a corresponding artifact or test.
* **Boss Fight Protocol:** You cannot "finish" a book; you can only finish a project *using* the book.

### 3.3 Definition of Done

A task is done only when it passes its **Unit Test** (verifiable outcome) or when the **Unit of Work** (MVA) is completed and verified.

---

## 4. State Management (Cryosleep)

To minimize the cost of context switching, perform a **Save State Commit** at the end of every session.

### The Save State Syntax (`#SAVESTATE`)

* **Timestamp:** Log the stop time.
* **Current Context:** A summary of the "Working Tree" (what was just done/current variables).
* **Next Micro-Step (MVA):** Explicit, kinetic instruction for re-entry (e.g., "Open file X and run command Y").
* **Mood/Energy:** Log emotional state to help the Future Self empathize with the context.

---

## 5. Tooling (LLM Prompts)

### 5.1 The Architect (Phase 3: Chartering)

> "Act as an expert in [Topic]. Create a syllabus split into **Concepts** (Mental Models), **Facts** (Memorization), and **Procedures** (Skills). For each Concept, define a 'Unit Test' (small project) to prove understanding. Finally, define a 'Capstone Project' for the whole course."

### 5.2 The Hostile Compiler (Phase 4: Execution)

> "I am learning [Topic]. Here is my attempt at [Task]. Act as a strict code reviewer/critic. Find the logical flaws, edge cases, or misunderstandings in my work. Do not fix it for me; tell me *why* it fails."

### 5.3 The Bridge Builder (Phase 5: Cryosleep)

> "Summarize my current session into a 'Bridge Note'. Capture the current state, the exact next physical step, and a 'hook' to get me excited to return."

---

## Deprecated Files
