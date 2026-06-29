---
created: 2026-02-22 16:53:18+00:00
hop_level: local
last_verified: 2026-02-22
modified: 2026-03-14 11:10:10+00:00
requires_tunnel: false
status: active
tags:
- argocd
- cmd
- credentials
- debug
- secrets
target_service: argocd
title: cmd_kubectl_argocd_get_secret_creds
tool: kubectl
type: command
permalink: llmeon/30-library/ops/cmd-kubectl-argocd-get-secret-creds
---

## Get ArgoCD Repository Secret Credentials

### 🎯 Intent

Decode and display the base64-encoded `username` and `password` fields from an ArgoCD repository Secret (`Opaque` type with label `argocd.argoproj.io/secret-type: repository` or `repo-creds`).

---

### 🌍 Execution Context

Run from:

- [x] Local machine (with context)

---

### ⚡ Action

```bash
kubectl get secret <SECRET_NAME> -n argocd -o json | \
  jq '{name: .metadata.name, username: (.data.username | @base64d), password: (.data.password | @base64d)}'
```

#### Placeholders

- `<SECRET_NAME>`—Name of the target Secret

---

### ✅ Verification

- Expected Output: A JSON object containing the plaintext `username` and `password`. Use this to compare against Vault credentials to detect stale synchronization.

### 💥 Failure Mode Analysis

- Symptom: `jq: error: base64d: input string is not valid base64` or `null` values.
  - Fix: The secret is missing the `username` or `password` fields, or they are not valid base64 strings. Verify the secret is properly formed or managed correctly by VSO.

---

### 🔗 Related

- [[cmd_kubectl_argocd_find_repo_secrets]]
- [[cmd_kubectl_get_image_pull_secret_creds]]