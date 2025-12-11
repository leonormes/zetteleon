---
aliases: [My Productivity System, ProdOS, The PRODOS Architecture]
confidence: 5/5
confidence-gaps: []
created: 2025-11-13T17:30:00Z
decay-signals: []
epistemic:
last-synthesis: 2025-12-07
last_reviewed: 2025-12-07
modified: 2025-12-10T19:59:40Z
purpose: The Master Index Note and System Specification for PRODOS, defining its architecture as an ADHD-centric cognitive augmentation system.
quality-markers: [Clarifies the Human-in-the-Loop LLM workflow., Defines the core cognitive loop., Establishes verifiable acceptance criteria., Integrates Hansei Reflection Loop.]
related-soTs: ["[[SoT - PKM Confidence and Acceptance Criteria]]", "[[SoT - PRODOS - Action Management (GTD)]]", "[[SoT - PRODOS - Knowledge Synthesis (Thinking)]]", "[[SoT - PRODOS - Structure & Storage (PARA/PKM)]]"]
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

---

## 2. The Core Problem: Why PRODOS Exists

Conventional PKM and productivity systems fail because they are not designed for the ADHD brain. They often exacerbate challenges like **task initiation paralysis**, **executive dysfunction**, and **dopamine dysregulation**. PRODOS is built to directly solve these failures:

| Failure Mode                | The Problem                                                                                                                                              | PRODOS Solution                                                                                                                                                  |
| :-------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **The Collector's Fallacy** | The dopamine loop of collecting information creates "content sprawl" and overwhelm, mistaking acquisition for understanding.                             | **Action over Collection:** The system forces the conversion of knowledge into testable experiments and Minimum Viable Actions (MVAs).                           |
| **Context Loss**            | The rich mental model of a project evaporates over time. Returning to flat notes requires high activation energy, leading to re-research or abandonment. | **The 60-Second Test:** The system is designed to allow a complete cognitive state restore (MVU + Next Action) in under a minute.                                |
| **Administrative Friction** | The "toil" of organizing, tagging, and processing notes drains executive function, causing the system to be abandoned.                                   | **Zero-Toil Automation:** The user's role is frictionless capture. A "Chief of Staff" LLM handles all synthesis, structuring, and metadata.                      |
| **Displacement Activity**   | "Organizing" (folders, tags) serves as a dopamine-rich distraction to avoid the pain of actual work ("The Alcohol").                                     | **The Psychiatrist Protocol:** Strict separation of "Writing to Think" (Therapy) vs. "Organizing to Hide" (Addiction). The only valid output is a reality-testing action.|
| **Version Control Failure** | Treating "Dev Branches" (HEAD notes) as "Master" (SoT). The system is flooded with broken, deprecated thoughts ("The Log"), making search unreliable.    | **The Merge & Delete Ritual:** Strict separation of ephemeral "Work" vs. durable "Knowledge". You must "squash and merge" your thinking into the SoT, then delete the branch. |
| **Engine Stall**            | Having Direction (Choice/Plan) but no Energy (Dopamine). "Turning the wheel but the car won't move." This is **[[The War of Art - Resistance and Turning Pro|Resistance]]**.                                                     | **The Ignition Protocol:** Use the HEAD note to refactor "Boring Tasks" into "Interesting Hypotheses" (Mystery, Spite, Urgency) to manufacture dopamine.                      |

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

## 3. The Architecture: An Action-Oriented Cognitive Loop

PRODOS functions as a continuous loop that processes thought, generates action, and synthesizes results. It operates on the **Compass-over-Clock** paradigm, prioritizing values and purpose over urgency.

**Capture -> Refine -> Synthesize -> Act -> Reflect (Hansei) -> Repeat**

