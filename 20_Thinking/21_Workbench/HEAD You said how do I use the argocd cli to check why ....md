---
captured: "2026-03-07T16:50:50+00:00 2026-03-07T16:50:50+00:00"
created: 2026-03-07T16:50:51+00:00
modified: 2026-03-14T11:10:31+00:00
source: "https://gemini.google.com/app/a8d8201b525b1794"
status: "processing"
tags: ["input"]
title: HEAD You said how do I use the argocd cli to check why ...
type: "head"
---

## Raw Output / Content

how do I use the argocd cli to check why this says outof sync

argocd/thehyve <https://kubernetes.default.svc> thehyve fitfile OutOfSync Healthy Auto-Prune SyncError <https://gitlab.com/fitfile/deployment.git> charts/integrations/thehyve eoe-test-release

---

When an Argo CD application shows as OutOfSync, it means there is a discrepancy between the desired state defined in your Git repository and the live state of the resources in your Kubernetes cluster.

To diagnose this using the Argo CD CLI, you can follow these steps to identify the specific differences and the reasons behind the sync error.

---

### 1\. View the Application Summary

First, get a detailed overview of the application status. This will confirm which specific resources are causing the `OutOfSync` or `SyncError` status.

Look for the Type, Name, and Status columns in the output. Resources marked as `OutOfSync` are the culprits.

### 2\. Check the Diff

To see exactly what has changed (e.g., a modified environment variable, a different image tag, or a missing label), use the `diff` command. This compares your Git manifest against the live cluster.

- Lines with `-` (Red): These exist in the cluster but are missing from Git (or are being changed).
- Lines with `+` (Green): These are in your Git repository but have not been applied to the cluster yet.

### 3\. Inspect Sync Errors

Since your output mentions a `SyncError`, there might be an issue preventing Argo CD from even attempting the sync (like a manifest syntax error or a permission issue). You can check the recent results and error messages with:

This provides details on the last sync attempt, including the specific error message that triggered the `SyncError` flag.

### 4\. Check Resource Health & Events

If the diff doesn't explain everything, you can look at the resource-level events. This is helpful if a hook is failing or a controller is rejecting the manifest.

---

### Common Reasons for "OutOfSync"

- Manual Changes: Someone edited a resource directly in the cluster using `kubectl`.
- Admission Controllers: A tool like Kyverno or a Mutating Admission Webhook is changing the resource after Argo CD applies it.
- Invalid Manifests: The Helm chart in `charts/integrations/thehyve` might be generating invalid YAML that Kubernetes is rejecting.
- Parameter Mismatch: The parameters defined in the Argo CD App manifest (like `eoe-test-release`) might not match what the Helm chart expects.

### Next Steps

Once you have identified the difference using `argocd app diff`, you can choose to:

1. Sync manually:`argocd app sync argocd/thehyve` (this will attempt to overwrite the live state with the Git state).
2. Update Git: Change your code in the GitLab repository to match the desired live state.

Would you like me to help you interpret the output of the `argocd app diff` command once you've run it?

---

I did just change the disc size for the postgress

argocd app get argocd/thehyve

{"execID":"6f92a","level":"error","msg":"\`helm version --client --short\` failed exit status 1: Error: unknown flag: --client","time":"2026-02-20T15:42:31Z"}

{"execID":"8790c","level":"error","msg":"\`helm version --client --short\` failed exit status 1: Error: unknown flag: --client","time":"2026-02-20T15:42:31Z"}

Name: argocd/thehyve

Project: fitfile

Server: <https://kubernetes.default.svc>

Namespace: thehyve

URL: <https://argocd.eoe-test-codisc.privatelink.fitfile.net/applications/thehyve>

Source:

\- Repo: <https://gitlab.com/fitfile/deployment.git>

Target: eoe-test-release

Path: charts/integrations/thehyve

Helm Values: /ffnodes/eoe/hie-test-34/thehyve\_values.yaml

SyncWindow: Sync Allowed

Sync Policy: Automated (Prune)

Sync Status: OutOfSync from eoe-test-release (a311b5c)

Health Status: Healthy

CONDITION MESSAGE LAST TRANSITION

SyncError Failed sync attempt to a311b5c764b20e6c7099c140812891f06c14a21a: one or more objects failed to apply, reason: error when patching "/dev/shm/1599540288": StatefulSet.apps "thehyve-postgresql" is invalid: spec: Forbidden: updates to statefulset spec for fields other than 'replicas', 'ordinals', 'template', 'updateStrategy', 'revisionHistoryLimit', 'persistentVolumeClaimRetentionPolicy' and 'minReadySeconds' are forbidden (retried 5 times). 2026-02-20 13:50:23 +0000 UTC

GROUP KIND NAMESPACE NAME STATUS HEALTH HOOK MESSAGE

networking.k8s.io NetworkPolicy thehyve thehyve-postgresql Synced networkpolicy.networking.k8s.io/thehyve-postgresql configured

policy PodDisruptionBudget thehyve thehyve-postgresql Synced Healthy poddisruptionbudget.policy/thehyve-postgresql configured

