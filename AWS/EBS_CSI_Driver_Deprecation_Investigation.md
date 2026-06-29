---
created: 2026-06-16 11:05:06+00:00
modified: 2026-06-16 11:08:09+00:00
title: EBS_CSI_Driver_Deprecation_Investigation
permalink: llmeon/aws/ebs-csi-driver-deprecation-investigation
---

## EBS CSI Driver Policy Deprecation Investigation Report

Investigation Date: 16 June 2026
AWS Account: 135808916559
Region: eu-west-2
Authenticated User: leon.ormes@fitfile.com (SSO)
Role: AWSReservedSSO_DiscoveryEngineeringAccess_b38ff0a73dfb5f6d

---

### Executive Summary

STATUS: Action Required

Two EKS clusters in the account are currently utilising the deprecated `AmazonEBSCSIDriverPolicy` and must be migrated to either `AmazonEBSCSIDriverPolicyV2` or `AmazonEBSCSIDriverEKSClusterScopedPolicy` before AWS transitions these policies out of service.

Additionally, 9 out of 37 EBS volumes lack the standard CSI driver tags (`ebs.csi.aws.com/cluster=true`), which could be subject to breaking changes during the deprecation transition.

---

### Section 1: Current IAM Context & Authorisation

#### Current Identity

- User/Role: leon.ormes@fitfile.com
- Assumed Role: AWSReservedSSO_DiscoveryEngineeringAccess_b38ff0a73dfb5f6d
- Account ID: 135808916559
- ARN: `arn:aws:sts::135808916559:assumed-role/AWSReservedSSO_DiscoveryEngineeringAccess_b38ff0a73dfb5f6d/leon.ormes@fitfile.com`

#### Permissions Assessment

Current Role Policies:

- DiscoveryEngineeringAccessPolicyPart1 (v2)
- DiscoveryEngineeringAccessPolicyPart2 (v2)
- DiscoveryEngineeringAccessPolicyPart3 (v2)
- ConsoleAccountInfoPolicy
- AWSMarketplaceManageSubscriptions

IAM Modification Authorisation: ✅ AUTHORISED

Your role has explicit permissions to:

- `iam:AttachRolePolicy`—attach managed policies to roles
- `iam:DetachRolePolicy`—detach managed policies from roles
- `iam:CreatePolicy`, `iam:DeletePolicy`—manage custom policies
- `iam:PassRole`—pass roles to AWS services
- Full EKS and EC2 management permissions

Restrictions Applied:

- Cannot delete or modify users, groups, or access keys
- Cannot view billing or modify account settings
- Cannot delete CloudTrail trails or disable logging
- Cannot schedule KMS key deletion

Conclusion: You have sufficient authorisation to execute the EBS CSI driver policy migration.

---

### Section 2: Affected Principals

#### Roles with Legacy Policy

Two IAM roles currently have the deprecated `arn:aws:iam::aws:policy/service-role/AmazonEBSCSIDriverPolicy` attached:

##### Role 1: eoe-sde-codisc-AmazonEKS_EBS_CSI_DriverRole

| Property | Value |
|----------|-------|
| Full ARN | `arn:aws:iam::135808916559:role/eoe-sde-codisc-AmazonEKS_EBS_CSI_DriverRole` |
| Created | 14 February 2025, 17:49:20 UTC |
| Associated Cluster | eoe-sde-codisc |
| Service Account | `system:serviceaccount:kube-system:ebs-csi-controller-sa` |
| Current Policy | `arn:aws:iam::aws:policy/service-role/AmazonEBSCSIDriverPolicy` |
| Status | ⚠️ Requires migration |

Tags:

- `eks_cluster`: eoe-sde-codisc
- `ProvisionByOrgName`: FITFILE
- `branch`: master
- `GitlabRepo`: gitlab.com/fitfile/customers/eoe/hie-sde-v2

##### Role 2: eoe-test-codisc-AmazonEKS_EBS_CSI_DriverRole

| Property | Value |
|----------|-------|
| Full ARN | `arn:aws:iam::135808916559:role/eoe-test-codisc-AmazonEKS_EBS_CSI_DriverRole` |
| Created | 10 February 2026, 10:03:40 UTC |
| Associated Cluster | eoe-test-codisc |
| Service Account | `system:serviceaccount:kube-system:ebs-csi-controller-sa` |
| Current Policy | `arn:aws:iam::aws:policy/service-role/AmazonEBSCSIDriverPolicy` |
| Status | ⚠️ Requires migration |

