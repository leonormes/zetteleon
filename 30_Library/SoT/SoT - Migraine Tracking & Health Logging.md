---
aliases: ["Health Schema", "Migraine HUD", "ProdOS Symptom Tracking"]
confidence: "5/5"
created: 2025-12-30T16:15:00Z
epistemic: "authoritative"
last_reviewed: "2025-12-30"
modified: 2026-01-08T10:49:42+00:00
purpose: "A unified system for tracking health events (migraines) and visualizing trends using Dataview and Tracker."
review_interval: "3 months"
see_also: ["[[SoT - Metabolic Health & Satiety Management]]"]
source_of_truth: []
status: "stable"
tags: ["dashboard", "dataview", "health", "migraine", "tracking"]
title: SoT - Migraine Tracking & Health Logging
type: "SoT"
uid: 
updated: 
---

## SoT - Migraine Tracking & Health Logging

### 1. The Data Schema (Input)

To maintain tracking consistency, use these specific frontmatter fields in your **Daily Notes**.

```yaml
migraine: true/false
migraine_severity: 0-10 # (0 = None, 10 = Emergency)
migraine_notes: "Description of triggers/symptoms"
```

---

### 2. The Command Dashboard (View)

#### I. Recent History (Last 30 Days)

```dataview
TABLE
    migraine_severity AS "Severity",
    migraine_notes AS "Notes"
FROM "01_journals/Dailies"
WHERE migraine = true
SORT file.name DESC
LIMIT 30
```

#### II. Severity Heat Map

> [!info] Requirement
> Requires the **Obsidian Tracker** plugin.

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

### 3. The Review Protocol

During your **Weekly Command Centre**, analyze the dashboard for:

1. **Clustering:** Are migraines occurring after specific dietary choices (See [[SoT - Metabolic Health & Satiety Management]])?
2. **Intensity Trend:** Is the severity increasing over time?
3. **Frequency:** Is the "Events per Month" metric stable?

---

### 4. Minimum Viable Understanding (MVU)

1. **Passive Input:** Just toggle the boolean in your daily note.
2. **Zero Recall:** Don't try to remember how bad it was; let the severity field capture the "present truth."
3. **Actionable Data:** Use the notes field to identify environmental triggers (Light, Sleep, Stress).
