---
created: 2026-02-21 15:07:25+00:00
modified: 2026-03-14 11:10:10+00:00
risk: read-only
service: reflector
tags:
- reflector
- secrets
- verification
title: cmd_kubectl_verify_reflector_sync
tool: kubectl
type: command
permalink: llmeon/30-library/ops/cmd-kubectl-verify-reflector-sync
---

## Verify Reflector Secret Sync

### 🎯 Intent

Audits mirrored copies of a secret across multiple namespaces to ensure they are synchronized with the source.

---

### 🌍 Execution Context

Run from:

- [x] Local machine (with context)

---

### ⚡ Action

```bash
# 1. Identify Target Namespaces
kubectl get secret <SECRET_NAME> -n <SOURCE_NAMESPACE> \
  -o jsonpath='{.metadata.annotations.reflector\.v1\.k8s\.emberstack\.com/reflection-auto-namespaces}'

# 2. Compare Data Hashes (Audit)
# Manually provide the list of namespaces to verify
for ns in NAMESPACE_LIST; do
  echo -n "$ns: "
  kubectl get secret <SECRET_NAME> -n $ns \
    -o jsonpath='{.data}' 2>/dev/null | md5sum || echo "NOT FOUND"
done
```

#### Placeholders

- `<SECRET_NAME>`—The name of the secret.
- `<SOURCE_NAMESPACE>`—The namespace containing the VSO-managed source.

---

### ✅ Verification

- All MD5 hashes should match the source namespace hash.

---

### 🔗 Related

- [[playbook_vso_secret_debugging]]