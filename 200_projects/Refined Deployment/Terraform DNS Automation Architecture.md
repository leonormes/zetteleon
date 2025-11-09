---
aliases: []
confidence: 
created: 2025-09-22T16:09:41Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T14:24:13Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [topic/technology/networking/dns]
title: Terraform DNS Automation Architecture
type:
uid: 
updated: 
version:
---

## Overview

This document defines the Terraform module architecture for automated DNS/hostname/Auth0 provisioning based on the Unified DNS Naming Policy. The system generates all required DNS records, certificates, and Auth0 configurations from minimal input parameters.

## Module Structure

### Core Module: `terraform-dns-automation`

```sh
terraform-dns-automation/
├── main.tf                 # Main module orchestration
├── variables.tf           # Input variable definitions
├── outputs.tf            # Generated hostnames and configurations
├── locals.tf             # DNS logic and hostname generation
├── versions.tf           # Provider requirements
├── modules/
│   ├── dns-records/      # DNS record management
│   ├── certificates/     # Certificate provisioning
│   ├── auth0/           # Auth0 tenant configuration
│   └── vault-secrets/   # Vault secret management
└── examples/
    ├── private-deployment/
    ├── public-deployment/
    └── customer-domain/
```

## Input Variables

### Primary Configuration

```hcl
# variables.tf
variable "deployment_config" {
  description = "Core deployment configuration"
  type = object({
    deployment_key    = string           # e.g., "cuh-prod-1"
    customer_name     = string           # e.g., "Cambridge University Hospitals"
    environment       = string           # prod, dev, test, staging

    # DNS Configuration
    customer_domain   = optional(string) # e.g., "nhstrust.co.uk"
    is_private        = bool             # true for private deployments

    # Regional Settings
    azure_region      = string           # e.g., "uksouth"

    # Service Configuration
    enabled_services  = list(string)     # ["app", "argocd", "workflows", "relay"]

    # Auth0 Configuration
    auth0_environment = string           # "prod" or "non-prod"

    # Certificate Preferences
    use_private_ca    = bool             # Use HCP Vault for internal certs
  })

  validation {
    condition = can(regex("^[a-z0-9]+-[a-z]+-[0-9]+$", var.deployment_config.deployment_key))
    error_message = "Deployment key must follow format: {customer}-{env}-{instance}"
  }
}

variable "dns_providers" {
  description = "DNS provider configurations"
  type = object({
    cloudflare = optional(object({
      api_token = string
      zone_id   = string
    }))

    azure_private_dns = optional(object({
      resource_group_name = string
      subscription_id     = string
    }))
  })
}

variable "certificate_config" {
  description = "Certificate management configuration"
  type = object({
    acme_email        = string
    vault_pki_path    = optional(string, "pki_int")
    cert_manager_namespace = optional(string, "cert-manager")
  })
}

variable "auth0_config" {
  description = "Auth0 tenant configuration"
  type = object({
    domain        = string  # e.g., "fitfile-prod.eu.auth0.com"
    client_id     = string
    client_secret = string
  })
}
```

## DNS Logic Implementation

### Hostname Generation Logic

