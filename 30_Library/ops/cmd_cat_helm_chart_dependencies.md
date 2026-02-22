---
type: command
tool: cat
hop_level: local
target_service: helm
requires_tunnel: false
status: active
last_verified: 2026-02-22
tags: [cmd, helm, dependencies, chart, git]
---

# Cat Helm Chart Dependencies

## 🎯 Intent
Extract and list the dependencies defined in a Helm `Chart.yaml` file to quickly identify if they rely on external OCI registries.

---

## 🌍 Execution Context
Run from:
- [x] Local machine (within the target Git repository)

---

## ⚡ Action

```bash
cat <CHART_PATH>/Chart.yaml | grep -A 5 'dependencies'
```

### Placeholders
- `<CHART_PATH>` — Relative path to the chart directory in your local git repository.

---

## ✅ Verification
- **Expected Output:** A YAML block showing `- name: <chart>`, `version: <version>`, and crucially `repository: oci://<REGISTRY_DOMAIN>`. If it's `oci://`, ArgoCD needs OCI permissions and valid credentials to resolve it during manifest generation.

## 💥 Failure Mode Analysis
- **Symptom:** Blank output.
  - **Fix:** The chart has no defined dependencies, or they are configured in a non-standard way. Manually open `Chart.yaml` to investigate.
