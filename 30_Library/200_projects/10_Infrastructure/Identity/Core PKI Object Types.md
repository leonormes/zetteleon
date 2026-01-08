---
aliases: []
confidence: ""
created: 2025-10-18T14:25:33+01:00
epistemic: ""
last_reviewed: ""
modified: 2026-01-08T10:49:54+00:00
purpose: ""
review_interval: ""
see_also: []
source_of_truth: []
status: ""
tags: []
title: Core PKI Object Types
type: ""
---

## Conceptual Framework: PKI as Type Verification

In a Type Theory context, Public Key Infrastructure (PKI) is not merely a hierarchy of objects, but a system of **cryptographic proofs** and **type constraints**.

- **Data Immutable:** Certificates and Keys are immutable data structures. They do not have internal state changes; they are created, verified, or discarded.
- **Verification as Type Conversion:** The act of "verifying" a certificate is a transformation function. It takes a `RawCertificate` (untrusted data) and a `TrustStore` (context) and, if successful, returns a `VerifiedCertificate` (a distinct type). This prevents the "use of unverified data" class of errors at the compiler level.
- **Signatures as Predicates:** A digital signature is a predicate  that asserts the message  was processed by the holder of.

---

## 1. Core Data Structures (The Primitive Types)

We define the domain using strictly typed `structs`. We avoid "stringly typed" logic by using newtypes for distinct semantic concepts (e.g., a `SerialNumber` is not just a `u64`).

```rust
// Core Newtypes for Type Safety
struct SerialNumber(u64);
struct DistinguishedName(String); // e.g., "CN=api.svc, O=Corp"
struct Signature(Vec<u8>);

// Algebraic Data Types for Algorithms
enum Algorithm {
    RSA2048,
    ECDSA_P256,
}

// The Key Pair
struct PublicKey {
    algo: Algorithm,
    bytes: Vec<u8>,
}

// PrivateKey is usually kept in a separate memory space or HSM handle
struct PrivateKey {
    algo: Algorithm,
    // In reality, this might be a handle to a KMS/HSM
    bytes: Vec<u8>, 
}

```

---

## 2. The Certificate Composition

A Certificate is a composite type containing the Data (TBS - To Be Signed) and the Proof (Signature).

```rust
struct TbsCertificate {
    serial: SerialNumber,
    subject: DistinguishedName,
    issuer: DistinguishedName,
    public_key: PublicKey,
    validity: std::ops::Range<u64>, // Epoch timestamp range
    extensions: Vec<u8>, // SAN, Constraints, etc.
}

// The Signed Object
struct Certificate {
    tbs_data: TbsCertificate,
    signature_algorithm: Algorithm,
    signature: Signature,
}

```

## 3. Transformations and Operations (Functional Logic)

Instead of methods mutating state on an object (OOP), we use pure functions representing cryptographic operations.

### The Signing Transformation

```rust
fn sign(data: &[u8], key: &PrivateKey) -> Result<Signature, CryptoError> {
    // Implementation of RSA/ECDSA signing
    todo!()
}

fn issue_certificate(csr: Csr, ca_key: &PrivateKey, ca_cert: &Certificate) -> Certificate {
    let tbs = TbsCertificate {
        serial: generate_serial(),
        subject: csr.subject,
        issuer: ca_cert.tbs_data.subject.clone(),
        public_key: csr.public_key,
        validity: validity_window(),
        extensions: default_extensions(),
    };
    
    let signature = sign(&tbs.encode(), ca_key).expect("Signing failed");
    
    Certificate {
        tbs_data: tbs,
        signature_algorithm: ca_key.algo,
        signature,
    }
}

```

### The Verification Transformation

This utilizes the **Parse, don't validate** pattern. We do not just return a boolean; we return a semantic type that carries the proof of validity.

