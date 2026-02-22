---
type: command
tool: kubectl
hop_level: local
target_service: argocd
requires_tunnel: false
status: active
last_verified: 2026-02-22
tags: [cmd, argocd, cm, configmap, globals]
---

# Extract ArgoCD ConfigMap Globals

## 🎯 Intent
Extract OCI and Helm configurations from the global `argocd-cm` ConfigMap. This contains system-wide parameters (like `helm.valuesFileSchemes`) or custom tool configurations overriding default behavior.

---

## 🌍 Execution Context
Run from:
- [x] Local machine (with context)

---

## ⚡ Action

```bash
kubectl get configmap argocd-cm -n argocd -o yaml | grep -i 'helm\|oci'
```

---

## ✅ Verification
- Expected Output: Any custom keys or data values associated with strings containing "helm" or "oci". If silent, ArgoCD operates strictly on out-of-the-box defaults for those subsystems.

## 💥 Failure Mode Analysis
- **Symptom:** `Error from server (NotFound): configmaps "argocd-cm" not found`.
  - **Fix:** Ensure you are actively targeting the `argocd` namespace.
