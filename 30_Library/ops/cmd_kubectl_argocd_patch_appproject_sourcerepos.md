---
created: 2026-02-22T16:57:13+00:00
hop_level: local
last_verified: 2026-02-22
modified: 2026-07-04T10:50:41+00:00
permalink: llmeon/30-library/ops/cmd-kubectl-argocd-patch-appproject-sourcerepos
requires_tunnel: false
status: active
tags: [appproject, argocd, cmd, patch, rbac]
target_service: argocd
title: cmd_kubectl_argocd_patch_appproject_sourcerepos
tool: kubectl
type: command
---

## Allow OCI Sources in ArgoCD Project

### 🎯 Intent

Explicitly permit an OCI registry as a valid source repository within an ArgoCD `AppProject`. Without this, ArgoCD will refuse to pull even with valid credentials, often throwing a `ComparisonError` with `are not permitted in project`. This completely replaces legacy patching commands.

---

### 🌍 Execution Context

Run from:

- [x] Local machine (with context)

---

### ⚡ Action

Wildcard patch to add the registry base domain natively and the `oci://` scheme protocol version. ArgoCD URL matching is inconsistent, so patching a wildcard `*` is the most robust fix.

```bash
kubectl patch appproject <PROJECT_NAME> -n argocd --type='json' \
  -p='[{"op": "add", "path": "/spec/sourceRepos/-", "value": "oci://<REGISTRY_DOMAIN>/*"}]'
```

#### Placeholders

- `<PROJECT_NAME>`—The name of the ArgoCD Project (usually `default` or customer-specific)
- `<REGISTRY_DOMAIN>`—The OCI registry host (e.g., `fitfileregistry.azurecr.io`)

---

### ✅ Verification

```bash
kubectl get appproject <PROJECT_NAME> -n argocd -o yaml | grep -A 5 -B 5 "oci://<REGISTRY_DOMAIN>"
```

### 💥 Failure Mode Analysis

- Symptom: Sync still failing with 'are not permitted' errors despite patch application.
  - Fix: ArgoCD heavily caches AppProject manifest generation. You must bust the cache. Restart the `argocd-repo-server` deployment `[[cmd_kubectl_restart_argocd_repo_server]]` and issue a hard-refresh `[[cmd_argocd_refresh_app]]`.
