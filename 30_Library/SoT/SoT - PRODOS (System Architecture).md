---
aliases: ["My Productivity System", "ProdOS", "The PRODOS Architecture"]
confidence: "5/5"
created: 2025-11-13T00:00:00Z
epistemic: ""
last_reviewed: "2025-12-07"
modified: 2025-12-30T14:11:34+00:00
purpose: "The Master Index Note and System Specification for PRODOS, defining its architecture as an ADHD-centric cognitive augmentation system."
review_interval: "3 months"
see_also: ["[[02 - GTD]]", "[[08 - Obsidian for PKM]]", "[[Complete Context ProdOS System]]", "[[Hansei]]", "[[Old ProdOS Product Description]]", "[[ProdOS System Overview and Development Progress]]", "[[SoT - ADHD and Motivation]]", "[[SoT - ADHD Environmental Design]]", "[[SoT - AI-Resilient Task Taxonomy (Human 3.0)]]", "[[SoT - Indistractable Model (Focus Management)]]", "[[SoT - Intentional Living (Habit Mastery)]]", "[[SoT - Physical Health and Vitality]]", "[[SoT - PKM Confidence and Acceptance Criteria]]", "[[SoT - PRODOS - Action Management (GTD)]]", "[[SoT - PRODOS - Knowledge Synthesis (Thinking)]]", "[[SoT - PRODOS - Structure & Storage (PARA/PKM)]]", "[[SoT - The Discipline of Perception (Mindset)]]", "[[SoT - The Inspiration Economy (Agentic Frameworks)]]", "[[SoT - The Telos Method]]", "[[The why of my zettelkasten]]"]
source_of_truth: []
status: "stable"
tags: ["architecture", "hansei", "prodos", "system_design", "topic/health/adhd"]
title: SoT - PRODOS (System Architecture)
type: "SoT"
uid: 
updated: 
---

## 1. Definitive Statement

> [!definition] Definition
> It operates as a **Thinking Utility**, not a storage archive. Its sole purpose is to: ""
> **The Metric: "** We do not measure "notes created." We measure "clarity achieved" and "actions taken.""

### 1.1 Theoretical Foundation: The Extended Mind

ProdOS is an operational implementation of the **[[SoT - The Extended Mind Thesis|Extended Mind Thesis]]**. It treats this Obsidian vault as a constitutive part of the user's cognitive machinery, utilizing **[[Epistemic Actions - Thinking via Doing|Epistemic Actions]]** to bypass internal executive function deficits.

## 1.2 Epistemic Stance: "Utility Over Truth"

- **The Map is Not the Territory: "** The system is a simplified model, not reality itself."
- **Utility over Completeness: "** We do not aim to catalogue the world. If a note does not help you *think* or *act*, it is noise. We prioritize "Good Enough" over "Perfect.""
- **The Rule: "** When the map disagrees with the territory (e.g., a plan fails), we update the map; we do not deny the reality."

### 1.2 The Zero-Maintenance Baseline

PRODOS is engineered for **Zero Maintenance Baseline**. Standard systems fail ADHD users because they demand high "Operational Overhead" (decision fatigue, grooming).

- **Maintenance Load:** Quantified as `Time Organizing / Time Executing`. Target: **< 10%**.
- **The Mandate:** Decouple maintenance from execution. If a system requires manual "gardening" before work can begin, it is broken.
- **Effortless Engagement:** The system must function on "Low Power Mode." It should rely on capture-first workflows and intuitive tools that work even during periods of low executive function. Neglect should not cause system failure.

## 2. The Core Problem: Why PRODOS Exists

| **Version Control Failure** | Treating "Dev Branches" (HEAD notes) as "Master" (SoT). The system is flooded with broken, deprecated thoughts. | **The Merge & Delete Ritual:** Strict separation of ephemeral "Work" vs. durable "Knowledge". You must "squash and merge" thinking into the SoT. |

### Comparative Analysis: Storage (Museum) vs. Compute (Factory)

## 3. The Architecture: Dual-Axis Engagement Model

PRODOS functions as a control room balancing two axes, derived from the principles of high-efficiency solar tracking:

| Engineering Axis | Cognitive Counterpart | ADHD Function | PRODOS Component |
|:--- |:--- |:--- |:--- |
| **Horizontal (Azimuth)** | **Temporal Axis (Time)** | *Time Blindness* | Calendar, Deadlines, Linear Progression. |
| **Vertical (Elevation)** | **Attentional Axis (Focus)** | *Hyperfocus / Distraction* | Project Depth, "Rabbit Holes", Flow State. |

