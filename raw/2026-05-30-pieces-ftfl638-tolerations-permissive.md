---
created: Invalid date
modified: 2026-07-20T16:32:57+00:00
permalink: llmeon/raw/2026-05-30-pieces-ftfl638-tolerations-permissive
pieces_ids: [fd75ff76-e61c-4d32-a5b1-f53c8679c090]
source: pieces-ltm
tags: [pieces, raw]
title: 2026-05-30-pieces-ftfl638-tolerations-permissive
---

## Asset 1 (Pieces: fd75ff76-e61c-4d32-a5b1-f53c8679c090)

_Captured: 2026-05-29T15:42:42.284747Z_

Yes, absolutely. Tolerations are permissive, not restrictive.

A toleration says _"this pod is allowed to schedule on nodes with this taint"_—it does not say _"this pod must only go to nodes with this taint."_

The two system nodes (`aks-system-*`) have no taints at all, so alloy-logs already schedules there freely. Adding tolerations for the workflow node taints has zero effect on that—the system node pods are unaffected.

The result after the change:

| Node | Taints | alloy-logs scheduled? |
|---|---|---|
| `aks-system-26060640-vmss0000tp` | none | ✅ yes (same as now) |
| `aks-system-26060640-vmss0000tq` | none | ✅ yes (same as now) |
| `aks-workflows-32842669-vmss*` | `dedicated=workflows:NoSchedule` + `spot:NoSchedule` | ✅ yes (newly unblocked) |

If you wanted to _restrict_ alloy-logs to only certain nodes you'd need a `nodeSelector` or `nodeAffinity`—tolerations alone never do that.
