---
aliases: [Chain of Explainability, Human 3.0 Framework, Self-Capture Architecture]
confidence: 5/5
created: 2025-12-24T12:12:06Z
epistemic: synthesis
last_reviewed: 2025-12-24
modified: 2025-12-28T09:56:09+00:00
purpose: Canonical source of truth for The Telos Method, a hierarchical framework for self-knowledge and AI context integration.
review_interval: 6 months
see_also: ["[[SoT - Identity-Based Habit Formation]]", "[[SoT - PRODOS (System Architecture)]]", "[[SoT - The Extended Mind Thesis]]"]
source_of_truth: []
status: stable
tags: ["ai_integration", "framework", "strategy", "telos"]
title: SoT - The Telos Method
type: SoT
uid:
updated:
---

> [!definition] Definition
> **The Telos Method:** An open-source framework for "self-capture," designed to create deep machine-readable context about a user's values and goals.
> **Human 3.0:** The shift from "Task Executor" (Human 2.0) to "Idea Originator," required as AI commoditizes execution.

## 1. Minimum Viable Understanding (MVU)

The Telos Method provides **"Chain of Explainability"** for every action. It prevents aimlessness by ensuring every **Project** has a clear lineage back to a core **Problem** the user wants to solve. It acts as the "Context Layer" that allows AI agents to act with high autonomy and alignment.

---

## 2. The Telos Hierarchy (The Stack)

The framework organizes self-knowledge into a strict directed acyclic graph (DAG):

| Layer | Definition | ProdOS Mapping |
|:--- |:--- |:--- |
| **1. Problems** | *Foundational.* Specific issues in the world you aim to address (e.g., "Software is insecure"). | **Vision / Values** |
| **2. Mission** | *Intent.* The primary statement of what you will do about the Problem. | **Life Goal** |
| **3. Narratives** | *Identity.* "Quick handles" or scripts to explain yourself to others and combat impostor syndrome. | **Identity Pacts** |
| **4. Goals** | *Targets.* Concrete, measurable milestones (e.g., "1M Downloads"). Categorized by urgency. | **Strategic Goals** |
| **5. Challenges** | *Obstacles.* Specific barriers preventing the Goal (e.g., "Lack of UX skills"). | **Tensions / Blockers** |
| **6. Strategies** | *Method.* "A very specific way you are addressing a challenge." The detailed plan of attack. | **Strategy Layer** |
| **7. Projects** | *Undertaking.* Long-term undertakings that "fall out" of the Strategy. | **Projects (Level 1)** |

---

## 3. The Chain of Explainability (Logic Flow)

> **Why am I doing this Project?**
> Because it is part of a **Strategy**...
>...to overcome a **Challenge**...
>...that is blocking a **Goal**...
>...which serves my **Mission**...
>...to solve a specific **Problem**.

### The Military Analogy

- **Challenge:** 10,000 enemy troops vs. 1,000 friendly. Direct fight = Loss.
- **Strategy:** Asymmetric warfare (Night attack, camouflage).
- **Project:** Train troops for night ops and deploy.

---

## 4. AI Integration (Context Injection)

The Telos Method is designed to be **Machine Readable**.

- **Format:** Markdown, JSON, or Graph (Excalidraw).
- **Usage:** This context is fed to AI agents (e.g., ProdOS LLM) to enable "Threat Modeling" of plans and identifying "Neglected Goals."
- **Benefit:** Allows the AI to function as a Chief of Staff that understands *why* you are doing something, not just *what* you are doing.

---

## 5. Implementation in ProdOS

- **Storage:** Defined in `02_bases/Telos.base` or within `SoT` notes for each Life Domain.
- **Review:** The "Horizon Alignment Check" in the Weekly Review validates the Chain of Explainability.
- **Project Initiation:** Every new Project must declare its Parent Strategy and Challenge.

---

## 6. Related Concepts

- **[[AI-Resilient Task Taxonomy]]**
- **[[Orchestrating the Inspiration Economy_ Agentic Frameworks and Human Augmentation]]**
- **[[SoT - PRODOS - The Cognitive Loop (A-C-T Framework)]]**
