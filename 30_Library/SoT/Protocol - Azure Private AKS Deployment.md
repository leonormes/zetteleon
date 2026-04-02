---
aliases: ["Private AKS Permissions", "AKS RBAC Setup", "Terraform AKS Permissions"]
created: 2026-04-02T10:30:00Z
last_reviewed: 2026-04-02
modified: 2026-04-02T10:30:00Z
status: evergreen
tags: ["azure", "aks", "terraform", "rbac", "protocol"]
title: Protocol - Azure Private AKS Deployment
type: "protocol"
---

## Logic Map
**Objective:** Configure a Service Principal (SP) or Managed Identity with the minimum necessary permissions to deploy a Private AKS cluster, specifically handling the automatic RBAC role assignments that occur during provisioning.

**Dependencies:**
- Azure CLI or Terraform
- Target Subscription ID
- Target Subnet and (optional) Private DNS Zone

---

## The Algorithm

### 1. Identify Required Permissions
A standard "Contributor" role is insufficient because AKS needs to assign roles (e.g., `Network Contributor`) to its own managed identity during deployment. This requires the `Microsoft.Authorization/roleAssignments/write` permission.

### 2. Assign Deployment Role to Service Principal
Grant the deployment identity (e.g., Terraform Cloud SP) one of the following roles at the required scope:

- **Option A: Role Based Access Control Administrator** (Recommended - Least Privilege for RBAC)
- **Option B: User Access Administrator** (Common but broader)

#### Execution (Azure CLI):
```bash
# Assign RBAC Admin at the subscription level
az role assignment create \
  --assignee <SP_APP_ID> \
  --role "Role Based Access Control Administrator" \
  --scope /subscriptions/<SUBSCRIPTION_ID>
```

### 3. Scope the Permissions (Narrower Alternative)
Instead of the entire subscription, apply the "User Access Administrator" role only to the specific resources where AKS will perform assignments:
- **The AKS Subnet** (For `Network Contributor` assignment)
- **The Private DNS Zone** (For `Private DNS Zone Contributor` assignment)

---

## Terraform Implementation

Ensure the Terraform runner's identity has the permission to create `azurerm_role_assignment` resources.

### Step 1: Grant TFC Identity Permission to assign roles
```hcl
# The TFC Service Principal gets permission to create role assignments on the subnet
resource "azurerm_role_assignment" "tfc_uaa_on_subnet" {
  scope                = azurerm_subnet.aks.id
  role_definition_name = "User Access Administrator"
  principal_id         = data.azuread_service_principal.tfc.object_id
}
```

### Step 2: AKS Cluster Identity Assignment (The one that usually fails without Step 1)
```hcl
# AKS identity gets Network Contributor on its own subnet
resource "azurerm_role_assignment" "aks_net_contrib" {
  scope                = azurerm_subnet.aks.id
  role_definition_name = "Network Contributor"
  principal_id         = azurerm_kubernetes_cluster.main.identity[0].principal_id
  
  # Ensure the TFC permission is in place first
  depends_on = [azurerm_role_assignment.tfc_uaa_on_subnet]
}
```

---

## Error Handling

### Symptom: `AuthorizationFailed` on `roleAssignments/write`
- **Cause:** The identity running the deployment has "Contributor" but lacks "User Access Administrator" or "RBAC Administrator".
- **Fix:** Verify the `assignee` of the role assignment has the `Microsoft.Authorization/roleAssignments/write` action.

### Symptom: Subnet does not have Network Contributor
- **Cause:** Provisioning failed mid-way or the SP lacked permissions to assign the role to the AKS Managed Identity.
- **Fix:** Manually assign `Network Contributor` to the AKS Cluster Identity on the subnet scope.

---

## Unit Test (Success Criteria)
- [ ] `terraform apply` completes without `AuthorizationFailed` errors during role assignment phases.
- [ ] The AKS Cluster Identity appears in the Access Control (IAM) list of the target subnet with the `Network Contributor` role.
- [ ] (If Private DNS used) The AKS Cluster Identity has `Private DNS Zone Contributor` on the auto-created or custom DNS zone.
