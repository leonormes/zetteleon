---
created: 2026-02-05T21:05:00+00:00
modified: 2026-07-04T10:50:45+00:00
permalink: llmeon/30-library/ops/protocol-legacy-to-cue-migration-strategy
status: active
tags: [cue, devops, helm, infra, migration, protocol]
title: Protocol - Legacy-to-CUE Migration Strategy
trust-level: high
type: protocol
---

> Objective: Safely migrate from legacy configuration (Helm/YAML) to CUE without service interruption.
> Core Logic: "Shadow Validation -> Hybrid Generation -> Full Unification".
> Success Criteria: CUE output bitwise matches legacy output (SHA-256 parity) before switchover.

## 1. Logic Map & Prerequisites

### Dependencies

- Tools: `cue` (latest), `helm`, `kubectl`, `yq`, `diff`.
- Access: Read access to legacy charts, Write access to CI pipelines.
- Baseline: Ability to generate deterministic output from legacy templates (`helm template`).

### The Phases

1. Phase 0: Audit: Inventory templates and establish drift baseline.
2. Phase 1: Shadow Validation: CUE validates legacy output; no generation. (Risk: Zero).
3. Phase 2: Hybrid Generation: CUE takes over "Type A" resources (ConfigMaps); Helm handles the rest. (Risk: Low).
4. Phase 3: Unification: Full CUE generation; Helm removed. (Risk: Medium).

---

## 2. The Algorithm

### Phase 0: Pre-Flight Audit

1. Baseline Generation

```bash
helm template my-chart -f values-prod.yaml > baseline-prod.yaml
sha256sum baseline-prod.yaml > baseline.checksums
```

1. Template Categorization
    - _Type A_: Static substitution (ConfigMaps).
    - _Type B_: Conditionals.
    - _Type C_: Loops.
    - _Type D_: Macros/Functions.

### Phase 1: Schema Extraction (Shadow Mode)

1. Import & Generalize

```bash
cue import baseline-dev.yaml --path 'dev' --out cue
cue trim baseline-dev.cue baseline-prod.cue --out schema.cue
```

1. Validate Legacy Output (CI Job)
    - Add non-blocking CI step: `cue vet schema.cue legacy-output.yaml`.
    - _Success:_ `cue vet` passes >98% of runs for 2 weeks.

### Phase 2: Hybrid Generation (The Strangler Pattern)

1. Migrate Type A Resource (e.g., ConfigMap)
    - Write CUE definition.
    - Verify Parity:

```bash
diff <(yq eval ... helm-out.yaml) <(cue export ... cue-out.yaml)
```

1. Hybrid Deploy Script

```bash
# Generate CUE parts
cue export cue/${ENV}.cue -e configMap > manifest-cue.yaml
# Generate Helm parts
helm template ... > manifest-helm.yaml
# Merge
cat manifest-cue.yaml manifest-helm.yaml | kubectl apply -f -
```

### Phase 3: Full Unification

1. Composition
    - Migrate complex logic (Deployments, Services) to CUE structs.
    - Use `tool.cue` for standardized generation commands.
2. Final Cutover
    - Remove Helm step from CI.
    - Archive Helm charts.

---

## 3. Error Handling & Rollback

| Scenario | Trigger | Action |
|:--- |:--- |:--- |
| Schema Too Strict | `cue vet` fails on valid legacy config | Loosen constraints in `schema.cue`; re-trim. |
| Parity Mismatch | `diff` shows non-whitespace changes | STOP. Do not apply. Debug CUE logic to match legacy exactly. |
| Deletion Risk | `kubectl diff` shows resource deletion | STOP. Check if CUE output filename/metadata matches legacy exactly. |
| Prod Incident | Bug traced to CUE manifest | Emergency Revert: `kubectl apply -f baseline-prod.yaml` (Last known good Helm output). |

---

## 4. Verification (Unit Test)

To verify the migration is safe to proceed to the next step:

1. Deterministic Output: Running the generator twice produces identical SHA sums.
2. Legacy Match: `cue export` output matches `helm template` baseline (ignoring whitespace/comments).
