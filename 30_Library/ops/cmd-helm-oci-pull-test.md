---
type: atomic_command
tool: helm
hop_level: local
target_service: registry
tags: #atomic #helm #oci #acr
---

# Test Helm OCI Login & Pull

## 🎯 Intent
Validate that a specific credential pair has the necessary permissions to authenticate and pull a chart from an OCI registry (like ACR). This isolates registry permissions from Kubernetes/ArgoCD config.

---

## 🌍 Execution Context
Run from:
- [x] Local machine
- [x] Jumpbox

---

## ⚡ Action

```bash
# 1. Login to the registry
helm registry login <REGISTRY_DOMAIN> --username "<APP_ID>" --password "<PASSWORD>"

# 2. Test pulling an artifact
helm pull oci://<REGISTRY_DOMAIN>/<CHART_PATH> --version <VERSION>
```

### Placeholders
- `<REGISTRY_DOMAIN>` — e.g., `fitfileregistry.azurecr.io`
- `<APP_ID>` — Service Principal Client ID
- `<PASSWORD>` — Service Principal Client Secret
- `<CHART_PATH>` — Full path to the chart (e.g., `helm/common`)
- `<VERSION>` — Specific version to pull

---

## ✅ Verification
Expected signal:
- `Login Succeeded`
- A `.tgz` file appears in the current directory after `pull`.

---

## 🔗 Related
- [[pb-argocd-oci-auth-fail]]
