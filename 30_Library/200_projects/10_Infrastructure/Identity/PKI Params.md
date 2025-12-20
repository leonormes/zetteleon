---
aliases: []
confidence: 
created: 2025-08-04T11:42:52Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:25Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [pki]
title: PKI Params
type:
uid: 
updated: 
version:
---

## 1. **Review Of Current Naming and Structure**

From your files, you are following a standard two-tier PKI model:

- **Root CA**: Long-lived, only used to sign the Intermediate CA.
- **Intermediate CA**: Shorter-lived, used for day-to-day certificate issuance (e.g., by cert-manager in Kubernetes). Your [README_PKI.md](file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/Clusters/FITFILE/Production/central-services/hcp/vault/README_PKI.md) describes this well, and the variable names (`pki_root`, `pki_int`) are conventional and clear.

### **Naming Recommendations**

- **Root CA**: Should be generic and organization-wide, e.g., `FITFILE Root CA`.
- **Intermediate CA**: Should be environmentor deployment-specific, e.g., `EOE SDE Intermediate CA` or `eoe-sde-codisc Intermediate CA`. This helps distinguish between the global trust anchor (root) and the environment-specific intermediate.

## 2. **Details For Root CA and Intermediate CA**

### **Root CA**

- **Common Name (CN)**: `FITFILE Root CA`
- **Organization (O)**: `FITFILE`
- **Country (C)**: `GB`
- **Province (ST)**: `London`
- **Locality (L)**: `London`
- **TTL**: 10 years (as per your docs)
- **Allowed Domains**: Should be broad, e.g., `fitfile.co.uk`, `*.fitfile.co.uk`
- **Usage**: Only to sign the Intermediate CA

### **Intermediate CA**

- **Common Name (CN)**: `EOE SDE Intermediate CA` or `eoe-sde-codisc Intermediate CA`
- **Organization (O)**: `FITFILE`
- **Country (C)**: `GB`
- **Province (ST)**: `London`
- **Locality (L)**: `London`
- **TTL**: 3 years (as per your docs)
- **Allowed Domains**: Restrict to the domains/subdomains used by the eoe deployment, e.g., `eoe.fitfile.co.uk`, `*.eoe.fitfile.co.uk`, or whatever matches your internal DNS structure.
- **Usage**: Used by cert-manager to issue certificates for workloads in the eoe VPC/Kubernetes cluster.

### **End-Entity Certificates (Issued by Intermediate)**

- **CN**: Should match the service or workload, e.g., `myservice.eoe.fitfile.co.uk`
- **SANs**: Include all DNS names the service will use.
- **TTL**: 30 days (default, renewable by cert-manager)
- **Key Usage**: `digitalSignature`, `keyEncipherment`
- **Extended Key Usage**: `serverAuth`, `clientAuth` as needed

## 3. **Domain And Subdomain Guidance**

From your [config.tf](file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/Clusters/eoe/Production/test-sde-v2/config.tf), your VPC CIDR is `10.65.0.0/20` and your deployment is named `eoe-sde-codisc`. For private/internal PKI, you should:

- Use internal DNS names that match your VPC's naming conventions, e.g., `*.eoe-sde-codisc.internal.fitfile.co.uk` or `*.eoe.fitfile.co.uk`.
- Ensure the `allowed_domains` in Vault's PKI config matches these.

## 4. **Terraform Variable Suggestions**

In your Vault PKI Terraform, set variables like:

```hcl
organization      = "FITFILE"
root_common_name  = "FITFILE Root CA"
int_common_name   = "EOE SDE Intermediate CA"
domain            = "eoe.fitfile.co.uk"
allowed_domains   = ["eoe.fitfile.co.uk", "*.eoe.fitfile.co.uk"]
cert_country      = "GB"
cert_province     = "London"
cert_locality     = "London"
cert_ttl          = 720 # 30 days
```

If you want to restrict even further, use your internal DNS zone, e.g., `*.eoe-sde-codisc.internal.fitfile.co.uk`.

## 5. **Summary Table**

| CA Type         | Common Name                             | Allowed Domains                 | TTL                     | Usage                |
| :-------------- | :-------------------------------------- | :------------------------------ | :---------------------- | :------------------- |
| Root CA         | FITFILE Root CA                         | fitfile.co.uk, \*.fitfile.co.uk | 10 years                | Sign Intermediate CA |
| Intermediate CA | eoe.fitfile.co.uk, \*.eoe.fitfile.co.uk | 3 years                         | EOE SDE Intermediate CA | Issue leaf certs     |
| Leaf Certs      | (service DNS name)                      | (service DNS name)              | 30 days                 | Workload TLS         |

## 6. **Best Practices**

