---
aliases: [Pattern - Data Centric IaC]
created: 2026-01-07T10:14:28+00:00
last_reviewed: 2026-01-07
modified: 2026-07-04T10:51:48+00:00
permalink: llmeon/30-library/100-zettelkasten/pattern-helm-chart-as-a-compiler
status: stable
tags: [devops, helm, pattern, SoftwareEngineering/Architecture]
title: Pattern - Helm Chart as a Compiler
type: concept
---

## Pattern: Helm Chart as a Compiler

> [!abstract] The Concept
> Move infrastructure configuration from a Wrapper model (exposing vendor flags) to a Compiler model (expanding Intent into Configuration).
> Goal: The user declares _Service Level Objectives_ (SLA), and the system generates the _Implementation Details_.

---

### 1. The Core Philosophy

This pattern applies Data-Oriented Design to DevOps.

#### The Shift

| Feature | Wrapper Pattern (Old) | Compiler Pattern (New) |
|:--- |:--- |:--- |
| Input | `replicas: 3`, `cpu: 2000m` | `class: production-ha` |
| Logic | `if.Values.enabled` | Table Lookup (`_specs.yaml`) |
| Validation | Runtime Errors (Invalid Config) | Unrepresentable States (Enum) |
| Role | Pass-through | Transformer |

#### The "Torvalds Loop" for IaC

1. Shape (The Type): Define the business intent. (e.g., "Mission Critical" vs "Dev").
2. Data (The Spec): Create a lookup table that maps Types to physical values.
3. Logic (The Adapter): Write code that purely transforms Data -> Config.

---

### 2. Implementation Strategy

#### Phase 1: The Shape (Intent Schema)

Reduce the user interface (`values.yaml`) to the absolute minimum.

```yaml
# User Input (Intent)
database:
  class: "mission-critical"  # The Intent
  vendor: "bitnami"          # The Provider
```

#### Phase 2: The Data (Structure of Arrays)

Replace conditional logic with a Spec Table (`_specs.yaml`). This is the "Source of Truth".

```yaml
# Internal Specs (The Truth)
_specs:
  classes:
    mission-critical:
      topology: "ha"         # Implies 3 replicas + Arbiter
      resources: "large"     # Implies 4GB RAM / 2 vCPU
      backup: true
```

#### Phase 3: The Logic (Compiler)

The template acts as an adapter. It does not decide _what_ to do; it only decides _how_ to format the instruction for the specific vendor.

```yaml
# The Compiler Logic
{{- $spec := index .Values._specs.classes .Values.database.class -}}

{{- if eq $spec.topology "ha" -}}
  # Compiler automatically sets valid HA config
  replicaCount: 3
  podDisruptionBudget: { minAvailable: 2 }
{{- end -}}
```

---

### 3. Benefits

1. Zero Human Error: Users cannot accidentally set `replicas: 1` on a `mission-critical` database. The state is unrepresentable.
2. Hardware Sympathy: Resources are defined in "T-Shirt Sizes" (Profiles) that match physical node pools, ensuring perfect bin-packing.
3. Vendor Agnosticism: Switching from Bitnami to AWS RDS only requires changing the Compiler Logic, not the User Intent.

## ## Pattern: Helm Chart as a Compiler

- [[SoT - Simple Made Easy (Rich Hickey)]]: The "Compiler Pattern" is a form of decomplecting, separating the _what_ (Intent Data) from the _how_ (Adapter Logic).
