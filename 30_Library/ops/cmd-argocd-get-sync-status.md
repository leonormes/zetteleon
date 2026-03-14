---
aliases: ["argocd app status", "check argocd sync", "is my app synced"]
cloud: agnostic
created: 2026-02-14T00:00:00+00:00
hop_level: bastion
k8s_version: "1.29"
last_verified: 2026-02-14
modified: 2026-03-14T11:10:11+00:00
namespace: argocd
status: verified
tags: [cmd, deployment, incident]
target_service: argocd-server
title: cmd-argocd-get-sync-status
tool: argocd
---

## Purpose

> Shows the current sync and health status of an ArgoCD Application, including which commit it's tracking and whether it's drifted from the desired state.

## Prerequisites

> [!warning] Execution Context: `bastion`
> This command must be run from: bastion host with ArgoCD CLI authenticated.

| # | Prerequisite | Link |
|---|-------------|------|
| 1 | SSH tunnel to bastion | [[establish-ssh-tunnel]] |
| 2 | ArgoCD CLI login | [[argocd-cli-login]] |
| 3 | Correct ArgoCD context | [[set-argocd-context]] |

## Command

```sh
# ── Get sync + health status for a specific application ──
argocd app get <APP_NAME> \
  --server <ARGOCD_SERVER_URL> \
  --grpc-web
```

### Placeholders

| Placeholder           | Description                 | Example                       |
| --------------------- | --------------------------- | ----------------------------- |
| `<APP_NAME>`          | The ArgoCD Application name | `platform-api-prod`           |
| `<ARGOCD_SERVER_URL>` | ArgoCD server endpoint      | `argocd.internal.example.com` |

## Verification

> How do you know it worked?

```shell
# ── Verify: sync status is 'Synced' and health is 'Healthy' ──
argocd app get <APP_NAME> \
  --server <ARGOCD_SERVER_URL> \
  --grpc-web \
  -o json | jq '{sync: .status.sync.status, health: .status.health.status, revision: .status.sync.revision}'
```

Expected output pattern:

```json
{
  "sync": "Synced",
  "health": "Healthy",
  "revision": "a1b2c3d4e5f6..."
}
```

> [!fail] Failure Signature
> If you see `sync: "OutOfSync"`, the live state has drifted from Git. See [[argocd-diff-app]].
> If you see `health: "Degraded"`, one or more resources failed. See [[get-argocd-app-resources]].

## Context & Why

ArgoCD reconciles desired state (Git) with live state (cluster). `app get` is the first command in any ArgoCD debugging flow because it tells you two orthogonal things: whether Git and the cluster agree (sync), and whether the resources are actually functioning (health). These can fail independently—an app can be `Synced` but `Degraded` if the manifest applied cleanly but the pod is crash-looping.

## Related

- Next step → [[argocd-diff-app]] (if OutOfSync)
- Next step → [[get-argocd-app-resources]] (if Degraded)
- Rollback → [[argocd-rollback-app]]
- Playbook → [[playbook-argocd-sync-failure-triage]]
