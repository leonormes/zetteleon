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
status: defined
tags: [head, maintenance, prodos, thinking]
title: HEAD - ProdOS Process Tracking
type: 
uid: 
updated: 
---

## HEAD - ProdOS Process Tracking

### The Spark

Derived from ProdOS Task: "Get prodOS to track the ongoing processes like patching".

I have recurring maintenance duties (patching, reviews, backups) that aren't "projects" with a clear end date, but they require tracking and visibility.

### My Current Model

ProdOS is currently optimized for "Projects" (finite goals) and "Tasks" (atomic actions).

I suspect I am missing a "Process" or "Loop" primitive. These are infinite games—things that must be maintained, not completed.

Currently, these just clutter my Todoist or get forgotten until they become emergencies.

### The Tension
- **Clutter vs. Visibility:** If I put every maintenance step in Todoist, I drown in recurring tasks. If I don't, I drop balls.
- **Structure:** How do I represent a "Process" in Obsidian? Is it a Note? A Dashboard?
- **Integration:** How does a static "Process Note" generate the necessary "Action Triggers" in Todoist without manual intervention?

### The Next Test
- [ ] Define a prototype "Process" template in `templates/`.
- [ ] Create one test Process note for "Server Patching".
- [ ] Determine how to link this to a recurring Todoist task (e.g., URL link in Todoist description back to the Process note).
