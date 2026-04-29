---
created: 2026-04-28T09:54:33+00:00
modified: 2026-04-28T12:48:01+00:00
title: pieces_copilot_message_export_april_28_2026_10_54am
---

_Shared Message from Pieces (<https://pieces.app>) by Leon Ormes (leonormes@gmail.com) on Tuesday Apr 28, 2026 - 10:54 AM_
---

Here's a tight field-guide you can paste into your terminal to fully audit the prod cluster's backup posture and the private networking for backups (incl. private endpoints), followed by a delta plan.

A. Set context (prod)

```bash
# Ensure you’re in the prod subscription
az account set --subscription "FITCloud Production"

# Sanity: list AKS clusters and note the prod one(s)
az aks list -o table

# If you know the prod AKS name, set it for reuse
AKS_NAME="fitfile-cloud-prod-1-aks-cluster"
AKS_RG="$(az aks show -n "$AKS_NAME" -g "$(az aks list --query "[?name=='$AKS_NAME'].resourceGroup" -o tsv)" --query resourceGroup -o tsv)"
```

B. Backup system audit (Data Protection Vault, Policies, Instances, Jobs, Extension)

```bash
# 1) Inventory backup vaults in prod (you’ve seen these before at ~9:37 AM)
az dataprotection backup-vault list \
  --query "[].{Name:name, RG:resourceGroup, Location:location, State:properties.provisioningState}" -o table

# 2) List policies in prod vault (expect: dailyaksbackups)
VAULT_RG="prod-1-backup-v2-rg"
VAULT_NAME="aksbackupvault"
az dataprotection backup-policy list -g "$VAULT_RG" --vault-name "$VAULT_NAME"

# Handy extracts:
az dataprotection backup-policy show -g "$VAULT_RG" --vault-name "$VAULT_NAME" -n dailyaksbackups \
  --query "{Name:name, Cadence:properties.policyRules[?name=='BackupIntervals'][0].trigger.schedule.repeatingTimeIntervals, Retention:properties.policyRules[?objectType=='AzureRetentionRule'][0].lifecycles[0].deleteAfter.duration}"

# 3) List backup instances (expect: prod1aksdailyv2)
az dataprotection backup-instance list -g "$VAULT_RG" --vault-name "$VAULT_NAME" \
  --query "[].{Name:name, Cluster:properties.friendlyName, State:properties.currentProtectionState}" -o table

# 4) Drill into instance scope (namespaces, resource filters, volume snapshots)
az dataprotection backup-instance show -g "$VAULT_RG" --vault-name "$VAULT_NAME" -n "prod1aksdailyv2" \
  --query "properties.policyInfo.policyParameters.backupDatasourceParametersList[0].{IncludedNamespaces:includedNamespaces,ExcludedNamespaces:excludedNamespaces,ExcludedTypes:excludedResourceTypes,IncludeClusterScope:includeClusterScopeResources,SnapshotVolumes:snapshotVolumes,LabelSelectors:labelSelectors}"

# 5) Where snapshots/operational store land (resource group pointer)
az dataprotection backup-instance show -g "$VAULT_RG" --vault-name "$VAULT_NAME" -n "prod1aksdailyv2" \
  --query "properties.policyInfo.policyParameters.dataStoreParametersList[0].resourceGroupId"

# 6) Recent backup jobs and status (succeeding/failed/last run)
az dataprotection job list -g "$VAULT_RG" --vault-name "$VAULT_NAME" \
  --query "[].{Name:name,Status:properties.status,Operation:properties.operationCategory,Start:properties.startTime,End:properties.endTime}" -o table

# 7) AKS Backup extension state on the prod cluster
az k8s-extension list --cluster-type managedClusters --cluster-name "$AKS_NAME" -g "$AKS_RG" \
  --query "[?extensionType=='microsoft.dataprotection.kubernetes'].{Name:name,ProvisioningState:provisioningState,Version:version}" -o table
```

C. Private networking audit (storage, private endpoints, DNS, subnets)

```bash
# 1) Find any backup-related storage accounts in prod (naming often includes 'backup' or 'bkp')
az storage account list \
  --query "[?contains(name,'backup')].{Name:name,RG:resourceGroup,Location:primaryLocation}" -o table

# 2) For each candidate storage account, check network posture and PEs
STO_RG="<prod-backup-rg-if-any>"     # e.g., prod-1-backup-v2-rg
STO_NAME="<prodbackupstorageacct>"   # substitute if you find one
az storage account show -g "$STO_RG" -n "$STO_NAME" \
  --query "{PublicNetworkAccess:publicNetworkAccess,DefaultAction:networkAcls.defaultAction,Bypass:networkAcls.bypass,PrivateEndpoints:privateEndpointConnections[].properties.privateLinkServiceConnectionState.status}"

# 3) Enumerate private endpoints across prod (filter by storage or vault)
az network private-endpoint list -o table

# 4) If you know a PE RG, show PE details and connection targets
PE_RG="<network-rg>"
PE_NAME="<pe-name>"
az network private-endpoint show -g "$PE_RG" -n "$PE_NAME" \
  --query "{Name:name, Subnet:subnet.id, Targets:privateLinkServiceConnections[].{ResourceId:privateLinkServiceId, GroupIds:groupIds}}"

# 5) Private DNS zones for storage privatelink, and VNet links
az network private-dns zone list --query "[].{Name:name,RG:resourceGroup}" -o table
az network private-dns zone show -g "$PE_RG" -n "privatelink.blob.core.windows.net" --query "{Name:name}" -o tsv 2>/dev/null || true
az network private-dns link vnet list -g "$PE_RG" -z "privatelink.blob.core.windows.net" \
  --query "[].{LinkName:name,VNet:virtualNetwork.id,Registration:registrationEnabled}" -o table 2>/dev/null || true

# 6) Check there’s a dedicated Private Endpoints subnet (best practice)
NET_RG="<prod-net-rg>"   # e.g., rg-ff-uks-gp-net
VNET_NAME="<prod-vnet>"  # e.g., NNUHFT-SDE-vnet1 (replace for prod)
az network vnet subnet list -g "$NET_RG" --vnet-name "$VNET_NAME" \
  --query "[].{Name:name,Prefix:addressPrefix,Delegations:delegations[].serviceName}" -o table
```

D. Plan: delta between deployed vs. desired

Based on your prod baseline already observed around 9:37–9:40 AM:

- Deployed now
  - Backup vault: prod-1-backup-v2-rg/aksbackupvault
  - Policy: dailyaksbackups with daily 9:00 PM UTC cadence and 14-day retention
  - Instance: prod1aksdailyv2 covering namespaces: barts, ff-a, ff-b, ff-c, spicedb; secrets excluded; snapshotVolumes=true
  - AKS backup extension installed and healthy (verify with the command above)
  - Private networking: to be verified; in analogous NNUH, storage had publicNetworkAccess Enabled and no private endpoints
- Desired target state
  1. Keep the daily cadence (or update per business decision) and set explicit retention as policy, not implied
     - Option A: daily × 30 days
     - Option B: daily × 14 + weekly × 12 (rolling), subject to cost sign-off
  2. Ensure namespace/PVC coverage includes all stateful workloads (MongoDB, PostgreSQL/SpiceDB, OMOP). Prefer labelSelectors to reduce drift risk, else enumerate all namespaces used for stateful apps
  3. Enforce private networking for backup data paths:
     - Storage account used for backups must be reachable via Private Endpoint (blob) in a dedicated "private-endpoints" subnet
     - Private DNS zone privatelink.blob.core.windows.net created and linked to the AKS VNet(s)
     - Storage account PublicNetworkAccess Disabled and networkAcls.defaultAction Deny (rely on PE)
  4. Optional: Private endpoint to the Backup Vault (if mandated by org policy) to restrict control plane access paths

Concrete changes and commands to implement the delta

- Update/confirm policy details (cadence and retention)

```bash
# Example: surface policy JSON for edit (you’ll set desired P1D cadence and P30D retention)
az dataprotection backup-policy show -g "$VAULT_RG" --vault-name "$VAULT_NAME" -n dailyaksbackups > /tmp/policy.json

# Edit /tmp/policy.json, then:
az dataprotection backup-policy create --source-storage /tmp/policy.json \
  -g "$VAULT_RG" --vault-name "$VAULT_NAME" -n dailyaksbackups
```

- Expand instance scope to cover required namespaces or add labelSelectors

```bash
# Show current parameters (repeat for reference)
az dataprotection backup-instance show -g "$VAULT_RG" --vault-name "$VAULT_NAME" -n "prod1aksdailyv2" \
  --query "properties.policyInfo.policyParameters" -o json > /tmp/instance-params.json

# Edit to add namespaces (e.g., mongodb, postgresql, omop) or labelSelectors, then update:
az dataprotection backup-instance update \
  -g "$VAULT_RG" --vault-name "$VAULT_NAME" -n "prod1aksdailyv2" \
  --policy-parameters @/tmp/instance-params.json
```

- Build the private endpoint path to storage

```bash
# Identify the storage account to use for backup data (if none, create one in prod-1-backup-v2-rg)
STO_RG="prod-1-backup-v2-rg"
STO_NAME="<prodbackupstorageacct>"

# Networking primitives (create if missing)
NET_RG="<rg-ff-uks-gp-net>"       # adjust for prod
VNET_NAME="<prod-vnet>"
PE_SUBNET_NAME="private-endpoints"
# If subnet doesn’t exist, create it (example /27; adjust address space)
az network vnet subnet create -g "$NET_RG" --vnet-name "$VNET_NAME" -n "$PE_SUBNET_NAME" \
  --address-prefixes "<10.0.50.0/27>"

# Private DNS zone for blob privatelink (if missing) and link it
DNS_RG="$NET_RG"
az network private-dns zone create -g "$DNS_RG" -n "privatelink.blob.core.windows.net"
VNET_ID="$(az network vnet show -g "$NET_RG" -n "$VNET_NAME" --query id -o tsv)"
az network private-dns link vnet create -g "$DNS_RG" -z "privatelink.blob.core.windows.net" \
  -n "pe-link-$VNET_NAME" -v "$VNET_ID" -e false

# Create Private Endpoint to the storage account (blob group)
STO_ID="$(az storage account show -g "$STO_RG" -n "$STO_NAME" --query id -o tsv)"
az network private-endpoint create -g "$NET_RG" -n "pe-${STO_NAME}-blob" \
  --vnet-name "$VNET_NAME" --subnet "$PE_SUBNET_NAME" \
  --private-connection-resource-id "$STO_ID" --group-ids "blob" \
  --connection-name "pec-${STO_NAME}-blob"

# Attach DNS zone group so the A records are auto-managed
PE_ID="$(az network private-endpoint show -g "$NET_RG" -n "pe-${STO_NAME}-blob" --query id -o tsv)"
az network private-endpoint dns-zone-group create \
  --endpoint-name "pe-${STO_NAME}-blob" -g "$NET_RG" -n "dg-${STO_NAME}-blob" \
  --private-dns-zone "privatelink.blob.core.windows.net" --zone-name "zg-${STO_NAME}-blob"

# Lock down the storage account to private only
az storage account update -g "$STO_RG" -n "$STO_NAME" \
  --public-network-access Disabled
az storage account update -g "$STO_RG" -n "$STO_NAME" \
  --default-action Deny --bypass None
```

- Optional: Private endpoint for the Backup Vault

```bash
# If your policy requires PE to the Backup Vault as well:
VAULT_ID="$(az dataprotection backup-vault show -g "$VAULT_RG" -n "$VAULT_NAME" --query id -o tsv)"
az network private-endpoint create -g "$NET_RG" -n "pe-${VAULT_NAME}" \
  --vnet-name "$VNET_NAME" --subnet "$PE_SUBNET_NAME" \
  --private-connection-resource-id "$VAULT_ID" --group-ids "AzureBackup" \
  --connection-name "pec-${VAULT_NAME}"

# (Create corresponding privatelink DNS zone for vault if required by service docs and link VNet)
```

What I'll look for in your outputs

- Backup posture is consistent with policy: last jobs are succeeding, instance scope covers all stateful namespaces/PVCs (MongoDB, PostgreSQL/SpiceDB, OMOP).
- The storage account used for backup data is reachable through a private endpoint; publicNetworkAccess is Disabled; defaultAction is Deny; DNS is wired through privatelink with VNet link(s).
- The "private-endpoints" subnet exists and is dedicated (no delegation that conflicts).
- Optional: Backup Vault private endpoint in place per policy.

If you paste back the outputs of sections B.4, B.6, C.2 and C.5, I can confirm the exact delta and provide final Terraform diffs for:

- terraform-azure-aks-backup (policy cadence/retention, instance scope)
- terraform-azure-private-infrastructure (private-endpoints subnet, private DNS)
- storage private endpoint resources and network ACL lockdown (plus optional vault PE)
