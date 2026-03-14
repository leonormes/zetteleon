---
created: 2026-02-22T16:56:49+00:00
hop_level: local
last_verified: 2026-02-22
modified: 2026-03-14T11:10:11+00:00
requires_tunnel: false
status: active
tags: [chart, cmd, dependencies, git, helm]
target_service: helm
title: cmd_cat_helm_chart_dependencies
tool: cat
type: command
---

## Cat Helm Chart Dependencies

### 🎯 Intent

Extract and list the dependencies defined in a Helm `Chart.yaml` file to quickly identify if they rely on external OCI registries.

---

### 🌍 Execution Context

Run from:

- [x] Local machine (within the target Git repository)

---

### ⚡ Action

```bash
cat <CHART_PATH>/Chart.yaml | grep -A 5 'dependencies'
```

#### Placeholders

- `<CHART_PATH>`—Relative path to the chart directory in your local git repository.

---

### ✅ Verification

- Expected Output: A YAML block showing `- name: <chart>`, `version: <version>`, and crucially `repository: oci://<REGISTRY_DOMAIN>`. If it's `oci://`, ArgoCD needs OCI permissions and valid credentials to resolve it during manifest generation.

### 💥 Failure Mode Analysis

- Symptom: Blank output.
  - Fix: The chart has no defined dependencies, or they are configured in a non-standard way. Manually open `Chart.yaml` to investigate.
