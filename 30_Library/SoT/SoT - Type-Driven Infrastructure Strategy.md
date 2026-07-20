---
aliases: [Formal Methods for IaC, Infrastructure as Applied Type Theory, The Witness Pattern, Type-Driven Infrastructure, Type-Safe IaC]
conformant: false
created: 2025-12-30T14:00:00+00:00
modified: 2026-07-20T16:33:42+00:00
non_conformance_reason: "Bulk inferred type. Needs review."
permalink: llmeon/30-library/so-t/so-t-type-driven-infrastructure-strategy
tags: [cdktf, devops, iac, rust, SoftwareEngineering/Architecture, terraform, type-theory]
title: SoT - Type-Driven Infrastructure Strategy
type: sot
---

## SoT - Type-Driven Infrastructure Strategy

### 1. Definitive Statement

> [!definition] Type-Driven Infrastructure
> A paradigm shift from Stringly-Typed configuration (loose strings/HCL) to Proof-Carrying Logic. It treats infrastructure as a dependency chain where valid states are mathematically proven at synthesis time, making illegal architectures unrepresentable.

---

### 2. Core Operational Primitives

#### I. The Witness Pattern (Capability Tokens)

A Witness is a data type whose instantiation serves as proof that a prerequisite state is satisfied.

- Mechanic: Downstream resources demand a Witness Type (e.g., `IpReachabilityWitness`) as an argument, not a raw string ID.
- Result: You cannot create a Certificate without proving DNS control; you cannot create DNS without proving IP existence.

#### II. Reachability as a Type (Phantom Types)

Reachability is a Type State, not a tag or metadata.

- Constraint: Use generics/phantom types to differentiate `IpAddress<Public>` from `IpAddress<Private>`.
- Gateway Functions: Transitioning a resource from private to public requires a explicit transformation function (e.g., `NatGateway::expose(Private) -> Public`).

#### III. Affine Resource Ownership (Move Semantics)

Treat infrastructure resources as Linear Assets (Rust model).

- Linearity: A specific Port 80 or PVC can be bound exactly once.
- Consumption: "Moving" a resource handle into a consumer prevents double-binding errors at the compiler level.

---

### 3. Implementation Patterns

#### Pattern A: The "Compiler" (CDKTF + TypeScript)

When HCL is insufficient, use a high-level language to synthesize the JSON manifest.

1. Source: Define strict types and private constructors in TypeScript.
2. Synthesis: `cdktf synth` validates logic. If types mismatch, the build fails.
3. Deployment: Commit the Assembly (`cdk.tf.json`) alongside source for VCS-triggered runs.

#### Pattern B: HCL Simulation (The "Poor Man's" Type System)

In pure Terraform, simulate Sum Types (Enums) to reduce state space.

1. The Interface: Restrict a `profile` variable to specific strings using `validation` blocks.
2. The Implementation: Use a `local` map to define the fixed configuration for each profile variant.
3. The Result: Users choose a Variant, not individual parameters, preventing "Configuration Explosion."

#### Pattern C: Capability-Based Access

Reject raw RBAC strings in favor of Capability Tokens.

- Identity: Modeled as a Sum Type (`Human | Bot`).
- Logic: A `DevCapability` token is physically incapable of targeting a `Production` environment in the code model.

---

### 4. Architectural Mapping (Data-Oriented View)

| Concept | Traditional IaC (Stringly) | Type-Driven (Data-Oriented) |
|:--- |:--- |:--- |
| Storage Class | String ID | Factory Function producing PVs |
| PVC | Resource Request | Type Constraint (`Req<Pending>`) |
| Binding | Status Code | Witness Type (`BoundClaim`) |
| Pod | Resource Bag | Consumer requiring `Vec<Witness>` |

---

### 5. Minimum Viable Understanding (MVU)

1. Shift Left: Move validation from Runtime (OPA/Deployment Failure) to Synthesis Time (Build Failure).
2. Modules are Types: Modules are contracts. Don't expose "all parameters"; expose "all valid states."
3. Parse, Don't Validate: Structure data so that only valid configurations can be represented.