1. **Horizontal Control:** Manages the linear progression of the day. Uses **Time Blocking** and **Interstitial Journaling** to create a visible temporal landscape, compensating for Time Blindness.
2. **Vertical Perspective:** Manages the depth of engagement. When in **Hyperfocus (High Elevation)**, the system supports depth without allowing the user to drift off-course. When dopamine is low (**Low Elevation**), the system lowers the "Bar of Entry" to maintain momentum.

## 4. The Note Schema: Thinking Space vs. Answer Space

The system maintains a strict separation of concerns utilizing a **Git Version Control** metaphor:

### The Architectural Rule: "Master" vs. "Dev" (Version Control)

| Feature | HEAD Notes (Working Tree) | SoT Notes (Master Branch) |
|:--- |:--- |:--- |
| **Role** | **The Workbench.** Volatile state where changes happen. | **The Canon.** Stable, production-ready knowledge. |
| **Trust Level** | **Zero Trust.** Chaotic stream of consciousness. | **High Trust.** The verified "System of Record." |
| **Lifecycle** | **Ephemeral.** Dump data without regard for taxonomy. | **Permanent.** Atomic, clean, and interconnected. |
| **The Protocol** | **Continuous Commit.** Log everything in real-time. | **Squash and Merge.** Synthesize and then delete HEAD. |

### A. HEAD Notes (The Working Tree)

- **Purpose:** The **universal container for active thinking**. It captures the *process* of cognition.
- **The Protocol (Always New, Never Resume):**
  - **Zero-Decision Entry:** Use a single hotkey to create a timestamped note (`YYYY-MM-DD-HHmm-HEAD`).
  - **Session State:** Your brain is the session state. Never resume an old note. Start fresh.
  - **The Tri-State Output Router:** At the end of the session, select one of three exit paths:
    - **Path A: Kinetic (Action):** "I figured it out." -> Extract Task to Todoist -> Archive Note.
    - **Path B: Static (Storage):** "I learned a fact." -> Merge Insight to SoT -> Archive Note.
    - **Path C: Dynamic (Thinking):** "I am paused." -> **Serialize State** -> Create **Pointer Task** in Todoist -> Keep Note Active.
- **Voice:** First-person, raw, and unpolished.

### B. SoT Notes (The Canon)

- **Purpose:** To be the trusted **System of Record** for stable, verified knowledge.
- **Voice:** Third-person, objective.
- **Key Constraint:** Must be durable and updated only through a formal synthesis process.

---

## 5. Trust & Verifiability: The Acceptance Criteria

1. **The 60-Second Context Restoration Test (Save State):** Can I open the relevant Project/SoT note and recall the **Minimum Viable Understanding (MVU)** and the very **Next Action** in under 60 seconds?
2. **The Reuse Score:** For any new project, was the system successfully leveraged to find and reuse existing knowledge, avoiding at least 30 minutes of new research?

### 5.1 Measurable Outcomes: The "Output First" Metric

> **The Rule:** If using the system feels like a chore, it is failing.

**Key Performance Indicators (KPIs):**
- **Output Volume:** Did the system directly contribute to finishing a project or task this week?
- **Retrieval Speed:** Can you find the exact information you need in < 30 seconds?
- **Mental Silence:** Does the "Brain Dump" actually clear the noise?
- **Simplicity:** Is the barrier to entry low enough that you capture ideas even when tired?

---

## 6. Functional Specification & Integrations

The system's logic is implemented through a series of integrated modules designed to handle the cognitive loop and support neurodivergent workflows.

### Module 1: The Ubiquitous Capture Hub

To ensure trust, the app must eliminate "holes in the bucket."

- **Zero-Friction Entry:** Multi-modal capture (voice-to-text, email forwarding, global hotkeys) that funnels all raw "stuff" into a single, unprocessed **In-box**.
- **External Brain Sync:** Real-time synchronization across all devices.

### Module 2: The Logic Processor (Clarify & Organise)

This module automates the thinking process required to define work before doing it.

- **The Actionability Filter:** A guided workflow for every In-box item:
	- **Is it actionable?** If NO: Auto-sort to **Trash**, **Reference**, or **Someday/Maybe** (Incubation).
	- **If YES:** Force-definition of the **Next Action** and the **Desired Outcome** (Project).
