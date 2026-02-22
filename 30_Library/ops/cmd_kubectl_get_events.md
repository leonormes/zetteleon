---
type: atomic_command
tool: kubectl
hop_level: local
target_service: k8s
requires_tunnel: true
tags: [atomic, kubectl, events, triage]
---

# Get Namespace Events

## 🎯 Intent
Surfaces recent Kubernetes events to diagnose underlying resource issues like image pull errors or scheduling constraints.

---

## 🌍 Execution Context
Run from:
- [x] Local machine (with context)

---

## ⚡ Action

```bash
kubectl get events -n <NAMESPACE> --sort-by='.lastTimestamp'
```

### Placeholders
- `<NAMESPACE>` — target namespace

---

## ✅ Verification
- Look for `Warning` type events in the last 10–15 minutes.

---

## 🔗 Related
- [[cmd_kubectl_get_pods]]
- [[playbook_argocd_sync_failure_triage]]