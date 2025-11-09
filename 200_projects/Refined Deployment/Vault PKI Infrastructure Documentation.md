---
aliases: []
confidence: 
created: 2025-09-02T12:53:56Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T14:24:13Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [documentation, infrastructure, security]
title: Vault PKI Infrastructure Documentation
type:
uid: 
updated: 
version:
---

## Overview

This document describes the Public Key Infrastructure (PKI) setup in HashiCorp Vault managed through Terraform. Our PKI system provides certificate management capabilities for internal services and applications.

## Architecture

### PKI Hierarchy

Our PKI implementation follows a two-tier certificate authority structure:

1. **Root Certificate Authority** - Stored in the `pki` mount
2. **Intermediate Certificate Authority** - Stored in the `pki_int` mount

### Namespace Structure

The PKI infrastructure is deployed within Vault's namespace hierarchy:

- Root namespace: `admin`
- Central namespace: Contains the PKI mounts and configuration
- Deployment namespaces: Individual namespaces for each deployment environment

## Terraform Resources

### Root Certificate Authority

The root CA is configured in the main PKI mount:

```hcl
resource "vault_mount" "pki" {
    namespace = vault_namespace.central_ns.path_fq
    path = "pki"
    type = "pki"
}

resource "vault_pki_secret_backend_root_cert" "root" {
    backend = vault_mount.pki.path
    type = "internal"
    common_name = "example.com Root CA"
    ttl = "87600h"  # 10 years
}
```

The root certificate is also exported to a local file for distribution:

```hcl
resource "local_file" "root_ca_cert" {
    content = vault_pki_secret_backend_root_cert.root.certificate
    filename = "${path.module}/root_ca.cert"
}
```

### Intermediate Certificate Authority

The intermediate CA handles the actual certificate issuance:

```hcl
resource "vault_mount" "pki_int" {
    path = "pki_int"
    type = "pki"
    max_lease_ttl_seconds = 43800 * 60  # 30 days
}

resource "vault_pki_secret_backend_intermediate_cert_request" "int" {
    backend = vault_mount.pki_int.path
    type = "internal"
    common_name = "example.com Intermediate CA"
}
```

### PKI URLs Configuration

Distribution points for certificates and CRLs are configured:

```hcl
resource "vault_pki_secret_backend_config_urls" "urls" {
    backend = vault_mount.pki.path
    issuing_certificates = ["${var.vault_addr}/v1/pki/ca"]
    crl_distribution_points = ["${var.vault_addr}/v1/pki/crl"]
}
```

### Certificate Roles

Roles define the certificate issuance policies. Based on the [secret_engines.tf](file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/helm_chart_deployment/central-services/secret_engines.tf), we create deployment-specific server certificate roles:

```hcl
resource "vault_pki_secret_backend_role" "deployment_server" {
    for_each = local.deployments
    namespace = vault_namespace.deployments[each.key].path_fq
    backend = vault_mount.pki_intermediate[each.key].path
    name = "${each.key}-server"
    allowed_domains = ["${each.key}.example.com"]
    allow_subdomains = true
    allow_wildcard_certificates = true
    key_type = "rsa"
    key_bits = 2048
    key_usage = [
        "DigitalSignature",
        "KeyEncipherment",
        "ServerAuth"
    ]
    ttl = "2160h"  # 90 days
}
```

## Setup Instructions

### Prerequisites

1. **HCP Vault Access**: Root token from HCP portal
2. **Terraform**: Version compatible with the hashicorp/vault provider
3. **Namespace Permissions**: Admin namespace access

### Initial Configuration

1. **Enable Cross-Namespace Secret Sharing**:
   - Login to Vault with root token from HCP portal
   - Switch to the admin namespace
   - Navigate to Tools → API Explorer
   - Search for `group_policy_application`
   - Send an API request with:

     ```json
     {
       "group_policy_application_mode": "any"
     }
     ```

2. **Configure Vault JWT Auth for Terraform Cloud** (as documented in [README.md](file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/helm_chart_deployment/central-services/README.md)):
   - Login to Vault with root token
   - Switch to admin namespace
   - Go to Access → Authentication Methods
   - Enable JWT auth method with mount path (e.g., `tfc-terraform`)
   - Configure the auth method to trust `app.terraform.io`

### Deployment Configuration

To add a new deployment environment, update the `locals.tf` file:

```hcl
locals {
    deployments = {
        "dev" = {
            secrets = tomap({
                "service-secrets" = {},
                "spicedb-secrets" = {},
            })
            auto_create = true
        },
        "prod" = {
            # Production configuration
        }
    }
}
```

### Terraform Workspace Variables

Configure the following environment variables in your Terraform Cloud workspace:

```bash
TFC_VAULT_ADDR=<address-of-vault-cluster>
TFC_VAULT_PROVIDER_AUTH=true
TFC_VAULT_AUTH_PATH=<your-jwt-auth-mount>
TFC_VAULT_NAMESPACE=admin
TFC_VAULT_RUN_ROLE=tfc-role
```

## Certificate Management

### Requesting Certificates

Applications can request certificates using the configured roles:

