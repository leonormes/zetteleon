---
created: 2026-06-11 16:00:00+01:00
modified: 2026-06-11 16:00:00+01:00
title: Filter - Overdue Open
tags:
- operon
- filters
operon_filter_id: fs_overdue_open
operon_filter_name: Overdue — Open
permalink: llmeon/operon/filters/filter-overdue-open
---

## Logic (all must match)

| Field | Operator | Value |
|-------|----------|-------|
| `checkbox` | is open | — |
| `dateDue` | before today (`beforeToday`) | — |
| `folder` | is in folder tree (`isInFolderTree`) | `Operon` |

## Sort

1. `dateDue` ascending
2. Priority ascending

## Embed

```operon
filter: Overdue — Open
```