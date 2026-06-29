---
created: 2026-02-21 15:07:24+00:00
modified: 2026-03-14 11:10:10+00:00
risk: high
service: vso
tags:
- k8s
- mutation
- recovery
- vso
title: cmd_kubectl_recreate_vso_secret
tool: kubectl
type: command
permalink: llmeon/30-library/ops/cmd-kubectl-recreate-vso-secret
---

## Recreate VSO Managed Secret

### 🎯 Intent

Forces VSO to recreate a secret with fresh credentials by deleting the current instance. Use this when credentials are stale or manually corrupted.

---

### 🌍 Execution Context

Run from:

- [x] Local machine (with context)

---

### ⚡ Action

```bash
# Delete the secret
kubectl delete secret <SECRET_NAME> -n <NAMESPACE>

# Watch for automatic recreation
kubectl get secret -n <NAMESPACE> -w | grep <SECRET_NAME>
```

#### Placeholders

- `<SECRET_NAME>`—The name of the Kubernetes secret.
- `<NAMESPACE>`—The namespace.

---

### ✅ Verification

- Check the `creationTimestamp` of the new secret.

---

### 🧠 Failure Modes

- `Secret does not reappear`: Check VSO operator logs; the `VaultAuth` or `VaultConnection` may be failing.

---

### 🔗 Related

- [[cmd_kubectl_patch_vso_overwrite]]
- [[playbook_vso_secret_debugging]]
- [[playbook_argocd_oci_helm_dependency_troubleshooting]]