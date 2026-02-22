---
type: command
tool: kubectl
hop_level: local
target_service: kubernetes
requires_tunnel: false
status: active
last_verified: 2026-02-22
tags: [cmd, registry, credentials, secrets, debug]
---

# Get Image Pull Secret Credentials

## 🎯 Intent
Decode and extract the plaintext credentials (username and password) stored inside the `.dockerconfigjson` field of a Kubernetes Image Pull Secret.

---

## 🌍 Execution Context
Run from:
- [x] Local machine (with context)

---

## ⚡ Action

```bash
kubectl get secret <IMAGE_PULL_SECRET> -n <NAMESPACE> \
  -o jsonpath='{.data.\.dockerconfigjson}' | base64 -d | \
  jq '{username: .auths["<REGISTRY>"].username, password: .auths["<REGISTRY>"].password}'
```

### Placeholders
- `<IMAGE_PULL_SECRET>` — Name of the Secret of type `kubernetes.io/dockerconfigjson`
- `<NAMESPACE>` — The Kubernetes namespace
- `<REGISTRY>` — The exact domain of the registry (e.g., `fitfileregistry.azurecr.io`)

---

## ✅ Verification
- Expected Output: A JSON object containing the plaintext `username` and `password` configured for that specific registry URL.

## 💥 Failure Mode Analysis
- **Symptom:** `jq: error: Cannot iterate over null`
  - **Fix:** The `<REGISTRY>` placeholder URL you provided exactly matches no keys in the `.auths` map within the decoded JSON. Run `[[cmd_kubectl_find_image_pull_secrets]]` to see the exact registry URL literal stored within the secret.

---

## 🔗 Related
- [[cmd_kubectl_find_image_pull_secrets]]
- [[cmd_kubectl_argocd_get_secret_creds]]