ServiceAccount thehyve thehyve-postgresql Synced serviceaccount/thehyve-postgresql unchanged

ServiceAccount thehyve thehyve Synced serviceaccount/thehyve unchanged

PersistentVolumeClaim thehyve thehyve-reports Synced Healthy persistentvolumeclaim/thehyve-reports unchanged

Service thehyve thehyve-postgresql-hl Synced Healthy service/thehyve-postgresql-hl unchanged

Service thehyve thehyve Synced Healthy service/thehyve unchanged

Service thehyve thehyve-postgresql Synced Healthy service/thehyve-postgresql configured

apps Deployment thehyve thehyve Synced Healthy deployment.apps/thehyve unchanged

apps StatefulSet thehyve thehyve-postgresql OutOfSync Healthy error when patching "/dev/shm/1599540288": StatefulSet.apps "thehyve-postgresql" is invalid: spec: Forbidden: updates to statefulset spec for fields other than 'replicas', 'ordinals', 'template', 'updateStrategy', 'revisionHistoryLimit', 'persistentVolumeClaimRetentionPolicy' and 'minReadySeconds' are forbidden

secrets.hashicorp.com VaultStaticSecret thehyve thehyve Synced vaultstaticsecret.secrets.hashicorp.com/thehyve unchanged

secrets.hashicorp.com VaultStaticSecret thehyve thehyve-postgresql Synced vaultstaticsecret.secrets.hashicorp.com/thehyve-postgresql unchanged

secrets.hashicorp.com VaultStaticSecret thehyve thehyve-postgresql-init-db Synced vaultstaticsecret.secrets.hashicorp.com/thehyve-postgresql-init-db unchanged

awsadmin@ip-10-66-2-4:~/terraform$ argocd app diff argocd/thehyve

{"execID":"3f92a","level":"error","msg":"\`helm version --client --short\` failed exit status 1: Error: unknown flag: --client","time":"2026-02-20T15:42:48Z"}

{"execID":"36cdd","level":"error","msg":"\`helm version --client --short\` failed exit status 1: Error: unknown flag: --client","time":"2026-02-20T15:42:49Z"}

\===== apps/StatefulSet thehyve/thehyve-postgresql ======

283d282

< creationTimestamp: null

434d432

< creationTimestamp: null

441c439

< storage: 32Gi

\---

\> storage: 64Gi

awsadmin@ip-10-66-2-4:~/terraform$ argocd app get argocd/thehyve --show-operation

{"execID":"0a5aa","level":"error","msg":"\`helm version --client --short\` failed exit status 1: Error: unknown flag: --client","time":"2026-02-20T15:43:01Z"}

{"execID":"a7659","level":"error","msg":"\`helm version --client --short\` failed exit status 1: Error: unknown flag: --client","time":"2026-02-20T15:43:02Z"}

Name: argocd/thehyve

Project: fitfile

Server: <https://kubernetes.default.svc>

Namespace: thehyve

URL: <https://argocd.eoe-test-codisc.privatelink.fitfile.net/applications/thehyve>

Source:

\- Repo: <https://gitlab.com/fitfile/deployment.git>

Target: eoe-test-release

Path: charts/integrations/thehyve

Helm Values: /ffnodes/eoe/hie-test-34/thehyve\_values.yaml

SyncWindow: Sync Allowed

Sync Policy: Automated (Prune)

Sync Status: OutOfSync from eoe-test-release (a311b5c)

Health Status: Healthy

CONDITION MESSAGE LAST TRANSITION

SyncError Failed sync attempt to a311b5c764b20e6c7099c140812891f06c14a21a: one or more objects failed to apply, reason: error when patching "/dev/shm/1599540288": StatefulSet.apps "thehyve-postgresql" is invalid: spec: Forbidden: updates to statefulset spec for fields other than 'replicas', 'ordinals', 'template', 'updateStrategy', 'revisionHistoryLimit', 'persistentVolumeClaimRetentionPolicy' and 'minReadySeconds' are forbidden (retried 5 times). 2026-02-20 13:50:23 +0000 UTC

Operation: Sync

Sync Revision: a311b5c764b20e6c7099c140812891f06c14a21a

Phase: Failed

Start: 2026-02-20 13:45:07 +0000 UTC

Finished: 2026-02-20 13:50:23 +0000 UTC

Duration: 5m16s

Message: one or more objects failed to apply, reason: error when patching "/dev/shm/1599540288": StatefulSet.apps "thehyve-postgresql" is invalid: spec: Forbidden: updates to statefulset spec for fields other than 'replicas', 'ordinals', 'template', 'updateStrategy', 'revisionHistoryLimit', 'persistentVolumeClaimRetentionPolicy' and 'minReadySeconds' are forbidden (retried 5 times).

GROUP KIND NAMESPACE NAME STATUS HEALTH HOOK MESSAGE

networking.k8s.io NetworkPolicy thehyve thehyve-postgresql Synced networkpolicy.networking.k8s.io/thehyve-postgresql configured

policy PodDisruptionBudget thehyve thehyve-postgresql Synced Healthy poddisruptionbudget.policy/thehyve-postgresql configured

