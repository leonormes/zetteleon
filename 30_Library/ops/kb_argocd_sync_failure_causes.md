---
created: 2026-02-21T15:05:08+00:00
modified: 2026-07-13T08:45:29+00:00
permalink: llmeon/30-library/ops/kb-argocd-sync-failure-causes
service: argocd
tags: [knowledge, triage, troubleshooting]
title: kb_argocd_sync_failure_causes
type: sot
---

## KB: ArgoCD Sync Failure Causes

### Mental Model: The Triage Tree

Sync failures usually fall into three categories:

1. Manifest Issues (The "Wait" Phase)
	- _ComparisonError_: Git contains invalid YAML/Kustomize/Helm.
	- _Admission Webhook_: The cluster rejected the valid manifest (e.g., OPA/Kyverno policy).
2. Cluster Drift (The "Diff" Phase)
	- _Unexpected Diff_: External controller (e.g., HPA, Vault Sidecar) is fighting ArgoCD over a field.
	- _Immutable Fields_: Trying to change a field (like `spec.selector`) that K8s doesn't allow updating without deletion.
3. Runtime Health (The "Degraded" Phase)
	- _ImagePullBackOff_: Registry auth or missing tag.
	- _OOMKilled/CrashLoop_: Application logic or resource limits.

### Decision Rules

- Diff is clean but status is OutOfSync? Force a `Hard Refresh`.
- Sync succeeds but app is Degraded? Shift focus from ArgoCD to `kubectl events`.
- ComparisonError? Run your rendering tool locally (`helm template` or `kustomize build`).
