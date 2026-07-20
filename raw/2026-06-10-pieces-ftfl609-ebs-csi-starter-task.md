---
created: 2026-06-10T13:50:00+00:00
modified: 2026-07-20T16:32:35+00:00
permalink: llmeon/raw/2026-06-10-pieces-ftfl609-ebs-csi-starter-task
pieces_ids: [2d9a335e-8a71-441f-8, 40673b4f-9513-4fb6-9, 71a4e746-173a-42bf-b]
source: pieces-ltm
tags: [pieces, raw]
title: 2026-06-10-pieces-ftfl609-ebs-csi-starter-task
---

## FTFL-609—EBS CSI Driver Starter Task Discovery

### User Request (14:51)

> "I have this ticket to do. /Volumes/DAL/Zettelkasten/LLMeon/jira/FTFL-609-EE-New-Managed-Policies-Available-for-EBS-CSI-Driver.md—what is the next starter task to get this rolling?"

### Agent Synthesis (14:56)

Using 3 search_memory pagination cycles across memory, the agent synthesised:

#### Next Starter Task

Open the [AWS Health Dashboard "Affected resources" tab](https://health.aws.amazon.com/health/home?region=us-east-1#/event-log?eventID=arn:aws:health:global::event/EBS/AWS_EBS_SECURITY_NOTIFICATION/AWS_EBS_SECURITY_NOTIFICATION_b442e27dd8716e7c072de57091a0415b820dcc8d346ca340250965b9e7f37890&eventTab=details) and list every IAM principal attached to `AmazonEBSCSIDriverPolicy` in AWS account `200461870400`.

Three reasons:

1. Robin's ordering constraint—step 4 of his migration plan (tagging existing volumes with `ebs.csi.aws.com/cluster-name: <cluster>`) _must happen before any IAM changes_
2. Todoist `@Work Next` list (Jun 5) already captures this verbatim
3. Zero-risk / zero-downtime—read-only discovery step

#### Dependency Chain

| Step | Action | Risk |
|------|--------|------|
| 0 (now) | AWS Health: list affected IAM principals | Read-only |
| 1 | Verify EBS volume/snapshot tagging is already applied | Read-only, must precede all changes |
| 2 | Test full migration on HIE Test Node (IRSA → Pod Identity, policy swap) | Isolated |
| 3 | Upgrade EBS CSI Driver to latest stable in `charts/components/ebs-csi-driver/` | Per-cluster rollout |
| 4 | Attach `AmazonEBSCSIDriverEKSClusterScopedPolicy`, detach old policy | Breaking if volumes untagged |

#### Context

- FTFL-609 in sprint since April 21
- AWS account 200461870400
- Existing raw `jira/FTFL-609-EE-New-Managed-Policies-Available-for-EBS-CSI-Driver.md`
