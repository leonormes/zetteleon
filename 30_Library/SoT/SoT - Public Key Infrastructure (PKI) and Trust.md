---
aliases: ["PKI Architecture", "Certificate Authority Trust Model", "Digital Certificates", "X.509 Trust"]
confidence: "5/5"
created: 2025-12-30T11:43:52+00:00
epistemic: "architecture"
last_reviewed: "2025-12-30"
modified: 2025-12-30T11:54:51+00:00
purpose: "To define the data-centric architecture of Public Key Infrastructure (PKI), framing Trust as a verifiable chain of cryptographic proofs rather than abstract faith."
review_interval: "12 months"
see_also: ["[[SoT - The Data Architecture of TLS 1.3]]", "[[SoT - The Infrastructure Witness Pattern]]", "[[SoT - Cryptography and Encryption]]", "[[SoT - Modern Authentication Standards]]"]
source_of_truth: []
status: "stable"
tags: ["SoftwareEngineering/Security", "pki", "cryptography", "SoftwareEngineering/Architecture", "trust"]
title: SoT - Public Key Infrastructure (PKI) and Trust
type: "SoT"
uid: 
updated: 
---

## 1. Core Concept: Trust as Data

> [!definition] Public Key Infrastructure (PKI)
> PKI is not just technology; it is the **Governance Framework** (Policies + Software) that binds a **Public Key** to an **Identity** via a **Digital Signature** from a Trusted Third Party (Certificate Authority).

From a data-centric perspective, "Trust" is not an abstract sentiment. It is the result of a **Verification Algorithm** traversing a chain of digital signatures until it reaches a locally stored **Root of Trust**.

---

## 2. The Data Structure: The Digital Certificate

A Certificate (X.509) is a **Witness Object** (see [[SoT - The Infrastructure Witness Pattern]]). It serves as a cryptographic proof that a specific Public Key belongs to a specific Identity.

**The Trinity of the Certificate:**
1. **Identity Data:** Who is this? (CN, SAN, Organization).
2. **Public Key Data:** How do we talk securely? (RSA/ECC Public Key).
3. **The Seal (Witness):** The CA's Digital Signature validating the link between 1 and 2.

### The Verification Logic

To trust a certificate, the client performs a rigorous check:

1. **Cryptographic Integrity:** Does `Verify(Cert.Body, Cert.Signature, CA.PublicKey) == True`?
2. **Temporal Validity:** Is `Now()` between `NotBefore` and `NotAfter`?
3. **Revocation Status:** Is the Serial Number absent from CRLs/OCSP?
4. **Identity Match:** Does `Cert.SAN` match the intended `Hostname`?

---

## 3. The Trust Hierarchy (Chain of Trust)

Trust is hierarchical. A client does not trust the server directly; it trusts the **Root CA** that signed the **Intermediate CA** that signed the **Server Certificate**.

1. **Root CA:** Self-signed. The "God Key." Trusted implicitly because it is hard-coded in the OS/Browser Trust Store. Offline and heavily guarded.
2. **Intermediate CA:** Signed by Root. Used for day-to-day issuance to protect the Root key.
3. **Leaf Certificate:** Signed by Intermediate. Installed on the Server. Cannot sign other certificates.

> **The Chain:** `Root -> Intermediate -> Leaf`. The client walks this path backwards from Leaf to Root.

---

## 4. Threat Model: The "God Key" Compromise

If a CA's private key is stolen, the attacker creates a **Golden Key** scenario.

- **The Power:** The attacker can issue valid, trusted certificates for *any* domain (Google, Your Bank, Military).
- **The Mechanism:** The browser sees a mathematically valid signature from a trusted Root and accepts the connection.
- **The Consequence:** Undetectable Man-in-the-Middle (MitM) attacks.

### Mitigations (The Defense Layers)

1. **Certificate Transparency (CT):** A public, append-only log of all issued certificates. If a CA issues a cert, it *must* log it. This makes covert issuance impossible; the world will see the fake cert immediately.
2. **Pinning (HPKP/Certificate Pinning):** Hard-coding the expected Public Key in the application (mostly deprecated for web, used in mobile apps).
3. **CAA Records:** DNS records explicitly authorizing which CAs can sign for a domain.
4. **OCSP Stapling:** The server proves its cert is fresh (not revoked) by delivering a recent, signed timestamp from the CA during the handshake.

---

## 6. Automation & Issuance (ACME)

The **Automated Certificate Management Environment (ACME)** protocol (used by Let's Encrypt) automates the "Proof of Ownership" required to get a certificate.

### The Challenge Mechanism
To get a cert for `example.com`, the CA challenges the requester to prove control over the domain.

*   **HTTP-01 Challenge:**
    *   **Mechanism:** CA says "Put this token at `http://example.com/.well-known/acme-challenge/token`".
    *   **Validation:** CA makes an HTTP request to that URL.
    *   **Constraint:** Requires port 80 to be open and public DNS to point to the server.
*   **DNS-01 Challenge:**
    *   **Mechanism:** CA says "Put this token in a TXT record at `_acme-challenge.example.com`".
    *   **Validation:** CA queries DNS.
    *   **Benefit:** Supports **Wildcards** (`*.example.com`) and private servers (no incoming HTTP needed).

## 7. Private CAs & Internal Trust

For internal services (e.g., `privatelink` URLs), you cannot use public CAs. You act as your own CA.

### The Private Architecture
1.  **Issuance:** An internal CA (e.g., AWS Private CA, Vault) signs the certs.
2.  **The Trust Gap:** Standard browsers/OSs do *not* trust your internal Root CA by default. They will show "Security Warning."
3.  **The Fix (Distribution):** You must distribute your Root CA public certificate to every client's Trust Store.
    *   *Linux:* `/etc/ssl/certs/`
    *   *Kubernetes:* Use **trust-manager** to mount the CA bundle into pods.

## 8. Alternative Architectures: DANE

**DNS-based Authentication of Named Entities (DANE)** uses DNSSEC to bind a cert to a domain directly in DNS (using `TLSA` records), potentially bypassing the need for CAs entirely. However, client support (browsers) remains low.

---

## 9. Minimum Viable Understanding (MVU)

1.  **Trust is Local:** You don't trust the internet; you trust the list of Root CAs shipped with your OS.
2.  **Private Key = Identity:** If you lose the private key, you are no longer you. If someone else gets it, they *are* you.
3.  **Certs are Witnesses:** A certificate is a portable proof of identity. It turns "I claim to be Google" into "Verisign swears I am Google."
4.  **ACME proves Control:** You only get a cert if you can prove you own the DNS or the Server.
