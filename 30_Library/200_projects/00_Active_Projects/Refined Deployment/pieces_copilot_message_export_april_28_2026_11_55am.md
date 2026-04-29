---
created: 2026-04-28T10:55:34+00:00
modified: 2026-04-28T12:48:01+00:00
title: pieces_copilot_message_export_april_28_2026_11_55am
---

_Shared Message from Pieces (<https://pieces.app>) by Leon Ormes (leonormes@gmail.com) on Tuesday Apr 28, 2026 - 11:55 AM_
---

## Step-by-Step Plan: FTFL-615 Private Endpoint—Staging Test

This follows directly from the Non-Production Delta Plan that Claude Code produced at 11:22–11:31 AM, using `stagingbackupsa` in `staging-backup-rg` as the test target before touching any prod environment.

---

### Phase 0—Pre-flight Checks

1. Confirm staging cluster is running (it was stopped for 10 days causing backup failures—confirmed running as of 2026-04-28):

   ```bash
   az aks show -n fitfile-cloud-staging-aks-cluster -g fitfile-cloud-staging-rg \
     --query "{Name:name, PowerState:powerState.code, ProvisioningState:provisioningState}" -o table
   ```

2. Confirm Terraform SP permissions in non-prod subscription—per the checklist in [Jira-FTFL-596.md](file:///Volumes/DAL/Zettelkasten/LLMeon/30_Library/200_projects/Jira-FTFL-596.md), FTFL-605 (non-prod) requires verification that the SP has `Contributor` + dataprotection roles:

   ```bash
   az role assignment list --assignee <SP_CLIENT_ID> \
     --subscription <NON_PROD_SUBSCRIPTION_ID> --all -o table
   ```

3. Record baseline posture (snapshot before any change):

   ```bash
   az storage account show -g staging-backup-rg -n stagingbackupsa \
     --query "{PublicAccess:publicNetworkAccess, DefaultAction:networkRuleSet.defaultAction, Bypass:networkRuleSet.bypass, PEs:privateEndpointConnections}" -o json
   ```

4. Identify available CIDR space in the staging VNet—from the audit at 11:22 AM, `aks-subnet` (PE policies Disabled) is the only non-delegated candidate. Agree a dedicated `/27` or `/28` CIDR with the network team before proceeding:

   ```bash
   az network vnet list -g fitfile-cloud-staging-rg \
     --query "[].{Name:name,AddressSpace:addressSpace.addressPrefixes}" -o table
   az network vnet subnet list -g fitfile-cloud-staging-rg --vnet-name aks-vnet-32767343  \
     --query "[].{Name:name,Prefix:addressPrefix,Delegations:join(',',delegations[].serviceName)}" -o table
   ```

---

### Phase 1—Terraform: Add Private-Endpoints Subnet (FTFL-615 non-prod)

1. Create a feature branch in `helm_chart_deployment` for the staging change:

   ```bash
   git checkout -b feat/FTFL-615-staging-private-endpoint
   ```

2. Add the `private-endpoints` subnet to the staging private-infra module. In your staging `tfvars`/module config, add:

   ```hcl
   # staging.tfvars (or the equivalent private-infra staging config)
   private_endpoints_subnet_cidr = "10.x.x.x/27"  # TBD — confirm with network team

   # private-infra module HCL
   resource "azurerm_subnet" "private_endpoints" {
     name                 = "private-endpoints"
     resource_group_name  = var.vnet_rg
     virtual_network_name = var.vnet_name
     address_prefixes     = [var.private_endpoints_subnet_cidr]

     private_endpoint_network_policies = "Disabled"
   }
   ```

3. Run `terraform plan` targeting staging and validate no unintended side-effects:

   ```bash
   terraform plan -var-file=staging.tfvars -target=azurerm_subnet.private_endpoints
   ```

4. Apply the subnet after reviewing the plan output:

   ```bash
   terraform apply -var-file=staging.tfvars -target=azurerm_subnet.private_endpoints
   ```

---

### Phase 2—Terraform: Private Endpoint + DNS Zone

1. Add `azurerm_private_endpoint` for `stagingbackupsa` (blob group):

   ```hcl
   resource "azurerm_private_endpoint" "staging_backup_blob" {
     name                = "pe-stagingbackupsa-blob"
     location            = var.location
     resource_group_name = "staging-backup-rg"
     subnet_id           = azurerm_subnet.private_endpoints.id

     private_service_connection {
       name                           = "psc-stagingbackupsa-blob"
       private_connection_resource_id = var.backup_storage_account_id   # stagingbackupsa resource ID
       subresource_names              = ["blob"]
       is_manual_connection           = false
     }
   }
   ```

2. Add privatelink DNS zone + VNet link:

    ```hcl
    resource "azurerm_private_dns_zone" "blob" {
      name                = "privatelink.blob.core.windows.net"
      resource_group_name = "staging-backup-rg"
    }

    resource "azurerm_private_dns_zone_virtual_network_link" "blob_staging" {
      name                  = "link-staging-blob"
      resource_group_name   = "staging-backup-rg"
      private_dns_zone_name = azurerm_private_dns_zone.blob.name
      virtual_network_id    = var.aks_vnet_id   # staging AKS VNet ID
      registration_enabled  = false
    }

    resource "azurerm_private_dns_a_record" "staging_backup_blob" {
      name                = "stagingbackupsa"
      zone_name           = azurerm_private_dns_zone.blob.name
      resource_group_name = "staging-backup-rg"
      ttl                 = 300
      records             = [azurerm_private_endpoint.staging_backup_blob.private_service_connection[0].private_ip_address]
    }
    ```

3. Plan and apply PE + DNS together:

    ```bash
    terraform plan -var-file=staging.tfvars \
      -target=azurerm_private_endpoint.staging_backup_blob \
      -target=azurerm_private_dns_zone.blob \
      -target=azurerm_private_dns_zone_virtual_network_link.blob_staging \
      -target=azurerm_private_dns_a_record.staging_backup_blob

    terraform apply -var-file=staging.tfvars \
      -target=azurerm_private_endpoint.staging_backup_blob \
      -target=azurerm_private_dns_zone.blob \
      -target=azurerm_private_dns_zone_virtual_network_link.blob_staging \
      -target=azurerm_private_dns_a_record.staging_backup_blob
    ```

---

### Phase 3—Lock Down the Storage Account

> ⚠️ This is the breaking change. Do this only after verifying the PE is provisioned and the DNS record resolves correctly from inside the VNet.

1. Verify PE is `Approved` and DNS resolves before flipping public access:

    ```bash
    # Confirm PE approved
    az network private-endpoint show -g staging-backup-rg -n pe-stagingbackupsa-blob \
      --query "privateLinkServiceConnections[0].privateLinkServiceConnectionState" -o json

    # From a pod inside the staging AKS cluster — confirm private DNS resolution
    kubectl run dns-test --image=busybox --restart=Never --rm -it -- \
      nslookup stagingbackupsa.blob.core.windows.net
    # Should resolve to a 10.x.x.x private IP, not a public Azure IP
    ```

2. Apply storage network lockdown via Terraform:

    ```hcl
    resource "azurerm_storage_account" "staging_backup" {
      # ... existing config ...
      public_network_access_enabled = false

      network_rules {
        default_action = "Deny"
        bypass         = []
      }
    }
    ```

    ```bash
    terraform apply -var-file=staging.tfvars -target=azurerm_storage_account.staging_backup
    ```

---

### Phase 4—Validate End-to-End

1. Trigger an on-demand backup job to confirm the backup extension can still reach the storage account via the private endpoint:

    ```bash
    az dataprotection backup-instance adhoc-backup \
      -g staging-backup-rg --vault-name aksbackupvault \
      -n <staging-backup-instance-name> \
      --rule-name BackupIntervals
    ```

2. Monitor the job to completion:

    ```bash
    az dataprotection job list -g staging-backup-rg --vault-name aksbackupvault \
      --query "sort_by([],&properties.startTime)[-5:].{Name:name,Status:properties.status,Start:properties.startTime,End:properties.endTime}" \
      -o table
    ```

    Expected outcome: `Completed` (not `UserErrorKubernetesBackupClusterIsStopped` or any network-related error).

3. Verify no public access to the storage account (negative test):

    ```bash
    # Should be denied from outside the VNet
    az storage blob list --account-name stagingbackupsa --container-name <backup-container> \
      --auth-mode login
    # Expected: AuthorizationFailure or network access blocked
    ```

---

### Phase 5—Document and Gate Production

1. Update [Jira-FTFL-596.md](file:///Volumes/DAL/Zettelkasten/LLMeon/30_Library/200_projects/Jira-FTFL-596.md) with:
    - Timestamp of staging apply
    - Job success confirmation (job ID + completion time)
    - DNS resolution proof
    - Any issues encountered and how they were resolved

2. Tick off the non-prod checklist item in FTFL-615 (non-prod), then raise a PR for the production equivalent targeting NNUH/MKUH—using the same parameterized Terraform templates with production-specific `tfvars`.
3. Get sign-off from a peer (Robin/Enric per your governance practice) before applying to prod—given your Defensive Documentation posture, capture this approval explicitly in Confluence or Jira before proceeding to FTFL-597/598.

---

### Summary Checklist

| # | Action | Blocker/Note |
|---|--------|--------------|
| 0a | Confirm staging cluster running | Must be `Running` |
| 0b | Confirm SP has dataprotection roles (non-prod) | FTFL-605 non-prod |
| 0c | Agree PE subnet CIDR with network team | TBD |
| 1 | Add `private-endpoints` subnet (Terraform apply) | Staging tfvars |
| 2 | Add PE + DNS zone + VNet link (Terraform apply) | Depends on Step 1 |
| 3 | Verify DNS resolution from inside AKS pod | Gate before Step 4 |
| 4 | Flip storage to `Deny` / public access off | Breaking change—do last |
| 5 | Trigger on-demand backup job; confirm `Completed` | Validation |
| 6 | Document findings; update FTFL-615 & FTFL-596.md | Pre-requisite for prod |
| 7 | Raise prod PR, get peer approval → apply NNUH/MKUH | FTFL-597/598 |
