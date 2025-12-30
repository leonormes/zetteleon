---
aliases: ["Formal Methods for IaC", "Type-Driven Infrastructure", "The Witness Pattern", "Infrastructure as Applied Type Theory"]
confidence: "High"
created: 2025-12-30T14:00:00Z
epistemic: "principle"
last_reviewed: "2025-12-30"
modified: 2025-12-30T14:00:00Z
purpose: "To define the architectural paradigm of using Type Theory and Formal Methods to make broken infrastructure configurations unrepresentable at synthesis time."
review_interval: "6 months"
see_also: []
source_of_truth: []
status: "stable"
tags: ["architecture", "iac", "type-theory", "devops", "rust", "cdktf"]
title: SoT - Type-Driven Infrastructure Strategy
type: "SoT"
uid: 
updated: 
---

# SoT - Type-Driven Infrastructure Strategy

## 1. Executive Summary

**Thesis:** Software architecture is Applied Type Theory.
**Goal:** Make "Illegal Infrastructure States" Unrepresentable.
**Method:** Shift validation from **Runtime** (Deployment Failure/OPA) to **Synthesis Time** (Compiler Failure).

Current paradigms (Terraform HCL, Helm) are "Stringly Typed." They allow loose couplings where dependencies (e.g., DNS pointing to a non-existent IP) are checked only after the expensive process of provisioning has begun.

We adopt a **Type-Driven** approach where infrastructure is treated not as a collection of resources, but as a **Dependency Chain of Proofs**.

---

## 2. Core Concepts

### A. The "Witness" Pattern (Proof-Carrying Code)

A **Witness** is a data type whose existence serves as a mathematical proof that a prerequisite state is satisfied.

*   **Traditional IaC:** "I hope this resource ID exists." (String)
*   **Type-Driven IaC:** "Here is the token proving I created this resource." (Witness)

**Rules of the Witness:**
1.  **Unforgeable:** Cannot be created manually (private constructor).
2.  **Context-Aware:** Carries "Phantom Types" (e.g., `<Public>` vs `<Private>`) to enforce logic at compile time.
3.  **Mandatory:** Downstream resources demand the Witness, not a string.

### B. Reachability as a Type

Reachability is not a tag; it is a **Type State**. A generic IP string is insufficient. We must differentiate between `IpAddress<Public>` and `IpAddress<Private>` at the compiler level.

*   **Phantom Types:** Types used during synthesis to enforce constraints but erased at runtime.
*   **Gateway Functions:** You cannot cast `Private` to `Public`. You must pass the `PrivateIP` through a `NatGateway` function to obtain a `PublicIP` witness.

### C. Resource Ownership (Affine Types)

We use **Rust** as our mental model for resource lifecycles because of **Affine Types (Move Semantics)**.
*   **Linearity:** A specific Port 80 on a Load Balancer can be bound *exactly once*.
*   **Consumption:** Binding a Volume to a Pod "moves" the Volume handle, preventing double-binding errors at the syntax level.

---

## 3. The Trinity of Identity (Domain Model)

To eliminate "loose couplings" between Network, DNS, and Identity, we model them as a dependent chain.

### 1. Existence (IP)
*   **Type:** `IpAddress<Scope>`
*   **Constraint:** Must be produced by a trusted Network Factory.

### 2. Binding (DNS)
*   **Type:** `VerifiedRecord<Scope>`
*   **Constraint:** Requires a `HostName` AND an `IpAddress<Scope>`.
*   **Invariant:** You cannot create a DNS record without proving the target IP exists.

### 3. Identity (Certificate)
*   **Type:** `TlsCertificate`
*   **Constraint:** Requires a `VerifiedRecord<Public>`.
*   **Invariant:** A CA will not sign a cert unless you prove you control the DNS binding.

**Rust Pseudo-Code Model:**
```rust
// The Service cannot be constructed unless all proofs are provided.
struct PublicService {
    name: String,
    ingress_ip: IpAddress<Public>,
    dns_proof: VerifiedRecord<Public>, // Proves DNS -> IP
    identity: TlsCertificate,          // Proves Cert -> DNS
}
```

---

## 4. Implementation: The "Compiler" Pattern

Since HCL is insufficient for this logic, we use **CDKTF (Cloud Development Kit for Terraform)** with **TypeScript**.

### Architecture
1.  **Source (Logic):** TypeScript with strict types and private constructors.
2.  **Synthesis (Compiler):** `cdktf synth` runs the logic. If types mismatch (e.g., Private IP to Public DNS), the build fails.
3.  **Artifact (Assembly):** The compiler emits `cdk.tf.json` (Standard Terraform JSON).
4.  **Execution (Runtime):** Terraform Cloud/CLI applies the JSON.

### Workflow: "Synthesize & Ship"

When using GitOps/VCS triggers:
1.  **Dev:** Write logic in `main.ts`.
2.  **Build:** Run `npx cdktf synth` locally/CI.
3.  **Commit:** Commit the **Assembly** (`cdk.tf.json`) alongside the source.
4.  **Deploy:** TFC/Atlantis executes the plan against the verified JSON.

---

## 5. Kubernetes Data-Oriented View

We reframe Kubernetes objects as Type Constraints to explain failures (like "Pending" PVCs) as missing Witnesses.

| Concept | Traditional K8s (YAML) | Type-Driven (Data Oriented) |
| :--- | :--- | :--- |
| **StorageClass** | A String field | A **Factory Function** producing PVs |
| **PVC** | A Request | A **Type Constraint** (`Request<Pending>`) |
| **Binding** | Status: Bound | A **Witness Type** (`BoundClaim`) |
| **Pod** | Resource | A Consumer requiring `Vec<VolumeSource>` |

**The Invariant:** A Pod cannot be instantiated (scheduled) without a `BoundClaim` witness.

---

## 6. Glossary

*   **Phantom Type:** A type parameter `T` in `Type<T>` that is not used in the runtime representation but enforces compile-time constraints.
*   **Sum Type:** An "OR" type (Enum). Data is *either* A *or* B. (e.g., `VolumeSource = Ephemeral | Persistent`).
*   **Product Type:** An "AND" type (Struct). Data requires A *and* B. (e.g., `PublicService = IP + DNS + Cert`).
*   **Affine Type:** A type that can be used at most once (Resource Ownership).
