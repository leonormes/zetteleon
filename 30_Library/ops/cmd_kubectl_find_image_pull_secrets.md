---
created: 2026-02-22T16:53:14+00:00
hop_level: local
last_verified: 2026-02-22
modified: 2026-07-13T08:53:00+00:00
permalink: llmeon/30-library/ops/cmd-kubectl-find-image-pull-secrets
requires_tunnel: false
tags: [cmd, credentials, debug, registry, secrets]
target_service: kubernetes
title: cmd_kubectl_find_image_pull_secrets
tool: kubectl
---

## Find Image Pull Secrets for a Registry

### 🎯 Intent

Locate all Kubernetes Secrets in a namespace that are structured as Docker configuration files (`type=kubernetes.io/dockerconfigjson`) and extract the registry URLs they authenticate against. This is used by the kubelet during pod scheduling.

---

### 🌍 Execution Context

Run from:

- [x] Local machine (with context)

---

### ⚡ Action

```bash
kubectl get secrets -n <NAMESPACE> --field-selector type=kubernetes.io/dockerconfigjson -o json | \
  jq '.items[] | {name: .metadata.name, registry: (.data[".dockerconfigjson"] | @base64d | fromjson | .auths | keys[])}'
```

#### Placeholders

- `<NAMESPACE>`—The Kubernetes namespace (e.g., `argocd` or `ff-hie-test-34`)

---

### ✅ Verification

- Expected Output: A stream of JSON objects containing the secret `name` and the `registry` domain it supports.

### 💥 Failure Mode Analysis

- Symptom: Your pods are failing with `ImagePullBackOff` but the secret exists.
  - Fix: Check if the secret's `registry` URL exactly matches the image path in the deployment. If they do match, proceed to [[cmd_kubectl_get_image_pull_secret_creds]] to verify the username/password.

---

### 🔗 Related

- [[cmd_kubectl_get_image_pull_secret_creds]]
- [[cmd_kubectl_argocd_find_repo_secrets]]
