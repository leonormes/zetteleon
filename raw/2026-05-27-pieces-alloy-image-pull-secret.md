---
created: 2026-05-27T00:00:00+00:00
modified: 2026-07-20T16:33:00+00:00
permalink: llmeon/raw/2026-05-27-pieces-alloy-image-pull-secret
pieces_ids: [197fa585-493b-4385-b7fd-ade194efe574, 22e8d732-027b-4357-8f4a-2497823a02dd, 36150679-1ce5-4182-b38d-c6c20236e8bf, 4f40a613-2281-4d8c-8ea1-c206cdf30cdb, 98a0aea4-ba8f-4161-b6ae-ff08d93dea69]
source: pieces-ltm
tags: [alloy, fitfile, grafana, kubernetes, monitoring, pieces, raw]
title: 2026-05-27-pieces-alloy-image-pull-secret
---

## Fitfile-image-pull-secret Missing—Alloy Logging Namespace Issue

### Asset 1 (Pieces: 98a0aea4-ba8f-4161-b6ae-ff08d93dea69)

Captured: 2026-05-27T10:41:28Z

User request: validate hermes output

Full Diagnosis—How the secret is supposed to work:

1. Terraform (vault_operator/main.tf) creates a VaultDynamicSecret named fitfile-image-pull in the argocd namespace
2. Vault Secrets Operator (VSO) reads creds/acr-pull from Vault and creates a fitfile-image-pull-secret (type: kubernetes.io/dockerconfigjson) in argocd
3. Reflector auto-replicates it to all namespaces listed in namespaces_for_image_pull_secret
4. kubernetes_default_service_account_v1 injects imagePullSecrets to pods

### Asset 2 (Pieces: 197fa585-493b-4385-b7fd-ade194efe574)

Captured: 2026-05-27T10:13:29Z

Two problems identified:

#### Problem 1—Wrong Secret name

The secret created is named `argocd-acr-pull-secret` in `monitoring`. The alloy-logs DaemonSet is looking for `fitfile-image-pull-secret`. Kubernetes imagePullSecrets must match by name exactly.

#### Problem 2—Wrong Secret Type

What was copied is an ArgoCD Helm OCI repository credential (type Opaque, fields name/url/username/password/type/enableOCI). Kubernetes imagePullSecrets need to be type kubernetes.io/dockerconfigjson with a.dockerconfigjson data key.

Correct approach: replicate the actual `fitfile-image-pull-secret` from argocd to monitoring, not the ArgoCD repo credential.

### Asset 3 (Pieces: 4f40a613-2281-4d8d-8ea1-c206cdf30cdb)

Captured: 2026-05-27T10:12:23Z

kubectl output showing wrong secret type in argocd:

```json
{
    "apiVersion": "v1",
    "data": {
        "ForceHttpBasicAuth": "dHJ1ZQ==",
        "_raw": "eyJjbG...",
        "enableOCI": "dHJ1ZQ==",
        "name": "Zml0ZmlsZXJlZ2lzdHJ5",
        "password": "TjRnOF..."
    }
}
```

Encoding: `Zml0ZmlsZXJlZ2lzdHJ5` = "fitfileregistry"

### Asset 4 (Pieces: 22e8d732-027b-4357-8f4a-2497823a02dd)

Captured: 2026-05-27T09:38:06Z

Root cause & fix: `fitfile-image-pull-secret` missing from `monitoring` namespace

This is a known recurring issue. Memory has at least three prior occurrences:

- Jan 22 2026
- Mar 27 2026
- May 5 2026

All producing the same `FailedToRetrieveImagePullSecret` pattern. The current occurrence is the latest in this pattern.

### Asset 5 (Pieces: 36150679-1ce5-4182-b38d-c6c20236e8bf)

Captured: 2026-05-27T09:34:46Z

Alloy-logs DaemonSet pods cannot restart to pick up new config. All three pods hitting `FailedToRetrieveImagePullSecret`:

- `alloy-logs-x8t45`—167 occurrences
- `alloy-logs-tbnz9`—212 occurrences
- `alloy-logs-hl9v2`—213 occurrences

The Alloy operator re…
