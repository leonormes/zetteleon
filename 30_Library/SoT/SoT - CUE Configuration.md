---
aliases: ["Configure Unify Execute", "CUE Configuration", "CUE Lang"]
created: 2026-02-03T19:15:00+00:00
last_synthesis: 2026-02-03
modified: 2026-02-03T20:24:13+00:00
source_of_truth: true
status: evergreen
synthesis-count: 1
tags: ["configuration-management", "cue", "infrastructure-as-code", "prodos/sot", "tool/cue"]
title: SoT - CUE Configuration
trust-level: stable
type: "SoT"
---

## Minimum Viable Understanding (MVU)

CUE (Configure Unify Execute) is a configuration language based on Order Theory (Lattices). Unlike Helm (Text Templating) or Kustomize (Patching), CUE manages configuration through Unification: combining constraints to refine values. It treats "Types" as "Values," enabling intrinsic validation where conflict is a compile-time feature, not a runtime bug.

---

## 1. Theoretical Foundation

_For the mathematical basis, see [[SoT - Order Theory]]._

### The Core Shift: Types Are Values

In CUE, a schema is not a separate validation layer; it is simply less specific data.

- `port: int` (A set of all integers).
- `port: >1024` (A set of integers > 1024).
- `port: 8080` (A concrete value).
Unification (`&`) computes the intersection. If the intersection is empty (e.g., `>1024 & 80`), the config is invalid.

---

## 2. Comparative Analysis: CUE vs. The World

| Metric | Helm / Jinja (Templating) | Kustomize (Patching) | CUE (Unification) |
|:--- |:--- |:--- |:--- |
| Model | String Interpolation | Strategic Merge Patch | Mathematical Unification |
| Schema Enforcement | Late/External. Schemas are separate JSON files, often ignored. | None/Late. Relies on API server validation. | Intrinsic. Types are values. Invalid config cannot be expressed. |
| Composition | Fragile. Order-dependent. "Override Hell" (Silent overwrites). | Fragile. Position-dependent overlays. | Robust. Commutative (`A & B == B & A`). Conflicts are explicit errors. |
| Error Locality | Poor. Errors appear in generated YAML or at runtime. | Medium. Errors at apply time. | High. Errors trace back to the specific conflicting constraint line. |

### The "Override Hell" Problem

- Helm: Layer 2 sets `replicas: 4`, silently overwriting Layer 1's `replicas: 2`. Intent is lost.
- CUE: Layer 2 defines `replicas: 4`. CUE throws a conflict error because `2!= 4`. You must explicitely _refine_ or _default_, not overwrite.

---

## 3. Strategic Critique: Operational Risks

While theoretically superior, CUE introduces friction in a Kubernetes/YAML world.

### 3.1 The "Export/Import" Friction

Kubernetes speaks YAML, not CUE.

- The Disconnect: You must compile (`cue export`) before applying. The "State of the World" (YAML) is a lossy projection of the "Source of Truth" (CUE).
- No Round-Trip: You cannot perfectly reverse-engineer CUE constraints from generated YAML.

### 3.2 Ecosystem Isolation

Vendors ship Helm Charts, not CUE modules.

- The Burden: You must wrap Helm charts (importing rendered YAML into CUE) or rewrite them. Rewriting offers purity but incurs high maintenance debt.

---

## 4. Related Knowledge

- Protocol: [[Protocol - Helm to CUE Migration]] (The Strangler Fig Pattern).
- Theory: [[SoT - Order Theory]] (Lattices and Partial Orders).
- Strategy: [[SoT - Type-Driven Infrastructure Strategy]] (The broader paradigm).
