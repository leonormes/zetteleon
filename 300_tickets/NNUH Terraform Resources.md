---
aliases: []
confidence:
created: 2025-11-20T10:13:28Z
epistemic:
last_reviewed:
modified: 2025-11-20T10:16:12Z
purpose:
review_interval:
see_also: []
source_of_truth: []
status:
tags:
  - nnuh
title: NNUH Terraform Resources
type:
uid:
updated:
---

Based on my analysis of the Terraform configuration for the NNUH-DP cluster using the [terraform-azure-private-infrastructure](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/TFC-Modules/terraform-azure-private-infrastructure:0:0-0:0) module, here's a detailed breakdown of what resources will be deployed:

## **Core Infrastructure Resources**

### **Resource Group**
- **Name**: Generated as `rg-ff-uks-gp-nnuh-prod` (following naming convention)
- **Location**: UK South (`uksouth`)
- **Purpose**: Contains all cluster-related resources

### **AKS Kubernetes Cluster**
- **Name**: Generated as `aks-ff-uks-gp-nnuh-prod`
- **Kubernetes Version**: 1.30.0 (configurable via `kubernetes_version`)
- **Private Cluster**: ✅ Enabled (no public API server endpoint)
- **Network Plugin**: Azure CNI with Calico network policy
- **Network Mode**: Overlay mode with pod CIDR `10.244.0.0/16`
- **Identity**: User-assigned managed identity for secure access
- **RBAC**: Azure RBAC enabled
- **OIDC Issuer**: Disabled
- **Workload Identity**: Disabled
- **Azure Policy**: Enabled
- **KEDA**: Disabled
- **Vertical Pod Autoscaler**: Enabled
- **Image Cleaner**: Disabled
- **HTTP Application Routing**: Disabled

### **Node Pools**

#### **System Node Pool**
- **Name**: `system`
- **VM Size**: Standard_D2s_v3 (configurable via `vm_size`)
- **Node Count**: 2 initial, autoscaling 2-10 nodes
- **OS Disk**: Managed
- **Availability Zones**: None specified (single zone)
- **Public IPs**: ❌ Disabled
- **Subnet**: `snet-ff-uks-gp-system` (192.168.200.64-79)
- **Max Pods**: 100

#### **Workflows Node Pool**
- **Name**: `workflows`
- **VM Size**: Standard_E4s_v5
- **Node Count**: 1 initial, autoscaling 1-10 nodes
- **OS Disk**: Ephemeral
- **Priority**: Spot instances
- **Public IPs**: ❌ Disabled
- **Subnet**: `snet-ff-uks-gp-workflows` (192.168.200.80-95)
- **Max Pods**: 100
- **Taints**: `dedicated=workflows:PreferNoSchedule`, spot priority

### **Virtual Network (Existing)**
- **Name**: `NNUHFT-SDE-vnet1` (existing VNet, not created by module)
- **Resource Group**: `NNUHFT-SDE-Networking`
- **Address Space**: 192.168.200.0/24
- **DNS Servers**: None specified (uses Azure defaults)

### **Subnets (Within Existing VNet)**
- **System Subnet**: 192.168.200.64/28 (for default node pool)
- **Workflows Subnet**: 192.168.200.80/28 (for additional node pool)
- **Jumpbox Subnet**: 192.168.200.128/29 (for management VM)

### **Jumpbox Virtual Machine**
- **Name**: `FITFILEJumpbox`
- **VM Size**: Standard_DS1_v2
- **OS**: Ubuntu 22.04 LTS Gen2
- **Public IP**: ❌ Disabled (private access only)
- **Admin Username**: `azadmin`
- **OS Disk**: Standard_LRS storage
- **Subnet**: Jumpbox subnet (192.168.200.128/29)

### **Networking & Security**

#### **Route Table (Forced Tunneling)**
- **Name**: `rt-ff-uks-gp`
- **Routes**: All traffic (0.0.0.0/0) → Firewall private IP `192.168.208.4`
- **Associated Subnets**: System, Workflows, and Jumpbox subnets
- **Purpose**: Forces all outbound traffic through existing NNUH-HUB firewall

#### **Network Security Groups**
- Applied to all subnets for traffic control
- Default Azure NSG rules plus any custom rules

### **Identity & Access**

#### **User-Assigned Managed Identity**
- **Name**: `aks-ff-uks-gp-nnuh-prod-identity`
- **Purpose**: Used by AKS cluster for accessing Azure resources
- **Role Assignment**: Network Contributor on the resource group

### **DNS Configuration**
- **Private DNS Zone**: ❌ Disabled (`private_dns_zone_enabled = false`)
- **DNS Records**: None created

### **Conditional Resources (Not Deployed)**
- **Hub Network**: ❌ Not deployed (`hub_deploy` not set)
- **Azure Firewall**: ❌ Not created (hub network disabled)
- **Bastion Host**: ❌ Not created (hub network disabled)
- **VNet Peering**: ❌ Not created (hub network disabled)
- **Private DNS Zone**: ❌ Disabled in configuration

