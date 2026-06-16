---
created: 2026-06-11T16:00:00+01:00
modified: 2026-06-11T16:00:00+01:00
title: Filter - ProdOS Active Open Work
tags: [operon, filters]
operon_filter_id: fs_prodos_active
operon_filter_name: ProdOS — Active Open Work
---

## Logic (all must match)

| Field | Operator | Value |
|-------|----------|-------|
| `checkbox` | is open | — |
| `folder` | is in folder tree (`isInFolderTree`) | `Operon` |
| `status` | not contains | `Finished` |
| `status` | not contains | `Dropped` |
| `status` | not contains | `Wont` |

## Sort

1. Priority ascending
2. Checkbox ascending

## Embed

```operon
filter: ProdOS — Active Open Work
```
