---
aliases: []
created: 2026-01-01T19:03:57+00:00
last_reviewed: ""
modified: 2026-02-01T15:08:05+00:00
status: ""
tags: [type/moc]
title: MOC - Learning Registry
type: map
---

## 🧠 Learning Registry

> [!tip] Prime Directive
> Single Threaded Processing. You cannot start a new quest until the current Boss Fight is won or the quest is formally abandoned.

### ⚔️ Active Quest (Limit: 1)

```dataview
TABLE WITHOUT ID 
file.link as "Current Mission",
boss_fight as "Final Boss",
progress as "Completion %"
FROM "30_Library/200_projects/50_Learning"
WHERE status = "active"
```

### 📜 Quest Board (Backlog)

_Priority ordered. Do not hoard cursors here._

```dataview
TABLE WITHOUT ID
file.link as "Project",
goal as "Goal",
priority as "Priority"
FROM "30_Library/200_projects/50_Learning"
WHERE status = "queued"
SORT priority desc
```

### 🏆 Hall of Heroes (Completed)

```dataview
TABLE WITHOUT ID
file.link as "Mastery",
completed_date as "Date Defeated"
FROM "30_Library/200_projects/50_Learning"
WHERE status = "finished"
SORT completed_date desc
```

---

#### ⚙️ Engine Rules

1. The Slot Rule: There is only one "Active" slot. To move a card from `queued` to `active`, you must first move the current `active` project to `finished` or `paused`.
2. The Boss Rule: No project enters `active` without a defined Boss Fight (a concrete deliverable).
