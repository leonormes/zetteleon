---
aliases: ["CUE Migration Strategy", "Helm to CUE Strangler Fig"]
created: 2026-02-03T19:20:00+00:00
last_synthesis: 2026-02-03
modified: 2026-02-04T07:26:38+00:00
source_of_truth: true
status: evergreen
synthesis-count: 1
tags: ["cue", "migration", "protocol", "refactoring"]
title: Protocol - Helm to CUE Migration
trust-level: stable
type: "protocol"
---

## Logic Map

- Objective: Migrate a legacy Helm-based infrastructure to CUE without a "Big Bang" rewrite.
- Strategy: The "Strangler Fig" pattern. Wrap the old system, validate it, then slowly replace its internals.
- Constraint: Zero downtime. CI/CD must pass at every stage.

---

## The Algorithm

### Phase 1: Validation (The Gatekeeper)

_Goal: Stop bad config from reaching the cluster using CUE's rigorous typing, without replacing Helm._

1. Define Schema: Create `schema.cue` for critical resources (e.g., `deployment.cue`).
2. Render Helm: In CI, run `helm template > out.yaml`.
3. Vet: Run `cue vet out.yaml schema.cue`.
4. Result: Helm still drives, but CUE catches type errors before apply.

### Phase 2: The Data Layer (Parameter Unification)

_Goal: Solve "Override Hell" in `values.yaml`._

1. Ingest: Import complex `values.yaml` into CUE (`cue import values.yaml`).
2. Unify: Use CUE to generate environment-specific values (dev/prod) using lattice unification.
3. Inject: Export back to JSON: `cue export env/prod.cue > values.json`.
4. Deploy: `helm install -f values.json`.
5. Result: CUE manages the _configuration logic_; Helm is downgraded to a simple template engine.

### Phase 3: Total Definition (Full Unification)

_Goal: Eliminate Helm templates for internal services._

1. Define Objects: Write Kubernetes objects directly in CUE.
2. Module Abstraction: Create a `#Service` module to abstract boilerplate.
3. Export: CI step: `cue export > manifest.yaml`.
4. Apply: `kubectl apply -f manifest.yaml`.
5. Result: Pure CUE pipeline.

---

## Error Handling

- If `cue vet` fails in Phase 1: Do not block deploy immediately. Run in "Warn" mode until schema is mature.
- If Vendor Charts change: Use Phase 2 (CUE generating values) rather than Phase 3 (Rewriting the chart).

## Unit Test

- Pass Criteria: `cue export` produces YAML that is byte-for-byte identical (or semantically equivalent) to the legacy Helm output during the transition.
