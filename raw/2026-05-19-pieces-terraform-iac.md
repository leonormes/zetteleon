---
created: Invalid date
modified: 2026-05-26 11:43:35+00:00
pieces_ids:
- 01eed862-bad9-4871-ab9e-8c157c7af1a5
- 88486d20-aa29-4a9a-aa44-dc318f400060
- 937d50fb-f707-468c-bf36-095c2bc867e9
- a4e75b56-6094-48ef-b660-5a548874f472
- a55085fd-ea64-43cb-b750-4a1b62880c95
- b86f62ea-f554-49c3-8f5f-d03a189d909b
- ff577e34-97b5-43b6-9d92-45feab40fd0b
source: pieces-ltm
tags:
- pieces
- raw
title: 2026-05-19-pieces-terraform-iac
permalink: llmeon/raw/2026-05-19-pieces-terraform-iac
---

## Asset 1 (Pieces: 88486d20-aa29-4a9a-aa44-dc318f400060)

Pagination complete. The corpus is exhausted—116 total candidates across 3 pages, `recommendation: sufficient`, `nextCursor: null`. Here is the new grounding from the paginated results:

---

## What Memory now confirms—the Key New Finding

From the final pages, two critical events surfaced:

Event at 16:53 UTC (16:53:54, event `b9cc8d69`)—Azure Cloud Shell session captured verbatim:

> `az k8s-extension create --resource-group rg-ff-uks-gp-net --cluster-name aks-ff-uks-gp-01 --cluster-type managedClusters --name azbkuextension --extension-type microsoft.dataprotection.kubernetes --release-train stable --configuration-settings blobContainer=aksbackups storageAccount=aksffuksgp01cuhbackup storageAccountResourceGroup=aks-ff-uks-gp-01-backup-rg storageAccountSubscriptionId=709f3d57-…`

This confirms the `az k8s-extension list` returned an empty table (nothing shown after the query filter), but `az k8s-extension create` immediately replied with `ValidationFailed: Multiple extensions of same type is not allowed at this scope`. This is the contradiction you're stuck in.

Event `634f8f6d` shows the FitFile subscription (`709f3d57`) in CUH directory with `Role: Specified access`—meaning you may not have the Contributor role needed to run `az k8s-extension list` with the extension details returned correctly, even though you can see the subscription.

---

## The Actual Diagnosis

The JMESPath filter `[?extensionType=='microsoft.dataprotection.kubernetes']` is case-sensitive. `az k8s-extension list` on `aks-ff-uks-gp-01` is returning the extension, but the filter is dropping it because the `extensionType` field in the API response is cased differently than the filter string.

Proof: The `create` command fails with "Multiple extensions of same type"—meaning the extension IS there. But `az k8s-extension show --name azbkuextension` returns `ResourceNotFound`—meaning it was not installed under the name `azbkuextension`.

The extension exists under a different name. The `az k8s-extension list` returned empty because the JMESPath filter `extensionType=='microsoft.dataprotection.kubernetes'` (all lowercase) didn't match—the actual `extensionType` value in Azure ARM is `Microsoft.DataProtection.Kubernetes` (PascalCase).

---

## The fix—run `az k8s-extension list` without the Filter

```bash
az k8s-extension list \
  --subscription 709f3d57-b6d7-48c6-8252-6b1c1174a541 \
  --cluster-name aks-ff-uks-gp-01 \
  --resource-group rg-ff-uks-gp-net \
  --cluster-type managedClusters \
  -o table
```

This will show all extensions—no JMESPath filter—so you'll see the real extension name regardless of casing. The existing extension is blocking `create` but hiding from your filtered `list` and `show` calls because of the name mismatch.

Once you see the real name from the unfiltered list, then:

```bash
az k8s-extension update \
  --subscription 709f3d57-b6d7-48c6-8252-6b1c1174a541 \
  --name <REAL-NAME-FROM-LIST> \
  --cluster-name aks-ff-uks-gp-01 \
  --resource-group rg-ff-uks-gp-net \
  --cluster-type managedClusters \
  --configuration-settings \
    blobContainer=aksbackups \
    storageAccount=aksffuksgp01cuhbackup \
    storageAccountResourceGroup=aks-ff-uks-gp-01-backup-rg \
    storageAccountSubscriptionId=709f3d57-b6d7-48c6-8252-6b1c1174a541
```

The two-step issue in a nutshell:

- `create` fails: extension already exists (under unknown name)
- `show --name azbkuextension` fails: that name doesn't exist in the FitFile subscription
- `list` returns empty: JMESPath filter `extensionType=='microsoft.dataprotection.kubernetes'` misses because ARM stores it as `Microsoft.DataProtection.Kubernetes`

## Asset 2 (Pieces: 01eed862-bad9-4871-ab9e-8c157c7af1a5)

export EXT_MSI=$(az k8s-extension show \
  --subscription 709f3d57-b6d7-48c6-8252-6b1c1174a541 \
  --name azbkuextension \
  --cluster-name aks-ff-uks-gp-01 \
  --resource-group rg-ff-uks-gp-net \
  --cluster-type managedClusters \
  --query "aksAssignedIdentity.principalId" -o tsv)

