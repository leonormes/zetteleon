---
aliases: []
confidence: ""
created: 2026-01-03T09:45:08+00:00
epistemic: ""
last_reviewed: ""
modified: 2026-01-08T10:49:41+00:00
purpose: ""
review_interval: ""
see_also: []
source_of_truth: []
status: ""
tags: [prodos]
title: SoT - PRODOS Core Specification
type: ""
---

## PRODOS Core Specification (v2.0)

### 1. The Kernel

#### 1.1 The Definition

PRODOS operates as a **Thinking Utility**, not a storage archive. Its sole purpose is to **reduce the friction of cognition**.

- **The Metric:** We do not measure "notes created." We measure **clarity achieved** and **actions taken**.
- **The Threshold:** Distinguish **Motion** (planning, organizing, capturing) from **Action** (executing, building, changing reality). Motion is a prerequisite; Action is the objective.

#### 1.2 The Three Axioms

1. **Utility Over Truth:** The map is not the territory. If a note does not help you _think_ or _act_, it is noise. We prioritize "Good Enough" over "Perfect."
2. **Throughput Over Storage:** The system is a runtime environment (Compute), not a database. Focus on the _flow_ of information into action, not its static preservation.
3. **Low Maintenance:** The system must operate with **< 10% Maintenance Load**. Decouple maintenance from execution to survive low-energy states.

#### 1.3 Data Schema (Thinking vs. Knowing)

- **HEAD Notes (The Workbench / Exploratory):** Volatile, chaotic, "Continuous Commit." Mode: **Type B (Exploratory)**. Writing to _discover_ what you think. Messy, raw, non-linear. "Defrosting the windshield." `YYYY-MM-DD-HHmm-HEAD`.
- **SoT Notes (The Canon / Explanatory):** Stable, atomic, "Squash & Merge." Mode: **Type A (Explanatory)**. Writing to _transmit_ what you know (to others or future self). Structured, logical, and polished. The System of Record.

#### 1.4 Problem Architecture

A problem exists **if and only if** there is a distinct gap between the **Current State** ($S_c$) and the **Desired State** ($S_d$), and the method to bridge that gap is **unknown**.

| Type | Definition | PRODOS Strategy |
|:--- |:--- |:--- |
| **Problem** | Gap + Unknown Path. | **HEAD Note**. Structure the gap, hypothesize the path. |
| **Task** | Gap + Known Path. | **Kinetic Action**. Execute immediately. |
| **Constraint** | Unchangeable Variable. | **Boundary Condition**. Optimize _around_ it. |

#### 1.5 The Wetware Protocols (Neuro-Optimization)

- **Pragmatism Over Purity:** Rejection is often a defensive reflex (RSD); Engagement is a strategic control mechanism. Power is relational—influence requires connection.
- **Facilitation Over Authority:** Reject rigid hierarchy. Lead through "Shared Agency" and system design to bypass the RSD triggers of command-and-control.
- **Data Over Shame:** Procrastination is not a moral failing; it is **System Feedback** (Dopamine/Energy mismatch). Adjust the system; do not punish the operator.
- **Infrastructure Over Willpower:** Motivation is formless liquid (flood or trickle). The System is the **Pipe**. We do not rely on the liquid to steer itself; we build the pipe to channel the flow regardless of pressure.
- **Capacity Over Calendar:** Time is abundant; Energy is finite. Do not commit to tasks that exceed your current biological voltage.
- **Alignment Over Obligation:** The system rejects "Shoulds." Productivity is not moral penance; it is a mechanism for achieving genuine, interest-driven desires.
- **Identity as North Star:** Goals are temporary coordinates; Identity is the compass. Ask "What would the person I am becoming do?" to determine the trajectory of action.
- **Novelty as Architecture:** The system must evolve to survive. Rotate tools, gamify mechanics, and rewrite protocols when dopamine fades. Stagnation is system failure.
- **Identity Editing:** You cannot adopt a habit that conflicts with your self-image. To change behavior, you must first edit the source code of "Who I am." (e.g., delete "I am not a morning person"; commit "I am a person who values sunrise").
- **Effortless Engagement:** The friction of maintaining the system must be lower than the friction of doing the work. Radical simplicity and low activation energy are required to prevent system abandonment.

#### 1.6 The Kernel Metrics

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

