---
type: command
tool: kubectl
hop_level: local
target_service: vso
requires_tunnel: false
status: active
last_verified: 2026-02-22
tags: [cmd, kubectl, vso, secrets, static]
---

# Get VaultStaticSecret Manifest

## 🎯 Intent
Output the YAML of a `VaultStaticSecret` deployed by Vault Secrets Operator (VSO) to verify the raw Vault path and the specific Go template rendering keys injecting values into the Kubernetes secret.

---

## 🌍 Execution Context
Run from:
- [x] Local machine (with context)

---

## ⚡ Action

```bash
kubectl get vaultstaticsecrets -n <NAMESPACE>
kubectl get vaultstaticsecret <VSO_SECRET_NAME> -n <NAMESPACE> -o yaml
```

### Placeholders
- `<NAMESPACE>` — Target namespace
- `<VSO_SECRET_NAME>` — Name of the VaultStaticSecret Custom Resource.

---

## ✅ Verification
- Look for the `spec.mount` and `spec.path` to confirm *where* VSO is reading from Vault.
- Look at `spec.destination.transformation` or `spec.destination.create` to see the exact Go templating rules (`{{ get .Secrets "auth0_client_id" }}`) mapping Vault KV pairs into the `auth.json` secret payload.

## 💥 Failure Mode Analysis
- **Symptom:** `error: the server doesn't have a resource type "vaultstaticsecrets"`.
  - **Fix:** VSO is either not installed on this cluster, or your kubeconfig context lacks the CRD definitions. Ensure you are targeting a cluster deploying HashiCorp VSO.
