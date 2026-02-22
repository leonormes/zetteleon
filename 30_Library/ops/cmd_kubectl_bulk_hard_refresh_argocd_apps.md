---
type: command
tool: kubectl
hop_level: local
target_service: argocd
requires_tunnel: false
status: active
last_verified: 2026-02-22
tags: [cmd, argocd, refresh, cache, debug]
---

# Bulk Hard-Refresh Failing ArgoCD Applications

## 🎯 Intent
Identify all ArgoCD Applications in a namespace experiencing a specific sync status (e.g., `Unknown`) and automatically patch them with the `argocd.argoproj.io/refresh=hard` annotation to force a complete re-evaluation, bypassing all caches.

---

## 🌍 Execution Context
Run from:
- [x] Local machine (with context)

---

## ⚡ Action

> [!WARNING] Load Inducing Command
> Hard refreshing many applications simultaneously can cause sudden spikes in CPU/Memory on the `repo-server` and `application-controller`.

```bash
kubectl get applications -n argocd -o json | \
  jq -r '.items[] | select(.status.sync.status == "Unknown") | .metadata.name' | \
  xargs -I{} kubectl patch application {} -n argocd --type='merge' \
    -p '{"metadata":{"annotations":{"argocd.argoproj.io/refresh":"hard"}}}'
```

---

## ✅ Verification
- Expected Output: A list of `application.argoproj.io/<NAME> patched` statements. You can then `watch kubectl get applications -n argocd` to observe them moving into the `Synced` state.

## 💥 Failure Mode Analysis
- **Symptom:** Output is silent but apps are still "Unknown".
  - **Fix:** It's possible the `Unknown` state is caused by a networking issue to the API server, not a drift or repository auth issue. Check controller logs.

---

## 🔗 Related
- [[cmd_argocd_refresh_app]]
