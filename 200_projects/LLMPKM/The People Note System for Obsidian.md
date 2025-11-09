---
aliases: []
confidence: 
created: 2025-10-24T11:38:40Z
epistemic: 
last_reviewed: 
modified: 2025-11-01T20:19:36Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: The People Note System for Obsidian
type:
uid: 
updated: 
version:
---

## Extract Key Takeaways

**Key Takeaways — The People Note System for Obsidian**

- **Purpose \& Problem Solved**
  - The People Note is designed to seamlessly roll up tasks, projects, and meeting notes tied to individuals, addressing the challenge of tracking collaborative work in personal knowledge management (PKM) systems.
  - Typical PKM setups struggle when it comes to collaboration—the People Note structure solves this.
- **Three Types of Collaborative Tracking**
  - *To Discuss*: Tasks/topics to raise in meetings.
  - *Waiting For*: Items that can't proceed until someone else acts.
  - *Assigned To*: Delegated tasks you need to monitor for success.
- **Obsidian Implementation**
  - Uses a templated note (People Note) with embedded queries pulling in:
    - Tasks to discuss with the person.
    - Items waiting on that person's action.
    - Tasks assigned to them but you're indirectly responsible for.
    - All meeting notes with them as attendee.
  - Tags (typically first names) are crucial for filtering content.
- **Workflow Components**
  - Obsidian plugins used: Tasks, QuickAdd, Templater, Callout Manager, Dataview.
  - Task queries filter actionable items by tags.
  - Meeting notes use Dataview queries and tag attendees for visibility.
- **Automated Creation**
  - QuickAdd macro + Templater plugin automate People Note creation.
    - Prompts for first name, last name, and tag (used to filter queries).
    - Files are kept organized in a dedicated folder.
    - All queries instantly update as notes/tasks are added/tagged.
- **Project Linkage**
  - Same principle applied for project notes: Each project gets a template, queries filter all related tasks/meetings using a project tag—everything is surfaced in one place.
- **Benefits**
  - Reduces things slipping through the cracks in group work.
  - Makes it easy to prep for meetings, track delegated work, and reference history.
  - Supports a calm, focused workflow (less urgency addiction, more deep work).
- **Resources \& Next Steps**
  - Free template available (Practical PKM Starter Vault).
  - Option for a full LifeHQ vault: prebuilt workflows, templates, plugins, and curriculum.

**Action Items:**

- Download the template vault for immediate setup.
- Configure QuickAdd and Templater macros for frictionless new People Note creation.
- Tag all tasks and meeting notes by individual/project for automatic rollup.

**Concrete Example:**

- Before a 1:1 with “John”, filter unfinished tasks tagged \#John \#discuss.
- After meetings, use Dataview query to list all notes with “John” as attendee, showing decisions/actions for reference.

This system is ideal for anyone seeking robust, scalable collaboration tracking in Obsidian—especially in environments where “handoffs,” “follow-ups,” and “delegated tasks” often get siloed or overlooked.
