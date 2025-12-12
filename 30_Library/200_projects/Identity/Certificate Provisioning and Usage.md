---
aliases: []
confidence: 
created: 2025-07-23T14:34:40Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:26Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: Certificate Provisioning and Usage
type:
uid: 
updated: 
version:
---

This document describes how TLS certificates are provisioned and managed within the Helm deployment, primarily for securing Ingress resources. The system leverages `cert-manager` to automate the entire lifecycle of certificates, from issuance to renewal.

## Overview

Certificate management is handled by [cert-manager](https://cert-manager.io/), a native Kubernetes certificate management controller. It is configured to automatically obtain certificates from [Let's Encrypt](https://letsencrypt.org/) using the DNS01 challenge method with Cloudflare as the DNS provider.

This approach allows for the issuance of wildcard certificates and avoids the need to expose services directly to the internet for HTTP01 challenges.

## Core Components

1. **`cert-manager` Helm Chart**:
   - The core `cert-manager` controller is deployed as an ArgoCD `Application` defined in `charts/ffnode/templates/cert-manager-application.yaml`.
   - This application is sourced from the official `jetstack/cert-manager` Helm chart.
   - Its deployment is controlled by the `deploy.certManager` flag in the `ffnode`'s `values.yaml`.

2. **`ClusterIssuer`**:
   - A single, cluster-wide issuer named `letsencrypt-prod` is defined in `charts/certs/templates/cluster-issuer.yaml`.
   - This issuer is configured to use the Let's Encrypt ACME server.
   - It uses the `dns01` solver, which proves domain ownership by creating temporary DNS records in Cloudflare.
   - The Cloudflare API token required for this process is sourced from a Kubernetes secret named `cloudflare-issuer-api-token`. This secret is typically populated from HashiCorp Vault, as seen in the `certManager.vaultSecrets` section of various `ffnode` values files (e.g., `ffnodes/fitfile/ff-test-a/values.yaml`).

3. **`fitfile-certificates` Chart (`charts/certs`)**:
   - This is a local utility chart that simplifies the creation of `Certificate` resources.
   - It iterates over a list of certificate specifications provided in the `values.yaml` and creates a corresponding `cert-manager.io/v1/Certificate` resource for each.
   - This chart is deployed as an ArgoCD `Application` via `charts/ffnode/templates/certificates-application.yaml`.

## Deployment Workflow

The process of provisioning a certificate for a service is as follows:

1. **Enable Certificate Management**: In an environment's `values.yaml` (e.g., `ffnodes/fitfile/ff-a/values.yaml`), the `deploy.certManager` flag is set to `true`.
2. **Deploy `cert-manager`**: ArgoCD syncs the `ffnode` chart, which first deploys the `cert-manager` application itself, setting up all the necessary CRDs and controllers in the `cert-manager` namespace.
3. **Deploy `fitfile-certificates`**: ArgoCD then syncs the `certificates` application. This applies our local `charts/certs` chart.
4. **Define Certificates**: The environment's `values.yaml` specifies the desired certificates under the `certs.certificates` key. Each entry includes a `name`, `namespace`, the `dnsNames` to be included in the certificate, and the `secretName` where the resulting TLS certificate and key will be stored.
5. **Issuance**:
   - The `fitfile-certificates` chart creates `Certificate` resources in the cluster based on the values.
   - The `cert-manager` controller detects these new `Certificate` resources.
   - It uses the `letsencrypt-prod` `ClusterIssuer` to begin the ACME challenge process with Let's Encrypt.
   - `cert-manager` securely communicates with Cloudflare's API to create the necessary DNS records to prove control over the domain.
   - Once the challenge is complete, Let's Encrypt issues the certificate.

6. **Store Secret**: `cert-manager` stores the issued certificate and its private key in the Kubernetes `Secret` specified by the `secretName` field (e.g., `cloudflare-tls`).
7. **Usage**: Application ingresses, such as the one for Argo Workflows (`argoWorkflows.server.ingress.tls`), are configured to use the generated secret to terminate TLS traffic.

## Certificate Authority and Production Readiness

### Certificate Authority

- **Primary CA**: The Certificate Authority (CA) used is **Let's Encrypt**, as defined by the `server` URL `https://acme-v02.api.letsencrypt.org/directory` in the `ClusterIssuer` (`charts/certs/templates/cluster-issuer.yaml`). This is a trusted, public CA.
- **Self-Signed Certificates**: In environments where `deploy.certManager` is set to `false` (e.g., `ffnodes/eoe/cuh-prod-1/values.yaml`), the system does **not** use Let's Encrypt. Ingress controllers in such cases typically fall back to using a default, self-signed certificate. These are **not secure for production** and will cause browser trust warnings.
- **No AWS ACM**: The configuration does not use AWS Certificate Manager (ACM) or any other cloud-provider-specific certificate services.

### Production Readiness Recommendations

The current setup using `cert-manager` with Let's Encrypt is a robust and common pattern for production. However, to further enhance its production readiness, consider the following:

1. **Implement a Staging Issuer**:
   - **Problem**: Let's Encrypt has strict [rate limits](https://letsencrypt.org/docs/rate-limits/) on its production API. Frequent deployments or misconfigurations during development can easily exhaust these limits, blocking the issuance of valid certificates.
   - **Solution**: Create a second `ClusterIssuer` that points to the Let's Encrypt staging server (`https://acme-staging-v02.api.letsencrypt.org/directory`). Use this staging issuer for all non-production environments. This allows for unlimited testing of the certificate issuance process without affecting production rate limits. Certificates from the staging server are not trusted by browsers, but they are perfect for validation and testing.

2. **Enhance Monitoring and Alerting**:
   - **Problem**: Certificate expiry or failed renewals can go unnoticed, leading to service outages.
   - **Solution**: Configure monitoring for `cert-manager`. It exposes Prometheus metrics that can be scraped to track certificate expiry dates, issuance successes, and failures. Set up alerts in Alertmanager (or a similar tool) to notify the team when certificates are nearing expiration or when issuance fails repeatedly.

3. **Backup Certificate Secrets**:
   - **Problem**: While `cert-manager` automates renewals, a cluster disaster could lead to the loss of the Kubernetes `Secrets` containing the TLS private keys and certificates.
   - **Solution**: Include these secrets in your regular Kubernetes backup and disaster recovery procedures. This ensures you can restore service quickly without needing to re-issue all certificates.

4. **Secure the ClusterIssuer Private Key**:
   - **Problem**: The `letsencrypt-cluster-issuer-key` secret contains the private key for your Let's Encrypt account. If compromised, it could be used to issue certificates for your domains maliciously.
   - **Solution**: Ensure that strict Kubernetes RBAC policies are in place to limit access to this secret, which is stored in the `cert-manager` namespace.

## Example Configuration

Here is an example from `ffnodes/fitfile/ff-test-a/values.yaml` showing how certificates are requested for multiple services in the `ff-test-a` environment. All certificates are stored in a single secret named `cloudflare-tls`, which can be shared across different namespaces.

```yaml
# In ffnodes/fitfile/ff-test-a/values.yaml
# Enable cert-manager deployment
deploy:
  certManager: true

# Configure the Cloudflare API token secret from Vault
certManager:
  vaultSecrets:
    - secretName: "cloudflare-issuer-api-token"
      vaultPath: "cloudflare"
      secretTransformation:
        excludes:
          - .*
        templates:
          api-token:
            text: '{{"{{`{{get .Secrets \"api_token\"}}`}}"}}'

# Define the list of certificates to be created
certs:
  certificates:
    - name: argocd
      namespace: argocd
      dnsNames: ["staging-argocd.fitfile.net"]
      secretName: cloudflare-tls
    - name: argo-workflows
      namespace: argo
      dnsNames: ["staging-argo-workflows.fitfile.net"]
      secretName: cloudflare-tls
    - name: fitfile-ff-test-a
      namespace: ff-test-a
      dnsNames: ["ff-test-a.fitfile.net"]
      secretName: cloudflare-tls
    - name: fitfile-ff-test-b
      namespace: ff-test-b
      dnsNames: ["ff-test-b.fitfile.net"]
      secretName: cloudflare-tls
    - name: fitfile-ff-test-c
      namespace: ff-test-c
      dnsNames: ["ff-test-c.fitfile.net"]
      secretName: cloudflare-tls
    - name: storybook
      namespace: storybook
      dnsNames: ["storybook.fitfile.net"]
      secretName: cloudflare-tls
```

To configure the cert-manager operator on a private AWS EKS cluster to use an AWS Private Certificate Authority (CA) for all certificate needs, you'll need to install and configure an external issuer called `aws-privateca-issuer`. This component acts as a bridge, enabling `cert-manager` to communicate with the AWS Private CA service.

The process involves installing the external issuer, granting it secure permissions to AWS using IAM Roles for Service Accounts (IRSA), and then creating a `ClusterIssuer` resource that points to your private CA.

---

### How It Works

The `aws-privateca-issuer` is an add-on for `cert-manager` that extends its functionality. When you create a `Certificate` resource and reference an `AWSPCAIssuer` or `AWSPCAClusterIssuer`, the following happens:

1. The main `cert-manager` controller creates a `CertificateRequest` resource.
2. The `aws-privateca-issuer` controller sees this request.
3. It securely authenticates with AWS using its assigned IAM role (via IRSA).
4. It sends the Certificate Signing Request (CSR) to your specified AWS Private CA. 1
5. AWS Private CA signs the request and returns a certificate. 2
6. The `aws-privateca-issuer` controller places the signed certificate back into the `CertificateRequest` resource.
7. The main `cert-manager` controller sees the completed request and saves the certificate and private key into a Kubernetes `Secret`.

---

### Prerequisites

- A running private AWS EKS cluster.
- `kubectl` and `helm` installed and configured to connect to your cluster.
- `cert-manager` already installed.
- An existing

  **AWS Private Certificate Authority**. 3 If you don't have one, you can create it in the AWS Console under

  **AWS Certificate Manager > Private CAs**.

- The AWS CLI configured with appropriate permissions.

---

### Step 1: Install the AWS Private CA Issuer

This external issuer is not included in the standard `cert-manager` installation and must be added separately.

1. **Add the Helm repository:**

   ```sh
   helm repo add awspca https://cert-manager.github.io/aws-privateca-issuer
   ```

2. Install the issuer controller:

   It's best practice to install it in its own namespace.

   ```sh
   helm install --create-namespace -n aws-privateca-issuer aws-privateca-issuer awspca/aws-privateca-issuer
   ```

---

### Step 2: Configure IAM Permissions with IRSA

To securely grant the issuer pod permissions to the AWS Private CA API, we'll use **IAM Roles for Service Accounts (IRSA)**. This method avoids the need for static AWS secret keys.

1. Create an IAM Policy:

   This policy defines the minimum permissions required. Save this as issuer-policy.json.

   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Action": [
           "acm-pca:DescribeCertificateAuthority",
           "acm-pca:GetCertificate",
           "acm-pca:IssueCertificate"
         ],
         "Resource": "*"
       }
     ]
   }
   ```

   Now, create the policy in AWS:

   ```sh
   aws iam create-policy \
       --policy-name AWSPrivateCAIssuerPolicyForCertManager \
       --policy-document file://issuer-policy.json
   ```

   Take note of the returned **Policy ARN**.

2. Create an IAM Role and Trust Policy:

   First, get your cluster's OIDC provider URL:

```sh
aws eks describe-cluster --name <YOUR_CLUSTER_NAME> --query "cluster.identity.oidc.issuer" --output text
```

    Next, create a trust policy file named `trust-policy.json`. This allows the Kubernetes Service Account used by the issuer to assume this IAM Role.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::<ACCOUNT_ID>:oidc-provider/<OIDC_PROVIDER_URL>"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "<OIDC_PROVIDER_URL>:sub": "system:serviceaccount:aws-privateca-issuer:aws-privateca-issuer"
        }
      }
    }
  ]
}
```

- Replace `<ACCOUNT_ID>` with your AWS Account ID.
- Replace `<OIDC_PROVIDER_URL>` with the output from the `aws eks describe-cluster` command, but **without** the `https://` prefix.

