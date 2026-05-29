# Wiki: Private AKS Cluster — `aks-ff-uks-gp-1`

> **Subscription:** Testing (`7bbc8ae5-1710-48ab-ab83-59b52bd0de1a`)
> **Region:** UK South
> **Primary Resource Group:** `rg-ff-uks-gp-net` (cluster) / `rg-ff-uks-gp-aks` (managed node resources)

---

## Table of Contents

1. [Architecture Overview](#1-architecture-overview)
2. [Resource Inventory](#2-resource-inventory)
3. [Why It's Private — The Core Concepts](#3-why-its-private--the-core-concepts)
4. [Resource Deep-Dive: What Each Thing Does](#4-resource-deep-dive-what-each-thing-does)
5. [Accessing the Cluster API From Your Laptop](#5-accessing-the-cluster-api-from-your-laptop)
6. [Backup Infrastructure](#6-backup-infrastructure)
7. [Automation](#7-automation)
8. [Network Security Groups Reference](#8-network-security-groups-reference)

---

## 1. Architecture Overview

```
Your Laptop
    │
    │  SSH or RDP (port 22 / 3389)
    ▼
┌─────────────────────────────────────────────┐
│  Azure Bastion (bas-ff-uks-gp)              │  ← HTTPS-only, no public SSH
│  Public IP: bas-ff-uks-gpPublicIp           │
└─────────────┬───────────────────────────────┘
              │  Private network hop
              ▼
┌─────────────────────────────────────────────┐
│  Jumpbox VM (FITFILEJumpbox)                │  ← Internal VM, no public IP
│  NIC: FITFILEJumpboxNic                     │
│  vNet: vnet-ff-uks-gp-1                     │
└─────────────┬───────────────────────────────┘
              │  kubectl / az aks get-credentials
              ▼
┌─────────────────────────────────────────────┐
│  Private Endpoint (kube-apiserver)          │  ← API server exposed only on private IP
│  Private DNS: *.privatelink.uksouth.azmk8s.io│
└─────────────┬───────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────┐
│  AKS Cluster: aks-ff-uks-gp-1               │
│  Node Pools: system VMSS + workflows VMSS   │
│  vNet injected into vnet-ff-uks-gp-1        │
└─────────────────────────────────────────────┘
```

**The key principle:** The Kubernetes API server has no public endpoint. It is only reachable via the Private Endpoint (`kube-apiserver`) which has a private IP address inside the VNet. Your laptop cannot reach that IP directly — you must go through Bastion → Jumpbox → kubectl.

---

## 2. Resource Inventory

All 37 resources, grouped by function.

### 2.1 Core Cluster

| Name | Type | Resource Group |
|------|------|---------------|
| `aks-ff-uks-gp-1` | Kubernetes service | `rg-ff-uks-gp-net` |
| `aks-system-65569669-vmss` | Virtual machine scale set | `rg-ff-uks-gp-aks` |
| `aks-workflows-10382344-vmss` | Virtual machine scale set | `rg-ff-uks-gp-aks` |
| `kubernetes` | Load balancer | `rg-ff-uks-gp-aks` |
| `pip-ff-uks-gp-1` | Public IP address | `rg-ff-uks-gp-aks` |
| `aksoutip` | Public IP address | `rg-ff-uks-gp-net` |

> **Note on the Public IPs:** These are for *egress* from the cluster (outbound internet traffic from pods), **not** for inbound access to the API server. The API server itself has no public IP.

### 2.2 Private API Access (makes it "private")

| Name | Type | Resource Group |
|------|------|---------------|
| `kube-apiserver` | Private endpoint | `rg-ff-uks-gp-aks` |
| `kube-apiserver.nic.3363d41a-...` | Network interface (for private endpoint) | `rg-ff-uks-gp-aks` |
| `f985395b-...privatelink.uksouth.azmk8s.io` | Private DNS zone | `rg-ff-uks-gp-aks` |

### 2.3 Access Path (Bastion + Jumpbox)

| Name | Type | Resource Group |
|------|------|---------------|
| `bas-ff-uks-gp` | Bastion | `rg-ff-uks-gp-net` |
| `bas-ff-uks-gpPublicIp` | Public IP address | `rg-ff-uks-gp-net` |
| `FITFILEJumpbox` | Virtual machine | `rg-ff-uks-gp-net` |
| `FITFILEJumpboxNic` | Network interface | `rg-ff-uks-gp-net` |
| `FITFILEJumpboxNsg` | Network security group | `rg-ff-uks-gp-net` |
| `FITFILEJumpboxOsDisk` | Disk | `RG-FF-UKS-GP-NET` |

### 2.4 Networking

| Name | Type | Resource Group |
|------|------|---------------|
| `vnet-ff-uks-gp-1` | Virtual network | `rg-ff-uks-gp-net` |
| `nsg-ff-uks-gp-jumpbox` | Network security group | `rg-ff-uks-gp-net` |
| `nsg-ff-uks-gp-system` | Network security group | `rg-ff-uks-gp-net` |
| `nsg-ff-uks-gp-workflows` | Network security group | `rg-ff-uks-gp-net` |
| `aks-agentpool-14508117-nsg` | Network security group | `rg-ff-uks-gp-aks` |
| `NetworkWatcher_uksouth` | Network Watcher | `NetworkWatcherRG` |
| `privatelink.blob.core.windows.net` | Private DNS zone | `rg-ff-uks-gp-net` |

### 2.5 Identities

| Name | Type | Resource Group | Purpose |
|------|------|---------------|---------|
| `aks-ff-uks-gp-1-agentpool` | Managed Identity | `rg-ff-uks-gp-aks` | Node pool identity (kubelet) |
| `azurepolicy-aks-ff-uks-gp-1` | Managed Identity | `rg-ff-uks-gp-aks` | Azure Policy add-on |
| `ext-21a39791cf3f...-aks-ff-uks-gp-1` | Managed Identity | `rg-ff-uks-gp-aks` | Extension/add-on identity |
| `uai-ff-uks-gp-aks` | Managed Identity | `rg-ff-uks-gp-net` | User-assigned cluster identity |

### 2.6 Storage / PVCs

| Name | Type | Resource Group |
|------|------|---------------|
| `pvc-0069703d-...` | Disk | `RG-FF-UKS-GP-AKS` |
| `pvc-38af7ba8-...` | Disk | `RG-FF-UKS-GP-AKS` |
| `pvc-c1c3b589-...` | Disk | `RG-FF-UKS-GP-AKS` |
| `pvc-e2a8d82b-...` | Disk | `RG-FF-UKS-GP-AKS` |

> These are Azure Managed Disks provisioned automatically by the AKS CSI driver for PersistentVolumeClaims.

### 2.7 Backup

| Name | Type | Resource Group |
|------|------|---------------|
| `sbox-aks-backup-vault` | Backup vault | `pentest-1-backup-rg` |
| `sboxaksbackup1a2b3` | Storage account | `pentest-1-backup-rg` |
| `stffuksgp1backup` | Storage account | `rg-ff-uks-gp-net` |
| `pe-sboxaksbackup1a2b3-blob` | Private endpoint | `pentest-1-backup-rg` |
| `pe-sboxaksbackup1a2b3-blob.nic.e74e...` | Network interface | `pentest-1-backup-rg` |

### 2.8 Automation

| Name | Type | Resource Group |
|------|------|---------------|
| `auto-sandbox-cluster` | Automation Account | `rg-ff-uks-gp-net` |
| `ClusterChangeState` | Runbook | `rg-ff-uks-gp-net` |

---

## 3. Why It's Private — The Core Concepts

### 3.1 What "private cluster" means

When you create a standard AKS cluster, the Kubernetes API server (the thing `kubectl` talks to) gets a public FQDN and a public IP. Anyone on the internet can attempt to reach it.

A **private cluster** removes that public endpoint entirely. The API server is only addressable via a **Private Endpoint** — a network interface with a private IP inside your VNet.

### 3.2 The three pieces that enforce privacy

**1. Private Endpoint (`kube-apiserver`)**

This is a network interface (`kube-apiserver.nic.3363d41a-...`) with a private IP in `vnet-ff-uks-gp-1`. It's a "wire" from inside your VNet directly to the managed AKS control plane that Microsoft runs. Traffic never leaves the Azure backbone.

**2. Private DNS Zone (`f985395b-cb31-425a-8c2e-6cea863534f0.privatelink.uksouth.azmk8s.io`)**

When `kubectl` or `az aks get-credentials` gives you a kubeconfig, the API server address is an FQDN like `aks-ff-uks-gp-1-abc123.hcp.uksouth.azmk8s.io`. For a private cluster, this resolves to a **private IP** (from the private endpoint), not a public one.

This Private DNS Zone contains the A record that maps that FQDN → private IP. It is linked to `vnet-ff-uks-gp-1`. Any VM inside that VNet that does a DNS lookup gets the private IP back.

Your laptop's DNS resolver is **not** connected to this zone — which is exactly why you can't run `kubectl` directly from your laptop.

**3. No public FQDN / API server access policy**

The cluster is configured at creation time with `--enable-private-cluster`. Azure simply does not create a public DNS record or expose the API server on the internet.

---

## 4. Resource Deep-Dive: What Each Thing Does

### `vnet-ff-uks-gp-1`

The Virtual Network is the private IP space that contains everything. All subnets — AKS node pools, the jumpbox, Bastion — live within this VNet. Private endpoint IPs are allocated from subnets within it.

### `bas-ff-uks-gp` (Azure Bastion)

Bastion is a fully managed PaaS service that provides browser-based (or native client) SSH/RDP to VMs **without those VMs needing a public IP**. It terminates your HTTPS connection and proxies it to the target VM's private IP. The `bas-ff-uks-gpPublicIp` is Bastion's own public IP — it's the only thing exposed to the internet in the access path.

### `FITFILEJumpbox`

A Linux (or Windows) VM that sits inside `vnet-ff-uks-gp-1`. Because it's in the same VNet as the private endpoint, its DNS resolves the AKS API FQDN to the private IP. This is where you run `kubectl`. It has no public IP of its own; you reach it exclusively via Bastion.

### `kubernetes` (Load Balancer)

This is the internal/external load balancer for **workload traffic** (services of type `LoadBalancer` in Kubernetes). It is distinct from API server access. It handles east-west traffic within the cluster and potentially north-south traffic for any exposed services.

### `aksoutip` and `pip-ff-uks-gp-1`

Outbound NAT public IPs. When pods inside the cluster make outbound internet requests (e.g. pulling images, calling external APIs), these IPs are used as the source. They are not used for inbound access to the API.

---

## 5. Accessing the Cluster API From Your Laptop

There are **two viable patterns**. Pick one based on your day-to-day workflow.

---

### Option A — Via Bastion to Jumpbox (Current Setup — No Extra Config)

This uses the infrastructure that already exists.

**How it works:** You SSH into the Jumpbox via Azure Bastion using the Azure CLI's native client feature, then run `kubectl` from inside the Jumpbox.

**Step-by-step:**

```bash
# Step 1: Install Azure CLI on your laptop (if not already present)
winget install Microsoft.AzureCLI   # Windows
# or
brew install azure-cli              # macOS

# Step 2: Log in and set the subscription
az login
az account set --subscription "7bbc8ae5-1710-48ab-ab83-59b52bd0de1a"

# Step 3: Open an SSH tunnel to the Jumpbox via Bastion
# (Bastion Standard SKU required for native client support)
az network bastion ssh \
  --name bas-ff-uks-gp \
  --resource-group rg-ff-uks-gp-net \
  --target-resource-id /subscriptions/7bbc8ae5-1710-48ab-ab83-59b52bd0de1a/resourceGroups/rg-ff-uks-gp-net/providers/Microsoft.Compute/virtualMachines/FITFILEJumpbox \
  --auth-type "AAD"
  # or --auth-type "ssh-key" --username <user> --ssh-key ~/.ssh/id_rsa

# Step 4: On the Jumpbox — get credentials and test
az aks get-credentials \
  --resource-group rg-ff-uks-gp-net \
  --name aks-ff-uks-gp-1 \
  --overwrite-existing

kubectl get nodes
```

**Limitations:** Every `kubectl` command requires an active SSH session on the Jumpbox. You cannot use local IDE integrations (Lens, k9s on your laptop) with this method.

---

### Option B — Bastion Tunnel (Port Forward to Your Laptop)

This is more ergonomic. It creates a local TCP port on your laptop that tunnels through Bastion to the Jumpbox, effectively letting your local `kubectl` reach the private API.

**How it works:** Azure Bastion can act as a TCP tunnel, forwarding a local port on your machine to a port on a private VM. We forward to the private endpoint IP on port `443`, making the API server reachable locally.

```bash
# Step 1: Find the private IP of the kube-apiserver private endpoint
az network private-endpoint show \
  --name kube-apiserver \
  --resource-group rg-ff-uks-gp-aks \
  --query "customDnsConfigs[0].ipAddresses[0]" \
  --output tsv
# → e.g. 10.x.x.x

# Step 2: Open a Bastion tunnel (runs in background / separate terminal)
az network bastion tunnel \
  --name bas-ff-uks-gp \
  --resource-group rg-ff-uks-gp-net \
  --target-resource-id /subscriptions/7bbc8ae5-1710-48ab-ab83-59b52bd0de1a/resourceGroups/rg-ff-uks-gp-net/providers/Microsoft.Compute/virtualMachines/FITFILEJumpbox \
  --resource-port 22 \
  --port 2222
# This opens localhost:2222 → Jumpbox port 22

# Step 3: From the Jumpbox (via the tunnel or a separate az bastion ssh session),
# set up a further kubectl proxy if needed — or use kubeconfig with server override.

# --- Alternative: Direct kubeconfig server override ---
# Get the kubeconfig from the Jumpbox, copy it to your laptop,
# then edit the server: field to point to localhost:<tunnelled_port>
# This is advanced and requires careful TLS handling.
```

> **Honest note:** Option B requires the **Bastion Standard SKU** (not Basic). Check your Bastion tier in the portal before attempting this. Basic Bastion does not support tunnelling.

---

### Option C — VPN / ExpressRoute (If Available in Future)

If the organisation adds a Point-to-Site VPN Gateway or ExpressRoute to `vnet-ff-uks-gp-1`, your laptop would join the VNet directly and DNS would resolve the private endpoint naturally. You could then run `kubectl` locally without any Bastion hop. This is the most seamless long-term solution but requires additional infrastructure.

---

### Credential Expiry

AKS kubeconfigs use Azure AD tokens with a **1-hour expiry** by default. When your token expires, `kubectl` will return a 401. Fix with:

```bash
kubelogin convert-kubeconfig -l azurecli
# or simply re-run:
az aks get-credentials --resource-group rg-ff-uks-gp-net --name aks-ff-uks-gp-1 --overwrite-existing
```

---

## 6. Backup Infrastructure

The cluster has AKS Backup configured, using Azure Backup Vault.

| Component | Role |
|-----------|------|
| `sbox-aks-backup-vault` | Azure Backup Vault that holds backup policies and restore points |
| `sboxaksbackup1a2b3` | Storage account where backup data is stored (blob containers) |
| `pe-sboxaksbackup1a2b3-blob` | Private endpoint for the backup storage account — ensures backup traffic stays on the private network |
| `stffuksgp1backup` | Secondary storage account in `rg-ff-uks-gp-net`, likely used for a separate backup policy or velero-style backups |
| `privatelink.blob.core.windows.net` | Private DNS zone enabling private resolution of `*.blob.core.windows.net` for the storage accounts |

The private endpoint for blob storage (`pe-sboxaksbackup1a2b3-blob`) is the same pattern as the API server — it means the AKS nodes write backups to Azure Storage without that traffic leaving the VNet.

---

## 7. Automation

| Component | Role |
|-----------|------|
| `auto-sandbox-cluster` | Azure Automation Account — a managed runner for PowerShell/Python runbooks |
| `ClusterChangeState` (runbook) | A runbook that likely starts/stops (scales down/up) the cluster on a schedule — common cost-saving pattern in test subscriptions |

> **Implication for you:** If the cluster is not responding or nodes are not present, check whether `ClusterChangeState` has recently run and stopped the cluster. You can view runbook job history in the portal under the Automation Account.

---

## 8. Network Security Groups Reference

| NSG Name | Attached To | Purpose |
|----------|-------------|---------|
| `aks-agentpool-14508117-nsg` | AKS node subnet | Auto-managed by AKS; controls traffic to/from node VMs. Do not manually edit — AKS overwrites rules. |
| `nsg-ff-uks-gp-system` | System node pool subnet | Custom NSG for the system node pool subnet |
| `nsg-ff-uks-gp-workflows` | Workflows node pool subnet | Custom NSG for the workflows node pool subnet |
| `nsg-ff-uks-gp-jumpbox` | Jumpbox subnet | Controls inbound to the Jumpbox; Bastion requires port 22/3389 from the `AzureBastionSubnet` |
| `FITFILEJumpboxNsg` | `FITFILEJumpboxNic` directly | NIC-level NSG on the Jumpbox VM itself (belt-and-braces) |

> **If Bastion can't connect to the Jumpbox**, the most common cause is the `nsg-ff-uks-gp-jumpbox` or `FITFILEJumpboxNsg` blocking inbound from the `AzureBastionSubnet`. The required rule is: **Allow inbound TCP 22 from `VirtualNetwork` (or the specific Bastion subnet CIDR)**.

---

*Last updated: May 2026 — generated from Azure subscription export.*
