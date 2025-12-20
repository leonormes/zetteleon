---
aliases: []
confidence: 
created: 2025-02-07T12:57:56Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:51Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [ff_deploy]
title: Azure Customer Checklist
type: instruction
uid: 
updated: 
version: 1
---

## Azure Customer Preparation Checklist

### Overview

This document outlines the necessary steps for preparing your Azure Tenant and Subscription for a FITFILE deployment. Each step is crucial for ensuring a successful deployment process.

### Required Setup Components

The following components must be configured in your Azure environment:

1. Azure Tenant (We need the Tenant ID)
2. Azure Subscription within the tenant (We need the Subscription ID)
3. Resource Provider registration in the Azure Subscription
4. Service Principal with Contributor access
5. Encryption at host enabled on the subscription
6. Correct compute quota configuration
7. FITFILE DevOps user access with Contributor role
8. Firewall configuration for FITFILE central services access

### Detailed Setup Instructions

#### 1. Register Resource Providers

Navigate to your subscription and register these essential resource providers:

```bash
# Required Resource Providers
Microsoft.ContainerService    # For Kubernetes Service
Microsoft.ManagedIdentity    # For kubernetes managed identities
Microsoft.Network           # For networking infrastructure
Microsoft.Storage          # For storage accounts
Microsoft.Compute         # For virtual machines
```

To register providers:

1. Navigate to the subscription
2. Click on "Resource Providers" in the side panel
3. Register each provider one by one

#### 2. Create Service Principal

1. Navigate to Microsoft Entra ID
2. Access App registrations
3. Click Add
4. Name it "FITFILE Terraform Cloud Provisioner"
5. On the overview page, click "Certificates & secrets"
6. Add a new secret and save both:
   - Secret ID
   - Secret Value
7. Copy the Application (client) ID from the overview page

#### 3. Configure Service Principal Permissions

After creating the service principal, assign the necessary roles:

1. Navigate to the subscription's access control
2. Add role assignment for Contributor:
   - Select "Privileged role administrator roles"
   - Choose "Contributor"
   - Assign to "User, group or service principal"
   - Select the FITFILE service principal

3. Add role assignment for User Access Administrator:
   - Follow the same process but select "User Access Administrator"
   - Add condition to constrain role to Network Contributor

#### 4. Enable Encryption at Host

Execute these commands in your terminal:

```bash
# Login to Azure
az login

# Register encryption feature
az feature register --namespace microsoft.compute --name EncryptionAtHost

# Verify registration (may take up to 20 minutes)
az feature show --namespace Microsoft.Compute --name EncryptionAtHost
```

#### 5. Configure Compute Quota

Your subscription needs the correct quota for ESv5 Series virtual CPUs:

1. Access the subscription
2. Go to "Usage & quotas"
3. Set filters:
   - Provider: Compute
   - Region: uk south
4. Search for "Es"
5. Select "Standard ESv5 Family vCPUs"
6. Request new quota limit of 10
7. Submit request and await approval

#### 6. Add FITFILE DevOps User

1. In Microsoft Entra ID:
   - Go to Users
   - Click "New User"
   - Select "Invite external user"
   - Enter FITFILE user's email and details
   - Change user type from Guest to Member

2. After invitation acceptance:
   - Go to subscription access control
   - Add role assignment
   - Assign Contributor role to FITFILE user

### Network Configuration

#### FITFILE Central Services Outbound Allow List

| Service | Purpose | URL | Protocol | Type |
|---------|---------|-----|----------|------|
| Hashicorp Vault | Secrets management | <https://vault-public-vault-8b38a0c2.e3dedc53.z1.hashicorp.cloud:8200/> | HTTPS | FQDN |
| Auth0 tenant | Authentication | <https://fitfile-prod.eu.auth0.com> | HTTPS | FQDN |
| Grafana (Prometheus) | Metrics | <https://prometheus-prod-05-gb-south-0.grafana.net> | HTTPS | FQDN |
| Grafana (Loki) | Logs | <https://logs-prod-008.grafana.net> | HTTPS | FQDN |
| Grafana (Tempo) | Traces | <https://tempo-prod-06-prod-gb-south-0.grafana.net> | HTTPS | FQDN |
| Gitlab | Deployment config | <https://gitlab.com> | HTTPS | FQDN |
| Azure Container Registry | Container images | fitfileregistry.azurecr.io | HTTPS | FQDN |

#### Auth0 Callback IPs

The following IPs must be allowed for Auth0 callback responses:

```sh
18.197.9.11, 18.198.229.148, 3.125.185.137, 3.65.249.224,
3.67.233.131, 3.68.125.137, 3.72.27.152, 3.74.90.247,
34.246.118.27, 35.157.198.116, 35.157.221.52, 52.17.111.199,
52.19.3.147, 52.208.95.174, 52.210.121.45, 52.210.122.50,
52.28.184.187, 52.30.153.34, 52.57.230.214, 54.228.204.106,
54.228.86.224, 54.73.137.216, 54.75.208.179, 54.76.184.103
```

### Service Principal Permissions

The service principal requires specific permissions defined in Terraform. Here's the complete permission set:

```hcl
resource "azurerm_role_definition" "private_aks" {
  name  = "private-aks-provisioner"
  scope = data.<given_subscription_id>
  
  permissions {
    actions =
      "Microsoft.Authorization/roleAssignments/",
      "Microsoft.Compute/disks/",
      "Microsoft.Compute/virtualMachines/",
      "Microsoft.Compute/virtualMachines/extensions/",
      "Microsoft.Compute/virtualMachines/powerOff/action",
      "Microsoft.ContainerService/managedClusters/",
      "Microsoft.ManagedIdentity/userAssignedIdentities/",
      "Microsoft.Network/networkInterfaces/",
      "Microsoft.Network/networkSecurityGroups/",
      "Microsoft.Network/privateDnsZones/",
      "Microsoft.Network/publicIPAddresses/",
      "Microsoft.Network/virtualNetworks/",
      "Microsoft.Resources/subscriptions/providers/read",
      "Microsoft.Resources/subscriptions/resourcegroups/"
    ]
    not_actions =
  }
  
  assignable_scopes =
    data.<given_subscription_id>
  ]
}
```