Now, create the IAM role and attach the policy:

```sh
# Create the IAM Role
aws iam create-role --role-name AWSPCAIssuerRoleForCertManager --assume-role-policy-document file://trust-policy.json

# Attach the permissions policy from the previous step
aws iam attach-role-policy --role-name AWSPCAIssuerRoleForCertManager --policy-arn <POLICY_ARN_FROM_STEP_1>
```

Take note of the returned **Role ARN**.

3. Annotate the Kubernetes Service Account:

   The Helm chart has already created a Service Account. You just need to link it to the IAM Role by adding an annotation.

```sh
kubectl annotate serviceaccount aws-privateca-issuer \
  -n aws-privateca-issuer \
  "eks.amazonaws.com/role-arn=arn:aws:iam::<ACCOUNT_ID>:role/AWSPCAIssuerRoleForCertManager"
```

Restart the issuer pod to ensure it picks up the new credentials:

```sh
kubectl rollout restart deployment -n aws-privateca-issuer aws-privateca-issuer
```

---

### Step 3: Create the AWSPCAClusterIssuer

To make your private CA available for `Certificate` resources in any namespace, you'll create an `AWSPCAClusterIssuer`. This resource tells `cert-manager` how to connect to your specific AWS Private CA.

Create a file named `awspca-cluster-issuer.yaml`:

