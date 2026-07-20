---
created: 2026-05-30T12:56:50+00:00
modified: 2026-07-20T16:32:57+00:00
permalink: llmeon/raw/2026-05-30-pieces-ftfl638-cpu-saturation
pieces_ids: [14aa82dd-ea33-4b05-b981-95ad9aa151ea]
source: pieces-ltm
tags: [pieces, raw]
title: 2026-05-30-pieces-ftfl638-cpu-saturation
---

## Asset 1 (Pieces: 14aa82dd-ea33-4b05-b981-95ad9aa151ea)

- Root cause: `grafana.alloy-logs` couldn't land cleanly on the workflow setup because the target node pool was already effectively full on CPU requests. One node was reported at 99% request saturation (`3852m/3860m`, only 8m free), while Alloy was requesting 10m CPU, so Kubernetes returned `Warning FailedScheduling … 0/3 nodes are available: 1 Insufficient cpu, 2 node(s) didn't satisfy plugin(s) [NodeAffinity]`.
- Impact: `alloy-logs-f54v9` stayed Pending, so workflow/Argo pod logs weren't being collected reliably. The fix was only partially effective until the pod/template rollout caught up.
- Proposed fix: reduce `alloy-logs` CPU request from `10m` → `5m` in `ffnodes/fitfile/testing/values.yaml`, keep the workflow/spot tolerations, then redeploy and verify the DaemonSet reschedules. See [FTFL-638 adds workflow tolerations](https://gitlab.com/fitfile/deployment/-/merge_requests/783).
- Related issue: the same change set also removed `pod: null` from `structuredMetadata`, which pushed `pod` out of Loki stream labels; restoring that keeps pod-based querying working.
