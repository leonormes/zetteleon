---
aliases: []
confidence: 
created: 2025-07-23T03:53:22Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:26Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [pki]
title: Core PKI Object Types
type:
uid: 
updated: 
version:
---

## **Core PKI Object Types**

### 1. **CertificateAuthority (CA)**

- **Attributes:**
  - `publicKey`
  - `privateKey`
  - `certificate` (self-signed or signed by a parent CA)
  - `issuedCertificates` (list of Certificates)
  - `revocationList` (CRL)
- **Methods:**
  - `issueCertificate(request)`
  - `revokeCertificate(certificate)`
  - `sign(data)`
  - `verify(certificate)`

### 2. **Certificate**

- **Attributes:**
  - `serialNumber`
  - `subject` (Distinguished Name, e.g., CN, O, OU, etc.)
  - `issuer` (CA that signed it)
  - `publicKey`
  - `validFrom`
  - `validTo`
  - `signature`
  - `extensions` (e.g., SAN, key usage, etc.)
- **Methods:**
  - `verifySignature(issuerPublicKey)`
  - `isValid(date)`
  - `getSubject()`
  - `getIssuer()`

### 3. **CertificateSigningRequest (CSR)**

- **Attributes:**
  - `subject`
  - `publicKey`
  - `signature` (signed by the private key corresponding to the public key in the request)
- **Methods:**
  - `verifySignature()`
  - `getSubject()`

### 4. **PrivateKey / PublicKey**

- **Attributes:**
  - `algorithm` (e.g., RSA, ECDSA)
  - `keyData`
- **Methods:**
  - `sign(data)` (PrivateKey)
  - `verify(data, signature)` (PublicKey)
  - `encrypt(data)` (PublicKey)
  - `decrypt(data)` (PrivateKey)

### 5. **CRL (Certificate Revocation List)**

- **Attributes:**
  - `issuer`
  - `revokedCertificates` (list of serial numbers and revocation dates)
  - `signature`
- **Methods:**
  - `isRevoked(serialNumber)`
  - `addRevokedCertificate(certificate)`

### 6. **OCSPResponse**

- **Attributes:**
  - `certificateStatus` (good, revoked, unknown)
  - `thisUpdate`
  - `nextUpdate`
  - `signature`
- **Methods:**
  - `verifySignature(issuerPublicKey)`

### 7. **TrustStore**

- **Attributes:**
  - `trustedCAs` (list of CA certificates)
- **Methods:**
  - `isTrusted(certificate)`
  - `addTrustedCA(caCertificate)`

---

## **Relationships**

- A **CertificateAuthority** issues **Certificates**.
- A **Certificate** is signed by a **CertificateAuthority** (or another CA in a chain).
- A **CertificateSigningRequest** is submitted to a CA to request a **Certificate**.
- **CRL** and **OCSPResponse** are used to check the revocation status of a **Certificate**.
- A **TrustStore** contains trusted root CA **Certificates**.

---

## **Example: PKI as OOP Classes (Python-like Pseudocode)**

```python
class CertificateAuthority:
    def __init__(self, name, publicKey, privateKey, certificate):
        self.name = name
        self.publicKey = publicKey
        self.privateKey = privateKey
        self.certificate = certificate
        self.issuedCertificates = []
        self.revocationList = CRL(self)

class Certificate:
    def __init__(self, serialNumber, subject, issuer, publicKey, validFrom, validTo, signature, extensions):
        self.serialNumber = serialNumber
        self.subject = subject
        self.issuer = issuer
        self.publicKey = publicKey
        self.validFrom = validFrom
        self.validTo = validTo
        self.signature = signature
        self.extensions = extensions

class CertificateSigningRequest:
    def __init__(self, subject, publicKey, signature):
        self.subject = subject
        self.publicKey = publicKey
        self.signature = signature

class CRL:
    def __init__(self, issuer):
        self.issuer = issuer
        self.revokedCertificates = []

class TrustStore:
    def __init__(self):
        self.trustedCAs = []
```

## **Summary Table**

