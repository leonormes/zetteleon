---
created: 2026-03-30 11:54:06+00:00
modified: 2026-06-08 11:49:16+00:00
project_category: deployments
project_name: Deployments
project_status: active
title: CUH
type: null
permalink: llmeon/30-library/200-projects/cuh
---

## 1. CUH Infrastructure Context

- Subscription ID: `709f3d57-b6d7-48c6-8252-6b1c1174a541`
- Virtual Network (VNet): `vnet-ff-uks-gp-01`
- Cluster Name: `aks-ff-uks-gp-01`
- API FQDN: `aks-ff-uks-gp-01-igmjlo7k.303e6cfc-b5ff-47c7-93cc-517c8ce1a9aa.privatelink.uksouth.azmk8s.io`
- Bastion Name: `bas-ff-uks-gp`
- Jumpbox VM: `vm-ff-uks-gp-jumpbox` (Resource Group: `rg-ff-uks-gp-net`)

---

## 2. Step-by-Step SSH Connection via Azure Bastion

Since the jumpbox has no direct public inbound IP allocated (it routes outbound traffic via the NAT gateway `nat-mkuh-uks-prd-01`), you must establish an SSH connection via your Standard Bastion Host.

### Step A: Authenticate to the CUH Tenant

```sh
az login --tenant "cuhfoundationtrust.onmicrosoft.com"
az account set --subscription "709f3d57-b6d7-48c6-8252-6b1c1174a541"
```

### Step B: Fetch the Jumpbox Resource ID

```sh
export JUMPBOX_ID=$(az vm show \
  --resource-group rg-ff-uks-gp-net \
  --name FITFILEJumpbox \
  --query id -o tsv)
```

### Step C: Connect Using Password Authentication

Execute the connection and provide your `azadmin` password when prompted:

```sh
az network bastion ssh \
  --name bas-ff-uks-gp \
  --resource-group rg-ff-uks-gp-net \
  --target-resource-id $JUMPBOX_ID \
  --auth-type password \
  --username azadmin \
  -- -o PubkeyAuthentication=no -o PreferredAuthentications=password
```

---

## 3. Configuring and Working with the K8s Cluster

Once inside the jumpbox terminal session, you are on the trusted network slice where the private FQDN of the AKS cluster resolves. Run the following to update your local kube-context:

### Step A: Retrieve the AKS Credentials

```sh
az aks get-credentials \
  --resource-group rg-ff-uks-gp-net \
  --name aks-ff-uks-gp-01 \
  --overwrite-existing
```

### Step B: Validate Connectivity

Ensure you can negotiate with the private API server:

```sh
kubectl cluster-info
kubectl get ns
```

### Step C: Skip Proxy Settings (Crucial for CUH)

Because the CUH environment enforces a proxy configuration (`http://10.252.142.180:8080/`), the cluster uses an explicit `noProxy` block to avoid routing internal traffic out to the gateway. If you deploy or query microservices on this cluster, ensure your local shell environments on the jumpbox do not pass internal requests through the proxy:

```sh
export no_proxy="localhost,127.0.0.1,10.244.0.0/16,10.2.0.0/24,.svc,.svc.cluster.local,GBCBGPCISQ001.net.addenbrookes.nhs.uk,168.63.129.16,${no_proxy:-}"
export NO_PROXY=$no_proxy
```

---

## 4. On-Deck: Private Backup Tasks

