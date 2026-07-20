---
created: 2026-07-17T13:20:18+00:00
date: 2026-07-17
modified: 2026-07-20T16:33:32+00:00
permalink: llmeon/work/distributed-workflow-inspector-review-clone-and-enhancement-attempt
project: Sandbox Stress-Test Dashboards & Observability
related_note: kube_pod_labels Metrics Plan — Sandbox Stress-Test Observability.md
tags: [argo-workflows, fitfile, grafana, observability, sandbox-testing]
title: Distributed Workflow Inspector — Review, Clone, and Enhancement Attempt
todoist_parent_task: https://app.todoist.com/app/task/6h6FcvqcW7gGW6wm
---

## Distributed Workflow Inspector—Review, Clone, and Enhancement Attempt

Ollie (workflows-api team) independently built the exact drill-down dashboard our earlier plan was working toward, before that plan was finished. This note covers the review, what it revealed about the actual join-key mechanism in use, the clone built on top of it, and an enhancement attempt that had to be reverted.

### The Original: Ollie's Dashboard

[Distributed Workflow Inspector](https://fitfiletest.grafana.net/d/olj9v2f/distributed-workflow-inspector)—UID `olj9v2f`, sitting in General (no folder), created `2026-07-17T09:03`. Not edited—reviewed only, via `gcx dashboards get olj9v2f -o json`.

16 panels across 8 rows: Instance ID Picker → Workflow Overview → DAG Nodes → Argo Workflow Pod Timeline → Pod Resource Usage → Kubernetes Events → Node Scaling → PostgreSQL.

### The Big Discovery: a Different Join-key Mechanism than Planned

Our [earlier plan](kube_pod_labels%20Metrics%20Plan%20—%20Sandbox%20Stress-Test%20Observability.md) assumed the only way to join FFCloud's instance UUID to Argo Workflow pods was a Kubernetes pod label (`ffcloud.io/instance-id`) plus the `kube_pod_labels` metric fix. Ollie's dashboard proves workflows-api solved this differently—with two purpose-built bridge metrics, confirmed live via `gcx metrics query`:

```
argo_workflow_by_fitfile_workflow{cluster, fitfile_workflow_id, argo_workflow_id, argo_workflow_name}
argo_workflow_by_pod{cluster, workflow_name, pod_name}
```

Sample data (`sandbox-testing-2`):

```
argo_workflow_by_fitfile_workflow{argo_workflow_id="28d6613a-905f-47d4-bb8c-b588e29f04c5",
  argo_workflow_name="100k-patients-single-source-privacy-on-1-workflow-7zr7b",
  fitfile_workflow_id="e6e3c571-290e-4f94-871d-45895954b3c3"}

argo_workflow_by_pod{workflow_name="100k-patients-single-source-privacy-on-1-workflow-7zr7b",
  pod_name="100k-patients-single-source-privacy-on-1-workflow-7zr7b-ohdsi-query-combiner-741408509"}
```

Chained as hidden dashboard variables (`$instance_id → $argo_workflow → $pods_in_workflow`), the resolved pod names filter standard, already-flowing metrics directly—`container_cpu_usage_seconds_total`, `kube_pod_container_resource_requests/limits`, `container_memory_working_set_bytes`—via plain `pod=~"$pods_in_workflow"`. No pod label, no `kube_pod_labels` dependency at all for this dashboard's purposes.

Grepped this deployment repo for both metric names—zero matches. They're emitted entirely at the application level (workflows-api, presumably watching Workflow objects via the Kubernetes API—it already has the RBAC for it), outside our Helm charts.

There's a matching log-side mechanism too: a new Loki event type, `WorkflowInstanceNodeStarted`/`WorkflowInstanceNodeCompleted`, carrying `workflow_receipt_name`/`workflow_receipt_uid`—the real Argo Workflow name/uid—per DAG node.

Consequence: the `kube_pod_labels` fix (MR 890, verified working in the [prior note](kube_pod_labels%20Metrics%20Plan%20—%20Sandbox%20Stress-Test%20Observability.md)) is no longer on the critical path for this dashboard. Still a legitimate general KSM improvement (e.g. for future OpenCost per-workflow cost allocation), just not blocking anymore. The workflows-api pod-label task is deprioritized, not deleted.

### The Clone

[Distributed Workflow Inspector (v2 - auto time range)](https://fitfiletest.grafana.net/d/ff-dwi-v2/distributed-workflow-inspector-v2)—UID `ff-dwi-v2`, placed in the Stress Testing folder (`dfs2pe0fy5ptse`) this time, unlike the original. Built via `gcx dashboards create` from a full copy of Ollie's JSON.

Changes from the original:

1. PostgreSQL row removed (3 panels: CPU/Memory, Database Size, Locks/Connections)—dedicated DB dashboards already cover this better, per request.
2. Auto time-range-scoping enhancement—attempted, then reverted. See below.

### The Enhancement Attempt and why it Was Reverted

The picker panel ("Select a Workflow to Inspect") already had a working click-to-load link on the Instance ID column (missed this on first read—it's a field-level `fieldConfig.overrides[].properties[].value[].links` entry, not a panel-level `links` array, easy to miss in a `2603`-line JSON dump). But the link only passed through `from=${__from}&to=${__to}`—the _currently viewed_ range, not the workflow's actual start/end. That gap matched what the original plan flagged (workflow durations range from minutes to ~4.5 hours, so a fixed/carried-over window is the wrong default).

Redesigned the picker query to extract real `StartTime`/`EndTime` per instance via explicit LogQL field renaming—verified working standalone via `gcx logs query` before touching the dashboard:

```logql
{cluster="$cluster", event="WorkflowInstanceStarted"} | json StartTime="time", instanceId="payload.instanceId", workflowName="payload.workflowName"
{cluster="$cluster", event=~"WorkflowInstanceCompleted|WorkflowInstanceFailed"} | json EndTime="time", instanceId="payload.instanceId", durationMs="payload.duration", status="event"
```

Joined via a `joinByField` transform on `instanceId`, with the data link updated to `from=${__data.fields.StartTime}&to=${__data.fields.EndTime}`.

Applied, but the panel showed "No data." Two rounds of Query Inspector debugging (via the user, since I couldn't get past Grafana's SSO to check visually myself) revealed the real cause: the actual `to` value Grafana sent to the datasource was frozen at an exact day-aligned absolute timestamp (`1783728000000` ms = precisely `2026-07-11T00:00:00.000Z`, evenly divisible by 86400) instead of tracking live "now"—while `from` correctly tracked `now-7d` and moved forward between the two checks. Confirmed via `gcx logs query` against the exact frozen window that zero events existed there (so "No data" was a _correct_ result for that wrong window, not a query bug)—real data existed in a normal recent window.

This from/to split-freeze behavior—one boundary live, the other stuck at a rounded absolute value, specific to this one multi-query+transform table panel while every other panel on the same dashboard refreshed correctly—is a genuine Grafana anomaly (possibly specific to the newer `dashboard.grafana.app/v2` "scenes" schema with multiple queries + a `joinByField` transform in a table panel) that couldn't be diagnosed further without live browser/network debugging access. Reverted panel-21 to Ollie's exact original query, viz config, and link (verified via diff against the original JSON) rather than ship something broken.

Net result: `ff-dwi-v2` is functionally identical to Ollie's original minus the PostgreSQL row. The auto-time-range enhancement remains a real, valid gap—worth revisiting interactively (user driving the Grafana UI, live) rather than blind iteration through the API.

### Remaining Open Work

- [Add data-link from "Workflow Instance Events" (aqr7ks) to the Distributed Workflow Inspector](https://app.todoist.com/app/task/6h6Ff33jjg37PWQF)—still nobody's done this; `aqr7ks` was last updated 2026-07-15, before Ollie's dashboard existed.
- Auto-time-range-scoping on the picker panel—reverted, not solved. Revisit live/interactively if picked back up.
- [kube_pod_labels fix](kube_pod_labels%20Metrics%20Plan%20—%20Sandbox%20Stress-Test%20Observability.md) remains valid as a general improvement, no longer urgent.

### References

- Todoist parent: [Build Argo Workflow instance drill-down dashboard](https://app.todoist.com/app/task/6h6FcvqcW7gGW6wm)
- Ollie's original (untouched): `olj9v2f`
- Clone: `ff-dwi-v2`, Stress Testing folder
- Bridge metrics: `argo_workflow_by_fitfile_workflow`, `argo_workflow_by_pod` (source unknown—not in this repo)