1.  **Capture (Human):** Raw, messy, unstructured thoughts are captured into a frictionless entry point (Daily Note). "Capture Now, Structure Later."
2.  **Refine (LLM) - "The Psychiatrist Workflow":** The LLM acts as a **Convergent Tool**, preventing the "Alcohol" of over-organization.
    -   **Vomit Chaos:** The user dumps raw, unstructured thought into a `HEAD` note (The Therapy).
    -   **Logic Linter:** The LLM debugs the thought, stripping emotion ("I hate this") to find the signal.
    -   **Extract Action:** The sole purpose is to compile the thought into a **Verifiable Next Action**.
    -   **Nuke the Rest:** Once the lesson is extracted to an SoT and the action to Todoist, the HEAD note is archived/ignored. No filing, no tagging.
    -   **The Architectural Rule:** "Human Write, Machine Read." The HEAD note is the "Kernel" (Source Code) for your eyes only. The SoT is the "Binary" (Compiled Output) managed by the LLM.
3.  **Synthesize (LLM & Human):** The LLM automates the "Chronos Synthesis" ritual, updating the canonical `SoT` note with new insights from `HEAD` notes. The user performs the final validation.
4.  **Act (Human):** The output of thinking is not another note, but a **verifiable `Next Action`**—a test, an experiment, or a command—to be executed in the real world.
5.  **Reflect (Hansei):** A structured feedback loop to transform behavior into learning (See Section 9).

---

## 4. The Note Schema: Capturing Thought vs. Storing Fact

The system maintains a strict separation of concerns between thinking and knowing.

### The Architectural Rule: "Master" vs. "Dev" (Version Control)

You must treat your notes exactly like a software repository to prevent "Version Control Failure":

| Feature | HEAD Notes (The Workbench) | SoT Notes (The Canon) |
| :--- | :--- | :--- |
| **Software Equivalent** | `feature/fix-bug-123` (Dev Branch) | `main` / `master` (Production) |
| **Trust Level** | **Zero Trust.** Contains errors, dead ends, and drafts. | **High Trust.** The "Single Source of Truth." |
| **Lifespan** | **Ephemeral.** Created to solve *one* problem, then archived. | **Permanent.** Durable, living documentation. |
| **Searchability** | **Hidden.** Should NOT appear in standard lookups. | **Primary.** The *only* place you look for answers. |

### A. HEAD Notes (The Workbench)
- **Purpose:** The **universal container for active thinking**. It is not a rigid form but a flexible space for journaling, questioning, learning, hypothesizing, or arguing with oneself. It captures the *process* of cognition, however messy.
- **The Protocol (Always New, Never Resume):**
    -   **Zero-Decision Entry:** Use a single hotkey to create a timestamped note (`YYYY-MM-DD-HHmm-HEAD`). **No titles, no folders, no prompts.** The cursor lands in free space.
    -   **Session State:** Your brain is the session state. Never resume an old note. Start fresh, check the SoT for context, and write.
    -   **The Tri-State Output Router:** At the end of the session, the user must select one of three exit paths:
        -   **Path A: Kinetic (Action):** "I figured it out." -> Extract Task to Todoist -> Archive Note.
        -   **Path B: Static (Storage):** "I learned a fact." -> Merge Insight to SoT -> Archive Note.
        -   **Path C: Dynamic (Thinking):** "I am paused." -> **Serialize State** (Write "I stopped at X, next step is Y") -> Create **Pointer Task** in Todoist ("Thinking: Resume [Link]") -> Keep Note Active.
- **Voice:** First-person, raw, and unpolished.

### B. LIB/SoT Notes (The Canon)
- **Purpose:** To be the trusted **System of Record** for stable, verified knowledge and the `Current Understanding` of a topic.
- **Voice:** Third-person, objective.
- **Key Constraint:** Must be durable and updated only through a formal synthesis process. It is the single source of truth that you can trust when returning to a topic.

---

## 5. Trust & Verifiability: The Acceptance Criteria

PRODOS is considered "working" only when it consistently passes these two acceptance tests:

1.  **The 60-Second Context Restoration Test (Save State):** The system is not an archive; it is a save state. Can I open the relevant Project/SoT note and recall the **Minimum Viable Understanding (MVU)** and the very **Next Action** in under 60 seconds? Everything "below the fold" is irrelevant history.
2.  **The Reuse Score:** For any new project, was the system successfully leveraged to find and reuse existing knowledge, avoiding at least 30 minutes of new research?

### 5.1 Measurable Outcomes: The "Output First" Metric

