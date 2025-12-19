---
aliases: [Low Activation Energy, ProdOS Simplicity, The Re-entry Protocol]
confidence: 5/5
created: 2025-12-11T20:05:12Z
epistemic: principle
last_reviewed: 2025-12-14
modified: 2025-12-19T10:12:34Z
purpose: To define the core design principles of ProdOS—Simplicity and Re-entry—that enable an ADHD brain to overcome context loss and executive dysfunction.
review_interval: 6 months
see_also: ["[[Breaking the Creation Cycle]]", "[[SoT - PRODOS - Action Management (GTD)]]", "[[SoT - PRODOS (System Architecture)]]"]
source_of_truth: true
status: stable
tags: [adhd, principles, prodos, simplicity, workflow]
title: SoT - Simplicity and Re-entry (ProdOS Principles)
type: SoT
uid: 2025-12-11-SIMPLICITY
updated: 
version: 2
---

## 1. Definitive Statement

> [!definition] Definition
> **Simplicity** in ProdOS is the radical reduction of cognitive load ("Don't Make Me Think") to prevent executive paralysis. **Re-entry** is the explicit design of workflows that allow for low-friction resumption of work after an interruption, acknowledging that for the ADHD brain, context is volatile and must be externalized.

---

## 2. Radical Simplicity ("Don't Make Me Think")

The system must be simpler than the chaos it manages.

### 2.1 Minimal Components

- **Rule:** If a component requires maintenance, it is a liability.

- **Implementation:** Limit moving parts to the absolute essential: One Inbox, One Active List, One Archive.

- **Anti-Pattern:** Complex folder structures, intricate tagging schemas, or multi-step filing systems that serve as "Productivity Porn" rather than functional tools.

### 2.2 Minimal Dependencies

- **Rule:** Fragility scales with complexity.

- **Implementation:** Rely on **Fundamentals** (Plain Text, Standard Libraries) over complex plugins or proprietary formats. Ask: "Is this feature essential for *output*, or is it just cool?"

### 2.3 Intuitive Workflow

- **Rule:** The path of least resistance must be the right path.

- **Implementation:** Capture and retrieval must be obvious. There should be no complex decision tree for "Where does this note go?" The default answer is always the [[00_Inbox]].

---

## 3. The Principle of Re-entry (Context Restoration)

For the ADHD brain, "stopping" is often permanent because the context evaporates. The system must be designed for **Crash-Proof Re-entry**.

### 3.1 Low Activation Energy

- **Concept:** The effort required to *start* a task must be practically zero. High activation energy leads to procrastination.

- **Mechanism:** Break tasks down until the first step is trivial (e.g., "Open file," not "Write report").

### 3.2 The Re-entry Rituals

To combat context loss, ProdOS enforces specific protocols to "save state" before exiting:

1. **The Parking Lot:** Never close a project without writing down the *exact* next step. "I stopped at X, the next action is Y."
2. **The Project Anchor:** Every project must have a "Current State" block in its dashboard. Reading this block should restore the mental model in < 60 seconds.
3. **Warm Start:** Automate the environment setup. A single command should open all necessary files and terminals, removing the friction of "getting ready to work."

---

## 4. Related Concepts

- [[SoT - PRODOS - Action Management (GTD)]] - Detailed Re-entry protocols (4.5).

- [[SoT - The Cognitive Physiology of Task Execution]] - Why activation energy matters.
