---
aliases:
- Configure Unify Execute
- CUE Configuration
- CUE Lang
- CUE Logic
- Unification Engine
- Value Lattice
created: 2026-02-03 19:15:00+00:00
last_synthesis: 2026-04-02
modified: 2026-05-26 11:44:20+00:00
source_of_truth: true
status: evergreen
synthesis-count: 2
tags:
- configuration-management
- cue
- infrastructure-as-code
- prodos/sot
- tool/cue
title: SoT - CUE Configuration
trust-level: stable
type: SoT
permalink: llmeon/30-library/so-t/so-t-cue-configuration
---

## Minimum Viable Understanding (MVU)

CUE (Configure Unify Execute) is a configuration language based on Order Theory (Lattices). Unlike Helm (Text Templating) or Kustomize (Patching), CUE manages configuration through Unification: combining constraints to refine values. It treats "Types" as "Values," enabling intrinsic validation where conflict is a compile-time feature, not a runtime bug.

---

## 1. Theoretical Foundation: The Value Lattice

_For the mathematical basis, see [[SoT - Order Theory & Lattices]]._

### The Core Shift: Types Are Values

In CUE, a schema is not a separate validation layer; it is simply less specific data. Values sit on a spectrum from General (Top) to Specific (Concrete).

```text
        ⊤ (top) — "anything at all"
        │
      string — "any string"
        │
    =~"^[a-z]+$" — "lowercase strings only"
        │
      "hello" — "exactly this string"
        │
        ⊥ (bottom) — "contradiction / error"
```

- `port: int` is a value (Infinite set of all integers).
- `port: >1024` (A set of integers > 1024).
- `port: 8080` (A concrete value / set of size 1).

Unification (`&`) computes the intersection. If the intersection is empty (e.g., `>1024 & 80`), the result is Bottom (⊥), representing an invalid configuration.

---

## 2. Unification vs. Assignment

### Assignment (Imperative/Helm)

Variables are containers. Later values overwrite earlier ones. History and intent are lost.

```python
x = 5
x = 6  # x is now 6.
```

### Unification (Declarative/CUE)

Variables are constraints. Values are merged (The Meet Operation). Unification is Commutative ($A \cap B = B \cap A$), solving "Override Hell."

```cue
x: int
x: >5
x: 6   # Valid: 6 is an int AND >5.

x: 6
x: 7   # Error: Bottom (⊥). A value cannot be 6 AND 7.
```

---

## 3. Failure Modes as Features

In template systems, conflicts often result in invalid YAML rejected at runtime. In CUE, conflicts are Compile-Time Errors caught in CI.

| Failure Type | Helm/Jinja Behavior | CUE Behavior |
|:--- |:--- |:--- |
| Type Mismatch | Silent coercion or runtime crash. | `string & int` → ⊥ (Error). |
| Constraint Violation | Template renders, API rejects. | `>10 & 5` → ⊥ (Error). |
| Missing Field | Renders `<no value>`. | Struct fails to close. Error. |
| Override Conflict | Silent overwrite (Last wins). | Explicit Error (Conflict). |

---

## 4. Comparative Analysis: CUE vs. The World

| Metric | Helm / Jinja (Templating) | Kustomize (Patching) | CUE (Unification) |
|:--- |:--- |:--- |:--- |
| Model | String Interpolation | Strategic Merge Patch | Mathematical Unification |
| Schema Enforcement | Late/External. | None/Late. | Intrinsic. Types are values. |
| Composition | Fragile. Order-dependent. | Fragile. Position-dependent. | Robust. Commutative. |
| Error Locality | Poor. Appears in output. | Medium. Appears at apply. | High. Traces to source line. |

---

## 5. Strategic Patterns

### 5.1 The "Secret Intent" Pattern

Use Disjunctions (`|`) to define mutually exclusive schemas for sensitive data. This forces the user to provide exactly the required fields for a specific source (e.g., Vault vs. K8s Secret).

```cue
#SecretIntent: {
    source: "vault"
    path:   string
} | {
    source: "k8s-secret"
    name:   string
}
```

### 5.2 Profile-Based Invariants

Enforce environment-specific rules (e.g., "Production must use Vault") via conditional constraints.

```cue
if profile == "prod" {
    capabilities: secrets: source: "vault"
}
```

---

## 6. Operational Risks (The Friction)

1. Export/Import Friction: Kubernetes speaks YAML, not CUE. You must compile (`cue export`) before applying. The "State of the World" (YAML) is a lossy projection of the "Source of Truth" (CUE).
2. Ecosystem Isolation: Vendors ship Helm Charts, not CUE modules. You must wrap or rewrite them, incurring maintenance debt.
3. Non-Monotonicity: Developers must shift from "overriding" (destructive) to "refining" or using Defaults (`*value | T`).

---

## Related Knowledge

- Protocol: [[Protocol - Helm to CUE Migration]] (The Strangler Fig Pattern).
- Theory: [[SoT - Order Theory & Lattices]] (Lattices and Partial Orders).
- Strategy: [[SoT - Type-Driven Infrastructure Strategy]].
- Framework: [[SoT - Generative Infrastructure Configuration Framework]].