---
aliases: [Configuration Generator Pattern, Contract-Based Infrastructure, Generative Config, GIC Framework]
conformant: false
created: 2025-12-13T00:00:00+00:00
modified: 2026-07-20T16:33:49+00:00
non_conformance_reason: "Bulk inferred type. Needs review."
permalink: llmeon/30-library/so-t/so-t-generative-infrastructure-configuration-framework
tags: [configuration_management, cue, devops, infrastructure_as_code, SoftwareEngineering/Architecture, terraform]
title: SoT - Generative Infrastructure Configuration Framework
type: sot
---

> Core Principle: "By defining a minimal, declarative Configuration Kernel (intent) and processing it through a validated Configuration Generator (code), the system automatically derives complex, error-prone values (protocols), ensuring consistency, reducing cognitive load, and making changes explicitly evident."

## Minimum Viable Understanding (MVU)

1. Intent-Implementation Separation: Distinguish between _declarative intent_ (what to deploy) and _implementation details_ (how to deploy it), reducing cognitive load.
2. Input Minimal Intent: Only define what distinguishes this deployment (Name, Env, CIDR) in a single source (`customer.yaml`).
3. Generate Complexity: Use code (`locals.tf`, CUE) to derive names, paths, IPs, and tags based on strict mathematical protocols.
4. Data Has One Home: Every value must trace to exactly one authoritative source. If you type a literal twice, the architecture is broken.
5. Unify Constraints: Treat configuration as a "Lattice" where values must satisfy all constraints (CUE `vet`).
6. Fail Fast: Validate the Generator contract (`infra_facts`) so individual deployments are safe by default.

## Working Knowledge (The Framework)

### The Core Problem: Fragile Precision (Error Surface Area)

Manual configuration in modern distributed systems is fragile. Reliance on vast, explicit `.tfvars` files or Helm values leads to a high Configuration Error Surface Area—the number of manually editable parameters (DNS names, bucket names, secret paths) that could contain errors. This leads to Accidental Complexity:

- String Coupling: `DB_PASSWORD` in Vault must match `database-pwd` in K8s. If they drift, the chain snaps at runtime.
- Linguistic Dependency: Systems communicate via "magic strings" rather than typed contracts.
- Deferred Fragility: Errors surface only when a specific path is exercised (e.g., a Pod CrashLooping at 3am), not at compile time.

By reducing this to a minimal Configuration Kernel (5-10 essential parameters) and generating all other values via a Configuration Generator, the error surface area decreases by 80-90%.

### The Solution: The "One Home" Hierarchy

Every value in the system must trace to exactly one authoritative source.

```
customer.yaml          ← Kernel: Customer-specific values (name, env, CIDR)
       ↓
locals.tf              ← Generator: Terraform derivations (The Math)
       ↓
infra_facts output     ← The Contract: Typed data passed to CUE
       ↓
CUE schema             ← Boundary: Validates the contract
       ↓
CUE render             ← Pure Transformation: reads policy.* and infra.*
       ↓
policy_defaults.cue    ← Constants: Platform-wide values (versions, timeouts)
       ↓
generated/values.yaml  ← The Manifest: The volatile output (Machine Read)
```

### Layer Responsibilities

| Layer | Responsibility | Constraint |
|:---|:---|:---|
| Kernel (`customer.yaml`) | Identity, Network space, Feature Overrides | No platform defaults here. |
| Derivations (`locals.tf`) | CIDR math, Naming conventions, environment mapping | No raw literals except templates. |
| Contract (`infra_facts`) | The API boundary between Infra and App layers | Must be mirrored in CUE schema. |
| Schema (`schema_infra.cue`) | Pure type declarations and structural enforcement | No values allowed. |
| Policy (`policy_defaults.cue`) | Platform constants (Chart versions, persistence sizes) | No customer-specific data. |
| Transformation (`render.cue`) | Maps flat facts to nested YAML structures | Zero literals; pure read from infra/policy. |