```hcl
# locals.tf
locals {
  # Parse deployment key components
  deployment_parts = split("-", var.deployment_config.deployment_key)
  customer_code    = local.deployment_parts[0]
  environment      = local.deployment_parts[1]
  instance         = local.deployment_parts[2]

  # Determine primary DNS zone based on configuration
  primary_zone = (
    var.deployment_config.customer_domain != null ? var.deployment_config.customer_domain :
    var.deployment_config.is_private ? "privatelink.fitfile.net" :
    "fitfile.net"
  )

  # Internal zones are always consistent
  internal_zone = "m2m.fitfile.internal"
  nhs_zone     = "nhs.fitfile.internal"

  # Generate service hostnames for user access layer
  user_hostnames = {
    for service in var.deployment_config.enabled_services :
    service => (
      var.deployment_config.customer_domain != null ?
      "${service}.${var.deployment_config.customer_domain}" :
      service == "app" ?
      "${var.deployment_config.deployment_key}.${local.primary_zone}" :
      "${service}.${var.deployment_config.deployment_key}.${local.primary_zone}"
    )
  }

  # Generate service hostnames for M2M layer
  m2m_hostnames = {
    for service in ["relay", "coordinator", "api"] :
    service => "${service}.${var.deployment_config.deployment_key}.${local.internal_zone}"
  }

  # Generate NHS-specific hostnames
  nhs_hostnames = {
    proxy       = "proxy.${var.deployment_config.deployment_key}.${local.nhs_zone}"
    integration = "integration.${var.deployment_config.deployment_key}.${local.nhs_zone}"
  }

  # Auth0 configuration
  auth0_audience = local.user_hostnames["app"]
  auth0_callback_urls = [
    "https://${local.user_hostnames["app"]}/callback",
    "https://${local.user_hostnames["app"]}/auth/callback"
  ]

  # Certificate requirements
  public_certificates = [
    for hostname in values(local.user_hostnames) : hostname
    if var.deployment_config.customer_domain != null || !var.deployment_config.is_private
  ]

  private_certificates = [
    for hostname in values(local.m2m_hostnames) : hostname
  ]
}
```

## DNS Records Module

### DNS Record Management

```hcl
# modules/dns-records/main.tf
resource "cloudflare_record" "public_records" {
  for_each = var.cloudflare_enabled ? var.public_hostnames : {}

  zone_id = var.cloudflare_zone_id
  name    = split(".", each.value)[0]
  value   = var.load_balancer_ip
  type    = "A"
  ttl     = 300

  comment = "Auto-generated for ${var.deployment_key}"
}

resource "azurerm_private_dns_a_record" "private_records" {
  for_each = var.azure_private_dns_enabled ? var.private_hostnames : {}

  name                = split(".", each.value)[0]
  zone_name          = var.private_dns_zone_name
  resource_group_name = var.resource_group_name
  ttl                = 300
  records            = [var.private_load_balancer_ip]

  tags = {
    deployment_key = var.deployment_key
    managed_by    = "terraform"
  }
}

resource "azurerm_private_dns_a_record" "m2m_records" {
  for_each = var.m2m_hostnames

  name                = split(".", each.value)[0]
  zone_name          = "m2m.fitfile.internal"
  resource_group_name = var.resource_group_name
  ttl                = 300
  records            = [var.cluster_internal_ip]
}
```

## Certificate Management Module

### Certificate Provisioning

```hcl
# modules/certificates/main.tf

# Public certificates via Let's Encrypt
resource "kubectl_manifest" "public_certificates" {
  for_each = toset(var.public_certificates)

  yaml_body = yamlencode({
    apiVersion = "cert-manager.io/v1"
    kind       = "Certificate"
    metadata = {
      name      = replace(each.value, ".", "-")
      namespace = var.namespace
    }
    spec = {
      secretName = "${replace(each.value, ".", "-")}-tls"
      issuerRef = {
        name = var.deployment_config.customer_domain != null ? "letsencrypt-http01" : "letsencrypt-dns01"
        kind = "ClusterIssuer"
      }
      dnsNames = [each.value]
    }
  })
}

# Private certificates via HCP Vault
resource "kubectl_manifest" "private_certificates" {
  for_each = toset(var.private_certificates)

  yaml_body = yamlencode({
    apiVersion = "cert-manager.io/v1"
    kind       = "Certificate"
    metadata = {
      name      = replace(each.value, ".", "-")
      namespace = var.namespace
    }
    spec = {
      secretName = "${replace(each.value, ".", "-")}-mtls"
      issuerRef = {
        name = "vault-issuer-${var.deployment_key}"
        kind = "Issuer"
      }
      dnsNames = [each.value]
      usages = [
        "digital signature",
        "key encipherment",
        "server auth",
        "client auth"
      ]
    }
  })
}

# Vault PKI Issuer for private certificates
resource "kubectl_manifest" "vault_issuer" {
  yaml_body = yamlencode({
    apiVersion = "cert-manager.io/v1"
    kind       = "Issuer"
    metadata = {
      name      = "vault-issuer-${var.deployment_key}"
      namespace = var.namespace
    }
    spec = {
      vault = {
        server = var.vault_server
        path   = "${var.vault_pki_path}/sign/${var.deployment_key}-role"
        auth = {
          appRole = {
            path   = "approle"
            roleId = var.vault_role_id
            secretRef = {
              name = "vault-approle-secret"
              key  = "secretId"
            }
          }
        }
      }
    }
  })
}
```

