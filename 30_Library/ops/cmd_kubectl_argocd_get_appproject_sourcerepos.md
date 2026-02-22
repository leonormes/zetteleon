---
type: command
tool: kubectl
hop_level: local
target_service: argocd
requires_tunnel: false
status: active
last_verified: 2026-02-22
tags: [cmd, argocd, appproject, rbac, security]
---

# Get ArgoCD AppProject SourceRepos

## 🎯 Intent
View the explicitly permitted `sourceRepos` configuration of an ArgoCD AppProject. Applications within this project cannot pull Helm charts or Git repositories from URLs not listed here.

---

## 🌍 Execution Context
Run from:
- [x] Local machine (with context)

---

## ⚡ Action

```bash
kubectl get appproject <PROJECT_NAME> -n <NAMESPACE> -o yaml | grep -A 20 'sourceRepos'
```

### Placeholders
- `<PROJECT_NAME>` — Name of the ArgoCD AppProject (e.g. `default`).
- `<NAMESPACE>` — Discovered via Context (usually `argocd`).

---

## ✅ Verification
- **Expected Output:** A YAML array of allowed URL strings or wildcards (e.g., `oci://fitfileregistry.azurecr.io/helm`).

## 💥 Failure Mode Analysis
- **Symptom:** Your registry URL is missing, or ONLY the `oci://` variant exists when a bare URL was requested (or vice-versa).
  - **Fix:** ArgoCD is very strict with URL string matching. Proceed to [[cmd_kubectl_argocd_patch_appproject_sourcerepos]] to inject the missing wildcard variant.
