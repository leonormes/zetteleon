---
created: 2026-04-29T08:54:35+00:00
modified: 2026-04-29T08:56:18+00:00
title: End-to-End Manual Proof AKS Backup via Private Endpoint
---

Good—your subnet output tells us a lot. Let me break down what you have, what's missing, and the exact sequence to prove the whole chain works before you touch Terraform.

---

## Current VNet Map (`vnet-ff-uks-gp-1`—`10.0.0.0/24`)

| CIDR | Subnet | Status |
|------|--------|--------|
| `10.0.0.0/27` | `snet-ff-uks-gp-system` | In use—already marked `Purpose: PrivateEndpoints` |
| `10.0.0.32/27` | `snet-ff-uks-gp-workflows` | In use |
| `10.0.0.64/27` | `snet-ff-uks-gp-jumpbox` | In use |
| `10.0.0.96/27` |—available—| 32 IPs free |
| `10.0.0.128/26` | `AzureBastionSubnet` | In use |
| `10.0.0.192/26` |—available—| 64 IPs free |

The `private-endpoint list` returned nothing, so no PEs exist yet in `rg-ff-uks-gp-net`.

---

## The Full Chain You Need to Prove

There are 8 distinct pieces. I've ordered them as dependencies:

### Phase 1—Storage Account + Private Networking

Step 1: Create the backup storage account

```bash
az storage account create \
  --name stffuksgp1backup \
  --resource-group rg-ff-uks-gp-net \
  --location uksouth \
  --sku Standard_LRS \
  --kind StorageV2 \
  --min-tls-version TLS1_2 \
  --allow-blob-public-access false \
  --public-network-access Disabled \
  --default-action Deny \
  --tags Environment=prod Department=SDE CreatedWith=Manual ManagedBy=FITFILE
```

> `--public-network-access Disabled` and `--default-action Deny` match the hardened posture you documented yesterday for the customer's `aksffuksgp01backupsa`.

Step 2: Create a dedicated Private Endpoints subnet (using the `10.0.0.96/27` gap)

```bash
az network vnet subnet create \
  --resource-group rg-ff-uks-gp-net \
  --vnet-name vnet-ff-uks-gp-1 \
  --name snet-ff-uks-gp-pe \
  --address-prefix 10.0.0.96/27 \
  --private-endpoint-network-policies Disabled
```

> You _could_ reuse `snet-ff-uks-gp-system` (it already has the `PrivateEndpoints` purpose), but a dedicated subnet is cleaner for the Terraform module later and mirrors what you specified in the desired-state delta from yesterday's audit.

Step 3: Create the Private Endpoint for blob

```bash
STORAGE_ID=$(az storage account show \
  --name stffuksgp1backup \
  --resource-group rg-ff-uks-gp-net \
  --query id -o tsv)

az network private-endpoint create \
  --name pe-stffuksgp1backup-blob \
  --resource-group rg-ff-uks-gp-net \
  --vnet-name vnet-ff-uks-gp-1 \
  --subnet snet-ff-uks-gp-pe \
  --private-connection-resource-id "$STORAGE_ID" \
  --group-id blob \
  --connection-name pec-stffuksgp1backup-blob \
  --location uksouth
```

Step 4: Private DNS Zone + VNet link

```bash
# Create the zone
az network private-dns zone create \
  --resource-group rg-ff-uks-gp-net \
  --name privatelink.blob.core.windows.net

# Link it to the VNet
az network private-dns zone vnet-link create \
  --resource-group rg-ff-uks-gp-net \
  --zone-name privatelink.blob.core.windows.net \
  --name link-vnet-ff-uks-gp-1 \
  --virtual-network vnet-ff-uks-gp-1 \
  --registration-enabled false

# Auto-register the PE's DNS record
PE_NIC_ID=$(az network private-endpoint show \
  --name pe-stffuksgp1backup-blob \
  --resource-group rg-ff-uks-gp-net \
  --query "networkInterfaces[0].id" -o tsv)

PE_IP=$(az network nic show --ids "$PE_NIC_ID" \
  --query "ipConfigurations[0].privateIpAddress" -o tsv)

az network private-dns record-set a add-record \
  --resource-group rg-ff-uks-gp-net \
  --zone-name privatelink.blob.core.windows.net \
  --record-set-name stffuksgp1backup \
  --ipv4-address "$PE_IP"
```

