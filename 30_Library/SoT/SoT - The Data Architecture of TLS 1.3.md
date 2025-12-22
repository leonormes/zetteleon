---
aliases: [Cryptographic Wrapping, SoT - TLS, TLS 1.3 Architecture, Transport Layer Security]
confidence: 5/5
created: 2025-08-14T20:21:09Z
epistemic: architecture
last_reviewed: 2025-12-22
modified: 2025-12-22T11:07:57Z
purpose: To define the fundamental data architecture of TLS 1.3, focusing on state negotiation, the cryptographic key schedule, and record framing.
review_interval: 6 months
see_also: ["[[SoT - Digital Identity]]", "[[SoT - The Architecture of Packet Encapsulation (TCP-IP)]]"]
source_of_truth: true
status: stable
tags: [architecture, cryptography, data-centric, networking, sot, tls]
title: SoT - The Data Architecture of TLS 1.3
type: SoT
uid:
updated:
---

## 1. Definitive Statement

> [!definition] Definition
> **TLS 1.3** is a state-negotiation and cryptographic-wrapping protocol designed to transform an untrusted byte-stream (TCP) into a secure, authenticated, and private communication channel.
>
> From a data-centric perspective, it is a **distributed state machine** driven by a **Hierarchical Key Schedule**. It deconstructs the security problem into two phases: the negotiation of a shared secret (Handshake) and the recursive framing of payloads within authenticated encryption envelopes (Record Layer).

---

## 2. State Definition (The Atoms)

The protocol manages two primary categories of state: negotiation parameters and cryptographic material.

### A. The Handshake Parameters (Negotiation State)

Represented by the `ClientHello` and `ServerHello` PDUs.

- **Tuple:** `(Version, CipherSuite, KeyShare, Extensions)`
- **Extensions Metadata:** `(SNI, ALPN, SupportedGroups)`. This data defines the "context" of the session.

### B. The TLS Record (Transport State)

The atomic unit of the data plane.

- **Record Tuple:** `(Type, Version, Length, EncryptedPayload, AuthTag)`
- **Key Field:** `AuthTag` (MAC). Ensures the integrity invariant of the wrapped state.

### C. The Keying Material (The Secret Atoms)

Derived using HKDF (HMAC-based Extract-and-Expand Key Derivation Function).

- **Tuple:** `(Secret, Label, Context)`

---

## 3. Structural Mapping (The Layout)

The complexity of TLS 1.3 resides in its **Key Schedule**—a directed graph of key derivations that ensures strict isolation between session stages.

### The HKDF Key Tree (The Derivation Layout)

State transitions move forward through a one-way derivation tree:

1.  **Early Secret:** Derived from PSK (External state).
2.  **Handshake Secret:** Derived from ECDHE shared secret (Ephemeral state).
3.  **Master Secret:** The root for application traffic.
4.  **Traffic Keys:** `(Client_Write_Key, Server_Write_Key)`.

**Design Intent:** By sharding the keys into "Handshake" and "Application" domains, the protocol ensures that a compromise of the handshake data does not expose the application payload.

### The Record Layer (Framing)

TLS frames are nested within the TCP payload.

-   **Layout:** 5-byte header followed by a variable-length opaque blob.
-   **Padding:** Appended to the payload to hide the true data length (Traffic Analysis mitigation).

---

## 4. Invariants & Constraints

For a TLS session to be "Secure by Design," it must satisfy these invariants:

1.  **PFS (Perfect Forward Secrecy):** Every session MUST use ephemeral key exchange (`ECDHE`). The compromise of the server's long-term private key must NOT allow the decryption of past recorded traffic.
2.  **Integrity Invariant:** `Verify(AuthTag, Ciphertext) == True`. Any modification to the Record PDU must result in immediate connection teardown.
3.  **Nonce Uniqueness (Anti-Replay):** `Nonce = SequenceNumber XOR IV`. Nonces must NEVER be reused with the same key. The monotonic sequence number in the record layer enforces this.
4.  **Cipher Constraint:** Only AEAD (Authenticated Encryption with Associated Data) ciphers are permitted (e.g., `AES-GCM`, `ChaCha20-Poly1305`).

---

## 5. Logic Derivation (The Algorithms)

Because the data is structured as a hierarchical key schedule and a set of supported parameters, the logic is "degenerate":

-   **Parameter Negotiation:** A simple **Set Intersection**.
    -   `Selected_Suite = Intersection(Client_Suites, Server_Suites).First()`.
-   **Key Derivation:** A sequence of **Fixed-length HMAC operations**. Logic is a direct consequence of the HKDF state tree.
-   **Secure Transport:** Applying the `Encrypt-then-MAC` transformation to the `Record` atom.

### Performance Optimization: 1-RTT Handshake

TLS 1.3 optimises for **latency** by speculative state inclusion. The client sends its `KeyShare` atom in the first packet (`ClientHello`), allowing the server to derive the `Handshake Secret` immediately. This reduces the logic of connection establishment from 2-RTT (TLS 1.2) to 1-RTT.