```rust
// A marker type indicating a certificate has passed crypto verification
struct VerifiedCertificate<'a>(&'a Certificate);

fn verify_signature<'a>(
    target: &'a Certificate, 
    issuer_key: &PublicKey
) -> Result<VerifiedCertificate<'a>, ValidationError> {
    
    let valid = crypto_verify(
        &target.tbs_data.encode(), 
        &target.signature, 
        issuer_key
    );

    if valid {
        Ok(VerifiedCertificate(target))
    } else {
        Err(ValidationError::InvalidSignature)
    }
}

```

---

## 4. Trust Evaluation (The TrustStore)

The `TrustStore` acts as the evaluation context or the "Environment" in type theory. It defines the axioms (Root CAs) accepted as true without proof.

```rust
struct TrustStore {
    roots: Vec<Certificate>, // Self-signed trust anchors
}

impl TrustStore {
    // Evaluation function: Reduces a chain of certs to a boolean trust decision
    fn evaluate_trust(&self, leaf: &Certificate, chain: &[Certificate]) -> bool {
        // 1. Find root in store that signed the last cert in the chain
        // 2. Iteratively verify_signature() down the chain
        // 3. Verify leaf.validity against current time
        // 4. Verify revocation status (CRL/OCSP)
        todo!()
    }
}

```

---

## 5. Revocation State (Oracles)

Revocation is a check against a dynamic exclusion set. This represents the mutability of trust over time.

- **CRL:** A `Set<SerialNumber>` representing invalidated proofs.
- **OCSP:** A function query `fn(SerialNumber) -> Status`.

```rust
enum CertStatus {
    Good,
    Revoked { date: u64 },
    Unknown,
}

trait RevocationOracle {
    fn check_status(&self, serial: SerialNumber) -> CertStatus;
}

```

---

## 6. Architecture Scenario: Kubernetes mTLS

We re-map the "HTTPS Trust between Clusters" scenario as a data distribution and verification pipeline.

### A. The Bootstrapping Phase (Axiom Distribution)

- **Input:** `RootCA_Certificate` (The Axiom).
- **Process:** Out-of-band distribution to Cluster A and Cluster B.
- **State Change:** `ClusterA.TrustStore` and `ClusterB.TrustStore` are mutated to include `RootCA`.

### B. The Issuance Pipeline (Data Factory)

This flow represents the **AWS Private CA + cert-manager** integration.

1. **Source (Pod):** Generates `(PrivateKey, PublicKey)`. Emits `CSR` (Data).
2. **Controller (cert-manager):** Observes `CSR`. Transmits to Issuer.
3. **Oracle (AWS Private CA):** Maps `(CSR, CA_Context)`  `Certificate`.
4. **Sink (Kubernetes Secret):** Stores the pair `(Certificate, PrivateKey)`.

### C. The Runtime Handshake (Proof Exchange)

The TLS handshake is a bidirectional exchange of serialised data structures to establish a shared session key.

| Step | Data Flow | Type constraint Check |
| --- | --- | --- |
| **1** | Client  Server: `ClientHello` | Protocol negotiation. |
| **2** | Server  Client: `[ServerCert, IntermediateCert]` | **Proof Presentation.** |
| **3** | Client internal logic | `verify_signature(ServerCert, IntermediateKey)` <br>

`verify_signature(IntermediateCert, RootKey)` <br>

<br> `TrustStore.contains(RootKey)` |

| **4** | **Result** | If `Ok(VerifiedCertificate)`, derivation of session keys proceeds. |

## Summary Matrix

| OOP Concept | Data-Oriented/Rust Equivalent |
| --- | --- |
| **Class** (`Certificate`) | **Struct** (`struct Certificate`) - Pure Data |
| **Method** (`verify()`) | **Function** (`fn verify() -> Result`) |
| **Inheritance** | **Composition** (Chains are `Vec<Certificate>`) |
| **Identity** (Instance) | **Value Semantics** (Equality by content) |
| **Trust** | **Context** (`TrustStore` passed into functions) |

Here are the specific `cert-manager` manifests to implement the **Issuance Pipeline** (Data Factory) we discussed.

I have annotated these manifests to map the YAML fields back to our **Type Theory** and **Rust** definitions, highlighting how the abstract data structures map to the concrete configuration.

