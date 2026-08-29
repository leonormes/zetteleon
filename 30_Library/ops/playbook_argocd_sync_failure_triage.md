---
created: 2026-02-21T15:05:08+00:00
last_verified: 2026-02-22
modified: 2026-08-29T09:36:49+00:00
permalink: llmeon/30-library/ops/playbook-argocd-sync-failure-triage
severity: p3
tags: [argocd, debug, drift, kubectl, playbook, sync]
target_service: argocd
title: playbook_argocd_sync_failure_triage
trigger: ArgoCD Application is OutOfSync, Degraded, or stuck on a SyncError
---

## Playbook: ArgoCD Sync Failure Triage

### ⚠️ Symptoms

> When to use this: Quick commands to refresh Argo CD Applications and identify precisely _why_ they are `OutOfSync`, `Degraded`, or stuck on failed sync attempts—using only `kubectl` (no `argocd` CLI required).

- Application sync status: `OutOfSync` or `Unknown`
- Application health status: `Degraded` or `Missing`
- Conditions explaining failures (e.g., `SyncError`, `ComparisonError`, `SharedResourceWarning`)

---

### 🧠 Mental Model

Argo evaluates an Application by:

1. Reading desired state (Git/Helm/Kustomize)
2. Comparing to live state in the cluster
3. Reporting the delta in `status` fields.

A "Refresh" tells Argo to re-run the comparison calculation _right now_. A "Sync" tells Argo to actively attempt applying the difference to the cluster.

---

### Phase 0: Context Establishment

1. List All Applications and their High-Level Status
   ![[cmd_kubectl_argocd_list_applications_table#1. The Command]]

2. Trigger an Immediate Hard Refresh
   _If Argo seems "stuck" or the manifest generation is severely cached, force an overwrite._
   ![[cmd_kubectl_argocd_annotate_hard_refresh#1. The Command]]

---

### Phase 1: Diagnosis

_Trace the exact reason the parent application is flagging errors by drilling down into specific resources or operation states._

1. Identify the Exact Failing/Drifting Child Resource
   _Print every tracked resource and its per-resource sync/health. This isolates the specific ConfigMap, Service, or Pod at fault._
   ![[cmd_kubectl_argocd_get_failing_resources#1. The Command]]

2. Check Overarching Application Error Conditions
   _Why did the Sync fail? Was it Admission Webhooks? Immutable Fields? Dependency Login?_
   ![[cmd_kubectl_argocd_get_failure_conditions#1. The Command]]

3. Check the Detailed Operation State Message
   _Specifically tracks the most recent `Failed Sync Attempt` output._
   ![[cmd_kubectl_argocd_get_app_operation_state#1. The Command]]

---

### Phase 2: Resolving App-of-Apps Edge Cases

_Parent apps can be `Degraded` even when workloads run perfectly, merely because a generated child application is `OutOfSync`._

1. List all Children of a Suspected Parent Application
   _Confirm if the application is an orchestration shell._
   ![[cmd_kubectl_argocd_get_child_applications#1. The Command]]

2. Trigger a Hard Refresh Across the Entire Bundle
   _Parent statuses rarely clear until their child applications have successfully re-compared. Blast refresh the entire node tree._
   ![[cmd_kubectl_argocd_bulk_refresh_children#1. The Command]]

---

### Phase 3: Drift Forensics & Resolution

_If you found an `OutOfSync` resource in Phase 1 but the workloads are currently running without issue, it's typically one of three root causes:_

#### Scenario A: The Hashed ConfigMap Drift

_When Helm hashes ConfigMap data and suffixes the name, sometimes the old name lingers in the tracking list while workloads use the new one._

1. Check if the Deploy Still References the Old ConfigMap
   ![[cmd_kubectl_argocd_grep_drifting_configmap#1. The Command]]
   _If silent, the ConfigMap is orphaned. Delete it directly from the cluster, then Hard Refresh the Application._

#### Scenario B: Operator-Managed Resource Mutation

_Argo natively expects 100% adherence to Git. If another tool (e.g., Cert-Manager or VSO) injects its own labels/status fields, Argo detects drift._

1. Grep the Specific Drifting Resource Metadata
   ![[cmd_kubectl_argocd_grep_operator_drift#1. The Command]]
   _If external annotations are present, you must either configure `ignoreDifferences` in the Application spec, or mirror the operator's expected labels back into Git._

#### Scenario C: Server-Side Re-evaluation

_If you manually mutated a Secret or ConfigMap out-of-band and need to prove the system accepts the change before triggering an Argo Sync:_

1. Force a Rollout Restart

   ```bash
   kubectl rollout restart deployment -n <NAMESPACE> <DEPLOYMENT_NAME>
   ```

---

### Final Verification Checklist

- [ ] All child applications (if using app-of-apps) report `Synced` and `Healthy`
- [ ] Orphaned tracking hashes deleted from live state
- [ ] No immutable field sync rejections present in conditions
- [ ] `lastOperation` reflects a successful, green sync.