Moving beyond the "buzz" of potential, we assess success through concrete, real-world utility. **The system exists to serve you, not for you to serve it.**

> **The Rule:** If using the system feels like a chore, it is failing.

**Key Performance Indicators (KPIs):**
-   **Output Volume:** Did the system directly contribute to finishing a project or task this week? (Transformation > Accumulation).
-   **Retrieval Speed:** Can you find the exact information you need in < 30 seconds?
-   **Mental Silence:** Does the "Brain Dump" actually clear the noise? (Reduction in "stuff I need to remember").
-   **Simplicity:** Is the barrier to entry low enough that you capture ideas even when tired?

---
## 6. Structural Implementation & Integrations

The folder structure and tool integration reflect the cognitive loop. PRODOS v5.0 represents the "ultimate maturation" of the system, consolidated into a highly optimized **4-file system** (down from 72) to maximize LLM efficiency (75-90% faster loading).

- **`00_Inbox` / Daily Note:** Frictionless capture.
- **`20_Thinking/21_Workbench`:** The home for active `HEAD` notes where cognitive work happens.
    -   **Flash Thinking Setup:** Configure a global hotkey to create a new file here with `YYYY-MM-DD-HHmm-HEAD` naming to bypass the "Naming Friction".
- **`30_Library/31_Resources`:** The home for canonical `SoT` notes.
- **`10_Actions/11_Projects`:** Project Dashboards that link to `HEAD` (thinking) and `SoT` (reference) notes.
- **Todoist (The Runtime):** Contains only executable tasks, often synced from and linking back to an Obsidian note that holds the context.
- **LLM (The Zero-Toil Engine):** Acts as a background service triggered by the user to perform refinement and synthesis.

---

## 7. Reality as a Unit Test (The Execution & Ignition Protocol)

The "Next Test" is not just a task; it is a **verifiable interface** between the internal mental model (Thinking) and external reality (Doing).

### The Compilation Target

You do not finish thinking when you have an answer; you finish when you have a **query for reality**.

-   **Input:** Tension/Hypothesis (HEAD Note).
-   **Function:** The Next Test (Action).
-   **Return Value:** Data/Outcome (Update SoT).

### The Specification (Acceptance Criteria)

To qualify as a "Next Test," an action must meet three criteria:

1.  **Atomic Scope:** The smallest possible unit of work (<15 mins).
2.  **Binary Outcome:** It must Pass or Fail. (e.g., "Did the script return error 401? Yes/No").
3.  **Learning Objective:** Focus on *information gain*, not just output.

### The Refactoring Logic (Thinking -> Testing)
-   **Confusion:** "I don't know X" -> **Test:** "Search docs for X. Found/Not Found."
-   **Assumption:** "I think X causes Y" -> **Test:** "Disable X. Does Y still happen?"
-   **Design:** "I need to build Z" -> **Test:** "Draft ugliest version of Z in 5 mins."

### The Ignition Protocol (Stimulus Injection)

[[Logic Does Not Produce Dopamine|Logic does not produce dopamine]]. To generate the energy for execution, you must convert "Work" (Boring Command) into "Inquiry" (Interesting Question). Use these 3 Energy Hacks to "Refactor" boring tasks:

1.  **The "Mystery" Hack (Hypothesis):** Refactor a chore into a bet.
    -   *Boring:* "Update CSS."
    -   *Ignition:* "Hypothesis: I can break the layout if I change padding to 50px. Does the flexbox hold?"
2.  **The "Time Trial" Hack (Urgency):** Refactor an infinite task into a binary sprint.
    -   *Boring:* "Clear inbox."
    -   *Ignition:* "Can I process 10 items in 3 minutes? Binary Outcome: Yes/No."
3.  **The "Spite" Hack (Logic Linter):** Refactor compliance into rebellion.
    -   *Boring:* "Write scope."
    -   *Ignition:* "Open a HEAD note and argue why this project is stupid." (Frustration generates heat, which can be channeled into solving the problem).

**The Workflow:** Select Task -> Open HEAD Note -> Refactor to Experiment -> **Wait for Spark** -> Execute.

---

## 8. Information Architecture & Retrieval Strategy

