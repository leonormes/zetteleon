---
aliases: [My Productivity System, ProdOS, The PRODOS Architecture]
confidence: 5/5
confidence-gaps: []
created: 2025-11-13T17:30:00Z
decay-signals: []
epistemic:
last-synthesis: 2025-12-20
last_reviewed: 2025-12-07
modified: 2025-12-20T20:28:08Z
purpose: The Master Index Note and System Specification for PRODOS, defining its architecture as an ADHD-centric cognitive augmentation system.
quality-markers: [Clarifies the Human-in-the-Loop LLM workflow., Defines the core cognitive loop., Establishes verifiable acceptance criteria., Integrates Hansei Reflection Loop.]
related-soTs: ["[[SoT - ADHD and Motivation]]", "[[SoT - ADHD Environmental Design]]", "[[SoT - Physical Health and Vitality]]", "[[SoT - PKM Confidence and Acceptance Criteria]]", "[[SoT - PRODOS - Action Management (GTD)]]", "[[SoT - PRODOS - Knowledge Synthesis (Thinking)]]", "[[SoT - PRODOS - Structure & Storage (PARA/PKM)]]"]
resonance-score: 10
review_interval: 3 months
see_also: []
source_of_truth: true
status: stable
supersedes: ["[[02 - GTD]]", "[[08 - Obsidian for PKM]]", "[[Complete Context ProdOS System]]", "[[Hansei]]", "[[Old ProdOS Product Description]]", "[[ProdOS System Overview and Development Progress]]", "[[The why of my zettelkasten]]"]
tags: ["adhd", "architecture", "hansei", "prodos", "system_design"]
title: SoT - PRODOS (System Architecture)
type: SoT
uid:
updated:
---

## 1. Definitive Statement

> [!definition] Definition
> PRODOS is a **cognitive augmentation system** designed to operate as an "extended mind" for a developer with ADHD. It offloads executive functions—such as context restoration, task initiation, and knowledge synthesis—to a structured, LLM-powered workflow.
>
> Fundamentally, it treats the system not as a **Database (Storage)** but as a **Runtime Environment (Compute)**. Its goal is not to preserve information (Retention) but to process context into reality (Throughput).

This approach is a direct solution to the problem of "Psychic RAM." The human mind is a processor, not a hard drive. When you store "open loops" (unresolved commitments) in your head, you consume cognitive resources. Your subconscious, lacking a sense of time, treats a trivial task like "buy milk" with the same urgency as a major deadline, leading to chronic stress. The goal of PRODOS is to achieve a state of **"Mind Like Water,"** where your response to any stimulus is exactly proportional to its importance, freeing up your attention for high-level thinking.

### 1.1 Epistemic Stance: The Map is Not the Territory

ProdOS is built on the principles of **General Semantics**, specifically Alfred Korzybski's insight that **"The Map is Not the Territory."**

- **The Reality:** Your life, your projects, and your thoughts are the "Territory"—complex, fluid, and infinite.
- **The System:** ProdOS is the "Map"—a simplified, abstract model designed to make that territory navigable.
- **The Rule:** We must never confuse the two. When the map disagrees with the territory (e.g., a plan fails), we update the map; we do not deny the reality. (See [[SoT - Reality, Models, and the Limits of Accuracy]]).

---

## 2. The Core Problem: Why PRODOS Exists

Conventional PKM and productivity systems fail because they are not designed for the ADHD brain. They often exacerbate challenges like **task initiation paralysis**, **executive dysfunction**, and **dopamine dysregulation**. PRODOS is built to directly solve these failures:

| Failure Mode                        | The Problem                                                                                                                                                                  | PRODOS Solution                                                                                                                                                           |
| :---------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **The Collector's Fallacy**         | The dopamine loop of collecting information creates "content sprawl" and overwhelm, mistaking acquisition for understanding.                                                 | **Action over Collection:** The system forces the conversion of knowledge into testable experiments and Minimum Viable Actions (MVAs).                               |
| **Context Loss**                    | The rich mental model of a project evaporates over time. Returning to flat notes requires high activation energy, leading to re-research or abandonment.                      | **The 60-Second Test:** The system is designed to allow a complete cognitive state restore (MVU + Next Action) in under a minute.                                     |
| **Procrastivity (System Perfectionism)** | Spending 40 hours building the "perfect" system in Notion or Obsidian instead of doing the work. The system becomes a dopamine-seeking playground, not a tool for execution. | **The Psychiatrist Protocol:** Strict separation of "Writing to Think" (Therapy) vs. "Organizing to Hide" (Addiction). The only valid output is a reality-testing action. |
| **The Weekly Review Breakdown**     | The Weekly Review is the master key to GTD, but it is executive-function heavy and offers no immediate dopamine hit, so it's the first component to be abandoned.           | **The Review Orchestrator:** A guided, ritualized, step-by-step program for system maintenance that removes decision fatigue.                                      |
| **The "Someday/Maybe" Abyss**       | For the "idea machine" ADHD brain, this list grows exponentially, becoming a "graveyard of guilt" that triggers overwhelm rather than inspiration.                           | **Incubation, not Deferral:** Items are not just "maybe" but are actively "incubating" with a defined (even if distant) review cycle.                            |
| **The "Now vs. Not Now" Conflict**  | The ADHD brain perceives time in two states: Now and Not Now. Once a task is "Not Now" (e.g., 'Waiting For'), it vanishes from consciousness until it becomes a crisis.    | **The "Now" Toggle & Visual Flow:** A distraction-free mode that shows only the next action, combined with visual Kanban boards that make "Not Now" work visible. |
| **Version Control Failure**         | Treating "Dev Branches" (HEAD notes) as "Master" (SoT). The system is flooded with broken, deprecated thoughts ("The Log"), making search unreliable.                        | **The Merge & Delete Ritual:** Strict separation of ephemeral "Work" vs. durable "Knowledge". You must "squash and merge" your thinking into the SoT.                |
| **Engine Stall**                    | Having Direction (Choice/Plan) but no Energy (Dopamine). "Turning the wheel but the car won't move." (See [[Breaking the Creation Cycle]])                                      | **The Ignition Protocol:** Use the HEAD note to refactor "Boring Tasks" into "Interesting Hypotheses" (Mystery, Spite, Urgency) to manufacture dopamine.              |

