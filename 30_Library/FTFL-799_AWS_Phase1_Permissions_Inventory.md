---
created: 2026-07-31T09:24:09+00:00
modified: 2026-08-29T09:35:56+00:00
permalink: llmeon/30-library/ftfl-799-aws-phase1-permissions-inventory
tags: [axiom:FTFL-799, infrastructure/aws, permissions, terraform, typed-edge]
title: FTFL-799_AWS_Phase1_Permissions_Inventory
---

## FTFL-799: AWS Phase 1—Terraform SP & Developer Permissions Inventory

Status: Phase 1 complete (AWS). Phase 2 (Azure) and Phase 3 (unified doc) in progress.

Evidence base: Live AWS account 592527451415 (FITFILE-Platforms sandbox, HCP Terraform project), Terraform modules, Confluence, git history.

Investigation context: Jira FTFL-799—"Update the permissions docs for a customer deployment." New permissions discovered during private-cluster-backup work need documented for customer discovery packs.

---

### Table A1: AWS Terraform SP (`tfc-role`)

Identity: `arn:aws:iam::592527451415:role/tfc-role`

Policy: `tfc-policy` (customer-managed, v15—actively evolving)

Auth method: OIDC federation to `app.terraform.io` (audience `aws.workload.identity`, workspace-scoped via subject pattern), no static keys

#### Permissions

| Permission / Block | Scope | Purpose | FTFL scope |
|---|---|---|---|
| OIDC trust (`sts:AssumeRoleWithWebIdentity`) | OIDC provider `app.terraform.io` | HCP Terraform assumes role per-run without long-lived keys | Core deployment auth |
| `ec2:*` | `Resource: *` | VPC/subnets/IGW/NAT/ENI/SG/launch-templates/jumpbox/EBS | Infrastructure provisioning (blanket) |
| EKS full lifecycle | `*` | Cluster/nodegroup/addon/pod-identity/access-entry create/delete/update | Cluster lifecycle |
| IAM role/policy/OIDC/SLR lifecycle | `*` | All workload role creation (OIDC provider, EBS-CSI, autoscaler, VPC-Lattice, jumpbox) | Workload identity |
| IAM user lifecycle (CreateUser/DeleteUser/CreateAccessKey/PutUserPolicy) | `*` | S3-export IAM user + static key, gated by `modules/s3-bucket` `create_access_keys` var | Optional external-tool integration |
| KMS full lifecycle | `*` | Customer-managed keys for secrets, EBS, S3 | Encryption orchestration |
| `s3:*` + `kms:GenerateDataKey` | `*` | State/export/logging buckets, server-side encryption | Deployment state + data export |
| Route53 + Route53 Domains | `*` | DNS zone/record/domain registration | DNS management |
| Elastic Load Balancing (Describe only) | `*` | Read LB state for outputs/health checks | Read-only observability |
| Network Firewall | `*` | `modules/gateway`—AWS Network Firewall policy/rules (egress control) | Private-cluster egress |
| CloudWatch Logs | `ListLogDeliveries` | Discover existing log delivery configs | Observability setup |
| ⚠️ SSM Session Manager (hardcoded ARNs) | `arn:aws:ec2:eu-west-2:135808916559:instance/i-01903aa5c47d2d015` | Unclear—appears to be environment-specific scaffolding | UNVERIFIED—account 135808916559 ≠ 592527451415 |

#### AWS Backup (FTFL-799 Delta)

Separate role `aws-backup-role` (service principal trust to `backup.amazonaws.com`), policy `aws-backup-role-policy` (v1—fresh):

```json
{
  "Statement": [
    {
      "Action": [
        "ec2:Describe*",
        "eks:DescribeCluster",
        "eks:ListClusters",
        "eks:DescribeNodegroup",
        "k8s:ListResources",
        "k8s:DescribeResources",
        "backup:*"
      ],
      "Effect": "Allow",
      "Resource": "*"
    }
  ]
}
```

Key addition: `k8s:ListResources`/`k8s:DescribeResources`—native EKS backup support for private clusters. Vaults (`eks-backup-vault`, `Default`) and plans (`eks-backup-plan`) exist live but not yet Terraform-managed in the module.

---

### Table A2: Roles the Terraform SP Creates & Assigns

| Workload | Role | Permissions | Why |
|---|---|---|---|
| EKS control plane | `aws_iam_role.this` (module `eks`) | `AmazonEKSClusterPolicy` | Service principal for cluster |
| Node group | `aws_iam_role.node_group` | `AmazonEKSWorkerNodePolicy`, `AmazonEKS_CNI_Policy`, ECR read-only | Worker node lifecycle |
| EBS CSI (IRSA) | `aws_iam_role.ebs_csi_role` | `AmazonEBSCSIDriverPolicy`, OIDC federated trust | Dynamic PersistentVolume provisioning |
| Cluster Autoscaler (IRSA) | `aws_iam_role.cluster_autoscaler_role` | Custom: ASG Describe*, EC2 Describe*, `eks:DescribeNodegroup` (read) + `SetDesiredCapacity`/`TerminateInstanceInAutoScalingGroup` (write) | Node group auto-scaling |
| VPC Lattice Controller (IRSA) | `aws_iam_role.vpc_lattice_controller` | `var.vpc_lattice_controller_policy_arn` | Service mesh ingress (optional) |
| Jumpbox/Bastion | `${deployment-key}-jumpbox-ssm-role` | `AmazonSSMManagedInstanceCore`, scoped KMS decrypt (hardcoded ARN to acct 135808916559 ⚠️), EKS describe + `AmazonEKSClusterAdminPolicy`, `ec2:Describe*` | Operator SSM access → cluster admin |
| S3 Export User | `aws_iam_user.s3_user` (module `s3-bucket`, if `create_access_keys=true`) | Custom S3 access + static access key | Integration with external tools (Hyve) |
| AWS Backup | `aws-backup-role` | See above (`backup:*` + k8s describe) | Private cluster backup restore |

