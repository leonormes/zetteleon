---
created: 2026-02-21 15:07:25+00:00
modified: 2026-03-14 11:10:10+00:00
risk: low
service: vso
tags:
- config
- k8s
- mutation
- vso
title: cmd_kubectl_patch_vso_overwrite
tool: kubectl
type: command
permalink: llmeon/30-library/ops/cmd-kubectl-patch-vso-overwrite
---

## Patch VSO Overwrite Property

### 🎯 Intent

Enables the `overwrite` property on a VSO resource to ensure the operator can recover from manual edits or drift.

---

### 🌍 Execution Context

Run from:

- [x] Local machine (with context)

---

### ⚡ Action

```bash
kubectl patch <CR_KIND> <CR_NAME> -n <NAMESPACE> \
  --type='merge' \
  -p '{"spec":{"destination":{"overwrite":true}}}'
```

#### Placeholders

- `<CR_KIND>`—The VSO resource kind.
- `<CR_NAME>`—The VSO resource name.
- `<NAMESPACE>`—The namespace.

---

### ✅ Verification

```bash
kubectl get <CR_KIND> <CR_NAME> -n <NAMESPACE> -o jsonpath='{.spec.destination.overwrite}'
```

---

### 🔗 Related

- [[kb_vso_stale_credentials_logic]]
- [[playbook_argocd_vso_oci_registry_auth_failure]]