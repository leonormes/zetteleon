---
created: 2026-02-21T15:07:24+00:00
modified: 2026-08-13T10:53:55+00:00
permalink: llmeon/30-library/ops/cmd-kubectl-decode-secret-data
risk: read-only
service: k8s
tags: [decode, kubectl, secrets]
title: cmd_kubectl_decode_secret_data
tool: kubectl
---

## Decode Secret Data

### 🎯 Intent

Decodes base64 data from Opaque secrets or `dockerconfigjson` registries for human inspection.

---

### 🌍 Execution Context

Run from:

- [x] Local machine (with context)

---

### ⚡ Action

#### For Registry Secrets (Dockerconfigjson)

```bash
kubectl get secret <SECRET_NAME> -n <NAMESPACE> \
  -o jsonpath='{.data.\.dockerconfigjson}' | base64 -d | jq .
```

#### For Opaque Secrets (KV)

```bash
# List all keys first
kubectl get secret <SECRET_NAME> -n <NAMESPACE> -o jsonpath='{.data}' | jq 'keys'

# Decode specific key
kubectl get secret <SECRET_NAME> -n <NAMESPACE> \
  -o jsonpath='{.data.<KEY>}' | base64 -d
```

#### Placeholders

- `<SECRET_NAME>`—Name of the secret.
- `<NAMESPACE>`—Target namespace.
- `<KEY>`—The specific key inside the Opaque secret.

---

### ✅ Verification

- Confirm the `client_id` or `username` matches the expected identity from Vault.

---

### 🔗 Related

- [[kb_vso_metadata_identifiers]]