| OOP Type/Class            | Description                      |
| ------------------------- | -------------------------------- |
| CertificateAuthority (CA) | Issues and revokes certificates  |
| Certificate               | Represents a digital certificate |
| CertificateSigningRequest | Request for a certificate        |
| PrivateKey/PublicKey      | Key pair for signing/encryption  |
| CRL                       | List of revoked certificates     |
| OCSPResponse              | Online status of a certificate   |
| TrustStore                | Stores trusted CA certificates   |

## How HTTPS Trust Works Between Two Kubernetes Clusters

(Using the PKI objects from the UML)

Below, “Cluster A” contains a client workload, “Cluster B” contains a server workload.

Both clusters sit behind their own ingress gateways but the flow is identical whether you’re talking **pod-to-pod**, **ingress-to-ingress**, or **service mesh mTLS**.

---

### 1. Boot-strapping a Shared Root of Trust

| Step | Objects Involved                       | What Happens                                                                                                     |
| ---- | -------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| 1 a  | **CertificateAuthority ⇢ Certificate** | • A Root CA (`RootCA`) is created once.• `RootCA.certificate` is **self-signed**.                                |
| 1 b  | **TrustStore** (each cluster)          | • `ClusterA.trustStore.addTrustedCA(RootCA.certificate)`• `ClusterB.trustStore.addTrustedCA(RootCA.certificate)` |

Result: both clusters now “trust” anything signed by `RootCA` (or by an Intermediate CA chained to it).

---

### 2. Issuing Service Certificates

| Step | Objects                                                      | Cluster A (client)                                           | Cluster B (server)                                           |
| ---- | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| 2 a  | **CertificateSigningRequest**                                | `csrA = CSR(subject=client.foo.svc, publicKeyA, signatureA)` | `csrB = CSR(subject=server.bar.svc, publicKeyB, signatureB)` |
| 2 b  | **CertificateAuthority.issueCertificate**                    | `certA = RootCA.issueCertificate(csrA)`                      | `certB = RootCA.issueCertificate(csrB)`                      |
| 2 c  | **PrivateKey / Certificate** stored as **Kubernetes Secret** | `Secret(client-tls)` holds `(certA, privateKeyA)`            | `Secret(server-tls)` holds `(certB, privateKeyB)`            |

---

### 3. TLS Handshake at Runtime

```mermaid
sequenceDiagram participant ClientPod as Client Pod (Cluster A) participant ServerPod as Server Pod (Cluster B) Note over ClientPod,ServerPod: Both clusters trust the same Root CA ClientPod->>ServerPod: ClientHello (SNI=server.bar.svc) ServerPod-->>ClientPod: ServerHello + CertificateChain ClientPod->>ClientPod: Check: Is issuer trusted? ClientPod->>ClientPod: Check: Is signature valid? ClientPod->>ClientPod: Check: Is certificate valid (date)? ClientPod->>ClientPod: Check: Is certificate revoked? Note over ClientPod: Server authenticated alt Mutual TLS enabled ClientPod-->>ServerPod: Client CertificateChain ServerPod->>ServerPod: Check: Is issuer trusted? ServerPod->>ServerPod: Check: Is signature valid? ServerPod->>ServerPod: Check: Is certificate valid (date)? ServerPod->>ServerPod: Check: Is certificate revoked? Note over ServerPod: Client authenticated end ClientPod-->>ServerPod: EncryptedFinished ServerPod-->>ClientPod: EncryptedFinished Note over ClientPod,ServerPod: Encrypted HTTP session established
```

All the method calls map directly to our OOP objects:

| Verification Call                         | Under the Hood                                                        |
| ----------------------------------------- | --------------------------------------------------------------------- |
| `TrustStore.isTrusted(certB)`             | Looks for `certB.issuer` (RootCA) in `trustedCAs`                     |
| `certB.verifySignature(RootCA.publicKey)` | `PublicKey.verify(certB.tbsData, certB.signature)`                    |
| Revocation check                          | `CRL.isRevoked(certB.serial)` **or** `OCSPResponse.certificateStatus` |

---

### 4. Ongoing Operations

| Scenario                             | Object Methods                                                                                                 |
| ------------------------------------ | -------------------------------------------------------------------------------------------------------------- |
| **Automatic renewal** (cert-manager) | `CertificateAuthority.issueCertificate(newCSR)` and secret update before `cert.validTo`                        |
| **Immediate revocation**             | `CertificateAuthority.revokeCertificate(certB)` → `CRL.addRevokedCertificate(certB)`; next handshake will fail |
| **Key rotation**                     | New `PrivateKey`, new `CSR`, repeat issuance flow                                                              |

