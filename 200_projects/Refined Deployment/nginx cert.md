---
aliases: []
confidence: 
created: 2025-09-08T17:07:53Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T14:24:14Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [security]
title: nginx cert
type:
uid: 
updated: 
version:
---

Of course. Here are the atomic Zettelkasten notes generated from our conversation, ready for your Obsidian vault.

Verifying Nginx Ingress Controller Connectivity via TLS

---

title: Verifying Nginx Ingress Controller Connectivity via TLS

created: 2025-09-08T18:05:30

tags:

- kubernetes
- nginx
- ingress
- tls
- troubleshooting
  aliases:
- Nginx Ingress TLS Probe

---

You can verify that traffic is reaching an Nginx Ingress Controller in Kubernetes, even if the final TLS handshake fails. The controller's response to a TLS probe provides a clear "fingerprint".

## Probing Methods

1. **`openssl s_client` (Most Explicit)**: This command attempts a TLS connection and shows the certificate presented by the server.
   - **Success Condition**: You receive a certificate chain. If the server certificate is either your application's certificate or the **"Kubernetes Ingress Controller Fake Certificate"**, you have successfully reached the ingress controller.
   - **Failure Condition**: The connection times out, is reset (RST), or you get "no peer certificate available". This indicates traffic is being blocked or misrouted *before* reaching the controller (e.g., by a firewall, network policy, or load balancer).

2. **`curl --resolve` (Good for DNS-less testing)**: `curl` can be used to test both the TLS layer and the HTTP layer. The `--resolve` flag is crucial as it correctly sets the `Host` header and the **TLS Server Name Indication (SNI)**, which the ingress controller uses for routing.

   ```bash
   curl -kvv --resolve <HOST_YOU_INTEND>:<PORT>:<PUBLIC_IP> https://<HOST_YOU_INTEND>/
   ```

   - **Success Condition**: The verbose output shows a server certificate (even if invalid), or you receive an HTTP response (e.g., `404 Not Found` from the default backend). This proves the network path is correct.

## Interpreting Outcomes

- **Fake Certificate Presented**: You've reached the controller, but no `tls:` block in any Ingress resource matched the requested hostname (SNI). The network path is working.
- **Your Real Certificate Presented**: You've reached the controller, and it successfully matched a `tls:` rule for your hostname.
- **HTTP 404 after TLS Handshake**: TLS terminated successfully at the controller, but no Ingress *rule* (`spec.rules`) matched the host/path. The TLS part is working correctly.
- **Connection Timeout / TCP RST**: Traffic is not reaching the ingress controller pod on port 443.

See Also:

- [[Increasing Nginx Ingress Controller Verbosity with Helm]]
- [[Kubernetes Test Workload for TLS Verification]]

## Increasing Nginx Ingress Controller Verbosity with Helm

title: Increasing Nginx Ingress Controller Verbosity with Helm

created: 2025-09-08T18:05:30

tags:

- kubernetes
- nginx
- ingress
- helm
- logging
- troubleshooting
  aliases:
- Nginx Ingress Logging Levels

---

When troubleshooting the `ingress-nginx` Helm chart, you can increase log verbosity at three distinct levels. This is done by upgrading the Helm release with new values.

## 1. Controller Process Verbosity (`--v`)

This increases the Kubernetes client-go logging (`klog`) level, which is useful for debugging Ingress rule processing, leader election, and SNI routing decisions.

- **Helm Value**: `controller.extraArgs.v`
- **Example**: To set the log level to 5 (very verbose):

  ```bash
  helm upgrade <release-name> ingress-nginx/ingress-nginx --namespace <namespace> --set controller.extraArgs.v=5
  ```

## 2. Nginx Error Log Level

This controls the log level within the Nginx worker processes themselves, providing details on connection processing phases.

- **Helm Value**: `controller.config.error-log-level`
- **Example**: To set the Nginx error log to `debug`:

  ```bash
  helm upgrade <release-name> ingress-nginx/ingress-nginx --namespace <namespace> --set controller.config.error-log-level=debug
  ```

## 3. Per-Ingress Request Debugging (Annotation)

This is a surgical approach that enables verbose logging for traffic matching a *single* Ingress resource, which is ideal for isolating an issue without flooding the logs.

- **Annotation**: `nginx.ingress.kubernetes.io/enable-debug: "true"`
- **Example**:

  ```yaml
  apiVersion: networking.k8s.io/v1
  kind: Ingress
  metadata:
    name: my-app-ingress
    annotations:
      nginx.ingress.kubernetes.io/enable-debug: "true"
  # ... rest of spec
  ```

## Recommended Approach

1. Start with `controller.extraArgs.v=3` or `5` to trace rule matching.
2. If more detail is needed on the Nginx side, add `controller.config.error-log-level=debug`.
3. Use the `enable-debug` annotation for targeted, production-safe debugging.

Remember to revert the logging levels after troubleshooting to avoid excessive log volume and performance overhead.

