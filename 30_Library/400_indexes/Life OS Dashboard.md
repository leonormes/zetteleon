---
aliases: [Dashboard]
confidence:
created: 2025-12-24T12:00:00Z
epistemic:
last_reviewed:
modified: 2025-12-28T18:49:18+00:00
purpose: Centralized Life OS Dashboard
review_interval:
see_also: []
source_of_truth: []
status:
tags: [dashboard]
title: Life OS Dashboard
type: dashboard
uid:
updated:
---

## 🌀 Fractal Life OS Dashboard

### 📅 Today's Progress

```dataview
LIST FROM "01_journals/Dailies"
WHERE file.day = date(today)
```

### 📈 Weekly Trends

```dataview
TABLE
  mood as Mood,
  focus as Focus,
  habit_meds as Meds,
  habit_water as Water
FROM "01_journals/Dailies"
WHERE file.day >= date(today) - dur(7 days)
SORT file.day DESC
```

### 🏗️ Monthly Review Status

```dataview
LIST FROM "01_journals/Monthlies"
SORT file.day DESC
LIMIT 5
```

### 🚀 Projects

```dataview
LIST FROM "30_Library/200_projects"
WHERE status = "active"
```

---

> [!info] Tip
> Use the **Log Habit/Metric** QuickAdd command to update your stats on the fly!
