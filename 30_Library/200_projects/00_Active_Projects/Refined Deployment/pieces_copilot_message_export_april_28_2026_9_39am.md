---
created: 2026-04-28T08:39:00+00:00
modified: 2026-04-28T12:48:01+00:00
title: pieces_copilot_message_export_april_28_2026_9_39am
---

## FTFL-596—What You Have vs. What You Still Need

You've made solid progress. Here's how your current output maps against the ticket's pre-flight questions.

---

### ✅ Questions Now Answered (from Prod Baseline)

Your `prod-1-backup-v2-rg` policy output directly answers three of the six questions:

| Ticket Question | Answer Extracted |
|---|---|
| Q1: Backup frequency | Daily at 9:00 PM UTC (`R/2024-09-02T21:00:00+00:00/P1D`)—outside operational hours ✅ |
| Q2: Retention period | 14 days (`P14D` absolute delete) ✅ |
| Q3: Minimum backups to retain | Implicit 14 (daily cadence × 14-day retention)—not an explicit count policy, worth confirming |

---

### ❌ Gaps Still to Close

#### 1. What PVCs/Namespaces Are Actually Being Backed Up? (Q5)

You know _one instance_ (`prod1aksdailyv2`) is `ProtectionConfigured`, but you don't yet know which namespaces or PVCs it covers. Drill into the instance detail:

```bash
az dataprotection backup-instance show \
  --resource-group prod-1-backup-v2-rg \
  --vault-name aksbackupvault \
  --name prod1aksdailyv2 \
  --query "properties.policyInfo.policyParameters"
```

This will reveal the `includedNamespaces`, `includedResourceTypes`, and `labelSelectors`—which tells you whether MongoDB, SpiceDB, PostgreSQL, and The Hyve OMOP PVCs are all covered or if there are gaps. This directly answers Q5 (do different PVCs have different requirements?).

---

#### 2. Terraform SA Permissions—NNUH & MKUH Directories (FTFL-605 / Q6)

You need to switch context to each customer's Azure directory. You can see you have access to both in your portal settings (`nnuhnorwich.onmicrosoft.com` and `mkuh.nhs.uk`).

For each, check the Terraform SA's role assignments:

```bash
# Switch to NNUH tenant first
az login --tenant "nnuhnorwich.onmicrosoft.com"

# Find the Terraform Service Principal (replace with actual SP name/app ID)
az ad sp list --display-name "<terraform-sp-name>" --query "[].{AppId:appId, DisplayName:displayName}"

# Check its role assignments at subscription or RG level
az role assignment list \
  --assignee "<app-id-of-terraform-sp>" \
  --all \
  --query "[].{Role:roleDefinitionName, Scope:scope}" \
  -o table
```

Repeat for MKUH (`mkuh.nhs.uk`). You're looking for Contributor or Role Based Access Control Administrator at either subscription or target resource group scope. If absent, you need to raise a change request with the customer (as per FTFL-605).

---

#### 3. `Microsoft.DataProtection` Resource Provider Registered? (FTFL-605)

Also per FTFL-605—confirm the resource provider is registered in both customer subscriptions:

```bash
# Run once per tenant (after switching context)
az provider show \
  --namespace Microsoft.DataProtection \
  --query "{Namespace:namespace, State:registrationState}" \
  -o table
```

If it returns `NotRegistered`, you'll need to either register it yourself (requires Contributor) or raise a change request.

---

#### 4. Cost Factored Into Node Costs? (Q4)

This one can't be answered via CLI—it's a stakeholder confirmation question. You'll need to verify with whoever owns node cost estimates (likely the commercial/delivery side) that Azure Backup storage costs for both NNUH and MKUH have been included. Given the OMOP data is specifically called out, this is worth a direct confirmation before deploying.

---

### Summary: Your Next Commands

```bash
# 1. See which PVCs/namespaces prod currently backs up
az dataprotection backup-instance show \
  --resource-group prod-1-backup-v2-rg \
  --vault-name aksbackupvault \
  --name prod1aksdailyv2 \
  --query "properties.policyInfo.policyParameters"

# 2. Switch to NNUH and check TF SA permissions + resource provider
az login --tenant "nnuhnorwich.onmicrosoft.com"
az provider show --namespace Microsoft.DataProtection --query "{Namespace:namespace, State:registrationState}" -o table
az role assignment list --assignee "<tf-sp-app-id>" --all --query "[].{Role:roleDefinitionName, Scope:scope}" -o table

# 3. Repeat for MKUH
az login --tenant "mkuh.nhs.uk"
az provider show --namespace Microsoft.DataProtection --query "{Namespace:namespace, State:registrationState}" -o table
az role assignment list --assignee "<tf-sp-app-id>" --all --query "[].{Role:roleDefinitionName, Scope:scope}" -o table
```

Once you have the namespace/PVC coverage from step 1 and the SA role status from steps 2–3, you'll have enough to either proceed directly with the Terraform changes to `NNUH-DP/main.tf` and `mkuh-prd-4`, or raise the change requests first as a blocker for [FTFL-597](https://fitfile.atlassian.net/browse/FTFL-597) and [FTFL-598](https://fitfile.atlassian.net/browse/FTFL-598).
