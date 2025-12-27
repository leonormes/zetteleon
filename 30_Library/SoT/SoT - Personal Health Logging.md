---
aliases: ["Migraine Logging", "Symptom Tracking"]
confidence: "5/5"
created: 2025-12-24T09:40:32Z
epistemic: "process"
last_reviewed: "2025-12-24"
modified: 2025-12-27T20:40:56+00:00
purpose: "To define a low-friction protocol for tracking health events (e.g., migraines) within the ProdOS ecosystem."
review_interval: "12 months"
see_also: ["[[MOC - ProdOS Lite]]", "[[SoT - Migraine Tracking Dashboard]]"]
source_of_truth: []
status: "stable"
tags: ["health", "prodos", "protocol", "tracking"]
title: SoT - Personal Health Logging
type: "SoT"
uid: 
updated: 
---

## 1. The Low-Friction Protocol (Lite)

To minimize executive function tax, use the **Single-Field Entry** method in your Daily Notes.

### A. The Setup

Add these fields to your `daily.md` template frontmatter:

```yaml
migraine: false
migraine_severity: 0 # 1-10
migraine_notes: ""
```

### B. The Action

When a migraine occurs:

1. Open your **Daily Note**.
2. Toggle `migraine: true`.
3. (Optional) Set a `severity` and add a short note in `migraine_notes`.

---

## 2. The Feedback Loop: The Dashboard

Data is useless without visibility. The **[[SoT - Migraine Tracking Dashboard]]** uses Dataview to aggregate these events into a chronological timeline and severity heat map.

---

## 3. Summary

Health tracking in ProdOS is a **Passive Collection, Active Review** system. By offloading the memory of the event to the daily note, you can identify triggers and patterns during your **Weekly Command Centre** review without needing to remember details mid-crisis.
