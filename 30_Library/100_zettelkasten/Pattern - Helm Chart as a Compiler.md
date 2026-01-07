---
confidence: high
epistemic: confirmed
purpose: "Define the Data-Centric pattern for Infrastructure as Code"
modified: 2026-01-07T14:56:29+00:00
last_reviewed: 2026-01-07
review_interval: yearly
see_also: 
  - "[[Refactor: Helm Chart Compiler]]"
source_of_truth: []
aliases:
  - "Pattern - Data Centric IaC"
created: 2026-01-07T10:14:28+00:00
status: stable
tags:
  - pattern
  - "SoftwareEngineering/Architecture"
  - helm
  - devops
title: "Pattern: Helm Chart as a Compiler"
type: concept
---

# Pattern: Helm Chart as a Compiler

> [!abstract] The Concept
> Move infrastructure configuration from a **Wrapper** model (exposing vendor flags) to a **Compiler** model (expanding Intent into Configuration).
> **Goal:** The user declares *Service Level Objectives* (SLA), and the system generates the *Implementation Details*.

---

## 1. The Core Philosophy

This pattern applies **Data-Oriented Design** to DevOps.

### The Shift

| Feature | Wrapper Pattern (Old) | Compiler Pattern (New) |
|:--- |:--- |:--- |
| **Input** | `replicas: 3`, `cpu: 2000m` | `class: production-ha` |
| **Logic** | `if.Values.enabled` | Table Lookup (`_specs.yaml`) |
| **Validation** | Runtime Errors (Invalid Config) | **Unrepresentable States** (Enum) |
| **Role** | Pass-through | Transformer |

### The "Torvalds Loop" for IaC

1. **Shape (The Type):** Define the business intent. (e.g., "Mission Critical" vs "Dev").
2. **Data (The Spec):** Create a lookup table that maps Types to physical values.
3. **Logic (The Adapter):** Write code that purely transforms Data -> Config.

---

## 2. Implementation Strategy

### Phase 1: The Shape (Intent Schema)

Reduce the user interface (`values.yaml`) to the absolute minimum.

```yaml
# User Input (Intent)
database:
  class: "mission-critical"  # The Intent
  vendor: "bitnami"          # The Provider
```

### Phase 2: The Data (Structure of Arrays)

Replace conditional logic with a **Spec Table** (`_specs.yaml`). This is the "Source of Truth".

```yaml
# Internal Specs (The Truth)
_specs:
  classes:
    mission-critical:
      topology: "ha"         # Implies 3 replicas + Arbiter
      resources: "large"     # Implies 4GB RAM / 2 vCPU
      backup: true
```

### Phase 3: The Logic (Compiler)

The template acts as an adapter. It does not decide *what* to do; it only decides *how* to format the instruction for the specific vendor.

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

## 3. Benefits

1. **Zero Human Error:** Users cannot accidentally set `replicas: 1` on a `mission-critical` database. The state is unrepresentable.
2. **Hardware Sympathy:** Resources are defined in "T-Shirt Sizes" (Profiles) that match physical node pools, ensuring perfect bin-packing.
3. **Vendor Agnosticism:** Switching from Bitnami to AWS RDS only requires changing the **Compiler Logic**, not the **User Intent**.
