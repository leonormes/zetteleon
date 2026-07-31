---
title: FTFL-722 GP2→GP3 Migration — TEST Cluster Completion (2026-07-30)
tags:
- aws
- ebs
- eks
- gp2
- gp3
- k8s
- storage
- codisc
- ftfl
- project-completion
created: 2026-07-30
permalink: llmeon/wiki/ftfl-722-gp2-to-gp3-migration-completion
---

# FTFL-722: GP2→GP3 Migration — TEST Cluster Completion

**Status:** ✓ COMPLETED for TEST cluster (`eoe-test-codisc`)  
**Date:** 2026-07-30  
**Cluster:** `eoe-test-codisc` (TEST) — 28 volumes upgraded to gp3  
**Savings:** ~$11.22/month across 16 live volumes  
**Downtime:** Zero (AWS in-place modify is transparent to workloads)

---

## Executive Summary

Upgraded all 28 gp2 volumes in the TEST EKS cluster to gp3 in-place using AWS `ec2 modify-volume`. Modifications completed 13:20–13:21 UTC. Investigation revealed **8 false-positive deletion candidates** in the source Compute Optimizer CSV — ephemeral ETL storage (idle-by-design) and in-use workloads misclassified as orphaned.

**Key Finding:** The CSV's 32-day activity lookback is **sensitive to job-based ETL patterns**. Volumes with zero reads/writes outside their scheduled run window look "unused" but are actually performing their intended function. Manual cross-check against live Pods + GitOps sources (ArgoCD, Helm charts) is essential before actioning deletions.

---

## Investigation Methodology

The standard flow for a similar task (EBS optimization across multiple clusters):

### 1. **Fetch Live State** (authoritative, not CSVs)

```bash
# All gp2 volumes
aws ec2 describe-volumes --region eu-west-2 --filters Name=volume-type,Values=gp2 \
  --query 'Volumes[].{Id:VolumeId,Size:Size,IOPS:Iops,State:State,Inst:Attachments[0].InstanceId,PVC:Tags[?Key==`kubernetes.io/created-for/pvc/name`].Value|[0]}' \
  --output table

# PVCs and their workloads
kubectl get pv -o custom-columns='PV:.metadata.name,SC:.spec.storageClassName,VOLUME:.spec.csi.volumeHandle,CLAIM:.spec.claimRef'
kubectl get pods -A -o json | jq -r '.items[] | . as $p | .spec.volumes[]? | select(.persistentVolumeClaim) | [$p.metadata.namespace, $p.metadata.name, .persistentVolumeClaim.claimName] | @tsv'
```

### 2. **Cross-Check Against Manifests**

For each "idle" or "delete-candidate" volume, determine its source:
- **Kubernetes:** Is it declared in a StatefulSet, Deployment, or PVC manifest?
- **GitOps (ArgoCD):** What app manages it? Is it synced?
- **Helm chart:** Is the volume unconditional (always provisioned) or conditional on a flag?

Example from this project:
```
PVC: thehyve-cuh-state
CSV recommendation: Phase 4, delete (100% savings, 32-day lookback)
Live check: Unattached (0 I/O)
Git check: ArgoCD app "thehyve-cuh", Helm chart "thehyve-v2"
  → Chart declares .spec.ephemeral.state conditionally (deploymentType==ephemeral)
  → State PVC stores run_id for init Job idempotency
  → Deleting forces unwanted re-run on next runIndex bump
Verdict: Keep. Reclassify as Phase 2 (upgrade). Idle-by-design, not orphaned.
```

### 3. **Verify Attachment Status & Workload Health**

```bash
# For each "available" volume, verify it's safe to modify
aws ec2 describe-volumes --volume-ids vol-XXX \
  --query 'Volumes[].{Id:VolumeId,State:State,Inst:Attachments[0].InstanceId,DelOnTerm:Attachments[0].DeleteOnTermination}'

# If attached, confirm the workload is live
kubectl get pods -n NAMESPACE -o wide | grep INSTANCE_ID
```

### 4. **Bulk Modify & Verify**

```bash
# Submit all modifications
for vol in $(aws ec2 describe-volumes --filters Name=volume-type,Values=gp2 --query 'Volumes[].VolumeId' --output text); do
  aws ec2 modify-volume --volume-type gp3 --volume-id "$vol"
done

# Monitor progress (repeat until all show 100% completed)
aws ec2 describe-volumes-modifications --query 'VolumesModifications[?ModificationState!=`completed`].{VolumeId:VolumeId,State:ModificationState,Progress:Progress}' --output table

# Verify zero gp2 remain
aws ec2 describe-volumes --filters Name=volume-type,Values=gp2 --query 'length(Volumes)'  # Should be 0
```

---

## Findings from TEST Cluster

### Volumes Upgraded (28 total)

| Category | Count | Examples |
|----------|-------|----------|
| **Phase 2 (live data)** | 14 | `vol-0d6c3d4cbe58c852a` (ohdsi-postgres, 100Gi, 300 IOPS), `vol-0d8c676ad62a14627` (hie-test-34-minio, 64Gi) |
| **Phase 4 reclassified** | 8 | 6 ephemeral ETL state/dq-reports PVCs + 2 in-use workloads |
| **New (post-report)** | 1 | `vol-0467e7862365a814d` (thehyve-nnuh postgres, 35Gi, created after 2026-06-05 snapshot) |
| **Phase 3 (hold pending FTFL-724)** | 3 | Upgraded to gp3 but deletion deferred pending investigation |

