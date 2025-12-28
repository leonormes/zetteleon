---
aliases: ["ProdOS Cognitive Architecture", "The Thinking Machine"]
confidence: "5/5"
created: 2025-12-21T00:00:00Z
epistemic: "Synthesized from system design principles and notes on AI-human interaction."
last_reviewed: "2025-12-21"
modified: 2025-12-28T18:49:16+00:00
purpose: "To define the philosophical and architectural integration of the Gemini CLI (agentic reasoning) and Obsidian (structured knowledge) within the ProdOS framework."
review_interval: "3 months"
see_also: []
source_of_truth: []
status: "stable"
tags: ["ai", "architecture", "gemini-cli", "obsidian", "prodos", "topic/cognition"]
title: SoT - ProdOS Cognitive Architecture (Obsidian + Gemini)
type: "SoT"
uid: 
updated: 
---

## 1. Definitive Statement: "The Thinking Machine"

The ProdOS cognitive architecture integrates two distinct but complementary systems to create a "Thinking Machine": ""

1. **Obsidian (The Knowledge Base): "** Functions as the structured, long-term memory and \"wisdom\" layer. It stores canonical knowledge in the form of SoTs, MOCs, and a library of mental models. This is the source of ground truth and high-level principles."
2. **Gemini CLI (The Agentic Processor): "** Functions as the active, agentic reasoning layer. It is a powerful, transient processor that can ingest context, perform complex tasks, and execute commands, but it lacks inherent wisdom or long-term memory."

---

## 2. The Architectural Workflow

The integration is governed by a master prompt system that transforms the Gemini CLI from a generic tool into a specialized ProdOS operator.

### 2.1. The `gemini.md` Master Prompt

The `gemini.md` file in the root of a project is the primary bridge between Obsidian and the CLI. It serves as the system prompt that bootstraps the agent's behavior for that specific context.

- **Role Definition:** It instructs the agent on its role (e.g., "ProdOS Operator," "Chief of Staff"), its objectives (e.g., "minimize toil," "maximize action"), and its constraints.
- **Workflow Logic:** It defines the process the agent must follow, such as:
    1. **Diagnose:** Ask clarifying questions to understand the deep context of a problem.
    2. **Scan & Select:** Access the local Obsidian vault (via `@` file references or MCPs) to find and select the most relevant mental models or SoTs for the task.
    3. **Synthesize & Execute:** Apply the selected frameworks to perform a detailed analysis, execute code, or generate a structured report.

### 2.2. The Library of Mental Models

Obsidian contains the library of mental models (e.g., First Principles Thinking, Inversion, The 10% Rule). Each model is a markdown file with a clear description and step-by-step instructions. When prompted, Gemini can be instructed to load a specific model (`@path/to/model.md`) and apply its framework to the current problem, ensuring a structured and principled analysis rather than a generic statistical response.

---

## 3. The Roles of Each Component

| Component | Role | Function | Key Analogy |
|:--- |:--- |:--- |:--- |
| **Obsidian Vault** | **The Brain / Wisdom** | Long-term storage of structured knowledge, principles, and mental models. | The University Library |
| **Gemini CLI** | **The Agent / Reasoner**| Active, real-time task execution, synthesis, and interaction with the digital world. | The brilliant but inexperienced research assistant |
| **`gemini.md`** | **The Operating Manual** | A set of specific instructions that tells the assistant *how* to use the library to help you. | The Syllabus |

This separation of concerns allows ProdOS to function as a true cognitive augmentation system: Obsidian provides the durable, structured "thought," while Gemini provides the powerful, transient "thinking."