## 1. The Oracle Definition (The Issuer)

In our model, the `Issuer` is the interface to the external signing oracle (AWS Private CA). It defines the `Sign` function scope.

**Type Mapping:**

- **Role:** `SigningOracle`
- **Rust Equivalent:** `struct AwsPcaClient { arn: String, region: Region }`

```yaml
# This Custom Resource Definition (CRD) represents the bound context 
# for the signing operation.
apiVersion: awspca.cert-manager.io/v1beta1
kind: AWSPCAClusterIssuer
metadata:
  name: aws-pca-root
spec:
  # The unique identifier for the remote signing oracle.
  # Maps to the 'Authority' that holds the PrivateKey.
  arn: arn:aws:acm-pca:eu-west-2:123456789012:certificate-authority/uuid
  
  # The physical location of the oracle.
  region: eu-west-2
  
  # The authentication context (IRSA).
  # This provides the capability proof to invoke the 'Sign' function.
  secretRef:
    name: awspca-issuer-creds
    namespace: cert-manager

```

## 2. The Type Request (The Certificate)

This resource represents the `Csr` (Certificate Signing Request) constructor. It defines the constraints and shape of the desired output type (`VerifiedCertificate`).

**Type Mapping:**

- **Role:** `TypeConstructor` & `Sink`
- **Rust Equivalent:** `fn request_cert(subject: Dn, dns: Vec<String>) -> (Certificate, PrivateKey)`

```yaml
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: payment-service-cert
  namespace: payments
spec:
  # -----------------------------------------------------------
  # 1. THE SINK (Output Location)
  # Where the resulting tuple (Certificate, PrivateKey) is stored.
  # Rust: let output: Secret = ...
  # -----------------------------------------------------------
  secretName: payment-service-tls
  
  # -----------------------------------------------------------
  # 2. THE SUBJECT (Identity Data)
  # The immutable identity fields bound to the Public Key.
  # Rust: struct DistinguishedName { ... }
  # -----------------------------------------------------------
  commonName: payment-service.payments.svc.cluster.local
  dnsNames:
    - payment-service.payments.svc
    - localhost
  
  # -----------------------------------------------------------
  # 3. THE FUNCTION POINTER (Issuer Reference)
  # Explicitly selects which implementation of 'Sign' to use.
  # Rust: trait Signer = AwsPcaClient
  # -----------------------------------------------------------
  issuerRef:
    group: awspca.cert-manager.io
    kind: AWSPCAClusterIssuer
    name: aws-pca-root

  # -----------------------------------------------------------
  # 4. TYPE CONSTRAINTS (Key Configuration)
  # Defines the cryptographic primitives for the generated key pair.
  # Rust: enum Algorithm { RSA2048, ... }
  # -----------------------------------------------------------
  privateKey:
    algorithm: RSA
    encoding: PKCS1
    size: 2048
    
  # -----------------------------------------------------------
  # 5. LIFETIME PARAMETERS
  # Defines the validity window logic.
  # Rust: validity: Duration
  # -----------------------------------------------------------
  duration: 2160h # 90 days
  renewBefore: 360h # 15 days

```

## 3. The Runtime Implementation (Under the Hood)

When you apply these manifests, the system executes the logical flow described in the `Core PKI Object Types.md` "Issuance" section:

1. **Instantiation:** `cert-manager` observes the `Certificate` resource and instantiates a `CertificateRequest` (an internal intermediate type).
2. **Key Generation:** It generates a strictly typed `PrivateKey` and `PublicKey` pair in memory.
3. **Transformation:** It transforms the `PublicKey` + `Subject` into a standard PEM-encoded CSR.
4. **Remote Procedure Call:** It invokes the `issueCertificate` method on the AWS Private CA (referenced by the `AWSPCAClusterIssuer`).
5. **Persisting State:** It retrieves the signed `Certificate` blob and atomic writes the `(Certificate, PrivateKey)` tuple to the Kubernetes Secret defined in `secretName`.