---

### Table A3: AWS Developer/Operator Permissions

| Role/Group | Type | Key Actions | Used by | Notes |
|---|---|---|---|---|
| Jumpbox instance role | IAM role via SSM Session Manager | EKS `AmazonEKSClusterAdminPolicy` (cluster scope), `ec2:Describe*`, scoped KMS decrypt | FITFILE DevOps | No SSH keys, no public IP. Cluster-admin access is bound to the instance, not individual IAM principals—least-privilege for operators depends on who gets `ssm:StartSession` to this one jumpbox |
| Named IAM user/role access entries | `aws_eks_access_entry.user_access` (if `enable_iam_user_access=true`) | Configurable Kubernetes groups per principal | Break-glass FITFILE engineers, customer IT admins | Optional, off by default. Requires per-workspace `.tfvars` or variable-set configuration. |
| IAM Identity Center | AWS SSO instance `ssoins-7535c9ff6ec965ed` ("FITFILE", Active since 2024-08-09, eu-west-2) | (TBD via permission sets) | FITFILE engineer federation | UNVERIFIED—`list-permission-sets` returned empty during investigation. Confirm via AWS console or a principal with appropriate SSO-admin perms. |
| `tfc-role` itself (OIDC) | IAM role | (see Table A1) | HCP Terraform automation only | No static access keys. Current practice contradicts the "API Key Credentials" language in older Confluence docs—OIDC is the live pattern. |

---

### Verification Checklist (Live Commands)

```bash
# Self-identity
aws sts get-caller-identity

# Terraform SP role + trust
aws iam get-role --role-name tfc-role \
  --query "Role.{Arn:Arn,AssumeRolePolicyDocument:AssumeRolePolicyDocument,MaxSessionDuration:MaxSessionDuration}"

# Policy (check version, currently v15)
aws iam list-attached-role-policies --role-name tfc-role
aws iam get-policy --policy-arn arn:aws:iam::592527451415:policy/tfc-policy --query "Policy.DefaultVersionId"
aws iam get-policy-version --policy-arn arn:aws:iam::592527451415:policy/tfc-policy --version-id v15 --query "PolicyVersion.Document"

# AWS Backup role + policy (FTFL-799)
aws iam get-role --role-name aws-backup-role
aws iam get-policy --policy-arn arn:aws:iam::592527451415:policy/aws-backup-role-policy --query "Policy.DefaultVersionId"
aws iam get-policy-version --policy-arn arn:aws:iam::592527451415:policy/aws-backup-role-policy --version-id v1 --query "PolicyVersion.Document"

# Backup infrastructure
aws backup list-backup-vaults
aws backup list-backup-plans

# OIDC provider (should be only app.terraform.io, no strays)
aws iam list-open-id-connect-providers

# EKS clusters (none in sandbox; re-run when deployed)
aws eks list-clusters
aws eks list-access-entries --cluster-name <cluster>

# IAM Identity Center
aws sso-admin list-instances
aws sso-admin list-permission-sets --instance-arn arn:aws:sso:::instance/ssoins-7535c9ff6ec965ed
```

---

### Gaps & Open Questions

1. Blanket EC2/S3 grants—`ec2:*` and `s3:*` in live `tfc-policy` v15. Intentional risk/simplicity trade-off, or technical debt? Recommend audit to itemize specific actions needed.
2. Hardcoded account 135808916559—appears in both `tfc-policy` (SSM session ARNs) and `modules/jumpbox/main.tf` (KMS key ARN). Known shared account (e.g., backup vault, shared logging)? Or stale scaffolding to remove before using as customer template?
3. IAM Identity Center permission sets—`list-permission-sets` returned empty; visibility issue or not configured? Verify via console.
4. Real customer `enable_iam_user_access` values—module defaults to false; confirm per deployment's actual `.tfvars` or variable sets.
5. AWS Backup Terraform codification—vaults/plans exist live but no `aws_backup_*` resources in the module (grep-confirmed). Is this in FTFL-799 scope or a follow-up?

---

### Doctrine Notes

- Auth pattern: OIDC federation (current, proven) > IAM user with static keys (legacy fallback, still documented). Customer-facing discovery pack should recommend OIDC.
- Principle: All workload identities (EBS-CSI, autoscaler, VPC-Lattice, jumpbox) are created by the Terraform SP on first deploy; SP holds unrestricted `iam:PassRole` and `iam:CreateRole`, so no additional privilege-escalation gates exist post-deploy.
- Backup delta: `k8s:ListResources`/`k8s:DescribeResources` are new for private-cluster backups. This is the core FTFL-799 discovery.

---

See also: FTFL-799 (Jira), Confluence "AWS - Customer Checklist" (Jan 2025, stale vs live), "FITFILE Deployment Requirements for AWS Environment" (Jul 2025, comprehensive but missing S3/backup details).

Next: Phase 2 (Azure), then Phase 3 (unified customer deliverable).