See Also:

- [[Verifying Nginx Ingress Controller Connectivity via TLS]]
- [[Troubleshooting Nginx Ingress Snippet Annotation Error]]

## Firewall Rules for Cert-Manager with Cloudflare DNS01

title: Firewall Rules for Cert-Manager with Cloudflare DNS01

created: 2025-09-08T18:05:30

tags:

- kubernetes
- cert-manager
- cloudflare
- security
- firewall
  aliases:
- Cert-Manager egress rules

---

For `cert-manager` to perform a DNS01 challenge using Cloudflare, it requires outbound access to specific API endpoints. All communication occurs over **TCP port 443 (HTTPS)**.

## Required Egress Destinations

1. **Cloudflare API**: Used to create and remove the `_acme-challenge` TXT records required for domain validation.
   - **Domain**: `api.cloudflare.com`

2. **ACME Certificate Authority (CA)**: Used to request challenges and download the issued certificates. For Let's Encrypt, these are:
   - **Production**: `acme-v02.api.letsencrypt.org`
   - **Staging**: `acme-staging-v02.api.letsencrypt.org`

## Whitelisting Best Practice

Because the IP addresses for these services are dynamic and served via CDNs, it is strongly recommended to **whitelist by domain name** rather than by IP address.

If your firewall only supports IP-based rules, you will need to consult the providers' published IP lists, but be aware these change frequently.

- Cloudflare IPs: `https://www.cloudflare.com/ips/`
- Let's Encrypt does not publish a stable list of IPs.

A Kubernetes `NetworkPolicy` can be used to enforce these egress rules at the pod level.

## Cloudflare Certificate Types Explained - Edge, Origin, and Client

title: Cloudflare Certificate Types Explained - Edge, Origin, and Client

created: 2025-09-08T18:05:30

tags:

- cloudflare
- tls
- security
- certificate
  aliases:
- Edge Certificate
- Origin Certificate
- Client Certificate

---

Cloudflare uses three distinct types of certificates, each serving a different purpose in the traffic flow.

## 1. Edge Certificates

- **Location**: Deployed on Cloudflare's global edge servers.
- **Purpose**: To secure the connection between an **end-user's browser** and **Cloudflare**. This is the public-facing certificate that users see.
- **Issuer**: A publicly trusted Certificate Authority (CA) like DigiCert or Let's Encrypt. Browsers trust these by default.
- **Management**: Typically managed automatically by Cloudflare's Universal SSL feature.
- **The "Root CA" for your domain (publicly)**: The public CA that issued this Edge Certificate is the root of trust for your public visitors.

## 2. Origin Certificates

- **Location**: Installed on your **origin server** (e.g., in your Kubernetes cluster on the Nginx Ingress).
- **Purpose**: To secure the connection between **Cloudflare's edge** and your **origin server**. This prevents traffic from being unencrypted "on the back end".
- **Issuer**: Issued by Cloudflare's own private Origin CA.
- **Trust**: **Not** trusted by public browsers. They are only trusted by Cloudflare's proxy services. Using them requires setting the Cloudflare SSL/TLS mode to `Full (Strict)`.
- **The "Root CA" for your origin**: The Cloudflare Origin CA is the root of trust for this specific connection.

## 3. Client Certificates (mTLS)

- **Location**: Installed on a client device or application (e.g., a mobile app, IoT device, or B2B API client).
- **Purpose**: To authenticate the **client** to **Cloudflare**. This is used for Mutual TLS (mTLS), where both the server and client must present a valid certificate. It is a zero-trust security control.
- **Issuer**: A private CA that you configure within your Cloudflare account.
- **Use Case**: Securing APIs and internal services where only authorised clients should have access.

See Also:

- [[Distributing a Custom Root CA to Customers]]
- [[The Impact of ECDSA Certificates on TLS Compatibility]]

## How the HashiCorp Vault PKI Secrets Engine Works

title: How the HashiCorp Vault PKI Secrets Engine Works

created: 2025-09-08T18:05:30

tags:

- vault
- pki
- certificate
- security
  aliases:
- Vault PKI

---

The HashiCorp Vault PKI secrets engine provides a dynamic and secure way to manage a Public Key Infrastructure. It functions as a Certificate Authority (CA) that can issue, sign, and revoke certificates on demand via its API.

## Core Concepts

- **PKI Mount**: An instance of the PKI secrets engine enabled at a specific path (e.g., `pki/`). Each mount represents a single CA, complete with its own key, certificates, and configuration. It can be either a root CA or an [[Configuring Vault PKI as an Intermediate CA|intermediate CA]].
- **Role**: A named configuration within a PKI mount that defines the parameters for certificate issuance. Roles act as policy templates, constraining what can be issued. For example, a role can enforce:
  - Allowed domains (`example.com`, `*.apps.example.com`)
  - Maximum Time-To-Live (TTL)
  - Key type (RSA, EC) and bit size
  - Allowed key usages (e.g., Server Authentication, Client Authentication)