### The Layer Ownership Rule

To maintain system integrity, every layer has a strict "No Literals" boundary:

1. `customer.yaml`: Owns customer-specific literals only.
2. `policy_defaults.cue`: Owns platform-wide constants only.
3. `locals.tf`: Owns Derived values only—no new literals.
4. `render_fitfile.cue`: Owns Mapping only—reads from `infra.*` and `policy.*`, zero literals.

> Onboarding Rule: Never manually edit the output in `generated/values.yaml`. If you need to change a platform setting, edit `policy_defaults.cue`. If you need to map a new secret or toggle for an app, edit `render_fitfile.cue`.

### The Generative Protocols ("The Math")

A core GIC implementation uses deterministic algorithms to eliminate human error in networking and naming.

#### 1. Subnet Slicing Logic

Given a VNet address space (e.g., `/16`), subnets are sliced using consistent indices:

- System: Index 0 (`cidrsubnet(base, 4, 0)`)
- Workflows: Index 1 (`cidrsubnet(base, 4, 1)`)
- App: Index 2 (`cidrsubnet(base, 4, 2)`)
- Jumpbox: Index 3 (`cidrsubnet(base, 4, 3)`)
- Ingress IP: Base IP of System Subnet + offset (e.g., `.203`)

#### 2. The Naming Protocol

Derived from the composite `deployment_key`: `${customer_name}-${env_prefix}-${instance_id}`.

- Resource Group: `rg-${workload}-${region}-${env_prefix}-net`
- VNet: `vnet-${workload}-plat-${region}-01`
- Secret Paths: `/{environment}/{app_name}/{secret_type}`
By encoding these rules in the Generator, the protocol ensures consistency across all deployments and eliminates manual naming errors. The protocol becomes the single source of truth for organisational naming standards.

## Theoretical Foundation

The framework resolves the tension between Flexibility and Resilience by adopting Lattice-Based Logic:

- Configuration as Constraint Unification: Instead of "A overrides B" (Last Writer Wins), CUE and GIC enforce "A and B must both be true".
- Monotonicity: Changes should narrow the possibility space (add information) rather than arbitrarily flip values.
- Strongly Typed Infrastructure: Moving from "Stringly Typed" config to "Contract Based" infrastructure allows for compile-time validation of the entire graph.

## Implementation Patterns

### Level 1: Terraform & Helm (Generative)

Terraform acts as the "Root Generator," producing values that are passed to Helm.

- _Workflow_: Terraform GIC module derives all names/tags -> provisions Cloud -> renders Helm values.
- _Benefit_: Ensures Infrastructure and Application layers share the exact same string derivations.

### Level 2: CUE (Constraint-Based)

For high-maturity environments, CUE (Configure, Unify, Execute) replaces simple templating. See [[SoT - CUE Configuration]] for the underlying logic of Unification.

- Schema as Truth: A single CUE struct defines the "Secret Contract".
- Multi-Target Export: The same CUE definition exports the Vault Policy (HCL), Kubernetes Secret (YAML), and App Config (.env).
- Validation: A mismatch between the Vault path and the K8s secret definition is caught as a Bottom (⊥) value (contradiction) during evaluation, preventing deployment.

## Anti-Patterns to Reject

- Literals in the Render Layer: Hardcoding `targetRevision: "main"` in CUE render files instead of `policy_defaults.cue`.
- Customer Data in Platform Policy: Putting `customer_name` inside CUE policy files.
- Values in the CUE Schema: Defining `registry: "fitfileregistry.azurecr.io"` inside `schema_infra.cue`.
- Manual Manifest Edits: Modifying `generated/values.yaml` directly instead of updating `customer.yaml`.

## Sources and Links

- [[SoT - FitFile Deployment - Strategy & Architecture]]
- [[SoT - Software Configuration Management Patterns]]
- [[SoT - CUE Configuration Logic]]