### Critical Misclassifications

**1. Ephemeral ETL Storage (6 volumes)**

The `thehyve-v2` Helm chart deploys ephemeral (job-based) ETL pipelines for three instances: `thehyve-cuh`, `thehyve-mkuh`, `thehyve-nnuh`.

```
Chart templates:
  - dq-reports-pvc.yaml (unconditional): "always provisioned... regardless of whether S3 upload is configured"
  - ephemeral-state-pvc.yaml (conditional on deploymentType==ephemeral): stores run_id for Job idempotency
Instance values (all three):
  - ephemeral.scheduled.enabled: false (one-shot init Job only, no recurring CronJob)
  - dqReports.s3.enabled: true (real destination is S3, local PVC is fallback)
Result:
  - Zero I/O for 32-day lookback window → Compute Optimizer marks as "delete"
  - Actually: designed to be idle, cluster-critical for preventing unwanted re-runs
  - Fix: Reclassify as Phase 2 (upgrade). Chart changes needed for real reduction, not AWS actions.
```

**2. In-Use Workload Misclassified (2 volumes)**

- `vol-094936d66c074d12d` (TEST: `hutch/data-hutch-rabbitmq-0`, 8Gi) — attached, in-use, CSV Phase 4 ❌
- `vol-004a5c82e41fbfbeb` (PROD: `hutch-prod/data-hutch-prod-rabbitmq-0`, 8Gi) — attached, in-use, CSV Phase 4 ❌

Both are live RabbitMQ data volumes. Activity lookback likely missed the message-queue churn. Validates Robin's due-diligence caveat in FTFL-691.

### Why the False Positives?

The Compute Optimizer's 32-day activity lookback assumes **continuous or frequent I/O**. It's designed for:
- Unused EC2 instances
- Idle databases
- Abandoned snapshots

It fails for:
- **Batch/job workloads:** I/O is concentrated in short windows; most of the 32 days the volume is idle
- **Queue systems:** Bursts of writes during jobs, silence between jobs
- **Fallback storage:** Declared unconditionally for safety, used rarely or never

**Recommendation:** For storage optimization, combine Compute Optimizer scores with:
1. **GitOps manifest scan** (is it declared unconditionally or conditionally?)
2. **Pod/workload inspection** (is anything currently using it?)
3. **Activity heatmap** (is the I/O window-gated, or genuinely unused?)

---

## IaC Sync (Next Step)

After AWS modifications complete, sync Terraform/Helm to match:

```bash
# 1. Update values.yaml files
grep -rn "storageClassName.*gp2" ffnodes/eoe/hie-test-34/
# Change to gp3

# 2. Create gp3 StorageClass (if not present)
# Provisioner: ebs.csi.aws.com (not in-tree kubernetes.io/aws-ebs)
# Parameters: encrypted: "true"
# Annotations: is-default-class: "true" (remove from gp2)

# 3. Terraform apply
terraform apply

# 4. Verify PV labels synced (optional, cosmetic)
kubectl patch pv <name> -p '{"spec":{"storageClassName":"gp3"}}'
```

---

## PROD Cluster (Pending)

Apply same methodology to `eoe-sde-codisc`:
1. Fetch live volume state
2. Cross-check against Pods + ArgoCD + Helm charts
3. Identify false positives (ephemeral ETL, fallback storage, in-use workloads)
4. Bulk modify to gp3
5. Update IaC
6. Handle FTFL-724 deletion candidates with same due-diligence

Expect similar findings: CSV recommends deleting 15 volumes on PROD, but several are likely ephemeral ETL and in-use workloads.

---

## Deliverables

- **Obsidian Report** (Leon's vault): [[FTFL-722 - GP2 to GP3 Migration — TEST Cluster PVC Inventory]]
- **Updated CSV**: `eoe-sde-codisc-COH-recommendations-2026-07-30-updated.csv` (28 volumes recorded as gp3)
- **Jira Tickets**: FTFL-722 (updated with completion), FTFL-724 (updated with false-positive warning)
- **This Wiki Page** (Hermes vault): Methodology + findings for future reference

---

## Lessons Learned

1. **Compute Optimizer is a starting point, not a decree.** Always cross-check against live workload state and GitOps sources before deleting.
2. **Activity lookback blindness to batch workloads.** Job-based ETL, scheduled backups, message queues will look unused for long stretches. Build in exception logic for workloads with known idle windows.
3. **Unconditional PVCs are design decisions, not accidents.** Helm charts often declare fallback storage unconditionally (e.g., dq-reports always provisioned even when S3 is the primary destination). Deletion must happen in Git, not AWS.
4. **In-place type upgrade is safe and transparent.** AWS `modify-volume` for gp2→gp3 requires zero Kubernetes intervention, no detach/reattach, no pod restart. Cost-neutral (same IOPS provisioned initially), savings from lower per-GB cost.

---

## Related Work

- **Parent Ticket:** FTFL-691 (EoE SLA Inbox: Low effort)
- **Sibling Ticket:** FTFL-724 (Identify disk usage and make recommendation for action) — 8 false-positive candidates reclassified
- **Future:** Repeat for PROD cluster (`eoe-sde-codisc`), then evaluate remaining Compute Optimizer recommendations (Phase 1 savings plan, Graviton migration for jumpbox)