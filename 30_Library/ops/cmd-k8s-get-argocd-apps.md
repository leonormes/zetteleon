---
type: atomic_command
tool: kubectl
hop_level: local
target_service: argocd
requires_tunnel: true
prerequisites:
  - [[cmd-ssh-bastion-tunnel]]
tags: #atomic #kubectl #argocd
---

# List ArgoCD Applications

## 🎯 Intent
Get a high-level overview of all applications managed by ArgoCD, including their sync and health status.

---

## 🌍 Execution Context
Run from:
- [x] Local machine (with tunnel)
- [ ] Bastion host
- [ ] Inside cluster

Active requirements:
- [x] KUBECONFIG set
- [x] SSH tunnel to cluster API active

---

## ⚡ Action

```bash
kubectl get applications -n argocd
```

### Table View (Recommended)
```bash
kubectl get applications -n argocd -o custom-columns=NAME:.metadata.name,SYNC:.status.sync.status,HEALTH:.status.health.status --no-headers
```

---

## ✅ Verification
Expected signal:
- List of applications with `Synced` and `Healthy` status.

---

## 🔗 Related
- [[cmd-k8s-describe-argocd-app]]