**Next Step:** Would you like to see the Terraform configuration required to provision the underlying IAM Roles (IRSA) that allow this `AWSPCAClusterIssuer` to authenticate with AWS?
Here is the Terraform configuration to provision the Identity Witness (IAM Role) required for the AWSPCAClusterIssuer.
Conceptual Framework: Capability & Witness
In our Type Theory model, the AWSPCAClusterIssuer requires a Capability (permission) to execute the Sign function on the AWS Private CA.
 - The Capability (IAM Role): A bounded context defining what functions can be called (IssueCertificate).
 - The Witness (OIDC Token): A cryptographically verifiable token presented by the Kubernetes Pod. The AWS IAM STS (Security Token Service) verifies this token against the OIDC provider (the "Trust Anchor") to dispense temporary credentials.
Terraform Configuration
This code creates the Capability and defines the Trust Relationship that allows the cert-manager Service Account to assume it.
1. The Permissions (The Functional Scope)
This policy defines the strictly typed set of allowed operations on the Oracle (Private CA).
variable "acm_pca_arn" {
  description = "The ARN of the AWS Private CA (The Oracle)"
  type        = string
}

resource "aws_iam_policy" "pca_issuer_policy" {

  name        = "AWSPCAIssuerPolicy"

  description = "Defines the Sign and Read capabilities for the CA Oracle"

  policy = jsonencode({

    Version = "2012-10-17"

    Statement = [

      {

        Effect = "Allow"

        # The allowed methods on the Oracle

        Action = [

          "acm-pca:DescribeCertificateAuthority",

          "acm-pca:GetCertificate",

          "acm-pca:IssueCertificate",

          "acm-pca:GetCertificateAuthorityCertificate",

          "acm-pca:ListPermissions"

        ]

        # The specific instance of the Oracle this policy binds to

        Resource = var.acm_pca_arn

      }

    ]

  })

}

2. The Trust Relationship (The Identity Verification)
This defines the predicate: "If the caller presents a valid OIDC token signed by the EKS Cluster for the subject cert-manager:aws-pca-issuer, then return the Credentials."
variable "eks_oidc_provider_arn" {
  description = "The ARN of the EKS OIDC Provider (The Identity Trust Anchor)"
  type        = string
}

variable "eks_oidc_provider_url" {

  description = "The URL of the EKS OIDC Provider (stripped of https://)"

  type        = string

}

data "aws_iam_policy_document" "pca_issuer_trust" {

  statement {

    actions = ["sts:AssumeRoleWithWebIdentity"]

    effect  = "Allow"

    principals {
      type        = "Federated"
      identifiers = [var.eks_oidc_provider_arn]
    }

    condition {
      test     = "StringEquals"
      # The assertion: verify the token's 'sub' (Subject) claim
      variable = "${var.eks_oidc_provider_url}:sub"
      # Format: system:serviceaccount:<namespace>:<service-account-name>
      values   = ["system:serviceaccount:cert-manager:aws-pca-issuer"]
    }

  }

}

resource "aws_iam_role" "pca_issuer_role" {

  name               = "AWSPCAIssuerRole"

  assume_role_policy = data.aws_iam_policy_document.pca_issuer_trust.json

}

resource "aws_iam_role_policy_attachment" "attach_pca" {

  role       = aws_iam_role.pca_issuer_role.name

  policy_arn = aws_iam_policy.pca_issuer_policy.arn

}

3. The Kubernetes Binding (The Link)
Finally, you must explicitly link the Service Account in Kubernetes to this IAM Role using an annotation. This injects the ARN into the Pod environment, triggering the AWS SDK to perform the OIDC exchange.
apiVersion: v1
kind: ServiceAccount
metadata:
  name: aws-pca-issuer
  namespace: cert-manager
  annotations:

## The Pointer to the Capability

    eks.amazonaws.com/role-arn: "arn:aws:iam::123456789012:role/AWSPCAIssuerRole"

Next Step: Would you like to review the validation logic (the "Verification Transformation") to test that a certificate issued by this pipeline is correctly trusted by a client pod?