echo "EXT_MSI=$EXT_MSI"

ERROR: (ResourceNotFound) Extension instance with name 'azbkuextension' not found.

Code: ResourceNotFound

Message: Extension instance with name 'azbkuextension' not found. Verify that the cluster-type is correct and the resource exists.

EXT_MSI=

leon [~]$ az k8s-extension list \
  --subscription 709f3d57-b6d7-48c6-8252-6b1c1174a541 \
  --cluster-name aks-ff-uks-gp-01 \
  --resource-group rg-ff-uks-gp-net \
  --cluster-type managedClusters \
  -o table

Name ExtensionType ProvisioningState LastModifiedAt Plan_name Plan_product IsSystemExtension

---------------- ----------------------------------- ------------------- -------------------------------- ----------- -------------- -------------- -------------------

azure-aks-backup Microsoft.DataProtection.Kubernetes Failed 2026-05-19T15:08:46.278830+00:00 plan_publisher False

## Asset 3 (Pieces: b86f62ea-f554-49c3-8f5f-d03a189d909b)

The user has finally run `az k8s-extension list` without the JMESPath filter and we can now see the real situation:

- Name: `azure-aks-backup`
- Type: `Microsoft.DataProtection.Kubernetes`
- State: `Failed`
- LastModifiedAt: `2026-05-19T15:08:46` (about an hour ago)

So the extension exists under the name `azure-aks-backup`, not `azbkuextension`. It's in a `Failed` state. This is the Terraform-created extension that timed out (as the user described in the meeting audio).

Now I see the issue—the Terraform module they're upgrading from v1.0.5 to v1.2.6 must have changed the extension naming convention. The existing failed extension is named `azure-aks-backup`, but they've been trying to create `azbkuextension`. I need to either update the existing extension to point to the CUH storage account, or delete it and recreate it with the correct configuration. between versions—older versions used `azure-aks-backup` as the extension name, while the Terraform module may now use `azbkuextension`.

Actually, looking at the user's Terraform work today (the CUH-DP AKS Backup—Terraform work), the module variable `backup_extension_name` or similar may control the extension name. The Terraform module at v1.2.x appears to use `azbkuextension` as the name, while the old deployed extension is `azure-aks-backup`.

The key facts:

1. Extension `azure-aks-backup` (type: `Microsoft.DataProtection.Kubernetes`) exists in `Failed` state—this was created by old Terraform
2. Terraform now wants to create `azbkuextension`—but can't because the type is already in use
3. The `Failed` state explains why `az k8s-extension show --name azure-aks-backup` would return it but the user was trying `azbkuextension`

So the cleanest solution is to delete the old `azure-aks-backup` extension and let Terraform create the new `azbkuextension` with the correct configuration, which aligns with the module upgrade from v1.0.5 to v1.2.6.

## Asset 4 (Pieces: a55085fd-ea64-43cb-b750-4a1b62880c95)

Now everything is clear. The mystery is solved.

Extension name on this cluster: `azure-aks-backup` (not `azbkuextension`)—installed in `Failed` state, likely from the Terraform timeout you described in the sprint planning meeting. Terraform v1.0.x used `azure-aks-backup` as the extension name; the upgraded v1.2.x module uses `azbkuextension`. The type conflict is between these two.

## The Path forward

### Step 1—Delete the Failed `azure-aks-backup` Extension

```bash
az k8s-extension delete \
  --subscription 709f3d57-b6d7-48c6-8252-6b1c1174a541 \
  --name azure-aks-backup \
  --cluster-name aks-ff-uks-gp-01 \
  --resource-group rg-ff-uks-gp-net \
  --cluster-type managedClusters \
  --yes
```

This takes a few minutes. Wait for it to complete.

### Step 2—Create `azbkuextension` with the Correct Config

```bash
az k8s-extension create \
  --subscription 709f3d57-b6d7-48c6-8252-6b1c1174a541 \
  --name azbkuextension \
  --extension-type Microsoft.DataProtection.Kubernetes \
  --scope cluster \
  --cluster-type managedClusters \
  --cluster-name aks-ff-uks-gp-01 \
  --resource-group rg-ff-uks-gp-net \
  --release-train stable \
  --configuration-settings \
    blobContainer=aksbackups \
    storageAccount=aksffuksgp01cuhbackup \
    storageAccountResourceGroup=aks-ff-uks-gp-01-backup-rg \
    storageAccountSubscriptionId=709f3d57-b6d7-48c6-8252-6b1c1174a541
```

### Step 3—Capture EXT_MSI and Apply RBAC

```bash
export EXT_MSI=$(az k8s-extension show \
  --subscription 709f3d57-b6d7-48c6-8252-6b1c1174a541 \
  --name azbkuextension \
  --cluster-name aks-ff-uks-gp-01 \
  --resource-group rg-ff-uks-gp-net \
  --cluster-type managedClusters \
  --query "aksAssignedIdentity.principalId" -o tsv)

echo "EXT_MSI=$EXT_MSI"

az role assignment create \
  --subscription 709f3d57-b6d7-48c6-8252-6b1c1174a541 \
  --assignee-object-id "$EXT_MSI" \
  --assignee-principal-type ServicePrincipal \
  --role "Storage Blob Data Contributor" \
  --scope "/subscriptions/709f3d57-b6d7-48c6-8252-6b1c1174a541/resourceGroups/aks-ff-uks-gp-01-backup-rg/providers/Microsoft.Storage/storageAccounts/aksffuksgp01cuhbackup"
```

