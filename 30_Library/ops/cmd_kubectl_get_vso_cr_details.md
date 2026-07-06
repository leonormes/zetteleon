---
created: 2026-02-21T15:07:24+00:00
modified: 2026-07-04T10:50:41+00:00
permalink: llmeon/30-library/ops/cmd-kubectl-get-vso-cr-details
risk: read-only
service: vso
tags: [k8s, secrets, status, vso]
title: cmd_kubectl_get_vso_cr_details
tool: kubectl
type: command
---

## Get VSO CR Details

### 🎯 Intent

Retrieves the specification and lease status (health) of the VSO Custom Resource managing a secret.

---

### 🌍 Execution Context

Run from:

- [x] Local machine (with context)

---

### ⚡ Action

```bash
# Get Full Spec and Status
kubectl get <CR_KIND> <CR_NAME> -n <NAMESPACE> -o yaml
```

#### Check Lease Health

```bash
kubectl get <CR_KIND> <CR_NAME> -n <NAMESPACE> -o jsonpath='{.status}' | jq .
```

#### Placeholders

- `<CR_KIND>`—`VaultStaticSecret`, `VaultDynamicSecret`, or `VaultPKISecret`.
- `<CR_NAME>`—The name of the VSO resource.
- `<NAMESPACE>`—The Kubernetes namespace.

---

### ✅ Verification

- `status.leaseID`: Should be present for dynamic secrets.
- `status.conditions`: Check for `SyncError` or `VaultConnectionError`.

---

### 🔗 Related

- [[cmd_kubectl_get_secret_origin]]
- [[playbook_vso_secret_debugging]]
- [[playbook_argocd_vso_oci_registry_auth_failure]]