### Comparative Analysis: Storage (Museum) vs. Compute (Factory)

The fundamental shift in ProdOS is moving from a "Librarian" mindset to an "Operator" mindset.

| Feature | Wiki / Archive (The Museum) | ProdOS (The Factory) |
| :--- | :--- | :--- |
| **Primary Goal** | Storage & Retrieval (Retention) | **Context Restoration & Action (Throughput)** |
| **Input Model** | Categorisation (Filing) | **Frictionless Capture (Stream)** |
| **Output Model** | Encyclopedia Entry | **Unit Test (Verifiable Action)** |
| **Maintenance** | Gardening (High Friction) | **Synthesis (Zero-Toil via LLM)** |
| **Metric** | "Did I save it?" | **"Did I change reality?"** |
| **ADHD Risk** | "Where did I put that?" | **N/A (Focus is on "Next Action")** |

---

## 3. The Architecture: Dual-Axis Engagement

PRODOS functions as a control room balancing two axes:

- **Horizontal Control (The Runway):** A system to capture, clarify, and execute daily actions.
- **Vertical Perspective (The Horizons):** A hierarchical map from **50,000 feet** (Purpose/Principles) down to **10,000 feet** (Projects).

This is implemented via an action-oriented cognitive loop: **Capture -> Refine -> Synthesize -> Act -> Reflect (Hansei) -> Repeat**

1. **Capture (Human):** Raw, messy, unstructured thoughts are captured into a frictionless entry point.
2. **Refine (LLM) - "The Psychiatrist Workflow":** The LLM acts as a **Convergent Tool**.
    - **Vomit Chaos:** The user dumps raw, unstructured thought into a `HEAD` note.
    - **Logic Linter:** The LLM debugs the thought, stripping emotion to find the signal.
    - **Extract Action:** The sole purpose is to compile the thought into a **Verifiable Next Action**.
    - **Nuke the Rest:** Once the lesson is extracted to an SoT and the action to Todoist, the HEAD note is archived/ignored.
3. **Synthesize (LLM & Human):** The LLM automates the "Chronos Synthesis" ritual, updating the canonical `SoT` note.
4. **Act (Human):** The output of thinking is not another note, but a **verifiable `Next Action`**.
5. **Reflect (Hansei):** A structured feedback loop to transform behavior into learning (See Section 10).

---

## 4. The Note Schema: Capturing Thought vs. Storing Fact

The system maintains a strict separation of concerns between thinking and knowing.

### The Architectural Rule: "Master" vs. "Dev" (Version Control)

| Feature | HEAD Notes (The Workbench) | SoT Notes (The Canon) |
| :--- | :--- | :--- |
| **Software Equivalent** | `feature/fix-bug-123` (Dev Branch) | `main` / `master` (Production) |
| **Trust Level** | **Zero Trust.** Contains errors, dead ends, and drafts. | **High Trust.** The "Single Source of Truth." |
| **Lifespan** | **Ephemeral.** Created to solve *one* problem, then archived. | **Permanent.** Durable, living documentation. |
| **Searchability** | **Hidden.** Should NOT appear in standard lookups. | **Primary.** The *only* place you look for answers. |

### A. HEAD Notes (The Workbench)

- **Purpose:** The **universal container for active thinking**. It captures the *process* of cognition.
- **The Protocol (Always New, Never Resume):**
  - **Zero-Decision Entry:** Use a single hotkey to create a timestamped note (`YYYY-MM-DD-HHmm-HEAD`).
  - **Session State:** Your brain is the session state. Never resume an old note. Start fresh.
  - **The Tri-State Output Router:** At the end of the session, select one of three exit paths:
    - **Path A: Kinetic (Action):** "I figured it out." -> Extract Task to Todoist -> Archive Note.
    - **Path B: Static (Storage):** "I learned a fact." -> Merge Insight to SoT -> Archive Note.
    - **Path C: Dynamic (Thinking):** "I am paused." -> **Serialize State** -> Create **Pointer Task** in Todoist -> Keep Note Active.
- **Voice:** First-person, raw, and unpolished.

### B. LIB/SoT Notes (The Canon)

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

[[Logic Does Not Produce Dopamine|Logic does not produce dopamine]]. To generate the energy for execution, you must convert "Work" into "Inquiry."

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
| :--- | :--- | :--- |
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
- [[SoT - PRODOS - NotebookLM Integration]]
- [[SoT - Accelerated Learning (3C Protocol)]]
- [[SoT - PRODOS - Knowledge Synthesis (Thinking)]]
- [[SoT - Dopamine Menu]]
- [[SoT - PRODOS - Action Management (GTD)]]
- [[SoT - Temporal Management (Blocking and Boxing)]]
- [[SoT - The Cognitive Physiology of Task Execution]]
- [[SoT - Six Levels of Thinking]]
- [[SoT - The Honeyman Method (Adaptive Routines)]]
- [[SoT - Identity-Based Habit Formation]]
- [[SoT - PRODOS - System Failure Modes]]
- **Case Study:** [[Breaking the Creation Cycle]]
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
