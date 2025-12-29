---
aliases: ["Cross-Cloud Security", "Secure Data Transport", "SoT - Cross-Cloud"]
confidence: "5/5"
created: 2025-03-13T15:51:37Z
epistemic: "architecture"
last_reviewed: "2025-12-22"
modified: 2025-12-28T18:49:16+00:00
purpose: "To define the architectural data patterns for secure, private communication between decoupled cloud environments (AWS/Azure)."
review_interval: "6 months"
see_also: ["[[SoT - Cloud Networking Core Components]]", "[[SoT - The Data-Centric Theory of Networking]]"]
source_of_truth: []
status: "stable"
tags: ["architecture", "cloud", "data-centric", "security", "sot"]
title: SoT - Secure Cross-Cloud Data Transport
type: "SoT"
uid: 
updated: 
---

## 1. Definitive Statement

> [!definition] Definition
> **Secure Cross-Cloud Transport** is the architectural pattern of establishing a **Virtual Private Data Plane** over untrusted public networks.
>
> It relies on **Tunneling Encapsulation** (to create a logical link layer) and **Cryptographic Wrapping** (to enforce confidentiality and integrity), effectively extending the trust boundary of one cloud's VPC into another.

---

## 2. State Definition (The Payload Atoms)

The system manages two distinct types of data state, each with specific sensitivity and lifecycle properties.

### A. The Request State (Job Queue)

*Direction: Consumer (Azure) -> Producer (AWS)*
- **Tuple:** `(JobID, Parameters, Metadata, AuthToken)`
- **Characteristics:**
    - **Idempotency:** Requests must be uniquely identifiable to prevent duplicate processing.
    - **Sensitivity:** High. Contains business logic configuration and potential PII.

### B. The Response State (Job Result)

*Direction: Producer (AWS) -> Consumer (Azure)*
- **Tuple:** `(JobID, Status, OutputData, Logs)`
- **Characteristics:**
    - **Volume:** Highly variable (kB to GB).
    - **Integrity:** The output must be cryptographically verifiable as originating from the specific job execution.

---

## 3. Structural Mapping (The Tunnel Architecture)

To transport these states securely, we construct a virtual circuit that abstracts the underlying public internet.

### The Virtual Wire (VPN / Interconnect)

Data is encapsulated within a **Tunneling Protocol** (e.g., IPsec, WireGuard).

- **Outer Header:** Public IPs (Routeable on Internet).
- **Inner Header:** Private IPs (Routeable only within the VPCs).
- **Payload:** Encrypted Data.

### The Gateway Pattern

The structural entry/exit points for data are **Gateways**, not individual nodes.

- **Ingress Gateway:** Decapsulates, Decrypts, and Routes to internal services.
- **Egress Gateway:** Encrypts, Encapsulates, and Routes to the peer gateway.

---

## 4. Functional Component Architecture (Abstract Handlers)

To maintain the security envelope, the transport bridge employs five abstract functional components at the **Network Entry Points** of each cloud environment.

### I. Private Pathway Creator (The Conduit)
- **Function:** Establishes a dedicated, isolated path (tunnel) between VPCs, bypassing the public internet.
- **Data Role:** Ensures all packets travel on a pre-defined, non-public logical route.

### II. Data Encryptor / Decryptor (Confidentiality)
- **Function:** Transforms plaintext into ciphertext at the Egress Gateway and reverses the process at the Ingress Gateway.
- **Data Role:** Ensures that data is unreadable to any entity outside the peer gateways.

### III. Data Integrity Verifier (Trustworthiness)
- **Function:** Attaches cryptographic signatures or hashes to data units.
- **Data Role:** Guarantees that the received data is bit-identical to the sent data, detecting any tampering.

### IV. Endpoint Authenticator (Identity)
- **Function:** Verifies the cryptographic identity of the peer gateway and the requesting service.
- **Data Role:** Ensures that "Bunny" only speaks to the real "Relay," and vice-versa.

### V. Access Controller (Authorization)
- **Function:** Enforces the "Allow/Deny" logic based on service permissions.
- **Data Role:** Regulates the flow of specific payloads (e.g., Job Requests vs. Logs) based on the requesting entity's role.

---

## 5. Fundamental Routing Principles & Requirements

Every cross-cloud data pathway must adhere to five fundamental principles to ensure the security and stability of the distributed system.

### I. Privacy and Isolation
- **Principle**: Data in transit must be isolated from the public internet to prevent unauthorized interception.
- **Requirement**: Establish a logically private network path (e.g., VPN Tunnel, AWS PrivateLink).
- **Example**: "Bunny" (Azure AKS) and "Relay" (AWS EKS) communicate over a private bridge rather than open ingress.

