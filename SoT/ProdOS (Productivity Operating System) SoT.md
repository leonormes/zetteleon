---
aliases: [My Productivity System, Principle-Centered Productivity, ProdOS]
confidence: 
confidence-gaps: [The friction of maintaining the system during low-energy states could lead to abandonment., The technical implementation of the LLM Chief of Staff is complex and not fully defined.]
created: 2025-11-13T17:30:00Z
decay-signals: []
epistemic: 
last-synthesis: 2025-11-13
last_reviewed: 
modified: 2025-11-13T17:04:37Z
mvu-hash: "" # To be calculated
purpose: 
quality-markers: ["Synthesized from over a dozen detailed project notes."]
related-soTs: ["[[Bridging the Intention-Action Gap SoT]]", "[[Evolutionary Note System SoT]]"]
resonance-score: 1
review_interval: 
see_also: []
source_of_truth: true
status: 
supersedes: ["[[01 - Capture Phase Requirements]]", "[[02 - GTD (Getting Things Done)]]", "[[03 - ProdOS (Productivity Operating System)]]", "[[03a A Unified System for Principle-Centered Productivity and Integrated Knowledge Management]]", "[[04 - Atomic Actions and Next Actions]]", "[[05 - Horizons of Focus]]", "[[06 - The Clarify and Organize Workflow]]", "[[07 - LLM as a Productivity Partner (CoS)]]", "[[08 - Obsidian for PKM]]", "[[09 - Todoist for Task Execution]]", "[[10 - The Review and Reflection Process]]", "[[11 - Time Management (Timeboxing and The Unschedule)]]", "[[12 - Core Principles and Values]]", "[[act framework]]", "[[Biggest problem]]"]
synthesis-count: 1
tags: [adhd, gtd, llm, pkm, prodos, productivity, SoT]
title: ProdOS (Productivity Operating System) SoT
trust-level: stable
type: SoT
uid: 
updated: 
---

## 1. Working Knowledge (Stable Foundation)

ProdOS is a cognitive operating system designed to manage life and work by unifying **GTD-based productivity** with **Zettelkasten-based knowledge management**. It is built for an ADHD neurotype, using an **LLM "Chief of Staff" (CoS)** to augment executive function. Its core purpose is to make principle-centered living automatic, not aspirational, by externalizing thought, clarifying commitments, and guiding action based on pre-defined values.

## 2. Current Understanding (Coherent Narrative)

ProdOS solves the "thought loop" and "Collector's Fallacy" problems by creating a trusted, external system for both tasks and knowledge. It integrates **Obsidian** (for thinking and planning) and **Todoist** (for execution) via the LLM CoS.

The system is built on a hierarchy of principles, most importantly the **Indistractable Stack (Self > Relationships > Work)**, which is enforced algorithmically. It uses the **A-C-T (Action-Container-Thought) Framework** as its core processing loop, ensuring that amorphous ideas are converted into concrete, minimal actions (MVAs) and that the learnings from those actions are reintegrated into the knowledge base. This creates a virtuous cycle of thoughtful action, rather than aimless thinking or unreflective doing.

## 3. Integration Queue (Structured Input)
*(This queue is ready for new insights on ProdOS.)*

## 4. Understanding Layers (Progressive Abstraction)

- **Layer 1: Basic Mental Model:** My brain is for *having* ideas, not *holding* them. ProdOS is my trusted external system that holds my commitments and knowledge, telling me what to do next based on my own values.
- **Layer 2: Mechanistic Explanation (The GTD/ADHD Engine):** ProdOS implements the five stages of GTD (Capture, Clarify, Organize, Reflect, Engage), but adapts them for ADHD.
  - **Capture:** Is made frictionless and ubiquitous.
  - **Clarify/Organize:** Is facilitated by the LLM CoS, which uses the A-C-T framework to turn vague thoughts into atomic actions and projects.
  - **Reflect:** Is a semi-automated, guided weekly review that analyzes domain balance and surfaces strategic insights.
  - **Engage:** Is driven by a priority algorithm that enforces the Indistractable Stack, ensuring I work on what's truly important, not just what's urgent.
- **Layer 3: Protocol/Detail Level (The Technical Architecture):**
  - **Data Layer:** The Obsidian vault is the source of truth, with a defined folder structure (`00_System`, `01_Inbox`, `02_Projects`, `10_PKM`, etc.) and a unified metadata schema for all notes. Todoist is the action inventory.
  - **LLM Chief of Staff (CoS):** An LLM agent with three modes (Executor, Socratic Coach, Strategic Advisor) that interacts with the data layer. Key commands include `/capture`, `/cleave`, `/engage-action`, and `/conduct-review`.
  - **Priority Algorithm:** `Score = ((Importance × 0.6) + (BigRockAlignment × 0.3) + (ContextMatch × 0.1)) * DomainMultiplier`, where the `DomainMultiplier` for `self` (1.5x) and `relationships` (1.2x) mathematically prioritizes life balance over `work` (1.0x).
  - **A-C-T Framework:** The core processing loop:
        1. **Action:** Use an LLM to turn a vague goal into a Minimum Viable Action (MVA).
        2. **Container:** Create a "one-note-container" in Obsidian to define the scope of the MVA.
        3. **Thought:** After executing the MVA, use an LLM to reflect on the outcome and define the *next* MVA.

## 5. Minimum Viable Understanding (MVU)

- **Established:** 2025-11-13
- **Status:** **STABLE**
- 1. Capture every thought and task into a single inbox (e.g., Obsidian Daily Note) with zero friction.
- 2. Once a day, process this inbox. For each item, decide if it's trash, reference, a project, or a single action.
- 3. Move single actions to a "Next Actions" list.
- 4. When ready to work, consult only the "Next Actions" list.

## 6. Battle Testing and Decay Signals

- **Core Claim(s):**
    1. A system that algorithmically enforces personal values (Indistractable Stack) will lead to better life balance than one relying on willpower.
    2. Externalizing the "clarify" step to an LLM CoS will reduce the activation energy for processing inboxes, a common failure point for ADHD-based systems.
- **Current Status:** **UNDER REVIEW**. The system is designed but not yet fully implemented and battle-tested.

## 7. Tensions, Gaps, and Cross-SoT Coherence

- **Tensions:** The desire for a perfect, comprehensive system (Collector's Fallacy) vs. the need for a simple, low-friction system that works even on low-energy days.
- **Confidence Gaps:** The technical implementation of the LLM CoS, especially the "cleaving" process and the seamless integration with Obsidian/Todoist, is the biggest unknown.
- **Cross-SoT Coherence:** This SoT is the master plan that operationalizes the principles found in `[[Bridging the Intention-Action Gap SoT]]` and `[[Evolutionary Note System SoT]]`. It is the "how" to their "what" and "why".

## 8. Sources and Links

- **Primary Sources:** The collection of notes in `200_projects/LLMPKM/` that detail the system's philosophy, architecture, and workflows.
- **Related MOCs:** [[ADHD and Motivation MOC]]
- **Related SoTs:** [[Bridging the Intention-Action Gap SoT]], [[Evolutionary Note System SoT]]
- [[ProdOS System Overview and Development Progress]]
