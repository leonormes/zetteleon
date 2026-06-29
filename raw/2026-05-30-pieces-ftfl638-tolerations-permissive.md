---
title: FTFL-638 — alloy-logs tolerations are permissive (not restrictive)
created: 2026-05-30 00:08:42.438724+00:00
source: pieces-ltm
pieces_ids:
- fd75ff76-e61c-4d32-a5b1-f53c8679c090
tags:
- raw
- pieces
permalink: llmeon/raw/2026-05-30-pieces-ftfl638-tolerations-permissive
---

## Asset 1 (Pieces: fd75ff76-e61c-4d32-a5b1-f53c8679c090)

*Captured: 2026-05-29T15:42:42.284747Z*

Yes, absolutely. **Tolerations are permissive, not restrictive.**

A toleration says *"this pod is allowed to schedule on nodes with this taint"* — it does not say *"this pod must only go to nodes with this taint."*

The two system nodes (`aks-system-*`) have **no taints at all**, so alloy-logs already schedules there freely. Adding tolerations for the workflow node taints has zero effect on that — the system node pods are unaffected.

The result after the change:

| Node | Taints | alloy-logs scheduled? |
|---|---|---|
| `aks-system-26060640-vmss0000tp` | none | ✅ yes (same as now) |
| `aks-system-26060640-vmss0000tq` | none | ✅ yes (same as now) |
| `aks-workflows-32842669-vmss*` | `dedicated=workflows:NoSchedule` + `spot:NoSchedule` | ✅ yes (newly unblocked) |

If you wanted to *restrict* alloy-logs to only certain nodes you'd need a `nodeSelector` or `nodeAffinity` — tolerations alone never do that.