### II. Confidentiality (Encryption)
- **Principle**: Data must be unreadable to interceptors.
- **Requirement**: Strong encryption (TLS 1.2+, AES-256) for all data flowing between environments.

### III. Integrity
- **Principle**: Data must not be altered or tampered with during transit.
- **Requirement**: Cryptographic signatures (HMAC) or hashing to guarantee that "Bunny" receives exactly what "Relay" sent.

### IV. Authentication
- **Principle**: Bidirectional verification of source and destination identity.
- **Requirement**: Implement **Mutual TLS (mTLS)** where possible. "Bunny" must verify "Relay" is legitimate, and "Relay" must verify the request comes from a valid "Bunny" instance.

### V. Authorization
- **Principle**: Access is granted based on the principle of least privilege.
- **Requirement**: "Bunny" is only authorized to poll the job queue and return results; it has no broader access to the AWS VPC or EKS APIs.

---

## 5. Invariants & Constraints (The Security Envelope)

For the cross-cloud bridge to be considered "Secure," four invariant properties must be maintained for every packet.

1. **Confidentiality Invariant:** `Decrypt(Intercept(Packet)) == Garbage`. All data traversing the public segment must be encrypted (AES-256).
2. **Integrity Invariant:** `Hash(Received_Data) == Hash(Sent_Data)`. Any bit-flip or tampering during transit must cause the packet to be dropped (HMAC).
3. **Mutual Authentication (mTLS):** The Consumer must prove its identity to the Producer, AND the Producer must prove its identity to the Consumer. Trust is bidirectional.
4. **Isolation Constraint:** No traffic is permitted to bypass the Gateway. Direct internet access for data transmission is structurally impossible (Private Subnets).

---

## 5. Logic Derivation (Routing & Access)

The logic of secure transport is derived from the data structure of the tunnel and the identity assertions of the endpoints.

- **Routing Logic:**
    - If `Dest_IP` is in `Peer_CIDR`, forward to `Local_Gateway`.
    - The `Local_Gateway` encapsulates and forwards to `Remote_Gateway_Public_IP`.
- **Access Control Logic (Zero Trust):**
    - **Authorization:** `Allow(Subject, Resource, Action)` is evaluated at the Application Layer (Layer 7) *after* the network connection is established. Network reachability does not imply application access.

### Performance Optimization: Protocol Selection

- For high-throughput "Job Results" (Bulk Data), prefer **UDP-based tunneling** (like WireGuard) to avoid TCP-over-TCP meltdown, or use dedicated **Cloud Interconnects** (Direct Connect / ExpressRoute) to bypass the public internet entirely.

---

## 6. The Strategic Argument: Why HTTPS is Insufficient

*Source: [[99_Archive/Why HTTPS is not good enough|Analysis of Public vs Private Networking]]*

A common architectural fallacy is believing that HTTPS (Encryption) negates the need for Private Networking (Isolation). This conflates **Message Security** with **Endpoint Security**.

### A. The Core Analogy: The Armored Car vs. The Tunnel

- **HTTPS (Public Internet):** Sending an armored car full of cash through busy public streets. The contents are safe, but the vehicle can be followed, mapped, and attacked (DDoS). The *Address* is public.
- **Private Connection (VPN/ExpressRoute):** Building a secret underground tunnel between two bank vaults. The armored car drives through it, but the tunnel itself is invisible to the world. The *Address* is private.

### B. The Four Risks of Public Endpoints

1. **Attack Surface (Reconnaissance):** A public IP announces your existence. Scanners will fingerprint your OS, Web Server, and TLS versions instantly. A private network is invisible.
2. **Endpoint Integrity:** HTTPS protects the *data*, not the *server*. It does not stop an attacker from exploiting an OS vulnerability (Heartbleed) or overwhelming the server (DDoS).
3. **Broken "Least Privilege":** Exposing a service changes the default from "Deny All" to "Allow All (who have a key)." This is a weaker posture than "Network Unreachable."
4. **Audit Fragility:** "We use a private tunnel" is a stronger compliance narrative than "We use a public endpoint with a firewall whitelist."

---

## 7. Compliance & Regulatory Alignment

For sensitive data (e.g., Patient Records), the **NHS Digital** and **NCSC** frameworks mandate a defense-in-depth approach.

- **NCSC Principle 1 (Data in Transit):** Requires both Encryption (HTTPS) *and* Network-Level Protection (VPN/Private Link).
- **NCSC Principle 11 (External Interface Protection):** Mandates defending external interfaces. The most effective defense is to *have no external interface* by using private peering.
- **GDPR Article 32:** Mandates "Security by Design." Network segmentation and isolation are fundamental to limiting the blast radius of a potential breach.
