---
project_id: { { title } }
horizon: H1
area:
goal:
status: active
created: { { date } }
todoist_project_id: 2260614191
todoist_project_name: Work
jira_epic:
---

# {{title}}

## Outcome (Definition of Done)

> Binary completion criteria - what does "done" look like?

**Done When:**

- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Context & Alignment

**Area:** [[Area Name]]
**Goal:** [[Goal Name]]
**Horizon:** H1 (Project)
**Jira Epic:** [EPIC-ID](https://fitfile.atlassian.net/browse/EPIC-ID)

## Next Actions

> Tasks tagged with #todoist sync to Todoist

### This Week (WIP - Max 3)

- [ ] Action item 1 #todoist @work @DeepWork p1 [due:: {{date:YYYY-MM-DD}}]
- [ ] Action item 2 #todoist @computer @Online p1 [due:: {{date:YYYY-MM-DD}}]

### Backlog (Ready)

- [ ] Future action 1 #todoist @work p2
- [ ] Future action 2 #todoist @computer p3

### Waiting For

- [ ] Waiting on X from Y #todoist @WaitingFor p3

### Support Tasks (Obsidian Only - No Sync)

- [ ] Research task
- [ ] Documentation task
- [ ] Reference gathering

## Project Planning

### Purpose

Why does this project matter?

### Vision

What does success look like in detail?

### Brainstorming

- Idea 1
- Idea 2
- Idea 3

### Resources Needed

- [ ] Resource 1
- [ ] Resource 2

## Project Notes

### Meeting Notes

### Decisions Made

### Reference Material

## Project Log

**{{date:YYYY-MM-DD}}:** Project created

---

## Dataview Queries

### Active Tasks

```dataview
TASK
FROM "{{title}}"
WHERE contains(text, "#todoist") AND !completed
SORT priority ASC, due ASC
```

### Completed Tasks

```dataview
TASK
FROM "{{title}}"
WHERE contains(text, "#todoist") AND completed
SORT completion DESC
LIMIT 10
```
