---
created: 2026-02-16T11:46:04+00:00
incident_type: sync_failure
modified: 2026-08-13T10:53:56+00:00
permalink: llmeon/30-library/ops/pb-argocd-sync-failure-triage
tags: [argocd, kubectl, playbook]
target_service: argocd
title: pb-argocd-sync-failure-triage
---

## Playbook: ArgoCD Sync Failure Triage (Kubectl-only)

### 🧭 Trigger Condition

- ArgoCD Application status is `OutOfSync` or `Unknown`.
- Alert: `failed to generate manifest… authentication required`.

---

### 🧱 Execution Flow

#### Phase 1: Initial Triage

1. List all applications to check scope of failure:
   ![[cmd-k8s-get-argocd-apps#⚡ Action]]

2. Describe the failing application:
   ![[cmd-k8s-describe-argocd-app#⚡ Action]]

#### Phase 2: Log Analysis

1. Check the controller logs for the specific app:
   ![[cmd-k8s-get-argocd-controller-logs#⚡ Action]]

#### Phase 3: Credential Repair (If Auth Error)

1. If credentials are managed by Vault, force a rotation:
   ![[cmd-k8s-annotate-vault-rotation#⚡ Action]]

2. Restart the repository server to clear cache

```bash
kubectl rollout restart deployment argocd-repo-server -n argocd
```

#### Phase 4: Reconciliation

1. Force a manual sync:
   ![[cmd-k8s-patch-argocd-app-sync#⚡ Action]]

---

### 🧠 End State

Success =

- App Synced
- Health Status: Healthy
