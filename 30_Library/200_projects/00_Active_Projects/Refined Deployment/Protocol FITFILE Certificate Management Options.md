---
captured: 2026-02-04T10:16:04+00:00 2026-02-04T10:16:04+00:00
created: 2026-02-04T10:16:07+00:00
modified: 2026-02-11T07:56:00+00:00
source: https://fitfile.atlassian.net/wiki/spaces/FITFILE/pages/2332655617/FITFILE+Certificate+Management+Options
tags:
  - ff_deploy
title: Protocol FITFILE Certificate Management Options
type: protocol
---

## Review of Certificate Management Options

This document reviews possible approaches to TLS certificate management. The goal is to be able to integrate with a customer's existing DNS management capabilities with an automated issuance process to ensure a robust and secure certificate lifecycle that supports FITFILE's operational requirements and security posture.

---

### 1\. Manual Certificate Management Approach

The FITFILE Ops team is sent the customer-generated certificates to configure on the FITFILE Node. Before certificates expire, new certificates must be provided to the FITFILE Ops team to reconfigure.

- DNS and TLS Management Responsibility: The customer is responsible for management of internal DNS and TLS certificates for hostnames used to access the FITFILE application internally.
- Proposed Certificate Lifecycle: customer controls the certificate lifetime, and FITFILE rolls out the update accordingly.

#### Implementation

![[Pasted image 20260204101618.png]]

#### Requirements

1. The Subject Alternative Names (SANs) of the certificate(s) must include either the hostnames or the IP addresses. If the FITFILE Node will be accessed from a static public IP address (i.e. when connecting to a FITFILE network of Nodes over the public internet) AND the customer is not providing access to a public DNS for the app's domain, then the static public IP address must be in the SANs of the issued certificate.
2. Customer must provide the initial certificate files to FITFILE to deploy through the Hashicorp Vault/Kubernetes integration.
3. Customer must notify FITFILE of the certificate lifetimes, and must provide the renewed certificates to FITFILE to redeploy with 2 weeks notice.

#### Risks and Operational Challenges of Manual Approach

- Significant Security Risks: Some customers may provide long-lived certificates which presents a substantial security risk, since a compromised private key provides attackers with a prolonged period to exploit the vulnerability. Manual management is also inherently prone to human error, which can lead to missed renewals or incorrect configurations.
- Operational Challenges: Managing certificates manually is resource-intensive and carries the risk of service disruption if renewals are missed. This approach also has significant scalability limitations as the number of services grows.

This option could be automated by providing the customer with limited access to FITFILE's Hashicorp Vault instance, to push the TLS certificates to their customer namespace via API integration.

---

### 2\. FITFILE Public CA Method

