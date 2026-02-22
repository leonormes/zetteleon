---
type: command
tool: kubectl
service: vso
risk: read-only
tags: [vso, k8s, secrets, status]
---

# Get VSO CR Details

## 🎯 Intent
Retrieves the specification and lease status (health) of the VSO Custom Resource managing a secret.

---

## 🌍 Execution Context
Run from:
- [x] Local machine (with context)

---

## ⚡ Action

```bash
# Get Full Spec and Status
kubectl get <CR_KIND> <CR_NAME> -n <NAMESPACE> -o yaml
```

### Check Lease Health
```bash
kubectl get <CR_KIND> <CR_NAME> -n <NAMESPACE> -o jsonpath='{.status}' | jq .
```

### Placeholders
- `<CR_KIND>` — `VaultStaticSecret`, `VaultDynamicSecret`, or `VaultPKISecret`.
- `<CR_NAME>` — The name of the VSO resource.
- `<NAMESPACE>` — The Kubernetes namespace.

---

## ✅ Verification
- `status.leaseID`: Should be present for dynamic secrets.
- `status.conditions`: Check for `SyncError` or `VaultConnectionError`.

---

## 🔗 Related
- [[cmd_kubectl_get_secret_origin]]
- [[playbook_vso_secret_debugging]]