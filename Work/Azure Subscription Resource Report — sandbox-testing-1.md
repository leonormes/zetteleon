---
created: 2026-04-30T12:34:36+00:00
modified: 2026-05-26T11:43:56+00:00
title: Azure Subscription Resource Report — sandbox-testing-1
---

## Azure Subscription Resource Report—sandbox-testing-1

Subscription ID: `7bbc8ae5-1710-48ab-ab83-59b52bd0de1a`

Location: UK South

Report Date: 2026-04-30

---

### Resource Groups

| Name | Purpose |
|------|---------|
| `rg-ff-uks-gp-net` | Network infrastructure + AKS cluster resource |
| `rg-ff-uks-gp-aks` | AKS-managed resources (node pools, NSGs, identities) |
| `pentest-1-backup-rg` | AKS Backup Vault |
| `pentest-1-backup-snapshots-rg` | Disk snapshots from backup |
| `NetworkWatcherRG` | Auto-created by Azure |

---

### AKS Cluster (Primary Resource)

Cluster: `aks-ff-uks-gp-1` in `rg-ff-uks-gp-net`

This is a fully private cluster—the kube-apiserver is not publicly reachable. Key characteristics:

- Private endpoint: `kube-apiserver` with a dedicated NIC in `rg-ff-uks-gp-aks`
- Private DNS zone: `f985395b-cb31-425a-8c2e-6cea863534f0.privatelink.uksouth.azmk8s.io` resolves the API server internally
- Node Pools (VMSSs):
  - `aks-system-65569669-vmss`—system pool
  - `aks-workflows-10382344-vmss`—user/workflows pool
- Persistent volumes: 4 PVC disks attached (`pvc-*`), meaning workloads with persistent storage are running
- AKS Managed Identity: `uai-ff-uks-gp-aks`—used by the cluster for VMSS upgrades and operations
- Additional Identities: agent pool identity, Azure Policy addon identity, and one extension identity

---

### Supporting Infrastructure

#### Networking (`rg-ff-uks-gp-net`)

- VNet: `vnet-ff-uks-gp-1`—single VNet housing all subnets
- NSGs: Separate NSGs for system pool, workflows pool, and jumpbox subnets; AKS also manages its own agent pool NSG
- Outbound IP: `aksoutip`—dedicated public IP for AKS egress traffic
- Internal Load Balancer: `kubernetes`—AKS-managed, handles in-cluster service traffic

#### Access to Private Cluster

- Azure Bastion: `bas-ff-uks-gp` with `bas-ff-uks-gpPublicIp`—browser-based SSH/RDP without exposing a public IP
- Jumpbox VM: `FITFILEJumpbox`—VM inside the VNet with NIC, NSG, and OS disk; the primary way admins reach the cluster

#### Backup

- Backup Vault: `aksbackupvault` (in `pentest-1-backup-rg`)
- Storage Account: `stffuksgp1backup`—backup data store, accessed via private endpoint `pe-stffuksgp1backup-blob` (no public blob access)
- Private DNS Zone: `privatelink.blob.core.windows.net`—resolves storage privately
- Snapshot: One disk snapshot exists in `pentest-1-backup-snapshots-rg`

#### Cost-Control Automation

- Automation Account: `auto-sandbox-cluster`
- Runbook: `ClusterChangeState`—starts and stops the cluster on a schedule; confirmed started today at 07:01 UTC, fully running by 07:10 UTC

---

### Activity Log—Today's Startup (2026-04-30, ~07:00–07:40 UTC)

The cluster was stopped overnight and started this morning. The startup was clean with transient health events that all resolved.

| Time (UTC) | Event |
|---|---|
| 07:01 | `Start Managed Cluster` initiated |
| 07:01–07:06 | Load balancer rebuilt; temporary outbound IP deleted; VMSS nodes recreated |
| 07:04–07:12 | Health events Active/Critical briefly on VMSS VMs 34, 35, 36, 37 and the `kubernetes` load balancer |
| 07:06–07:12 | System VMSS nodes came healthy; upgrades applied by `uai-ff-uks-gp-aks` |
| 07:10 | `Start Managed Cluster` Succeeded |
| 07:12–07:13 | Manual VMSS upgrades completed; `AKSLinuxExtension` applied to both pools |
| 07:19 | Load balancer health event Resolved |
| 07:28–07:30 | Last VMSS node health events Resolved |

All events resolved. Cluster is healthy. One policy audit warning fired against the workflows VMSS during startup—not blocking, but worth noting if Azure Policy compliance is tracked.

---

### Access & Role Assignments

| Principal | Type | Role | Scope |
|---|---|---|---|
| Jon Bradshaw | User | Owner | Subscription + Sandbox MG |
| Robin Mofakham | User | Contributor + constrained Owner | Subscription + Sandbox MG |
| Leon Ormes | User | Contributor + MG Contributor | Subscription + Sandbox MG |
| Oliver Rushton | User | Contributor | Subscription |
| DevOpsEngineers | Group | User Access Administrator | Subscription |
| FITFILE Terraform Cloud Provisioner | Service Principal | Contributor + constrained UAA | Subscription |
| Gareth Hailes | User | Security Admin | Management Group |
| Richard J. Brain (Procheckup—external guest) | User | Reader + Security Reader + AKS Cluster User | Subscription |

Pentester access: Richard Brain from Procheckup has read-only access plus AKS Cluster User—enough to enumerate resources and get cluster credentials, but no write permissions.

Terraform provisioner: The User Access Administrator role is conditioned to only assign two specific custom role IDs, preventing privilege escalation.

---

### Summary

This is a well-structured private AKS environment designed to mirror customer private clusters:

- Cluster is completely private (no public API endpoint), accessed only via the jumpbox through Bastion
- Two node pools (system + workflows), with 4 PVC disks indicating persistent workloads
- Cluster is cost-managed via start/stop automation—stopped overnight, started each morning
- AKS Backup is configured with private storage access and snapshot retention
- Pentester access (Procheckup) is appropriately scoped—read-only plus cluster user, no write permissions
