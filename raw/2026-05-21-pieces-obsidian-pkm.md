---
title: Pieces LTM — Obsidian Pkm (2026-05-21)
created: 2026-05-21T19:15:29+00:00
source: pieces-ltm
pieces_ids: [4c9ba5fd-2926-4abf-b978-f42e2fb2b85d, 53d0bb40-334f-4f0a-85b5-e63f0c717786]
tags: [raw, pieces]
---

## Asset 1 (Pieces: 4c9ba5fd-2926-4abf-b978-f42e2fb2b85d) — 11:22:13

Based on your Obsidian records and historical command output, here is the exact process for SSHing into the **CUH Jumpbox** using Azure Bastion so that you can interact with your CUH AKS Cluster (`aks-ff-uks-gp-01`).

---

## 1. Context: Your CUH Network Topology

Your CUH private networking resources live within subscription `709f3d57-b6d7-48c6-8252-6b1c1174a541` under the **Norwich/CUH** environment (`NNUHFT-SDE`).
*   **AKS Cluster:** `aks-ff-uks-gp-01` (inside the resource group `rg-ff-uks-gp-aks`)
*   **Virtual Machine (Jumpbox):** `vm-ff-uks-gp-jumpbox`
*   **VNet:** `NNUHFT-SDE-vnet1` (inside `rg-ff-uks-gp-net` or its managed equivalent)
*   **Bastion Name:** `bas-ff-uks-gp`

Because the AKS cluster has private API access enabled (`aks-ff-uks-gp-01-igmjlo7k.303e6cfc-b5ff-47c7-93cc-517c8ce1a9aa.privatelink.uksouth.azmk8s.io`), your local kubernetes config must be routed through this jumpbox.

---

## 2. Step-by-Step SSH Connection via Azure Bastion

Since the jumpbox NIC has no direct public inbound IP, you must tunnel into it using Azure Bastion (`bas-ff-uks-gp`). 

### Step A: Log in to Azure in your local terminal
Confirm your active active-directory session targets the CUH/NNUH Tenant:
```sh
az login --tenant "4ae8fd93-d084-481f-ba6e-370b7d4d8d0d"
```

### Step B: Locate your jumpbox target resource ID
Run the following to save your VM's resource ID for the subsequent SSH trigger:
```sh
export VM_ID=$(az vm show --resource-group rg-ff-uks-gp-net --name vm-ff-uks-gp-jumpbox --query id -o tsv)
```

### Step C: Execute the Bastion SSH Tunnel
Use the `az network bastion ssh` command specifying the Standard Bastion host, the target jumpbox ID, and your default administrative username (`azadmin`):
```sh
az network bastion ssh \
  --name bas-ff-uks-gp \
  --resource-group rg-ff-uks-gp-net \
  --target-resource-id $VM_ID \
  --auth-type password \
  --username azadmin \
  -- -o PubkeyAuthentication=no -o PreferredAuthentications=password
```
*(Note: You will be prompted interactively in your terminal to input your `azadmin` password).*

---

## 3. Interacting with the CUH Kubernetes Cluster

Once you have established your shell session inside `vm-ff-uks-gp-jumpbox`, you can interact with the AKS cluster using `kubectl`.

### Step A: Grab Cluster Credentials
Merge the cluster Context into your local kubeconfig on the jumpbox:
```sh
az aks get-credentials \
  --resource-group rg-ff-uks-gp-aks \
  --name aks-ff-uks-gp-01 \
  --subscription 709f3d57-b6d7-48c6-8252-6b1c1174a541 \
  --overwrite-existing
```

### Step B: Verify the Connection
Run standard commands to verify you can now seamlessly cross-reference the private API backend:
```sh
kubectl get nodes
kubectl get namespaces
```

Most of your services live in namespaces such as `thehyve-cuh`, `monitoring`, `vault-secrets-operator-system`, and `reflector`. You are good to pull logs or run manual manifests.

## Asset 2 (Pieces: 53d0bb40-334f-4f0a-85b5-e63f0c717786) — 11:26:31

Thank you for correcting that. Indeed, you are referring to the actual **CUH cluster** context (`aks-ff-uks-gp-01` in subscription `709f3d57-b6d7-48c6-8252-6b1c1174a541` under `rg-ff-uks-gp-net` / `rg-ff-uks-gp-aks`) rather than NNUH. 

Based on your active work history on the **CUH-DP / cuh-poc-1** infrastructure, your Obsidian notes, and your terminal sessions, here is the exact protocol to SSH into the **CUH Jumpbox** using **Azure Bastion** and configure it to work with your private `aks-ff-uks-gp-01` cluster.

---

## 1. CUH Infrastructure Context
*   **Subscription ID:** `709f3d57-b6d7-48c6-8252-6b1c1174a541`
*   **Virtual Network (VNet):** `vnet-ff-uks-gp-01`
*   **Cluster Name:** `aks-ff-uks-gp-01`
*   **API FQDN:** `aks-ff-uks-gp-01-igmjlo7k.303e6cfc-b5ff-47c7-93cc-517c8ce1a9aa.privatelink.uksouth.azmk8s.io`
*   **Bastion Name:** `bas-ff-uks-gp`
*   **Jumpbox VM:** `vm-ff-uks-gp-jumpbox` (Resource Group: `rg-ff-uks-gp-net`)

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
  --name vm-ff-uks-gp-jumpbox \
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
