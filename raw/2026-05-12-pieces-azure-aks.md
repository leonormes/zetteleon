---
created: 2026-05-12 22:06:30+00:00
modified: 2026-05-26 11:43:45+00:00
pieces_ids:
- 23e03e0d-fccf-4ad1-85fd-5ee8ff14b8c4
source: pieces-ltm
tags:
- pieces
- raw
title: 2026-05-12-pieces-azure-aks
permalink: llmeon/raw/2026-05-12-pieces-azure-aks
---

## Pieces LTM Ingest—Azure AKS

Ingestion window: Last 24 hours (4-hour window returned 0 new assets; extended per skill instructions)

Summary: 1 assets captured for Azure AKS.

---

### Asset 1 (Pieces: 23e03e0d-fccf-4ad1-85fd-5ee8ff14b8c4)

Captured: 2026-05-12T08:36:45.233581Z

All three cursors are now drained (`recommendation: 'sufficient'`). The additional pages did not surface any new MRs or commits not already covered. However, the pagination did surface richer detail on the two outstanding issues—here is the supplementary information:

---

### Additional Detail from Exhaustive Drain

#### `kube-state-metrics` Timestamp collision—root Cause Confirmed

The additional pages surface the live Alloy log evidence directly:

> `level=warn msg="Error on ingesting samples with different value but same timestamp" component_id=prometheus.scrape.kube_state_metrics num_dropped=1`

This fires every 60 seconds without interruption on `alloy-metrics-0`. The root cause is confirmed: the Alloy discovery config uses `role = "endpoints"` for kube-state-metrics. If the kube-state-metrics Service exposes multiple ports (e.g. a metrics port and a telemetry port), Alloy scrapes the same target twice within the same 60-second window and receives conflicting values for the same timestamp—one sample is dropped.

How to investigate further (from your own notes in `considerate-zebra`):

```bash
kubectl --context fitfile-cloud-testing-aks-cluster \
  -n monitoring get endpoints grafana-k8s-monitoring-kube-state-metrics -o yaml
```

Look for multiple ports in the endpoint object. If present, switch the discovery `role` from `endpoints` to `pod` to avoid double-scraping. This fix was identified but no PR was raised—it remains an open item.

#### `fitfile-image-pull-secret`—event Count Confirmed, Scope Broader than `aks-system`

The drain confirms the event count at 179+ warnings across multiple namespaces including `thehyve`, `aks-system`, and ArgoCD pods. From your documented summary:

> "The secret does not exist anywhere in the cluster: `kubectl get secret fitfile-image-pull-secret -A` returns nothing. Pods are only running because images are node-cached. Any pod rescheduled to a node that hasn't cached the image will fail to start."

This was flagged as pre-existing and unrelated to FTFL-638, but a follow-up is needed. The fix path is ensuring the `SharedSecret` resource (or equivalent) that provisions `fitfile-image-pull-secret` is correctly rendering in the testing cluster—likely a Vault Secrets Operator issue, not a Grafana Alloy issue.

#### MR!758—confirmed Separately (7 May 2026)

The later pages also confirm MR!758 ("FTFL-638 Fix Alloy job label to use `namespace/container` format") was opened on 7 May 2026 and merged, with the fix plan documented in `GRAFANA_ALLOY_FIX_PLAN.md`. The `v3.7.5` chart's broken `job` relabel rule (producing `job="namespace"` instead of `job="namespace/container"`) was the residual issue after the main fix, and this MR addressed it via `extraRelabelingRules` in `ffnodes/fitfile/testing/values.yaml`.

---

No new MRs or commits were surfaced beyond those already summarised. The two open loops (`kube-state-metrics` double-scrape and `fitfile-image-pull-secret`) remain unresolved as of the evidence in memory, with no follow-up PRs found.

---