---
created: 2026-02-22T17:01:31+00:00
hop_level: local
last_verified: 2026-02-22
modified: 2026-08-13T10:53:55+00:00
permalink: llmeon/30-library/ops/cmd-kubectl-argocd-grep-drifting-configmap
requires_tunnel: false
tags: [argocd, cmd, configmap, drift, helm, secrets]
target_service: argocd
title: cmd_kubectl_argocd_grep_drifting_configmap
tool: kubectl
---

## Grep Deployment for Drifting ConfigMap Reference

### 🎯 Intent

Introspect a workload deployment manifest for references to an orphaned or drifting hashed ConfigMap/Secret. Common issue when Helm generates a hash-suffixed configmap that changes, leaving the old one lingering in ArgoCD's `OutOfSync` list.

---

### 🌍 Execution Context

Run from:

- [x] Local machine (with context)

---

### ⚡ Action

```bash
kubectl get deploy -n <NAMESPACE> <DEPLOYMENT_NAME> -o yaml | grep -n '<OLD_CONFIGMAP_NAME>\|configMap'
```

#### Placeholders

- `<NAMESPACE>`—Namespace of the deployed workload (NOT argocd).
- `<DEPLOYMENT_NAME>`—Name of the Deployment resource showing `Synced`.
- `<OLD_CONFIGMAP_NAME>`—The name of the configmap causing the drift (found via [[cmd_kubectl_argocd_get_failing_resources]]).

---

### ✅ Verification

- Expected Output: If the `grep` matches nothing for the old configmap name, it means the workload is already consuming the _new_ configuration, and the old ConfigMap is orphaned.

### 💥 Failure Mode Analysis

- Symptom: The deploy _does_ reference the old configmap!
  - Fix: Your deployment did not successfully roll out the payload update and is currently dependent on the drifting resource. Do not delete the drifted ConfigMap until the deployment itself triggers a rollout (via `kubectl rollout restart deployment`).
