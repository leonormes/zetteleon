---
aliases: [My Productivity System, ProdOS, The PRODOS Architecture]
confidence: 5/5
confidence-gaps: []
created: 2025-11-13T17:30:00Z
decay-signals: []
epistemic: 
last-synthesis: 2025-12-07
last_reviewed: 2025-12-07
modified: 2025-12-07T18:13:20Z
purpose: "The Master Index Note and System Specification for PRODOS, defining its architecture as an ADHD-centric cognitive augmentation system."
quality-markers: ["Clarifies the Human-in-the-Loop LLM workflow.", "Defines the core cognitive loop.", "Establishes verifiable acceptance criteria."]
related-soTs: ["[[SoT - PKM Confidence and Acceptance Criteria]]", "[[SoT - PRODOS - Action Management (GTD)]]", "[[SoT - PRODOS - Knowledge Synthesis (Thinking)]]", "[[SoT - PRODOS - Structure & Storage (PARA/PKM)]]"]
resonance-score: 10
review_interval: "3 months"
see_also: []
source_of_truth: true
status: stable
supersedes: ["[[02 - GTD]]", "[[08 - Obsidian for PKM]]", "[[Complete Context ProdOS System]]", "[[Old ProdOS Product Description]]", "[[ProdOS System Overview and Development Progress]]", "[[The why of my zettelkasten]]"]
tags: [adhd, architecture, prodos, SoT, system_design]
title: SoT - PRODOS (System Architecture)
type: SoT
uid: 
updated: 
---

## 1. Definitive Statement

> [!definition] Definition
> PRODOS is a **cognitive augmentation system** designed to operate as an "extended mind" for a developer with ADHD. It offloads executive functions—such as context restoration, task initiation, and knowledge synthesis—to a structured, LLM-powered workflow.
>
> Its purpose is to transform a Personal Knowledge Management (PKM) system from a passive library into an **active laboratory for thinking and action**.

---

## 2. The Core Problem: Why PRODOS Exists

Conventional PKM and productivity systems fail because they are not designed for the ADHD brain. They often exacerbate challenges like **task initiation paralysis**, **executive dysfunction**, and **dopamine dysregulation**. PRODOS is built to directly solve these failures:

| Failure Mode                | The Problem                                                                                                                                              | PRODOS Solution                                                                                                                                                  |
| :-------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **The Collector's Fallacy** | The dopamine loop of collecting information creates "content sprawl" and overwhelm, mistaking acquisition for understanding.                             | **Action over Collection:** The system forces the conversion of knowledge into testable experiments and Minimum Viable Actions (MVAs).                           |
| **Context Loss**            | The rich mental model of a project evaporates over time. Returning to flat notes requires high activation energy, leading to re-research or abandonment. | **The 60-Second Test:** The system is designed to allow a complete cognitive state restore (MVU + Next Action) in under a minute.                                |
| **Administrative Friction** | The "toil" of organizing, tagging, and processing notes drains executive function, causing the system to be abandoned.                                   | **Zero-Toil Automation:** The user's role is frictionless capture. A "Chief of Staff" LLM handles all synthesis, structuring, and metadata.                      |
| **Lack of Trust**           | Static notes become outdated as thinking evolves, making the system an unreliable "graveyard" of past thoughts.                                          | **Trust Through Verifiability:** The system's effectiveness is not a "gut feeling" but is measured against clear acceptance criteria. SoTs are living documents. |

---

## 3. The Architecture: An Action-Oriented Cognitive Loop

PRODOS functions as a continuous loop that processes thought, generates action, and synthesizes results. It operates on the **Compass-over-Clock** paradigm, prioritizing values and purpose over urgency.

**Capture -> Refine -> Synthesize -> Act -> Repeat**

1.  **Capture (Human):** Raw, messy, unstructured thoughts are captured into a frictionless entry point (Daily Note). "Capture Now, Structure Later."
2.  **Refine (LLM):** The LLM acts as a **Convergent Tool**, applying the **Raw Input Refactoring Protocol** to parse the raw input into a structured `HEAD` note.
    *   **Isolation:** Extract raw text into a dedicated HEAD note.
    *   **Parsing:** Separate concerns into `Spark` (Trigger), `Model` (Hypothesis), and `Tension` (Conflict).
    *   **Logic Linter:** Debug the thought by stripping emotion ("I hate this") to find the signal ("The docs are missing X").
    *   **Compilation:** Convert the tension into a verifiable **Micro-Experiment** (The Next Test).