Step 5: Verify DNS resolution from inside the VNet (via your SOCKS proxy)

```bash
# From Tab 3 (with HTTPS_PROXY set)
kubectl run dnstest --image=busybox --rm -it --restart=Never -- \
  nslookup stffuksgp1backup.blob.core.windows.net
```

> This should resolve to the private IP (something in `10.0.0.96/27`), not a public IP. That's your first proof point.

---

### Phase 2—Backup Vault + AKS Extension

Step 6: Create the Backup Vault

```bash
az dataprotection backup-vault create \
  --vault-name bv-ff-uks-gp-1 \
  --resource-group rg-ff-uks-gp-net \
  --location uksouth \
  --storage-setting "[ { \"type\": \"LocallyRedundant\", \"datastore-type\": \"VaultStore\" } ]" \
  --type SystemAssigned
```

Step 7: Install the AKS Backup Extension

```bash
az k8s-extension create \
  --name azure-aks-backup \
  --extension-type microsoft.dataprotection.kubernetes \
  --scope cluster \
  --cluster-type managedClusters \
  --cluster-name aks-ff-uks-gp-1 \
  --resource-group rg-ff-uks-gp-net \
  --release-train stable \
  --configuration-settings \
    blobContainer=aks-backups \
    storageAccount=stffuksgp1backup \
    storageAccountResourceGroup=rg-ff-uks-gp-net \
    storageAccountSubscriptionId=7bbc8ae5-1710-48ab-ab83-59b52bd0de1a
```

> You'll also need to create the blob container first:

```bash
# This must be done via the PE — from the jumpbox, or using a managed identity
# Simplest: temporarily allow your IP, create the container, re-deny
az storage container create \
  --name aks-backups \
  --account-name stffuksgp1backup \
  --auth-mode login
```

Step 8: Verify the extension installed cleanly

```bash
az k8s-extension show \
  --name azure-aks-backup \
  --cluster-type managedClusters \
  --cluster-name aks-ff-uks-gp-1 \
  --resource-group rg-ff-uks-gp-net \
  --query "{Name:name, State:provisioningState, Version:version}" \
  -o table

# And from kubectl
kubectl get pods -n dataprotection-microsoft --context aks-ff-uks-gp-1
```

---

### Phase 3—RBAC, Policy, and the Actual Backup

Step 9: Grant the Vault's MSI the required roles

```bash
VAULT_MSI=$(az dataprotection backup-vault show \
  --vault-name bv-ff-uks-gp-1 \
  --resource-group rg-ff-uks-gp-net \
  --query "identity.principalId" -o tsv)

# Reader on the AKS cluster
AKS_ID=$(az aks show -g rg-ff-uks-gp-net -n aks-ff-uks-gp-1 --query id -o tsv)
az role assignment create --assignee "$VAULT_MSI" --role "Reader" --scope "$AKS_ID"

# Storage Blob Data Contributor on the storage account
az role assignment create --assignee "$VAULT_MSI" --role "Storage Blob Data Contributor" --scope "$STORAGE_ID"
```

> The extension's own identity also needs `Storage Blob Data Contributor`—check the extension's identity with:

```bash
az k8s-extension show \
  --name azure-aks-backup \
  --cluster-type managedClusters \
  --cluster-name aks-ff-uks-gp-1 \
  --resource-group rg-ff-uks-gp-net \
  --query "aksAssignedIdentity.principalId" -o tsv
```

Step 10: Create a backup policy

