---
created: 2026-07-30
date: 2026-07-30
jira-assignee: Leon Ormes
jira-key: FTFL-722
jira-parent: FTFL-691
jira-reporter: Robin Mofakham
jira-status: In Progress
project: FITFILE
source: investigation
tags:
- aws
- ebs
- eks
- ftfl
- gp2
- gp3
- k8s
- storage
- codisc
title: FTFL-722 - GP2 to GP3 Migration — TEST Cluster PVC Inventory
permalink: llmeon/jira/ftfl-722-gp2-to-gp3-migration-test-cluster-pvc-inventory
---

## FTFL-722 — Upgrade disks from GP2 to GP3 (TEST cluster: `eoe-test-codisc`)

Parent: [[FTFL-691]] (EoE SLA Inbox: Low effort) · Sibling ticket for cleanup: FTFL-724 (Identify disk usage and make recommendation for action)

Account: `135808916559` · Region: `eu-west-2` · Cluster: `eoe-test-codisc` (TEST — do this one first per ticket instruction, before `eoe-sde-codisc`/PROD)

Source data: Compute Optimizer recommendations CSV (`eoe-sde-codisc-COH-recommendations-2026-06-05.csv`, exported from the codisc AWS account — stale, cross-checked live against AWS/kubectl below), Jira [FTFL-722](https://fitfile.atlassian.net/browse/FTFL-722), [FTFL-691](https://fitfile.atlassian.net/browse/FTFL-691).

---

### Summary

TEST has **16 gp2 volumes**, all `Bound` PVs, all still gp2 as of today. All 16 should be upgraded in-place to gp3 — none should be deleted, despite the source CSV recommending deletion for some of them. AWS's in-place `modify-volume` API changes the type with zero downtime and no Kubernetes object edits, and this account has already done it twice for size (not type) changes without issue, so the mechanism is proven safe here.

A new `gp3` StorageClass should also be created and made cluster default, so future PVCs (new instances, or existing StatefulSets if ever recreated) stop defaulting to gp2. No Helm chart edits are needed for that part — every StatefulSet's `volumeClaimTemplates` already omits `storageClassName`, so they inherit whatever the cluster default is.

---

### Cluster-wide resource (one-off, do first)

| Resource | Action | Why |
|---|---|---|
| StorageClass `gp2` (provisioner `kubernetes.io/aws-ebs`, default: true) | Create new `gp3` StorageClass, remove `is-default-class` from `gp2`, set it on `gp3` | New PVCs should stop being created as gp2. Confirmed no chart changes needed elsewhere — see StatefulSet note below. |
| New StorageClass provisioner choice | Use `ebs.csi.aws.com` (CSI), not `kubernetes.io/aws-ebs` (in-tree) | The in-tree provisioner only works today because EKS's CSI migration shim translates it — the EBS CSI controller/node pods are already running and doing the actual provisioning. Declaring the new SC against the CSI driver directly avoids relying on the migration shim and matches AWS's own guidance. |
| New StorageClass `encrypted` parameter | Set `encrypted: "true"` explicitly | `aws ec2 get-ebs-encryption-by-default --region eu-west-2` confirms account-level default encryption is already `true`, so every existing gp2 volume is encrypted despite the **current** `gp2` SC having no `encrypted` parameter at all. Making it explicit removes the implicit dependency on an account setting nobody who reads the SC would see. |
| `allowVolumeExpansion`, `volumeBindingMode` | Carry over unchanged (`true`, `WaitForFirstConsumer`) | No reason to change either; matches current `gp2` behaviour. |
| IOPS / throughput parameters | Do not set them | Largest volume in the whole gp2 fleet is 100Gi at 300 provisioned IOPS. gp3's free baseline (3000 IOPS / 125 MiB/s) already exceeds every volume here, so explicit `iops`/`throughput` params would be pure overhead. |
| Existing PVs' `storageClassName: gp2` label | Leave as-is (cosmetic only), optionally `kubectl patch pv <name> -p '{"spec":{"storageClassName":"gp3"}}'` per volume after modification | AWS confirms the PV's stated SC has no functional effect once bound — it's purely a label mismatch, safe to defer or skip. |

---

### Per-volume actions (all 16, TEST cluster)

Run `aws ec2 modify-volume --region eu-west-2 --volume-type gp3 --volume-id <id>` for each. No `--iops`/`--throughput` flags needed (see above). Confirm via `aws ec2 describe-volumes-modifications` afterwards.

| Volume ID | Namespace / PVC | Size | State | Action | Why |
|---|---|---|---|---|---|
| `vol-01bde71ec7e43914e` | `thehyve/data-thehyve-postgresql-0` | 64Gi | in-use | Upgrade to gp3 | Live Postgres data. Already modified once before (size expansion, Feb 2026) — in-place modify proven safe on this exact volume. |
| `vol-0287a6c4f10e4b646` | `hie-test-34/data-hie-test-34-postgresql-0` | 64Gi | in-use | Upgrade to gp3 | Live Postgres data, 192 IOPS provisioned — comfortably under gp3's 3000 baseline. |
| `vol-08902bb1432256cc3` | `spicedb/data-spicedb-postgresql-0` | 8Gi | in-use | Upgrade to gp3 | Live SpiceDB Postgres data. |
| `vol-0d6c3d4cbe58c852a` | `ohdsi/data-ohdsi-postgresql-0` | 100Gi | in-use | Upgrade to gp3 | Live OHDSI Postgres data, largest volume in the fleet (300 IOPS) — still well under gp3 baseline. Already modified once before (size expansion, 29 June 2026). |
| `vol-0d8c676ad62a14627` | `hie-test-34/hie-test-34-minio` | 64Gi | in-use | Upgrade to gp3 | Live MinIO object storage backing volume. |
| `vol-0b34d054cafed67bd` | `hutch/data-hutch-postgresql-0` | 8Gi | in-use | Upgrade to gp3 | Live Hutch Postgres data. |
| `vol-0bf5e64f262301143` | `hie-test-34/datadir-hie-test-34-mongodb-b17ef-0` | 8Gi | in-use | Upgrade to gp3 | Live MongoDB data. |
| `vol-094936d66c074d12d` | `hutch/data-hutch-rabbitmq-0` | 8Gi | in-use | **Upgrade to gp3 — reclassify from "delete" to "upgrade"** | Source CSV listed this under Phase 4 ("detach, snapshot, delete"). Live check shows it's attached and in-use by a running RabbitMQ StatefulSet. This is exactly the kind of misclassification Robin flagged in FTFL-691 ("one disk was still attached to a live service") — confirmed here as a second instance. Must not be deleted. |
| `vol-0467e7862365a814d` | `thehyve-nnuh/data-thehyve-nnuh-postgresql-0` | 35Gi | in-use | **Add to scope, then upgrade to gp3** | Not present in the source CSV at all — created after the 2026-06-05 snapshot. Live Postgres data for `thehyve-nnuh`, needs including in FTFL-722. |
| `vol-014fab41bc1429995` | `thehyve-nnuh/thehyve-nnuh-dq-reports` | 10Gi | available (unattached) | Upgrade to gp3 | Local-fallback DQ report storage — unconditional by chart design even though S3 upload (`dqReports.s3.enabled: true`) is the real destination. Idle-by-design, not abandoned — do not delete (see FTFL-724 note below). |
| `vol-00f637771455815c8` | `thehyve-nnuh/thehyve-nnuh-state` | 1Gi | available (unattached) | Upgrade to gp3 | Stores `run_id`/`last_run_at` for the ephemeral ETL init Job's idempotency check. Deleting it would force an unwanted re-run next time `ephemeral.init.runIndex` is bumped. |
| `vol-0693b5d206c740f6f` | `thehyve-cuh/thehyve-cuh-dq-reports` | 10Gi | available (unattached) | Upgrade to gp3 | Same as nnuh's dq-reports — unconditional local fallback, S3 is the real destination for this instance too. |
| `vol-07ff86eedcafb758c` | `thehyve-cuh/thehyve-cuh-state` | 1Gi | available (unattached) | Upgrade to gp3 | Same idempotency role as nnuh's state PVC. `thehyve-cuh` namespace has **no workload at all** currently (`kubectl get all` returns nothing) — ArgoCD app `thehyve-cuh` is Synced/Healthy because its rendered manifest is genuinely PVC/ConfigMap/Secret-only (`postgresql.enabled: false`, ephemeral scheduled CronJob disabled). This is intentional, not orphaned. |
| `vol-06d71e50482b80577` | `thehyve-mkuh/thehyve-mkuh-dq-reports` | 10Gi | available (unattached) | Upgrade to gp3 | Same as cuh — unconditional local fallback. |
| `vol-07bff1cde590299f4` | `thehyve-mkuh/thehyve-mkuh-state` | 1Gi | available (unattached) | Upgrade to gp3 | Same idempotency role. `thehyve-mkuh` is likewise a PVC/ConfigMap/Secret-only ArgoCD app by design. |
| `vol-0e54b7465a4c06b3f` | `thehyve/thehyve-reports` | 1Gi | available (unattached) | Upgrade to gp3 — **do not delete without checking usage** | This is genuinely listed for deletion in the source CSV (Phase 3, "snapshot then delete", 32-day lookback). Unlike the cuh/mkuh/nnuh PVCs, this one isn't explained by the `thehyve-v2` chart's ephemeral pattern — it belongs to the older/different `thehyve` release. Recommend upgrading to gp3 now (cheap, reversible) and handling the delete decision separately under FTFL-724 once its purpose is confirmed. |

Corrected count: **16 volumes on TEST**, not the 14 the CSV implied for "Phase 2" — the extra two are `vol-0467e7862365a814d` (untracked, created after the report) and `vol-094936d66c074d12d` (miscategorised as a Phase 4 delete candidate).

---

### Related GitOps context (for the "why", not required to touch)

- Chart: `charts/integrations/thehyve-v2` (repo `deployment.git`, branch `eoe-test-release`) — deploys `thehyve-cuh`, `thehyve-mkuh`, `thehyve-nnuh` via ArgoCD.
- Per-instance values: `ffnodes/eoe/hie-test-34/thehyve_v2_{cuh,mkuh,nnuh}_values.yaml`.
- `templates/dq-reports-pvc.yaml` — unconditional PVC, comment explicitly says "always provisioned as a local fallback... regardless of whether S3 upload is also configured."
- `templates/ephemeral-state-pvc.yaml` — only renders when `deploymentType: ephemeral`; all three instances are.
- `templates/scheduled-etl-cron-job.yaml` / `templates/init-pipeline-job.yaml` — base `values.yaml` defaults both `ephemeral.init.enabled` and `ephemeral.scheduled.enabled` to `true`, but every instance values file overrides `scheduled.enabled: false`. Only the one-shot `init` Job (triggered by bumping `runIndex` in Git) is live; it self-cleans after completion, which is why nothing shows up in `kubectl get jobs` right now.
- Both PVC templates already support an optional `storageClassName` override (`dqReports.localPvc.storageClassName`, `ephemeral.statePvc.storageClassName`) if a future need arises to pin these three instances to gp3 explicitly rather than relying on the cluster default — not needed for this ticket since flipping the cluster default covers it.

### Note for FTFL-724 (separate ticket, not in scope here)

Do not action deletion for any of the 6 `thehyve-{cuh,mkuh,nnuh}` `state`/`dq-reports` PVCs based on the source CSV — they are declared unconditionally in the chart, so a raw `kubectl delete pvc` would simply be recreated by ArgoCD on next sync. Any real reduction has to happen in Git (e.g., making the local-fallback PVC conditional on `dqReports.s3.enabled == false`, or shrinking its size), and is a chart-level decision, not a per-volume AWS action.

`thehyve/thehyve-reports` (`vol-0e54b7465a4c06b3f`) is the one CSV deletion candidate on TEST that isn't explained by the ephemeral pattern — worth the same due-diligence Robin already did for the PROD copy of this recommendation before deleting.

---

### Verification after modification

```bash
aws ec2 describe-volumes-modifications --region eu-west-2 --query 'VolumesModifications[?ModificationState!=`completed`]' --output table
```

```bash
aws ec2 describe-volumes --region eu-west-2 --filters Name=volume-type,Values=gp2 --query 'length(Volumes)'
```

Second command should return `0` once every TEST volume above (and PROD's, once actioned separately) is migrated — currently the account-wide gp2 count is 28.

---

### Changelog

| Date | Change |
|---|---|
| 2026-07-30 | Investigation completed for TEST cluster (`eoe-test-codisc`); this note created. |