```yaml
apiVersion: awspca.cert-manager.io/v1beta1
kind: AWSPCAClusterIssuer
metadata:
  name: "aws-private-ca"
spec:
  # The ARN of your AWS Private Certificate Authority
  arn: "arn:aws:acm-pca:eu-west-1:123456789012:certificate-authority/12345678-1234-1234-1234-123456789012"
  # The AWS region your Private CA is in
  region: "eu-west-1"
```

Replace the `arn` and `region` with your specific values and apply it:

```sh
kubectl apply -f awspca-cluster-issuer.yaml
```

Verify the issuer is ready:

Bash

```sh
kubectl describe awspcaclusterissuer aws-private-ca
# Look for a condition with Type=Ready and Status=True
```

---

### Step 4: Request a Certificate (Example)

With the issuer configured, you can now request a certificate for any application in your cluster.

1. Create a `Certificate` resource referencing your new `AWSPCAClusterIssuer`.

```yaml
# my-app-certificate.yaml
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: my-app-tls
  namespace: my-app
spec:
  secretName: my-app-tls-secret
  dnsNames:
    - my-app.internal.mydomain.com
  issuerRef:
    # The name of the issuer created in the previous step
    name: "aws-private-ca"
    # Must be AWSPCAClusterIssuer to use the cluster-scoped issuer
    kind: AWSPCAClusterIssuer
    # The API group for the AWS Private CA issuer
    group: awspca.cert-manager.io
```