- **The 2-Minute Rule Engine:** If an action is tagged <2 minutes, the app triggers an immediate "Do It" prompt.

### Module 3: The Visual Flow Engine (Kanban)

Drawing from *Making Work Visible*, the app replaces static lists with dynamic visual boards.

- **WIP (Work-In-Progress) Limits:** A hard constraint (e.g., 3 items) on the "Doing" column to prevent cognitive overload from context switching.
- **Flow Metrics:** Real-time dashboards for **Cycle Time** (how long it takes to finish a task) and **Aging Reports** (flagging neglected work).

### Module 4: The Review Orchestrator

This is the master key to maintaining system integrity.

- **The Guided Weekly Review:** A ritualized, step-by-step program:
	1. **Get Clear:** Emptying physical and digital in-boxes.
	2. **Get Current:** Updating Projects and Waiting-For lists.
	3. **Get Creative:** Using trigger lists to "Mind Sweep" new ideas.
- **Horizon Alignment Check:** A quarterly prompt to verify if **Projects** (10k feet) support **Goals** (30k feet) and **Vision** (40k feet).

### Module 5: ADHD & Cognitive Support

This layer supports "Now" vs. "Not Now" time-blindness.

- **The "Now" Toggle:** A distraction-free mode that hides everything except the single next action for the current context.
- **Visual Feedback Loops:** Gamified indicators of progress to provide immediate "natural rewards."
- **Interruption Capture:** A "Flash Capture" or "Pink Dot" button for unplanned work, allowing the user to record the interruption and return to flow state immediately.

### Core Integrations

- **`00_Inbox` / Daily Note:** Frictionless capture.
- **`20_Thinking/21_Workbench`:** Home for active `HEAD` notes.
- **`30_Library/31_Resources`:** Home for canonical `SoT` notes.
- **`10_Actions/11_Projects`:** Project Dashboards linking to `HEAD` and `SoT` notes.
- **Todoist (The Runtime):** Contains only executable tasks.
- **LLM (The Zero-Toil Engine):** Background service for refinement and synthesis.

---

## 7. Tactical Protocols: The Command Centre (Manual Execution)

