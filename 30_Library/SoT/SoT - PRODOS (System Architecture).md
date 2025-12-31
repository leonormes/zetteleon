---
aliases: ["My Productivity System", "ProdOS", "The PRODOS Architecture", "The Unified Runtime", "ProdOS Manual"]
confidence: "5/5"
created: 2025-11-13T00:00:00Z
epistemic: "The canonical definition of the ProdOS system architecture."
last_reviewed: "2025-12-30"
modified: 2025-12-30T17:49:05+00:00
purpose: "The Master Index Note and System Specification for PRODOS, defining its architecture as an ADHD-centric cognitive augmentation system."
review_interval: "3 months"
see_also: ["[[SoT - PRODOS - The Cognitive Loop (A-C-T Framework)]]", "[[SoT - PRODOS - Structure & Storage]]", "[[SoT - PRODOS - Action Management (GTD)]]", "[[SoT - The Extended Mind Thesis]]"]
source_of_truth: []
status: "stable"
tags: ["architecture", "hansei", "prodos", "system_design", "topic/health/adhd"]
title: SoT - PRODOS (System Architecture)
type: "SoT"
uid: 
updated: 
---

## 1. Definitive Statement

> [!definition] The Core Philosophy
> ProdOS is a **Thinking Utility**, not a storage archive. Its purpose is to bridge the gap between "Knowing" and "Doing" for an Interest-Based Nervous System (ADHD).
>
> **The Metric:** We do not measure "notes created." We measure "clarity achieved" and "actions taken." If the system does not change reality, it is failing.

### 1.1 The Epistemic Stance: Factory vs. Museum

- **The Museum Model (Reject):** Collecting facts, hoarding definitions, and "gardening" knowledge for a hypothetical future.
- **The Factory Model (Accept):** A high-throughput runtime. Input (Chaos) -> Processing (Thinking) -> Output (Action).
- **The Rule:** **"Utility Over Truth."** We do not aim to catalogue the world. If a note does not help you *think* or *act*, it is noise.

---

## 2. The Core Problem: Hardware Constraints

The system is engineered to patch three specific "hardware failures" in the ADHD brain:

| Failure Mode | Description | The ProdOS Patch |
|:--- |:--- |:--- |
| **RAM Failure** | Working memory is volatile. We cannot hold a plan and execute it simultaneously. | **Externalize State:** All thinking must happen on "disk" (Obsidian), not in the head. |
| **Initiation Paralysis** | We cannot force "importance"; we can only trigger Interest, Novelty, Challenge, Urgency, or Passion (INCUP). | **The Ignition Protocol:** Reframing boring tasks as "Mysteries" or "Spite" to manufacture dopamine. |
| **Context Decay** | Re-loading a mental model is expensive. If "re-entry" takes >60 seconds, the project is abandoned. | **The Project Anchor:** Strict "Save State" protocols to ensure <60s context restoration. |

### 2.1 System Failure Modes (Traps)

* **The "Shoulder Massage" (Zettelkasten):** Using infinite linking as a displacement activity. It feels productive but solves nothing.
* **The "Graze vs Process" Gap:** Collecting inputs (easy) without synthesizing them (hard), leading to "Note Hoarding."

---

## 3. The Architecture: The Thinking Machine

ProdOS integrates three components to create a "Cognitive Augmentation System":

| Component | Role | Analogy |
|:--- |:--- |:--- |
| **Obsidian Vault** | **The Wisdom (Memory)** | **The Library.** Durable, structured, long-term storage of principles and SoTs. |
| **Gemini CLI** | **The Agent (Processor)** | **The Research Assistant.** Active, real-time reasoning and synthesis. |
| **`gemini.md`** | **The Protocol (Instruction)** | **The Syllabus.** The master prompt that defines *how* the Agent uses the Library. |

### 3.1 Dual-Axis Engagement

The system manages two dimensions of work:

1. **Horizontal (Time):** The Calendar/Todoist. Manages linear progression and deadlines.
2. **Vertical (Focus):** The Workbench/Obsidian. Manages depth, "rabbit holes", and flow states.

---

## 4. The Logic: The Tri-State Router

To prevent decision fatigue, **all inputs** (Inbox, Thoughts) and **all outputs** (Thinking sessions) must be routed to one of three metabolic states. There is no "Maybe."

| State | Definition | Destination | Protocol |
|:--- |:--- |:--- |:--- |
| **1. KINETIC** | **Action.** I know the physical next step. | **Todoist** | Extract Task -> Archive Note. |
| **2. STATIC** | **Reference.** I learned a fact / found a resource. | **SoT Folder** | Merge into Canon -> Archive Note. |
| **3. DYNAMIC** | **Thinking.** I am stuck, confused, or designing. | **Workbench** | Initialize **A-C-T Loop** in a `HEAD` Note. |

---

## 5. The Runtime: The A-C-T Loop

When routed to **Dynamic (Thinking)**, do not just "journal." Execute the **A-C-T Framework** to force convergence.

*For full procedure, see: [[SoT - PRODOS - The Cognitive Loop (A-C-T Framework)]]*

1. **Phase A (Action):** Define the **Minimum Viable Action (MVA)**. "What is the single physical output of this session?"
2. **Phase C (Container):** Work inside a bounded `HEAD` note. Use the **120-Second Commitment** if stuck.
3. **Phase T (Thought):** Synthesize the result. **Squash and Merge** insights into the SoT.

---

## 6. Structure: Version Control for the Mind

The system mimics Git Version Control to separate "Work" from "Knowledge."

*For full folder specs, see: [[SoT - PRODOS - Structure & Storage]]*

| Feature | HEAD Notes (Working Tree) | SoT Notes (Master Branch) |
|:--- |:--- |:--- |
| **Location** | `20_Thinking/21_Workbench` | `30_Library/SoT` |
| **Role** | **The Workbench.** Volatile, messy, active. | **The Canon.** Stable, trusted, authoritative. |
| **Protocol** | **Continuous Commit.** Log everything. | **Squash & Merge.** Synthesize, then delete the branch. |

---

## 7. Operational Protocols (Mechanisms)

### 7.1 The Project Anchor (Context Saver)

Every active project must have a **Project Note** with a `## Current State` block.

* **Protocol:** At the end of a session, update this block with:
    * **Now:** What was just done.
    * **Next:** The exact next physical step.
    * **Why:** The current design intent.
* **The Test:** You must be able to read this and resume flow in **< 60 seconds**.

### 7.2 The "Merge and Delete" Ritual

To prevent "Archive Guilt," `HEAD` notes are ephemeral.

* **The Ritual:** Once a problem is solved (Kinetic) or understood (Static), you extract the value and **Delete/Archive** the `HEAD` note.
* **Result:** A clean workspace.

### 7.3 The Ignition Protocol (Stimulus Injection)

If paralyzed, do not rely on willpower. Inject stimulus:

1. **Mystery:** "Hypothesis: I can break X..."
2. **Time Trial:** "Can I do X in 3 mins?"
3. **Spite:** "Prove why this is stupid."

---

## 8. Status & Roadmap

**Current Status:** ProdOS v5.0 (Stable).
* **Core:** Architecture consolidated.
* **Integrations:** Obsidian-Todoist Sync operational.
* **Next:** Automated background sync and advanced AI decision support.