2. Apply this manifest:

```sh
kubectl apply -f my-app-certificate.yaml
```

`cert-manager` will now process this request, and a Kubernetes `Secret` named **my-app-tls-secret** will be created in the **my-app** namespace. This secret will contain the signed certificate and private key, ready to be used by your application pods. ✅

Public Key Infrastructure (PKI) is a comprehensive system designed to enable secure communication between parties who have never met by relying on trusted third parties to issue and manage digital certificates. The components of a PKI span fundamental cryptographic elements, the entities involved in the infrastructure, the mechanisms for its operation, and specific software tools that implement PKI principles.

Here's a breakdown of these components based on your provided materials:

### 1. Core Cryptographic Building Blocks

At its foundation, PKI relies on various cryptographic primitives and protocols, which are essentially the "building blocks" of secure communication.

- **Cryptographic Primitives/Algorithms**: These are individual functions designed for specific security functionalities:
  - **Symmetric Algorithms**: While not directly part of public-key cryptography, symmetric ciphers are widely used for data encryption and integrity checks of messages in secure systems. Examples include the Advanced Encryption Standard (AES) and the Data Encryption Standard (DES). Modern systems often combine symmetric and asymmetric algorithms in "hybrid schemes" due to their respective strengths and weaknesses.
  - **Asymmetric (Public-Key) Algorithms**: These were introduced in 1976 and are fundamental to PKI. They involve a pair of keys: a secret key and a public key. Public-key algorithms are crucial for applications like digital signatures, key establishment, and data encryption, although they are generally slower and computationally more intensive than symmetric ciphers. Important examples include:
    - **RSA**: Currently the most widely used asymmetric cryptographic scheme, though elliptic curves and discrete logarithm schemes are gaining ground.
    - **Diffie–Hellman Key Exchange (DHKE)**: The first asymmetric scheme published in open literature, providing a practical solution for establishing secret keys over an insecure channel.
    - **Elgamal Encryption Scheme**: Another public-key cryptosystem based on the discrete logarithm problem.
    - **Elliptic Curve Cryptosystems (ECC)**: Offer similar functions to RSA and DHKE but can provide comparable security with shorter key lengths.
  - **Hash Functions**: These compute a fixed-length "message digest" or "fingerprint" of a message without a key. They are essential for digital signature schemes and Message Authentication Codes (MACs). SHA-1 is an example of a Secure Hash Algorithm.