Your recent work on the `cuh-poc-1` workspace ([HCP Terraform](https://app.terraform.io/app/FITFILE-Platforms/workspaces/cuh-poc-1)) relates to configure private backups (`aksbackupvault` / `aksffuksgp01cuhbackup` in `aks-ff-uks-gp-01-backup-rg`).

If you are using the jumpbox to debug pod restarts in `dataprotection-microsoft` due to the Helm installation hang on `dataprotection-microsoft-geneva-service` (from your failed Terraform apply `run-VsHz6gWZmEyW3MzJ`), run these commands on the box to gather diagnostics:

```sh
# Trace backup extension deployment events
kubectl get events -n dataprotection-microsoft --sort-by='.metadata.creationTimestamp' | tail -n 25

# Inspect the geneva-service agent status
kubectl describe ds/dataprotection-microsoft-geneva-service -n dataprotection-microsoft
```

Ah, classic naming discrepancy! Based on the VM JSON payload you just provided, the virtual machine resource name in your CUH network is actually `FITFILEJumpbox` (with system-internal computer name `FITFILEJumpbox`), rather than `vm-ff-uks-gp-jumpbox`.

Here are the revised commands targeting the correct resource name:

### 2. Connect Using Azure Bastion

Execute the tunnel command using `FITFILEJumpbox` credentials:

```sh
az network bastion ssh \
  --name bas-ff-uks-gp \
  --resource-group rg-ff-uks-gp-net \
  --target-resource-id $JUMPBOX_ID \
  --auth-type password \
  --username azadmin \
  -- -o PubkeyAuthentication=no -o PreferredAuthentications=password
```

_Shared Message from Pieces (<https://pieces.app>) by Leon Ormes (leonormes@gmail.com) on Thursday May 21, 2026 - 1:50 PM_
---

## The Cause of the `ResourceNotFound` Error

The error occurs because the bastion host you are trying to query does not reside in the resource group `rg-ff-uks-gp-net` as passed in your command.

Your history and local files ([Understanding NAT Gateways.md](/Users/leon.ormes/Documents/LeonLM/20_Thinking/21_Workbench/Understanding NAT Gateways.md)) indicate that:

1. The bastion subnet and IP configurations are actually inside the `NNUHFT-SDE-Networking` resource group.
2. The correct resource ID of your Bastion Host is:
   `/subscriptions/4ae8fd93-d084-481f-ba6e-370b7d4d8d0d/resourceGroups/NNUHFT-SDE-Networking/providers/Microsoft.Network/bastionHosts/BAS-FF-UKS-GP`

The active jumpbox virtual machine in that network is name-mapped as `FITFILEJumpbox` (previously initialized under virtual machine resource path `…/Microsoft.Compute/virtualMachines/FITFILEJumpbox` in your realigned network specifications).

---

## Corrected Shell Commands & Connection Steps

To connect to your CUH jumpbox cleanly through the Bastion host, you need to target `NNUHFT-SDE-Networking` as the bastion's native resource group.

### Step 1: Run the Bastion SSH Tunnel Commands

Execute the following corrected `az network bastion` command on your workstation:

```bash
JUMPBOX_ID=$(az vm show \
  --resource-group rg-ff-uks-gp-net \
  --name FITFILEJumpbox \
  --subscription 709f3d57-b6d7-48c6-8252-6b1c1174a541 \
  --query id -o tsv)

az network bastion ssh \
  --name bas-ff-uks-gp \
  --resource-group rg-ff-uks-gp-net \
  --target-resource-id "$JUMPBOX_ID" \
  --auth-type password \
  --username azadmin \
  -- -o PubkeyAuthentication=no -o PreferredAuthentications=password
```

### Alternate Approach: Tunnel Locally as a Background Process

If you prefer mapping access through a local background tunnel to copy files (via `rsync` or `scp`) or hold persistency:

```bash
# Establish local SSH port forwarding tunnel on port 2222
az network bastion tunnel \
  --name BAS-FF-UKS-GP \
  --resource-group NNUHFT-SDE-Networking \
  --target-resource-id "$JUMPBOX_ID" \
  --resource-port 22 \
  --port 2222 &

# Wait a few seconds for the tunnel to negotiate, then access local port 2222
ssh -o PreferredAuthentications=password \
  -o PubkeyAuthentication=no \
  -o NumberOfPasswordPrompts=1 \
  azadmin@localhost -p 2222
```

---

## Once Authenticated: Configure Kubernetes (`cuh-prod-1`)

Once you are shell-connected to your `FITFILEJumpbox`, you need to set up your environment to communicate with the private `aks-ff-uks-gp-01` cluster.

### Step 2: Fetch AKS Cluster Credentials

Merge the Kubernetes config into your context:

```bash
az aks get-credentials \
  --resource-group rg-ff-uks-gp-aks \
  --name aks-ff-uks-gp-01 \
  --subscription 709f3d57-b6d7-48c6-8252-6b1c1174a541
```

### Step 3: Configure Proxy Environment Bypasses

Because the CUH network deploys an outbound decryption/proxy gateway at `http://10.252.142.180:8080/`, you must configure your shell's `NO_PROXY` parameters natively so cluster operations do not try to route through external endpoints:

```bash
# Set external outgoing proxies
export HTTP_PROXY="http://10.252.142.180:8080/"
export HTTPS_PROXY="http://10.252.142.180:8080/"

# Set cluster-wide internal exemptions
export NO_PROXY="localhost,127.0.0.1,10.244.0.0/16,10.252.0.0/16,192.168.200.0/24,.svc,.svc.cluster.local,aks-ff-uks-gp-01-igmjlo7k.303e6cfc-b5ff-47c7-93cc-517c8ce1a9aa.privatelink.uksouth.azmk8s.io"
export no_proxy="$NO_PROXY"
```