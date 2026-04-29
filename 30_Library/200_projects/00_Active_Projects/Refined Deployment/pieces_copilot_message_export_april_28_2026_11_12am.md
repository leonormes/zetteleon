---
created: 2026-04-28T10:12:52+00:00
modified: 2026-04-28T12:48:01+00:00
title: pieces_copilot_message_export_april_28_2026_11_12am
---

_Shared Message from Pieces (<https://pieces.app>) by Leon Ormes (leonormes@gmail.com) on Tuesday Apr 28, 2026 - 11:12 AM_
---

Thanks—this is all consistent with what you ran between 11:06–11:08 AM. Two things to fix in your script so you can complete the audit cleanly:

- Use --vault-name (not -n/--name) with az dataprotection backup-vault show.
- Derive the AKS VNet/subnet from a VMSS NIC (your NIC list query returned empty).

Paste-and-run fixes

1. Get the vault ID and re-run the Private Endpoint filters

```bash
# Known good IDs
VAULT_RG="prod-1-backup-v2-rg"
VAULT_NAME="aksbackupvault"
STORAGE_RG="prod-1-backup-v2-rg"
STORAGE_NAME="prod1backupv2sa"

# Robust vault ID fetch (use --vault-name)
VAULT_ID="$(az dataprotection backup-vault show -g "$VAULT_RG" --vault-name "$VAULT_NAME" --query id -o tsv)" || true
# Fallback if your CLI/environment trips over the DP subcommand:
if [[ -z "${VAULT_ID:-}" ]]; then
  VAULT_ID="$(az resource show -g "$VAULT_RG" --resource-type "Microsoft.DataProtection/backupVaults" -n "$VAULT_NAME" --query id -o tsv)"
fi

# Storage account ID
STO_ID="$(az storage account show -g "$STORAGE_RG" -n "$STORAGE_NAME" --query id -o tsv)"

echo "-- Storage PEs (blob) --"
az network private-endpoint list \
  --query "[?privateLinkServiceConnections[0].privateLinkServiceId=='${STO_ID}'].{Name:name,RG:resourceGroup,Subnet:subnet.id,GroupIds:privateLinkServiceConnections[0].groupIds,ConnStatus:privateLinkServiceConnections[0].privateLinkServiceConnectionState.status}" \
  -o table

echo "-- Vault PEs (if any) --"
az network private-endpoint list \
  --query "[?privateLinkServiceConnections[0].privateLinkServiceId=='${VAULT_ID}'].{Name:name,RG:resourceGroup,Subnet:subnet.id,GroupIds:privateLinkServiceConnections[0].groupIds,ConnStatus:privateLinkServiceConnections[0].privateLinkServiceConnectionState.status}" \
  -o table
```

2. Reliable AKS VNet/subnet discovery via VMSS NIC

```bash
AKS_NAME="fitfile-cloud-prod-1-aks-cluster"
AKS_RG="fitfile-cloud-prod-1-rg"

# Node RG
NODE_RG="$(az aks show -n "$AKS_NAME" -g "$AKS_RG" --query nodeResourceGroup -o tsv)"

# One agent VMSS (prefer pool with 'agent' or 'node' in the name)
VMSS_NAME="$(az vmss list -g "$NODE_RG" --query "[?contains(name,'agent') || contains(name,'node')][0].name" -o tsv)"
if [[ -z "${VMSS_NAME:-}" ]]; then
  VMSS_NAME="$(az vmss list -g "$NODE_RG" --query "[0].name" -o tsv)"
fi

# First NIC on that VMSS
NIC_ID="$(az vmss nic list -g "$NODE_RG" --vmss-name "$VMSS_NAME" --query "[0].id" -o tsv)"
SUBNET_ID="$(az network nic show --ids "$NIC_ID" --query "ipConfigurations[0].subnet.id" -o tsv)"
echo "SUBNET_ID: $SUBNET_ID"

# Parse VNet details
VNET_RG="$(awk -F/ '{for(i=1;i<=NF;i++) if($i=="resourceGroups"){print $(i+1); exit}}' <<<"$SUBNET_ID")"
VNET_NAME="$(awk -F/ '{for(i=1;i<=NF;i++) if($i=="virtualNetworks"){print $(i+1); exit}}' <<<"$SUBNET_ID")"
SUBNET_NAME="$(awk -F/ '{for(i=1;i<=NF;i++) if($i=="subnets"){print $(i+1); exit}}' <<<"$SUBNET_ID")"
echo "AKS VNet/Subnet: $VNET_RG / $VNET_NAME / $SUBNET_NAME"

# List subnets so you can confirm a 'private-endpoints' subnet exists/where to add it
az network vnet subnet list -g "$VNET_RG" --vnet-name "$VNET_NAME" \
  --query "[].{Name:name,Prefix:addressPrefix,Delegations:join(',',delegations[].serviceName)}" -o table
```

3. Confirm network plugin/mode (so we know why vnetSubnetID was blank)

```bash
az aks show -n "$AKS_NAME" -g "$AKS_RG" --query "networkProfile.{Plugin:networkPlugin,Mode:networkPluginMode,PodCidr:podCidr,ServiceCidr:serviceCidr}" -o table
```

What your run already proved (timestamps)

- 11:06 AM: AKS backup extension present and healthy on prod (azbkuextension Succeeded).
- 11:04–11:07 AM: Policy is daily at 9:00 PM UTC with 14-day retention; jobs complete nightly around 9:00–9:10 PM.
- 11:07 AM: OMOP/The Hyve namespaces exist (thehyve, thehyve-cuh, thehyve-mkuh) but are NOT in IncludedNamespaces, so those PVCs are out of scope right now.
- Storage posture: prod1backupv2sa PublicNetworkAccess Enabled; no PrivateEndpoints found; privatelink.blob.core.windows.net DNS zone not present.

Delta to target (what to change)

- Scope: Add OMOP namespaces thehyve, thehyve-cuh, thehyve-mkuh OR switch to labelSelectors (recommended to avoid drift).
  - Quick CLI prototype to append namespaces:

    ```bash
    az dataprotection backup-instance show -g "$VAULT_RG" --vault-name "$VAULT_NAME" -n "prod1aksdailyv2" \
      --query "properties.policyInfo.policyParameters" -o json >/tmp/instance-params.json

    # Edit /tmp/instance-params.json → add "thehyve","thehyve-cuh","thehyve-mkuh" to backupDatasourceParametersList[0].includedNamespaces

    az dataprotection backup-instance update -g "$VAULT_RG" --vault-name "$VAULT_NAME" -n "prod1aksdailyv2" \
      --policy-parameters @/tmp/instance-params.json
    ```

  - If using labels:

    ```bash
    kubectl label ns thehyve backup=enabled --overwrite
    kubectl label ns thehyve-cuh backup=enabled --overwrite
    kubectl label ns thehyve-mkuh backup=enabled --overwrite
    # Then set policyParameters.backupDatasourceParametersList[0].labelSelectors to:
    # [ { "matchLabels": { "backup": "enabled" } } ]
    ```

- Private networking for backups:
  - Create Private Endpoint (blob) for prod1backupv2sa in a dedicated private-endpoints subnet.
  - Create and link Private DNS zone privatelink.blob.core.windows.net to the AKS VNet.
  - Lock storage to private: publicNetworkAccess Disabled, defaultAction Deny, bypass None.
- Cadence/retention: Keep daily 9:00 PM UTC + P14D unless you decide to extend (e.g., daily x 30 or daily x 14 + weekly x 12 once costs are confirmed in FTFL-596).

Reference: The NNUH storage you viewed shows identical posture (no PEs, public access enabled). You captured that here at about 10:23 AM: [aksffuksgp01backupsa](https://portal.azure.com/#@nnuhnorwich.onmicrosoft.com/resource/subscriptions/4ae8fd93-d084-481f-ba6e-370b7d4d8d0d/resourceGroups/aks-ff-uks-gp-01-backup-rg/providers/Microsoft.Storage/storageAccounts/aksffuksgp01backupsa/overview)

If you paste back:

- The two PE tables (after the --vault-name fix),
- The VNet/subnet discovery result via VMSS NIC,
I'll confirm the exact Terraform diffs to:
- add thehyve* namespaces (or move to labelSelectors) in the AKS backup module,
- stand up the PE subnet + storage PE + DNS zone/link, and
- apply the equivalent for NNUH/MKUH under FTFL-596/597/598.
