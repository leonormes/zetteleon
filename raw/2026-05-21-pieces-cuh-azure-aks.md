---
title: Pieces LTM — Cuh Azure Aks (2026-05-21)
created: 2026-05-21T19:15:29+00:00
source: pieces-ltm
pieces_ids: [03f0e240-846c-4819-87c8-e847b18c394b, 4d85f4d9-2534-4dd0-9968-81a669497506, 536c69aa-3e7e-431b-9a6b-654ffdf0b2d0, 4c9ba5fd-2926-4abf-b978-f42e2fb2b85d, e3a40c5d-1ff9-4d25-8778-9c09ce81205e, 563a8591-9407-41e2-889a-c0599bc93f65, dd611007-ba29-475d-9a0f-7b07b607c70d, 53d0bb40-334f-4f0a-85b5-e63f0c717786]
tags: [raw, pieces]
---

## Asset 1 (Pieces: 03f0e240-846c-4819-87c8-e847b18c394b) — 11:18:37

search my history for how I ssh'd on the cuh jumpbox so that I could work with the cuh k8s cluster. There might be obsidian notes on it.

## Asset 2 (Pieces: 4d85f4d9-2534-4dd0-9968-81a669497506) — 11:18:40

**Recalling Access Method**

I'm focusing on recalling the exact SSH command used to access the CUH jumpbox, which then provides entry to the CUH k8s cluster. My current thought process is to retrieve the specific syntax and any associated authentication details.

## Asset 3 (Pieces: 536c69aa-3e7e-431b-9a6b-654ffdf0b2d0) — 11:19:22

**Investigating Access Methods**

My recent focus has been on understanding how users SSH into the CUH jumpbox to interact with the CUH Kubernetes cluster. I'm exploring potential Obsidian notes that might contain relevant documentation or explanations for this process.

## Asset 4 (Pieces: 4c9ba5fd-2926-4abf-b978-f42e2fb2b85d) — 11:22:13

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

## Asset 5 (Pieces: e3a40c5d-1ff9-4d25-8778-9c09ce81205e) — 11:24:03

