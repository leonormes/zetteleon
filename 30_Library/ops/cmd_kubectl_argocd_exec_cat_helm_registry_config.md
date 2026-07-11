---
created: 2026-02-22 16:57:54+00:00
hop_level: local
last_verified: 2026-02-22
modified: 2026-07-04 10:50:42+00:00
permalink: llmeon/30-library/ops/cmd-kubectl-argocd-exec-cat-helm-registry-config
requires_tunnel: false
tags:
- argocd
- cmd
- config
- exec
- registry
target_service: argocd
title: cmd_kubectl_argocd_exec_cat_helm_registry_config
tool: kubectl
prodos:
  kind: ops
  lifecycle: active
---


## View Repo-Server Internal Helm Config

### 🎯 Intent

View the runtime `config.json` constructed internally by ArgoCD for the Helm CLI directly inside the `repo-server` pod. This proves decisively whether Kubernetes `repository` mapping secret configurations ever reached Helm's execution environment.

---

### 🌍 Execution Context

Run from:

- [x] Local machine (with context)

---

### ⚡ Action

```bash
POD=$(kubectl get pod -n argocd -l app.kubernetes.io/name=argocd-repo-server -o jsonpath='{.items[0].metadata.name}')

kubectl exec -n argocd $POD -c repo-server -- cat /helm-working-dir/registry/config.json 2>/dev/null | jq .
```

---

### ✅ Verification

- Expected Output: Structured JSON payload containing an `auths` object. Confirm your `<REGISTRY_URL>` exists as a key, with `auth` details attached.

### 💥 Failure Mode Analysis

- Symptom: `cat: /helm-working-dir/registry/config.json: No such file or directory`.
  - Fix: Either Helm hasn't attempted a registry interaction since the pod started, or ArgoCD is managing configuration via alternative temporary directories.
