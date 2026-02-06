---
aliases: ["CUE Logic", "Unification Engine", "Value Lattice"]
created: 2026-02-04T00:00:00+00:00
modified: 2026-02-05T19:59:54+00:00
tags: ["configuration", "cue", "sot"]
title: SoT - CUE Configuration Logic
type: SoT
---

## Minimum Viable Understanding (MVU)

CUE (Configure Unify Execute) is a constraint-based language. Unlike Helm or Jinja2, which generate text strings, CUE manages data integrity via Unification. It treats Types as Values, meaning schemas are just generic data that get refined into specific data.

---

## 1. The Value Lattice (Hierarchy of Specificity)

CUE values sit on a spectrum from General to Specific.

```
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

### Types Are Values

There is no distinction between "Schema" and "Data".

- `port: int` is a value (Infinite set of integers).
- `port: 8080` is a value (Set of size 1).
- Validation is just checking if the specific value fits within the general value.

---

## 2. Unification vs. Assignment

### Assignment (Imperative/Helm)

Variables are containers. Later values overwrite earlier ones.

```python
x = 5
x = 6  # x is now 6. History is lost.
```

### Unification (Declarative/CUE)

Variables are constraints. Values are merged (The Meet Operation).

```cue
x: int
x: >5
x: 6   # Valid: 6 is an int AND >5.
```

If you attempt:

```cue
x: 6
x: 7   # Error: Bottom (⊥). A value cannot be 6 AND 7.
```

Key Property: Unification is Commutative.

`Constraint A & Constraint B` is identical to `Constraint B & Constraint A`. This solves the "Override Hell" of layered YAML files.

---

## 3. Failure Modes as Features

In template systems (Helm), conflicts often result in invalid YAML being generated and rejected by the Kubernetes API at runtime. In CUE, conflicts are Compile-Time Errors.

| Failure Type | Helm Behavior | CUE Behavior |
|:--- |:--- |:--- |
| Type Mismatch | Silent coercion or runtime crash. | `string & int` → $\bot$ (Error). |
| Constraint Violation | Template renders, API rejects. | `>10 & 5` → $\bot$ (Error). |
| Missing Field | Renders `<no value>`. | Struct fails to close. Error. |

GitOps Benefit: Errors are caught in CI (Build Time), not in the Cluster (Deploy Time).

---

## 4. Comparison: CUE vs. The World

| Metric | Helm / Kustomize | CUE |
|:--- |:--- |:--- |
| Schema Enforcement | External/Late. JSONSchema is separate from logic. Often skipped. | Intrinsic. Types _are_ the logic. You cannot write invalid config. |
| Composition | Fragile. String interpolation or patches. Sensitive to order. | Robust. Mathematical unification. Order independent. |
| Error Locality | Poor. Errors appear in output YAML, far from the source. | Precise. Traces conflict to specific lines in source files. |

---

## 5. Tooling Friction (The Cost)

Adopting CUE introduces specific operational friction:

1. Export/Import: Kubernetes speaks YAML, not CUE. You must compile (`cue export`) before applying. The "State of the World" (YAML) is a lossy projection of the "Source of Truth" (CUE).
2. Ecosystem Isolation: Vendors supply Helm Charts. You must either wrap them (importing rendered YAML) or rewrite them.
3. Non-Monotonicity: Developers used to "overriding" values (e.g., `image: latest` in dev, `image: v1` in prod) must learn to use Disjunctions and Defaults instead.
