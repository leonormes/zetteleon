---
alias: ["Forensic Chart Analysis", "Helm Refactoring Strategy", "Tesler's Law Application"]
created: 2026-02-05T00:00:00+00:00
modified: 2026-02-05T17:41:10+00:00
status: stable
tags: ["architecture", "helm", "protocol", "refactoring", "sot"]
title: Protocol - Legacy Helm Refactoring
type: protocol
---

## Logic Map

- Objective: Refactor legacy "God Charts" by shifting complexity from the User (manual flags) and the Code (templates) to the Data (Schema).
- Theory: Based on [[SoT - Conservation of Complexity]] (Tesler's Law).
- Outcome: A "Compiler" style chart where invalid states are unrepresentable.

---

## The Algorithm

### Phase 1: The "Profile" Abstraction (Interface)

_Goal: Eliminate the "Boolean Swamp"._

- Action: Replace loose boolean flags (`enableMonitoring`, `enableHA`) with a single `profile` enum.
- Mechanism: The chart loads a `profiles.yaml`.
- Logic: `if profile == "prod-ha"` $\rightarrow$ automatically sets `replicas: 3`, `pdb: true`, `monitoring: true`.

### Phase 2: The Canonical Secret Registry (Data)

_Goal: Remove "Templating in YAML"._

- Action: Implement a Registry where the chart defines _Requirements_ (`mongo_password`) and the user defines _Sources_ (`vault_path`).
- Mechanism: Recursive template helper generating `ExternalSecret` manifests.
- Benefit: The user never writes Go templates; they just map keys.

### Phase 3: The Unified Graph (Topology)

_Goal: Solve "Connectivity Complexity"._

- Action: Centralize network truth.
- Mechanism: Users configure `global.topology`. Sub-charts import this to derive `DB_HOST` and `API_URL`.
- Benefit: Removes the "N+1" update problem where every sub-chart needs manual overrides.

### Phase 4: Strict Validation (Compiler)

_Goal: Enforce the API Contract._

- Action: Implement `values.schema.json`.
- Mechanism: Use `oneOf` and `if/then` logic to reject invalid configs at `helm install` time.

---

## Tooling: The Forensic Prompt

_Use this prompt to analyze a legacy chart's complexity distribution._

> System Role: Senior Systems Architect (Kubernetes/DDD).
> Context: Refactoring a legacy Helm chart suffering from "Pass-Through Complexity".
> Task: Conduct a forensic analysis of `values.yaml`.
> 1. Complexity Heatmap: Where is the user "squeezing the balloon"? (e.g., manually linking dependencies).
> 2. Formal Data API: Draft a TypeScript interface for a new, strict `values.yaml`.
> 3. Validation Logic: Define the JSON Schema invariants (e.g., "If `prod`, `vault` must be true").

_Related:_ [[Pattern - Helm Chart as a Compiler]]
