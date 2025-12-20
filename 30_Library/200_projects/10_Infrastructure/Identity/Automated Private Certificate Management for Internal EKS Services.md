---
aliases: []
confidence: 
created: 2025-07-23T11:23:25Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:26Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: Automated Private Certificate Management for Internal EKS Services
type:
uid: 
updated: 
version:
---

This document outlines the end-to-end process for integrating AWS Private Certificate Authority (CA) with your private EKS cluster using `cert-manager`. The goal is to provide a seamless, automated workflow for issuing and renewing a wildcard TLS certificate, which can then be used by any internal-facing service.

The process is divided into five distinct phases:

1. **PKI and IAM Foundation (Terraform):** Establishing the root of trust with AWS Private CA and granting the necessary permissions.
2. **Kubernetes Tooling Setup (Terraform/EKS Add-on):** Installing and configuring the necessary in-cluster components.
3. **Wildcard Certificate Provisioning (Kubernetes Manifest):** Creating the reusable wildcard certificate for your domain.
4. **Developer Workflow & Ingress Configuration:** Documenting the simple process for application teams to use the certificate.
5. **Establishing Client Trust (Manual Action):** The critical final step to ensure VDI users' browsers trust the new certificates.

---

## **Phase 1: PKI and IAM Foundation (Terraform)**

The foundation of this solution is a private Public Key Infrastructure (PKI) managed by AWS. We will create a dedicated Certificate Authority and the IAM Role required for the cluster to interact with it. These actions should be performed using Terraform.

**1.1. Create the AWS Private Certificate Authority (CA)**

A best practice is to use a two-tiered hierarchy: a secure Root CA that signs a Subordinate CA, which in turn issues your application certificates

- **Action:** Using Terraform, define resources to create a Root CA and a Subordinate CA within the AWS Private CA service.
- **Key Configuration:**
  - The Subordinate CA will be used to issue certificates for the domain `eoe-sde-codisc.privatelink.fitfile.net`.
  - The private keys for these CAs are stored and protected within FIPS 140-2 validated Hardware Security Modules (HSMs), providing a high level of security

**1.2. Export the Root CA Certificate**

For the VDI users' browsers to trust the certificates issued by your new Subordinate CA, they must first trust its parent, the Root CA.

- **Action:** After the Root CA is created, export its public certificate.
- **Deliverable:** A file, for example `EKS-Private-Root-CA.pem`. This file is not secret and is essential for Phase 5.

**1.3. Create an IAM Role for Service Account (IRSA)**

The `cert-manager` controller in your EKS cluster needs permission to request certificates from your Subordinate CA. We will grant this permission securely using an IAM Role for Service Account (IRSA)

- **Action:** Define an IAM Role in Terraform with a trust relationship that allows the `cert-manager` Kubernetes Service Account to assume it.
- **IAM Policy:** Attach an IAM policy to this role that grants the following permissions, restricted to the ARN of your Subordinate CA 3:
  - `acm-pca:IssueCertificate`
  - `acm-pca:GetCertificate`
  - `acm-pca:ListPermissions`

---

## **Phase 2: Kubernetes Tooling Setup (Terraform/EKS Add-on)**

With the AWS infrastructure in place, we will now install the automation tooling into the EKS cluster.

**2.1. Install `cert-manager`**

`cert-manager` is the standard Kubernetes add-on for automating certificate lifecycle management

- **Action:** Install `cert-manager` into your cluster. The recommended method is using its official Helm chart, which can be managed via the Terraform Helm provider. Ensure you install the Custom Resource Definitions (CRDs) as part of the installation

**2.2. Install the AWS Private CA Issuer Plugin**

This plugin acts as the bridge between `cert-manager` and AWS Private CA

- **Action:** Install the `aws-privateca-issuer` plugin. This is available as a managed Amazon EKS add-on, which simplifies installation and management You can provision this add-on using Terraform.

**2.3. Create the `AWSPCAClusterIssuer`**

This resource tells `cert-manager` how to use your private CA. A `ClusterIssuer` is a non-namespaced resource, making it available for use across the entire cluster

- **Action:** Define and apply an `AWSPCAClusterIssuer` manifest. This can be managed with Terraform's `kubernetes_manifest` resource.
- **Example Manifest (`cluster-issuer.yaml`):**

```yaml
apiVersion: awspca.cert-manager.io/v1beta1
kind: AWSPCAClusterIssuer
metadata:
  name: private-ca-issuer
spec:
  arn: <YOUR_SUBORDINATE_CA_ARN> # ARN of the Subordinate CA from Phase 1
  region: <YOUR_AWS_REGION>
```

---

