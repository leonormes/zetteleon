---
aliases: []
confidence: 
created: 2025-10-19T13:16:15Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:24Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: 09 - Todoist for Task Execution
type:
uid: 
updated: 
version:
---

## Todoist for Task Execution: The Tactical Engine

Todoist serves as the tactical execution layer of the ProdOS system. It is the home for all **Next Actions** (the "Ground" level of the Horizons of Focus) and is optimized for quick capture, mobile access, and frictionless engagement with what needs to be done *right now*.

### Core Philosophy: Horizontal Execution & Mode-Based Work

While Obsidian provides the "vertical coherence" of project plans, Todoist provides "horizontal clarity" by organizing tasks based on the context and energy required to do them. This is crucial for a developer workload where nearly all tasks fall under a uselessly broad `@Computer` context.

The `@Computer` context is subdivided into **cognitive modes**:

- **`@DeepWork`:** For high-energy, cognitively demanding tasks requiring 60+ minutes of uninterrupted focus.
- **`@QuickWins`:** For low-energy, low-friction tasks that can be done in 15 minutes or less. This is for clearing the decks or making progress when focus is low.
- **`@Comms`:** For batching communication tasks like email and Slack.
- **`@Offline`:** For tasks that can be done without an internet connection (e.g., local coding, drafting documents).

### The Tagging System: The Agent's Language

A simple, consistent tagging system allows the LLM "Chief of Staff" to understand and manipulate tasks.

- **`#next_action`:** Applied by the agent to every task that is currently unblocked and at the head of an Action Sequence. This tag creates the pool of all possible work.
- **`#now_action`:** Applied by the agent to the *single* task it recommends you do right now.
- **Context Tags:** `@DeepWork`, `@QuickWins`, `@Calls`, `@Errands`, etc.
- **Energy/Time Tags:** `#low_energy`, `#15_mins`, etc.
- **`@starter_task`:** A special tag for tiny, momentum-building actions designed to overcome procrastination.
- **`@WaitingFor`:** For delegated tasks where you are awaiting an external input.
- **`@WIP` (Work-in-Progress):** A temporary tag or priority flag used to enforce a strict limit (e.g., ≤3) on the number of active `@DeepWork` tasks to ensure focus and completion.

### The Workflow: From Plan to Action

1. **Sync from Obsidian:** New Next Actions, defined during the clarification process in Obsidian, are synced to Todoist with their relevant project, context, and energy tags.
2. **`plan out next` Command:** The user runs a command that triggers the LLM agent to analyze all available `#next_action` tasks.
3. **Agent Reasoning:** The agent uses the ProdOS priority algorithm to select the single best `#now_action` based on current context (time, energy), deadlines, and strategic goals from Obsidian.
4. **Engage via Filters:** The user does not work from project lists in Todoist. Instead, they engage with dynamic, mode-based **Filters**.

#### Key Todoist Filters

These saved filters are the primary interface for daily work.

- **`🟢 Get Started`:**
  - **Query:** `@starter_task & today`
  - **Purpose:** Shows only the tiny, 5-minute tasks designed to break inertia. This is the go-to filter when feeling overwhelmed or resistant.
- **`🔥 Deep Work (Now)`:**
  - **Query:** `@DeepWork & p1` (if using priorities for WIP) or `@DeepWork & @WIP`
  - **Purpose:** Shows only the 1-3 committed deep work tasks, eliminating all other distractions.
- **`☕️ Quick Wins`:**
  - **Query:** `@QuickWins & (today | no date)`
  - **Purpose:** The list for "in-between" moments or low-energy periods.
- **`✈️ Offline Pack`:**
  - **Query:** `@Offline & (today | no date)`
  - **Purpose:** A pre-compiled list of tasks that can be done while traveling or without internet access.

By using Todoist as a dynamic, filter-based execution engine, you separate the act of *planning* from the act of *doing*, significantly reducing in-the-moment cognitive load and making it easier to engage with the right task at the right time.
