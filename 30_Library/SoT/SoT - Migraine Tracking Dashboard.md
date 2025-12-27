---
aliases: ["Migraine HUD"]
confidence: "5/5"
created: 2025-12-24T09:40:41Z
epistemic: "synthesis"
last_reviewed: "2025-12-24"
modified: 2025-12-27T20:40:57+00:00
purpose: "A central HUD for visualizing migraine frequency, severity, and notes over time."
review_interval: "1 month"
see_also: ["[[SoT - Personal Health Logging]]"]
source_of_truth: []
status: "stable"
tags: ["dashboard", "dataview", "health", "tracking"]
title: SoT - Migraine Tracking Dashboard
type: "SoT"
uid: 
updated: 
---

## Migraine Tracking HUD

> [!abstract] Overview
> This dashboard aggregates all migraine events recorded in your Daily Notes.

---

### 1. Migraine History (Last 90 Days)

```dataview
TABLE
    migraine_severity AS "Severity",
    migraine_notes AS "Notes"
FROM "01_journals/Dailies"
WHERE migraine = true OR contains(tags, "migraine")
SORT file.name DESC
LIMIT 30
```

---

### 2. Monthly Frequency

```dataview
TABLE 
    length(rows) AS "Events"
FROM "01_journals/Dailies"
WHERE migraine = true OR contains(tags, "migraine")
GROUP BY dateformat(file.day, "yyyy-MM") AS "Month"
SORT Month DESC
```

---

### 3. Visualization (Requires "Tracker" Plugin)

> [!info] Plugin Required
> Ensure you have the **Obsidian Tracker** plugin (by pyrochlore) installed and enabled.

```tracker
searchType: frontmatter
searchTarget: migraine_severity
folder: 01_journals/Dailies
datasetName: Migraine
line:
    title: Migraine Severity Trend
    yAxisLabel: Severity
    lineColor: "#ff0000"
    showLegend: true
```

---

### 4. Troubleshooting

If the chart is empty:

1. Ensure the plugin name is exactly **Obsidian Tracker**.
2. Check that your Daily Notes are in the folder `01_journals/Dailies`.
3. Check that the frontmatter in your daily note has `migraine_severity: 4` (number, not text).