## **Phase 3: Wildcard Certificate Provisioning (Kubernetes Manifest)**

Now we will create the specific wildcard certificate that your services will use.

- **Action:** Define and apply a `Certificate` manifest. This declarative object instructs `cert-manager` to request a certificate, and `cert-manager` will then handle its renewal automatically before it expires
- **Example Manifest (`wildcard-certificate.yaml`):**

```yaml
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: wildcard-fitfile-net-tls
  namespace: default # Or a dedicated namespace like 'networking'
spec:
  secretName: wildcard-fitfile-net-tls-secret # The secret that will store the cert/key
  commonName: "*.eoe-sde-codisc.privatelink.fitfile.net"
  dnsNames:
    - "*.eoe-sde-codisc.privatelink.fitfile.net"
  issuerRef:
    name: private-ca-issuer # Reference to the ClusterIssuer from Phase 2
    kind: AWSPCAClusterIssuer
```

- **Outcome:** Once applied, `cert-manager` will create a Kubernetes secret named `wildcard-fitfile-net-tls-secret` in the specified namespace containing the `tls.crt` and `tls.key` for your wildcard certificate

---

## **Phase 4: Developer Workflow & Ingress Configuration**

This phase fulfills the core acceptance criteria of providing a simple, documented method for developers to enable SSL.

**4.1. Document the Ingress Configuration**

Application teams will not need to add any special annotations. They simply need to reference the pre-provisioned wildcard secret in the `tls` section of their `Ingress` manifest.

- **Action:** Provide the following manifest snippet as the documented standard for enabling HTTPS on an internal service.
- **Example Ingress Manifest:**

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: my-internal-app-ingress
  # No special cert-manager annotations are needed
spec:
  rules:
    - host: my-app.eoe-sde-codisc.privatelink.fitfile.net
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: my-internal-app-service
                port:
                  number: 80
  tls:
    - hosts:
        - my-app.eoe-sde-codisc.privatelink.fitfile.net
      secretName: wildcard-fitfile-net-tls-secret # Reference the centrally managed secret
```

This approach ensures that services like ArgoCD can also reuse the same wildcard certificate by referencing the same secret.

---

## **Phase 5: Establishing Client Trust (Manual Action)**

This final, crucial step is performed outside of Terraform and Kubernetes. It is the key to eliminating the "insecure connection" warnings for your VDI users.

- **Action:** The `EKS-Private-Root-CA.pem` file exported in Phase 1.2 must be distributed and installed as a trusted root certificate on all RES VDI client machines.
- **Responsibility:** This typically falls to the team managing the VDI environment. The Platform Engineer must coordinate with them to ensure this is rolled out. For Windows environments, this can often be automated via Group Policy.
- **Verification:** Once the Root CA is trusted by a client machine, any certificate signed by it (or its subordinates) will be considered valid by the browser, and the HTTPS connection will show as secure.

Of course. It's a great question. The "insecure connection" warning is fundamentally a problem of trust, and the solution, Public Key Infrastructure (PKI), is best understood as a hierarchical data structure designed to create and verify that trust.

Let's break it down from the perspective of its components and data structures.

### The Core Problem: A Lack of Verifiable Identity

When your browser connects to a server like `https://app.eoe-sde-codisc.privatelink.fitfile.net`, it receives a certificate. The "insecure" warning appears because of two potential issues:

1. **Unproven Identity:** The browser has no way of knowing if the server it's talking to is *really* `app.eoe-sde-codisc.privatelink.fitfile.net` or an imposter. The certificate presented is "self-signed," meaning the server essentially says, "Trust me, I am who I say I am," without any external validation.
2. **Unencrypted Communication:** Without a trusted certificate, a secure, encrypted (TLS) channel cannot be established, leaving the connection vulnerable.

PKI solves the identity problem, which in turn enables the encryption.

---

### The Solution: A Hierarchy of Trust (PKI)

Think of PKI as a system of digital passports. You trust a passport because it's issued by a government you recognize, not just because the person holding it says it's real. PKI works the same way, using a chain of verifiable digital signatures.

Here are the core components and data structures involved:

#### 1. The End-Entity Certificate (The "Passport")

This is the certificate that your application server (like ArgoCD) will use. It's a data file with several key fields:

- **Subject:** Who the certificate belongs to. For your use case, this will be `*.eoe-sde-codisc.privatelink.fitfile.net`.
- **Public Key:** The public part of a cryptographic key pair. The server holds the corresponding private key securely and secretly. This is what allows for encryption.
- **Issuer:** Who issued and vouched for this certificate (e.g., "EOE Internal Subordinate CA").
- **Validity Period:** The dates for which the certificate is valid.
- **Signature:** A cryptographic signature created by the **Issuer** using *their* private key. This is the seal of approval that proves the certificate is authentic and hasn't been tampered with.

