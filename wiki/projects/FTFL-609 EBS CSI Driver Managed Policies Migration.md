---
title: "FTFL-609 — EBS CSI Driver Managed Policies Migration"
wiki_type: dossier
entity_kind: project
created: 2026-06-10T17:40:00+01:00
modified: 2026-06-10T17:40:00+01:00
tags: [wiki, dossier, project]
sources:
  - "[[raw/2026-06-10-pieces-ftfl609-ebs-csi-starter-task]]"
  - "[[raw/2026-06-10-pieces-cos-cron-fix-ftfl658-comment]]"
---

# FTFL-609 — EBS CSI Driver Managed Policies Migration

## Summary
AWS released new managed policies for the EBS CSI Driver (`AmazonEBSCSIDriverEKSClusterScopedPolicy`). FTFL-609 tracks the migration from the existing `AmazonEBSCSIDriverPolicy` to the new cluster-scoped policy across FITFILE's fleet of ~15+ EKS clusters. Currently in the discovery phase — identifying which IAM principals use the old policy is the first action.

> "This is the right first move: **Open the AWS Health Dashboard 'Affected resources' tab and list every IAM principal attached to `AmazonEBSCSIDriverPolicy`** in AWS account `200461870400`." — [[raw/2026-06-10-pieces-ftfl609-ebs-csi-starter-task]]

## Key Facts
- **Jira ticket**: FTFL-609 — "[EE] New Managed Policies Available for the EBS CSI Driver"
- **Status**: In Progress (as of 2026-06-10)
- **Priority**: 🟡 Medium
- **AWS Account**: `200461870400`
- **In sprint since**: 2026-04-21 (6+ weeks)
- **Related work**: Robin's migration plan, Todoist `@Work Next` list (Jun 5)

## Migration Dependency Chain
1. **Discover** — List affected IAM principals (read-only, current required action)
2. **Verify tagging** — Confirm EBS volume/snapshot tagging with `ebs.csi.aws.com/cluster-name`
3. **Test** — Full migration on HIE Test Node (IRSA → Pod Identity, policy swap)
4. **Upgrade driver** — Update `charts/components/ebs-csi-driver/` to latest stable
5. **Swap policies** — Attach new cluster-scoped policy, detach old policy

## Connections
- [[wiki/projects/Terraform IaC Modules]] — EBS CSI Driver provisioned via Terraform `aws_eks_addon.ebs_driver_addon`
- [[wiki/projects/HIE AWS Cluster — RDP via Jumpbox]] — Test node target for migration testing
- [[wiki/projects/CoS-Work-Review-System]] — Tracked as open loop in daily SoT reviews

## Open Questions
- Which specific IAM roles carry `AmazonEBSCSIDriverPolicy` and are they shared across clusters?
- Is the EBS volume tagging already in effect or still outstanding?
- What is the exact scope of clusters affected?

## Timeline
| Date | Event |
|------|-------|
| 2026-04-21 | Ticket entered sprint |
| 2026-06-05 | Starter task identified in Todoist `@Work Next` |
| 2026-06-10 | Agent synthesis delivered the starter task via search_memory pagination |
| 2026-06-10 | Status moved to In Progress (CoS 09:38 run) |