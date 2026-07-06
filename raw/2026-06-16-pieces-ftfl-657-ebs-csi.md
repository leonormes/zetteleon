---
created: 2026-06-16T15:15:00+00:00
modified: 2026-07-04T10:49:23+00:00
permalink: llmeon/raw/2026-06-16-pieces-ftfl-657-ebs-csi
pieces_ids: [934d6bb2-9bfd-4836-a886-89c2c091d359, badfd52a-2ef5-42be-a345-e287cab55456, c44adf14-6708-4d88-86d8-7ab8d7b5b861, eed0c8e5-7c10-44f5-86db-9e4e6570eebd, f31e398d-b4bb-48cc-a0a6-affea218e982, f370484e-fa2d-4380-aa4e-425ba24654b8]
source: pieces-ltm
tags: [aks, aws, bastion, ebs-csi, infrastructure, pieces, raw]
title: 2026-06-16-pieces-ftfl-657-ebs-csi
---

## Session A: FTFL-657—Bastion Direct to Private AKS (13:41-15:12 UTC)

### User Query (13:41 UTC—Pieces: eed0c8e5)

> we deploy IaC managed infrastructure to private networks. We have to use a bastion -> jumpbox to then access the k8s cluster to complete the deployment. I have a ticket that says Investigate Bastion Direct to Private AKS cluster. Trying to go from my local machine to run commands against the private AKS API. We should investigate the possibility of using Bastion Direct to Private AKS cluster to avoid Jumpbox password/SSH connectivity (and costs), as well as improving the overall architecture. The ticket references another ticket with more details
>
> FITFILEJumpbox (Ubuntu 22.04 LTS Gen2) allows password-based SSH authentication. Admin user: azadmin. The VM is accessible via Azure Bastion, but password authentication leaves the VM vulnerable to bruteforce attacks if any alternate access path exists.
>
> Prowler FAIL: SSH key auth not enforced
>
> Microsoft Defender for Cloud recommendation: "Authentication to Linux machines should require SSH keys"
>
> What is Bastion Direct? Is it a better option for us?

### Agent Delivered Summary (14:00 UTC—Pieces: c44adf14)

Key findings from the agent's LTM research:

- FTFL-657—Spike (Low) to investigate Bastion Direct to private AKS cluster. Assigned to Leon. Timebox: 1 day. Part of FITFILE Sprint 22 (10-17 Jun 2026). Parent: FTFL-579 (EntraFF-22 Jumpbox VM—Password Authentication Enabled, CVSS 7.5).
- Current architecture: Local machine → Azure Bastion (`bas-ff-uks-gp`, Standard SKU, tunneling enabled) → FITFILEJumpbox (azadmin, password auth) → SOCKS5 proxy → private AKS API.
- Jumpbox details: `FITFILEJumpbox` (Ubuntu 22.04 LTS Gen2) in subscription `7bbc8ae5-1710-48ab-ab83-59b52bd0de1a` (Testing), resource group `rg-ff-uks-gp-net`.
- Sandbox cluster: `aks-ff-uks-gp-1` in the same subscription.
- Bastion Direct approach: Use Azure Bastion native client tunneling (preview) to connect directly to the AKS API server's private endpoint on port 443, eliminating the jumpbox middleman entirely.
- Test plan: Deploy a test cluster without jumpbox dependency, use `az network bastion tunnel` directly to AKS private endpoint, validate kubectl access.
- Bootstrapping context: Investigating how to automate ArgoCD bootstrapping for private AKS clusters without manual jumpbox steps.

## Session B: AWS EBS CSI Driver—EOE Policy Detach Issue (15:12 UTC—Pieces: 934d6bb2)

### User Query

> we need to ask Kieran to help make this change. aws iam detach-role-policy \
> --role-name eoe-test-codisc-AmazonEKS_EBS_CSI_DriverRole \
> --policy-arn arn:aws:iam::aws:policy/service-role/AmazonEBSCSIDriverPolicy \
> --profile eoe-hie

### Error & Analysis

Access Denied when calling `iam:DetachRolePolicy`. The user's role `AWSReservedSSO_DiscoveryEngineeringAccess_…` has an explicit DENY on `iam:DetachRolePolicy` via `DiscoveryEngineeringAccessPolicyPart1`.

Options discussed:

1. Use a higher-privilege role (AdministratorAccess, AWSPowerUserAccess)
2. Request Kieran to execute the detach or update the policy
3. Use CloudFormation/IaC with broader permissions

User conclusion: "Either we need to update that role to allow me to detach or he removes them? What is the easier safer option? Write an email describing the problem"
