---
created: 2026-02-21T15:05:07+00:00
hop_level: local
modified: 2026-07-13T08:45:27+00:00
permalink: llmeon/30-library/ops/cmd-argocd-diff-app
requires_tunnel: true
tags: [argocd, atomic, diff, triage]
target_service: argocd
title: cmd_argocd_diff_app
tool: argocd
---

## Diff ArgoCD Application

### 🎯 Intent

Compares the desired state in Git with the live state in the Kubernetes cluster to identify specific drifts.

---

### 🌍 Execution Context

Run from:

- [x] Local machine (with tunnel)

---

### ⚡ Action

```bash
argocd app diff <APP_NAME>
```

#### Placeholders

- `<APP_NAME>`—The name of the ArgoCD application.

---

### ✅ Verification

- Review the output for `+` (added) or `-` (removed) fields.
- If output is empty, the states are perfectly aligned.

---

### 🧠 Failure Modes

- `ComparisonError`: Indicates an issue rendering manifests or connection issues with the cluster.

---

### 🔗 Related

- [[cmd_argocd_get_app]]
- [[kb_argocd_sync_failure_causes]]