Tags:

- `eks_cluster`: eoe-test-codisc
- `ProvisionByOrgName`: FITFILE
- `branch`: main
- `environment`: test
- `GitlabRepo`: gitlab.com/fitfile/customers/eoe/hie-test-34

#### No IAM Users with Legacy Policy

Searched all users in the account—none have the legacy EBS CSI policy attached.

---

### Section 3: EKS Clusters & IRSA Configuration

#### Cluster 1: Eoe-sde-codisc

| Property | Value |
|----------|-------|
| Status | ACTIVE |
| Kubernetes Version | 1.33 |
| Created | 14 February 2025, 17:41:25 UTC |
| OIDC Issuer | `https://oidc.eks.eu-west-2.amazonaws.com/id/23BDD27C5ECF85950BCEA129801871CB` |
| Region | eu-west-2 |

IRSA Configuration:

- OIDC Provider ARN: `arn:aws:iam::135808916559:oidc-provider/oidc.eks.eu-west-2.amazonaws.com/id/23BDD27C5ECF85950BCEA129801871CB`
- Client IDs: `sts.amazonaws.com`
- Thumbprints: 3 certificates configured (active, rotated)
- Service Account: `system:serviceaccount:kube-system:ebs-csi-controller-sa`

Associated Role:

- `eoe-sde-codisc-AmazonEKS_EBS_CSI_DriverRole` (Legacy policy attached)

Tags:

- `Name`: eoe-sde-codisc
- `ProvisionByOrgName`: FITFILE
- `branch`: master
- `GitlabRepo`: gitlab.com/fitfile/customers/eoe/hie-sde-v2

---

#### Cluster 2: Eoe-test-codisc

| Property | Value |
|----------|-------|
| Status | ACTIVE |
| Kubernetes Version | 1.33 |
| Created | 10 February 2026, 09:55:35 UTC |
| OIDC Issuer | `https://oidc.eks.eu-west-2.amazonaws.com/id/BB08B20C015244FA577F249465CE5B2F` |
| Region | eu-west-2 |

IRSA Configuration:

- OIDC Provider ARN: `arn:aws:iam::135808916559:oidc-provider/oidc.eks.eu-west-2.amazonaws.com/id/BB08B20C015244FA577F249465CE5B2F`
- Client IDs: `sts.amazonaws.com`
- Thumbprints: 3 certificates configured (active, rotated)
- Service Account: `system:serviceaccount:kube-system:ebs-csi-controller-sa`

Associated Role:

- `eoe-test-codisc-AmazonEKS_EBS_CSI_DriverRole` (Legacy policy attached)

Tags:

- `Name`: eoe-test-codisc
- `ProvisionByOrgName`: FITFILE
- `branch`: main
- `environment`: test
- `GitlabRepo`: gitlab.com/fitfile/customers/eoe/hie-test-34

---

#### IRSA Trust Policy Analysis

Both EBS CSI driver roles have correctly configured IRSA trust policies with:

- Federated principal pointing to the cluster-specific OIDC provider
- Condition restricting assumption to the EBS CSI controller service account
- Proper `aud` (audience) claim validation set to `sts.amazonaws.com`

Example trust policy structure:

```json
{
  "Effect": "Allow",
  "Principal": {
    "Federated": "arn:aws:iam::135808916559:oidc-provider/oidc.eks.eu-west-2.amazonaws.com/id/23BDD27C5ECF85950BCEA129801871CB"
  },
  "Action": "sts:AssumeRoleWithWebIdentity",
  "Condition": {
    "StringEquals": {
      "oidc.eks.eu-west-2.amazonaws.com/id/23BDD27C5ECF85950BCEA129801871CB:aud": "sts.amazonaws.com",
      "oidc.eks.eu-west-2.amazonaws.com/id/23BDD27C5ECF85950BCEA129801871CB:sub": "system:serviceaccount:kube-system:ebs-csi-controller-sa"
    }
  }
}
```

---

