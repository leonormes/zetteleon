---
aliases: []
confidence: 
created: 2025-07-24T07:37:08Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:25Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [pki]
title: PKI In AWS With cert-manager
type:
uid: 
updated: 
version:
---

To secure your application at `app.private.fitfile.net` within your private VPC and resolve the "site not secure" warning, it is essential to understand how Public Key Infrastructure (PKI) operates and how **AWS Private CA** and **cert-manager** integrate to manage digital certificates.

## Understanding Public Key Infrastructure (PKI) and Certificates

At its core, **PKI** is a system designed to enable **secure communication between parties who have never met before**. It achieves this by relying on **trusted third parties, known as Certification Authorities (CAs), to issue digital certificates**.

A **digital certificate**, specifically an **X.509 certificate**, is a cryptographic building block that **affirms the identity of a certificate subject and binds that identity to a public key**. This binding ensures that when you receive a public key, you can be confident that it belongs to the entity it claims to represent. For instance, a certificate binds a user's identity (like `IDA`) to their public key (`kpub,A`).

Key components and concepts of certificates include:

- **Subject**: This field contains the distinguished name of the entity associated with the public key. While historically the Common Name (CN) was used for hostnames, the **Subject Alternative Name (SAN) extension is now preferred for specifying multiple hostnames** (e.g., `www.example.com` and `example.com`).
- **Validity Period**: Certificates are valid for a specific time interval, defined by a starting and ending date.
- **Key Usage and Extended Key Usage**: These extensions restrict what a certificate can be used for, such as digital signatures, key encipherment, or TLS web server authentication.
- **Authority Information Access (AIA)**: This extension often lists the address of the CA's Online Certificate Status Protocol (OCSP) responder for real-time revocation checks and may link to the issuer's certificate in the chain.

**Certification Authorities (CAs)** are responsible for generating and issuing certificates for users in the system, acting as a mutually trusted third party. They sign certificates by hashing the contents and then encrypting the hash with their private key, which is then decrypted by a client using the CA's public key to verify authenticity.

There are two main types of CAs:

- **Public CAs**: These CAs issue certificates that are **publicly trusted** by browsers and operating systems, as their root certificates are pre-installed in trust stores (e.g., Let's Encrypt). They are primarily used for public-facing websites to ensure broad trust.
- **Private CAs**: These CAs issue certificates that are **only trusted within a specific organisation or environment**. They are ideal for internal applications, IoT devices, or VPN users where public trust is not required, and fine-grained control over the PKI is desired.

## The "Site Not Secure" Warning for `app.private.fitfile.net`

The "site not secure" warning you are encountering indicates that your browser does not trust the certificate presented by `app.private.fitfile.net`. This is a common issue when using **self-signed certificates** or certificates issued by a **private CA** whose root certificate is not present in your browser's (or operating system's) trust store. For proper security, your browser needs to establish that it is communicating with the legitimate server, and it does this by verifying the certificate chain back to a trusted root CA.

For an internal application like `app.private.fitfile.net` within a private VPC, using a publicly trusted CA is often not feasible or necessary, especially if the domain is not publicly accessible. Instead, a **private PKI** solution is typically employed. However, for such a solution to work without warnings, the **root CA certificate of your private PKI must be explicitly installed in the trust stores of all client devices** (e.g., user laptops, servers) that access `app.private.fitfile.net`.

## Securing `app.private.fitfile.net` Using AWS Private CA and Cert-manager

To secure `app.private.fitfile.net` and remove the "site not secure" warning in a private VPC environment, you can leverage **AWS Private CA** for your private PKI and **cert-manager** for automated certificate lifecycle management within Kubernetes.

### AWS Private CA Components and Role

**AWS Private CA** is a managed service that allows you to **create and manage private certificate authority (CA) hierarchies**, including root and subordinate CAs, without the operational overhead of running your own on-premises CA. It is designed for **private use within an organisation** to issue X.509 certificates for various internal scenarios, such as:

- **Creating encrypted TLS communication channels**.
- **Authenticating users, computers, API endpoints, and IoT devices**.
- **Cryptographically signing code**.

Key features and components of AWS Private CA include:

- **CA Hierarchies**: You can design a CA hierarchy with up to five levels (a root CA and up to four levels of subordinate CAs). Best practice dictates that a **root CA should primarily issue certificates for intermediate CAs**, which then perform the daily task of issuing **end-entity certificates** (also known as client or leaf certificates) to resources like servers and applications.
- **Certificate Customisation**: AWS Private CA allows for significant customisation, enabling you to **create certificates with any subject name, expiration date, supported private key algorithm, key length, and signing algorithm**.
- **Key Security**: The **private keys for private CAs are securely stored in FIPS PUB 140-2 Level 3 compliant hardware security modules (HSMs) managed by AWS**. This offloads the critical burden of private key protection.
- **Revocation Mechanisms**: AWS Private CA supports fully managed **Online Certificate Status Protocol (OCSP)** and **Certificate Revocation Lists (CRLs)** to provide notice when a certificate has been revoked. When OCSP is enabled, its URL is included in the Authority Information Access (AIA) extension of new certificates.
- **Integration with Kubernetes (EKS)**: AWS Private CA can be integrated with Amazon Elastic Kubernetes Service (EKS) to **provide certificate issuance directly inside your Kubernetes clusters**.

### Cert-manager Components and Role

**cert-manager** is a **Kubernetes add-on that automates the management and issuance of TLS certificates** for workloads running in your cluster. It simplifies the process of obtaining certificates from various CAs, including private PKI solutions like AWS Private CA.