```bash
vault write pki_int/issue/<deployment>-server \
    common_name=service.<deployment>.example.com \
    ttl=720h
```

### Certificate Specifications

- **Key Type**: RSA 2048-bit
- **Validity Period**: 90 days (configurable)
- **Allowed Domains**: `<deployment>.example.com` and subdomains
- **Wildcard Support**: Enabled
- **Key Usage**: Digital Signature, Key Encipherment, Server Authentication

## Security Considerations

1. **Root CA Protection**: The root CA private key is generated and stored within Vault's secure storage
2. **Namespace Isolation**: Each deployment has its own namespace with isolated PKI infrastructure
3. **Certificate Lifetime**: Short-lived certificates (90 days) reduce exposure from compromised certificates
4. **Audit Logging**: All certificate operations are logged in Vault's audit log

## Monitoring and Maintenance

### Certificate Expiration

Monitor certificate expiration using Vault's API:

```bash
vault list pki_int/certs
```

### CRL Management

Certificate Revocation Lists are automatically managed by Vault and accessible at the configured distribution points.

### Backup Considerations

- Root CA certificate should be backed up securely
- Intermediate CA can be regenerated if needed
- Regular backups of Vault's storage backend are critical

## Troubleshooting

### Common Issues

1. **Permission Denied**: Ensure proper namespace access and policy attachments
2. **Certificate Request Failed**: Verify the requested domain matches the role's allowed_domains
3. **JWT Auth Issues**: Check TFC workspace variables and auth method configuration

### Useful Commands

```bash
# Check PKI mount status
vault secrets list -namespace=<namespace>

# View certificate role configuration
vault read pki_int/roles/<role-name>

# List issued certificates
vault list pki_int/certs
```

## Related Documentation

- [HashiCorp Vault PKI Secrets Engine](https://www.vaultproject.io/docs/secrets/pki)
- [Terraform Vault Provider](https://registry.terraform.io/providers/hashicorp/vault/latest/docs)
- Internal Terraform modules in [TFC-Modules](file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/TFC-Modules)

---

### 1. **Vault PKI Configuration**

From your [pki.tf](file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/helm_chart_deployment/central-services/vault/pki.tf) and [outputs_pki.tf](file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/helm_chart_deployment/central-services/vault/outputs_pki.tf), the PKI infrastructure includes:

- **Root CA**: Mounted at `pki` path
- **Intermediate CA**: Mounted at `pki_int` path
- **Certificate Role**: A specific role for cert-manager to request certificates
- **Kubernetes Auth**: Authentication method for cert-manager service account

### 2. **cert-manager Integration**

According to your [PKI Params](https://obsidian.md) notes from **August 6, 2025**, you create a ClusterIssuer that tells cert-manager how to communicate with Vault:

```yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: hcp-vault-issuer
spec:
  vault:
    server: "https://your-vault-cluster.private.vault.cloud:8200"
    path: "kubernetes_eks_prod"
    caBundle: <base64 encoded CA bundle>
    auth:
      kubernetes:
        role: "cert-manager"
        mountPath: "/v1/auth/kubernetes"
        serviceAccountRef:
          name: "cert-manager"
```

### 3. **Requesting Certificates**

Applications can request certificates by creating a Certificate resource:

```yaml
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: fitfile-net-wildcard-tls
  namespace: your-app-namespace
spec:
  secretName: fitfile-net-wildcard-tls-secret
  dnsNames:
    - "*.fitfile.net"
    - "fitfile.net"
  issuerRef:
    name: hcp-vault-issuer
    kind: ClusterIssuer
```

### 4. **Using Certificates in Ingress**

The certificates are automatically stored as Kubernetes secrets and can be used in Ingress resources:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: frontend-ingress
  namespace: your-app-namespace
spec:
  tls:
    - hosts:
        - "app.fitfile.net"
      secretName: frontend-tls-secret
  rules:
    - host: "app.fitfile.net"
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: your-frontend-service
                port:
                  number: 80
```

## Key Benefits

1. **Automatic Certificate Management**: cert-manager handles certificate issuance, renewal, and rotation automatically
2. **Wildcard Support**: Your Vault configuration supports wildcard certificates (enabled by `allow_glob_domains = true`)
3. **Short-Lived Certificates**: 90-day validity reduces security exposure
4. **Namespace Isolation**: Each deployment can have its own PKI infrastructure in separate Vault namespaces

## Implementation Steps

Based on your [Configure the Certificate Authority](https://obsidian.md) documentation from **August 4, 2025**:

1. **Extract CA Bundle** from Vault:

```bash
vault read -field=issuing_ca pki_int/cert/ca > fitfile-ca-bundle.pem
```

2. **Install cert-manager** in your Kubernetes cluster (if not already installed)
3. **Create the ClusterIssuer** using the manifest above
4. **Verify** the issuer is ready:

```bash
kubectl describe clusterissuer hcp-vault-issuer
```

5. **Create Certificate resources** for your applications

## Important Considerations

- The Vault server must be accessible from your Kubernetes cluster
- cert-manager's service account needs proper Vault authentication configured
- The CA bundle must be trusted by clients (VDI golden images in your case)
- Monitor certificate expiration and ensure cert-manager can renew them