### Section 4: EBS Resources Analysis

#### Volume Summary

| Metric | Count |
|--------|-------|
| Total Volumes | 37 |
| Volumes with CSI Tags | 28 |
| Volumes WITHOUT CSI Tags | 9 |
| Percentage Tagged | 75.7% |
| Status | ⚠️ Breaking change risk |

#### Volumes Missing CSI Tags (ebs.csi.aws.com/cluster)

⚠️ BREAKING CHANGE RISK—These volumes may be affected during the deprecation transition

| Volume ID | Size | State | Current Tags | Cluster | Risk Level |
|-----------|------|-------|--------------|---------|-----------|
| vol-0495ed05c42bdb021 | 60 GB | in-use | eks:nodegroup-name, eks:cluster-name | eoe-test-codisc | 🟡 MEDIUM |
| vol-03c23f95447153a18 | 32 GB | in-use | ProvisionByOrgName, branch, GitlabRepo | eoe-test-codisc | 🔴 HIGH |
| vol-0834da1f3486fea9a | 60 GB | in-use | eks:cluster-name, eks:nodegroup-name | eoe-sde-codisc | 🟡 MEDIUM |
| vol-0a929e0fedba97937 | 60 GB | in-use | eks:nodegroup-name, eks:cluster-name | eoe-test-codisc | 🟡 MEDIUM |
| vol-0f512bf32e7a77a79 | 40 GB | in-use | None | Unknown | 🔴 CRITICAL |
| vol-045d9a2ba2ce0059c | 60 GB | in-use | eks:nodegroup-name, eks:cluster-name | eoe-sde-codisc | 🟡 MEDIUM |
| vol-084a2470987348115 | 60 GB | in-use | eks:cluster-name, eks:nodegroup-name | eoe-sde-codisc | 🟡 MEDIUM |
| vol-0c9b7bbfc0f08c77d | 60 GB | in-use | eks:cluster-name, eks:nodegroup-name | eoe-test-codisc | 🟡 MEDIUM |
| vol-0ec0cf31c76b3e885 | 32 GB | in-use | GitlabRepo, ProvisionByOrgName, branch | eoe-sde-codisc | 🔴 HIGH |

Risk Classification:

- 🔴 CRITICAL (1): Completely untagged—no identification possible
- 🔴 HIGH (2): Missing both EKS and CSI tags—cluster affiliation unclear
- 🟡 MEDIUM (6): Has EKS tags but missing CSI driver tags—partially identifiable

#### Snapshot Summary

| Metric | Count |
|--------|-------|
| Total Snapshots | 0 |
| Status | ✅ No action required |

---

### Section 5: Deprecation Policy Comparison

#### Current vs. Recommended Policies

| Feature | Legacy Policy | V2 Policy | Cluster-Scoped Policy |
|---------|---------------|-----------|----------------------|
| AWS Policy Name | AmazonEBSCSIDriverPolicy | AmazonEBSCSIDriverPolicyV2 | AmazonEBSCSIDriverEKSClusterScopedPolicy |
| ARN | `arn:aws:iam::aws:policy/service-role/AmazonEBSCSIDriverPolicy` | `arn:aws:iam::aws:policy/service-role/AmazonEBSCSIDriverPolicyV2` | `arn:aws:iam::aws:policy/service-role/AmazonEBSCSIDriverEKSClusterScopedPolicy` |
| Support Status | 🔴 Deprecated | 🟢 Current | 🟢 Current |
| Recommended For | None | Multi-cluster setups | Single EKS cluster |
| Permissions Scope | Broad | Refined | Fine-grained, cluster-scoped |
| Breaking Changes | High risk on untagged resources | Low risk | Low risk |

#### Migration Recommendation

For your environment:

- eoe-sde-codisc cluster: Use `AmazonEBSCSIDriverEKSClusterScopedPolicy` (single cluster, highest security)
- eoe-test-codisc cluster: Use `AmazonEBSCSIDriverEKSClusterScopedPolicy` (single cluster, highest security)

The cluster-scoped variant is recommended because:

1. Each cluster has its own dedicated IRSA role
2. It provides the most restrictive permissions (principle of least privilege)
3. It aligns with EKS security best practices
4. It minimises the blast radius if a pod is compromised

