---
created: 2026-02-22T16:52:55+00:00
hop_level: local
last_verified: 2026-02-22
modified: 2026-07-20T16:33:37+00:00
permalink: llmeon/30-library/ops/cmd-kubectl-argocd-find-repo-secrets
requires_tunnel: false
tags: [argocd, cmd, credentials, debug, secrets]
target_service: argocd
title: cmd_kubectl_argocd_find_repo_secrets
tool: kubectl
---

## Find ArgoCD Repository Secrets

### 🎯 Intent

Locate all Kubernetes Secrets in the `argocd` namespace that are tagged as exact-match repository credentials (`secret-type=repository`). Decodes the URL to easily identify which registry they target.

---

### 🌍 Execution Context

Run from:

- [x] Local machine (with context)

---

### ⚡ Action

```bash
kubectl get secrets -n argocd -l argocd.argoproj.io/secret-type=repository -o json | \
  jq '.items[] | select(.data.url) | {name: .metadata.name, url: (.data.url | @base64d)}'
```

---

### ✅ Verification

- Expected Output: A stream of JSON objects containing `name` and decoded `url`. Find the secret targeting your specific registry URL.

### 💥 Failure Mode Analysis

- Symptom: Blank output
  - Fix: There are no exact-match repository secrets. Check for template credentials using `repo-creds` instead.

---

### 🔗 Related

- [[cmd_kubectl_argocd_find_repo_creds]]
- [[cmd_kubectl_argocd_get_secret_creds]]