The core challenge of any knowledge system is retrieving the right thought at the right time. Previous iterations failed because files (SoT, MOC, HEAD, Summary) **competed for authority**, creating decision fatigue.

### The Unified Hierarchy

PRODOS establishes a clear, non-competing hierarchy for file types:

| File Type | Role | The Question It Answers |
| :--- | :--- | :--- |
| **SoT Notes** | **The Canon (Authority)** | "What is the trusted, current state of the system?" (The Destination) |
| **MOCs** | **The Map (Entrypoint)** | "Where do I start? Show me the landscape." (The Table of Contents) |
| **HEAD Notes** | **The Workbench (Active)** | "What am I figuring out right now? What is the tension?" (The Scratchpad) |
| **Base Files** | **The Dashboard (Dynamic)** | "Show me a live list of all X." (The Saved Search) |

### The "Safe Search" Guarantee

To fix "Version Control Failure," the retrieval system must enforce the "Master Branch" view.

- **Configuration:** Search tools must exclude `HEAD` / `Thinking` folders by default.
- **The Promise:** When you search for a topic, you should see **one result**: The SoT. You can blindly trust it because you know you *always* merge to Master.

### The Retrieval Algorithm
1.  **Specific Topic:** Search directly for the **SoT** (e.g., "ProdOS SoT"). This is the source of truth.
2.  **Broad Topic:** Start with the **MOC**. It provides the context and links to the correct SoTs.
3.  **System View:** Use **Base Files** (`.base`) as dashboards to see the high-level state of the vault.

### The Organization Logic (Feed, Don't Compete)
-   **Frictionless Capture:** Daily Notes are for raw capture. Do not organize here.
-   **Integration:** When a raw thought belongs to a topic, **do not create a new note.** Feed it into the **Integration Queue** of the existing SoT.
-   **Synthesis:** The LLM processes the Integration Queue to update the SoT. This ensures the SoT remains the living canon, preventing "competitor notes" from splintering knowledge.

---

## 9. Maintenance Rituals: The Hansei Feedback Loop

The system is not static; it requires active maintenance to prevent "Trust Decay." This is not "admin"; it is the mechanism of improvement.

> **Philosophy:** "No problem is a problem." If you don't find friction, you are blind to it.

### The Weekly Hansei Protocol
1.  **Identify Friction:** Analyze where the system failed (e.g., missed habits, untrusted lists).
2.  **Adjust Process:** Do not blame willpower. Tweak the **Environment** or **Rules**.
    -   *Example:* "I missed writing 3 times. Adjustment: Move writing to 8 AM timebox."
3.  **Verify Alignment:** Check if actions align with Identity/Goals. Behavior reveals true purpose.

---

## 10. Open Questions & Tensions

- **Tension:** The core struggle remains balancing **Action (Kinetic)** vs. **Thinking (Dynamic)**. The system mitigates this by demanding that all "Thinking" cycles must terminate in an "Action" (The Next Test).
- **Confidence Gap:** The system's trustworthiness depends entirely on the discipline of adhering to the synthesis loop. If `HEAD` notes proliferate without being integrated into `SoT` notes, trust decays.

## 11. Related Components
- [[SoT - PRODOS - The Cognitive Loop (A-C-T Framework)]]
- [[SoT - Process Primacy (Systems Over Goals)]]
- [[SoT - Temporal Management (Blocking and Boxing)]]
- [[The War of Art - Resistance and Turning Pro]]
- **Example Implementation:** [[Detailed Example From Spark to Synthesis]]

## 12. Status & Roadmap

**Current Status:** ProdOS v5.0 is considered **production-ready**.
- **Core:** Architecture consolidated and operational.
- **Integrations:** Obsidian-Todoist bidirectional sync is robust. Jira data ingestion is functional (pending auth fix).
- **Operations:** Phase 1 commands (`/daily-plan`, `/engage-action`) are live.

**Roadmap:**
- **Phase 2:** Automated background sync and system synchronization.
- **Phase 3:** Advanced AI decision support (energy-aware task selection).
- **Phase 4:** Smart capture processing and proactive notifications.
- **Phase 5:** Mobile accessibility and team coordination.
