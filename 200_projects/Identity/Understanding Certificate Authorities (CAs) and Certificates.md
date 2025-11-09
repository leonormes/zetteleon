---
aliases: []
confidence: 
created: 2025-07-24T08:23:11Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:25Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [pki]
title: Understanding Certificate Authorities (CAs) and Certificates
type:
uid: 
updated: 
version:
---

At its core, the goal of Public Key Infrastructure (PKI) is to enable secure communication among parties who have never met before [1]. This model relies on **Certification Authorities (CAs)**, which are mutually trusted third parties that generate and issue digital certificates [1-4].

## Why is a Root CA Trusted to Issue Certificates

The trust in a Root CA stems from a "chain of trust" model [5-9]. Here's how it works and why a Root CA, like one you might set up with AWS Private CA, is trusted:

1. **The Role of a CA**: A CA's primary task is to affirm the identity of a certificate subject and bind that identity to a public key [4]. It does this by signing the certificate with its own private key [2, 4]. The idea is that if you trust the CA, you can trust the certificates it issues [5].
2. **Explicit Trust in Root CAs**:
   - **Pre-installation in Trust Stores**: For publicly trusted CAs, their public verification keys (Root CA certificates) are often pre-installed in operating systems, web browsers (like Mozilla's CA Certificate Program), and other software products [3, 5, 10-13]. This pre-installation represents an explicit decision by the software vendor to trust that particular Root CA [5, 11].
   - **"Transfer of Trust"**: This mechanism creates a "chain of trust" [5-8, 14]. Instead of needing to directly trust every individual's public key, parties only need to trust the CA's public key. If the CA signs other public keys, then Alice and Bob know they can trust those as well [5]. This single, initial trusted distribution of the Root CA's public key is crucial and typically needs to happen only once, at set-up time [5].
   - **Audits and Compliance**: Publicly trusted CAs are subjected to rigorous technical requirements and continuous independent audits to maintain their trusted status [15-18]. For example, AWS Private CA itself undergoes third-party audits for compliance programs like SOC, PCI, FedRAMP, and HIPAA [19].

3. **AWS Private CA as a Root CA**:
   - **Purpose**: AWS Private CA enables you to create and manage private CA hierarchies, including root and subordinate CAs, for **internal use** within your organization [20, 21]. These private certificates are **not publicly trusted** on the internet by default [22].
   - **Trust in a Private PKI**: If you set up AWS Private CA as your Root CA, it is trusted **within your defined environment** because *you* (the internal administrator) explicitly configure your applications, browsers, or operating systems to trust that private Root CA by adding its certificate to their trust stores [13, 22]. This is a crucial distinction from public CAs like Let's Encrypt or DigiCert, whose roots are already universally trusted by common software.
   - **Benefits of AWS Private CA**: Even though they are private, using a service like AWS Private CA provides significant security and operational advantages over self-managed CAs, such as secure storage of private keys, managed revocation services (OCSP/CRLs), and integrations with other AWS services [23-26]. It also allows you to customize certificates to meet internal needs, such as subject names, expiration dates, and algorithms, without external validation requirements [27, 28].

In summary, when AWS is mentioned as a "Root CA," it's important to differentiate between a publicly trusted CA whose roots are pre-installed by default, and a private CA (like AWS Private CA) which *you* set up, and whose trust is established within your specific organizational environment by explicitly configuring clients to trust it. Both types of CAs rely on the fundamental concept of a trusted third party, but the scope of their trust differs.

## How a Certificate Works (for Your Wiki)

A **certificate** (specifically, an X.509 certificate) is a digital document that contains a public key, information about the entity associated with it (the "subject"), and one or more digital signatures used to verify its authenticity [4, 29]. It essentially binds an identity to a public key [2].

Here's a breakdown of how certificates work:

**1. The Purpose of a Certificate**
Certificates are critical for establishing trust in asymmetric (public-key) cryptography [30, 31]. Public-key schemes, while powerful for key establishment, have a critical shortcoming: they require an authenticated channel to distribute public keys to prevent a **Man-in-the-Middle (MIM) attack** [31-33]. Without certificates, an attacker (Oscar) could intercept a public key, replace it with their own, and trick both parties into communicating securely with him instead of each other [32, 33]. Certificates solve this by having a trusted third party (the CA) cryptographically sign the public key and identity [2]. If Oscar tries to manipulate the public key, the signature will be detected as invalid [2].

**2. Key Components of a Certificate**
A certificate, in its most basic form, looks like this: `CertA = [(kpub,A, IDA), sigkpr (kpub,A, IDA)]` [2].
This means it includes:

- **Public Key (kpub,A)**: The public key of the entity (e.g., a server, user, or another CA) [2, 4, 29].
- **Identity (IDA)**: Information identifying the entity, such as its distinguished name (DN) and common name (CN) [2, 29, 34-37].
- **Digital Signature (sigkpr)**: A signature created by the *issuing CA's private key* over the public key and identity information [2, 4]. This signature assures the recipient that the CA vouches for the binding between the public key and the identity [2].

Certificates also contain extensions that provide additional information and constraints [38]. Key extensions include:

- **Authority Information Access (AIA)**: Provides links to the issuing CA's certificate and its Online Certificate Status Protocol (OCSP) responder for real-time revocation checks [38-40].
- **Basic Constraints**: Crucial for CA certificates. It indicates whether the certificate belongs to a CA (`CA:TRUE`) and, if so, can specify a `pathlenConstraint` which limits the number of subordinate CAs that may exist below it in the chain [8, 41-49]. A root CA certificate generally has no path length constraint, allowing unlimited levels of subordinate CAs (though AWS Private CA limits the path to five levels) [43].
- **Subject Key Identifier (SKI) and Authority Key Identifier (AKI)**: These extensions are used to uniquely identify public keys and their corresponding issuing authority's key, aiding in the construction of the certificate path [36, 50-58].

**3. Certificate Hierarchy and Types**
Certificates typically exist within a hierarchical structure [7, 8, 10, 59, 60]:

- **Root Certificates**: These are at the top of the hierarchy and are **self-signed** [7, 8, 61]. They are explicitly trusted and usually have very long lifetimes (often decades) [62, 63]. The private key of a Root CA is highly valuable and should be kept offline and tightly controlled [23, 62, 64, 65].
- **Intermediate Certificates**: These are CA certificates signed by another CA, usually a Root CA [7, 62]. They have shorter lifetimes than roots and are often used by CAs for day-to-day issuance to keep the valuable root keys offline and compartmentalize risk [23, 62, 66, 67]. A single Root CA can have multiple levels of intermediate CAs below it [59, 62].
- **Leaf Certificates (End-entity Certificates)**: These are issued at the bottom of the chain and are used to identify a specific entity, such as a website (e.g., `example.com`), server, or user [68, 69]. They are not used to sign other certificates [68, 69] and usually have the shortest validity periods [70]. They must be sent along with any necessary intermediate certificates to form a complete chain back to a trusted root [68].
- **Self-Signed Certificates**: A certificate signed by its own private key [61, 69, 71]. While technically a form of certificate, they act as their own root and cannot be revoked in the traditional sense [69, 72, 73]. They are generally considered unacceptable for public trust because they don't provide identity verification and can be easily confused with certificates used in MIM attacks [69, 74]. They are, however, useful for bootstrapping private PKIs or for local testing [75].

**4. How Certificates are Issued**
The process of issuing a certificate involves the entity (subscriber) requesting a certificate from a CA:

- **Certificate Signing Request (CSR)**: The subscriber typically generates a key pair and then creates a Certificate Signing Request (CSR) containing their public key and identifying information [34, 76-79]. This request is sent to the CA [76].
- **CA Validation**: The CA then performs validation to ensure the requester controls the domain or identity for which the certificate is being issued [27, 80, 81]. For publicly trusted certificates, this often involves automated "challenges" like HTTP01 or DNS01, where the requester proves control over the domain by placing a specific file on a web server or creating a DNS TXT record [82-86].
- **Signing and Issuance**: Once validated, the CA uses its private key to sign the requestor's public key and identity, creating the new certificate [2, 87]. The CA then provides the newly signed certificate and any necessary intermediate certificates back to the subscriber [76, 87].

**5. How Certificates are Verified (Validation Path)**
When a client (e.g., a web browser) receives a certificate (typically a leaf certificate) from a server, it performs a validation process [2, 14]:

- **Signature Verification**: The client uses the public key of the *issuing CA* to decrypt the digital signature on the received certificate [2, 4]. It then independently hashes the certificate's content and compares this hash to the decrypted signature [4]. If they match, the signature is valid, meaning the certificate has not been tampered with and was indeed issued by that CA [2].
- **Chain Building**: Since leaf certificates are rarely signed directly by a Root CA, the client receives a "chain" of certificates (leaf, then intermediate(s)) [7, 68]. The client "walks up" this chain, verifying each certificate's signature using the public key of the next certificate in the chain, until it reaches a Root CA certificate [7, 14, 68].
- **Trust Anchor Check**: Finally, the client checks if this Root CA certificate is present in its **trust store** (a collection of pre-installed, explicitly trusted Root CA certificates) [3, 11-13]. If a valid chain can be built to a trusted root, the certificate is deemed trustworthy [13, 14]. This process confirms the identity of the server and establishes a secure, encrypted communication channel (TLS/SSL) [88].

**6. Certificate Revocation**
Certificates have a validity period, but they may need to be invalidated *before* their expiration if, for example, the private key is compromised or the certificate was issued erroneously [24, 87, 89, 90]. Two primary mechanisms exist for revocation:

- **Certificate Revocation Lists (CRLs)**: The CA periodically publishes a list of revoked certificates (identified by serial number) [89]. Clients download these lists and check if a certificate is on it [89, 91-93]. CRLs are signed by the CA to ensure their integrity [89, 91].
- **Online Certificate Status Protocol (OCSP)**: Clients can send real-time queries to an OCSP responder to check the revocation status of a specific certificate [24, 25, 38, 39]. The responder returns a cryptographically signed status message (e.g., "good," "revoked," or "unknown") [40].
  While both methods exist, effective revocation has historically been a challenge due to issues like propagation delays and client "soft-fail" policies (where clients might ignore failures to retrieve revocation status) [94-96].

**7. Enhancing Trust and Control**

- **Certificate Transparency (CT)**: A system designed to log all publicly trusted certificates issued by CAs into public, verifiable logs [97-99]. This provides transparency, allowing anyone to monitor certificate issuance and detect misissuances or errors [97-99]. Browsers may require certificates to be recorded in CT logs to be considered valid [98, 100, 101].
- **Certification Authority Authorization (CAA)**: A DNS-based mechanism that allows domain owners to specify which CAs are authorized to issue certificates for their domain names [102-104]. CAs are required to check CAA records before issuing a certificate [18, 105]. This acts as a defense-in-depth measure, reducing the attack surface by limiting the number of CAs that could legitimately issue a certificate for a domain [102, 106].

---