3.  **Synthesize (LLM & Human):** The LLM automates the "Chronos Synthesis" ritual, updating the canonical `SoT` note with new insights from `HEAD` notes. The user performs the final validation.
4.  **Act (Human):** The output of thinking is not another note, but a **verifiable `Next Action`**—a test, an experiment, or a command—to be executed in the real world.

---

## 4. The Note Schema: Capturing Thought vs. Storing Fact

The system maintains a strict separation of concerns between thinking and knowing.

### A. HEAD Notes (The Workbench)
- **Purpose:** To capture the *process of thinking*. Records the struggle, assumptions, confusion, and the evolution of a mental model. They are volatile and exist to be processed.
- **Voice:** First-person ("I think," "I'm confused about," "My hypothesis is").
- **Key Sections:** `The Spark`, `My Current Model`, `The Tension`, `The Next Test`.

### B. LIB/SoT Notes (The Canon)
- **Purpose:** To be the trusted **System of Record** for stable, verified knowledge and the `Current Understanding` of a topic.
- **Voice:** Third-person, objective.
- **Key Constraint:** Must be durable and updated only through a formal synthesis process. It is the single source of truth that you can trust when returning to a topic.

---

## 5. Trust & Verifiability: The Acceptance Criteria

PRODOS is considered "working" only when it consistently passes these two acceptance tests:

1.  **The 60-Second Context Restoration Test:** For any active project, can I open the relevant Project/SoT note and recall the **Minimum Viable Understanding (MVU)** and the very **Next Action** in under 60 seconds?
2.  **The Reuse Score:** For any new project, was the system successfully leveraged to find and reuse existing knowledge, avoiding at least 30 minutes of new research?

---

## 6. Structural Implementation & Integrations

The folder structure and tool integration reflect the cognitive loop. PRODOS v5.0 represents the "ultimate maturation" of the system, consolidated into a highly optimized **4-file system** (down from 72) to maximize LLM efficiency (75-90% faster loading).

- **`00_Inbox` / Daily Note:** Frictionless capture.
- **`20_Thinking/21_Workbench`:** The home for active `HEAD` notes where cognitive work happens.
- **`30_Library/31_Resources`:** The home for canonical `SoT` notes.
- **`10_Actions/11_Projects`:** Project Dashboards that link to `HEAD` (thinking) and `SoT` (reference) notes.
- **Todoist (The Runtime):** Contains only executable tasks, often synced from and linking back to an Obsidian note that holds the context.
- **LLM (The Zero-Toil Engine):** Acts as a background service triggered by the user to perform refinement and synthesis.

---

## 7. Minimum Viable Understanding (MVU) & The Architect's Triage

1.  **Capture** every thought, no matter how messy, into the Daily Note.
2.  **Triage (The Router):** Categorize the input by **Metabolic State**:
    *   **Kinetic (#state/action):** A defined task. Move to Todoist.
    *   **Static (#state/lib):** A fact or reference. Move to SoT Library.
    *   **Dynamic (#state/head):** An unresolved problem or insight. Keep in HEAD.
3.  **Figure Out** in a `HEAD` note. The goal is always to define the `Next Test`.
4.  **Store** stable conclusions in a `SoT` note via synthesis.
5.  **Do** the `Next Test` and capture the results, restarting the loop.

## 8. Open Questions & Tensions

- **Tension:** The core struggle remains balancing **Action (Kinetic)** vs. **Thinking (Dynamic)**. The system mitigates this by demanding that all "Thinking" cycles must terminate in an "Action" (The Next Test).
- **Confidence Gap:** The system's trustworthiness depends entirely on the discipline of adhering to the synthesis loop. If `HEAD` notes proliferate without being integrated into `SoT` notes, trust decays.

## 9. Related Components
- [[SoT - PRODOS - Action Management (GTD)]]
- [[SoT - PRODOS - Knowledge Synthesis (Thinking)]]
- [[SoT - PRODOS - Structure & Storage (PARA/PKM)]]
- [[SoT - PRODOS - The Cognitive Loop (A-C-T Framework)]]
- [[SoT - PKM Confidence and Acceptance Criteria]]

## 10. Status & Roadmap

**Current Status:** ProdOS v5.0 is considered **production-ready**.
- **Core:** Architecture consolidated and operational.
- **Integrations:** Obsidian-Todoist bidirectional sync is robust. Jira data ingestion is functional (pending auth fix).
- **Operations:** Phase 1 commands (`/daily-plan`, `/engage-action`) are live.

**Roadmap:**
- **Phase 2:** Automated background sync and system synchronization.
- **Phase 3:** Advanced AI decision support (energy-aware task selection).
- **Phase 4:** Smart capture processing and proactive notifications.
- **Phase 5:** Mobile accessibility and team coordination.
