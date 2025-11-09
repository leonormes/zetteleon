---
aliases: []
confidence: 
created: 2025-10-19T13:15:59Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:24Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: 08 - Obsidian for PKM
type:
uid: 
updated: 
version:
---

## Obsidian for PKM: The Strategic Hub

Obsidian serves as the strategic hub and "thinking vault" within the ProdOS system. It is the home for **Personal Knowledge Management (PKM)**, where ideas are developed, connections are made, and long-term project planning occurs. It is optimized for thinking and reflection, contrasting with Todoist's role as a tactical execution engine.

### Core Philosophy: "Capture Now, Structure Later"

The system is designed to be ADHD-friendly by minimizing friction at the point of capture.

- **Messy Capture:** All initial thoughts, ideas, and meeting notes are dumped into a single location (e.g., a Daily Note or an `/Inbox` folder) without the immediate need for organization. This respects the brain's natural, non-linear thinking process.
- **Progressive Formalization:** Ideas are structured and refined later, during dedicated, low-friction "triage" or "clarify" sessions. An idea evolves from a fleeting thought into a permanent, well-linked "evergreen" note over time.

### System Architecture in Obsidian

A simple, clear folder structure provides the necessary scaffolding:

- `/Inbox`: The default location for all new, unstructured captures.
- `/Projects`: Contains one note per active project, detailing the plan, outcome, and support material.
- `/Sources`: Literature notes summarizing books, articles, or other external content.
- `/Notes` or `/Zettels`: The home for permanent, atomic notes—single, self-contained ideas.
- `/MOCs` (Maps of Content): Thematic hub notes that link together multiple atomic notes to provide an overview of a topic.
- `/Templates`: Contains pre-formatted templates for different note types (Daily Note, Project Plan, etc.) to ensure consistency.

### The Note Lifecycle: From Seedling to Evergreen

To make the Zettelkasten method more forgiving and visual, notes are given a status to indicate their level of development.

1. **Fleeting Note / Daily Note Capture:** An idea is first captured in its raw form.
2. **`#status/seedling` 🌱:** The idea is given its own note but remains a simple, undeveloped thought. It may have one or two tentative links.
3. **`#status/budding` 🌿:** The idea is being actively developed. You have added your own thoughts, connected it to other notes, and started to refine the core concept.
4. **`#status/evergreen` 🌳:** The note represents a well-developed, core concept in your own words. It is densely linked and serves as a stable foundation in your knowledge base.

### Key Plugins for an ADHD-Friendly Vault

- **Daily Notes / Periodic Notes:** The cornerstone of the capture workflow.
- **Templater / QuickAdd:** Automates the creation of new notes from pre-defined templates, reducing setup friction.
- **Dataview:** Your system's superpower. It allows you to create dynamic dashboards that automatically query and display lists of notes based on tags or folders (e.g., "Show all notes in `/Inbox`," or "List all notes with `#status/seedling`").
- **Todoist Sync Plugin:** The bridge to your execution system, allowing you to embed live task lists within project notes and maintain vertical coherence.
- **Calendar:** Provides visual navigation for your daily notes.

### Obsidian's Role in the GTD Workflow

- **Project Planning (Horizon 1):** Every multi-step outcome is planned in a dedicated Obsidian project note using the Natural Planning Model. This note contains the "Why" (Purpose), the "What" (Vision), and the "How" (Brainstorm & Plan).
- **Project Support Material:** All reference files, meeting notes, and related ideas are linked within the project note, creating a single source of truth for that outcome.
- **Review & Reflection:** The Weekly Review is conducted from a central "Review Hub" dashboard in Obsidian. This dashboard uses Dataview to pull in all relevant information: stale projects, overdue tasks from Todoist, and items on the `@WaitingFor` list.

Obsidian is where you think, plan, and connect ideas. It holds the "why" and "what" of your work, providing the strategic context for the "how" that is executed in Todoist.
