---
aliases: ["PRODOS", "Productivity Operating System"]
confidence: "5/5"
created: 2026-01-03T09:45:08+00:00
epistemic: "Axiomatic"
last_reviewed: "2026-01-10"
modified: 2026-01-10T14:00:00+00:00
purpose: "The definitive specification for the PRODOS operating system, defining its kernel, protocols, and execution rules for both human and AI agents."
review_interval: "6 months"
see_also: []
source_of_truth: []
status: "stable"
tags: ["prodos", "system-architecture", "methodology"]
title: SoT - PRODOS Core Specification
type: "SoT"
---

# PRODOS Core Specification (v3.1 - Unified)

## 1. The Kernel

### 1.1 The Definition
PRODOS operates as a **Thinking Utility** for both Human and Artificial Intelligence. Its sole purpose is to **reduce the friction of cognition** and **maximize high-signal context**.

- **The Metric:** We do not measure "notes created." We measure **clarity achieved**, **decisions hardened**, and **actions taken**.
- **The Threshold:** Distinguish **Motion** (planning, organizing) from **Action** (executing). Motion is a prerequisite; Action is the objective.

### 1.2 The Four Axioms
1. **Utility Over Truth:** The map is not the territory. If a note does not help you _think_ or _act_, it is noise. Prioritize "Good Enough" over "Perfect."
2. **Throughput Over Storage:** The system is a runtime environment (Compute), not a database. Focus on the _flow_ of information into action.
3. **Low Maintenance:** The system must operate with **< 10% Maintenance Load**. Decouple maintenance from execution.
4. **Context is Scarcity:** For both Human (Attention) and Agent (Context Window), "More Information" = "Less Intelligence." We must aggressively **compact** and **scope** context.

### 1.3 Data Schema (The Git Flow)
- **HEAD Notes (The Feature Branch):** Long-lived "dev" branches.
    - **Purpose:** Active thinking and **Decision Tracing**.
    - **Content:** Assumption Audits, Raw Logic, `reason::` logs.
    - **Naming:** `YYYY-MM-DD-HHmm-HEAD [Topic]`.
- **SoT Notes (The Main Branch):** Production-ready code.
    - **Purpose:** Canonical Truth and **Topology Signatures**.
    - **Lifespan:** Permanent. Updated via **Compaction Rituals**.
    - **Rule:** **TRUSTED AUTHORITY.** High-signal, low-noise.
- **The Context Cache (`.ai/`):** Machine-readable memory.
    - **Purpose:** Structured context for Agents to prevent re-analysis.
    - **Structure:**
        - `persona/`: Role definitions.
        - `episodic/`: Compacted decision logs.
        - `entity/`: Specific project states.

### 1.4 Problem Architecture
A problem exists when there is a gap between Current State ($S_c$) and Desired State ($S_d$) with an unknown path.

| Type | Definition | PRODOS Strategy |
|:--- |:--- |:--- |
| **Problem** | Gap + Unknown Path. | **HEAD Note**. Trace the decision lineage (`reason::`). |
| **Task** | Gap + Known Path. | **Kinetic Action**. Execute immediately. |
| **Constraint** | Unchangeable Variable. | **Boundary Condition**. Optimize around it. |

---

## 2. Context Engineering (The Agent Protocol)

To prevent "Context Rot" (Agent Hallucination) and "Attention Fatigue" (Human Overwhelm), we apply strict engineering to our information flow.

### 2.1 Decision Lineage (The Trace)
We do not just record _what_ happened (State); we record _why_ (Trace).
- **Syntax:** `decision:: [Action Taken] reason:: [Context/Why] authorisation:: [Source]`.
- **Goal:** Enable emergent "Context Graphs" where an Agent can traverse the _history of reasoning_.

### 2.2 Context Hygiene (Rot Defense)
- **Ingestion:** Never paste raw HTML/PDFs. Use tools (e.g., `r.jina.ai`) to strip noise.
- **Tagging:** Strictly separate `#source/truth` (Canonical) from `#log/daily` (Transient).
- **Compaction:** Periodic "Garbage Collection" where Agents summarize weekly traces into SoT notes.

### 2.3 Entity Scoping (The Mount)
Agents are forbidden from "Global Scans." They must "Mount" a specific Entity before reasoning.
- **The Rule:** "Activating **Persona: [Role]**. Loading **Entity: [Project]**. Compare against **Reference: [Gold Master]**."

---

## 3. Human Protocols (The Operator)

