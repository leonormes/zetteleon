---
aliases: ["Infrastructure Witness", "Proof-Carrying Infrastructure", "Type Witness", "Witness Pattern"]
confidence: "5/5"
created: 2025-12-30T10:39:13+00:00
epistemic: "architecture"
last_reviewed: "2025-12-30"
modified: 2026-01-08T10:49:40+00:00
purpose: "To define the Witness Pattern in infrastructure, enabling 'Proof-Carrying Code' that replaces implicit trust (strings) with explicit capabilities (types)."
review_interval: "6 months"
see_also: ["[[MOC - Type Theory]]", "[[SoT - Parse, Don't Validate]]", "[[SoT - Type-Driven Development (The Torvalds Loop)]]", "[[SoT - Type-Driven Infrastructure as Code]]"]
source_of_truth: []
status: "stable"
tags: ["iac", "pattern", "SoftwareEngineering/Architecture", "SoftwareEngineering/Security", "type_theory"]
title: SoT - The Infrastructure Witness Pattern
type: "SoT"
uid: 
updated: 
---

## 1. Definition

> [!definition] The Infrastructure Witness
> A **Witness** is a specific data type (or object) whose existence serves as a mathematical proof that a prerequisite infrastructure state has been successfully satisfied.
>
> Unlike standard configuration values (strings, booleans) which describe _what_ we want, a Witness describes _what has been established_.

It transforms temporal dependencies ("Resource A must exist before Resource B") into structural dependencies ("Function B requires Type A as an argument").

---

## 2. The Context: "Stringly Typed" Trust

In traditional paradigms (Terraform HCL, Helm), dependencies are loose and trust is implicit. This is the "Stringly Typed" anti-pattern.

- **The Anti-Pattern:** A Load Balancer resource asks for a `subnet_id` as a `string`.
- **The Risk:** The developer can supply _any_ string (e.g., a private subnet ID, a deleted ID, or `"foo"`).
- **The Failure Mode:** The error is only discovered at **Runtime** (during `terraform apply` or, worse, via outage).

---

## 3. Working Knowledge: Proof-Carrying Code

The Witness pattern enforces the **[[SoT - Parse, Don't Validate|Parse, Don't Validate]]** principle.

### 3.1 The Mechanics of a Witness

1. **Unforgeable:** A Witness cannot be created manually by the user (e.g., via a private constructor). It is only returned by a trusted "Factory" (e.g., a Network Module).
2. **Context-Aware:** It often uses **Phantom Types** or Generics to carry metadata (e.g., `<Public>` vs `<Private>`) that disappears at runtime but enforces logic at compile-time.
3. **Required Consumer:** Downstream resources do not accept strings; they accept only the specific Witness type.

> "A Witness is a capability token. Holding the token proves you have the right to use the resource."

---

## 4. Formal Domain Modeling (The Identity Trinity)

We model the chain **IP $\to$ DNS $\to$ Identity** not as sibling resources, but as a **Dependency Chain** where each step produces a Witness required by the next.

### Phase 1: Reachability as a Type (The Phantom)

"Public" and "Private" are not tags; they are disjoint types with different allowed operations. We use Phantom Types to enforce this without runtime overhead.

```rust
// The Scopes (Phantom Tags)
struct Public;
struct Private;

// The IP acts as a container for reachability context
struct IpAddress<Scope> {
    val: String, 
    _marker: std::marker::PhantomData<Scope>,
}

// Factories enforce strict typing
impl IpAddress<Public> {
    fn new_public() -> Self { ... }
}
```

### Phase 2: The Gateway Witness (Type Transformation)

How does a Private IP become Public? Through a **Gateway Function** (NAT/LB).

```rust
struct NatGateway;

impl NatGateway {
    // This function is the "Witness" of reachability.
    // It consumes a Private IP and proves it is now exposed as a Public IP.
    fn expose(&self, internal: IpAddress<Private>) -> IpAddress<Public> {
        // Synthesis: Create Elastic IP, bind NAT rule...
        IpAddress::<Public>::new(...)
    }
}
```

### Phase 3: The Binding Witness (Proof of Routing)

A DNS record is not a string; it is a **Product Type** binding a Name to an IP.

```rust
struct VerifiedRecord<Scope> {
    name: HostName,
    target: IpAddress<Scope>, // The generic <Scope> propagates here
}

struct Zone;
impl Zone {
    // You cannot create a VerifiedRecord without a valid IP of the correct scope.
    pub fn bind<Scope>(&mut self, host: HostName, ip: &IpAddress<Scope>) -> VerifiedRecord<Scope> {
        VerifiedRecord { name: host, target: ip.clone() }
    }
}
```

### Phase 4: Identity (The Dependent Consumer)

A Certificate Authority (CA) signs a "Proof of Control," not a string.

```rust
struct CertificateAuthority;

impl CertificateAuthority {
    // It is a type error to request a Cert for a Private IP 
    // or a non-existent DNS record.
    pub fn issue(&self, proof: &VerifiedRecord<Public>) -> TlsCertificate {
        // ... logic ...
    }
}
```

---

## 5. The "PublicService" Product Type

We assemble these witnesses into a final Product Type. This makes the "Illegal State" (Service with Cert but no DNS) unrepresentable.

```rust
struct PublicService {
    name: String,
    ingress_ip: IpAddress<Public>,
    dns_proof: VerifiedRecord<Public>, // Ensures DNS points to ingress_ip
    identity: TlsCertificate,          // Ensures Cert matches DNS
}
```

If you try to construct this struct without providing the `dns_proof` (which you can only get by actually creating the DNS record), the code **will not compile**.

---

## 6. Comparison: Implicit vs. Explicit Trust

| Feature | Standard IaC (HCL/YAML) | Type-Driven (Witness Pattern) |
|:--- |:--- |:--- |
| **Identity** | String (`"api.com"`) | `HostName` (NewType) |
| **Binding** | Resource (loose pointer) | `VerifiedRecord<Scope>` (Proof) |
| **Reachability** | Boolean flag / Tag | `IpAddress<Public>` vs `IpAddress<Private>` |
| **Transformation** | Implicit (Security Group) | Explicit Function (`NatGateway::expose`) |
| **Validation** | Runtime (Failure) | Compile-time (Type Mismatch) |

---

## 7. Implementation Notes

- **CDKTF (TypeScript):** Use `private` constructors and class nominal typing (`private _scope: Scope`) to simulate Phantom Types.
- **Linear Types:** In the future, we can use Affine Types (Rust's Move semantics) to ensure a specific IP port is bound _exactly once_, preventing port collisions at compile time.