Based on cert-manager: [cert-manager](https://cert-manager.io/docs/)

This approach utilises ACME issuer as a trusted public certificate authority. ACME issuer utilises challenges to prove an entity controls a given public domain. This should only be considered if public access to the FITFILE Node is required (i.e. if the FITFILE Node is apart of a FITFILE Node Network which uses the public internet, and not a private networking solution - e.g. VPN).

- Automated Lifecycle with Short-Lived Certificates: Certificates are automatically provisioned and renewed using tools like `cert-manager` and HashiCorp Vault, with a typical Time-To-Live (TTL) of 90 days. This drastically reduces the impact of a private key compromise.
- Trust inherent: Certificates issued by ACME issuer are globally trusted.
- Public domain: The domain must be public for the challenges to work. Split-view DNS can be used to have both public and private DNS, but comes with networking requirements.

#### Implementation

![[Pasted image 20260204101648.png]]

#### Requirements

1. `cert-manager` outbound DNS lookup of public DNS record does not resolve via split horizon DNS - it must reach the public DNS resolver (i.e. 1.1.1.1:53).
2. Split horizon DNS record must have the same exact hostname as the public DNS record so that the certificate is valid for both.
3. Outbound traffic (https 443) to ACME issuer and the API controller of the public DNS must be allowed.

### 3\. FITFILE Private CA Method

Based on cert-manager: [cert-manager](https://cert-manager.io/docs/)

This approach utilises a robust, automated, and secure Public Key Infrastructure (PKI) managed by FITFILE.

- Automated Lifecycle with Short-Lived Certificates: Certificates are automatically provisioned and renewed using tools like `cert-manager` and HashiCorp Vault, with a typical Time-To-Live (TTL) of 90 days. This drastically reduces the impact of a private key compromise.
- Secure Two-Tier CA Hierarchy: A secure structure with an offline Root CA signs a per-customer Intermediate CA used for day-to-day issuance, ensuring the Root CA's private key is highly protected.
- Trust Establishment: Trust is established when the customer distributes the FITFILE Root CA and Intermediate CA certificates to client trust stores (e.g., VDI golden images). The lifetime of Intermediate certificates can be configured as needed.

#### Implementation

![[Pasted image 20260204101702.png]]

#### Requirements

1. Customer IT must distribute the FITFILE Root CA and Intermediate CA certificates to client trust stores (e.g., VDI golden images), and must reconfigure when FITFILE managed Intermediate CA certificate or Root CA certificates are updated.

### 4\. Hybrid Approach (Customer-Managed Issuer)

Based on cert-manager: [cert-manager](https://cert-manager.io/docs/)

As a compromise, this option allows the customer to retain control over the certificate issuing authority while still benefiting from FITFILE's automation.

- Shared Responsibility Model: The customer would manage the certificate Issuer (e.g., their own internal CA or a trusted third-party CA). They would then provide FITFILE with scoped credentials to this Issuer, compatible with `cert-manager`.
- Automated Issuance: FITFILE's `cert-manager` would use the provided credentials to automate the request, renewal, and deployment of certificates for the application.
- Benefits: This approach addresses potential security concerns by giving them full control over the CA and its policies. Simultaneously, it allows FITFILE to maintain an automated, error-resistant, and efficient certificate lifecycle.
- Considerations: This model requires a clear process for the secure management and rotation of the credentials provided to `cert-manager`. This would need to be discussed and agreed upon.

#### Implementation

![[Pasted image 20260204101716.png]]

Requirements:

1. Outbound networking configured for access to customer certificate issuer.
2. Issuer must be compatible with cert-manager: [Issuers](https://cert-manager.io/docs/configuration/issuers/).
3. Secrets to request certificate from customer certificate issuer must be provided to FITFILE to deploy to the cert-manager instance in the FITFILE Node. FITFILE must be notified when secrets require updating.

---

### Comparison of Approaches

| Feature              | Option 1: Manual Approach                                    | Option 2: FITFILE public CA Approach                     | Option 3: FITFILE private CA Approach                                         | Option 4: Hybrid Approach                                          |
|----------------------|--------------------------------------------------------------|----------------------------------------------------------|-------------------------------------------------------------------------------|--------------------------------------------------------------------|
| Feature              | Option 1: Manual Approach                                    | Option 2: FITFILE public CA Approach                     | Option 3: FITFILE private CA Approach                                         | Option 4: Hybrid Approach                                          |
| Certificate Lifespan | ~1 year?                                                     | ~90 Days                                                 | ~90 Days                                                                      | ~90 Days (or as per Issuer policy)                                 |
| Management           | Manual (preference for direct control, alignment with CAB)   | Automated (cert-manager, ACME issuer, DNS integration)   | Automated (cert-manager, Vault, DNS integration)                              | Hybrid (Customer manages Issuer; FITFILE automates issuance)       |
| Security Risk        | High (extended exposure if compromised, human error)         | Low (minimal exposure due to short lifespan, automation) | Low (minimal exposure due to short lifespan, automation)                      | Medium (Customer controls Issuer; risk in credential management)   |
| Operational Overhead | High (manual tracking, renewal, potential resource strain)   | Lowest (utilising globally trusted certificate chain)    | Low (automation minimises human error and resource strain)                    | Low for FITFILE, Medium for Customer (manage Issuer &amp; secrets) |
| Scalability          | Poor (relies on manual effort)                               | High (automation scales with infrastructure)             | High (automation scales with infrastructure)                                  | High (automation scales)                                           |
| Error Potential      | High (human error in manual processes)                       | Lowest (fully automated)                                 | Low (automation minimises human error)                                        | Low (automation for issuance; risk in credential rotation)         |
| Trust Establishment  | Customer manages their internal CA/certificate distribution. | Globally trusted certificate. No new trust required      | Customer distributes FITFILE Root CA to client trust stores (one-time setup). | Customer uses their own trusted Issuer. No new trust required.     |
| Wildcard Support     | Indicated, but no specifics on use cases or scope.           | Supported and configurable                               | Supported and configurable within Vault roles.                                | Dependent on Customer's Issuer configuration.                      |

---

While a proposal for manual, long-lived certificate management would be understood to be driven by a desire for oversight and alignment with existing processes, it introduces significant security and operational risks.

FITFILE's automated approaches offer demonstrably superior security, efficiency, and scalability. The recommend tier approach:

1. Preferred Option if a subdomain of [fitfile.net](http://fitfile.net/ "http://fitfile.net") is acceptable: Adopt FITFILE's Public CA Approach.This offers the same level of security as the FITFILE Private CA method, and also produces globally trusted certificates, removing the need for CA cert distribution.
2. Preferred Option if customer domain is required (e.g. \*.nhs.net): Adopt FITFILE's Private CA Method. This offers the highest level of security and efficiency by combining short-lived certificates with full automation.
3. Alternative Option: Adopt the Hybrid Approach. This model is an excellent compromise, balancing the need for control over the issuing authority with the proven benefits of FITFILE's automation.
4. Initial Fallback: If none of the automated approaches can be agreed upon for the initial deployment, FITFILE can accommodate a manual certificate update process for the initial phase. FITFILE would then strongly recommend establishing a roadmap to migrate towards one of the automated solutions at a later date to reduce long-term risk and operational overhead.
