---
created: 2026-02-22T16:53:22+00:00
hop_level: local
last_verified: 2026-02-22
modified: 2026-03-14T11:10:10+00:00
requires_tunnel: false
status: active
tags: [cmd, credentials, debug, registry, secrets]
target_service: kubernetes
title: cmd_kubectl_get_image_pull_secret_creds
tool: kubectl
type: command
---

## Get Image Pull Secret Credentials

### 🎯 Intent

Decode and extract the plaintext credentials (username and password) stored inside the `.dockerconfigjson` field of a Kubernetes Image Pull Secret.

---

### 🌍 Execution Context

Run from:

- [x] Local machine (with context)

---

### ⚡ Action

```bash
kubectl get secret <IMAGE_PULL_SECRET> -n <NAMESPACE> \
  -o jsonpath='{.data.\.dockerconfigjson}' | base64 -d | \
  jq '{username: .auths["<REGISTRY>"].username, password: .auths["<REGISTRY>"].password}'
```

#### Placeholders

- `<IMAGE_PULL_SECRET>`—Name of the Secret of type `kubernetes.io/dockerconfigjson`
- `<NAMESPACE>`—The Kubernetes namespace
- `<REGISTRY>`—The exact domain of the registry (e.g., `fitfileregistry.azurecr.io`)

---

### ✅ Verification

- Expected Output: A JSON object containing the plaintext `username` and `password` configured for that specific registry URL.

### 💥 Failure Mode Analysis

- Symptom: `jq: error: Cannot iterate over null`
  - Fix: The `<REGISTRY>` placeholder URL you provided exactly matches no keys in the `.auths` map within the decoded JSON. Run `[[cmd_kubectl_find_image_pull_secrets]]` to see the exact registry URL literal stored within the secret.

---

### 🔗 Related

- [[cmd_kubectl_find_image_pull_secrets]]
- [[cmd_kubectl_argocd_get_secret_creds]]
