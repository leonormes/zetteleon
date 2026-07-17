---
title: pieces_copilot_message_export_july_17_2026_9_56am
type: note
permalink: llmeon/00-inbox/pieces-copilot-message-export-july-17-2026-9-56am
---

*Shared Message from Pieces (https://pieces.app) by Leon Ormes (leonormes@gmail.com) on Friday Jul 17, 2026 - 9:56 AM*
---
## Cardinality risks for workflow-level UID labels

Your own audit history gives a clear, evidence-backed answer here — and it's a direct warning against exactly the design pattern in the drill-down plan (a `$workflow_uid` dashboard variable).

### The core risk: UID/pod-identity labels are your documented #1 cardinality driver

Three separate audits on the `fitfiletest` stack all converge on the same finding — labels that embed a unique-per-run identifier (pod UID, container hash, workflow run ID) are the dominant cause of series/stream explosion:

- The **`2026-06-04-k8s-cluster-audit-testing`** report flags `uid` (pod UUID) as a **CRITICAL** issue: *"Drop label `uid` on kube-state-metrics → eliminates 95 pod UUID values across 940 series"*, alongside `name` and `id` on cAdvisor metrics (*"the `name` label contains the full 64-character SHA256 container ID (206 distinct values)... high-entropy and duplicates the information in the container label"*).
- The **`2026-06-05-fitfile-loki-prometheus-cardinality-audit`** (the formal Loki & Prometheus audit you ran via `gcx`) documents the same class of finding for log streams — labels with unbounded value sets get flagged for immediate removal.
- A live incident confirms the mechanism at cost scale: your **July 1 DPM spike investigation** (`zippy-platypus` session) found *"The #1 offender: `kube_pod_status_reason` with the `vid` label — 18,352 series in staging alone. Each pod generates 8+ entries because the metric splits by pod UID + reason. That's ~$50-100/month just from one metric."* The fix was a one-line `labeldrop` rule in `charts/ffnode/templates/_grafana.tpl`, which cut that metric's cardinality entirely with no functional loss.

The billing dashboard at [fitfiletest.grafana.net/a/grafana-cmab-app/attributions](https://fitfiletest.grafana.net/dashboards/f/integration---alloy-health/integration-alloy-health) (checked 2026-06-23) shows `uid` still sitting at **6.60% of total label value pairs** and `container_id` at **10.40%** — these are your two highest-cardinality labels stack-wide, out of 131 unique labels.

### Specifically for Argo Workflow UIDs (the drill-down use case)

Your Perplexity research session on **"Labeling Argo Workflow Containers for Loki"** (2026-07-15) addresses this exact scenario directly:

> "Loki indexes on label values, so keep the promoted label to a small, bounded set of values (e.g., extract, transform, load — not one value per run/UID). If you also want per-run identifiers (workflow name, run ID) queryable but don't want them exploding your stream count, put those in Loki's structured metadata instead of indexed labels."

This is the precise architectural conflict for the drill-down dashboard: you need a workflow UID/name to join logs and metrics for one run, but promoting it to an **indexed Loki stream label** creates one new log stream per workflow execution — an unbounded, ever-growing cardinality dimension, exactly like the `uid`/`vid`/`container_id` problems already fixed elsewhere. Every new workflow run mints a brand-new label value that never gets reused, and old streams don't get cleaned up automatically.

### The established mitigation pattern (already in use on your stack)

Your team has a standing two-tier rule, documented in the **`Labels vs Structured Metadata in Kubernetes`** note (2026-06-04) and the FITFILE Sprint 21 board note: *"do not use this method to attach highly unique metadata like `git_commit_sha`, `user_id`, or `request_id` as Kubernetes labels. High cardinality will bloat your Loki index and degrade query performance."* The recommended pattern, already piloted (`Structured Metadata Enrichment Pilot`, `ff-test-a` cluster, June 8):

- **Indexed labels**: keep to bounded/low-cardinality dimensions (namespace, cluster, workflow *template name* if that's a small fixed set — NOT the per-run UID).
- **Structured metadata** (non-indexed, queryable via `| workflow_uid="..."` filters): put the actual workflow UID/run name here. This is exactly the mechanism your `structuredMetadataPilot` toggle in `charts/ffnode/values.yaml` already implements for other high-entropy fields (`pod`, `container`, `service_name`).
- On the **Prometheus** side, the corresponding pattern (per the `674...4bd Grafana k8s-monitoring: Labels and Structured Metadata` doc) is to avoid per-workflow-run labels on metrics series entirely — Prometheus has no structured-metadata equivalent, so a `workflow_uid` label there would inflate active series count directly and hit Grafana Cloud DPM billing (as the `vid` incident already demonstrated at ~$50-100/month for one metric).

### Practical implication for the drill-down dashboard plan

This directly changes the design recommendation I gave earlier: the `$workflow_uid` dashboard variable should be populated by **querying Loki structured metadata** (e.g. `| workflow_uid="..."`), not by treating `workflow_uid` as an indexed stream label. For the Prometheus side, confirm with `gcx metrics labels` whether Argo Workflow controller metrics expose workflow name/UID as a label at all — if they do, that's a candidate for the same cardinality review your June 4 audit already ran on `kube_pod_status_reason`, since a live stress-testing harness could generate hundreds of short-lived workflow runs per day, each minting new series.

One more relevant cross-check worth doing before implementation: query `gcx metrics query 'count by (workflow_uid) ({namespace="argo"})'` (mirroring the exact `topk` cardinality-check pattern your team used on `k8s_pod_uid` on 2026-06-04) to get real numbers before deciding label vs. structured-metadata placement.