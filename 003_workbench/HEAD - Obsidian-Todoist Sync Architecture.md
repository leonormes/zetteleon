---
aliases: []
confidence:
created: 2025-12-08T00:00:00Z
epistemic:
last_reviewed:
modified: 2025-12-08T11:11:32Z
purpose:
review_interval:
see_also: []
source_of_truth: []
status: archived
tags:
  - architecture
  - head
  - prodos
  - thinking
title: HEAD - Obsidian-Todoist Sync Architecture
type: head
uid:
updated:
---

## HEAD - Obsidian-Todoist Sync Architecture

### The Spark

Derived from ProdOS Task: "Get prodOS to use todoist sync from obsidian".

The core "Runtime" of ProdOS is Todoist, but the "Context" is Obsidian. I need a robust sync between them.

### My Current Model
- **Obsidian:** Master of "Why" and "What" (Project Specs, Plans, Thinking).
- **Todoist:** Master of "When" and "Status" (Reminders, Checkboxes).
- **Sync:** Currently manual or fragile.
I want to manage tasks in Obsidian (during planning) and have them appear in Todoist.

### The Tension
- **Source of Truth:** If I change a task name in Todoist, should it update Obsidian? (Complexity).
- **Format Mismatch:** Obsidian is Markdown text; Todoist is structured data.
- **Fragility:** Bi-directional sync is prone to loops and conflicts.

### The Next Test
- [ ] Define the "Canonical Fields" map (e.g., Obsidian Task `- [ ] text` -> Todoist Content).
- [ ] Experiment with a "One-Way Push" (Obsidian -> Todoist) script for the initial plan.
- [ ] Evaluate if existing plugins (Todoist Sync) suffice or if I need a custom script for specific "Project" note handling.