This is the "leaf" node in our data structure tree.

#### 2. The Certificate Authority (CA) (The "Passport Office")

The `Issuer` field on a certificate points to a **Certificate Authority (CA)**. A CA is an entity whose entire job is to issue certificates.1 To do this, it must first validate that the requester actually owns the domain or identity they are asking for. In a private environment, you control the CA, so you define the rules for issuance.

#### 3. The Hierarchy (The "Government Structure")

A single CA issuing all certificates is possible, but it's not secure. If that one CA's private key is compromised, the entire system collapses. To solve this, we use a hierarchy, which is the most critical concept to understand.3

```sh
              +------------------+

| Root CA | (The Ultimate Trust Anchor)
| (Self-Signed) | (Private Key is kept OFFLINE)
              +--------+---------+
|
| Signs the Intermediate CA
                       v
            +--------------------+

| Intermediate CA | (The Day-to-Day Issuer)
| (Signed by Root CA)| (Handles all certificate requests)
            +----------+---------+
|
| Signs the End-Entity Certificates
                       v
      +----------------------------------+

| End-Entity / Leaf Certificate |
| (e.g., *.your-domain.net) |
| (Signed by Intermediate CA) |
      +----------------------------------+
```

- **The Root CA (The Ultimate Authority):** This is the top of the trust tree. It has a certificate that is **self-signed**. Its only purpose is to be the absolute root of trust for your entire organization.5 Because it is so critical, its private key is guarded ferociously, often kept completely offline and only used to sign a handful of Intermediate CAs.5 The public certificate of this Root CA is the "golden key" that needs to be distributed to all clients that need to trust your internal services.
- **The Intermediate CA (The Regional Office):** This CA sits below the Root CA. Its certificate is signed by the Root CA's private key. Its purpose is to handle the day-to-day operational work of issuing and renewing the thousands of certificates needed for your applications, servers, and services.3 This creates a crucial security buffer: even if the Intermediate CA's key is compromised, you can revoke it at the Root CA level without having to rebuild your entire trust foundation.

### How This Solves the "Insecure Connection" Problem: The Chain of Trust

When a VDI user's browser connects to your internal service, the following "chain of trust" verification happens in milliseconds:

1. **Server Presents Certificates:** Your application server presents its **End-Entity Certificate** *and* the **Intermediate CA's certificate**.
2. **Browser Verifies Step 1:** The browser looks at the End-Entity certificate and sees it was signed by the "Intermediate CA". It uses the public key from the Intermediate CA's certificate to mathematically verify the signature. If it checks out, the browser knows the End-Entity certificate is authentic and unaltered.
3. **Browser Verifies Step 2:** The browser now looks at the Intermediate CA's certificate and sees it was signed by the "Root CA".
4. **The Final Check:** The browser now looks in its own local "Trusted Root Certificate Store". This is a list of Root CAs that the browser manufacturer (Microsoft, Google, Mozilla) has pre-installed and trusts implicitly.

This is where the problem lies for your internal services. Your private "Root CA" is not in that public list.

**The solution is to manually add your private Root CA's public certificate to the Trusted Root Certificate Store on every single RES VDI machine.**

Once you do that, the chain of trust is complete:

- The browser can verify the server's certificate against the Intermediate CA.
- It can verify the Intermediate CA's certificate against the Root CA.
- It finds the Root CA in its trusted store and declares the entire chain valid.

The "insecure" warning disappears, and the browser proceeds to establish a secure, encrypted TLS connection. By building this hierarchy, you have created your own private, verifiable system of identity.

Of course. This is an excellent question because it gets to the heart of how these components work together in a real-world sequence. Let's walk through the entire process, from the initial setup to a user making a request, and pinpoint where each stage happens and what each component does.

We can break this down into three distinct phases:

1. **Phase 1: The Foundation (One-Time Setup)** - This is where an administrator builds the trust infrastructure.
2. **Phase 2: The Automated Request (Per-Service)** - This is where `cert-manager` gets a certificate for a new application.
3. **Phase 3: The Live Transaction (Per-User Request)** - This is the TLS handshake that happens every time a user connects.

---

### Phase 1: The Foundation (One-Time Setup)

This phase happens **outside the cluster**, typically performed by a platform or security administrator using tools like the AWS Console or Terraform. The goal is to create the ultimate source of trust for your entire internal ecosystem.

