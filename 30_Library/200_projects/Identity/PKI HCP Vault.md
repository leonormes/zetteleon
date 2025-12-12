---
aliases: []
confidence: 
created: 2025-08-18T03:35:24Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:25Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: PKI HCP Vault
type:
uid: 
updated: 
version:
---

To create a root CA for Fitfile that can be used across different customer deployments and ensure that specific customers trust your certificates, you need to follow a structured approach using HashiCorp Vault and cert-manager. Here's a detailed guide on how to achieve this:

## 1. Setting Up the Root CA in HCP Vault

### **Root CA Configuration:**

- **Common Name (CN):** Use a generic name like "FITFILE Root CA".
- **Organization (O):** Set to "FITFILE".
- **Country (C), Province (ST), Locality (L):** Use "GB", "London", "London" respectively.
- **TTL:** Set to 10 years (87600 hours).
- **Allowed Domains:** Use broad domains like `*.fitfile.net` or `*`.
- **Usage:** The Root CA should only be used to sign the Intermediate CA.

### **Terraform Configuration:**

- Use Terraform to configure the Vault PKI. You can refer to the [Vault PKI Configuration](https://www.vaultproject.io/docs/secrets/pki) for detailed steps.
- Ensure the Root CA is configured to be long-lived and offline-style, only used for signing the Intermediate CA.

## 2. Creating a Certificate for CUH Private Network Deployment

### **Intermediate CA Configuration:**

- **Common Name (CN):** Use a specific name like "CUH Intermediate CA".
- **TTL:** Set to 3 years.
- **Allowed Domains:** Restrict to domains used by the CUH deployment, e.g., `*.cuh.fitfile.com`.
- **Usage:** Used by cert-manager to issue certificates for workloads in the CUH VPC/Kubernetes cluster.

### **Certificate Issuance:**

- Use cert-manager to automate the issuance of certificates within Kubernetes.
- Configure cert-manager to use the Intermediate CA for signing certificates.
- Ensure the Intermediate CA is configured with appropriate constraints for server authentication.

## 3. Ensuring Browser Trust for CUH Deployment

- **Install the Root CA Certificate:** The public part of the Root CA should be installed in the trust store of the VDI golden image used by CUH. This ensures that browsers on these VDIs trust the certificates issued by your Intermediate CA.
- **Wildcard Certificates:** Consider using wildcard certificates to secure the primary domain and all its subdomains.

## 4. Setting Up for SDE Deployment

### **Intermediate CA Configuration:**

- **Common Name (CN):** Use a specific name like "SDE Intermediate CA".
- **TTL:** Set to 3 years.
- **Allowed Domains:** Restrict to domains used by the SDE deployment, e.g., `*.sde.fitfile.com`.
- **Usage:** Similar to CUH, used by cert-manager for certificate issuance.

### **Certificate Issuance:**

- Follow the same process as the CUH deployment for certificate issuance using cert-manager.
- Ensure that the Intermediate CA for SDE is configured with the necessary constraints and domain restrictions.

## 5. Additional Considerations

- **Security Best Practices:** Ensure that the Root CA's private key is stored securely, possibly using Vault's HSM integration.
- **Certificate Rotation:** Implement a process for rotating the Intermediate CA and end-entity certificates before they expire.
- **Access Control:** Use least-privilege policies in Vault to control access to certificate signing operations.

By following these steps, you can establish a robust PKI infrastructure that supports multiple customer deployments while ensuring that your certificates are trusted by the necessary parties. If you need further assistance with the Terraform configuration or any specific setup, feel free to ask!

To transform your original request into a well-structured and detailed LLM (Large Language Model) prompt, we need to ensure clarity, context, and specific instructions. Here's a suggested format:

---

**Prompt Title:** Creating a Root CA and Intermediate CA for FITFILE Deployments

**Objective:**
Guide the user through the process of setting up a Root Certificate Authority (CA) and Intermediate CA using HashiCorp Vault for FITFILE deployments, ensuring browser trust for specific customer networks.

**Context:**
You are tasked with establishing a Public Key Infrastructure (PKI) for FITFILE that can be used across different customer deployments. The goal is to create a Root CA that is trusted by specific customers and to issue certificates for deployments such as CUH and SDE, ensuring that browsers trust these certificates.

**Instructions:**

1. **Root CA Setup:**
   - Define the Root CA with the following attributes:
     - Common Name (CN): "FITFILE Root CA"
     - Organization (O): "FITFILE"
     - Country (C): "GB"
     - Province (ST): "London"
     - Locality (L): "London"
     - TTL: 10 years
     - Usage: Only to sign the Intermediate CA

2. **Intermediate CA Configuration:**
   - For CUH Deployment:
     - Common Name (CN): "CUH Intermediate CA"
     - TTL: 3 years
     - Allowed Domains: "\*.cuh.fitfile.com"
     - Usage: Issue certificates for workloads in the CUH VPC/Kubernetes cluster
   - For SDE Deployment:
     - Common Name (CN): "SDE Intermediate CA"
     - TTL: 3 years
     - Allowed Domains: "\*.sde.fitfile.com"
     - Usage: Issue certificates for workloads in the SDE VPC/Kubernetes cluster

3. **Certificate Issuance:**
   - Use cert-manager to automate certificate issuance within Kubernetes.
   - Ensure the Intermediate CA is configured with appropriate constraints for server authentication.

4. **Browser Trust:**
   - Install the Root CA certificate in the trust store of the VDI golden image used by customers.
   - Consider using wildcard certificates to secure the primary domain and all its subdomains.

5. **Security Best Practices:**
   - Store the Root CA's private key securely, possibly using Vault's HSM integration.
   - Implement a process for rotating the Intermediate CA and end-entity certificates before they expire.
   - Use least-privilege policies in Vault to control access to certificate signing operations.

**Expected Outcome:**
A robust PKI infrastructure that supports multiple customer deployments, ensuring that certificates are trusted by the necessary parties.

---

## **Prerequisites**

- **Terraform CLI**: Installed and in your system's PATH.
- **Vault Provider for Terraform**: Configured with a token that has sufficient permissions to manage PKI backends. Set the `VAULT_ADDR` and `VAULT_TOKEN` environment variables.

---

## **Terraform Configuration**

It is best practice to separate your configuration into logical files.

### **`variables.tf`**

Define variables to make your configuration reusable.

```json
variable "vault_addr" {
  type        = string
  description = "The address of the Vault server."
  default     = "http://127.0.0.1:8200" # Or get from an environment variable
}

variable "root_ca_ttl" {
  type        = string
  description = "TTL for the Root CA. 10 years."
  default     = "315360000s"
}

variable "intermediate_ca_ttl" {
  type        = string
  description = "TTL for Intermediate CAs. 3 years."
  default     = "94608000s"
}
```

### **`main.tf`**

This file contains the core resources for creating the CAs and roles.

```hcp
################################################################################
# 1. ROOT CA SETUP
################################################################################

# Enable the PKI secrets engine for the Root CA
resource "vault_mount" "root" {
  path                      = "pki_root"
  type                      = "pki"
  description               = "FITFILE Root CA"
  max_lease_ttl_seconds     = var.root_ca_ttl
}

# Generate the self-signed Root CA Certificate
resource "vault_pki_secret_backend_root_cert" "root" {
  backend      = vault_mount.root.path
  type         = "internal"
  common_name  = "FITFILE Root CA"
  organization = "FITFILE"
  country      = "GB"
  province     = "London"
  locality     = "London"
  ttl          = var.root_ca_ttl
  key_type     = "rsa"
  key_bits     = 4096
}

# Configure the CRL and AIA URLs for the Root CA
resource "vault_pki_secret_backend_config_urls" "root" {
  backend = vault_mount.root.path
  issuing_certificates = [
    "${var.vault_addr}/v1/${vault_mount.root.path}/ca"
  ]
  crl_distribution_points = [
    "${var.vault_addr}/v1/${vault_mount.root.path}/crl"
  ]
}

################################################################################
# 2. INTERMEDIATE CA SETUP (CUH Deployment)
################################################################################

# Enable the PKI secrets engine for the CUH Intermediate CA
resource "vault_mount" "intermediate_cuh" {
  path                  = "pki_int_cuh"
  type                  = "pki"
  description           = "CUH Intermediate CA for fitfile.com"
  max_lease_ttl_seconds = var.intermediate_ca_ttl
}

# Generate a CSR for the CUH Intermediate CA
resource "vault_pki_secret_backend_intermediate_cert_request" "cuh" {
  backend     = vault_mount.intermediate_cuh.path
  type        = "internal"
  common_name = "CUH Intermediate CA"
}

# Sign the CUH intermediate CSR with the Root CA
resource "vault_pki_secret_backend_root_sign_intermediate" "cuh" {
  backend      = vault_mount.root.path
  csr          = vault_pki_secret_backend_intermediate_cert_request.cuh.csr
  common_name  = "CUH Intermediate CA"
  ttl          = var.intermediate_ca_ttl
  revoke       = true
}

# Import the signed certificate into the CUH Intermediate CA engine
resource "vault_pki_secret_backend_intermediate_set_signed" "cuh" {
  backend     = vault_mount.intermediate_cuh.path
  certificate = vault_pki_secret_backend_root_sign_intermediate.cuh.certificate
}

################################################################################
# 3. INTERMEDIATE CA SETUP (SDE Deployment) - Repeat the process
################################################################################

resource "vault_mount" "intermediate_sde" {
  path                  = "pki_int_sde"
  type                  = "pki"
  description           = "SDE Intermediate CA for fitfile.com"
  max_lease_ttl_seconds = var.intermediate_ca_ttl
}

resource "vault_pki_secret_backend_intermediate_cert_request" "sde" {
  backend     = vault_mount.intermediate_sde.path
  type        = "internal"
  common_name = "SDE Intermediate CA"
}

resource "vault_pki_secret_backend_root_sign_intermediate" "sde" {
  backend      = vault_mount.root.path
  csr          = vault_pki_secret_backend_intermediate_cert_request.sde.csr
  common_name  = "SDE Intermediate CA"
  ttl          = var.intermediate_ca_ttl
  revoke       = true
}

resource "vault_pki_secret_backend_intermediate_set_signed" "sde" {
  backend     = vault_mount.intermediate_sde.path
  certificate = vault_pki_secret_backend_root_sign_intermediate.sde.certificate
}

################################################################################
# 4. ROLE CONFIGURATION FOR CERTIFICATE ISSUANCE
################################################################################

# Create a role for issuing certificates for the CUH deployment
resource "vault_pki_secret_backend_role" "cuh_server" {
  backend                     = vault_mount.intermediate_cuh.path
  name                        = "cuh-server"
  allowed_domains             = ["cuh.fitfile.com"]
  allow_subdomains            = true
  allow_wildcard_certificates = true
  key_type                    = "rsa"
  key_bits                    = 2048
  key_usage = [
    "DigitalSignature",
    "KeyEncipherment",
    "ServerAuth",
  ]
  ttl = "2160h" # 90 days
}

# Create a role for issuing certificates for the SDE deployment
resource "vault_pki_secret_backend_role" "sde_server" {
  backend                     = vault_mount.intermediate_sde.path
  name                        = "sde-server"
  allowed_domains             = ["sde.fitfile.com"]
  allow_subdomains            = true
  allow_wildcard_certificates = true
  key_type                    = "rsa"
  key_bits                    = 2048
  key_usage = [
    "DigitalSignature",
    "KeyEncipherment",
    "ServerAuth",
  ]
  ttl = "2160h" # 90 days
}
```

### **`outputs.tf`**

This file defines what information to display after Terraform applies the configuration. This is crucial for retrieving the public root certificate.

```hcp
output "fitfile_root_ca_public_cert" {
  description = "The public certificate for the FITFILE Root CA. Install this in client trust stores."
  value       = vault_pki_secret_backend_root_cert.root.certificate
  sensitive   = true # Mark as sensitive to prevent showing in CLI output by default
}

output "cuh_intermediate_ca_public_cert" {
  description = "The public certificate for the CUH Intermediate CA."
  value       = vault_pki_secret_backend_root_sign_intermediate.cuh.certificate
  sensitive   = true
}

output "sde_intermediate_ca_public_cert" {
  description = "The public certificate for the SDE Intermediate CA."
  value       = vault_pki_secret_backend_root_sign_intermediate.sde.certificate
  sensitive   = true
}
```

---

## **Execution And Usage**

### **Step 1: Apply the Terraform Configuration**

### **Step 2: Retrieve the Root Certificate**

After the apply is complete, retrieve the root CA's public certificate from the Terraform output. This is the certificate you will distribute to establish browser trust.

Bash

```sh
# Save the root CA public key to a file
terraform output -raw fitfile_root_ca_public_cert > fitfile_root_ca.crt
```

### **Step 3: Establish Browser Trust**

Use the generated `fitfile_root_ca.crt` file to install the Root CA in the trust store of your VDI golden image, typically via Group Policy (GPO) as described in the previous guide.

### **Step 4: Configure `cert-manager`**

Your Vault infrastructure is now ready. The Terraform code has created the PKI backends and roles. You can now point `cert-manager` to these roles. The `VaultIssuer` and `Certificate` YAML manifests for Kubernetes remain the same as in the previous guide; you are simply automating the backend setup with Terraform.

For example, your `VaultIssuer` for CUH would reference the path `pki_int_cuh/sign/cuh-server`, which was created by the `vault_pki_secret_backend_role.cuh_server` resource.

Perfect! Now that your PKI is working, I'll show you how to issue a certificate for your private application and configure it properly.

---

---

[[2025-08-21]]

## **Step 1: Issue a Certificate for Your Application**

First, let's issue a certificate. You'll need to know which deployment this application belongs to. Let's say it's for the `testing` deployment and your app runs on `myapp.testing.fitfile.net`:

```bash
# Issue a certificate using the Vault CLI
vault write -namespace=central pki_int_testing/issue/testing-server \
    common_name="myapp.testing.fitfile.net" \
    ttl="2160h"
```

Or using the API:

```bash
curl -X POST \
    -H "X-Vault-Token: $VAULT_TOKEN" \
    -H "X-Vault-Namespace: central" \
    -d '{"common_name": "myapp.testing.fitfile.net", "ttl": "2160h"}' \
    https://vault.fitfile.co.uk/v1/pki_int_testing/issue/testing-server
```

This will return:

- `certificate` - Your server certificate
- `private_key` - Private key for your server
- `ca_chain` - The certificate chain (intermediate + root CA)

## **Step 2: Get the Root CA Certificate for Browsers**

Users need to install your Root CA certificate in their browsers to trust your certificates. Here's how to get it:

```bash
# Get the Root CA certificate
vault read -namespace=central -field=certificate pki_root/cert/ca > fitfile-root-ca.crt
```

Or via API:

```bash
curl -H "X-Vault-Token: $VAULT_TOKEN" \
     -H "X-Vault-Namespace: central" \
     https://vault.fitfile.co.uk/v1/pki_root/cert/ca > fitfile-root-ca.crt
```

## **Step 3: Install Root CA in Browsers**

**Windows:**

1. Double-click `fitfile-root-ca.crt`
2. Click "Install Certificate"
3. Choose "Local Machine" → "Trusted Root Certification Authorities"

**macOS:**

1. Double-click `fitfile-root-ca.crt`
2. Add to "System" keychain
3. Set trust to "Always Trust"

**Linux/Chrome:**

1. Chrome Settings → Privacy and Security → Security → Manage Certificates
2. Authorities tab → Import → Select `fitfile-root-ca.crt`

## **Step 4: Configure Your Server**

Save the certificate files on your server and configure your web server. Here are examples for common servers:

**Apache:**

```apache
<VirtualHost *:443>
    ServerName myapp.testing.fitfile.net
    SSLEngine on
    SSLCertificateFile /path/to/server.crt
    SSLCertificateKeyFile /path/to/server.key
    SSLCertificateChainFile /path/to/ca_chain.crt
</VirtualHost>
```

**Nginx:**

```nginx
server {
    listen 443 ssl;
    server_name myapp.testing.fitfile.net;

    ssl_certificate /path/to/server.crt;
    ssl_certificate_key /path/to/server.key;
    ssl_trusted_certificate /path/to/ca_chain.crt;
}
```

**Docker/Node.js:**

```javascript
const https = require("https")
const fs = require("fs")

const options = {
  key: fs.readFileSync("/path/to/server.key"),
  cert: fs.readFileSync("/path/to/server.crt"),
  ca: fs.readFileSync("/path/to/ca_chain.crt")
}

https.createServer(options, app).listen(443)
```

## **Complete PKI Certificate Workflow**

### **Quick Commands for Your Use Case:**

**1. Issue Certificate:**

```bash
vault write -namespace=central pki_int_testing/issue/testing-server \
    common_name="myapp.testing.fitfile.net" \
    ttl="2160h" \
    -format=json > cert_response.json
```

**2. Extract Certificate Files:**

```bash
# Server certificate
jq -r '.data.certificate' cert_response.json > server.crt

# Private key
jq -r '.data.private_key' cert_response.json > server.key

# CA chain (for server config)
jq -r '.data.ca_chain[]' cert_response.json > ca_chain.crt

# Root CA (for browser installation)
vault read -namespace=central -field=certificate pki_root/cert/ca > fitfile-root-ca.crt
```

**3. Server Configuration Example (Nginx):**

```nginx
server {
    listen 443 ssl;
    server_name myapp.testing.fitfile.net;

    ssl_certificate /etc/ssl/certs/server.crt;
    ssl_certificate_key /etc/ssl/private/server.key;
    ssl_trusted_certificate /etc/ssl/certs/ca_chain.crt;

    # Your app configuration
    location / {
        proxy_pass http://localhost:8080;
    }
}
```

### **Distribution Process:**

1. **Deploy certificates** to your server using the files above
2. **Distribute `fitfile-root-ca.crt`** to all VDI users
3. **Users install** the root CA in their browsers
4. **Access** `https://myapp.testing.fitfile.net` - no security warnings!

### **Certificate Renewal:**

Certificates expire in 90 days. Set up a cron job to renew them automatically using the same `vault write` command.

Your PKI is now fully operational for eliminating browser security warnings on private applications!
