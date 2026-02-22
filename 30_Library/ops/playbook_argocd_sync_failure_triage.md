---
type: playbook
target_service: argocd
incident_type: sync_failure
status: verified
severity: p2
tags: [playbook, argocd, incident]
created: 2026-02-21T15:05:08+00:00
modified: 2026-02-21T15:09:04+00:00
---

# Playbook: ArgoCD Sync Failure Triage

## Mental Model
This playbook assumes a "GitOps First" approach. We distinguish between **Sync Errors** (ArgoCD can't apply the manifest) and **Health Errors** (Manifest applied, but the app is crashing).

---

## Phase 0: Preconditions / Safety
1. Verify you are in the correct cluster context:
```sh
kubectl config current-context
```
1. Confirm ArgoCD CLI connectivity:
```sh
argocd account get-capabilities
```

---

## Phase 1: Orient
Establish the baseline state.
1. Check overall status:
   ![[cmd_argocd_get_app]]
2. Inspect the delta between Git and Cluster:
   ![[cmd_argocd_diff_app]]

---

## Phase 2: Diagnosis
Identify the bottleneck.
1. Check individual resource health:
   ![[cmd_argocd_get_resources]]
2. Surface cluster-level errors:
   ![[cmd_kubectl_get_events]]
3. Review detailed failure context:
   ![[kb_argocd_sync_failure_causes]]

---

## Phase 3: Remediation
Unblock the deployment.
1. **Option A**: If the cache is stale:
   ![[cmd_argocd_refresh_app]]
2. **Option B**: Force a manual sync:
   ![[cmd_argocd_sync_app]]

---

## Phase 4: Verification
Confirm the resolution.
1. Verify pod stability:
   ![[cmd_kubectl_get_pods]]
2. Check final sync state:
   ![[cmd_argocd_get_app]]

---

## Rollback
If remediation makes things worse:
1. Revert to last known good state:
   ![[cmd_argocd_rollback_app]]
