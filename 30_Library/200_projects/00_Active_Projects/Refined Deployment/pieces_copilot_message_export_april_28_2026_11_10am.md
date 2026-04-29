---
created: 2026-04-28T10:10:07+00:00
modified: 2026-04-28T12:48:01+00:00
title: pieces_copilot_message_export_april_28_2026_11_10am
---

_Shared Message from Pieces (<https://pieces.app>) by Leon Ormes (leonormes@gmail.com) on Tuesday Apr 28, 2026 - 11:10 AM_
---

Great run—here's what you've just confirmed and the exact next commands to finish the audit and close the gaps.

What you confirmed just now

- AKS backup extension: Present and healthy on prod (azbkuextension Succeeded at 11:06 AM).
- Policy/cadence/retention: daily at 9:00 PM UTC; retention P14D.
- Instance scope: includedNamespaces = [barts, ff-a, ff-b, ff-c, spicedb]; exclusions: secrets, volumesnapshotcontent; snapshotVolumes=true.
- Jobs: nightly backups completing successfully each day around 9:00–9:10 PM.
- Storage network posture: prod1backupv2sa has PublicNetworkAccess Enabled and no private endpoints returned.
- Critical gap: OMOP/The Hyve namespaces exist (thehyve, thehyve-cuh, thehyve-mkuh; seen at 11:07 AM) but are NOT in includedNamespaces. That means those PVCs are not currently in scope. This contradicts FTFL-596 requirements and needs fixing before templating to NNUH/MKUH.

Fix the two audit command hiccups

- The "unrecognized arguments: --name aksbackupvault" error is a CLI parsing quirk. Use one of these robust alternatives to fetch the vault ID, then re-run the PE filters.

Commands to complete the audit now

Copy/paste:

```bash
# A) Robust vault ID fetch (use -n or az resource)
VAULT_RG="prod-1-backup-v2-rg"
VAULT_NAME="aksbackupvault"
STORAGE_RG="prod-1-backup-v2-rg"
STORAGE_NAME="prod1backupv2sa"

# Option 1 (preferred):
VAULT_ID="$(az dataprotection backup-vault show -g "$VAULT_RG" -n "$VAULT_NAME" --query id -o tsv)" || true
# Fallback if the above errors in your shell:
if [[ -z "${VAULT_ID:-}" ]]; then
  VAULT_ID="$(az resource show -g "$VAULT_RG" \
    --resource-type "Microsoft.DataProtection/backupVaults" \
    -n "$VAULT_NAME" --query id -o tsv)"
fi

STO_ID="$(az storage account show -g "$STORAGE_RG" -n "$STORAGE_NAME" --query id -o tsv)"

echo "-- Storage PEs (blob) --"
az network private-endpoint list \
  --query "[?privateLinkServiceConnections[0].privateLinkServiceId=='${STO_ID}'].{Name:name,RG:resourceGroup,Subnet:subnet.id,GroupIds:privateLinkServiceConnections[0].groupIds,ConnStatus:privateLinkServiceConnections[0].privateLinkServiceConnectionState.status}" \
  -o table

echo "-- Vault PEs (if any) --"
az network private-endpoint list \
  --query "[?privateLinkServiceConnections[0].privateLinkServiceId=='${VAULT_ID}'].{Name:name,RG:resourceGroup,Subnet:subnet.id,GroupIds:privateLinkServiceConnections[0].groupIds,ConnStatus:privateLinkServiceConnections[0].privateLinkServiceConnectionState.status}" \
  -o table

# B) DNS zone presence and links (privatelink.blob.core.windows.net)
DNS_ZONE="privatelink.blob.core.windows.net"
ZONE_RG="$(az network private-dns zone list --query "[?name=='$DNS_ZONE'].resourceGroup" -o tsv)"
if [[ -n "${ZONE_RG:-}" ]]; then
  echo "DNS zone '$DNS_ZONE' found in RG: $ZONE_RG"
  az network private-dns link vnet list -g "$ZONE_RG" -z "$DNS_ZONE" \
    --query "[].{LinkName:name,VNet:virtualNetwork.id,Registration:registrationEnabled}" -o table
else
  echo "DNS zone '$DNS_ZONE' not found in this subscription."
fi

# C) More reliable AKS VNet/Subnet derivation (node NIC fallback)
AKS_NAME="fitfile-cloud-prod-1-aks-cluster"
AKS_RG="fitfile-cloud-prod-1-rg"
NODE_RG="$(az aks show -n "$AKS_NAME" -g "$AKS_RG" --query nodeResourceGroup -o tsv)"
SUBNET_ID="$(az network nic list -g "$NODE_RG" \
  --query "[?ipConfigurations[0].subnet.id!=null].[ipConfigurations[0].subnet.id]" -o tsv | head -n1)"
echo "SUBNET_ID: $SUBNET_ID"
VNET_RG="$(awk -F/ '{for(i=1;i<=NF;i++) if($i=="resourceGroups"){print $(i+1); exit}}' <<<"$SUBNET_ID")"
VNET_NAME="$(awk -F/ '{for(i=1;i<=NF;i++) if($i=="virtualNetworks"){print $(i+1); exit}}' <<<"$SUBNET_ID")"
echo "AKS VNet/Subnet: $VNET_RG / $VNET_NAME / $(awk -F/ '{for(i=1;i<=NF;i++) if($i=="subnets"){print $(i+1); exit}}' <<<"$SUBNET_ID")"

# D) List subnets to confirm a dedicated private-endpoints subnet exists/belongs in the plan
az network vnet subnet list -g "$VNET_RG" --vnet-name "$VNET_NAME" \
  --query "[].{Name:name,Prefix:addressPrefix,Delegations:join(',',delegations[].serviceName)}" -o table
```

Immediate remediation for the backup scope gap (prod)

We must include The Hyve/OMOP namespaces (thehyve, thehyve-cuh, thehyve-mkuh). Two paths:

- Safer/low-drift (recommended): use labelSelectors (e.g., backup=enabled) and label all stateful namespaces. Then backup policy targets by label.
- Quick fix: add namespaces directly to includedNamespaces.

CLI prototype (quick fix):

```bash
# Export current params, edit, and update
az dataprotection backup-instance show \
  -g prod-1-backup-v2-rg --vault-name aksbackupvault -n prod1aksdailyv2 \
  --query "properties.policyInfo.policyParameters" -o json >/tmp/instance-params.json

# Edit /tmp/instance-params.json:
# - In backupDatasourceParametersList[0].includedNamespaces,
#   append: "thehyve", "thehyve-cuh", "thehyve-mkuh"
# - Keep snapshotVolumes: true

az dataprotection backup-instance update \
  -g prod-1-backup-v2-rg --vault-name aksbackupvault -n prod1aksdailyv2 \
  --policy-parameters @/tmp/instance-params.json
```

If you prefer labels, I can give you the exact JSON shape for labelSelectors and a kubectl one-liner to tag those namespaces.

Delta plan to target state (applies to prod baseline and to NNUH/MKUH rollout under FTFL-596)

- Scope
  - Current: barts, ff-a, ff-b, ff-c, spicedb
  - Desired: include OMOP (thehyve, thehyve-cuh, thehyve-mkuh) and any other stateful app namespaces. Prefer labelSelectors to avoid drift.
- Cadence/retention
  - Current: Daily 9:00 PM UTC; keep 14 days
  - Decision: either keep-as-is, or adopt
    - Daily x 30 days, or
    - Daily x 14 + Weekly x 12 (needs cost sign-off; ties to OMOP cost Q4 in [FTFL-596](https://fitfile.atlassian.net/browse/FTFL-596))
- Private networking (backups data path)
  - Current: prod1backupv2sa shows PublicNetworkAccess Enabled; no PEs found so far
  - Desired: Private Endpoint (blob) in a dedicated private-endpoints subnet; privatelink.blob.core.windows.net DNS zone + VNet link(s); storage PublicNetworkAccess Disabled and defaultAction Deny. This is the same dependency tracked in [FTFL-615](https://fitfile.atlassian.net/browse/FTFL-615).

If you want, I'll:

- Produce the labelSelectors JSON and namespace label commands.
- Draft the Terraform changes (aks_backup inputs for cadence/retention and scope; private-infra subnet + storage PE + DNS) so you can PR the module updates for NNUH/MKUH straight away.
