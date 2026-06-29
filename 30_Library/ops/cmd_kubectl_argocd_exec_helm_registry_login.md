---
created: 2026-02-22 16:57:21+00:00
hop_level: local
last_verified: 2026-02-22
modified: 2026-03-14 11:10:11+00:00
requires_tunnel: false
status: active
tags:
- argocd
- auth
- cmd
- exec
- helm
- oci
target_service: argocd
title: cmd_kubectl_argocd_exec_helm_registry_login
tool: kubectl
type: command
permalink: llmeon/30-library/ops/cmd-kubectl-argocd-exec-helm-registry-login
---

## Test Helm Registry Login from Repo-Server Pod

### 🎯 Intent

Test registry authentication explicitly from _inside_ the `argocd-repo-server` pod. This isolates network boundary issues (e.g., Egress restrictions from the ArgoCD namespace to the ACR endpoint) while proving the helm binary inside ArgoCD can negotiate the TLS handshake successfully.

---

### 🌍 Execution Context

Run from:

- [x] Local machine (with context)

---

### ⚡ Action

```bash
POD=$(kubectl get pod -n argocd -l app.kubernetes.io/name=argocd-repo-server -o jsonpath='{.items[0].metadata.name}')

kubectl exec -n argocd $POD -c repo-server -- \
  sh -c "echo '<PASSWORD>' | helm registry login <REGISTRY_DOMAIN> --username '<USERNAME>' --password-stdin"
```

#### Placeholders

- `<PASSWORD>`—Credential from repository secret
- `<USERNAME>`—Credential from repository secret
- `<REGISTRY_DOMAIN>`—The registry endpoint (e.g., `myregistry.azurecr.io`)

---

### ✅ Verification

- Expected Output: `Login Succeeded` printed directly from the stdout of the `repo-server` pod execution stream.

### 💥 Failure Mode Analysis

- Symptom: `dial tcp: lookup <REGISTRY> on 10.96.0.10:53: no such host` or connection timed out.
  - Fix: The pod is unable to egress to the public internet or resolve DNS to reach the registry. Check Calico network policies, NAT gateways, or private DNS link configurations in this specific cluster.