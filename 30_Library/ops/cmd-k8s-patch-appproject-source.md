---
type: atomic_command
tool: kubectl
hop_level: local
target_service: argocd
requires_tunnel: true
tags: #atomic #kubectl #argocd
---

# Allow OCI Sources in ArgoCD Project

## 🎯 Intent
Explicitly permit an OCI registry as a valid source repository within an ArgoCD `AppProject`. Without this, ArgoCD will refuse to pull even with valid credentials.

---

## 🌍 Execution Context
Run from:
- [x] Local machine (with tunnel)

---

## ⚡ Action

```bash
kubectl patch appproject <PROJECT_NAME> -n argocd --type='merge' -p 
'{"spec": {"sourceRepos": ["*", "oci://<REGISTRY_DOMAIN>/*"]}}'
```

### Placeholders
- `<PROJECT_NAME>` — The name of the ArgoCD Project (usually `default` or customer-specific)
- `<REGISTRY_DOMAIN>` — The OCI registry host (e.g., `fitfileregistry.azurecr.io`)

---

## ✅ Verification
```bash
kubectl get appproject <PROJECT_NAME> -n argocd -o jsonpath='{.spec.sourceRepos}'
```

---

## 🔗 Related
- [[pb-argocd-oci-auth-fail]]
