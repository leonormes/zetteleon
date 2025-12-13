---
aliases: []
confidence: 
created: 2025-02-07T12:57:56Z
dependencies: 
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:45Z
name: cicd_minimal_permissions
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [cli, gitops]
title: cicd_minimal_permissions
type: security_configuration
uid: 
updated: 
version:
---

## Minimal IAM Permissions for GitOps Infrastructure Deployment

### Overview

This document outlines the minimal IAM permissions required for a secure GitOps workflow using Terraform Cloud (TFC) and GitLab. The setup ensures:

- Changes only deploy from the main branch
- Required peer review before merging
- Principle of least privilege
- Service principal-based authentication
- No direct user access to cloud resources

### GitLab Configuration

#### Branch Protection Rules

1. Main Branch Protection

```yaml
protected_branches:
 - name: main
   allowed_to_push:
   allowed_to_merge:
     - group_ids:
   require_code_owner_approval: true
   require_approvals: true
   approvals_required: 2
   code_owner_approval_required: true
   reject_unsigned_commits: true
```

2. Required Status Checks

```yaml
status_checks:
 - context: "terraform/plan"
   required: true
 - context: "security/scan"
   required: true
 - context: "lint/tflint"
   required: true
```

#### Repository Settings

```yaml
repository:
  allow_force_push: false
  allow_merge_on_skipped_pipeline: false
  only_allow_merge_if_pipeline_succeeds: true
  only_allow_merge_if_all_discussions_are_resolved: true
```

### Terraform Cloud Configuration

#### Workspace Configuration

```hcl
# workspace.tf
resource "tfe_workspace" "infrastructure" {
  name                = "infrastructure"
  organization        = var.tfc_org_name
  working_directory   = "terraform/"
  execution_mode      = "remote"
  auto_apply          = false
  queue_all_runs      = false
  global_remote_state = false
  
  vcs_repo {
    identifier     = "organization/repository"
    branch         = "main"
    oauth_token_id = var.gitlab_oauth_token
  }
}

# Limit who can approve runs
resource "tfe_team" "approvers" {
  name         = "infrastructure-approvers"
  organization = var.tfc_org_name
}

resource "tfe_team_token" "approver_token" {
  team_id = tfe_team.approvers.id
}
```

### AWS IAM Configuration

#### TFC Service Role

```hcl
# aws_iam.tf
resource "aws_iam_role" "tfc_role" {
  name = "tfc-deployment-role"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement =
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          AWS = "arn:aws:iam::${var.tfc_account_id}:root"
        }
        Condition = {
          StringEquals = {
            "sts:ExternalId": var.tfc_workspace_id
          }
        }
      }
    ]
  })
}

# Minimal EKS deployment permissions
resource "aws_iam_role_policy" "eks_deployment" {
  name = "eks-deployment-policy"
  role = aws_iam_role.tfc_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement =
      {
        Effect = "Allow"
        Action =
          "eks:CreateCluster",
          "eks:DeleteCluster",
          "eks:DescribeCluster",
          "eks:UpdateClusterVersion",
          "eks:UpdateClusterConfig"
        ]
        Resource = "arn:aws:eks:${var.region}:${var.account_id}:cluster/"
      },
      {
        Effect = "Allow"
        Action =
          "ec2:CreateVpc",
          "ec2:DeleteVpc",
          "ec2:ModifyVpcAttribute",
          "ec2:CreateSubnet",
          "ec2:DeleteSubnet",
          "ec2:ModifySubnetAttribute"
        ]
        Resource = ""
        Condition = {
          StringEquals = {
            "aws:ResourceTag/Environment":
          }
        }
      }
    ]
  })
}
```

### Azure Service Principal Configuration

#### Minimal RBAC for TFC