You have got the nnuh part wrong. Here is the cuh cluster I am talking about. 
{
    "apiVersion": "2026-03-01",
    "id": "/subscriptions/709f3d57-b6d7-48c6-8252-6b1c1174a541/resourceGroups/rg-ff-uks-gp-net/providers/Microsoft.ContainerService/managedClusters/aks-ff-uks-gp-01",
    "name": "aks-ff-uks-gp-01",
    "type": "microsoft.containerservice/managedclusters",
    "sku": {
        "name": "Base",
        "tier": "Free"
    },
    "kind": "Base",
    "location": "uksouth",
    "identity": {
        "type": "UserAssigned",
        "userAssignedIdentities": {
            "/subscriptions/709f3d57-b6d7-48c6-8252-6b1c1174a541/resourceGroups/rg-ff-uks-gp-net/providers/Microsoft.ManagedIdentity/userAssignedIdentities/uai-ff-uks-gp-aks": {
                "clientId": "6120d87f-85d8-4768-adfe-af8d540d4018",
                "principalId": "0eb04d09-5d1b-4ee9-98ae-17742560e807"
            }
        }
    },
    "properties": {
        "provisioningState": "Succeeded",
        "powerState": {
            "code": "Running"
        },
        "kubernetesVersion": "1.32.6",
        "currentKubernetesVersion": "1.32.6",
        "dnsPrefix": "aks-ff-uks-gp-01",
        "azurePortalFQDN": "630ed9cdbb0be7d84c554fd71ef40682-priv.portal.hcp.uksouth.azmk8s.io",
        "privateFQDN": "aks-ff-uks-gp-01-igmjlo7k.303e6cfc-b5ff-47c7-93cc-517c8ce1a9aa.privatelink.uksouth.azmk8s.io",
        "agentPoolProfiles": [
            {
                "name": "system",
                "count": 2,
                "vmSize": "Standard_E4s_v5",
                "osDiskSizeGB": 128,
                "osDiskType": "Managed",
                "kubeletDiskType": "OS",
                "vnetSubnetID": "/subscriptions/709f3d57-b6d7-48c6-8252-6b1c1174a541/resourceGroups/rg-ff-uks-gp-net/providers/Microsoft.Network/virtualNetworks/vnet-ff-uks-gp-01/subnets/snet-ff-uks-gp-system",
                "maxPods": 100,
                "type": "VirtualMachineScaleSets",
                "maxCount": 2,
                "minCount": 2,
                "enableAutoScaling": true,
                "scaleDownMode": "Delete",
                "provisioningState": "Succeeded",
                "powerState": {
                    "code": "Running"
                },
                "orchestratorVersion": "1.32.6",
                "currentOrchestratorVersion": "1.32.6",
                "enableNodePublicIP": false,
                "tags": {
                    "createdWith": "Terraform",
                    "environment": "dev",
                    "managedBy": "FITFILE",
                    "status": "development"
                },
                "mode": "System",
                "enableEncryptionAtHost": true,
                "enableUltraSSD": false,
                "osType": "Linux",
                "osSKU": "Ubuntu",
                "nodeImageVersion": "AKSUbuntu-2204gen2containerd-202603.18.1",
                "upgradeSettings": {
                    "maxSurge": "10%",
                    "nodeSoakDurationInMinutes": 0,
                    "maxUnavailable": "0"
                },
                "enableFIPS": false,
                "securityProfile": {
                    "enableVTPM": false,
                    "enableSecureBoot": false
                },
                "eTag": "fe50d9cc-c470-49b2-9e89-828ed32ceb89"
            }
        ],
        "windowsProfile": {
            "adminUsername": "azureuser",
            "enableCSIProxy": true
        },
        "servicePrincipalProfile": {
            "clientId": "msi"
        },
        "addonProfiles": {
            "azurepolicy": {
                "enabled": true,
                "config": {
                    "version": "v2"
                },
                "identity": {
                    "resourceId": "/subscriptions/709f3d57-b6d7-48c6-8252-6b1c1174a541/resourcegroups/rg-ff-uks-gp-aks/providers/Microsoft.ManagedIdentity/userAssignedIdentities/azurepolicy-aks-ff-uks-gp-01",
                    "clientId": "527133ed-07c8-4deb-95b8-62c37c6b24f6",
                    "objectId": "3380ef85-d2e3-4101-bdc5-77be8e4da0ec"
                }
            },
            "extensionManager": {
                "enabled": true,
                "config": null
            }
        },
        "nodeResourceGroup": "rg-ff-uks-gp-aks",
        "enableRBAC": true,
        "supportPlan": "KubernetesOfficial",
        "networkProfile": {
            "networkPlugin": "azure",
            "networkPluginMode": "overlay",
            "networkPolicy": "calico",
            "networkDataplane": "azure",
            "loadBalancerSku": "standard",
            "loadBalancerProfile": {
                "backendPoolType": "nodeIPConfiguration"
            },
            "podCidr": "10.244.0.0/16",
            "serviceCidr": "10.2.0.0/24",
            "dnsServiceIP": "10.2.0.10",
            "outboundType": "userDefinedRouting",
            "podCidrs": [
                "10.244.0.0/16"
            ],
            "serviceCidrs": [
                "10.2.0.0/24"
            ],
            "ipFamilies": [
                "IPv4"
            ]
        },
        "maxAgentPools": 100,
        "privateLinkResources": [
            {
                "id": "/subscriptions/709f3d57-b6d7-48c6-8252-6b1c1174a541/resourcegroups/rg-ff-uks-gp-net/providers/Microsoft.ContainerService/managedClusters/aks-ff-uks-gp-01/privateLinkResources/management",
                "name": "management",
                "type": "Microsoft.ContainerService/managedClusters/privateLinkResources",
                "groupId": "management",
                "requiredMembers": [
                    "management"
                ]
            }
        ],
        "apiServerAccessProfile": {
            "enablePrivateCluster": true,
            "privateDNSZone": "system",
            "enablePrivateClusterPublicFQDN": false
        },
        "identityProfile": {
            "kubeletidentity": {
                "resourceId": "/subscriptions/709f3d57-b6d7-48c6-8252-6b1c1174a541/resourcegroups/rg-ff-uks-gp-aks/providers/Microsoft.ManagedIdentity/userAssignedIdentities/aks-ff-uks-gp-01-agentpool",
                "clientId": "d601580a-895b-45e4-be6c-e4c4be0c7a88",
                "objectId": "ad138ceb-eed9-4bb4-a54a-84528f1f68db"
            }
        },
        "autoScalerProfile": {
            "balance-similar-node-groups": "false",
            "daemonset-eviction-for-empty-nodes": false,
            "daemonset-eviction-for-occupied-nodes": true,
            "expander": "random",
            "ignore-daemonsets-utilization": false,
            "max-empty-bulk-delete": "10",
            "max-graceful-termination-sec": "600",
            "max-node-provision-time": "15m",
            "max-total-unready-percentage": "45",
            "new-pod-scale-up-delay": "0s",
            "ok-total-unready-count": "3",
            "scale-down-delay-after-add": "10m",
            "scale-down-delay-after-delete": "10s",
            "scale-down-delay-after-failure": "3m",
            "scale-down-unneeded-time": "10m",
            "scale-down-unready-time": "20m",
            "scale-down-utilization-threshold": "0.5",
            "scan-interval": "10s",
            "skip-nodes-with-local-storage": "false",
            "skip-nodes-with-system-pods": "true"
        },
        "autoUpgradeProfile": {
            "upgradeChannel": "none",
            "nodeOSUpgradeChannel": "NodeImage"
        },
        "disableLocalAccounts": false,
        "httpProxyConfig": {
            "httpProxy": "http://10.252.142.180:8080/",
            "httpsProxy": "http://10.252.142.180:8080/",
            "noProxy": [
                "cuh-prod-1-mongodb-b17ef-metrics",
                "10.244.0.0/16",
                "workflows-api.cuh-prod-1",
                "argocd-server-metrics",
                "argocd-metrics",
                "cuh-prod-1-mongodb-b17ef-headless.cuh-prod-1",
                "cuh-prod-1-mongodb-b17ef-headless.cuh-prod-1.svc.cluster.local",
                "cuh-prod-1-mongodb-b17ef-arbiter-headless.cuh-prod-1.svc.cluster.local",
                "cuh-prod-1-ffcloud-service.cuh-prod-1.svc.cluster.local",
                "cuh-prod-1-postgresql-hl.cuh-prod-1",
                "cuh-prod-1-mongodb-b17ef-arbiter-headless",
                ".svc",
                "argocd-server",
                "workflows-api.cuh-prod-1.svc.cluster.local",
                "10.2.0.0/24",
                "argocd-redis",
                "cuh-prod-1-postgresql-hl.cuh-prod-1.svc.cluster.local",
                "10.2.0.10",
                "10.250.16.16/28",
                "argocd-application-controller",
                "GBCBGPCISQ001.net.addenbrookes.nhs.uk",
                "cuh-prod-1-postgresql-hl",
                "10.250.16.0/28",
                ".svc.cluster.local",
                "cuh-prod-1-minio",
                "cuh-prod-1-postgresql.cuh-prod-1",
                "168.63.129.16",
                "cuh-prod-1-fitconnect-ftc",
                "cuh-prod-1-fitconnect-ftc.cuh-prod-1",
                "127.0.0.1",
                "localhost",
                "mutating-proxy-webhook.cuh-prod-1",
                "cuh-prod-1-minio.cuh-prod-1",
                "cuh-prod-1-postgresql",
                "10.252.0.0/16",
                "cuh-prod-1-frontend-frontend.cuh-prod-1",
                "cuh-prod-1-mongodb-b17ef-metrics.cuh-prod-1",
                "spicedb.spicedb",
                "argocd-dex-server",
                "mutating-proxy-webhook",
                "cuh-prod-1-frontend-frontend.cuh-prod-1.svc.cluster.local",
                "cuh-prod-1-mongodb-b17ef-arbiter-headless.cuh-prod-1",
                "workflows-api",
                "cuh-prod-1-postgresql.cuh-prod-1.svc.cluster.local",
                "cuh-prod-1-minio.cuh-prod-1.svc.cluster.local",
                "cuh-prod-1-ffcloud-service.cuh-prod-1",
                "cuh-prod-1-mongodb-b17ef-metrics.cuh-prod-1.svc.cluster.local",
                "cuh-prod-1-fitconnect-ftc.cuh-prod-1.svc.cluster.local",
                "argocd-repo-server",
                "cuh-prod-1-mongodb-b17ef-headless",
                "mutating-proxy-webhook.cuh-prod-1.svc.cluster.local",
                "cuh-prod-1-frontend-frontend",
                "cuh-prod-1-ffcloud-service"
            ],
            "effectiveNoProxy": [
                "workflows-api",
                "argocd-repo-server",
                "aks-ff-uks-gp-01-igmjlo7k.303e6cfc-b5ff-47c7-93cc-517c8ce1a9aa.privatelink.uksouth.azmk8s.io",
                "168.63.129.16",
                "workflows-api.cuh-prod-1",
                "cuh-prod-1-postgresql",
                "cuh-prod-1-postgresql.cuh-prod-1.svc.cluster.local",
                "cuh-prod-1-ffcloud-service.cuh-prod-1",
                "cuh-prod-1-fitconnect-ftc.cuh-prod-1.svc.cluster.local",
                "cuh-prod-1-ffcloud-service",
                "cuh-prod-1-postgresql-hl.cuh-prod-1",
                "workflows-api.cuh-prod-1.svc.cluster.local",
                "mutating-proxy-webhook.cuh-prod-1",
                "cuh-prod-1-mongodb-b17ef-arbiter-headless.cuh-prod-1",
                "argocd-server-metrics",
                "localhost",
                "spicedb.spicedb",
                "cuh-prod-1-fitconnect-ftc",
                "argocd-metrics",
                "cuh-prod-1-mongodb-b17ef-headless.cuh-prod-1.svc.cluster.local",
                "10.250.16.16/28",
                "10.252.0.0/16",
                "mutating-proxy-webhook.cuh-prod-1.svc.cluster.local",
                "cuh-prod-1-frontend-frontend",
                "cuh-prod-1-mongodb-b17ef-metrics",
                "cuh-prod-1-mongodb-b17ef-headless.cuh-prod-1",
                ".svc",
                "cuh-prod-1-minio.cuh-prod-1.svc.cluster.local",
                "cuh-prod-1-mongodb-b17ef-headless",
                "konnectivity",
                "cuh-prod-1-mongodb-b17ef-arbiter-headless",
                "10.2.0.0/24",
                "cuh-prod-1-ffcloud-service.cuh-prod-1.svc.cluster.local",
                ".svc.cluster.local",
                "cuh-prod-1-postgresql.cuh-prod-1",
                "argocd-dex-server",
                "argocd-redis",
                "GBCBGPCISQ001.net.addenbrookes.nhs.uk",
                "cuh-prod-1-minio",
                "mutating-proxy-webhook",
                "169.254.169.254",
                "10.244.0.0/16",
                "cuh-prod-1-mongodb-b17ef-arbiter-headless.cuh-prod-1.svc.cluster.local",
                "10.250.16.0/28",
                "cuh-prod-1-mongodb-b17ef-metrics.cuh-prod-1.svc.cluster.local",
                "argocd-server",
                "cuh-prod-1-postgresql-hl.cuh-prod-1.svc.cluster.local",
                "cuh-prod-1-postgresql-hl",
                "127.0.0.1",
                "10.250.16.0/24",
                "10.2.0.10",
                "cuh-prod-1-frontend-frontend.cuh-prod-1",
                "cuh-prod-1-frontend-frontend.cuh-prod-1.svc.cluster.local",
                "argocd-application-controller",
                "cuh-prod-1-fitconnect-ftc.cuh-prod-1",
                "cuh-prod-1-minio.cuh-prod-1",
                "cuh-prod-1-mongodb-b17ef-metrics.cuh-prod-1"
            ],
            "enabled": true
        },
        "securityProfile": {},
        "storageProfile": {
            "diskCSIDriver": {
                "enabled": true
            },
            "fileCSIDriver": {
                "enabled": true
            },
            "snapshotController": {
                "enabled": true
            }
        },
        "oidcIssuerProfile": {
            "enabled": false
        },
        "workloadAutoScalerProfile": {
            "verticalPodAutoscaler": {
                "enabled": true
            }
        },
        "azureMonitorProfile": {
            "metrics": {
                "enabled": false,
                "kubeStateMetrics": {}
            }
        },
        "upgradeSettings": {
            "overrideSettings": {
                "forceUpgrade": false
            }
        },
        "resourceUID": "685c290aa58ad3000182ac0d",
        "metricsProfile": {
            "costAnalysis": {
                "enabled": false
            }
        },
        "nodeProvisioningProfile": {
            "mode": "Manual",
            "defaultNodePools": "Auto"
        },
        "bootstrapProfile": {
            "artifactSource": "Direct"
        }
    },
    "etag": "16c52e19-9fb9-4953-a598-f569890c3d5f"
}
I previously worked on it.