---

### Section 6: Pre-Migration Action Items

#### 6.1 Tag Untagged Volumes (HIGH PRIORITY)

Before migrating policies, tag all untagged volumes to prevent breaking changes:

Critical Volume (vol-0f512bf32e7a77a79)—Requires Investigation:

```bash
# First, determine which cluster this volume belongs to
aws ec2 describe-volume-attribute --volume-id vol-0f512bf32e7a77a79 \
  --attribute attachmentSet --region eu-west-2

# Then apply appropriate tags:
aws ec2 create-tags --resources vol-0f512bf32e7a77a79 \
  --tags Key=ebs.csi.aws.com/cluster,Value=<CLUSTER_NAME> \
  --region eu-west-2
```

High-Risk Volumes—Tag with Cluster Name:

```bash
# vol-03c23f95447153a18 (eoe-test-codisc)
aws ec2 create-tags --resources vol-03c23f95447153a18 \
  --tags Key=ebs.csi.aws.com/cluster,Value=eoe-test-codisc \
  --region eu-west-2

# vol-0ec0cf31c76b3e885 (eoe-sde-codisc)
aws ec2 create-tags --resources vol-0ec0cf31c76b3e885 \
  --tags Key=ebs.csi.aws.com/cluster,Value=eoe-sde-codisc \
  --region eu-west-2
```

Medium-Risk Volumes—Already Have Cluster Info via EKS Tags:

- These can be tagged automatically using their `eks:cluster-name` tag value
- Execute tagging for all 6 medium-risk volumes before policy migration

#### 6.2 Verify EBS CSI Driver Deployment

Before policy migration, confirm the EBS CSI driver is operational on both clusters:

```bash
# For eoe-sde-codisc
kubectl get pods -n kube-system -l app=ebs-csi-controller

# For eoe-test-codisc
kubectl get pods -n kube-system -l app=ebs-csi-controller
```

#### 6.3 Plan Maintenance Window

Policy migration may cause temporary service interruption:

- Minimal downtime expected (seconds)
- Recommend executing during low-traffic windows
- Test on eoe-test-codisc first

---

### Section 7: Migration Commands

#### Phase 1: Detach Legacy Policy (Both Roles)

```bash
# eoe-sde-codisc-AmazonEKS_EBS_CSI_DriverRole
aws iam detach-role-policy \
  --role-name eoe-sde-codisc-AmazonEKS_EBS_CSI_DriverRole \
  --policy-arn arn:aws:iam::aws:policy/service-role/AmazonEBSCSIDriverPolicy \
  --profile eoe-hie

# eoe-test-codisc-AmazonEKS_EBS_CSI_DriverRole
aws iam detach-role-policy \
  --role-name eoe-test-codisc-AmazonEKS_EBS_CSI_DriverRole \
  --policy-arn arn:aws:iam::aws:policy/service-role/AmazonEBSCSIDriverPolicy \
  --profile eoe-hie
```

#### Phase 2: Attach Cluster-Scoped Policy (Both Roles)

```bash
# eoe-sde-codisc-AmazonEKS_EBS_CSI_DriverRole
aws iam attach-role-policy \
  --role-name eoe-sde-codisc-AmazonEKS_EBS_CSI_DriverRole \
  --policy-arn arn:aws:iam::aws:policy/service-role/AmazonEBSCSIDriverEKSClusterScopedPolicy \
  --profile eoe-hie

# eoe-test-codisc-AmazonEKS_EBS_CSI_DriverRole
aws iam attach-role-policy \
  --role-name eoe-test-codisc-AmazonEKS_EBS_CSI_DriverRole \
  --policy-arn arn:aws:iam::aws:policy/service-role/AmazonEBSCSIDriverEKSClusterScopedPolicy \
  --profile eoe-hie
```

#### Phase 3: Verify Migration

```bash
# Verify policy was detached and new policy attached
aws iam list-attached-role-policies \
  --role-name eoe-sde-codisc-AmazonEKS_EBS_CSI_DriverRole \
  --profile eoe-hie

aws iam list-attached-role-policies \
  --role-name eoe-test-codisc-AmazonEKS_EBS_CSI_DriverRole \
  --profile eoe-hie

# Both should show: AmazonEBSCSIDriverEKSClusterScopedPolicy
```

