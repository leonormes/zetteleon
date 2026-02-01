---
aliases: [Dashboard]
created: 2025-12-24T12:00:00Z
last_reviewed:
modified: 2026-02-01T15:08:08+00:00
status:
tags: [dashboard]
title: Life OS Dashboard
type: dashboard
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
> Use the Log Habit/Metric QuickAdd command to update your stats on the fly!

### 🎬 Media & Leisure

- [[Sci-Fi Watchlist (Screen)]]
- [[Sci-Fi Watchlist (Books)]]
- [[Music Watchlist (Listening)]]
- [[LIST - Master Sci-Fi Rankings]] (Reference)