- **Root CA**: Never used directly for workloads. Store securely in Vault, consider HSM integration.
- **Intermediate CA**: Rotate every few years, revoke if compromised.
- **Leaf Certs**: Short TTL, automate renewal with cert-manager.
- **Naming**: Be explicit about environment and scope in Intermediate CA names.

## 7. **References**

- [Vault PKI Secrets Engine](https://www.vaultproject.io/docs/secrets/pki)
- [cert-manager Vault Issuer](https://cert-manager.io/docs/configuration/vault/)

## Plan Overview

This plan is divided into four distinct phases:

1. Phase 1: Configure the Certificate Authority (HCP Vault): We will establish a secure, two-tier CA hierarchy within your HCP Vault cluster using Terraform. This creates the root of trust for your entire private network.
2. Phase 2: Establish Client Trust (VDI Golden Image): We will install the public part of our new CA into the master VDI image. This is the crucial step that makes the browsers on the VDIs trust your internal certificates.
3. Phase 3: Integrate Kubernetes with the CA (`cert-manager`): We will configure `cert-manager` in your EKS cluster to communicate with Vault, enabling it to request and receive certificates automatically.
4. Phase 4: Deploy and Secure the Application: We will request a certificate for your frontend application and configure it to use the new, trusted TLS certificate.

---

## Phase 1: Configure the Certificate Authority (HCP Vault)

The foundation of our PKI is a two-tier CA structure. This is a security best practice where a highly-protected Root CA signs an Intermediate CA. The Intermediate CA is then used for the day-to-day operations of signing certificates for your applications. This keeps the Root CA's private key offline and secure.

We will manage this entire setup using the Terraform Vault provider.

### Terraform Configuration for Vault PKI

This code will set up the necessary PKI engines, roles, and authentication methods in your HCP Vault.

```hcp
# -------------------------------------------------------------------------
# VARIABLES
# -------------------------------------------------------------------------
variable "organization" {
  description = "Organisation name for certificates"
  type        = string
  default     = "FitFile Inc"
}

variable "pki_root_path" {
  description = "Path for the Root PKI Secrets Engine"
  type        = string
  default     = "pki_root_fitfile"
}

variable "pki_int_path" {
  description = "Path for the Intermediate PKI Secrets Engine"
  type        = string
  default     = "pki_int_fitfile"
}

variable "kubernetes_auth_path" {
  description = "Path for the Kubernetes authentication backend"
  type        = string
  default     = "kubernetes_eks_prod"
}

variable "allowed_domains" {
  description = "List of allowed domains for certificate issuance"
  type        = list(string)
  default     = ["fitfile.net"]
}

variable "kubernetes_host" {
  description = "Kubernetes API URL for the EKS cluster"
  type        = string
}

variable "kubernetes_ca_cert" {
  description = "PEM-encoded CA certificate for the Kubernetes API"
  type        = string
  sensitive   = true
}

variable "token_reviewer_jwt" {
  description = "A long-lived Kubernetes service account token that has permission to perform TokenReview"
  type        = string
  sensitive   = true
}

# -------------------------------------------------------------------------
# ROOT CA SETUP
# -------------------------------------------------------------------------
resource "vault_mount" "pki_root" {
  path        = var.pki_root_path
  type        = "pki"
  description = "FitFile Root CA PKI Engine"
  # 20 year max TTL for the root
  max_lease_ttl_seconds = 630720000
}

resource "vault_pki_secret_backend_root_cert" "root" {
  depends_on = [vault_mount.pki_root]

  backend     = vault_mount.pki_root.path
  type        = "internal"
  common_name = "FitFile Root CA"
  # 10 year TTL for the root certificate
  ttl         = "87600h"
  key_type    = "rsa"
  key_bits    = 4096
  organization = var.organization
}

# ------------------------------------------------------------------------
# INTERMEDIATE CA SETUP
# -------------------------------------------------------------------------
resource "vault_mount" "pki_int" {
  path        = var.pki_int_path
  type        = "pki"
  description = "FitFile Intermediate CA PKI Engine"
  # 5 year max TTL for the intermediate
  max_lease_ttl_seconds = 157680000
}

resource "vault_pki_secret_backend_intermediate_cert_request" "intermediate" {
  depends_on = [vault_mount.pki_int]

  backend     = vault_mount.pki_int.path
  type        = "internal"
  common_name = "FitFile Intermediate CA"
}

resource "vault_pki_secret_backend_root_sign_intermediate" "intermediate" {
  depends_on = [vault_pki_secret_backend_root_cert.root]

  backend     = vault_mount.pki_root.path
  csr         = vault_pki_secret_backend_intermediate_cert_request.intermediate.csr
  common_name = "FitFile Intermediate CA"
  # 3 year TTL for the intermediate certificate
  ttl         = "26280h"
  format      = "pem_bundle"
}

resource "vault_pki_secret_backend_intermediate_set_signed" "intermediate" {
  backend     = vault_mount.pki_int.path
  certificate = vault_pki_secret_backend_root_sign_intermediate.intermediate.certificate
}

# -------------------------------------------------------------------------
# CERT-MANAGER ROLE & POLICY
# -------------------------------------------------------------------------
resource "vault_pki_secret_backend_role" "cert_manager_role" {
  depends_on = [vault_pki_secret_backend_intermediate_set_signed.intermediate]

  backend          = vault_mount.pki_int.path
  name             = "cert-manager-role"
  allowed_domains  = var.allowed_domains
  allow_subdomains = true
  # 30 day TTL for leaf certificates
  max_ttl          = "720h"
}

resource "vault_policy" "cert_manager_policy" {
  name = "cert-manager-policy"

  policy = <<EOT
# Allow cert-manager to sign certificates using its role
path "${vault_mount.pki_int.path}/sign/${vault_pki_secret_backend_role.cert_manager_role.name}" {
  capabilities = ["create", "update"]
}
EOT
}

# -------------------------------------------------------------------------
# KUBERNETES AUTHENTICATION
# -------------------------------------------------------------------------
resource "vault_auth_backend" "kubernetes" {
  type = "kubernetes"
  path = var.kubernetes_auth_path
}

resource "vault_kubernetes_auth_backend_config" "config" {
  backend            = vault_auth_backend.kubernetes.path
  kubernetes_host    = var.kubernetes_host
  kubernetes_ca_cert = var.kubernetes_ca_cert
  token_reviewer_jwt = var.token_reviewer_jwt
}

resource "vault_kubernetes_auth_backend_role" "cert_manager_auth" {
  backend                          = vault_auth_backend.kubernetes.path
  role_name                        = "cert-manager"
  bound_service_account_names      = ["cert-manager"]
  bound_service_account_namespaces = ["cert-manager"]
  token_policies                   = [vault_policy.cert_manager_policy.name]
  token_ttl                        = 3600 # 1 hour
}
```

Key Deliverable: After applying this Terraform, you need to extract the public CA bundle. This is what you will install on the VDIs.

```bash
# Get the intermediate CA public certificate
vault read -field=issuing_ca ${vault_mount.pki_int.path}/cert/ca > intermediate_ca.pem
# Get the root CA public certificate
vault read -field=certificate ${vault_mount.pki_root.path}/cert/ca > root_ca.pem
# Combine them into a single bundle file
cat intermediate_ca.pem root_ca.pem > fitfile-ca-bundle.pem
```

Keep the `fitfile-ca-bundle.pem` file for the next phase.

---

## Phase 2: Establish Client Trust (VDI Golden Image)

This phase ensures that every user's VDI instance trusts your new internal CA. We will do this by updating the "golden image" from which all VDIs are provisioned.

1. Launch a Template VDI Instance: Start a single AWS WorkSpace that you use as a master image.
2. Install the CA Bundle:
   For a Windows Image: 1. Copy the `fitfile-ca-bundle.pem` file to the instance. 2. Open PowerShell as an Administrator and run:
   `powershell
Import-Certificate -FilePath "C:\path\to\your\fitfile-ca-bundle.pem" -CertStoreLocation "Cert:\LocalMachine\Root"
`
   For an Amazon Linux 2 Image: 3. Copy the `fitfile-ca-bundle.pem` file to the instance. 4. Run the following commands:
   `bash
sudo cp fitfile-ca-bundle.pem /etc/pki/ca-trust/source/anchors/
sudo update-ca-trust extract
`
3. Create the Golden Image: After installing the certificate (and any other updates), go to the AWS WorkSpaces console and create a new Custom Bundle from this instance.
4. Provision VDIs: Deploy new WorkSpaces for your users using this updated bundle.

---

## Phase 3: Integrate Kubernetes with the CA (`cert-manager`)

Now, we'll create a `ClusterIssuer` in EKS. This resource tells `cert-manager` how to communicate with your HCP Vault to get certificates.

1. Create the `ClusterIssuer` Manifest:

   ```yaml
   # hcp-vault-clusterissuer.yaml
   apiVersion: cert-manager.io/v1
   kind: ClusterIssuer
   metadata:
     name: hcp-vault-issuer
   spec:
     vault:
       # Your HCP Vault server address (ensure it's reachable from EKS)
       server: "https://your-vault-cluster.private.vault.cloud:8200"
       # The path where you enabled the Kubernetes auth method
       path: "kubernetes_eks_prod"
       # The Kubernetes auth role you created in Terraform
       role: "cert-manager"
       # The full path to the signing endpoint in the intermediate CA
       pkiPath: "pki_int_fitfile/sign/cert-manager-role"
   ```

2. Apply the Manifest:

   ```bash
   kubectl apply -f hcp-vault-clusterissuer.yaml
   ```

3. Verify the Issuer: Check that the issuer is ready and can connect to Vault.

   ```bash
   kubectl describe clusterissuer hcp-vault-issuer
   # Look for a condition with Type=Ready and Status=True
   ```

---

## Phase 4: Deploy and Secure the Application

The final step is to request a certificate for your frontend application and use it.

1. Create a `Certificate` Resource:
   This resource tells `cert-manager` to get a certificate for `frontend.fitfile.net` from your new `ClusterIssuer`.

   ```yaml
   # frontend-certificate.yaml
   apiVersion: cert-manager.io/v1
   kind: Certificate
   metadata:
     name: frontend-tls
     namespace: your-app-namespace # The namespace of your frontend app
   spec:
     secretName: frontend-tls-secret
     dnsNames:
       - frontend.fitfile.net
     issuerRef:
       name: hcp-vault-issuer
       kind: ClusterIssuer
   ```

   Apply it: `kubectl apply -f frontend-certificate.yaml`

2. Use the Certificate in Your Deployment/Ingress:
   `cert-manager` will create a secret named `frontend-tls-secret` in the `your-app-namespace`. You can now use this secret in your application's deployment or, more commonly, in your Ingress resource.

   Example Ingress:

   ```yaml
   apiVersion: networking.k8s.io/v1
   kind: Ingress
   metadata:
     name: frontend-ingress
     namespace: your-app-namespace
   spec:
     rules:
       - host: "frontend.fitfile.net"
         http:
           paths:
             - path: /
               pathType: Prefix
               backend:
                 service:
                   name: your-frontend-service
                   port:
                     number: 80
     tls:
       - hosts:
           - frontend.fitfile.net
         secretName: frontend-tls-secret # Use the secret created by cert-manager
   ```

## Final Verification

Once the application is running and the Ingress is configured, a user on a VDI provisioned from your new golden image can navigate to `https://frontend.fitfile.net`. Their browser will now show a secure connection with a valid padlock, as it trusts the certificate presented by the application because its entire chain of trust leads back to the Root CA you installed in the VDI's trust store.

Yes, this is possible using what is known as a **wildcard certificate**. It is designed specifically for this purpose.

A single wildcard certificate can secure your primary domain and all of its immediate subdomains.

### What is a Wildcard Certificate

A wildcard certificate is defined by using an asterisk (`*`) as a placeholder for the subdomain level. For your use case, the name on the certificate would be `*.fitfile.net`.

- **It Covers:**
  - `www.fitfile.net`
  - `api.fitfile.net`
  - `dashboard.fitfile.net`
  - Any other single-level subdomain.
- **It Does NOT Cover:**
  - **The bare domain:** A certificate for `*.fitfile.net` does **not** cover `fitfile.net`. You must explicitly add the bare domain as a separate name on the certificate.
  - **Multi-level subdomains:** It will not cover `staging.api.fitfile.net`. The asterisk only applies to a single level.

### How to Request a Wildcard Certificate with `cert-manager`

To get a certificate that covers both `fitfile.net` and all its subdomains, you simply list both the bare domain and the wildcard domain in the `dnsNames` section of your `Certificate` resource.

Here is how you would modify your `Certificate` resource:

```yaml
# my-wildcard-certificate.yaml
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: fitfile-net-wildcard-tls
  namespace: your-app-namespace
spec:
  secretName: fitfile-net-wildcard-tls-secret
  dnsNames:
    - "*.fitfile.net" # The wildcard for all subdomains
    - "fitfile.net" # The bare domain itself
  issuerRef:
    name: hcp-vault-issuer # Your Vault ClusterIssuer
    kind: ClusterIssuer
```

When you apply this, `cert-manager` will request a single certificate from your HCP Vault CA that is valid for both `fitfile.net` and any subdomain ending in `.fitfile.net`. You can then use the resulting `fitfile-net-wildcard-tls-secret` in all your Ingress resources for these services.

#### Vault Configuration Check

Your current Terraform configuration for the Vault PKI role (`kubernetes-apps`) is already set up to permit this, thanks to these lines:

- `allow_subdomains = true`
- `allow_glob_domains = true` (This specifically allows the asterisk `*` character)

This means your Vault CA is ready to sign these wildcard requests from `cert-manager` without any changes.