## Asset 6 (Pieces: 563a8591-9407-41e2-889a-c0599bc93f65) — 11:25:36

**Refining Cluster Identification**

I'm now focusing on the specific `aks-ff` cluster you've detailed. My previous interpretation of "nnuh" was incorrect; I understand you're referring to the "cuh cluster" which you have prior experience with. This JSON provides the necessary context.

**Examining CUH Cluster Details**

I'm now deeply examining the provided JSON for the `aks-ff` cluster, specifically focusing on its unique subscription, resource group `rg-ff-uks-gp-net`, VNet subnet, and FQDN. I'm also cross-referencing this with `JUMPBOX_DEPLOYMENT.md` to understand the Kubernetes authentication configuration.

## Asset 7 (Pieces: dd611007-ba29-475d-9a0f-7b07b607c70d) — 11:26:14

**Analyzing CUH Network Configuration**

I'm focusing on the CUH cluster's unique networking specifics, distinct from NNUH's hierarchy. I need to correlate the correct CUH cluster configuration details to ensure precise integration.

**Mapping CUH Networking Details**

I'm now mapping CUH's specific Azure Directory and network VNet configurations, including subnets for nodes, workflows, jumpbox, and Bastion. This detailed topology is critical for successful integration.

**Integrating CUH Network Details**

I'm now analyzing the CUH cluster's egress routing, confirming its user-defined path points to an internal proxy with an extensive noProxy list, which is distinct from NNUH's setup. I am also actively detailing the SSH access method via Bastion to the CUH jumpbox.

**Establishing CUH Jumpbox Access**

I'm actively working on establishing SSH access to the CUH jumpbox via Azure Bastion. My current focus involves correctly configuring the tunnel and executing password-based SSH login to facilitate this connection.

## Asset 8 (Pieces: 53d0bb40-334f-4f0a-85b5-e63f0c717786) — 11:26:31

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
