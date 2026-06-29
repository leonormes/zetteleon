---
created: 2026-02-22 17:01:27+00:00
hop_level: local
last_verified: 2026-02-22
modified: 2026-03-14 11:10:11+00:00
requires_tunnel: false
status: active
tags:
- app-of-apps
- argocd
- bulk
- cmd
- refresh
target_service: argocd
title: cmd_kubectl_argocd_bulk_refresh_children
tool: kubectl
type: command
permalink: llmeon/30-library/ops/cmd-kubectl-argocd-bulk-refresh-children
---

## Bulk Hard-Refresh ArgoCD Child Applications

### 🎯 Intent

Automatically discover all child applications belonging to an "app-of-apps" parent and trigger a hard refresh on every single one. Parent application statuses often don't clear until their children have successfully re-compared.

---

### 🌍 Execution Context

Run from:

- [x] Local machine (with context)

---

### ⚡ Action

```bash
# Refresh parent first
kubectl annotate application -n argocd <PARENT_APP_NAME> argocd.argoproj.io/refresh=hard --overwrite

# Feed the list of child apps into a loop and hard-refresh them
kubectl get application -n argocd <PARENT_APP_NAME> -o jsonpath='{range .status.resources[?(@.kind=="Application")]}{.name}{"\n"}{end}' | \
xargs -I{} kubectl annotate application -n argocd {} argocd.argoproj.io/refresh=hard --overwrite
```

#### Placeholders

- `<PARENT_APP_NAME>`—Name of the Parent ArgoCD Application

---

### ✅ Verification

- Watch the output stream to ensure every child `application.argoproj.io/name patched` succeeds.

### 💥 Failure Mode Analysis

- Symptom: `xargs: missing operand`.
  - Fix: The parent app has no children, so the loop received empty input.