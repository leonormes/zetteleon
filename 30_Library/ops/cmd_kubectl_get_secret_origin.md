---
created: 2026-02-21 15:07:23+00:00
modified: 2026-03-14 11:10:10+00:00
risk: read-only
service: vso
tags:
- k8s
- secrets
- triage
- vso
title: cmd_kubectl_get_secret_origin
tool: kubectl
type: command
permalink: llmeon/30-library/ops/cmd-kubectl-get-secret-origin
---

## Get Secret Origin Metadata

### 🎯 Intent

Identifies the controller that manages a secret and finds the corresponding owner references (VSO, Helm, ArgoCD).

---

### 🌍 Execution Context

Run from:

- [x] Local machine (with context)

---

### ⚡ Action

```bash
kubectl get secret <SECRET_NAME> -n <NAMESPACE> -o yaml
```

#### Specialized Extraction

```bash
# Extract Owner References and Managed-By Labels
kubectl get secret <SECRET_NAME> -n <NAMESPACE> \
  -o jsonpath='{.metadata.ownerReferences}{"\n"}{.metadata.labels}{"\n"}{.metadata.annotations}' | jq .
```

#### Placeholders

- `<SECRET_NAME>`—Name of the secret.
- `<NAMESPACE>`—Target namespace.

---

### ✅ Verification

- Check `metadata.labels` for `app.kubernetes.io/managed-by: hashicorp-vso`.
- Check `metadata.ownerReferences` for the VSO Custom Resource type (`VaultStaticSecret`, etc.).

---

### 🧠 Failure Modes

- `Secret not found`: Verify namespace and name.
- `Empty OwnerReferences`: The secret was likely created manually or via a tool that doesn't use OwnerRefs.

---

### 🔗 Related

- [[kb_vso_metadata_identifiers]]
- [[playbook_vso_secret_debugging]]