---
type: command
tool: kubectl
service: vso
risk: low
tags: [vso, k8s, mutation, config]
---

# Patch VSO Overwrite Property

## 🎯 Intent
Enables the `overwrite` property on a VSO resource to ensure the operator can recover from manual edits or drift.

---

## 🌍 Execution Context
Run from:
- [x] Local machine (with context)

---

## ⚡ Action

```bash
kubectl patch <CR_KIND> <CR_NAME> -n <NAMESPACE> \
  --type='merge' \
  -p '{"spec":{"destination":{"overwrite":true}}}'
```

### Placeholders
- `<CR_KIND>` — The VSO resource kind.
- `<CR_NAME>` — The VSO resource name.
- `<NAMESPACE>` — The namespace.

---

## ✅ Verification
```bash
kubectl get <CR_KIND> <CR_NAME> -n <NAMESPACE> -o jsonpath='{.spec.destination.overwrite}'
```

---

## 🔗 Related
- [[kb_vso_stale_credentials_logic]]