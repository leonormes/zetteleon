---
type: atomic_command
tool: kubectl
hop_level: local
target_service: k8s
requires_tunnel: true
tags: [atomic, kubectl, pods, verification]
---

# Get Pods Wide Output

## 🎯 Intent
Confirms pod status, node placement, and restart counts to verify deployment health.

---

## 🌍 Execution Context
Run from:
- [x] Local machine (with context)

---

## ⚡ Action

```bash
kubectl get pods -n <NAMESPACE> -l <LABEL_SELECTOR> -o wide
```

### Placeholders
- `<NAMESPACE>` — target namespace
- `<LABEL_SELECTOR>` — label filter (e.g., `app=my-service`)

---

## ✅ Verification
- `STATUS` should be `Running`.
- `RESTARTS` should be 0 or stable.

---

## 🔗 Related
- [[cmd_kubectl_get_events]]