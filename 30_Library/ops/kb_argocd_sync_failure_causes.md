---
type: sot
service: argocd
tags: [triage, troubleshooting, knowledge]
---

# KB: ArgoCD Sync Failure Causes

## Mental Model: The Triage Tree
Sync failures usually fall into three categories:

1. **Manifest Issues (The "Wait" Phase)**
	- *ComparisonError*: Git contains invalid YAML/Kustomize/Helm.
	- *Admission Webhook*: The cluster rejected the valid manifest (e.g., OPA/Kyverno policy).
2. **Cluster Drift (The "Diff" Phase)**
	- *Unexpected Diff*: External controller (e.g., HPA, Vault Sidecar) is fighting ArgoCD over a field.
	- *Immutable Fields*: Trying to change a field (like `spec.selector`) that K8s doesn't allow updating without deletion.
3. **Runtime Health (The "Degraded" Phase)**
	- *ImagePullBackOff*: Registry auth or missing tag.
	- *OOMKilled/CrashLoop*: Application logic or resource limits.

## Decision Rules
- **Diff is clean but status is OutOfSync?** Force a `Hard Refresh`.
- **Sync succeeds but app is Degraded?** Shift focus from ArgoCD to `kubectl events`.
- **ComparisonError?** Run your rendering tool locally (`helm template` or `kustomize build`).
