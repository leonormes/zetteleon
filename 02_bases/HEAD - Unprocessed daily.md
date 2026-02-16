---
created: 2025-12-04T12:02:41Z
last_reviewed:
modified: 2026-02-16T09:40:49+00:00
status: processing
tags: [state/thinking]
title: HEAD - Unprocessed daily
type: map
updated:
---

```dataview
TABLE item.text AS "Unprocessed Noise"
FROM "01_journals/Dailies"
FLATTEN file.lists AS item
WHERE file.day < date(today) AND !item.task
SORT file.day desc

```