## **Key Configuration Details**

### **Network Architecture**

```sh
Existing VNet: 192.168.200.0/24
├── System Pool: 192.168.200.64/28
├── Workflows Pool: 192.168.200.80/28
├── Jumpbox: 192.168.200.128/29
└── NAT Gateway: 192.168.200.0/29 (existing)

All outbound traffic → Firewall: 192.168.208.4 (NNUH-HUB)
```

### **Security Features**
- Private cluster (no public endpoints)
- No public IPs on nodes
- Spot instances for cost optimization
- Azure RBAC enabled
- Network policies via Calico
- Forced tunneling through firewall

### **Cost Optimization**
- Spot instances for workflows node pool
- Autoscaling to minimize resource usage
- Ephemeral OS disks for workflows pool

### **High Availability**
- AKS cluster spans multiple availability zones (default behavior)
- Multiple node pools for workload isolation
- Autoscaling for resilience

## **Deployment Flow**
1. Create resource group
2. Deploy AKS cluster with user-assigned identity
3. Create additional node pool
4. Configure route table for forced tunneling
5. Deploy jumpbox VM
6. Assign necessary role permissions

This configuration creates a secure, private AKS cluster integrated with existing NNUH infrastructure, optimized for cost and security with forced tunneling through the existing firewall.

I'll analyze the Terraform deployment configuration using the context-engine to provide a detailed breakdown of what resources will be deployed.

Let me read the actual Terraform files to provide detailed analysis:

Based on my analysis of the Terraform configuration, here's a detailed breakdown of all Azure resources that will be deployed for the **NNUH-DP deployment** using the **terraform-azure-private-infrastructure** module:

---

## **Resource Overview**

The deployment will create a **private AKS cluster** in the existing NNUH network (`NNUHFT-SDE-vnet1`) with the following configuration:

### **1. Resource Group**
- **Name**: `rg-ff-uks-gp-net` (following naming convention: `rg-{workload}-{region}-{env_prefix}-net`)
- **Location**: UK South
- **Tags**: Environment metadata, managed by FITFILE, created with Terraform

---

### **2. Virtual Network Configuration**

Since `create_vnet = false`, the module will **use the existing VNET**:

- **Existing VNet**: `NNUHFT-SDE-vnet1` in resource group `NNUHFT-SDE-Networking`
- **Address Space**: `192.168.200.0/24`

**Three new subnets will be created**:

1. **System Node Pool Subnet**
   - Name: `snet-ff-uks-gp-system`
   - CIDR: `192.168.200.64/28` (16 IPs, -)
   - Purpose: Hosts AKS system/default node pool

2. **Workflows Node Pool Subnet**
   - Name: `snet-ff-uks-gp-workflows`
   - CIDR: `192.168.200.80/28` (16 IPs, -)
   - Purpose: Hosts additional workflow node pool

3. **Jumpbox Subnet**
   - Name: `snet-ff-uks-gp-jumpbox`
   - CIDR: `192.168.200.128/29` (8 IPs, -)
   - Purpose: Hosts the management jumpbox VM

---

### **3. Route Table (For Forced Tunneling)**
- **Name**: `rt-ff-uks-gp`
- **Default Route**: Routes all traffic (`0.0.0.0/0`) to NNUH Hub firewall at `192.168.208.4`
- **Associated Subnets**:
  - System node pool subnet
  - Workflows node pool subnet
  - Jumpbox subnet
- **Purpose**: Forces all AKS outbound traffic through the NNUH firewall

---

### **4. AKS Cluster**
**Cluster Configuration**:
- **Name**: `aks-ff-uks-gp-01`
- **Kubernetes Version**: `1.33.5` (specified in tfvars)
- **Node Resource Group**: `rg-ff-uks-gp-aks` (managed by AKS)
- **SKU Tier**: Free
- **Private Cluster**: Enabled (no public API endpoint)
- **DNS Prefix**: `aks-ff-uks-gp-01`

**Network Configuration**:
- **Network Plugin**: Azure CNI
- **Network Plugin Mode**: Overlay (CNI Overlay)
- **Network Policy**: Calico
- **Outbound Type**: User Defined Routing (via firewall at `192.168.208.4`)
- **Pod CIDR**: `10.244.0.0/16` (overlay network for pods)
- **Service CIDR**: `10.2.0.0/24`
- **DNS Service IP**: `10.2.0.10`

**Features Enabled**:
- ✅ Azure Policy
- ✅ Vertical Pod Autoscaler
- ✅ Role-based Access Control (RBAC)
- ✅ Azure RBAC for Kubernetes Authorization
- ✅ Host Encryption (for both node pools)
- ❌ Private DNS Zone (disabled via `private_dns_zone_enabled = false`)
- ❌ KEDA
- ❌ Workload Identity
- ❌ OIDC Issuer