---

## Key Take-aways

1. **Single Root of Trust**
   Distributing the *Root CA certificate* to every cluster’s **TrustStore** is what makes cross-cluster TLS possible.
2. **Leaf Certificates Are Just Data**
   A **Certificate** object is nothing more than a signed blob binding a subject to a `PublicKey`. All trust decisions are pure method calls (`verifySignature`, `isRevoked`, `isValid`).
3. **Handshake == Runtime Verification**
   Every HTTPS session replays the same OOP interactions: send `Certificate`, call `TrustStore.isTrusted`, etc. If any step returns `false`, the connection is dropped.
4. **Mutual TLS Optional**
   Turn it on simply by having the *client* also send its own **Certificate** and letting the server run the same verification logic.

This object-centric view shows that HTTPS trust between clusters is nothing more than orchestrating these class interactions at three moments: boot-strap, issuance, and every handshake.

---

## **1. Setting Up a CA in AWS**

- **You use AWS Certificate Manager Private CA (ACM PCA)** to create a private root or subordinate CA.
- This CA can issue certificates for your internal services, ingress controllers, or service mesh workloads.

**Steps:**

1. In the AWS Console, go to ACM PCA and create a new private CA (root or subordinate).
2. Activate the CA (requires a certificate signing process if subordinate).
3. The CA now has a private key (managed by AWS) and a public certificate.

---

## **2. Integrating the CA with Your EKS Cluster**