#### Phase 4: Verify Cluster Functionality

```bash
# Check EBS CSI controller pods are healthy
kubectl get pods -n kube-system -l app=ebs-csi-controller -o wide

# Attempt PVC creation to verify EBS provisioning works
kubectl apply -f - <<EOF
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: ebs-claim-test
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: ebs-sc
  resources:
    requests:
      storage: 4Gi
EOF

# Verify volume was created
kubectl get pvc ebs-claim-test
aws ec2 describe-volumes --filters "Name=tag:ebs.csi.aws.com/cluster,Values=<cluster-name>"
```

---

### Section 8: Post-Migration Verification

#### Checklist

- [ ] All 9 untagged volumes have been tagged with appropriate CSI tags
- [ ] Legacy `AmazonEBSCSIDriverPolicy` has been detached from both roles
- [ ] `AmazonEBSCSIDriverEKSClusterScopedPolicy` has been attached to both roles
- [ ] EBS CSI controller pods are running and healthy on both clusters
- [ ] New PVCs can be created and volumes are provisioned correctly
- [ ] Existing volumes remain accessible and mounted
- [ ] No errors in EBS CSI driver logs: `kubectl logs -n kube-system -l app=ebs-csi-controller`

#### Success Criteria

✅ Migration is complete when:

1. Both roles show `AmazonEBSCSIDriverEKSClusterScopedPolicy` as the only attached EBS CSI-related policy
2. EBS CSI driver pods show no restart loops or errors
3. PVC creation and volume provisioning functions normally
4. Existing persistent volumes remain in-use without errors

---

### Section 9: Rollback Procedure (If Required)

If issues arise post-migration, rollback is straightforward:

```bash
# Detach the new policy
aws iam detach-role-policy \
  --role-name <ROLE_NAME> \
  --policy-arn arn:aws:iam::aws:policy/service-role/AmazonEBSCSIDriverEKSClusterScopedPolicy \
  --profile eoe-hie

# Re-attach the legacy policy
aws iam attach-role-policy \
  --role-name <ROLE_NAME> \
  --policy-arn arn:aws:iam::aws:policy/service-role/AmazonEBSCSIDriverPolicy \
  --profile eoe-hie

# Restart EBS CSI controller pods to re-authenticate
kubectl delete pod -n kube-system -l app=ebs-csi-controller
```

---

### Section 10: Recommendations & Next Steps

#### Immediate Actions (This Week)

1. Tag all untagged EBS volumes—prevents breaking changes during deprecation
2. Schedule maintenance window—plan for eoe-test-codisc migration first (lower risk)
3. Communicate with stakeholders—brief teams managing these clusters

#### Short-term Actions (Next 2 Weeks)

1. Test migration on eoe-test-codisc—validate process and impacts
2. Iterate on findings—refine timing and approach based on test results
3. Execute production migration on eoe-sde-codisc—once test cluster confirms success

#### Long-term Best Practices

1. Establish tagging automation—ensure all future EBS volumes are tagged at creation
2. Audit IRSA configurations—quarterly review of all service account roles
3. Monitor AWS Health notifications—set up automated alerts for deprecation notices
4. Document cluster dependencies—maintain clear records of which roles support which clusters

---

### Appendix A: Raw Data References

Investigation Data Files:

- Volume metadata: `/tmp/volumes.json`
- Snapshot metadata: `/tmp/snapshots.json`
- All roles: `/tmp/all_roles.txt`

Key Cluster Identifiers:

- SDE Cluster OIDC ID: 23BDD27C5ECF85950BCEA129801871CB
- Test Cluster OIDC ID: BB08B20C015244FA577F249465CE5B2F

---

### Document Control

| Field | Value |
|-------|-------|
| Created By | Claude Code (Automated Investigation) |
| Created Date | 16 June 2026 |
| Last Updated | 16 June 2026 |
| Status | ✅ Investigation Complete—Action Required |
| Classification | Internal—AWS Infrastructure |

---

End of Report


---

## ADDENDUM: Critical Finding on vol-0f512bf32e7a77a79

### Volume Classification Update

**Volume:** vol-0f512bf32e7a77a79  
**Status:** ⚠️ **NOT EKS-RELATED — JUMPBOX/KALI INSTANCE**

