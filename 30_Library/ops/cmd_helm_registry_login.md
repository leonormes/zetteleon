---
type: command
tool: helm
hop_level: local
target_service: registry
requires_tunnel: false
status: active
last_verified: 2026-02-22
tags: [cmd, helm, oci, acr, auth, test]
---

# Test Helm OCI Registry Login

## 🎯 Intent
Validate that a specific credential pair (username and password) has the necessary permissions to authenticate and pull a chart from an OCI registry. This isolates pure registry RBAC permissions from Kubernetes or ArgoCD secret configuration complexities.

---

## 🌍 Execution Context
Run from:
- [x] Local machine
- [x] Jumpbox

---

## ⚡ Action

```bash
# 1. Login to the registry
echo "<PASSWORD>" | helm registry login <REGISTRY_DOMAIN> --username "<USERNAME>" --password-stdin

# 2. Test pulling an artifact
helm pull oci://<REGISTRY_DOMAIN>/<CHART_PATH> --version <VERSION>
```

### Placeholders
- `<REGISTRY_DOMAIN>` — e.g., `fitfileregistry.azurecr.io`
- `<USERNAME>` — Service Principal Client ID or Token
- `<PASSWORD>` — Service Principal Client Secret
- `<CHART_PATH>` — Full path to the chart (e.g., `helm/common`)
- `<VERSION>` — Specific version to pull

---

## ✅ Verification
Expected signal:
- `Login Succeeded` prints to standard output.
- A `.tgz` file appears in the current directory after `pull`.

## 💥 Failure Mode Analysis
- **Symptom:** `response status code 401: unauthorized...`
  - **Fix:** The provided credentials are fundamentally invalid, expired, or lack `AcrPull` permissions on the Azure Container Registry. Do not proceed to debugging ArgoCD until this succeeds locally.