- **What Happens:**
  1. A **Root Certificate Authority (CA)** is created in AWS Private CA. This is the most important component in the hierarchy. Its private key is kept highly secure, often offline, and is used very rarely
  2. An **Intermediate CA** is created. Its Certificate Signing Request (CSR) is signed by the Root CA's private key. This Intermediate CA is what will handle all the day-to-day certificate issuance for your applications This two-tier structure is a security best practice that protects the Root CA
  3. The **public certificate of the Root CA** is exported (e.g., as a `.pem` file). This file is not a secret. It's the "public key" of your organization's trust system that clients will need
- **Where it Happens:** AWS Private CA service.
- **Analogy:** This is like the government establishing a central passport agency (the Root CA) and then authorizing regional offices (the Intermediate CAs) to issue passports on its behalf.

### Phase 2: The Automated Request (Per-Service)

This phase happens **inside the EKS cluster** whenever a new internal service needs to be secured. It's a fully automated process orchestrated by `cert-manager`.

- **What Happens:**
  1. **The Trigger:** A developer deploys an application and includes a `Certificate` manifest in their Kubernetes configuration. This manifest is a declarative request for a certificate, specifying the domain name (e.g., `*.eoe-sde-codisc.privatelink.fitfile.net`) and which issuer to use
  2. **`cert-manager` Detects:** The `cert-manager` controller, which is always running in the cluster, sees this new `Certificate` resource
  3. **CSR Generation:** `cert-manager` generates a new private key and a **Certificate Signing Request (CSR)**. A CSR is a standardized block of encrypted text that contains all the information needed to create the certificate, like the domain name and public key
  4. **Plugin Handoff:** `cert-manager` passes this CSR to the **`aws-privateca-issuer` plugin**. This plugin acts as the secure bridge between your Kubernetes cluster and the AWS Private CA service
  5. **Signing Request:** The `aws-privateca-issuer` plugin uses its IAM role to make a secure API call to AWS Private CA, presenting the CSR and asking the **Intermediate CA** to sign it
  6. **Issuance:** The Intermediate CA validates the request, signs the CSR with its private key, and issues the final **End-Entity Certificate**
  7. **Secret Storage:** The signed certificate is passed back through the plugin to `cert-manager`, which then packages it with the private key it generated in step 3 and stores them both in a Kubernetes `Secret`
  8. **Ingress Configuration:** The Ingress controller (e.g., AWS Load Balancer Controller) is configured to use this newly created secret for any traffic directed at `*.eoe-sde-codisc.privatelink.fitfile.net`.
- **Where it Happens:** Entirely within the EKS cluster, orchestrated by `cert-manager` and the `aws-privateca-issuer` plugin, communicating with the AWS Private CA API.
- **Analogy:** This is like an automated kiosk at the regional passport office. You fill out a form (the `Certificate` manifest), the kiosk takes your photo and information (generates the CSR), sends it to the back office for approval (the API call to the Intermediate CA), and then prints your official passport (the Kubernetes `Secret`).

### Phase 3: The Live Transaction (Per-User Request)

This phase happens **over the network** every single time a VDI user's browser tries to connect to your application. This is the **TLS Handshake**, and it's where the chain of trust is verified.

- **What Happens:**
  1. **Client Hello:** The user's browser sends a "Hello" message to the server (your application's Ingress), saying it wants to establish a secure connection.
  2. **Server Hello & Certificate Exchange:** The server responds and sends its certificate chain, which includes:
     - The **End-Entity Certificate** (from the Kubernetes secret).
     - The **Intermediate CA's Certificate**.

  3. **Client-Side Verification (The Magic Moment):** The user's browser performs the following checks in milliseconds:
     - It looks at the End-Entity Certificate and sees it was signed by the "Intermediate CA". It uses the public key from the Intermediate CA's certificate to verify this signature. **Trust is established between the server and the Intermediate CA.**
     - It then looks at the Intermediate CA's certificate and sees it was signed by the "Root CA".
     - Finally, it checks its own local "Trusted Root Certificate Store". Because the Root CA's public certificate was installed on the VDI machine (in Phase 1), it finds a match. **Trust is established between the Intermediate CA and the Root CA.**

  4. **Secure Connection:** Because the entire chain is verified back to a trusted root, the browser knows the server is authentic. It gives the user the green padlock, and they proceed to negotiate a session key to encrypt all further communication.

- **Where it Happens:** Between the user's browser and the EKS Ingress controller.
- **Analogy:** This is like a border agent checking your passport. They see it was issued by a regional office (verifying the End-Entity cert against the Intermediate CA). They then check that the regional office is a legitimate part of the government they recognize (verifying the Intermediate CA against the Root CA). Since their government is on their list of trusted countries, they stamp your passport and let you through.
