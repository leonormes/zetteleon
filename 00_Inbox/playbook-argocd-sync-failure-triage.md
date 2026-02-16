---
aliases: ["app won't sync", "argocd outOfSync", "argocd sync stuck", "deployment not rolling out"]
cloud: agnostic
created: 2026-02-14T00:00:00+00:00
domain: deployment
estimated_time: "15m"
last_verified: 2026-02-14
modified: 2026-02-16T09:40:49+00:00
status: verified
tags: [deployment, incident, playbook]
title: playbook-argocd-sync-failure-triage
trigger: "ArgoCD Application shows OutOfSync or sync operation fails"
---

## Trigger Condition

> When do you reach for this playbook?
> An ArgoCD Application is stuck in `OutOfSync`, a sync operation returns an error, or a deployment isn't rolling out despite a merged PR.

## Typical Alert or Observation

Application 'platform-api-prod' sync status is 'OutOfSync'

## Or

ComparisonError: failed to compare: …

### Decision Context

> [!info] Before You Start
> - Execution origin: `bastion` (ArgoCD CLI + kubectl access required)
> - Required access: ArgoCD CLI auth, kubeconfig for target cluster
> - Blast radius: Phases 1–2 are read-only. Phase 3 is mutating (forces sync or hard-refresh).

### Flow

#### Phase 1: Orient

> _Goal: Confirm the problem is real and understand what ArgoCD sees._

- [ ] Step 1 → [[get-argocd-app-sync-status]]
      _Why:_ Establishes baseline—is it truly OutOfSync, and what's the health status?
- [ ] Step 2 → [[argocd-diff-app]]
      _Why:_ Shows the exact delta between Git desired state and live cluster state. This is the single most informative command.

> [!question] Decision Point
> - If diff shows expected resource changes (e.g., new image tag) → The sync just hasn't run. Go to Phase 3.
> - If diff shows unexpected resources or fields you didn't change → Someone or something mutated the cluster directly. Go to Phase 2.
> - If diff errors with `ComparisonError` → The manifest is invalid or a CRD is missing. Go to Phase 2, Step 4.

#### Phase 2: Diagnose

> _Goal: Identify why the sync can't or won't complete._

- [ ] Step 3 → [[get-argocd-app-resources]]
      _Why:_ Lists every resource managed by this app and its individual sync/health status. Look for resources stuck in `Progressing` or `Unknown`.
- [ ] Step 4 → [[get-argocd-app-sync-errors]]
      _Why:_ Surfaces the actual error message from the last sync attempt (e.g., admission webhook denied, immutable field changed, quota exceeded).
- [ ] Step 5 → [[kubectl-get-events-namespace]]
      _Why:_ Kubernetes Events often contain the real error (image pull failures, scheduling constraints, OOM kills) that ArgoCD surfaces only as `Degraded`.

> [!question] Decision Point
> - If sync error is `admission webhook denied` → See [[troubleshoot-webhook-blocking-sync]]
> - If sync error is `immutable field` → You need to delete and recreate the resource. See [[argocd-replace-resource]]
> - If events show `ImagePullBackOff` → Image doesn't exist or registry auth is broken. See [[troubleshoot-image-pull]]
> - If events show `FailedScheduling` → Node resources exhausted. See [[check-node-capacity]]

#### Phase 3: Act

> _Goal: Unblock the sync._

> [!danger] Mutating Step—Confirm Context
> Run `kubectl config current-context` before proceeding.
> Expected: `<your-target-cluster-context>`

- [ ] Step 6a (if clean diff, just stale) → [[argocd-sync-app]]
      _Why:_ Triggers a manual sync. Use `--prune` only if you're certain removed resources should be deleted.
- [ ] Step 6b (if ArgoCD cache is stale) → [[argocd-hard-refresh-app]]
      _Why:_ Forces ArgoCD to re-read from Git and re-compare. Solves phantom drifts caused by cache staleness.
- [ ] Step 7 (Verify) → [[get-argocd-app-sync-status]]
      _Why:_ Confirms sync status is now `Synced` and health is `Healthy`.

#### Phase 4: Confirm & Close

- [ ] Step 8 → [[kubectl-get-pods-wide]]
      _Why:_ Confirms pods are running, on expected nodes, and not restarting.
- [ ] Step 9 → [[curl-health-endpoint]]
      _Why:_ End-to-end smoke test—hit the actual service endpoint to confirm it's serving traffic.

> [!success] Resolution Criteria
> The playbook is complete when:
> - ArgoCD shows `Synced` + `Healthy`
> - All pods are `Running` with 0 restarts in the last 5 minutes
> - Health endpoint returns 200

### Rollback

> If the forced sync in Phase 3 made things worse:

- [ ] Rollback Step 1 → [[argocd-rollback-app]]
      _Why:_ Reverts to the previous successfully synced revision.
- [ ] Rollback Step 2 → [[get-argocd-app-sync-status]]
      _Why:_ Verify the rollback landed cleanly.

### Post-Incident

- [ ] Update `last_verified` date on all Atomic Commands used
- [ ] If any command syntax changed, update the Atomic Command note
- [ ] If a new failure mode was discovered, create a new Atomic Command note
- [ ] Link this playbook run to your incident ticket: `<TICKET-ID>`

### Appendix: Related Playbooks

| Playbook | When to Use Instead |
|----------|-------------------|
| [[playbook-argocd-app-degraded-healthy-sync]] | App is `Synced` but `Degraded`—the manifest applied but resources are unhealthy |
| [[playbook-argocd-permission-denied]] | Sync fails with RBAC/permission errors |
| [[playbook-helm-values-drift]] | Helm values in Git don't match what ArgoCD rendered |