- **Cryptographic Protocols**: These combine primitives to achieve complex security objectives:
  - **Key Establishment Protocols**: Mechanisms like Diffie–Hellman key exchange and RSA key transport protocols are used to establish shared secret keys over insecure channels. TLS 1.3, for instance, uses a "key schedule" based on the HMAC-based key derivation function (HKDF) to generate various encryption keys securely during a connection handshake.
  - **Digital Signature Schemes**: Provide nonrepudiation and message integrity, ensuring the origin and integrity of data. Examples include RSA, Elgamal, Digital Signature Algorithm (DSA), and Elliptic Curve Digital Signature Algorithm (ECDSA).
  - **Message Authentication Codes (MACs)**: Used to ensure message integrity and authentication. HMAC (from hash functions) and CBC-MAC (from block ciphers) are examples.

### 2. PKI Entities and Infrastructure Elements

The PKI ecosystem comprises specific roles and structural components that facilitate trust and security:

- **Certification Authorities (CAs)**: These are trusted third parties responsible for issuing digital certificates that confirm the identities of subscribers.
  - **Root CAs**: The top of the trust hierarchy, whose self-signed certificates are universally trusted and form the basis of a trust store. AWS Private CA allows users to create and manage root CAs. The private keys for these CAs are securely stored in FIPS PUB 140-2 Level 3 compliant Hardware Security Modules (HSMs).
  - **Subordinate/Intermediate CAs**: Issued by a root CA or another intermediate CA, these CAs issue certificates to end-entities. They can be configured with "path length constraints" to limit the depth of the certification path beneath them.
- **Relying Parties**: These are the consumers of certificates, such as web browsers, operating systems, and other applications, which validate certificates by verifying their chain of trust back to a trusted root CA in their "trust store".
- **Subscribers**: The end-users, servers, or devices that request and use certificates to establish their identity or encrypt communications.
- **Certificates**: Digital documents that bind a public key to an identity, signed by a CA. They contain various fields and extensions. Types include TLS server certificates, end-entity certificates, and self-signed certificates. Important extensions include:
  - **Basic Constraints**: Identifies if a certificate belongs to a CA and its path length.
  - **Authority Information Access (AIA)**: Specifies how to access additional information or services from the issuing CA, like OCSP responders or the issuer's certificate.
  - **Subject Alternative Name (SAN)**: Replaces the traditional Subject field to support multiple identities (e.g., DNS names, IP addresses).
  - **Subject Key Identifier (SKI) and Authority Key Identifier (AKI)**: Used to uniquely identify subjects and authorities, aiding in certificate path building.
- **Certificate Revocation Lists (CRLs)**: Lists of certificates that have been revoked before their expiry date.
- **Online Certificate Status Protocol (OCSP) Responders**: Provide real-time status (valid or revoked) of a certificate. "OCSP stapling" allows servers to include revocation information directly in the TLS handshake, improving performance and privacy.
- **Certificate Transparency (CT) Logs**: Public, verifiable logs where CAs submit issued certificates, enabling monitoring and detection of mis-issuances.

### 3. PKI Operational Mechanisms and Protocols