- **Issuance**: Clients (like [[Using Vault AppRole for Cert-Manager in Kubernetes|cert-manager]]) authenticate to Vault and request a certificate from a specific path, such as `pki/issue/web-server-role`. Vault generates a certificate according to the role's policy and returns it.
- **Signing**: Alternatively, a client can generate its own private key and Certificate Signing Request (CSR), then ask Vault to sign it via a path like `pki/sign/web-server-role`. This is often preferred as the private key never leaves the client.

## Common Architecture

The best practice is to configure Vault's PKI mount as an **intermediate CA**. This allows the true **root CA** to remain offline and air-gapped for maximum security, only being used to sign or rotate the Vault intermediate's certificate.

See Also:

- [[Configuring Vault PKI as an Intermediate CA]]
- [[Structuring Vault PKI for Multi-Tenancy - Mounts vs Roles]]
- [[The Purpose of the Vault PKI Secret Backend Role]]

## Configuring Vault PKI as an Intermediate CA

title: Configuring Vault PKI as an Intermediate CA

created: 2025-09-08T18:05:30

tags:

- vault
- pki
- certificate
- security
  aliases:
- Vault Intermediate CA

---

The most secure and recommended architecture for using [[How the HashiCorp Vault PKI Secrets Engine Works|Vault's PKI engine]] is to configure it as an intermediate Certificate Authority (CA), signed by an offline root CA.

## Workflow

1. **Enable a New PKI Mount**: A dedicated mount is created in Vault for the intermediate CA.

   ```bash
   vault secrets enable -path=pki_int pki
   vault secrets tune -max-lease-ttl=43800h pki_int # 5 years
   ```

2. **Generate an Intermediate CSR**: Vault generates a private key (which never leaves Vault) and a Certificate Signing Request (CSR) for the intermediate CA.

   ```bash
   vault write -format=json pki_int/intermediate/generate/internal \
       common_name="My Org Intermediate CA" > intermediate.json
   ```

3. **Sign the CSR with the Offline Root CA**: The CSR generated in the previous step is taken to the offline root CA system (e.g., using `openssl`) and signed. This produces the intermediate CA's certificate.
4. **Import the Signed Certificate into Vault**: The signed intermediate certificate is imported back into the Vault PKI mount. This activates the mount as a signing authority.

   ```bash
   vault write pki_int/intermediate/set-signed certificate=@signed_certificate.pem
   ```

5. **Configure AIA and CRL URLs**: Set the public-facing URLs that Vault will embed in issued certificates for the Authority Information Access (AIA) and CRL Distribution Point (CDP) fields. This allows clients to build the trust chain and check for revocation.

   ```bash
   vault write pki_int/config/urls \
       issuing_certificates="[http://vault.example.com/v1/pki_int/ca](http://vault.example.com/v1/pki_int/ca)" \
       crl_distribution_points="[http://vault.example.com/v1/pki_int/crl](http://vault.example.com/v1/pki_int/crl)"
   ```

Once configured, this mount can issue leaf certificates through roles, and all issued certificates will chain up to the offline root CA.

See Also:

- [[Structuring Vault PKI for Multi-Tenancy - Mounts vs Roles]]
- [[Distributing a Custom Root CA to Customers]]

## Structuring Vault PKI for Multi-Tenancy - Mounts Vs Roles

title: Structuring Vault PKI for Multi-Tenancy - Mounts vs Roles

created: 2025-09-08T18:05:30

tags:

- vault
- pki
- architecture
- security
  aliases:
- Vault PKI Multi-Tenancy

---

When managing certificates for multiple customers or trust domains with [[How the HashiCorp Vault PKI Secrets Engine Works|Vault's PKI engine]], a key architectural decision is whether to use a single PKI mount with multiple roles, or multiple PKI mounts.

## Single Mount, Multiple Roles

In this model, one [[Configuring Vault PKI as an Intermediate CA|intermediate CA]] (one PKI mount) issues certificates for all tenants. Isolation is achieved through separate roles.

- **Pros**: Simpler to manage; only one intermediate CA to rotate.
- **Cons**:
  - **Shared Fate**: All tenants share the same intermediate CA key, CRL, and AIA/CDP URLs.
  - **Revocation**: Revoking the intermediate certificate affects all tenants simultaneously.
  - **Configuration**: All tenants are bound by the mount-level configuration.

This approach is suitable when tenants are part of the same trust domain (e.g., different applications within one organisation).

## Multiple Mounts, Separate Roles

In this model, a dedicated PKI mount is created for each tenant or trust domain (e.g., `pki-cust-a`, `pki-cust-b`). Each mount is its own intermediate CA, signed by the same offline root.

- **Pros**:
  - **Strong Isolation**: Each tenant has its own intermediate key, CRL, and AIA/CDP URLs.
  - **Independent Lifecycle**: An intermediate CA for one customer can be rotated or revoked without impacting any other customer.
  - **Customisation**: Each mount can have completely different configurations and TTLs.
- **Cons**: Higher operational overhead; more intermediate CAs to manage and rotate.

This is the **recommended approach for true multi-tenancy**, such as managing certificates for separate customers, as it provides the strongest security and operational isolation.

## Rule of Thumb

- **Different Customers / Trust Domains**: Use separate **mounts**.
- **Different Applications / Teams within the same Trust Domain**: Use a single mount with multiple **roles**.

## Using Vault AppRole for Cert-Manager in Kubernetes

title: Using Vault AppRole for Cert-Manager in Kubernetes

created: 2025-09-08T18:05:30

tags:

- kubernetes
- vault
- cert-manager
- security
- authentication
  aliases:
- Cert-Manager Vault AppRole

---

AppRole is a secure authentication method for machines and applications, making it an ideal choice for connecting `cert-manager` in Kubernetes to a HashiCorp Vault instance.

## The Authentication Flow

1. **AppRole**: An AppRole is defined in Vault, consisting of a **RoleID** (public, like a username) and a **SecretID** (private, like a password).
2. **Policy**: The AppRole is bound to a Vault policy that grants least-privilege access. For `cert-manager`, this policy should only allow access to the specific paths needed for certificate issuance on a given [[How the HashiCorp Vault PKI Secrets Engine Works|PKI mount]].
3. **Kubernetes Secret**: The `RoleID` and `SecretID` are stored in a Kubernetes Secret.
4. **Vault Issuer**: A `cert-manager` `Issuer` or `ClusterIssuer` resource is configured to use the AppRole method. It references the Kubernetes Secret containing the credentials.
5. **Login**: When `cert-manager` needs to issue a certificate, it reads the credentials from the Secret, presents them to Vault's AppRole login endpoint, and receives a short-lived Vault token in return.
6. **Issuance**: `cert-manager` uses this temporary token to call the PKI mount's `sign` or `issue` endpoint.

## Example Vault `Issuer` for AppRole

This configuration tells `cert-manager` how to authenticate and which PKI path and role to use for signing requests.

````yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: vault-pki-issuer
spec:
  vault:
    server: [https://vault.example.com](https://vault.example.com)
    path: pki-cust-x/sign/ingress # Path to the signing endpoint for the 'ingress' role
    auth:
      appRole:
        path: approle # Path where the approle auth method is mounted
        roleId: "<your-role-id>"
        secretRef:
          name: vault-approle-credentials # Name of the K8s Secret
          key: secretId # Key within the Secret containing the SecretID

This method is more secure than using static tokens as the SecretID can be rotated, have a TTL, and be restricted by usage count or network CIDRs.
See Also:
 * [[Terraform for Vault AppRole and Policy for Cert-Manager]]
 * [[The Purpose of the Vault PKI Secret Backend Role]]
<!-- end list -->

***

### Terraform for Vault AppRole and Policy for Cert-Manager

```markdown
---
title: Terraform for Vault AppRole and Policy for Cert-Manager
created: 2025-09-08T18:05:30
tags:
  - terraform
  - vault
  - cert-manager
  - iac
  - security
---

This Terraform code defines a least-privilege Vault policy and an AppRole for use with `cert-manager`. It allows `cert-manager` to sign certificate requests against a specific [[The Purpose of the Vault PKI Secret Backend Role|PKI role]] on a specific mount.

### Vault Policy (`vault_policy`)

The policy grants the minimum necessary permissions: `update` on the `/sign` endpoint and `read` on the CA chain endpoints.

```hcl
variable "pki_mount_path" { default = "pki-cust-x" }
variable "pki_role_name"  { default = "ingress" }

resource "vault_policy" "cert_manager" {
  name   = "cert-manager-policy"
  policy = <<-EOT
    # Allow signing requests for the specified role
    path "${var.pki_mount_path}/sign/${var.pki_role_name}" {
      capabilities = ["update"]
    }

    # Allow reading the issuing CA chain to build the full cert chain
    path "${var.pki_mount_path}/ca_chain" {
      capabilities = ["read"]
    }
  EOT
}

Vault AppRole (vault_approle_auth_backend_role)
This creates the AppRole itself, binding it to the policy created above. It configures TTLs and other security parameters.
resource "vault_approle_auth_backend_role" "cert_manager" {
  backend        = "approle"
  role_name      = "cert-manager-role"
  token_policies = [vault_policy.cert_manager.name]

  # Security settings
  bind_secret_id     = true
  secret_id_ttl      = "24h"
  secret_id_num_uses = 10
  token_ttl          = "1h"
  token_bound_cidrs  = ["10.42.0.0/16"] # Example: Restrict to K8s pod network
}

AppRole SecretID (vault_approle_auth_backend_role_secret_id)
This resource generates a SecretID for the AppRole, which can be securely passed to Kubernetes, for example via CI/CD pipeline variables.
resource "vault_approle_auth_backend_role_secret_id" "cert_manager" {
  backend   = "approle"
  role_name = vault_approle_auth_backend_role.cert_manager.role_name
}

output "approle_role_id" {
  value = vault_approle_auth_backend_role.cert_manager.role_id
}

output "approle_secret_id" {
  value     = vault_approle_auth_backend_role_secret_id.cert_manager.secret_id
  sensitive = true
}

This Infrastructure-as-Code approach ensures the configuration is repeatable, version-controlled, and adheres to the principle of least privilege.
See Also:
 * [[Using Vault AppRole for Cert-Manager in Kubernetes]]
<!-- end list -->

***

### The Purpose of the Vault PKI Secret Backend Role

```markdown
---
title: The Purpose of the Vault PKI Secret Backend Role
created: 2025-09-08T18:05:30
tags:
  - vault
  - pki
  - security
aliases:
  - Vault PKI Role
---

A **PKI Secret Backend Role** in HashiCorp Vault is a named set of constraints that governs the creation of certificates within a specific [[How the HashiCorp Vault PKI Secrets Engine Works|PKI secrets engine mount]]. It is a mandatory component for issuing any certificate.

It should not be confused with an **AppRole**, which is an *authentication* mechanism.
-   **AppRole**: Defines *who* can access Vault and *how* they authenticate.
-   **PKI Role**: Defines *what* certificates an authenticated entity is allowed to issue.

### Key Constraints Defined in a PKI Role

When `cert-manager` requests a certificate from Vault, it must specify a role (e.g., `/pki/sign/my-role`). Vault then uses the configuration of `my-role` to validate and generate the certificate. Common constraints include:

-   `allowed_domains`: A list of domains the role is allowed to issue certificates for.
-   `allow_subdomains` / `allow_wildcard_certificates`: Booleans to control issuance for subdomains and wildcards.
-   `max_ttl`: The maximum lifetime of a certificate issued by this role.
-   `key_type`: The cryptographic key algorithm to use (e.g., `rsa`, `ec`).
-   `key_bits`: The size of the key (e.g., `2048` for RSA, `256` for EC).
-   `key_usage` / `ext_key_usage`: Specifies the allowed X.509 key usages, such as `ServerAuth` or `ClientAuth`.
-   `use_csr_sans`: If true, Vault will honour the Subject Alternative Names (SANs) from the client's CSR, provided they are within the `allowed_domains`.

### Example Terraform

```hcl
resource "vault_pki_secret_backend_role" "ingress" {
  backend                   = "pki-cust-x"
  name                      = "ingress"
  allowed_domains           = ["apps.cust-x.example.com"]
  allow_subdomains          = true
  allow_wildcard_certificates = true
  max_ttl                   = "720h" # 30 days
  key_type                  = "ec"
  key_bits                  = 256
}

This role, named ingress, allows cert-manager to issue 30-day ECDSA certificates for any subdomain under apps.cust-x.example.com.

***

### Verifying a Certificate Chain with OpenSSL

```markdown
---
title: Verifying a Certificate Chain with OpenSSL
created: 2025-09-08T18:05:30
tags:
  - openssl
  - tls
  - certificate
  - troubleshooting
aliases:
  - openssl verify
---

The `openssl verify` command is a standard tool for validating that a leaf certificate correctly chains up to a trusted root Certificate Authority (CA).

### The Command

The basic syntax requires specifying a CA file containing the trusted certificates and the leaf certificate to be verified.

```bash
openssl verify -CAfile <ca-bundle.pem> <leaf-cert.pem>

 * <leaf-cert.pem>: The certificate you want to check (e.g., tls.crt from a Kubernetes Secret).
 * <ca-bundle.pem>: A file containing the full chain of trust. This file must include every intermediate certificate and the final root certificate in PEM format.
Example Workflow
 * Gather Certificates:
   * leaf.pem: The end-entity certificate.
   * intermediate.pem: The certificate of the intermediate CA that signed the leaf.
   * root.pem: The self-signed root CA certificate.
 * Create the CA Bundle: The intermediates and root must be concatenated into a single file. The order does not strictly matter for openssl verify, but conventionally the root is last.
   cat intermediate.pem root.pem > ca-bundle.pem

 * Run Verification:
   openssl verify -CAfile ca-bundle.pem leaf.pem

   * Successful Output: leaf.pem: OK
   * Failed Output: An error message indicating the point of failure, such as error 20 at 0 depth lookup: unable to get local issuer certificate.
This process confirms cryptographic validity but does not typically check for certificate revocation (CRL/OCSP) by default.
See Also:
 * [[Why OpenSSL Verify Needs the Intermediate Certificate]]
 * [[Distributing a Custom Root CA to Customers]]
<!-- end list -->

***

### Why OpenSSL Verify Needs the Intermediate Certificate

```markdown
---
title: Why OpenSSL Verify Needs the Intermediate Certificate
created: 2025-09-08T18:05:30
tags:
  - openssl
  - tls
  - certificate
  - troubleshooting
  - pki
---

A common point of confusion when using `openssl verify` is why it fails when provided with only the root CA certificate for a leaf certificate issued by an intermediate CA.

### The Chain of Trust

A typical PKI setup has a chain:
`Root CA` -> signs -> `Intermediate CA` -> signs -> `Leaf Certificate`

-   The **Issuer** field of the `Leaf Certificate` contains the name of the `Intermediate CA`.
-   The **Issuer** field of the `Intermediate CA` certificate contains the name of the `Root CA`.

### How `openssl verify` Works

When you run `openssl verify -CAfile root.pem leaf.pem`:

1.  OpenSSL inspects `leaf.pem` and sees it was issued by `Intermediate CA`.
2.  It then looks inside the `-CAfile` (`root.pem`) to find the certificate for `Intermediate CA` so it can verify the signature on the leaf.
3.  The certificate for `Intermediate CA` is **not** in `root.pem`.
4.  Unable to find the issuer, OpenSSL cannot build the chain and fails with an error like `unable to get local issuer certificate`.

### The Solution

The `-CAfile` must contain all the certificates needed to build a complete chain from the leaf up to a trusted root. Therefore, you must provide a file containing both the intermediate certificate(s) and the root certificate.

```bash
# Create a bundle with the necessary chain
cat intermediate.pem root.pem > ca-bundle.pem

# This will now succeed
openssl verify -CAfile ca-bundle.pem leaf.pem

This is different from a web browser, which relies on the server to send the leaf certificate plus any necessary intermediates during the TLS handshake. openssl verify does not have this context and must be given the full chain manually.
See Also:
 * [[Verifying a Certificate Chain with OpenSSL]]
 * [[Distributing a Custom Root CA to Customers]]
<!-- end list -->

***

### Distributing a Custom Root CA to Customers

```markdown
---
title: Distributing a Custom Root CA to Customers
created: 2025-09-08T18:05:30
tags:
  - security
  - pki
  - certificate
  - administration
---

When you issue certificates from a private PKI (e.g., using [[How the HashiCorp Vault PKI Secrets Engine Works|HashiCorp Vault]]), you must provide customers with the necessary information to trust those certificates.

### What to Provide

Customers only need to trust the **root of your PKI chain**. Therefore, you should provide them with one file:

-   **The Root CA Certificate (`rootCA.pem`)**: This is the public certificate of your self-signed root CA. It is the ultimate "trust anchor".

You should **NOT** provide them with:
-   Any private keys.
-   The intermediate CA certificate for installation in their trust store.

### Why Only the Root Certificate?

-   **Trust Anchor**: By installing the root certificate into their system's trust store, a customer's machine is configured to trust *any* certificate that can be cryptographically linked back to that root.
-   **Chain Presentation**: It is the responsibility of your servers (e.g., your web server or ingress controller) to present the full certificate chain (leaf certificate + intermediate certificate(s)) during the TLS handshake.
-   **Client Validation**: A client (like a web browser) receives the full chain from the server and validates it against the root CA already present in its trust store.

This separates the concern of *distributing trust* (giving the customer the root) from the concern of *using certificates* (configuring servers to present the full chain).

### How to Generate the Files

-   **Root Certificate**: This is generated once when you create your offline root CA.
-   **Full Chain for Servers**: This can be exported from Vault. It will contain the intermediate and root certificates, and should be deployed alongside the leaf certificate on your servers.
    ```bash
    vault read -field=ca_chain pki_int/ca/chain > ca_chain.pem
    ```

See Also:
-   [[Adding a Custom Root CA to System Trust Stores]]
-   [[Why OpenSSL Verify Needs the Intermediate Certificate]]

Adding a Custom Root CA to System Trust Stores
---
title: Adding a Custom Root CA to System Trust Stores
created: 2025-09-08T18:05:30
tags:
  - certificate
  - security
  - macos
  - windows
  - administration
---

To make a system trust certificates issued by a private Certificate Authority (CA), the root certificate of that CA must be added to the operating system's trust store.

### macOS

#### GUI Method (Keychain Access)

1.  Double-click the `rootCA.pem` file or open the **Keychain Access** application.
2.  Select the **System** keychain in the top-left pane.
3.  From the menu, choose `File` > `Import Items...` and select your `rootCA.pem` file.
4.  Find the newly imported certificate in the list, double-click it.
5.  Expand the **Trust** section.
6.  Set "When using this certificate" to **Always Trust**.
7.  Close the window and enter your administrator password when prompted.

#### Command Line Method

```bash
sudo security add-trusted-cert -d -r trustRoot -k /Library/Keychains/System.keychain rootCA.pem

Windows
GUI Method (Certificate Import Wizard)
 * Double-click the rootCA.crt file (you may need to rename it from .pem).
 * Click the Install Certificate... button.
 * Choose the Local Machine store location and click Next.
 * Select Place all certificates in the following store.
 * Click Browse... and select the Trusted Root Certification Authorities store.
 * Click Next, then Finish. Acknowledge the security warning.
Command Line Method (certutil)
Open Command Prompt or PowerShell as an Administrator.
certutil -addstore -f "ROOT" rootCA.crt

After these steps, applications that use the OS trust store (like Chrome, Edge, Safari, and curl) will automatically trust certificates issued by your private CA.
See Also:
 * [[Distributing a Custom Root CA to Customers]]
<!-- end list -->

***

### Kubernetes Test Workload for TLS Verification

```markdown
---
title: Kubernetes Test Workload for TLS Verification
created: 2025-09-08T18:05:30
tags:
  - kubernetes
  - yaml
  - ingress
  - tls
  - troubleshooting
---

This set of Kubernetes manifests creates a simple "hello world" application, service, and ingress. It is useful for testing that an ingress controller is correctly configured for TLS termination.

Replace the following placeholders:
-   `NAMESPACE`: The target namespace.
-   `tls-test.example.com`: The hostname covered by your TLS certificate.
-   `tls-test-cert`: The name of the Kubernetes `tls` Secret containing your certificate and private key.
-   `nginx`: Your `ingressClassName`.

```yaml
---
apiVersion: v1
kind: Namespace
metadata:
  name: NAMESPACE
---
# A simple Pod that responds to HTTP requests on port 80
apiVersion: v1
kind: Pod
metadata:
  name: tls-test-pod
  namespace: NAMESPACE
  labels:
    app: tls-test
spec:
  containers:
    - name: app
      image: nginxdemos/hello:plain-text
      ports:
        - containerPort: 80
---
# A ClusterIP Service to expose the Pod internally
apiVersion: v1
kind: Service
metadata:
  name: tls-test-svc
  namespace: NAMESPACE
spec:
  selector:
    app: tls-test
  ports:
    - name: http
      port: 80
      targetPort: 80
---
# An Ingress resource to expose the Service externally via HTTPS
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: tls-test-ing
  namespace: NAMESPACE
  annotations:
    # Forces HTTP traffic to redirect to HTTPS
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  ingressClassName: nginx
  tls:
    - hosts:
        - tls-test.example.com
      secretName: tls-test-cert
  rules:
    - host: tls-test.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: tls-test-svc
                port:
                  number: 80

How to Test
After applying this YAML, you can test the configuration from outside the cluster.
# Replace INGRESS_IP with the public IP of your ingress controller
curl -kvv --resolve tls-test.example.com:443:<INGRESS_IP> [https://tls-test.example.com](https://tls-test.example.com)

A successful test will show a valid TLS handshake (with the certificate from tls-test-cert) and an HTTP 200 response from the nginxdemos/hello application.
See Also:
 * [[Verifying Nginx Ingress Controller Connectivity via TLS]]
<!-- end list -->

***

### Troubleshooting Nginx Ingress Snippet Annotation Error

```markdown
---
title: Troubleshooting Nginx Ingress Snippet Annotation Error
created: 2025-09-08T18:05:30
tags:
  - kubernetes
  - nginx
  - ingress
  - troubleshooting
  - security
---

When creating or updating an Ingress resource for `ingress-nginx`, you may encounter an error from the admission webhook:

> admission webhook "validate.nginx.ingress.kubernetes.io" denied the request: nginx.ingress.kubernetes.io/server-snippet annotation cannot be used. Snippet directives are disabled by the Ingress administrator

### Cause

This error occurs because, for security reasons, the ability to inject raw Nginx configuration snippets via annotations (`server-snippet`, `configuration-snippet`, etc.) is disabled by default in the `ingress-nginx` Helm chart. Allowing arbitrary snippets can create security vulnerabilities if not properly controlled, as it allows users who can edit Ingress objects to modify server behaviour at a low level.

### Solution 1: Remove the Snippet (Recommended)

The simplest and most secure solution is to remove the snippet annotation from your Ingress manifest if it is not strictly necessary. For most use cases, dedicated annotations exist to achieve the desired behaviour (e.g., `nginx.ingress.kubernetes.io/proxy-body-size` instead of a snippet).

### Solution 2: Enable Snippets Globally

If snippets are required, you must explicitly enable them in the ingress controller's configuration. This is typically done by setting a command-line argument on the controller's deployment.

#### Using Helm

You can enable snippets by upgrading the `ingress-nginx` Helm release with the `controller.allowSnippetAnnotations` value set to `true`.

```bash
helm upgrade <release-name> ingress-nginx/ingress-nginx \
  --namespace <namespace> \
  --set controller.allowSnippetAnnotations=true

Warning: Enabling this feature globally reduces the security posture of your ingress controller. It should only be done in environments where all users with permission to edit Ingress resources are trusted.
See Also:
 * [[Increasing Nginx Ingress Controller Verbosity with Helm]]
<!-- end list -->

***

### Troubleshooting TLS Handshake Failure with Cloudflare

```markdown
---
title: Troubleshooting TLS Handshake Failure with Cloudflare
created: 2025-09-08T18:05:30
tags:
  - troubleshooting
  - tls
  - cloudflare
  - curl
  - security
---

When using `curl` to connect to a domain proxied by Cloudflare, you may encounter the following error:


curl: (35) LibreSSL/3.3.6: error:1404B410:SSL routines:ST_CONNECT:sslv3 alert handshake failure

This generic error indicates that the TLS handshake was aborted by the server. When Cloudflare is proxying traffic (orange cloud), this error comes from **Cloudflare's edge**, not your origin server.

### Common Causes

1.  **Mutual TLS (mTLS) is Enabled**: The most common cause is a Cloudflare mTLS policy requiring clients to present a valid [[Cloudflare Certificate Types Explained - Edge, Origin, and Client|Client Certificate]]. A standard `curl` request does not send one, so Cloudflare terminates the connection.
2.  **Strict TLS/Cipher Policy**: Cloudflare might be configured to only allow modern TLS versions (e.g., TLS 1.3) and specific cipher suites. If the client (`curl`'s underlying TLS library like LibreSSL) does not support or offer a matching cipher, the handshake will fail.
3.  **WAF or Security Rules**: A Web Application Firewall (WAF) rule or other security feature could be blocking the request at the TLS layer before it even reaches the HTTP stage.

### Diagnosis and Resolution

1.  **Check Cloudflare Settings**: Verify if mTLS is enabled for the zone or hostname in the Cloudflare dashboard under `SSL/TLS` > `Client Certificates`.
2.  **Test Origin Directly**: To confirm the issue is at Cloudflare's edge, bypass the proxy.
    -   Temporarily set the DNS record to **DNS Only** (grey cloud) in Cloudflare.
    -   Or, use `curl --resolve` to connect directly to your origin server's public IP address.
        ```bash
        curl -kvv --resolve myapp.example.com:443:<ORIGIN_SERVER_IP> [https://myapp.example.com/](https://myapp.example.com/)
        ```
    If the connection succeeds when bypassing Cloudflare, the problem lies within your Cloudflare configuration.

If the error persists when connecting directly to the origin, the issue may be a cipher suite mismatch between your client and your origin server, often related to using [[The Impact of ECDSA Certificates on TLS Compatibility|ECDSA certificates]].

The Impact of ECDSA Certificates on TLS Compatibility
---
title: The Impact of ECDSA Certificates on TLS Compatibility
created: 2025-09-08T18:05:30
tags:
  - tls
  - certificate
  - security
  - troubleshooting
  - pki
aliases:
  - EC Certificates
  - ECDSA
---

While Elliptic Curve Digital Signature Algorithm (ECDSA) certificates offer smaller key sizes and better performance than RSA, they can introduce compatibility issues, particularly with older TLS clients.

### The Cipher Suite Mismatch Problem

During a TLS handshake, the client sends a list of cipher suites it supports, and the server picks one it also supports. A cipher suite defines the entire cryptographic process (key exchange, bulk encryption, MAC).

-   An **RSA certificate** can only be used with cipher suites that specify an RSA-based key exchange.
-   An **ECDSA certificate** can only be used with cipher suites that specify an ECDSA-based key exchange.

If a server is configured *only* with an ECDSA certificate, and a client connects that *only* proposes RSA-based cipher suites, there is no common algorithm they can agree on. The server has no choice but to abort the connection, often resulting in a `sslv3 alert handshake failure` error.

### Common Scenarios

This issue often arises when:
-   **Older TLS Libraries**: Clients using older libraries (like older versions of OpenSSL, LibreSSL on macOS, or legacy Java applications) may have limited or no support for modern ECDSA cipher suites.
-   **Strict Server Configuration**: A server might be configured to only support a narrow set of modern, secure ciphers that the older client doesn't offer.

### Recommendations for Compatibility

1.  **Use RSA for Broadest Compatibility**: For public-facing services where you do not control the clients, using an **RSA 2048-bit** certificate remains the safest choice for maximum compatibility.
2.  **Use P-256 for EC**: If using ECDSA, the **P-256** (also known as `prime256v1`) curve has the widest support among modern clients. Avoid less common curves unless you are certain all your clients support them.
3.  **Dual Certificates**: Modern servers (like Nginx 1.11+) can be configured with both an RSA and an ECDSA certificate simultaneously. The server will then automatically select the best certificate based on the cipher suites offered by the connecting client.

When troubleshooting TLS handshake failures with an ECDSA certificate, always test with a modern TLS client (e.g., `curl` linked against a recent OpenSSL version) to rule out client-side compatibility as the cause.

See Also:
-   [[Troubleshooting TLS Handshake Failure with Cloudflare]]
-   [[The Purpose of the Vault PKI Secret Backend Role]]
````