Core resources in cert-manager:

- **Issuers and ClusterIssuers**: These Kubernetes resources **represent certificate authorities (CAs)** that can sign certificate requests. `Issuers` are namespace-scoped, while `ClusterIssuers` are cluster-wide versions.
- **Certificate Resource**: This is a human-readable definition of a certificate request that cert-manager uses to generate a private key and a `CertificateRequest` resource.
- **CertificateRequest Resource**: This namespaced resource contains a base64 encoded PEM-encoded certificate request, which is sent to the referenced issuer. `CertificateRequests` are typically managed by controllers or other systems, not humans.
- **Secrets**: Once a certificate is successfully issued, **the signed certificate and its private key are stored in a Kubernetes Secret resource**, which your application Pods can then mount and use. **cert-manager will also ensure that the certificate is automatically renewed before it expires**.

### End-to-End Process for Securing `app.private.fitfile.net`

Here’s a breakdown of the components and steps to secure `app.private.fitfile.net` using AWS Private CA and cert-manager, addressing your "site not secure" warning:

1. **Design and Create your Private CA Hierarchy in AWS Private CA**:
   - Start by creating a **private root CA** in AWS Private CA. It's recommended to dedicate this root CA solely to signing intermediate CAs and to keep it highly secure.
   - Next, create one or more **subordinate CAs** in AWS Private CA, signed by your root CA. These subordinate CAs will then be used for the daily issuance of end-entity certificates for your applications.

2. **Install cert-manager in your Kubernetes Cluster (EKS)**:
   - Deploy **cert-manager** into your Kubernetes cluster. This involves installing the core cert-manager components like the controller and webhook.

3. **Install the `aws-privateca-issuer` Plugin**:
   - **AWS Private CA provides an open-source plug-in, `aws-privateca-issuer`, for cert-manager**. This plug-in acts as an `Issuer` or `ClusterIssuer` within Kubernetes, enabling cert-manager to communicate with and leverage your AWS Private CA instance. This is crucial as it allows cert-manager to request certificates from your private CA without storing the private keys within your Kubernetes cluster.

4. **Configure an Issuer/ClusterIssuer in Kubernetes**:
   - Create a `ClusterIssuer` (for cluster-wide use) or an `Issuer` (for namespace-specific use) Kubernetes resource, specifying its kind as `AWSPCAIssuer` (or similar, depending on the plugin's exact kind) and referencing your AWS Private CA ARN. This tells cert-manager to use your AWS Private CA for signing certificates. You'll need to configure appropriate IAM permissions to allow the cert-manager controller to interact with AWS Private CA.

5. **Create a Certificate Resource for `app.private.fitfile.net`**:
   - Define a `Certificate` resource in Kubernetes for `app.private.fitfile.net`. In this resource, you will specify the desired DNS names (e.g., `app.private.fitfile.net`) in the `spec.dnsNames` field and reference the `Issuer` or `ClusterIssuer` configured in the previous step.
   - cert-manager will then automatically generate a private key and a `CertificateRequest` based on this `Certificate` resource. The `aws-privateca-issuer` will then submit this request to your AWS Private CA.

6. **Automated Certificate Issuance and Storage**:
   - AWS Private CA will sign the certificate request and return the signed certificate to cert-manager.
   - **cert-manager will then store the issued certificate and its corresponding private key in a Kubernetes `Secret`** (e.g., named `app-private-fitfile-net-tls`). This `Secret` is what your application will consume.

7. **Deploy your Application Pods and Mount the Secret**:
   - Configure your application's Kubernetes `Deployment` or `Pod` to **mount the `Secret` containing the TLS certificate and private key**. Your web server (e.g., NGINX, Apache, or your application's server) will then use these files to serve traffic over HTTPS.

8. **Distribute the Private CA Root Certificate to Client Trust Stores**:
   - This is the **most crucial step to eliminate the "site not secure" warning for internal domains**. Since your certificates are issued by a private CA, clients (users' browsers, operating systems, or internal services) will not automatically trust them. You **must distribute the root CA certificate from your AWS Private CA hierarchy to the trust stores of all devices that will access `app.private.fitfile.net`**.
   - This typically involves:
     - Exporting the root CA certificate from AWS Private CA.
     - Distributing it to all client machines (e.g., via Group Policy in Windows, MDM solutions, or manual installation for personal devices).
     - Installing it in the operating system's trust store. Once installed, applications and browsers on that device will trust certificates issued by your AWS Private CA.

9. **Automated Renewal**:
   - cert-manager will **automatically renew the certificate** for `app.private.fitfile.net` before it expires, ensuring continuous secure operation without manual intervention.

This entire process enables you to have a robust, secure, and automated private PKI solution for your internal applications within a Kubernetes environment on AWS.

Think of it like building a secure internal postal service for your company. **AWS Private CA** is like the company's central stamp-making office (the trusted authority for internal mail). It makes unique, company-specific stamps (root and intermediate CA certificates) and then individual package stamps (end-entity certificates) for every department and person. **cert-manager** is your highly efficient mailroom automation system in your Kubernetes office building. When a department needs to send a secure package, cert-manager automatically requests a new package stamp from the stamp-making office, applies it, and ensures it's renewed before it expires. However, for anyone outside your company or using their own personal mail service (like public internet users), these company-specific stamps are meaningless. To get their mail, you need to provide them with a copy of your company's official "stamp design guide" (the root CA certificate) and instruct them to add it to their personal list of trusted stamp designs. Without that, their mail service will just flag your packages as "unsecured" because it doesn't recognise your company's internal stamps.