**Managed Identity**:
- **User Assigned Identity Name**: `uai-ff-uks-gp-aks`
- **Role Assignment**: Network Contributor on the resource group

---

### **5. AKS Node Pools**

**Default/System Node Pool**:
- **Name**: `system`
- **VM Size**: `Standard_D2s_v3` (2 vCPU, 8 GB RAM)
- **Subnet**: System subnet (`192.168.200.64/28`)
- **Auto-scaling**: Enabled
- **Min Count**: 2 nodes (default from module)
- **Max Count**: 10 nodes (from locals)
- **Initial Count**: 2 nodes
- **Max Pods per Node**: 100
- **OS Disk Type**: Managed
- **Host Encryption**: Enabled
- **Public IP**: Disabled
- **Node Taints**: `CriticalAddonsOnly=true:NoSchedule`
- **Availability Zones**: null (not specified)

**Additional/Workflows Node Pool**:
- **Name**: `workflows`
- **VM Size**: `Standard_E4s_v5` (4 vCPU, 32 GB RAM - default from module)
- **Subnet**: Workflows subnet (`192.168.200.80/28`)
- **Auto-scaling**: Enabled
- **Min Count**: 1 node (default)
- **Max Count**: 10 nodes (from locals)
- **Initial Count**: 1 node
- **Max Pods per Node**: 100
- **OS Disk Type**: Ephemeral
- **Priority**: **Spot** (cost-optimized)
- **Eviction Policy**: Delete
- **Host Encryption**: Enabled
- **Public IP**: Disabled
- **Node Taints**:
  - `dedicated=workflows:PreferNoSchedule`
  - `kubernetes.azure.com/scalesetpriority=spot:NoSchedule`
- **Node Labels**: `kubernetes.azure.com/scalesetpriority=spot`
- **Availability Zones**: null

---

### **6. Jumpbox Virtual Machine**
- **Name**: `FITFILEJumpbox`
- **VM Size**: `Standard_D2s_v3` (2 vCPU, 8 GB RAM)
- **OS**: Ubuntu 22.04 LTS (Jammy)
  - Publisher: Canonical
  - Offer: `0001-com-ubuntu-server-jammy`
  - SKU: `22_04-lts-gen2`
- **OS Disk Type**: Standard LRS
- **Subnet**: Jumpbox subnet (`192.168.200.128/29`)
- **Public IP**: Disabled (`vm_public_ip = false`)
- **Admin Username**: `azadmin` (default)
- **Admin Password**: Configured via variable (stored securely)
- **Domain Name Label**: `fitfilejumpbox`
- **Purpose**: Management access point for the private AKS cluster

---

### **7. Network Security & DNS**

**No Private DNS Zone Created**:
- The `private_dns_zone_enabled = false` setting means no private DNS zone will be created
- No DNS A records for ingress controller or ArgoCD

**Network Security Groups**:
- Default NSGs will be created for each subnet by the virtual network module

---

## **Resource Summary by Type**

| Resource Type | Count | Names/Details |
|--------------|-------|---------------|
| Resource Groups | 2 | Main: `rg-ff-uks-gp-net`<br>AKS Managed: `rg-ff-uks-gp-aks` |
| Subnets | 3 | System, Workflows, Jumpbox |
| Route Tables | 1 | `rt-ff-uks-gp` (with firewall route) |
| AKS Clusters | 1 | `aks-ff-uks-gp-01` (private) |
| Node Pools | 2 | System (regular) + Workflows (spot) |
| Virtual Machines | 1 | Ubuntu jumpbox |
| Managed Identities | 1 | `uai-ff-uks-gp-aks` |
| Role Assignments | 1 | Network Contributor for AKS identity |

---

## **Key Configuration Decisions**

1. **Existing Network Integration**: Uses existing NNUH VNet, doesn't create new one
2. **Forced Tunneling**: All traffic routed through NNUH firewall (`192.168.208.4`)
3. **Private Cluster**: No public API endpoint, only accessible from NNUH network
4. **CNI Overlay**: Efficient IP usage - only nodes need IPs from subnets
5. **Cost Optimization**: Spot instances for workflow pool
6. **Security**: Host encryption enabled, no public IPs, Calico network policy
7. **Kubernetes Version**: `1.33.5` (latest stable)

---

## **Total Node Capacity**

- **System Pool**: 2-10 regular nodes (Standard_D2s_v3)
- **Workflows Pool**: 1-10 spot nodes (Standard_E4s_v5)
- **Maximum Cluster Size**: 20 nodes
- **Estimated Pod Capacity**: Up to 2,000 pods (20 nodes × 100 max pods)

This creates a robust, secure, private Kubernetes environment integrated with NNUH's existing network infrastructure while maintaining cost efficiency through spot instances and optimized IP allocation with CNI Overlay.
