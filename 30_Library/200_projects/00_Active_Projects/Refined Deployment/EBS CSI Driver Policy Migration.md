---
created: 2026-04-21T07:31:46+00:00
modified: 2026-04-21T07:32:43+00:00
---
*Shared Message from Pieces (https://pieces.app) by Leon Ormes (leonormes@gmail.com) on Tuesday Apr 21, 2026 - 8:31 AM*
---
## EBS CSI Driver Policy Migration — FITFILE Action Summary

This thread (active this morning at ~7:53 AM) covers an AWS security notification and Ollie Rushton's detailed reply. Here's the consolidated picture:

---

### Do We Use the EBS CSI Driver at EoE? ✅ Yes

Your Terraform config (visible in GitKraken on March 27) explicitly provisions it:
```hcl
resource "aws_eks_addon" "ebs_driver_addon" {
  cluster_name = aws_eks_cluster.this.name
  addon_name   = "aws-ebs-csi-driver"
  addon_version = "v1.48.0-eksbuild.2"
  ...
  service_account_role_arn = aws_iam_role.ebs_csi_role.arn
}
```
This means FITFILE **is affected** by this notification and action is required.

---

### Recommended Target Policy

AWS offers two new options. Given your multi-cluster setup, **`AmazonEBSCSIDriverEKSClusterScopedPolicy`** is the right choice — it restricts permissions to resources belonging to a specific EKS cluster, preventing cross-cluster access.

---

### Full Migration Checklist

> ⚠️ **Critical: Complete Step 1 (tagging) before making any IAM changes.** This is the most important sequencing point Ollie raised.

| #   | Action                                                                                                 | Notes                                                                                                             |
| --- | ------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------- |
| 1   | **Audit & tag existing EBS volumes and snapshots** with `ebs.csi.aws.com/cluster-name: <cluster-name>` | May already be applied — verify first. **Do this before anything else.**                                          |
| 2   | **Move from IRSA to EKS Pod Identity** for the EBS CSI Driver identity                                 | The `eks-pod-identity-agent` addon is already installed (`v1.3.8-eksbuild.2`) — just not wired up for EBS CSI yet |
| 3   | **Update `ebs_csi_assume_role_policy`** to add `sts:TagSession` (and potentially `sts:AssumeRole`)     | Required for Pod Identity session tagging                                                                         |
| 4   | **Upgrade the EBS CSI Driver** to the latest stable version                                            | Currently on `v1.48.0-eksbuild.2` — check for newer release                                                       |
| 5   | **Attach `AmazonEBSCSIDriverEKSClusterScopedPolicy`** to the IAM role used by the driver               |                                                                                                                   |
| 6   | **Detach the old `AmazonEBSCSIDriverPolicy`**                                                          | ⚠️ Do not leave both attached — the old policy's broader permissions will remain in effect if you do              |

---

### Scope of Change

This needs to be applied to **both**:
- **HIE Production Node**
- **HIE Test Node**

---

### Testing Strategy

**Yes, you should test this first.** Ollie is right that this migration is error-prone (identity changes + tagging + addon upgrades in sequence). The recommendation is:

1. **Spin up a temporary test cluster** using a tweaked version of the existing HIE Terraform (`hie-test-34` workspace on [HCP Terraform](https://app.terraform.io/app/FITFILE-Platforms/workspaces/hie-test-34/runs/run-rf5j8Bg8HmNuq3TA))
2. Run through the full migration on that cluster
3. Validate that PVCs provision and mount correctly
4. Then apply to HIE Test → HIE Production in sequence

---

### Immediate Next Steps

1. **Confirm with Keiran** when Health Innovation East plans to enforce the policy change — this sets your deadline
2. **Check whether EBS volumes already have the cluster-name tag** in the `eoe-sde-codisc` account (Account ID: 135808916559, eu-west-2)
3. **Assign ownership** — Ollie has the most context here and has volunteered the path forward; you'll likely need to own the Terraform changes for Pod Identity wiring given your platform role