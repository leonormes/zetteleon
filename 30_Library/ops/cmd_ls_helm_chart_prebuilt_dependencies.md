---
type: command
tool: ls
hop_level: local
target_service: helm
requires_tunnel: false
status: active
last_verified: 2026-02-22
tags: [cmd, helm, dependencies, cache, git]
---

# List Helm Chart Pre-Built Dependencies

## 🎯 Intent
Check if a Helm chart has pre-built (.tgz) dependencies committed inside its local `charts/` directory.

---

## 🌍 Execution Context
Run from:
- [x] Local machine (within the target Git repository)

---

## ⚡ Action

```bash
ls -la <CHART_PATH>/charts/
```

### Placeholders
- `<CHART_PATH>` — Relative path to the parent chart directory in your local git repository.

---

## ✅ Verification
- **Expected Output:** Presence of compressed tarballs (e.g., `dependency-1.0.0.tgz`). If present, `helm dependency build` is bypassed by ArgoCD entirely, and registry authentication errors during sync are impossible. 

## 💥 Failure Mode Analysis
- **Symptom:** `ls: <CHART_PATH>/charts/: No such file or directory` or an empty directory.
  - **Fix:** ArgoCD will attempt to resolve and download the dependencies dynamically. It requires exact `repo-creds` and AppProject rules configuration.