## Auth0 Configuration Module

### Auth0 Tenant Setup

```hcl
# modules/auth0/main.tf
resource "auth0_client" "application" {
  name        = "${var.customer_name} ${title(var.environment)}"
  description = "FITFILE application for ${var.customer_name}"
  app_type    = "spa"

  callbacks = var.callback_urls
  allowed_logout_urls = [
    for url in var.callback_urls : replace(url, "/callback", "/logout")
  ]

  web_origins = [
    for url in var.callback_urls : regex("https://[^/]+", url)
  ]

  jwt_configuration {
    alg = "RS256"
  }

  grant_types = [
    "authorization_code",
    "implicit",
    "refresh_token"
  ]
}

resource "auth0_resource_server" "api" {
  name       = "${var.customer_name} API"
  identifier = "https://${var.api_audience}"

  scopes {
    value       = "read:data"
    description = "Read access to patient data"
  }

  scopes {
    value       = "write:data"
    description = "Write access to patient data"
  }
}

# Output Auth0 configuration for Vault
output "auth0_secrets" {
  value = {
    client_id     = auth0_client.application.client_id
    client_secret = auth0_client.application.client_secret
    audience      = auth0_resource_server.api.identifier
    domain        = var.auth0_domain
  }
  sensitive = true
}
```

## Vault Secrets Module

### Secret Management

```hcl
# modules/vault-secrets/main.tf
resource "vault_generic_secret" "application_secrets" {
  path = "deployments/${var.deployment_key}/application"

  data_json = jsonencode({
    auth0_client_id     = var.auth0_config.client_id
    auth0_client_secret = var.auth0_config.client_secret
    auth0_audience      = var.auth0_config.audience
    auth0_domain        = var.auth0_config.domain

    # Database credentials
    mongodb_username = "root"
    mongodb_password = random_password.mongodb.result

    # S3/Storage credentials
    s3_access_key_id     = var.s3_credentials.access_key_id
    s3_secret_access_key = var.s3_credentials.secret_access_key

    # Generated UDE key
    ude_key = var.ude_key
  })
}

resource "vault_generic_secret" "spicedb_secrets" {
  path = "deployments/${var.deployment_key}/spicedb"

  data_json = jsonencode({
    postgresql_username    = "postgres"
    postgresql_password   = random_password.spicedb_postgres.result
    spicedb_preshared_key = random_password.spicedb_psk.result
  })
}

# Generate secure random passwords
resource "random_password" "mongodb" {
  length  = 32
  special = true
}

resource "random_password" "spicedb_postgres" {
  length  = 32
  special = true
}

resource "random_password" "spicedb_psk" {
  length  = 64
  special = false
}
```

## Main Module Orchestration

### Complete Implementation

```hcl
# main.tf
module "dns_records" {
  source = "./modules/dns-records"

  deployment_key           = var.deployment_config.deployment_key
  public_hostnames        = local.user_hostnames
  private_hostnames       = local.user_hostnames
  m2m_hostnames          = local.m2m_hostnames

  # DNS Provider Configuration
  cloudflare_enabled     = var.dns_providers.cloudflare != null
  cloudflare_zone_id     = try(var.dns_providers.cloudflare.zone_id, null)

  azure_private_dns_enabled = var.dns_providers.azure_private_dns != null
  resource_group_name       = try(var.dns_providers.azure_private_dns.resource_group_name, null)

  # Load balancer IPs (from infrastructure module)
  load_balancer_ip         = var.load_balancer_ip
  private_load_balancer_ip = var.private_load_balancer_ip
  cluster_internal_ip      = var.cluster_internal_ip
}

module "certificates" {
  source = "./modules/certificates"
  depends_on = [module.dns_records]

  deployment_key      = var.deployment_config.deployment_key
  public_certificates = local.public_certificates
  private_certificates = local.private_certificates

  namespace           = var.certificate_config.cert_manager_namespace
  vault_server        = var.vault_server
  vault_pki_path      = var.certificate_config.vault_pki_path
  vault_role_id       = var.vault_role_id
}

module "auth0" {
  source = "./modules/auth0"

  customer_name    = var.deployment_config.customer_name
  environment      = var.deployment_config.environment
  callback_urls    = local.auth0_callback_urls
  api_audience     = local.auth0_audience
  auth0_domain     = var.auth0_config.domain
}

module "vault_secrets" {
  source = "./modules/vault-secrets"
  depends_on = [module.auth0]

  deployment_key = var.deployment_config.deployment_key
  auth0_config   = module.auth0.auth0_secrets
  s3_credentials = var.s3_credentials
  ude_key        = var.ude_key
}
```

