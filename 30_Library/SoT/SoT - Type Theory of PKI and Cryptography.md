---
aliases: ["Cryptographic Types", "PKI as Logic", "Trust as Transformation"]
confidence: "5/5"
created: 2025-12-30
epistemic: "authoritative"
last_reviewed: "2025-12-30"
modified: 2025-12-30
purpose: "To define Public Key Infrastructure (PKI) through the lens of Type Theory and Data-Oriented Design, treating certificates as proofs and verification as type conversion."
review_interval: "6 months"
see_also: ["[[SoT - Parse, Don't Validate]]", "[[SoT - The Infrastructure Witness Pattern]]", "[[SoT - Digital Identity]]"]
source_of_truth: []
status: "stable"
tags: ["cryptography", "pki", "rust", "type_theory", "architecture"]
title: SoT - Type Theory of PKI and Cryptography
type: "SoT"
uid: 
updated: 
---

## 1. The Core Philosophy

In a Type Theory context, PKI is not a hierarchy of objects, but a system of **cryptographic proofs** and **type constraints**.

- **Immutable Data:** Certificates and Keys are immutable. They do not change state; they are generated, verified, or discarded.
- **Verification as Type Conversion:** The act of "verifying" a certificate is a transformation function. It consumes untrusted data and, if successful, produces a **Proof Type** (e.g., `VerifiedCertificate`).
- **Signatures as Predicates:** A digital signature is a predicate $P(m, k)$ asserting that message $m$ was processed by the holder of private key $k$.

---

## 2. Domain Data Structures (The Primitives)

We avoid "stringly typed" logic by using **NewTypes** to enforce semantic separation of identical underlying shapes (e.g., `u64`).

```rust
// Core NewTypes for Semantic Integrity
struct SerialNumber(u64);
struct DistinguishedName(String); // e.g., "CN=api.svc, O=Corp"
struct Signature(Vec<u8>);

// Algebraic Data Types for Algorithm Selection
enum Algorithm {
    RSA2048,
    ECDSA_P256,
}

// The Key Pair
struct PublicKey {
    algo: Algorithm,
    bytes: Vec<u8>,
}

// PrivateKey is a Capability handle (HSM/KMS)
struct PrivateKey {
    algo: Algorithm,
    handle: String, 
}
```

---

## 3. The Certificate Composition

A certificate binds identity data to a public key via a signature. It is a **Product Type** of the "To-Be-Signed" (TBS) data and the proof.

```rust
struct TbsCertificate {
    serial: SerialNumber,
    subject: DistinguishedName,
    issuer: DistinguishedName,
    public_key: PublicKey,
    validity: std::ops::Range<u64>,
}

struct Certificate {
    tbs_data: TbsCertificate,
    signature_algorithm: Algorithm,
    signature: Signature,
}
```

---

## 4. The Logic Pipeline (The Arrows)

We apply the **[[SoT - Parse, Don't Validate|Parse, Don't Validate]]** pattern to cryptographic operations.

### A. The Signing Transformation
Constructs a new `Certificate` from a `Csr` (Identity + PublicKey) and a `PrivateKey` (Capability).

```rust
fn issue_certificate(csr: Csr, ca_key: &PrivateKey, ca_cert: &Certificate) -> Certificate {
    // 1. Construct TBS Data
    // 2. Perform Crypto Sign (Side Effect)
    // 3. Construct Certificate Product
}
```

### B. The Verification Transformation (The Proof)
Transforms a raw `Certificate` into a `VerifiedCertificate`. This is the **Structure Discovery** phase of parsing.

```rust
// A marker type (Proof) that carries the verified identity
struct VerifiedCertificate<'a>(&'a Certificate);

fn verify<'a>(cert: &'a Certificate, trust_store: &TrustStore) -> Result<VerifiedCertificate<'a>, Error> {
    // 1. Perform Crypto Verification
    // 2. Check Chain of Trust
    // 3. If Valid: Return Type Proof
}
```

---

## 5. Trust Evaluation (The Environment)

The `TrustStore` acts as the **Context** or **Environment** ($\Gamma$) in type theory. It defines the axioms (Root CAs) accepted as true without further proof.

- **Trust Evaluation:** A function that reduces a sequence of certificates (The Chain) to a single `VerifiedCertificate` based on the Root Axioms in the `TrustStore`.

---

## 6. Revocation (The Oracle)

Revocation is a check against a dynamic exclusion set, representing the **temporal mutability** of trust.

- **CRL (Certificate Revocation List):** A `Set<SerialNumber>` of invalidated proofs.
- **OCSP (Online Certificate Status Protocol):** A query function `fn(SerialNumber) -> Status`.

---

## 7. Minimum Viable Understanding (MVU)

1.  **Trust is a Type:** You should not be able to use a certificate until it has been "parsed" into a `VerifiedCertificate` type.
2.  **Context is King:** Verification cannot happen in a vacuum; it requires a `TrustStore` (Environment).
3.  **Naming:** Use names that reflect the **guarantee** (`VerifiedCertificate`) or the **capability** (`SigningOracle`).
