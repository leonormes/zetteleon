---
alias: [Configuration Migration Protocol, Helm to CUE Strategy, Shadow & Strangulate]
conformant: false
created: 2026-02-05T00:00:00+00:00
modified: 2026-07-20T16:33:55+00:00
non_conformance_reason: "Bulk inferred type. Needs review."
permalink: llmeon/30-library/so-t/protocol-helm-to-cue-migration
status: stable
tags: [cue, helm, migration, protocol, sot]
title: Protocol - Helm to CUE Migration
type: protocol
---

## Logic Map

- Objective: Transition from "Template-Based" (Helm/Jinja2) to "Constraint-Based" (CUE) configuration without downtime or regression.
- Strategy: "Shadow & Strangulate". Use CUE to validate existing outputs _before_ it generates them.
- Core Principle: Parity Verification. Every step must be mathematically provable via `diff` or `cue vet`.

---

## The Algorithm

### Phase 1: Shadow Validation (The "Read-Only" State)

_Objective: Create a mathematical proof that current configuration is valid._

1. Import: Use `cue import` on the _output_ of your current templates (rendered YAML) to derive a base schema.

```bash
helm template . > current_state.yaml
cue import current_state.yaml -p config -l 'metadata.name'
```

1. Unify: Find the common structure (Lattice Supremum) across environments.
2. Verify: Add a CI step that renders the Helm chart and validates it against the new schema.

```bash
helm template . | cue vet -d '#Deployment' schema.cue -
```

1. Rollback Trigger: If `cue vet` fails on _existing_ deployments, the schema is over-constrained. Loosen the schema.

### Phase 2: Hybrid Generation (The "Leaf-Node" Strategy)

_Objective: Replace volatile `values.yaml` with CUE, keeping heavy templates._

1. Model: Define the input parameters in CUE.
2. Export: Generate JSON from CUE to feed into Helm.
3. Parity Check: Prove that CUE-generated JSON matches the original `values.yaml`.

```bash
diff <(cue export values.cue) original-values.json
```

1. Deploy: `helm install -f <(cue export values.cue)`

### Phase 3: Full Unification (The "Source of Truth" Shift)

_Objective: Retire Helm templates. CUE generates manifests directly._

1. Lift: Move structural logic (Deployments, Services) into CUE Definitions.
2. Replace: Switch from String Injection (`{{.Values.image }}`) to Type Unification (`image: string`).
3. Verify: Use `kubectl diff` to ensure no unintended cluster state changes.

---

## Failure Mode Analysis

| Failure | Helm (Template) | CUE (Constraint) |
|:--- |:--- |:--- |
| Type Conflict | Runtime Error (Cluster rejects YAML) | Compile Error (Generation blocked) |
| Override Hell | Layer 2 silently overwrites Layer 1 | Bottom ($\bot$): Explicit Conflict Error |
| Missing Field | Empty string in YAML | Compile Error (Incomplete Value) |

_Related:_ [[SoT - CUE Configuration]]