```hcl
# azure_rbac.tf
resource "azuread_service_principal" "tfc" {
  application_id = var.tfc_application_id
}

resource "azurerm_role_assignment" "tfc_aks" {
  scope                = azurerm_resource_group.aks.id
  role_definition_name = "AKS Cluster Creator"
  principal_id         = azuread_service_principal.tfc.object_id
}

resource "azurerm_role_assignment" "tfc_network" {
  scope                = azurerm_resource_group.network.id
  role_definition_name = "Network Contributor"
  principal_id         = azuread_service_principal.tfc.object_id
}

# Custom role with minimal permissions
resource "azurerm_role_definition" "tfc_custom" {
  name        = "TFC Minimal Access"
  scope       = data.azurerm_subscription.primary.id
  description = "Custom role for TFC with minimal permissions"

  permissions {
    actions =
      "Microsoft.ContainerService/managedClusters/read",
      "Microsoft.ContainerService/managedClusters/write",
      "Microsoft.Network/virtualNetworks/read",
      "Microsoft.Network/virtualNetworks/subnets/read",
      "Microsoft.Network/virtualNetworks/subnets/join/action"
    ]
    not_actions =
  }

  assignable_scopes =
    data.azurerm_subscription.primary.id
  ]
}
```

### TFC Environment Variables

#### AWS Authentication

```hcl
resource "tfe_variable" "aws_role_arn" {
  workspace_id = tfe_workspace.infrastructure.id
  category     = "env"
  key         = "AWS_ROLE_ARN"
  value       = aws_iam_role.tfc_role.arn
  sensitive   = true
}

resource "tfe_variable" "aws_external_id" {
  workspace_id = tfe_workspace.infrastructure.id
  category     = "env"
  key         = "AWS_EXTERNAL_ID"
  value       = var.tfc_workspace_id
  sensitive   = true
}
```

#### Azure Authentication

```hcl
resource "tfe_variable" "azure_client_id" {
  workspace_id = tfe_workspace.infrastructure.id
  category     = "env"
  key         = "ARM_CLIENT_ID"
  value       = azuread_service_principal.tfc.application_id
  sensitive   = true
}

resource "tfe_variable" "azure_client_secret" {
  workspace_id = tfe_workspace.infrastructure.id
  category     = "env"
  key         = "ARM_CLIENT_SECRET"
  value       = azuread_service_principal_password.tfc.value
  sensitive   = true
}
```

### Security Controls

#### Access Control Matrix

| Role                    | GitLab                  | TFC                    | Cloud Resources |
|------------------------|-------------------------|------------------------|-----------------|
| Developer              | Push to feature branches| View plans             | No access      |
| Infrastructure Maintainer| Merge to main         | Approve applies        | No access      |
| Service Principal      | N/A                    | Execute plans/applies  | Limited RBAC   |

#### Audit Requirements

1. GitLab Audit Events
   - Branch protection changes
   - Merge request approvals
   - Repository setting changes

2. TFC Audit Events
   - Plan executions
   - Apply approvals
   - Variable changes
   - Team membership changes

3. Cloud Provider Audit
   - AWS CloudTrail
   - Azure Activity Logs
   - Service principal usage

### Implementation Steps

1. Initial Setup

   ```bash
   # Create service principals
   az ad sp create-for-rbac --name "tfc-deployer" --role "Contributor"
   aws iam create-role --role-name tfc-deployer --assume-role-policy-document file://trust-policy.json
   ```

2. GitLab Configuration
   - Enable branch protection
   - Configure required approvals
   - Set up status checks

3. TFC Configuration
   - Create workspace
   - Configure VCS integration
   - Set up environment variables

4. Validation

   ```bash
   # Test TFC role assumption
   aws sts assume-role --role-arn $TFC_ROLE_ARN --external-id $TFC_WORKSPACE_ID
   
   # Test Azure SP access
   az login --service-principal -u $CLIENT_ID -p $CLIENT_SECRET --tenant $TENANT_ID
   ```

### Security Best Practices

1. Rotation Schedule
   - Service principal credentials: 90 days
   - TFC team tokens: 180 days
   - OAuth tokens: 365 days

2. Access Reviews
   - Monthly review of maintainers group
   - Quarterly review of service principal permissions
   - Semi-annual review of workspace configurations

3. Monitoring
   - Alert on unauthorized access attempts
   - Monitor for unused permissions
   - Track failed pipeline executions

### Related Documentation
