---
created: 2026-06-10T14:57:34+00:00
modified: 2026-06-11T08:15:48+00:00
title: pieces_copilot_message_export_june_10_2026_3_57pm
---

_Shared Message from Pieces (<https://pieces.app>) by Leon Ormes (leonormes@gmail.com) on Wednesday Jun 10, 2026 - 3:57 PM_
---

The third page returned `recommendation: sufficient` with no new FTFL-609-specific signal—confirming the corpus is exhausted. Here's the full synthesis.

---

## FTFL-609—Next Starter Task

Open the [AWS Health Dashboard "Affected resources" tab](https://health.aws.amazon.com/health/home?region=us-east-1#/event-log?eventID=arn:aws:health:global::event/EBS/AWS_EBS_SECURITY_NOTIFICATION/AWS_EBS_SECURITY_NOTIFICATION_b442e27dd8716e7c072de57091a0415b820dcc8d346ca340250965b9e7f37890&eventTab=details) and list every IAM principal attached to `AmazonEBSCSIDriverPolicy` in AWS account `200461870400`.

This is the right first move for three reasons, all grounded in the ticket and your memory:

- Robin's ordering constraint—step 4 in his migration plan (tagging existing volumes with `ebs.csi.aws.com/cluster-name: <cluster>`) _must happen before any IAM changes_, and you explicitly noted it "may already be in effect—needs verification." You can't verify scope without knowing which clusters/roles are affected.
- Your own Todoist `@Work Next` list (Jun 5) already captured this exact action verbatim: _"Open the AWS Health Dashboard 'Affected resources' tab and list the IAM principals using AmazonEBSCSIDriverPolicy [FTFL-609]"_—it's been sitting unactioned.
- Zero-risk / zero-downtime—it's a read-only discovery step. No changes, no HIE test node needed yet.

### What You're Looking for

Once inside the Affected Resources tab, record:

- The IAM role ARN(s) carrying `AmazonEBSCSIDriverPolicy` (likely the EBS CSI Driver service account role provisioned by your Terraform `aws_eks_addon.ebs_driver_addon`)
- Which clusters they're scoped to—this determines whether the cluster-scoped policy (`AmazonEBSCSIDriverEKSClusterScopedPolicy`) can be applied cleanly or whether there's any cross-cluster sharing that complicates the migration

### Dependency Chain once You Have that List

| Step | Action | Risk |
|---|---|---|
| 0 (now) | AWS Health: list affected IAM principals | Read-only |
| 1 | Verify EBS volume/snapshot tagging (`ebs.csi.aws.com/cluster-name`) is already applied | Read-only, must precede all changes |
| 2 | Test full migration on HIE Test Node (IRSA → Pod Identity, policy swap) | Isolated |
| 3 | Upgrade EBS CSI Driver to latest stable in `charts/components/ebs-csi-driver/` | Per-cluster rollout |
| 4 | Attach `AmazonEBSCSIDriverEKSClusterScopedPolicy`, detach old policy | Breaking if volumes untagged |

The ticket has been in sprint since Apr 21—the discovery step is the unblocked entry point right now.