These describe how PKI functions to provide security services:

- **Key Establishment**: The process of securely establishing a shared secret between two or more parties. Public-key methods like Diffie-Hellman are key for this.
- **Certificate Lifecycle Automation**: Standards like Automated Certificate Management Environment (ACME) streamline the process of obtaining and renewing certificates.
- **Authentication**: PKI provides authentication by relying on public key cryptography and certificates. For instance, in TLS, the client verifies the server's identity using its public key derived from a validated certificate.
- **Certificate Validation**: Relying parties construct a chain of trust from an end-entity certificate through intermediate CAs up to a trusted root CA to verify its authenticity and validity.

### 4. Software/Tooling Components

Modern PKI deployments often leverage specialized software components and tools to manage and automate the complex processes:

- **cert-manager Components**: This is a Kubernetes add-on that automates the management and issuance of TLS certificates within Kubernetes or OpenShift clusters. Its core components, often running as Docker images in containers, include:
  - **Controller**: The primary component that processes and reconciles `cert-manager`'s custom resources and other Kubernetes resources.
  - **Webhook**: Provides API validation, mutation, and conversion functionality for `cert-manager`'s Custom Resources.
  - **cainjector**: A unique component designed to inject CA (Certificate Authority) data from various sources (Kubernetes Secrets, `cert-manager` Certificates, or the Kubernetes API server CA certificate) into "injectable" resources like ValidatingWebhookConfiguration, MutatingWebhookConfiguration, and CustomResourceDefinition. This is critical for propagating trust within the cluster.
  - **acmesolver**: A component deployed by the `cert-manager` controller to handle ACME (Automated Certificate Management Environment) HTTP01 challenges, which are used to prove domain ownership for certificate issuance.
  - **Issuers and ClusterIssuers**: These are `cert-manager`'s custom resources that define *how* TLS certificates will be requested and signed. Issuers are namespace-specific, while ClusterIssuers operate cluster-wide. `cert-manager` supports various built-in and external issuer types, including ACME, Venafi TLS Protect, HashiCorp Vault, CA (for private PKI), and Self-Signed issuers.
  - **Certificate Resource**: A Custom Resource that defines the desired state of a TLS certificate, typically resulting in a private key and certificate being stored in a Kubernetes Secret.
  - **CertificateRequest Resource**: Represents a Certificate Signing Request (CSR) that `cert-manager` uses to interact with an issuer.
- **cert-manager Satellite Projects**: These extend `cert-manager`'s core functionality:
  - **csi-driver** and **csi-driver-spiffe**: Container Storage Interface (CSI) driver plugins for Kubernetes that seamlessly request and mount certificate key pairs directly to application pods. `csi-driver-spiffe` specifically delivers SPIFFE SVIDs (X certificate key pairs).
  - **trust-manager**: Simplifies the management and distribution of TLS trust bundles across Kubernetes and OpenShift clusters. It can source certificates from ConfigMaps, Secrets, or directly specified strings.
- **AWS Private Certificate Authority (Private CA)**: This is a cloud service that provides managed infrastructure for creating and managing private CA hierarchies (root and subordinate CAs) without the overhead of on-premise operations.
  - **AWS Private CA Connectors**: These components integrate AWS Private CA with other systems:
    - **Connector for Kubernetes**: An EKS Add-on for seamless integration with Kubernetes clusters.
    - **Connector for Active Directory**: Provides support for issuing certificates to Active Directory environments.
    - **Connector for SCEP (Simple Certificate Enrollment Protocol)**: Enables distribution of digital identity certificates to mobile devices and networking equipment using the SCEP protocol.
  - **Templates**: AWS Private CA uses predefined templates (e.g., `EndEntityCertificate/V1`, `OCSPSigningCertificate/V1`) to specify the X extensions and fields for certificates during issuance.

In summary, the components of PKI range from the foundational mathematical algorithms that underpin cryptographic security to the complex organizational structures of Certification Authorities, and finally to the sophisticated software tools like `cert-manager` and AWS Private CA that enable their practical deployment and management in modern computing environments. Each component plays a vital role in establishing and maintaining trust in digital communications.
