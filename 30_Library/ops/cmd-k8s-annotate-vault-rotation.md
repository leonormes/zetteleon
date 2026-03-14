---
created: 2026-02-16T11:46:04+00:00
hop_level: local
modified: 2026-03-14T11:10:11+00:00
requires_tunnel: true
tags: [atomic, kubectl, vault]
target_service: vault-secrets-operator
title: cmd-k8s-annotate-vault-rotation
tool: kubectl
type: atomic_command
---

## Force Vault Secret Rotation

### 🎯 Intent

Force the Vault Secrets Operator to immediately re-fetch secrets from Vault, bypassing the refresh interval. Useful when rotating Git tokens or updating credentials.

---

### 🌍 Execution Context

Run from:

- [x] Local machine (with tunnel)

---

### ⚡ Action

```bash
kubectl annotate vaultstaticsecret <secret_name> -n argocd secrets.hashicorp.com/vault-force-rotation="$(date +%s)" --overwrite
```

#### Placeholders

- `<secret_name>`—Name of the `VaultStaticSecret` resource

---

### ✅ Verification

```bash
kubectl get events -n argocd --sort-by='.lastTimestamp' -w | grep SecretRotated
```

Expected signal:

- `SecretRotated` event appearing for the target secret.

---

### 🔗 Related

- [[pb-argocd-sync-failure-triage]]
