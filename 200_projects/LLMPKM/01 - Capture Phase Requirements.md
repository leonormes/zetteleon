---
aliases: []
confidence: 
created: 2025-11-06T00:00:00Z
epistemic: 
last_reviewed: 
modified: 2025-11-09T11:31:01Z
purpose: Documenting requirements for the Capture phase of ProdOS
review_interval: 
see_also: []
source_of_truth: []
status: draft
tags: [Capture, GTD, ProdOS, Requirements]
title: 01 - Capture Phase Requirements
type: requirements
uid: 
updated: 
version: 0.1
---

## **ProdOS: Capture Phase Requirements**

### **1.0 Purpose and Mindset**

The **Capture** phase is the foundational stage of the ProdOS (Productivity Operating System). Its primary purpose is to externalize every commitment, idea, task, and piece of information from the user's mind into a small, trusted set of digital inboxes with the least possible friction.

This phase is governed by an ADHD-friendly mindset of **"Capture Now, Structure Later."** The emphasis is on speed, completeness, and reducing the cognitive load of "remembering to remember." The system must act as a ubiquitous, always-on "extended mind," allowing the user to capture thoughts instantaneously before the context is lost or a decision can be made about the item's importance. The goal is to achieve a state of "mind like water," free from the psychic drag of uncaptured "stuff."

### **2.0 Functional Requirements**

The capture system must meet the following functional requirements to successfully implement the ProdOS philosophy:

| ID | Requirement | Description | Rationale |
| :--- | :--- | :--- | :--- |
| **2.1** | **Unstructured Input Processing** | The system must be able to accept and parse unstructured, natural language inputs. This will be primarily facilitated by the LLM "Chief of Staff" (CoS) via a `/capture-thought` command. | Reduces friction by allowing the user to capture thoughts as they occur, without needing to pre-format or categorize them. Aligns with the "Capture Now, Structure Later" principle. |
| **2.2** | **LLM-Powered Triage** | The LLM CoS must analyze unstructured inputs and perform an initial triage, suggesting a classification (e.g., Project, Next Action, Reference, Someday/Maybe) for the Clarification phase. | Automates the first step of processing, lowering the barrier to the "Clarify" workflow and preventing inbox build-up. |
| **2.3** | **Centralized Default Inboxes** | The system must have a minimal number of designated default locations for all new captures. This includes the Todoist inbox for tasks and a dedicated `/000_inbox` folder in Obsidian for notes and ideas. | Prevents "capture friction" by eliminating the need to decide where an item should go at the moment of capture. |
| **2.4** | **Multi-Modal Capture** | The system must support capture from various sources, including but not limited to: quick-add shortcuts (Todoist), voice memos, email forwarding, and web clippers. | Ensures capture is ubiquitous and can happen from any context (mobile, desktop, on the go), which is critical for an ADHD-friendly workflow. |
| **2.5** | **Separation of Capture & Clarification** | The act of capturing an item must be a distinct and separate process from the act of clarifying or organizing it. Captured items must land in an inbox to await a later, dedicated "Clarify" session. | Protects the low-friction nature of capture. Mixing capture with organization creates a "Clarification Bottleneck" and increases the likelihood of procrastination. |
| **2.6** | **Atomic Action Engineering** | For actionable items, the capture and clarification process must ultimately produce "Atomic Actions"—the single, next physical, visible activity required. This includes identifying `@starter_task` items. | Ensures that all commitments are broken down into non-intimidating, momentum-building first steps, directly addressing the challenge of task initiation. |
| **2.7** | **Project & Reference Integration** | The system must be able to route non-actionable but valuable information to the correct long-term storage (Obsidian) and identify multi-step items as "Projects" to be planned within Obsidian. | Ensures that the PKM serves not just as a task manager but as a comprehensive knowledge and project planning hub. |