```bash
az dataprotection backup-policy create \
  --vault-name bv-ff-uks-gp-1 \
  --resource-group rg-ff-uks-gp-net \
  --name dailyaksbackups \
  --policy @- <<'EOF'
{
  "policyRules": [
    {
      "name": "BackupDaily",
      "objectType": "AzureBackupRule",
      "trigger": {
        "objectType": "ScheduleBasedTriggerContext",
        "schedule": {
          "repeatingTimeIntervals": ["R/2026-04-29T21:00:00+00:00/P1D"]
        },
        "taggingCriteria": [
          { "tagInfo": { "tagName": "Default" }, "taggingPriority": 99, "isDefault": true }
        ]
      },
      "backupParameters": {
        "objectType": "AzureBackupParams",
        "backupType": "Incremental"
      },
      "dataStore": { "objectType": "DataStoreInfoBase", "dataStoreType": "OperationalStore" }
    },
    {
      "name": "RetainDefault",
      "objectType": "AzureRetentionRule",
      "lifecycles": [
        {
          "deleteAfter": { "objectType": "AbsoluteDeleteOption", "duration": "P14D" },
          "sourceDataStore": { "objectType": "DataStoreInfoBase", "dataStoreType": "OperationalStore" }
        }
      ],
      "isDefault": true
    }
  ],
  "datasourceTypes": ["Microsoft.ContainerService/managedClusters"]
}
EOF
```

> This matches your documented desired state: 9:00 PM UTC daily, 14-day retention.

Step 11: Configure the backup instance and trigger a test backup

```bash
# Initialize the backup instance config
az dataprotection backup-instance initialize-backupconfig \
  --datasource-type AzureKubernetesService \
  > backup-config.json

# Initialize the backup instance
az dataprotection backup-instance initialize \
  --datasource-id "$AKS_ID" \
  --datasource-type AzureKubernetesService \
  --datasource-location uksouth \
  --policy-id $(az dataprotection backup-policy show -g rg-ff-uks-gp-net --vault-name bv-ff-uks-gp-1 -n dailyaksbackups --query id -o tsv) \
  --backup-configuration @backup-config.json \
  > backup-instance.json

# Validate
az dataprotection backup-instance validate-for-backup \
  --resource-group rg-ff-uks-gp-net \
  --vault-name bv-ff-uks-gp-1 \
  --backup-instance @backup-instance.json

# Create
az dataprotection backup-instance create \
  --resource-group rg-ff-uks-gp-net \
  --vault-name bv-ff-uks-gp-1 \
  --backup-instance @backup-instance.json

# Trigger an ad-hoc backup now
az dataprotection backup-instance adhoc-backup \
  --resource-group rg-ff-uks-gp-net \
  --vault-name bv-ff-uks-gp-1 \
  --name <instance-name-from-create-output> \
  --rule-name BackupDaily
```

---

## The Proof Points (What "Works" Means)

| # | What to Verify | How |
|---|---------------|-----|
| 1 | DNS resolves privately | `nslookup` from inside the VNet returns `10.0.0.96/27` IP |
| 2 | No public path exists | Storage account shows `PublicNetworkAccess: Disabled`, `defaultAction: Deny` |
| 3 | Extension is healthy | `az k8s-extension show` → `ProvisioningState: Succeeded`; pods running in `dataprotection-microsoft` namespace |
| 4 | Backup completes | Ad-hoc backup job finishes with status `Completed` |
| 5 | Data lands in blob | Container `aks-backups` has backup data (check via jumpbox or portal) |
| 6 | Restore works | Create a test namespace, back it up, delete it, restore it, verify objects return |

Point 6 is the real proof—without a restore test, you've only proven half the chain. I'd suggest:

```bash
# Create something to back up
kubectl create ns backup-test
kubectl create configmap test-data -n backup-test --from-literal=proof="it-works"

# Back it up (ad-hoc), then:
kubectl delete ns backup-test

# Restore from the recovery point, confirm:
kubectl get configmap test-data -n backup-test -o yaml
```

---

## Suggested Order of Work

1. Steps 1–5 (storage + PE + DNS)—~20 mins
2. Steps 6–8 (vault + extension)—~15 mins, extension install can take 5–10 mins
3. Steps 9–10 (RBAC + policy)—~10 mins
4. Step 11 (configure + trigger)—~10 mins, then wait for backup job
5. Restore test—the final proof

Once this all passes, you'll have the exact resource config to encode into Terraform modules, and you'll know every RBAC assignment and networking dependency from first-hand experience rather than documentation.