*Source: [YouTube Video: The Command Centre (Manual Execution)](https://youtu.be/qP6e8kcurgQ)*

The Command Centre is a structural solution to planning inconsistency, reframing it not as a failure of willpower but as a failure of **system design**. It externalizes hard-coded algorithms for operational routines (daily, weekly, monthly planning) that execute on "autopilot."

**Objective:** Eliminate decision fatigue and reduce the cognitive load required to *initiate* and *execute* maintenance routines.

---

## 8. Reality as a Unit Test (The Execution & Ignition Protocol)

The "Next Test" is not just a task; it is a **verifiable interface** between the internal mental model (Thinking) and external reality (Doing).

### The Compilation Target

You do not finish thinking when you have an answer; you finish when you have a **query for reality**.

- **Input:** Tension/Hypothesis (HEAD Note).
- **Function:** The Next Test (Action).
- **Return Value:** Data/Outcome (Update SoT).

### The Specification (Acceptance Criteria)

1. **Atomic Scope:** The smallest possible unit of work (<15 mins).
2. **Binary Outcome:** It must Pass or Fail.
3. **Learning Objective:** Focus on *information gain*, not just output.

### The Ignition Protocol (Stimulus Injection)

 To generate the energy for execution, you must convert "Work" into "Inquiry." If paralyzed by emotion, first execute the **[[SoT - The 3-Switch Protocol (Emotional Reset)]]** to restore control.

1. **The "Mystery" Hack (Hypothesis):** Refactor a chore into a bet.
    - *Boring:* "Update CSS." -> *Ignition:* "Hypothesis: I can break the layout if I change padding to 50px."
2. **The "Time Trial" Hack (Urgency):** Refactor an infinite task into a binary sprint.
    - *Boring:* "Clear inbox." -> *Ignition:* "Can I process 10 items in 3 minutes? Yes/No."
3. **The "Spite" Hack (Logic Linter):** Refactor compliance into rebellion.
    - *Boring:* "Write scope." -> *Ignition:* "Open a HEAD note and argue why this project is stupid."

---

## 9. Information Architecture & Retrieval Strategy

The core challenge is retrieving the right thought at the right time.

### The Unified Hierarchy

| File Type | Role | The Question It Answers |
|:--- |:--- |:--- |
| **SoT Notes** | **The Canon (Authority)** | "What is the trusted, current state of the system?" |
| **MOCs** | **The Map (Entrypoint)** | "Where do I start? Show me the landscape." |
| **HEAD Notes** | **The Workbench (Active)** | "What am I figuring out right now?" |
| **Base Files** | **The Dashboard (Dynamic)** | "Show me a live list of all X." |

### The "Safe Search" Guarantee

To fix "Version Control Failure," the retrieval system must enforce the "Master Branch" view.

- **Configuration:** Search tools must exclude `HEAD` / `Thinking` folders by default.
- **The Promise:** When you search for a topic, you should see **one result**: The SoT.

---

## 10. Maintenance Rituals: The Hansei Feedback Loop

The system is not static; it requires active maintenance to prevent "Trust Decay."

> **Philosophy:** "No problem is a problem." If you don't find friction, you are blind to it.

### The Weekly Hansei Protocol (Kaizen & Ikigai)

1. **Identify Friction (Deconstruct):** Analyze where the system failed without judgment.
2. **Adjust Process (Kaizen):** Do not blame willpower. Apply the **1% Rule**.
3. **Verify Alignment (Ikigai):** Check if actions align with your *Reason for Being*.

---

## 11. The Three-Layer Architecture (Capacity & Maintenance)

*Source: [The Missing Middle: Why Goals Fail](http://www.youtube.com/watch?v=sztRU38bE_Q)*

Most planning systems fail because they oscillate between **Strategic Goals** (Top) and **Execution Tasks** (Bottom), ignoring the **Maintenance Layer** that sustains life.

### The Architecture

1. **Strategic Layer (Top-Down):** Goals, Vision. Provides *direction*.
2. **Maintenance Layer (The Missing Link):** Recurring operations. Provides *stability*.
    - **Rule:** **Capacity Regulation.** `Capacity = Total Time - Maintenance`.
3. **Execution Layer (Bottom-Up):** Ad-hoc tasks. Provides *responsiveness*.

---

## 12. Open Questions & Tensions

- **Tension:** The core struggle remains balancing **Action (Kinetic)** vs. **Thinking (Dynamic)**. The system mitigates this by demanding that all "Thinking" cycles must terminate in an "Action" (The Next Test).
- **Confidence Gap:** The system's trustworthiness depends entirely on the discipline of adhering to the synthesis loop.

## 13. Related Components

- [[SoT - PRODOS - The Cognitive Loop (A-C-T Framework)]]
- [[SoT - Accelerated Learning (3C Protocol)]]
- [[SoT - PRODOS - Knowledge Synthesis (Thinking)]]
- [[SoT - AI-Resilient Task Taxonomy (Human 3.0)]]
- [[SoT - Dopamine Menu]]
- [[SoT - Indistractable Model (Focus Management)]]
- [[SoT - Intentional Living (Habit Mastery)]]
- [[SoT - PRODOS - Action Management (GTD)]]
- [[SoT - Temporal Management (Blocking and Boxing)]]
- [[SoT - The Discipline of Perception (Mindset)]]
- [[SoT - The Inspiration Economy (Agentic Frameworks)]]
- [[SoT - The Telos Method]]
- [[SoT - The Cognitive Physiology of Task Execution]]
- [[SoT - Six Levels of Thinking]]
- [[SoT - The Honeyman Method (Adaptive Routines)]]
- [[SoT - Identity-Based Habit Formation]]
- [[SoT - PRODOS - System Failure Modes]]
- **Example Implementation:** [[Detailed Example From Spark to Synthesis]]

## 14. Status & Roadmap

**Current Status:** ProdOS v5.0 is considered **production-ready**.

- **Core:** Architecture consolidated and operational.
- **Integrations:** Obsidian-Todoist bidirectional sync is robust. Jira data ingestion is functional (pending auth fix).
- **Operations:** Phase 1 commands (`/daily-plan`, `/engage-action`) are live.

**Roadmap:**

- **Phase 2:** Automated background sync and system synchronization.
- **Phase 3:** Advanced AI decision support (energy-aware task selection).
- **Phase 4:** Smart capture processing and proactive notifications.
- **Phase 5:** Mobile accessibility and team coordination.
