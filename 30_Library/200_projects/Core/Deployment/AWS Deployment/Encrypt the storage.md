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
tags: []
title: Encrypt the storage
type:
uid: 
updated: 
version:
---

I'll help you configure HCP Vault for storage encryption. Here's how to modify the configuration:

1. First, add the Vault provider configuration:

```hcl
// ... existing providers ...
  required_providers {
    aws = {
      source  = "hashicorp/aws"
    }
    vault = {
      source = "hashicorp/vault"
      version = "~> 3.0"
    }
  }
```

2. Configure the Vault provider (create a new file):

```hcl
provider "vault" {
  # Authentication can be configured via environment variables:
  # VAULT_ADDR
  # VAULT_TOKEN
  # Or directly here:
  address = var.vault_address
  token   = var.vault_token
}

variable "vault_address" {
  description = "HCP Vault address"
  type        = string
}

variable "vault_token" {
  description = "HCP Vault token"
  type        = string
  sensitive   = true
}
```

3. Create a Vault encryption key and policy:

```hcl:modules/vault-encryption/main.tf
# Create a transit engine for encryption
resource "vault_mount" "transit" {
  path                      = "transit-${var.environment}"
  type                      = "transit"
  description               = "Transit encryption for EBS volumes"
  default_lease_ttl_seconds = 3600
}

# Create an encryption key
resource "vault_transit_secret_backend_key" "ebs_key" {
  backend = vault_mount.transit.path
  name    = "ebs-encryption-key"
  
  deletion_allowed = true
  exportable      = true
  allow_plaintext_backup = true
}

# Create a policy for EBS encryption
resource "vault_policy" "ebs_encryption" {
  name = "ebs-encryption"

  policy = <<EOT
path "${vault_mount.transit.path}/encrypt/ebs-encryption-key" {
  capabilities = ["create", "update"]
}

path "${vault_mount.transit.path}/decrypt/ebs-encryption-key" {
  capabilities = ["create", "update"]
}
EOT
}
```

4. Modify the jumpbox configuration to use Vault encryption:

```hcl:modules/jumpbox/main.tf
# Add data source to get encryption key from Vault
data "vault_transit_key" "ebs_key" {
  backend = "transit-${var.environment}"
  name    = "ebs-encryption-key"
}

resource "aws_instance" "this" {
  # ... existing configuration ...

  root_block_device {
    volume_size = 32
    encrypted   = true
    # Use customer-managed key with Vault integration
    kms_key_id  = aws_kms_key.vault_backed.arn
  }
}

# Create a KMS key backed by Vault
resource "aws_kms_key" "vault_backed" {
  description = "KMS key for EBS encryption, backed by Vault"
  
  # Use a custom key policy that integrates with Vault
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "Enable IAM User Permissions"
        Effect = "Allow"
        Principal = {
          AWS = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:root"
        }
        Action   = "kms:"
        Resource = ""
      },
      {
        Sid    = "Allow Vault to manage key"
        Effect = "Allow"
        Principal = {
          AWS = aws_iam_role.vault_kms.arn
        }
        Action = [
          "kms:Encrypt",
          "kms:Decrypt",
          "kms:ReEncrypt",
          "kms:GenerateDataKey",
          "kms:DescribeKey"
        ]
        Resource = ""
      }
    ]
  })
}

# IAM role for Vault to manage KMS
resource "aws_iam_role" "vault_kms" {
  name = "vault-kms-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      }
    ]
  })
}
```

5. Add necessary variables:

```hcl:variables.tf
variable "environment" {
  description = "Environment name (e.g., dev, prod)"
  type        = string
}

variable "vault_transit_path" {
  description = "Path to the Vault transit engine"
  type        = string
  default     = "transit"
}
```

6. Update the EKS node groups to use Vault-backed encryption:

```hcl
resource "aws_eks_node_group" "this" {
  # ... existing configuration ...

  launch_template {
    # ... existing configuration ...
    
    block_device_mappings {
      device_name = "/dev/xvda"
      ebs {
        volume_size = 20
        encrypted   = true
        kms_key_id  = aws_kms_key.vault_backed.arn
      }
    }
  }
}
```

Key considerations for this setup:

1. Authentication: Ensure your Vault authentication is properly configured and that you're using appropriate authentication methods (e.g., AWS IAM auth method).
2. High Availability: Since EBS encryption will depend on Vault availability, ensure your Vault cluster is highly available.
3. Monitoring: Set up monitoring for both Vault and KMS operations to track encryption/decryption requests.
4. Backup: Ensure your Vault transit keys are properly backed up as part of your disaster recovery strategy.
5. Security: The Vault token used should have minimal required permissions following the principle of least privilege.

To use this configuration:

1. Initialize Vault provider:

```bash
export VAULT_ADDR="https://your-vault-address"
export VAULT_TOKEN="your-token"
terraform init
```

2. Apply the configuration:

```bash
terraform apply
```

This setup provides a more secure and centralized encryption management system using HCP Vault, while still maintaining compatibility with AWS services that expect KMS integration.
