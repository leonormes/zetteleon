---
created: 2026-04-28T10:06:02+00:00
modified: 2026-04-28T12:48:01+00:00
title: pieces_copilot_message_export_april_28_2026_11_06am
---

_Shared Message from Pieces (<https://pieces.app>) by Leon Ormes (leonormes@gmail.com) on Tuesday Apr 28, 2026 - 11:06 AM_
---

Here's what your run just confirmed (11:04 AM), plus the quick fixes to finish the audit and a tight delta plan you can action.

What your results show (11:04 AM)

- Policy/cadence/retention: daily at 9:00 PM UTC, 14-day retention (P14D).
- Protection instance scope: includedNamespaces = [barts, ff-a, ff-b, ff-c, spicedb]; snapshotVolumes=true; secrets and volumesnapshotcontent excluded.
- Operational store pointer: prod-1-snapshot-v2-rg.
- Jobs: nightly backups are completing successfully every day around 9:00–9:10 PM.
- Storage network posture (prod1backupv2sa): PublicNetworkAccess Enabled; no PrivateEndpoints detected.
- Two gaps to complete the audit:
  - AKS Backup extension health table printed empty. We'll re-run without the filter to see the raw list.
  - Private Endpoints listing for the vault errored due to a CLI flag (-n). We'll fix the flag and re-run.

Fixes to complete the audit

1. Re-run AKS backup extension check (no filters)

```bash
az k8s-extension list \
  --cluster-type managedClusters \
  --cluster-name "fitfile-cloud-prod-1-aks-cluster" \
  -g "fitfile-cloud-prod-1-rg" \
  -o table
```

2. Re-run Private Endpoints filtering with corrected vault show flag

```bash
# IDs
VAULT_ID="$(az dataprotection backup-vault show -g prod-1-backup-v2-rg --name aksbackupvault --query id -o tsv)"
STO_ID="$(az storage account show -g prod-1-backup-v2-rg -n prod1backupv2sa --query id -o tsv)"

echo "-- Storage PEs (blob) --"
az network private-endpoint list \
  --query "[?privateLinkServiceConnections[0].privateLinkServiceId=='${STO_ID}'].{Name:name,RG:resourceGroup,Subnet:subnet.id,GroupIds:privateLinkServiceConnections[0].groupIds,ConnStatus:privateLinkServiceConnections[0].privateLinkServiceConnectionState.status}" \
  -o table

echo "-- Vault PEs (if any) --"
az network private-endpoint list \
  --query "[?privateLinkServiceConnections[0].privateLinkServiceId=='${VAULT_ID}'].{Name:name,RG:resourceGroup,Subnet:subnet.id,GroupIds:privateLinkServiceConnections[0].groupIds,ConnStatus:privateLinkServiceConnections[0].privateLinkServiceConnectionState.status}" \
  -o table
```

3. Optional: if you want the AKS VNet/subnet details (your earlier extraction returned blanks), use this fallback to derive them from a node NIC:

```bash
NODE_RG="$(az aks show -n fitfile-cloud-prod-1-aks-cluster -g fitfile-cloud-prod-1-rg --query nodeResourceGroup -o tsv)"
SUBNET_ID="$(az network nic list -g "$NODE_RG" --query "[0].ipConfigurations[0].subnet.id" -o tsv)"
echo "SUBNET_ID: $SUBNET_ID"
VNET_RG="$(awk -F/ '{for(i=1;i<=NF;i++) if($i=="resourceGroups"){print $(i+1); exit}}' <<<"$SUBNET_ID")"
VNET_NAME="$(awk -F/ '{for(i=1;i<=NF;i++) if($i=="virtualNetworks"){print $(i+1); exit}}' <<<"$SUBNET_ID")"
SUBNET_NAME="$(awk -F/ '{for(i=1;i<=NF;i++) if($i=="subnets"){print $(i+1); exit}}' <<<"$SUBNET_ID")"
echo "AKS VNet/Subnet: $VNET_RG / $VNET_NAME / $SUBNET_NAME"
```

Coverage check for OMOP namespace (likely missing)

- Your current includedNamespaces do not list an OMOP namespace. To confirm the namespace name(s), run:

```bash
# If you have Kube creds:
az aks get-credentials -n fitfile-cloud-prod-1-aks-cluster -g fitfile-cloud-prod-1-rg --overwrite-existing
kubectl get ns | grep -Ei "omop|hyve|postgres"
kubectl get pvc -A | grep -Ei "omop|hyve|postgres"
```

- If OMOP (or any other stateful workload) sits in a namespace not listed, we should either:
  - add that namespace to includedNamespaces, or
  - switch to a labelSelectors model (e.g., label stateful namespaces backup=enabled to avoid drift).

Delta plan (from current → desired)

1. Retention/cadence
- Current: daily at 9:00 PM UTC; retain 14 days.
- Decision: keep as-is or move to one of:
  - Daily x 30 days (simple), or
  - Daily x 14 + Weekly x 12 (rolling) for longer-term protection.
- Action (Terraform): update the azurerm_data_protection_backup_policy_kubernetes_cluster inputs for prod baseline and for NNUH/MKUH when you roll the modules.

1. Instance scope (namespaces/PVCs)
- Current: [barts, ff-a, ff-b, ff-c, spicedb]; snapshotVolumes=true.
- Desired: include OMOP and any other stateful DB namespaces (MongoDB, PostgreSQL/SpiceDB, OMOP). Prefer labelSelectors to reduce future drift.
- Action:
  - Prototype via CLI if needed:
    - az dataprotection backup-instance show -g prod-1-backup-v2-rg --vault-name aksbackupvault -n prod1aksdailyv2 -o json > /tmp/instance-params.json
    - Edit includedNamespaces or add labelSelectors.
    - az dataprotection backup-instance update -g prod-1-backup-v2-rg --vault-name aksbackupvault -n prod1aksdailyv2 --policy-parameters @/tmp/instance-params.json
  - Commit in Terraform variables for the aks_backup module for NNUH/MKUH.

1. Private networking for backups (prod shows public access; no PEs)
- Desired:
  - Private Endpoint (blob) to prod1backupv2sa in a dedicated private-endpoints subnet.
  - Private DNS zone privatelink.blob.core.windows.net + VNet link(s).
  - Storage account publicNetworkAccess Disabled; network ACL defaultAction Deny; no bypass.
- Action (Terraform; same pattern for NNUH/MKUH):
  - Add/ensure the private-endpoints subnet in the private infra module (FTFL-615).
  - Create the storage PE (groupIds: blob) + DNS zone group/link.
  - Lock down storage (disable public access, defaultAction Deny).

1. Optional: Private endpoint to the Backup Vault
- Only if your policy mandates vault control-plane confinement. If yes, add a PE for the vault (groupIds often "AzureBackup") and wire the corresponding privatelink DNS zone.

What this gives you for FTFL-596

- Q1, Q2, Q3: answered off prod baseline (daily at 9:00 PM UTC; retain 14 days).
- Q5: partially answered—we now know prod scope; confirm/add OMOP (and any gaps) before templating for NNUH/MKUH.
- Q4 (costs): still requires stakeholder confirmation for any increased retention (esp. OMOP).
- Q6 (Terraform SP): for prod you're set; for customer tenants you already stated the SP deployed infra previously (Contributor present). No further action unless customers changed roles.

Want me to append this summary and the corrected commands to your working note [Jira-FTFL-596.md](file:///Volumes/DAL/Zettelkasten/LLMeon/30_Library/200_projects/Jira-FTFL-596.md) and draft the Terraform variable diffs (cadence/retention + namespace/labelSelectors) so you can PR them directly?
