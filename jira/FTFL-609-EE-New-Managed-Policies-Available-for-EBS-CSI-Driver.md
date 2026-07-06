---
created: 2026-06-10T08:00:57+00:00
date: 2026-06-09
jira-assignee: Leon Ormes
jira-key: FTFL-609
jira-reporter: Robin Mofakham
jira-status: In Progress
modified: 2026-07-04T10:50:33+00:00
permalink: llmeon/jira/ftfl-609-ee-new-managed-policies-available-for-ebs-csi-driver
project: FITFILE
source: atlassian-jira
tags: [aws, csi, ebs, eks, ftfl, iam, jira]
title: FTFL-609-EE-New-Managed-Policies-Available-for-EBS-CSI-Driver
---

## FTFL-609—[EE] New Managed Policies Available for the EBS CSI Driver

Status: In Progress · Priority: Medium · Type: Task

Assignee: Leon Ormes · Reporter: Robin Mofakham

Parent Epic: FTFL-1 (Bugs, BAU & Debt)

Created: 2026-04-21 · Updated: 2026-06-10

Sprint: FITFILE Sprint 21 · Story Points: 5

---

### Description

See the following notice forward to FITFILE SLA Inbox from Keiran at EE:

Hello,

You are receiving this notification because your AWS account has one or more IAM principals with the `AmazonEBSCSIDriverPolicy` managed policy attached.

AWS has released two new managed IAM policies that align the EBS CSI Driver with least-privilege best practices:

1. AmazonEBSCSIDriverPolicyV2—restricts actions to resources tagged as managed by the EBS CSI Driver.
2. AmazonEBSCSIDriverEKSClusterScopedPolicy—restricts actions to resources belonging to a specific EKS cluster, preventing cross-cluster access.

> ⚠️ If you use static provisioning (volumes/snapshots not created by but imported for use by the driver), you must manually tag those resources before switching policies. This is a breaking change for those use cases.

Migration steps:

1. Attach one of the new policies to the IAM identity used by the EBS CSI Driver.
2. Detach the old `AmazonEBSCSIDriverPolicy`—keeping both attached means the broader permissions remain in effect.

Reference: [AWS Health Dashboard](https://health.aws.amazon.com/health/home?region=us-east-1#/event-log?eventID=arn:aws:health:global::event/EBS/AWS_EBS_SECURITY_NOTIFICATION/AWS_EBS_SECURITY_NOTIFICATION_b442e27dd8716e7c072de57091a0415b820dcc8d346ca340250965b9e7f37890&eventTab=details)

#### Docs

- [AmazonEBSCSIDriverPolicyV2](https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AmazonEBSCSIDriverPolicyV2.html)
- [AmazonEBSCSIDriverEKSClusterScopedPolicy](https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AmazonEBSCSIDriverEKSClusterScopedPolicy.html)
- [Migration guidance (GitHub)](https://github.com/kubernetes-sigs/aws-ebs-csi-driver/issues/2918)
- [Adding/removing IAM policies](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_manage-attach-detach.html)

---

### Robin's Analysis (Comment)

From Robin Mofakham (@Ollie Rushton):

The migration requires:

1. Move from IRSA identity to EKS Pod Identity—so the session tag is set automatically. The addon is already installed for EKS Pod Identity, just not used for the EBS CSI Driver identity.
2. Update the `ebs_csi_assume_role_policy`—add `sts:TagSession` action (and possibly `sts:AssumeRole`).
3. Upgrade EBS CSI Drivers to latest stable version.
4. Tag existing EBS volumes and snapshots with the cluster name:

```
ebs.csi.aws.com/cluster-name: <replace-with-cluster-name>
```

   This may already be in effect—needs verification. Must be done first before any changes.

1. Attach `AmazonEBSCSIDriverEKSClusterScopedPolicy` to the IAM role.
2. Detach the old `AmazonEBSCSIDriverPolicy` from the IAM role.

> ⚠️ Error prone—test first if downtime is not acceptable.
> → Should be tested on the HIE Test Node first.

---

### Changelog (Key Events)

| Date | Change |
|---|---|
| 2026-04-21 | Created by Robin, assigned to FITFILE Sprint 15 |
| 2026-05-18 | Prioritised to Medium, moved to Selected for Development, linked to FTFL-1 |
| 2026-05-26 | Story Points set to 5 |
| 2026-05-27 | Assigned to Leon Ormes |
| 2026-06-04 | Added to Sprint 21 |
| 2026-06-10 | Status → In Progress |

---

### Related

- Respository: `FITFILE/Deployment` [[git-history-analysis-merge-commits-and-commit-message-standards]]
- EBS CSI Driver chart: `charts/components/ebs-csi-driver/`
