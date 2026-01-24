# Terraform Cloud Integration Setup Guide

This guide configures HCP Vault Dedicated to provide dynamic GitLab tokens to Terraform Cloud workspaces using the Terraform Secrets Engine and JWT authentication.

## Overview

The `terraform_cloud_integration.tf` configuration creates:
- **Terraform Secrets Engine**: For dynamic TFC token generation
- **JWT Authentication**: For TFC workspaces to authenticate to Vault
- **GitLab KV Secrets**: Secure storage for GitLab tokens
- **Vault Policies**: Least-privilege access control
- **JWT Roles**: Scoped access for TFC workspaces

## Prerequisites

1. **HCP Vault Dedicated Cluster**: Active and accessible
2. **Terraform Cloud Organization Token**: For Terraform secrets engine configuration
3. **Terraform Cloud User ID**: For role configuration
4. **GitLab Group Access Token**: To be stored in Vault KV

## Implementation Steps

### 1. Gather Required Information

**Get TFC Organization Token**:
- Navigate to: TFC UI → Settings → API Tokens
- Create Organization Token: `vault-integration`
- Copy the token value

**Get TFC User ID**:
```bash
# Using TFC API with your user token
curl -H "Authorization: Bearer YOUR_USER_TOKEN" \
  https://app.terraform.io/api/v2/account/details | jq -r '.data.id'
```

**Create GitLab Group Access Token**:
- Navigate to: GitLab → Groups → FITFILE → Settings → Access Tokens
- Token Name: `vault-terraform-integration`
- Scopes: `api`
- Role: Developer or Maintainer
- Expiration: 90-365 days

### 2. Deploy Vault Configuration

```bash
# Navigate to Vault configuration directory
cd /Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/hcp/vault

# Set required variables
export TF_VAR_tfc_organization_token="YOUR_TFC_ORG_TOKEN"
export TF_VAR_tfc_user_id="user-XXXXXXXXXX"

# Plan the changes
terraform plan

# Apply the configuration
terraform apply
```

### 3. Store GitLab Token in Vault

After the Vault configuration is applied, store the GitLab token:

```bash
# Set Vault environment
export VAULT_ADDR="https://your-vault-cluster.hashicorp.cloud:8200"
export VAULT_TOKEN="your-vault-token"
export VAULT_NAMESPACE="central"

# Store GitLab token
vault kv put gitlab/token \
  value="YOUR_GITLAB_GROUP_ACCESS_TOKEN" \
  description="GitLab Group Access Token for Terraform operations" \
  scopes="api" \
  expires_at="2025-12-31"
```

### 4. Update TFC Variable Set Configuration

Update your TFC Variable Set to use the new Vault configuration:

```bash
# Navigate to TFC configuration
cd /Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/hcp/tfc

# Set the Vault address variable
export TF_VAR_hcp_vault_dedicated_address="https://your-vault-cluster.hashicorp.cloud:8200"

# Apply the updated Variable Set configuration
terraform apply
```

## Configuration Details

### Vault Paths Created

- **Terraform Secrets Engine**: `central/terraform/`
- **GitLab KV Secrets**: `central/gitlab/`
- **JWT Auth Method**: `central/jwt-tfc/`

### JWT Roles

1. **tfc-role**: General access for all FITFILE-Platforms workspaces
2. **tfc-gitlab-role**: Restricted to specific projects needing GitLab access

### Policies

- **tfc-gitlab-access**: Allows reading GitLab secrets and Terraform credentials

## Verification Steps

### 1. Verify Vault Configuration

```bash
# Check Terraform secrets engine
vault secrets list -namespace=central

# Check JWT auth method
vault auth list -namespace=central

# Verify GitLab secret exists
vault kv get -namespace=central gitlab/token
```

### 2. Test JWT Authentication

```bash
# Test JWT role configuration
vault read -namespace=central auth/jwt-tfc/role/tfc-role
vault read -namespace=central auth/jwt-tfc/role/tfc-gitlab-role
```

### 3. Test Dynamic Credentials

Create a test workspace with the following configuration:

```hcl
terraform {
  required_providers {
    vault = {
      source  = "hashicorp/vault"
      version = "~> 4.0"
    }
    gitlab = {
      source  = "gitlabhq/gitlab"
      version = "~> 17.0"
    }
  }
}

provider "vault" {
  # Uses dynamic credentials from TFC
  namespace = "central"
}

data "vault_kv_secret_v2" "gitlab_token" {
  mount = "gitlab"
  name  = "token"
}

provider "gitlab" {
  token = data.vault_kv_secret_v2.gitlab_token.data["value"]
}

data "gitlab_user" "current" {}

output "authenticated_user" {
  value = data.gitlab_user.current.username
}
```

## Security Features

✅ **Dynamic Authentication**: TFC workspaces authenticate using JWT tokens
✅ **Least Privilege**: Scoped policies and roles
✅ **Short-lived Tokens**: 1-hour default TTL, 24-hour maximum
✅ **Namespace Isolation**: All resources in dedicated `central` namespace
✅ **Audit Trail**: All Vault operations are logged

## Token Rotation

### Manual Rotation

1. **Generate New GitLab Token** in GitLab UI
2. **Update Vault Secret**:
   ```bash
   vault kv put -namespace=central gitlab/token \
     value="NEW_GITLAB_TOKEN" \
     description="Rotated GitLab Group Access Token" \
     scopes="api" \
     expires_at="2026-12-31"
   ```
3. **Test**: Trigger a TFC run to verify new token works

### Automated Rotation (Future Enhancement)

Consider implementing automated rotation using:
- Vault's GitLab secrets engine (if available)
- Custom rotation scripts with Vault Agent
- GitLab API automation for token lifecycle

## Troubleshooting

### Common Issues

1. **JWT Authentication Fails**:
   - Verify `bound_claims` match TFC workspace metadata
   - Check TFC workspace is in correct organization/project

2. **GitLab Token Access Denied**:
   - Verify policy allows `gitlab/data/token` path
   - Check namespace is correctly set to `central`

3. **Terraform Secrets Engine Issues**:
   - Verify TFC organization token has correct permissions
   - Check TFC User ID is valid and accessible

### Debug Commands

```bash
# Check JWT token claims (from TFC run)
vault write -namespace=central auth/jwt-tfc/login \
  role=tfc-role \
  jwt="$TFC_WORKLOAD_IDENTITY_TOKEN"

# Test policy permissions
vault policy read -namespace=central tfc-gitlab-access

# Check secret accessibility
vault kv get -namespace=central gitlab/token
```

## Next Steps

1. **Deploy Configuration**: Apply the Vault Terraform configuration
2. **Store GitLab Token**: Add your GitLab token to Vault KV
3. **Update TFC Variables**: Configure Variable Set with Vault address
4. **Test Integration**: Create test workspace to verify functionality
5. **Update Workspaces**: Migrate existing workspaces to use dynamic credentials

This setup provides a secure, scalable foundation for GitLab token distribution across your Terraform Cloud workspaces using 2025 best practices.