#### Details

| Property | Value |
|----------|-------|
| **Attached Instance** | i-0c1ed2ec1275b511d |
| **Instance Name** | KALI |
| **Instance Type** | t2.xlarge |
| **Instance State** | **STOPPED** |
| **Volume State** | in-use |
| **Launch Time** | 9 July 2025, 09:20:03 UTC |
| **Device** | /dev/xvda (root volume) |

### Assessment

This volume is the **root volume** (`/dev/xvda`) of a stopped security testing instance (KALI), not a Kubernetes or EBS CSI-provisioned volume. 

**EBS CSI tagging requirement:** NOT APPLICABLE to this volume

The volume does not require the `ebs.csi.aws.com/cluster` tag because:
1. It is not provisioned or managed by EBS CSI driver
2. It is a node instance root volume, not a dynamically provisioned persistent volume
3. It exists outside the EKS cluster architecture

### Revised Volume Assessment

**Updated Untagged Volumes Count:** 8 (not 9)

| Volume ID | Category | Recommendation | CSI Tag Required |
|-----------|----------|-----------------|------------------|
| vol-0495ed05c42bdb021 | EKS Node / Medium Risk | Tag with cluster name | ✅ YES |
| vol-03c23f95447153a18 | EKS PVC / High Risk | Tag with cluster name | ✅ YES |
| vol-0834da1f3486fea9a | EKS Node / Medium Risk | Tag with cluster name | ✅ YES |
| vol-0a929e0fedba97937 | EKS Node / Medium Risk | Tag with cluster name | ✅ YES |
| **vol-0f512bf32e7a77a79** | **Non-EKS (KALI)** | **No action needed** | ❌ NO |
| vol-045d9a2ba2ce0059c | EKS Node / Medium Risk | Tag with cluster name | ✅ YES |
| vol-084a2470987348115 | EKS Node / Medium Risk | Tag with cluster name | ✅ YES |
| vol-0c9b7bbfc0f08c77d | EKS Node / Medium Risk | Tag with cluster name | ✅ YES |
| vol-0ec0cf31c76b3e885 | EKS PVC / High Risk | Tag with cluster name | ✅ YES |

### Revised Pre-Migration Action Items

**UPDATED:** Only **8 volumes require tagging** (not 9).

**High-Risk Volumes (2) — Immediate Tagging:**
```bash
# vol-03c23f95447153a18 (eoe-test-codisc PVC)
aws ec2 create-tags --resources vol-03c23f95447153a18 \
  --tags Key=ebs.csi.aws.com/cluster,Value=eoe-test-codisc \
  --region eu-west-2 --profile eoe-hie

# vol-0ec0cf31c76b3e885 (eoe-sde-codisc PVC)
aws ec2 create-tags --resources vol-0ec0cf31c76b3e885 \
  --tags Key=ebs.csi.aws.com/cluster,Value=eoe-sde-codisc \
  --region eu-west-2 --profile eoe-hie
```

**Medium-Risk Volumes (6) — Tag with EKS Cluster Identifier:**
```bash
for VOL in vol-0495ed05c42bdb021 vol-0834da1f3486fea9a vol-0a929e0fedba97937 \
           vol-045d9a2ba2ce0059c vol-084a2470987348115 vol-0c9b7bbfc0f08c77d; do
  CLUSTER=$(aws ec2 describe-volumes --volume-ids $VOL --region eu-west-2 \
    --profile eoe-hie --query 'Volumes[0].Tags[?Key==`eks:cluster-name`].Value' \
    --output text)
  [ -n "$CLUSTER" ] && aws ec2 create-tags --resources $VOL \
    --tags Key=ebs.csi.aws.com/cluster,Value=$CLUSTER \
    --region eu-west-2 --profile eoe-hie
done
```

**Non-EKS Volume (1) — NO ACTION REQUIRED:**
- vol-0f512bf32e7a77a79 (KALI instance root volume) — skip tagging

### Conclusion

The discovery of vol-0f512bf32e7a77a79 as a non-EKS volume **does not impact the EBS CSI driver migration timeline or scope**. The migration can proceed as planned with only the 8 EKS-related volumes requiring tagging.