#### Phase Definitions

1. **Phase 1: Ingestion (The Stream):** Capture trigger in a **HEAD Note**. Do not process; capture context only.
2. **Phase 2: The Gate (4D Filter):**
    - **Do:** Actionable in < 2 mins? Execute immediately.
    - **Delegate:** Can someone else do it? Assign (`@Waiting`).
    - **Defer:** Needs time? Move to **Hangar** (Project) or **SoT** (Reference).
    - **Delete:** No value? Ruthlessly remove.
3. **Phase 3: The Hangar (Chartering):** Define the **Capstone** ("I will build X") and the **First Unit Test** ("I will make function Y work").
4. **Phase 4: The Cockpit (Execution Loop):** Load context, attempt Unit Test, fail, fetch info, fix, verify. **Rule:** No Input without Output.
5. **Phase 5: Cryosleep (State Preservation):** Write Bridge Note (Save State) and disengage.

---

### 3. Execution Rules (The Constraints)

#### 3.1 The Minimal Viable Action (MVA)

To bypass initiation resistance, every task must be reduced to an MVA:

- **Micro-Temporal:** Takes < 120 seconds.
- **Kinetic:** Involves physical movement (e.g., "Open laptop," "Type command").
- **Binary:** Strictly True/False outcome.
- **Atomic Standard:** Indivisible, Physical & Visible, Unambiguous Definition of Done, Context-Specific.

#### 3.2 The Golden Rule of Learning

**"We do not 'study' topics. We attack them."**
- **No Input without Output:** You cannot consume information without producing a corresponding artifact or test.
- **Boss Fight Protocol:** You cannot "finish" a book; you can only finish a project _using_ the book.

#### 3.3 Definition of Done

A task is done only when it passes its **Unit Test** (verifiable outcome) or when the **Unit of Work** (MVA) is completed and verified.

#### 3.4 The Clarification Protocol (Transforming Stuff)

`clarify(stuff) → action`

1. **Clarify:** Define the **Nature** ("What is it?") and the **Outcome** ("What does 'Done' look like?").
2. **Classify:**
    - **> 1 Step?** It is a **Project**. Move to **Hangar**.
    - **1 Step?** It is a **Task**. Proceed.
3. **Atomize:** Define the **Next Physical Action**. It must adhere to **MVA** standards (Section 3.1).
4. **Momentum:** If execution resistance > 0, break the MVA into a `@starter_task` (e.g., "Write Report" -> "Open Document"). Continue until Activation Energy ≈ 0.

#### 3.5 The Motion Threshold

- **Motion:** Activities that _prepare_ for work (Capture, Clarify, Organize, Review).
- **Action:** Activities that _are_ work (Execution, "The Cockpit").
- **Rule:** If you are in Motion for > 20% of your session, you are likely procrastinating via "productive-feeling" preparation. Force a transition to Action via a `@starter_task`.

---

### 4. State Management (Cryosleep)

To minimize the cost of context switching, perform a **Save State Commit** at the end of every session.

#### The Save State Syntax (`#SAVESTATE`)

- **Timestamp:** Log the stop time.
- **Current Context:** A summary of the "Working Tree" (what was just done/current variables).
- **Next Micro-Step (MVA):** Explicit, kinetic instruction for re-entry (e.g., "Open file X and run command Y").
- **Mood/Energy:** Log emotional state to help the Future Self empathize with the context.

---

### 5. Tooling (LLM Prompts)

#### 5.1 The Architect (Phase 3: Chartering)

> "Act as an expert in [Topic]. Create a syllabus split into **Concepts** (Mental Models), **Facts** (Memorization), and **Procedures** (Skills). For each Concept, define a 'Unit Test' (small project) to prove understanding. Finally, define a 'Capstone Project' for the whole course."

#### 5.2 The Hostile Compiler (Phase 4: Execution)

> "I am learning [Topic]. Here is my attempt at [Task]. Act as a strict code reviewer/critic. Find the logical flaws, edge cases, or misunderstandings in my work. Do not fix it for me; tell me _why_ it fails."

#### 5.3 The Bridge Builder (Phase 5: Cryosleep)

> "Summarize my current session into a 'Bridge Note'. Capture the current state, the exact next physical step, and a 'hook' to get me excited to return."

---

### Deprecated Files
