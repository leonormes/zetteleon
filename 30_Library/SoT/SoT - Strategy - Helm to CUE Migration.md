---
aliases:
- Helm to CUE
- Infrastructure Refactoring
- The Strangler Fig Pattern
created: 2026-02-04 00:00:00+00:00
modified: 2026-07-04 10:50:50+00:00
permalink: llmeon/30-library/so-t/so-t-strategy-helm-to-cue-migration
tags:
- cue
- helm
- migration
- sot
- strategy
title: SoT - Strategy - Helm to CUE Migration
prodos:
  kind: sot
---


## The Strategic Goal

Move from Template-Based (Helm/Jinja2) workflows to Constraint-Based (CUE) workflows to eliminate configuration drift and "Override Hell."

## The Logic: Shadow & Strangulate

Do not "rip and replace." Use CUE to validate existing templates first, then slowly replace the generation logic.

---

## Phase 1: Shadow Validation (The Gatekeeper)

Goal: Create a mathematical proof that current config is valid without changing deployment logic.

1. Import Data: Use `cue import` to convert existing `values.yaml` files into CUE structs.
2. Generalize Schema: Create a `schema.cue` that defines the shape of your `values.yaml`.
3. CI Check (`cue vet`):
    - Render the Helm chart: `helm template > out.yaml`.
    - Validate output against CUE: `cue vet out.yaml schema.cue`.
4. Rollback Trigger: If `cue vet` fails on >10% of existing configs, the schema is too tight. Relax constraints.

---

## Phase 2: Hybrid Generation (The Data Layer)

Goal: Replace the complex `values.yaml` logic with CUE, but keep Helm for K8s resource generation.

1. Model Input: Create `config.cue` to handle environment differences (Dev vs Prod) using Unification/Defaults instead of duplication.
2. Export Values: Generate the values file: `cue export config.cue --out yaml > values.gen.yaml`.
3. Feed Helm: `helm install -f values.gen.yaml`.
4. Parity Check:
    - `diff <(cue export) <(legacy values.yaml)`
    - Must be byte-identical or logically equivalent.

---

## Phase 3: Full Unification (Total Definition)

Goal: Retire Helm templates. CUE generates K8s manifests directly.

1. Define Resources: Write `#Deployment`, `#Service` schemas in CUE.
2. Module Abstraction: Create a "Standard Service" module that abstracts boilerplate.
3. Export Manifests: `cue export > manifest.yaml`.
4. Apply: `kubectl apply -f manifest.yaml`.

---

## The Comparison Matrix

| Dimension | Helm (Template Expansion) | CUE (Unification) |
|:--- |:--- |:--- |
| Logic Model | String Concatenation | Lattice Intersection |
| Overrides | Last-Write-Wins (Destructive) | Refinement (Additive) |
| Validation | Runtime (API Server reject) | Build Time (Compile error) |
| Debug | "Where did this string come from?" | "Which constraint conflicts?" |

## Operational Risks

1. Learning Curve: Developers must unlearn "Assignment" and learn "Lattices."
2. CRD Gaps: K8s CRDs use OpenAPI. CUE can import them (`cue import openapi`), but alignment must be maintained.
3. Lossy Export: YAML is a static snapshot. You cannot round-trip YAML back to CUE without losing the logic/constraints. CUE is the Source of Truth; YAML is a build artifact.