## Usage Examples

### Private Deployment Example

```hcl
# examples/private-deployment/main.tf
module "dns_automation" {
  source = "../../"

  deployment_config = {
    deployment_key   = "cuh-prod-1"
    customer_name    = "Cambridge University Hospitals"
    environment      = "prod"
    customer_domain  = null  # Use privatelink.fitfile.net
    is_private       = true
    azure_region     = "uksouth"
    enabled_services = ["app", "argocd", "workflows"]
    auth0_environment = "prod"
    use_private_ca   = true
  }

  dns_providers = {
    azure_private_dns = {
      resource_group_name = "rg-cuh-prod-dns"
      subscription_id     = "12345678-1234-1234-1234-123456789012"
    }
  }

  certificate_config = {
    acme_email = "devops@fitfile.net"
  }

  auth0_config = {
    domain        = "fitfile-prod.eu.auth0.com"
    client_id     = var.auth0_client_id
    client_secret = var.auth0_client_secret
  }
}
```

### Customer Domain Example

```hcl
# examples/customer-domain/main.tf
module "dns_automation" {
  source = "../../"

  deployment_config = {
    deployment_key   = "barts-prod-1"
    customer_name    = "Barts Health NHS Trust"
    environment      = "prod"
    customer_domain  = "fitfile.bartshealth.nhs.uk"  # Customer provides domain
    is_private       = true
    azure_region     = "uksouth"
    enabled_services = ["app", "argocd", "workflows"]
    auth0_environment = "prod"
    use_private_ca   = true
  }

  # Customer manages DNS, we only handle certificates
  dns_providers = {}

  certificate_config = {
    acme_email = "devops@fitfile.net"
  }
}
```

## Output Structure

### Generated Outputs

```hcl
# outputs.tf
output "deployment_hostnames" {
  description = "All generated hostnames for the deployment"
  value = {
    user_access = local.user_hostnames
    m2m_internal = local.m2m_hostnames
    nhs_services = local.nhs_hostnames
  }
}

output "certificate_secrets" {
  description = "Kubernetes secret names for certificates"
  value = {
    public_certs = [
      for cert in local.public_certificates : "${replace(cert, ".", "-")}-tls"
    ]
    private_certs = [
      for cert in local.private_certificates : "${replace(cert, ".", "-")}-mtls"
    ]
  }
}

output "auth0_configuration" {
  description = "Auth0 tenant configuration"
  value = {
    client_id = module.auth0.auth0_secrets.client_id
    audience  = module.auth0.auth0_secrets.audience
    domain    = module.auth0.auth0_secrets.domain
  }
  sensitive = true
}

output "dns_records_created" {
  description = "Summary of DNS records created"
  value = {
    cloudflare_records = keys(module.dns_records.cloudflare_records)
    azure_private_records = keys(module.dns_records.azure_private_records)
    m2m_records = keys(module.dns_records.m2m_records)
  }
}

output "vault_secret_paths" {
  description = "Vault secret paths for the deployment"
  value = {
    application = "deployments/${var.deployment_config.deployment_key}/application"
    spicedb     = "deployments/${var.deployment_config.deployment_key}/spicedb"
    monitoring  = "deployments/${var.deployment_config.deployment_key}/monitoring"
  }
}
```

This Terraform architecture provides complete automation for DNS, hostname, certificate, and Auth0 configuration based on minimal input parameters, ensuring consistency across all FITFILE deployments while accommodating customer-specific requirements.
