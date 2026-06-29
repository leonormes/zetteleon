---
created: 2026-06-11 16:00:00+01:00
modified: 2026-06-11 16:00:00+01:00
title: Filter - Deployments Infrastructure Open
tags:
- operon
- filters
operon_filter_id: fs_deploy_infra_open
operon_filter_name: Deployments & Infrastructure — Open
permalink: llmeon/operon/filters/filter-deployments-infrastructure-open
---

## Logic

**All** of:

| Field | Operator | Value |
|-------|----------|-------|
| `checkbox` | is open | — |

**Any** of:

| Field | Operator | Value |
|-------|----------|-------|
| `prodosCategory` | is | `deployments` |
| `prodosCategory` | is | `refined_deployment` |
| `prodosCategory` | is | `infrastructure` |

## Sort

1. `prodosCategory` ascending
2. Priority ascending

## Embed

```operon
filter: Deployments & Infrastructure — Open
```