ServiceAccount thehyve thehyve-postgresql Synced serviceaccount/thehyve-postgresql unchanged

ServiceAccount thehyve thehyve Synced serviceaccount/thehyve unchanged

PersistentVolumeClaim thehyve thehyve-reports Synced Healthy persistentvolumeclaim/thehyve-reports unchanged

Service thehyve thehyve-postgresql-hl Synced Healthy service/thehyve-postgresql-hl unchanged

Service thehyve thehyve Synced Healthy service/thehyve unchanged

Service thehyve thehyve-postgresql Synced Healthy service/thehyve-postgresql configured

apps Deployment thehyve thehyve Synced Healthy deployment.apps/thehyve unchanged

apps StatefulSet thehyve thehyve-postgresql OutOfSync Healthy error when patching "/dev/shm/1599540288": StatefulSet.apps "thehyve-postgresql" is invalid: spec: Forbidden: updates to statefulset spec for fields other than 'replicas', 'ordinals', 'template', 'updateStrategy', 'revisionHistoryLimit', 'persistentVolumeClaimRetentionPolicy' and 'minReadySeconds' are forbidden

secrets.hashicorp.com VaultStaticSecret thehyve thehyve Synced vaultstaticsecret.secrets.hashicorp.com/thehyve unchanged

secrets.hashicorp.com VaultStaticSecret thehyve thehyve-postgresql Synced vaultstaticsecret.secrets.hashicorp.com/thehyve-postgresql unchanged

secrets.hashicorp.com VaultStaticSecret thehyve thehyve-postgresql-init-db Synced vaultstaticsecret.secrets.hashicorp.com/thehyve-postgresql-init-db unchanged

awsadmin@ip-10-66-2-4:~/terraform$ argocd app resources argocd/thehyve

{"execID":"3f3a6","level":"error","msg":"\`helm version --client --short\` failed exit status 1: Error: unknown flag: --client","time":"2026-02-20T15:43:22Z"}

GROUP KIND NAMESPACE NAME ORPHANED

PersistentVolumeClaim thehyve thehyve-reports No

Service thehyve thehyve No

Service thehyve thehyve-postgresql No

Service thehyve thehyve-postgresql-hl No

ServiceAccount thehyve thehyve No

ServiceAccount thehyve thehyve-postgresql No

apps Deployment thehyve thehyve No

apps StatefulSet thehyve thehyve-postgresql No

networking.k8s.io NetworkPolicy thehyve thehyve-postgresql No

policy PodDisruptionBudget thehyve thehyve-postgresql No

secrets.hashicorp.com VaultStaticSecret thehyve thehyve No

secrets.hashicorp.com VaultStaticSecret thehyve thehyve-postgresql No

secrets.hashicorp.com VaultStaticSecret thehyve thehyve-postgresql-init-db No

---

The output confirms exactly what is happening: you have hit a fundamental Kubernetes restriction regarding StatefulSets.

### The Problem

You modified the disk size for your PostgreSQL instance from `32Gi` to `64Gi` in your Helm values. However, Kubernetes does not allow updates to the `volumeClaimTemplates` field of an existing StatefulSet.

As the error message states:

> `spec: Forbidden: updates to statefulset spec for fields other than 'replicas', 'ordinals', 'template', 'updateStrategy', 'revisionHistoryLimit', 'persistentVolumeClaimRetentionPolicy' and 'minReadySeconds' are forbidden`

Because the storage request is inside the `volumeClaimTemplates` (which defines how the PVC is created), Kubernetes rejects the patch, and Argo CD remains `OutOfSync` because it cannot apply the change.

---

### How to Fix It

You have two main paths depending on whether you can afford a brief period of downtime.

#### Option A: The "Delete and Recreate" (Easiest)

Since the `OutOfSync` status is on the StatefulSet object itself, you can delete the StatefulSet without deleting your data. Kubernetes will then allow Argo CD to recreate the StatefulSet with the new configuration.

1. Delete the StatefulSet only (keep the pods/PVCs for a moment):
2. Manually expand the PVC: Kubernetes won't automatically resize the existing disk just because you changed the StatefulSet template. You must update the PVC directly:
3. Sync Argo CD:
	Argo CD will see the StatefulSet is missing and recreate it with the `64Gi` definition.

---

#### Option B: The "Argo CD Replace"

You can tell Argo CD to use a "replace" strategy instead of a "patch" strategy. This will essentially do the delete-and-recreate for you.

_Note: This might still fail if the underlying Persistent Volume Claim (PVC) isn't resized first, as the new Pods might try to claim 64Gi while the existing PVC is still 32Gi._

---

### A Note on the Helm Error

You might have noticed this in your logs:`"msg":"helm version --client --short failed exit status 1: Error: unknown flag: --client"`

This is a common compatibility issue between the Argo CD CLI version and the Helm version installed on your local machine (Helm v3 removed the `--client` flag). It isn't causing your sync failure, but it makes the CLI output look messy. You can usually ignore it, or update your Argo CD CLI to a more recent version to resolve the warning.

Would you like me to help you find the exact name of the Persistent Volume Claim (PVC) to patch?
