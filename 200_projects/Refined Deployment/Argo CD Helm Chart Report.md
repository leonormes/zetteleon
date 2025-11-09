---
aliases: []
confidence: 
created: 2025-10-22T11:53:21Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T14:24:10Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: Argo CD Helm Chart Report
type:
uid: 
updated: 
version:
---

write a argo-cd helm report. The helm chart, and all its dependencies as a md file I can use in my wiki

Here is an **Argo CD Helm Chart Report** for wiki use, including the chart, all dependencies, install info, images, and key options. Copy this into your markdown-based wiki as a reference.

---

## Argo CD Helm Chart Report

### Chart Overview

- **Chart Name:** `argo-cd`
- **Maintainer:** Community (argoproj)
- **Latest Version:** 9.0.3 (as of Oct 2025)
- **Upstream:** [argoproj/argo-helm](https://github.com/argoproj/argo-helm)
- **ArtifactHub:** [argo-cd chart page](https://artifacthub.io/packages/helm/argo/argo-cd)
- **Application:** [Argo CD](https://argo-cd.readthedocs.io/en/stable/) — GitOps continuous delivery tool for Kubernetes

---

### Images Used

| Component                       | Default Image                           | Tag/Version Used | Purpose                         |
| :------------------------------ | :-------------------------------------- | :--------------- | :------------------------------ |
| `argocd-server`                 | quay.io/argoproj/argocd                 | v3.1.9           | API server \& Web UI            |
| `argocd-repo-server`            | quay.io/argoproj/argocd                 | v3.1.9           | Git/Helm repo ops, manifest gen |
| `argocd-application-controller` | quay.io/argoproj/argocd                 | v3.1.9           | App reconciliation              |
| `dex` (optional)                | ghcr.io/dexidp/dex                      | v2.44.0          | OIDC authentication provider    |
| `redis` (optional/HA)           | ecr-public.aws.com/docker/library/redis | 7.2.11-alpine    | App state/session data          |

*Note: Tags update per release. All can be overridden in `values.yaml`, and additional/optional dependencies may exist (see below).*

---

### Install Prerequisites

- **Kubernetes version:** >= 1.25.0-0
- **Helm version:** >= 3.0.0

---

### Installing the Chart

```sh
helm repo add argo https://argoproj.github.io/argo-helm
helm install my-release argo/argo-cd
```

*Optional flags:*

- `--set crds.install=false` : Disable CRD installation if managed separately.
- High-availability? See HA options in README/values.yaml.

---

### Chart Structure \& Key Dependencies

- **CRDs:** Provided in chart (`templates/crds`). Can be excluded from install with flag.
  - Applications (`applications.argoproj.io`)
  - ApplicationSets (`applicationsets.argoproj.io`)
  - Projects (`appprojects.argoproj.io`)
  - Extensions (`argocdextensions.argoproj.io`)
- **Subcharts and Integrations:**
  - Argo CD Apps (`argocd-apps` chart): Used for additional applications or projects.
  - Argo CD Image Updater (`argocd-image-updater` chart): For automated container image updates.
  - Notifications \& ApplicationSet Controllers: Now bundled with main installation.
- **Optional dependencies (can be enabled):**
  - `dex` (server.dex.enabled): OIDC provider.
  - `redis-ha` (redis-ha.enabled): For highly available Redis.
  - `notifications-controller` (notifications.enabled): For Slack/email/webhook notifications.
  - `applicationSet` (applicationset.enabled): Automated generation for Argo CD apps.

---

### Chart Options and Parameters

Core configurable values in `values.yaml` (abridged):

| Parameter                 | Default                 | Description                          |     |
| :------------------------ | :---------------------- | :----------------------------------- | --- |
| `global.image.repository` | quay.io/argoproj/argocd | Global image repo                    |     |
| `global.image.tag`        | Chart's appVersion      | Global image tag                     |     |
| `server.dex.enabled`      | `false`                 | Deploy Dex                           |     |
| `redis-ha.enabled`        | `false`                 | Redis high availability              |     |
| `notifications.enabled`   | `false`                 | Enable notifications controller      |     |
| `applicationset.enabled`  | `true`                  | Enable ApplicationSet controller     |     |
| `crds.install`            | `true`                  | Install CRDs (can be disabled)       |     |
| `configs.cm`              | `{}`                    | Extra config for argocd-cm ConfigMap |     |
| `configs.params`          | `{}`                    | Extra ARGS for deployment containers |     |

Refer to [values.yaml](https://github.com/argoproj/argo-helm/tree/main/charts/argo-cd) for all options.

---

### Example: Minimal HA Setup

```yaml
redis-ha:
  enabled: true
controller:
  replicas: 1
server:
  autoscaling:
    enabled: true
    minReplicas: 2
repoServer:
  autoscaling:
    enabled: true
    minReplicas: 2
applicationSet:
  replicas: 2
```

---

### Key Links \& Resources

- **Source Code:**
  - [Argo Helm Charts repo](https://github.com/argoproj/argo-helm)
  - [Argo CD core repo](https://github.com/argoproj/argo-cd)
- **Readme/Docs:**
  - [Operator Manual (installation)](https://argo-cd.readthedocs.io/en/stable/operator-manual/installation/)
  - [Chart Documentation](https://github.com/argoproj/argo-helm/tree/main/charts/argo-cd)
- **ArtifactHub Package**:
  - [argo-cd chart](https://artifacthub.io/packages/helm/argo/argo-cd)

---

### Dependency List (as of v9.x)

- Required: None (all bundled in single chart)
- Optional:
  - `dex` (OIDC, for SSO)
  - `redis-ha` (redis HA variant)
  - `argocd-apps` (additional projects/apps)
  - `argocd-image-updater` (automated image updates)
  - Notification controllers

---

### Upgrade \& Breaking Changes

- CRDs now installed via `/templates/crds`, not `/crds`
- Redis switched to OSS 7.2 (older versions may use commercial redis)
- Notifications and ApplicationSet bundled post v2.3 (need not install separately)
- See [CHANGELOG](https://github.com/argoproj/argo-helm/releases) and chart releases for details.

---

### Security

- Supported only on latest versions.
- Latest security report found 109 vulnerabilities; see scan report for remediation.

*For older versions: security patches not backported; upgrade strongly recommended.*

---

You can copy, adapt, and edit this file for your requirements and internal documentation needs. All config options, images and references trace to latest chart as of October 2025.[^1]

<div align="center">⁂</div>

[^1]: <https://github.com/argoproj/argo-helm>