- **Certificate Issuance:**
  Use [cert-manager](https://cert-manager.io/docs/) in your EKS cluster, along with the [AWS Private CA Issuer plugin](https://github.com/cert-manager/aws-privateca-issuer), to automate certificate requests and renewals from ACM PCA.
- **Trust Store:**
  Distribute the ACM PCA’s root certificate to all workloads (and to any other clusters that need to trust your services).

**How it works in EKS:**

- cert-manager is configured with an `AWSPCAClusterIssuer` that points to your ACM PCA.
- When a service (e.g., an ingress controller) needs a certificate, it creates a `Certificate` resource.
- cert-manager requests a certificate from ACM PCA, which issues and returns it.
- The certificate and private key are stored as a Kubernetes Secret, which your service uses for TLS.

---

## **3. Trust for Other Clusters Calling In**

- **Distribute the Root CA Certificate:**
  Any external cluster (on AWS, on-prem, GCP, etc.) that needs to trust your EKS services must have the ACM PCA’s root certificate in its trust store.
- **How External Clusters Use It:**
  - When they connect to your EKS service over HTTPS, your service presents a certificate signed by your ACM PCA.
  - The external cluster verifies the certificate chain up to the ACM PCA root.
  - If the root is in their trust store, the connection is trusted.
- **For Mutual TLS:**
  If you want to require client certificates (mTLS), you can:
  - Issue client certificates from the same ACM PCA (or a subordinate).
  - Configure your EKS ingress/service mesh to require and verify client certificates.
  - External clusters present their client certificates, which your EKS workloads verify against the same root CA.

---

## **4. Visual Flow**

```sh
[ACM Private CA]
      |
      | issues certs via cert-manager
      v
[EKS Cluster] -- exposes HTTPS endpoint signed by ACM PCA
      ^
      | (external clusters must trust ACM PCA root)
[Other Clusters] -- call in over HTTPS, verify server cert using ACM PCA root
```

## **5. Key Points and Best Practices**

- **ACM PCA never exposes its private key**; all signing is done via AWS APIs.
- **cert-manager + AWS Private CA Issuer** is the standard way to automate cert issuance in EKS.
- **Distribute the root CA cert** securely to all clients (other clusters, CI/CD, etc.) that need to trust your services.
- **Rotate and revoke certificates** using cert-manager and ACM PCA as needed.
- **For mTLS**, both sides need certs issued by the same (or cross-trusted) CA, and both must trust the root.

---

## **References**

- [AWS ACM Private CA documentation](https://docs.aws.amazon.com/acm-pca/latest/userguide/PcaWelcome.html)
- [cert-manager AWS Private CA Issuer](https://cert-manager.io/docs/configuration/acm-privateca/)
- [AWS blog: TLS-enabled Kubernetes clusters with ACM Private CA and Amazon EKS](https://aws.amazon.com/blogs/security/tls-enabled-kubernetes-clusters-with-acm-private-ca-and-amazon-eks-2/)

---

**Summary:**
You set up ACM PCA as your CA, use cert-manager in EKS to automate certs, and distribute the root CA cert to any other clusters that need to trust your endpoints. For mTLS, issue client certs from the same CA and configure your services to require and verify them.

Of course. The Public Key Infrastructure (PKI) system establishes trust through a hierarchical model. At its core, a client trusts a server's identity not by knowing the server directly, but because a third party, which the client *already* trusts, has vouched for the server's identity. This trusted third party is a Certificate Authority (CA).

Your UML diagram perfectly captures the data objects involved in this process. Let's break down the hierarchy and how they enable secure connections, especially in a context like AWS EKS.

---

## The Core Components (Your UML Explained)

Your diagram shows the essential data structures for PKI. Here's how they relate:

- **Keys (`PublicKey`, `PrivateKey`):** These are the foundation. A key pair is generated by the entity requesting a certificate (e.g., your web server). The **private key** is kept secret and is used to create digital signatures. The **public key** is shared openly and is used to verify those signatures.
- **Certificate Signing Request (CSR):** This is a formal request sent to a CA. It contains the entity's details (the **Subject**, e.g., `api.your-company.co.uk`) and its **public key**. The entire request is signed using the entity's **private key** to prove ownership.
- **Certificate Authority (CA):** This is the trusted entity. Its primary job is to verify the identity of a requester and, if successful, issue a `Certificate`. The CA uses its own `privateKey` to sign the certificate it issues. A top-level CA is called a **Root CA**. A Root CA can also authorise an **Intermediate CA** to issue certificates on its behalf, creating a chain.
- **Certificate:** This is the digital passport. It binds an identity (`Subject`) to a `PublicKey`. Crucially, it contains the `Issuer` (the CA that signed it) and a digital `Signature` from that CA. Anyone can use the CA's public key to verify this signature.
- **Trust Store:** This is a collection of pre-installed `Certificate`s from Root CAs that a client (like a browser or an operating system) implicitly trusts. This is the starting point for all trust verification.
- **Revocation (`CRL`, `OCSPResponse`):** A certificate might need to be invalidated before its expiry date (e.g., if the private key is compromised). A Certificate Revocation List (CRL) or the Online Certificate Status Protocol (OCSP) are mechanisms to check if a certificate is still valid.

---

## The Hierarchy of Trust

The entire system works by creating a "chain of trust" that starts from the client's Trust Store and ends at the server's certificate.

Here is the typical flow for a secure connection:

1. **Connection Initiated:** Your browser (the client) attempts to connect to a server, for example, an application running behind an Ingress in your EKS cluster.
2. **Server Presents Certificate:** The server presents its `Certificate`. Often, it will also present the certificate of the Intermediate CA that issued its certificate.
3. **Client Verification Begins:**
   - The client looks at the `Issuer` field in the server's certificate. Let's say it's "Intermediate CA X".
   - The client uses the public key from "Intermediate CA X"'s certificate to verify the `Signature` on the server's certificate.

4. **Building the Chain:**
   - Now the client must verify the certificate of "Intermediate CA X". It looks at the `Issuer` field of *that* certificate. Let's say it's "Root CA Y".
   - The client checks its own `TrustStore` to see if it has a certificate for "Root CA Y".

5. **Anchoring Trust:**
   - If "Root CA Y" is in the `TrustStore`, it's a trusted anchor. The client uses the public key from its trusted copy of the "Root CA Y" certificate to verify the `Signature` on the "Intermediate CA X" certificate.

6. **Trust Established:** If all signatures in the chain are valid, the server's certificate is not expired or revoked, and the name on the certificate matches the domain the client is trying to reach, a secure, encrypted session is established. ✅

If at any point a signature is invalid or the root of the chain is not in the client's `TrustStore`, the connection will fail with a security warning.

---

## Practical Application in AWS EKS

For a production-ready certificate infrastructure in EKS, you won't manage these objects manually. You'll use an automated tool like **`cert-manager`**, which is the Kubernetes standard for certificate management.

Here's how the PKI concepts map to `cert-manager` and EKS:

- **`Issuer` or `ClusterIssuer`:** This is the `cert-manager` resource that represents your **`CertificateAuthority`**. You configure it to point to a real CA.
  - **Let's Encrypt (ACME Protocol):** For public-facing services exposed via an Ingress. This is the most common choice for production web traffic. `cert-manager` handles the entire domain validation and issuance process automatically.
  - **Vault:** If you run HashiCorp Vault, you can configure it as a private CA for issuing certificates for internal, service-to-service communication (mTLS). This is excellent for a secure service mesh.
  - **SelfSigned:** A simple issuer for development or for creating your own internal root CA where public trust is not required.
- **`Certificate` Resource:** This Kubernetes resource is effectively your **`CertificateSigningRequest`**. You define a `Certificate` object in YAML, specifying the domain names (`dnsNames`) you need and which `Issuer` should sign it. `cert-manager` does the rest:
  1. It creates a `PrivateKey`.
  2. It generates a `CSR`.
  3. It sends the `CSR` to the configured `Issuer` (e.g., Let's Encrypt).
  4. Once the signed certificate is returned, `cert-manager` saves both the certificate and the private key in a Kubernetes `Secret`.
- **Ingress / Gateway API:** You configure your Ingress (e.g., AWS Load Balancer Controller, NGINX) to use the certificate. You simply reference the Kubernetes `Secret` that `cert-manager` created. The Ingress controller will then automatically use that certificate to terminate TLS for incoming traffic.

By using `cert-manager`, you automate the entire lifecycle, including renewals, ensuring your EKS services are always secured with valid, trusted certificates.

Hello! I'm here to be your personal guide to the shared knowledge base you've provided. I'm an expert in all the documents, tutorials, and configuration details within this material, covering topics like cert-manager installation, certificate issuance, AWS Private CA, and trust management. My goal is to help you quickly understand and effectively use this information, whether you need summaries, specific facts, or clarification on complex procedures. Think of me as your dedicated expert, ready to assist you in navigating and mastering these resources.

You're looking for practical instructions for setting up AWS Private CA with cert-manager. This involves configuring both AWS Private CA as your certificate authority and cert-manager in your Kubernetes cluster to interact with it for certificate issuance.

Here's a detailed guide on how to approach this setup, combining the functionalities of AWS Private CA and cert-manager, including best practices for integration:

### Understanding the Components

Before diving into the steps, let's quickly understand the two main components:

- **AWS Private CA**: This is a managed Amazon Web Services (AWS) service that enables you to create and manage private certificate authority (CA) hierarchies, including root and subordinate CAs [1]. It helps you issue X.509 certificates for internal use within your organization for purposes like encrypted TLS communication channels, authenticating users/devices, and cryptographically signing code, without the operational overhead of running your own on-premises CA [1-3]. AWS Private CA operations can be accessed via the AWS Management Console, API, or CLI [2, 4].
- **cert-manager**: This is a Kubernetes add-on that automates the management and issuance of TLS certificates for workloads in your Kubernetes or OpenShift cluster [5, 6]. It ensures certificates are valid and renews them before they expire [5, 6]. cert-manager can obtain certificates from various CAs, including Let's Encrypt, HashiCorp Vault, Venafi, and private PKI [5]. It uses `Issuer` and `ClusterIssuer` resources to define how it requests TLS certificates [7-9].
- **`aws-privateca-issuer`**: This is an open-source plug-in for cert-manager that allows cert-manager users to set up a CA without storing private keys directly in the Kubernetes cluster [10]. It integrates cert-manager with AWS Private CA, making it suitable for users with regulatory requirements for controlling access to and auditing their CA operations [10]. This plugin is supported on Amazon Elastic Kubernetes Service (Amazon EKS), self-managed Kubernetes on AWS, or on-premises Kubernetes, and supports x86 and ARM architectures [10]. It is listed as a "Maintained" (🥈 Tier) issuer integration for cert-manager [9, 11].

### Prerequisites

Before you begin, ensure you have the following:

1. **AWS Account and AWS CLI**: You need an active AWS account [12, 13] and the AWS Command Line Interface (CLI) installed and configured with appropriate credentials and a default region [12, 14-16].
2. **Kubernetes Cluster**: An Amazon EKS cluster is recommended for the most seamless integration with AWS services [10, 17]. Other Kubernetes environments are also supported [10].
3. **`kubectl`**: The Kubernetes command-line tool, installed and configured to interact with your cluster [18, 19].
4. **`helm`**: Helm version 3 or later is recommended for installing cert-manager [20, 21].

### Practical Instructions for Setting up AWS Private CA with Cert-manager

The overall process involves setting up your private CA in AWS, installing cert-manager in your Kubernetes cluster, and then configuring cert-manager to use your AWS Private CA as an issuer.

#### Step 1: Set up Your Private Certificate Authority (CA) in AWS Private CA

You'll start by creating your CA hierarchy within AWS Private CA. A best practice is to minimize the direct use of a root CA for issuing end-entity certificates and instead use intermediate/subordinate CAs for daily operations [22, 23].

1. **Sign up for AWS and Create an Administrative User (if not already done)**:
   - Sign up for an AWS account [12, 13].
   - Create an IAM user with administrative access and enable multi-factor authentication (MFA) for your root user. Avoid using the root user for daily tasks [24-27].
2. **Create a Private CA**:
   - You can create either a **Root CA** or a **Subordinate CA** [15, 28, 29].
     - **Root CA**: Establishes a new CA hierarchy and is backed by a self-signed certificate [29].
     - **Subordinate CA**: Must be signed by a parent CA higher in the hierarchy. AWS Private CA provides an automated signing process if the parent is also hosted by AWS Private CA [29-31]. If your parent CA is external (e.g., on-premises), you'll obtain a Certificate Signing Request (CSR) from AWS Private CA, get it signed by your external CA, and then import the signed certificate back into AWS Private CA [23, 30, 32-34].
   - When creating the CA, you'll specify its configuration, including the key algorithm (e.g., `RSA_2048`, `EC_prime256v1`), signing algorithm (e.g., `SHA256WITHRSA`, `SHA256WITHECDSA`), and X.500 subject information [35-38].
   - **Choose CA Mode**: You can select `General-purpose` (default, issues certificates with any validity period) or `Short-lived certificate` (maximum validity of seven days, often used without a revocation mechanism) [39-42].
   - **Configure Revocation (Recommended)**: AWS Private CA supports two fully managed mechanisms:
     - **Online Certificate Status Protocol (OCSP)**: Provides real-time certificate status. You can enable default OCSP support or provide a custom CNAME (FQDN) for branding, which requires a proxy server to forward traffic to AWS OCSP responder and a corresponding CNAME DNS record [43-51].
     - **Certificate Revocation Lists (CRLs)**: A file containing a list of revoked certificates [52]. If enabling CRLs, you'll need to specify an Amazon S3 bucket for storage. AWS Private CA will automatically deposit and update the CRL in the designated S3 bucket periodically [48, 53-57]. You can configure partitioned CRLs for larger scale or omit the CDP extension [58-62]. Ensure your S3 bucket has the correct IAM permissions for AWS Private CA to write to it, and be aware of S3 Block Public Access (BPA) settings which can cause issues if not configured correctly for public CRLs [54, 57, 63-67].
   - **Install the CA Certificate**: After creation, the CA will have a "Pending certificate" status [68].
     - For a **Root CA** hosted by AWS Private CA, you'll generate a CSR, and AWS Private CA will self-sign it using a root CA certificate template, then import it to activate the CA [69-72].
     - For a **Subordinate CA** hosted by AWS Private CA, you'll select a parent CA from your AWS Private CA account, and AWS Private CA will handle the CSR generation, signing by the parent, and import [30, 31, 73, 74].
     - For a **Subordinate CA signed by an external parent CA**, you'll obtain the CSR from AWS Private CA, submit it to your external signing authority, and then import the signed certificate and its chain into AWS Private CA [23, 33, 34, 75-80].
   - **Turn on AWS CloudTrail**: It's a best practice to enable CloudTrail logging before operating your private CA to monitor API calls and identify users/accounts [22, 81-83].

#### Step 2: Install Cert-manager in Your Kubernetes Cluster

cert-manager can be installed using Helm, `kubectl apply`, or the experimental `cmctl` command [84, 85]. Helm is a widely used and supported method for installation [21, 86, 87].

1. **Add the Helm Repository**:

   ```bash
   helm repo add jetstack https://charts.jetstack.io
   helm repo update
   ```

   [88]

2. **Install cert-manager**:

   ```bash
   helm install \
     cert-manager jetstack/cert-manager \
     --namespace cert-manager \
     --create-namespace \
     --version v1.12.0 # Use a supported version
   ```

   [21, 86, 87]

   *Note*: If you plan to use `csi-driver-spiffe` with cert-manager, it is **vital** to disable the default cert-manager approver during installation to prevent race conditions and ensure policy enforcement [89, 90]. For example, by adding `--set cert-manager.controllers='*, -certificaterequests-approver'` to your Helm install command [90].

#### Step 3: Configure `aws-privateca-issuer` and Its IAM Permissions

The `aws-privateca-issuer` plugin allows cert-manager to interact with your AWS Private CA. While specific installation manifests for `aws-privateca-issuer` are not in the provided sources, the general approach involves deploying its controller and then configuring a `ClusterIssuer` (or `Issuer`) resource that references your AWS Private CA. The most critical aspect is granting cert-manager the necessary permissions to interact with AWS Private CA.

The recommended and most secure method for cert-manager (and thus `aws-privateca-issuer`) to authenticate to AWS Private CA is using **IAM Roles for Service Accounts (IRSA)** if your Kubernetes cluster is EKS [91-93]. This avoids storing long-term AWS credentials in Kubernetes Secrets [94].

1. **Create an IAM OIDC Provider for your EKS Cluster**: This is a prerequisite for using IRSA [95, 96].
2. **Create an IAM Policy for AWS Private CA Access**: This policy grants the necessary `acm-pca` permissions. For example, `IssueCertificate`, `GetCertificate`, etc. [97-99].

   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Action": [
           "acm-pca:IssueCertificate",
           "acm-pca:GetCertificate",
           "acm-pca:DescribeCertificateAuthority",
           "acm-pca:GetCertificateAuthorityCertificate",
           "acm-pca:ListPermissions"
         ],
         "Resource": "arn:aws:acm-pca:<REGION>:<ACCOUNT_ID>:certificate-authority/<CA_ID>"
       }
     ]
   }
   ```

   *Note*: Replace `<REGION>`, `<ACCOUNT_ID>`, and `<CA_ID>` with your specific AWS details. For a broader policy (e.g., for all CAs in an account), you might use `*` for the `Resource` ARN, but least privilege is recommended [97].

3. **Create an IAM Role and Associate it with a Kubernetes Service Account**: This process involves creating a dedicated Kubernetes ServiceAccount and configuring an AWS IAM Role with the policy from the previous step. The Role is configured to be assumable only by clients with tokens for this specific ServiceAccount in your EKS cluster [92, 93, 95, 100].
   - This typically involves commands like `eksctl create iamserviceaccount` which performs multiple tasks: creating the ServiceAccount, configuring the IAM Role, and setting up the trust policy [95, 100].
4. **Grant Permission for cert-manager to Create ServiceAccount Tokens**: cert-manager needs permission to generate JWT tokens for the Kubernetes ServiceAccount created in the previous step [100, 101]. This is achieved by applying specific RBAC `Role` and `RoleBinding` resources in the `cert-manager` namespace [100, 101].
5. **Configure a `ClusterIssuer` (or `Issuer`) for AWS Private CA**: This `ClusterIssuer` will tell cert-manager to use your AWS Private CA for signing certificates. You'll specify the `aws-privateca-issuer` `kind` and reference the IAM role or credentials.

   An example `ClusterIssuer` for `aws-privateca-issuer` (conceptual, based on general issuer patterns and IRSA authentication):

   ```yaml
   apiVersion: cert-manager.io/v1
   kind: ClusterIssuer
   metadata:
     name: aws-privateca-issuer
   spec:
     # This assumes the aws-privateca-issuer controller is installed and listening for this group/kind
     awsPrivateCA:
       region: <AWS_REGION> # e.g., us-east-1
       certificateAuthorityArn: arn:aws:acm-pca:<REGION>:<ACCOUNT_ID>:certificate-authority/<CA_ID>
       # Use IRSA by referencing the service account created in Step 3.3
       serviceAccountName: <YOUR_CERT_MANAGER_SA_NAME> # e.g., cert-manager
       # You would typically annotate the cert-manager ServiceAccount
       # with the IAM role ARN for IRSA as described in Step 3.3
   ```

   *Note*: The exact specification for `awsPrivateCA` might vary depending on the plugin's API version. This is a conceptual example based on how cert-manager integrates with other AWS services.

#### Step 4: Create a Certificate Resource

Once your AWS Private CA is active and your cert-manager `ClusterIssuer` is configured, you can request certificates.

1. **Create a `Certificate` Resource**: This resource defines the desired X.509 certificate characteristics. When you create or update this resource, cert-manager will automatically create a `CertificateRequest` (and `Order` if it's an ACME issuer) and manage the issuance process [102, 103].

   ```yaml
   apiVersion: cert-manager.io/v1
   kind: Certificate
   metadata:
     name: my-private-app-certificate
     namespace: default
   spec:
     secretName: my-private-app-tls-secret
     issuerRef:
       name: aws-privateca-issuer
       kind: ClusterIssuer # or Issuer if namespaced
     commonName: myapp.internal
     dnsNames:
       - myapp.internal
       - another.myapp.internal
     # You may need to specify other fields based on your CA's policy,
     # like duration, usages, etc., that align with AWS Private CA templates.
   ```

   cert-manager will attempt to request this certificate from your configured `aws-privateca-issuer`, which in turn will interact with your AWS Private CA. The resulting private key and signed certificate will be stored in the Kubernetes Secret `my-private-app-tls-secret` [5].

### Key Considerations and Best Practices

- **Security for Private Keys**: With AWS Private CA, the private keys for your CAs are securely stored in AWS-managed hardware security modules (HSMs) that comply with FIPS PUB 140-2 Level 3 [22, 104]. This is a significant security benefit compared to managing keys yourself.
- **CA Hierarchy Design**: Carefully plan your CA hierarchy (root, subordinate CAs) with up to five levels to align with your organization's trust model [105]. Separate administration and issuer roles for better security [22, 106].
- **Certificate Templates**: AWS Private CA uses templates (e.g., `EndEntityCertificate/V1`, `SubordinateCACertificate_PathLen0/V1`) which encapsulate best practices for basic constraints [107, 108]. When using `aws-privateca-issuer`, ensure your `Certificate` resource requests align with the templates and policies defined in your AWS Private CA.
- **Automated Renewal**: cert-manager will ensure that certificates are valid and up-to-date, attempting to renew them at an appropriate time before expiry [6]. For certificates issued directly by AWS Private CA through `issue-certificate` CLI command or `IssueCertificate` API action, they are "unmanaged" by ACM and require manual renewal [109, 110]. However, if integrated with ACM, ACM can manage certificate issuance from Private CA and automate renewals [111, 112].
- **Compliance and Auditing**: AWS Private CA helps meet compliance requirements by integrating with AWS CloudTrail for API call logging [81, 83] and by allowing audit report generation for issued/revoked certificates [113-115].
- **`approver-policy`**: For production environments, the default cert-manager auto-approval of `CertificateRequests` is not recommended [116]. Consider using `approver-policy`, a cert-manager plugin, to define stricter approval rules based on policies [117, 118].
- **`csi-driver`**: For secretless provisioning of certificates unique to each Pod and facilitating mTLS, the `cert-manager csi-driver` can be used. It is explicitly recommended to use a private Certificate Authority (like AWS Private CA) for issuance with this driver, as public CAs have strict rate limits [119, 120].

Setting up AWS Private CA with cert-manager creates a robust and automated internal PKI solution within your Kubernetes environment, leveraging AWS's managed CA service for secure key management and compliance.

Would you like me to elaborate on any of these steps, such as a deeper dive into the IAM policy setup, or perhaps explore how to test the certificate issuance once everything is configured?