### Step 4—Terraform Import

```bash
terraform import \
  'module.aks_backup.azurerm_kubernetes_cluster_extension.aks_backup_extension' \
  '/subscriptions/709f3d57-b6d7-48c6-8252-6b1c1174a541/resourceGroups/rg-ff-uks-gp-net/providers/Microsoft.ContainerService/managedClusters/aks-ff-uks-gp-01/providers/Microsoft.KubernetesConfiguration/extensions/azbkuextension'
```

The root cause of today's hours of pain was the old Terraform module creating `azure-aks-backup`, leaving it in `Failed` state after the timeout, and the new module expecting `azbkuextension`. Deleting the failed one unblocks everything.

## Asset 5 (Pieces: ff577e34-97b5-43b6-9d92-45feab40fd0b)

az k8s-extension delete \
  --subscription 709f3d57-b6d7-48c6-8252-6b1c1174a541 \
  --name azure-aks-backup \
  --cluster-name aks-ff-uks-gp-01 \
  --resource-group rg-ff-uks-gp-net \
  --cluster-type managedClusters \
  --yes

leon [~]$ export EXT_MSI=$(az k8s-extension show \
  --subscription 709f3d57-b6d7-48c6-8252-6b1c1174a541 \
  --name azbkuextension \
  --cluster-name aks-ff-uks-gp-01 \
  --resource-group rg-ff-uks-gp-net \
  --cluster-type managedClusters \
  --query "aksAssignedIdentity.principalId" -o tsv)

echo "EXT_MSI=$EXT_MSI"

az role assignment create \
  --subscription 709f3d57-b6d7-48c6-8252-6b1c1174a541 \
  --assignee-object-id "$EXT_MSI" \
  --assignee-principal-type ServicePrincipal \
  --role "Storage Blob Data Contributor" \
  --scope "/subscriptions/709f3d57-b6d7-48c6-8252-6b1c1174a541/resourceGroups/aks-ff-uks-gp-01-backup-rg/providers/Microsoft.Storage/storageAccounts/aksffuksgp01cuhbackup"

ERROR: (ResourceNotFound) Extension instance with name 'azbkuextension' not found.

Code: ResourceNotFound

Message: Extension instance with name 'azbkuextension' not found. Verify that the cluster-type is correct and the resource exists.

EXT_MSI=

usage error: --assignee STRING | --assignee-object-id GUID

## Asset 6 (Pieces: 937d50fb-f707-468c-bf36-095c2bc867e9)

The user deleted `azure-aks-backup` but then jumped straight to `az k8s-extension show --name azbkuextension` without first running the `az k8s-extension create` step. That's why it's not found—the create step was skipped.

They need to run the create command first.

## Asset 7 (Pieces: a4e75b56-6094-48ef-b660-5a548874f472)

You skipped Step 2. The delete succeeded, but you jumped straight to `show` without running the `create` first. `azbkuextension` doesn't exist yet because you never created it.

Run the create now:

```bash
az k8s-extension create \
  --subscription 709f3d57-b6d7-48c6-8252-6b1c1174a541 \
  --name azbkuextension \
  --extension-type Microsoft.DataProtection.Kubernetes \
  --scope cluster \
  --cluster-type managedClusters \
  --cluster-name aks-ff-uks-gp-01 \
  --resource-group rg-ff-uks-gp-net \
  --release-train stable \
  --configuration-settings \
    blobContainer=aksbackups \
    storageAccount=aksffuksgp01cuhbackup \
    storageAccountResourceGroup=aks-ff-uks-gp-01-backup-rg \
    storageAccountSubscriptionId=709f3d57-b6d7-48c6-8252-6b1c1174a541
```

This will take a few minutes to provision. Once it returns (look for `"provisioningState": "Succeeded"`), then run the show + RBAC block:

```bash
export EXT_MSI=$(az k8s-extension show \
  --subscription 709f3d57-b6d7-48c6-8252-6b1c1174a541 \
  --name azbkuextension \
  --cluster-name aks-ff-uks-gp-01 \
  --resource-group rg-ff-uks-gp-net \
  --cluster-type managedClusters \
  --query "aksAssignedIdentity.principalId" -o tsv)

echo "EXT_MSI=$EXT_MSI"

az role assignment create \
  --subscription 709f3d57-b6d7-48c6-8252-6b1c1174a541 \
  --assignee-object-id "$EXT_MSI" \
  --assignee-principal-type ServicePrincipal \
  --role "Storage Blob Data Contributor" \
  --scope "/subscriptions/709f3d57-b6d7-48c6-8252-6b1c1174a541/resourceGroups/aks-ff-uks-gp-01-backup-rg/providers/Microsoft.Storage/storageAccounts/aksffuksgp01cuhbackup"
```