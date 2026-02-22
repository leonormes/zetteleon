---
type: command
tool: kubectl
hop_level: local
target_service: pod
requires_tunnel: false
status: active
last_verified: 2026-02-22
tags: [cmd, kubectl, logs, init, crash, debug]
---

# Get Init-Container Logs

## 🎯 Intent
Retrieve logs specifically from an init-container (including previous crashed instances) to debug bootstrap failures like Auth0 token retrieval or database migrations that block the main application container from ever starting.

---

## 🌍 Execution Context
Run from:
- [x] Local machine (with context)

---

## ⚡ Action

```bash
# Get logs for the currently running/failing init container
kubectl logs -n <NAMESPACE> <POD_NAME> -c <INIT_CONTAINER_NAME>

# Get logs for the previous instance of the container (if it crashed and restarted)
kubectl logs -n <NAMESPACE> <POD_NAME> -c <INIT_CONTAINER_NAME> --previous
```

### Placeholders
- `<NAMESPACE>` — Target namespace
- `<POD_NAME>` — Name of the pod stuck in `Init:Error` or `Init:CrashLoopBackOff`
- `<INIT_CONTAINER_NAME>` — The specific init container (find this via `kubectl describe pod`).

---

## ✅ Verification
- Expected Output: Streamed logs detailing HTTP failures (e.g., `403 Forbidden` from Auth0) or exit codes explaining why the initialization sequence aborted.

## 💥 Failure Mode Analysis
- **Symptom:** `Error from server (BadRequest): previous terminated container... not found`.
  - **Fix:** The container has never crashed in this pod's lifecycle, so there is no `--previous` state. Drop the `--previous` flag.