### 3.1 Knowledge Synthesis (Writing is Thinking)
> [!definition] The Core Axiom
> **Writing IS Thinking.** Writing acts as a "mirror," forcing vague neural patterns into linear, testable syntax.

#### The 3-Stage Architecture
1. **Generation (The "Barf" Draft):** Quantity > Quality. No editing. (Input: `HEAD`)
2. **Refinement (The Logic Engine):** Clarity > Cleverness. Edit for Audience/Critics.
3. **Integration (The Wisdom Layer):** Wisdom > Knowledge. Does this change behavior? (Output: `SoT`)

#### Note Types (Cognitive Roles)
- **Model Note:** Framework for prediction ("Analogy", "Where it breaks").
- **Move Note:** Tactical pattern (Situation -> Move -> Outcome).
- **Delta Note:** Record of learning (Old Belief vs New Belief).

### 3.2 Learning Architecture (The Attack)
> [!definition] Core Philosophy
> **We do not "study" topics. We attack them.**
> - **Rule:** No Input without Output.
> - **Metric:** Unit Tests passed.

#### Phase I: The Hangar (Architecture)
- **Ingest:** Compress noise via AI.
- **Charter:** Define the "Capstone Project" (Boss Fight). You are not done until this exists.

#### Phase II: The Cockpit (Execution)
- **The Oakley Hard Start:** Attempt the hardest problem first (5m). Fail -> Load into Working Memory.
- **The Diffuse Retreat:** Switch to mechanical drills (20m) to let the subconscious process.
- **The Return:** Attack the hard problem with fresh context.

#### Phase III: Cryosleep (Consolidation)
- **The Hemingway Bridge:** Write the *next* action before stopping to lower re-entry friction.
- **The Merge:** Synthesize HEAD into SoT.

---

## 4. Execution Rules (The Constraints)

### 4.1 The Minimal Viable Action (MVA)
- **Micro-Temporal:** < 120 seconds.
- **Kinetic:** Physical movement.
- **Binary:** True/False outcome.

### 4.2 Definition of Done
Done = Passed **Unit Test** (verifiable outcome) or **MVA** completed.

### 4.3 The Clarification Protocol
`clarify(stuff) → action`
1. **Clarify:** Nature & Outcome.
2. **Classify:** Project (>1 step) or Task (1 step).
3. **Atomize:** Define Next Physical Action (MVA).
4. **Momentum:** Break down until Activation Energy ≈ 0.

### 4.4 The Assumption Protocol
1. **List "Facts":** What do I believe?
2. **Trace Source:** When did I decide this?
3. **Unit Test:** Is this a Physics Constraint or Stale Decision?

### 4.5 The Scribe Protocol (Zero-Friction Documentation)
**Do not write HEAD notes; Export them.**
1. **Prompt:** "Extract the 'Long-Lived HEAD' update (Conflict, Current State, Next Test)."
2. **Copy:** Paste the "Diff" into the local HEAD note.
3. **Commit:** Close the file.

---

## 5. State Management (Cryosleep)

Minimize context switching costs via **Scribe Commits**.

### The Save State Syntax (`#SAVESTATE`)
- **Timestamp:** `YYYY-MM-DD-HHmm`.
- **The Conflict:** What assumption did we challenge?
- **The Current State:** What is the new logic/hypothesis?
- **The Next Test:** The immediate next MVA/Unit Test.

---

## 6. Tooling (LLM Prompts)

### 6.1 The Architect (Phase 3: Chartering)
> "Act as an expert in [Topic]. Create a syllabus split into **Concepts**, **Facts**, and **Procedures**. Define a 'Unit Test' for each Concept and a 'Capstone Project'."

### 6.2 The Hostile Compiler (Phase 4: Execution)
> "I am learning [Topic]. Act as a strict code critic. Find logical flaws and edge cases. Do not fix; tell me _why_ it fails."

### 6.3 The Context Compressor (Weekly Review)
> "Read my Daily Notes from the last 7 days. Identify any architectural decisions regarding [System]. Summarise them into the 'Architecture SoT' note and verify if they contradict our 'Design Principles'. Discard the noise."

### 6.4 The Topology Mapper (Gold Master)
> "Analyze this architecture. Create a 'Logic Map' that explains the relationship between modules. Identify critical data flows and state dependencies. Save this as a structured Markdown file in `.ai/ctx_logic.md`."

### 6.5 The Scribe (Commit Protocol)
> "Stop processing. Review conversation. Extract the 'Long-Lived HEAD' update: 1. Conflict, 2. Current State, 3. Next Test. Format as raw Markdown diff."