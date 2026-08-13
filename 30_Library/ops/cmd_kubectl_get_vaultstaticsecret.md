---
created: 2026-02-22T17:06:27+00:00
hop_level: local
last_verified: 2026-02-22
modified: 2026-08-13T10:53:55+00:00
permalink: llmeon/30-library/ops/cmd-kubectl-get-vaultstaticsecret
requires_tunnel: false
tags: [cmd, kubectl, secrets, static, vso]
target_service: vso
title: cmd_kubectl_get_vaultstaticsecret
tool: kubectl
---

## Get VaultStaticSecret Manifest

### 🎯 Intent

Output the YAML of a `VaultStaticSecret` deployed by Vault Secrets Operator (VSO) to verify the raw Vault path and the specific Go template rendering keys injecting values into the Kubernetes secret.

---

### 🌍 Execution Context

Run from:

- [x] Local machine (with context)

---

### ⚡ Action

```bash
kubectl get vaultstaticsecrets -n <NAMESPACE>
kubectl get vaultstaticsecret <VSO_SECRET_NAME> -n <NAMESPACE> -o yaml
```

#### Placeholders

- `<NAMESPACE>`—Target namespace
- `<VSO_SECRET_NAME>`—Name of the VaultStaticSecret Custom Resource.

---

### ✅ Verification

- Look for the `spec.mount` and `spec.path` to confirm _where_ VSO is reading from Vault.
- Look at `spec.destination.transformation` or `spec.destination.create` to see the exact Go templating rules (`{{ get.Secrets "auth0_client_id" }}`) mapping Vault KV pairs into the `auth.json` secret payload.

### 💥 Failure Mode Analysis

- Symptom: `error: the server doesn't have a resource type "vaultstaticsecrets"`.
  - Fix: VSO is either not installed on this cluster, or your kubeconfig context lacks the CRD definitions. Ensure you are targeting a cluster deploying HashiCorp VSO.
