---
created: 2026-02-05T10:29:29+00:00
modified: 2026-02-05T11:10:31+00:00
title: Legacy-to-CUE Migration Framework Incremental Refactoring Strategy
---

## Acknowledgment: Your Strategic Framing is Sound

Your "Shadow Validation → Hybrid Generation → Full Unification" approach is the only production-safe path. The key insight: CUE must first prove it can replicate legacy behavior before it replaces legacy tooling. This is a formal verification problem, not a code cleanup exercise.

---

## Phase 0: Pre-Flight Audit (Before You Provide Code)

Before analyzing specific templates, conduct this systematic inventory:

### 1. Template Inventory Checklist

```bash
# Map your current configuration surface area
find . -name "*.yaml" -o -name "*.yml" -o -name "*.json" | wc -l
# → How many files need migration?

grep -r "{{" . --include="*.yaml" | wc -l
# → How many template interpolations exist?

grep -r "{% if" . --include="*.yaml" | wc -l
# → How many conditional branches?

grep -r "{% for" . --include="*.yaml" | wc -l
# → How many loops/iterations?
```

Categorize templates by complexity:
- Type A (Static + Simple substitution): `{{.Values.name }}` only
- Type B (Conditionals): `{% if.Values.enabled %}`
- Type C (Iteration): `{% for item in.Values.list %}`
- Type D (Functions/Macros): `{{ include "myapp.labels". }}`

Migration Priority: A → D (simplest first, prove the model works)

### 2. Schema Presence Check

```bash
# Do you have explicit schemas?
find . -name "*schema.json" -o -name "*openapi.yaml"

# Do you have validation layers?
grep -r "required:" . --include="*.yaml"
grep -r "pattern:" . --include="*.yaml"
```

Schema Maturity Levels:
- Level 0: No schema (pure YAML with implicit types)
- Level 1: Inline validation (Helm values.schema.json)
- Level 2: External schema (OpenAPI/JSONSchema)
- Level 3: Runtime validation (OPA policies, admission webhooks)

CUE Benefit Matrix:

| Schema Level | CUE Value Proposition |
|--------------|----------------------|
| 0 | High (CUE replaces tribal knowledge) |
| 1 | High (CUE unifies schema + data) |
| 2 | Medium (CUE adds cross-field constraints) |
| 3 | Low (You already have strong guarantees) |

### 3. Drift Detection Baseline

```bash
# Establish current "ground truth" outputs
helm template my-chart -f values-dev.yaml > baseline-dev.yaml
helm template my-chart -f values-prod.yaml > baseline-prod.yaml

# Checksum for byte-level comparison
sha256sum baseline-*.yaml > baseline.checksums
```

Critical: These baselines are your acceptance test. CUE migration succeeds only if:

```bash
cue export ./cue/dev.cue --out yaml | sha256sum
# → MUST match baseline-dev.yaml checksum (or have documented diffs)
```

---

## Phase 1: Schema Extraction & Shadow Validation (Weeks 1-3)

Goal: CUE validates existing outputs without generating anything.

### Step 1.1: Import Existing Data → CUE Schemas

```bash
# Convert a sample YAML to CUE
cue import baseline-dev.yaml --path 'dev' --out cue
# Produces: baseline-dev.cue

# Generalize the schema
cue trim baseline-dev.cue baseline-prod.cue --out schema.cue
# Produces: schema.cue (common constraints across envs)
```

Example Output (`schema.cue`):

```cue
package config

#Deployment: {
    apiVersion: "apps/v1"
    kind: "Deployment"
    metadata: {
        name: string
        namespace: string
    }
    spec: {
        replicas: int & >0 & <100  // CUE inferred bounds from samples
        template: {
            spec: {
                containers: [...{
                    name: string
                    image: string
                    resources: {
                        limits?: {
                            cpu?: string
                            memory?: string
                        }
                    }
                }]
            }
        }
    }
}
```

Verification Command:

```bash
# Does the schema accept existing data?
cue vet schema.cue baseline-dev.yaml
# Exit 0 = schema is valid, Exit 1 = schema too restrictive
```

Rollback Trigger: If `cue vet` fails on >10% of existing configs, the schema is over-constrained. Loosen bounds, re-trim.

### Step 1.2: Add Business Constraints (Not in Legacy System)

```cue
// schema.cue (enhanced)
#Deployment: {
    // ... existing fields ...
    
    // NEW: Enforce relationship between HPA and deployment
    if spec.replicas > 1 {
        metadata: annotations: "autoscaling.enabled": "true"
    }
    
    // NEW: CPU requests must exist if limits exist
    spec: template: spec: containers: [...{
        resources: {
            if limits != _|_ {
                requests: cpu: string  // Required if limits exist
            }
        }
    }]
}
```

Verification Command:

```bash
# Does the enhanced schema still accept legacy data?
cue vet schema.cue baseline-dev.yaml -c
# -c = "concrete" mode, ensures all constraints are satisfiable
```

Rollback Trigger: New constraints fail on >5% of baselines → constraints encode aspirational policy, not current reality. Document as "Phase 3 cleanup items."

### Step 1.3: CI Integration (Shadow Mode)

```yaml
# .gitlab-ci.yml
validate-cue-shadow:
  stage: validate
  script:
    # Generate YAML using legacy tooling
    - helm template my-chart -f values-${ENV}.yaml > legacy-output.yaml
    
    # Validate with CUE schema
    - cue vet schema.cue legacy-output.yaml
    
    # Allow failure (shadow mode - doesn't block deployment)
  allow_failure: true
  
  artifacts:
    when: on_failure
    reports:
      junit: cue-validation-report.xml
```

Success Metric: Run shadow validation for 2 weeks. If `allow_failure` is triggered <2% of the time, proceed to Phase 2.

---

## Phase 2: Hybrid Generation (Weeks 4-8)

Goal: CUE generates a subset of configuration while Helm generates the rest. Outputs are merged.

### Step 2.1: Identify "Low-Hanging Fruit" (Type A Templates)

Criteria for CUE-first migration:
1. Static structure (no loops)
2. Simple substitution (no complex functions)
3. High duplication (ConfigMaps, Secrets, common labels)

Example: Migrate `ConfigMap` generation to CUE.

Before (Helm template):

```yaml
# templates/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ .Release.Name }}-config
  namespace: {{ .Release.Namespace }}
data:
  APP_NAME: {{ .Values.app.name }}
  LOG_LEVEL: {{ .Values.app.logLevel }}
```

After (CUE):

```cue
// cue/configmap.cue
package k8s

import "strings"

#ConfigMap: {
    _input: {
        releaseName: string
        namespace: string
        app: {
            name: string
            logLevel: "debug" | "info" | "warn" | "error"  // Enum constraint
        }
    }
    
    apiVersion: "v1"
    kind: "ConfigMap"
    metadata: {
        name: "\(_input.releaseName)-config"
        namespace: _input.namespace
    }
    data: {
        APP_NAME: _input.app.name
        LOG_LEVEL: strings.ToUpper(_input.app.logLevel)  // CUE function
    }
}

// cue/dev.cue
package k8s

configMap: #ConfigMap & {
    _input: {
        releaseName: "myapp-dev"
        namespace: "development"
        app: {
            name: "myapp"
            logLevel: "debug"
        }
    }
}
```

Generation Command:

```bash
cue export cue/dev.cue --expression 'configMap' --out yaml > cue-configmap.yaml
```

Parity Verification:

```bash
# Generate both outputs
helm template my-chart -f values-dev.yaml | yq eval 'select(.kind == "ConfigMap")' > helm-configmap.yaml
cue export cue/dev.cue --expression 'configMap' --out yaml > cue-configmap.yaml

# Semantic diff (ignore whitespace, key order)
diff <(yq eval --sort-keys helm-configmap.yaml) \
     <(yq eval --sort-keys cue-configmap.yaml)
# Exit 0 = byte-identical (SUCCESS)
```

Rollback Trigger: If diff shows ANY unexpected changes (not just whitespace), revert CUE changes. Re-analyze template logic.

### Step 2.2: Merge Outputs (Hybrid Pipeline)

```bash
#!/bin/bash
# deploy.sh (hybrid generation)

# CUE generates ConfigMaps/Secrets
cue export cue/${ENV}.cue --expression 'configMap' --out yaml > cue-outputs/configmap.yaml
cue export cue/${ENV}.cue --expression 'secret' --out yaml > cue-outputs/secret.yaml

# Helm generates Deployments/Services (still in Helm)
helm template my-chart -f values-${ENV}.yaml > helm-outputs/manifests.yaml

# Merge and apply
cat cue-outputs/*.yaml helm-outputs/manifests.yaml | kubectl apply -f -
```

Verification:

```bash
# Before applying, dry-run diff
kubectl diff -f <(cat cue-outputs/*.yaml helm-outputs/manifests.yaml)
# Review changes manually before apply
```

Rollback Trigger: If `kubectl diff` shows deletion of existing resources, STOP. Investigate why CUE/Helm outputs overlap.

### Step 2.3: Incremental Template Removal

Strategy: Remove one Helm template per sprint, replace with CUE.

```
Sprint 1: ConfigMap (done in Step 2.1)
Sprint 2: Secret
Sprint 3: ServiceAccount + RBAC
Sprint 4: Service
Sprint 5: Deployment (most complex, last)
```

Per-Sprint Checklist:
- [ ] CUE schema defined
- [ ] `cue export` matches Helm output (diff verified)
- [ ] Helm template deleted
- [ ] CI updated to merge CUE + Helm outputs
- [ ] Deployed to staging without incident
- [ ] 1-week soak test (no rollbacks)

---

## Phase 3: Full Unification (Weeks 9-12)

Goal: Helm is completely removed. CUE is the single source of truth.

### Step 3.1: Multi-Environment Composition

Structure:

```
cue/
├── schema/
│   ├── deployment.cue   # #Deployment definition
│   ├── service.cue      # #Service definition
│   └── configmap.cue    # #ConfigMap definition
├── base/
│   └── defaults.cue     # Shared constraints across envs
├── environments/
│   ├── dev.cue          # Dev-specific values
│   ├── staging.cue      # Staging-specific values
│   └── prod.cue         # Prod-specific values
└── tool.cue             # CUE commands for generation
```

Example (`base/defaults.cue`):

```cue
package config

#BaseConfig: {
    app: {
        name: string & =~"^[a-z0-9-]+$"
        version: string & =~"^v[0-9]+\\.[0-9]+\\.[0-9]+$"
    }
    
    deployment: {
        replicas: int & >0
        resources: {
            requests: {
                cpu: string
                memory: string
            }
            limits: {
                cpu: string & >=resources.requests.cpu  // Constraint
                memory: string & >=resources.requests.memory
            }
        }
    }
}
```

Example (`environments/prod.cue`):

```cue
package config

import (
    "github.com/myorg/myapp/cue/schema"
    "github.com/myorg/myapp/cue/base"
)

// Prod inherits base constraints, adds specifics
prodConfig: base.#BaseConfig & {
    app: {
        name: "myapp"
        version: "v1.2.3"
    }
    
    deployment: {
        replicas: 10
        resources: {
            requests: {
                cpu: "1000m"
                memory: "2Gi"
            }
            limits: {
                cpu: "2000m"
                memory: "4Gi"
            }
        }
    }
}

// Generate K8s manifests
deployment: schema.#Deployment & {_input: prodConfig}
service: schema.#Service & {_input: prodConfig}
configMap: schema.#ConfigMap & {_input: prodConfig}
```

### Step 3.2: CUE Commands (Reproducible Generation)

Define generation logic (`tool.cue`):

```cue
package config

import (
    "tool/cli"
    "tool/file"
    "encoding/yaml"
)

command: generate: {
    // Read environment input
    env: cli.Ask & {
        prompt: "Environment (dev/staging/prod):"
    }
    
    // Export YAML
    manifests: file.Create & {
        filename: "manifests/\(env.response).yaml"
        contents: yaml.MarshalStream([
            deployment,
            service,
            configMap,
        ])
    }
}

command: validate: {
    // Validate all environments
    dev: file.Glob & {glob: "environments/dev.cue"}
    staging: file.Glob & {glob: "environments/staging.cue"}
    prod: file.Glob & {glob: "environments/prod.cue"}
    
    // CUE automatically validates during import
}
```

Usage:

```bash
# Generate prod manifests
cue cmd generate -t env=prod

# Validate all environments
cue cmd validate
```

### Step 3.3: Final Parity Verification

Compare CUE outputs against historical Helm baselines:

```bash
# Generate with CUE
cue export environments/prod.cue --out yaml > cue-prod.yaml

# Compare against final Helm baseline
diff <(yq eval --sort-keys baseline-prod.yaml) \
     <(yq eval --sort-keys cue-prod.yaml) > migration-diff.txt

# Review diff manually
cat migration-diff.txt
```

Expected Differences (acceptable):
- Key ordering (YAML is order-preserving, CUE alphabetizes)
- Whitespace (insignificant)
- Comments (CUE doesn't preserve YAML comments)

Unacceptable Differences:
- Changed values
- Missing fields
- Added fields (unless intentional enhancements)

Rollback Trigger: >10 unacceptable differences → CUE schema has bugs. Do NOT deploy.

---

## Rollback Strategy (Failure State Handling)

### Phase 1 Rollback

Trigger: `cue vet` fails on >10% of baselines
Action: Delete `schema.cue`, restart schema extraction with looser constraints
Impact: Zero (CUE is shadow-only)

### Phase 2 Rollback

Trigger: CUE-generated ConfigMap differs from Helm output
Action: Remove `cue-outputs/*.yaml` from merge, revert to 100% Helm
Impact: Low (only affects one resource type)

### Phase 3 Rollback

Trigger: Production incident traced to CUE-generated manifest
Action:

```bash
# Emergency: revert to last-known Helm baseline
kubectl apply -f baseline-prod.yaml --force

# Long-term: keep Helm charts in repo (tagged)
git checkout tags/v1.0-helm
helm upgrade myapp ./charts/myapp -f values-prod.yaml
```

Impact: High (requires full deployment rollback)

Mitigation: Maintain Helm charts in read-only mode for 3 months post-migration.

---

## Input Data Request

To proceed with concrete migration plan, provide:

### 1. Sample Legacy Templates

```
Provide 2-3 representative files:
- Simplest template (Type A)
- Most complex template (Type C/D)
- Template with cross-field dependencies
```

### 2. Current Values Structure

```yaml
# values.yaml or equivalent
# Show nesting depth, list usage, conditionals
```

### 3. Target Output Example

```yaml
# Show what helm template produces today
# Include 1 dev + 1 prod example
```

### 4. Existing Schema (if any)

```json
// values.schema.json or OpenAPI spec
```

### 5. Pain Points

```
What specifically breaks today?
- Overrides not working?
- Validation too late (runtime)?
- Drift between envs?
```

With this data, I will provide:
1. Exact `cue import` commands for your schemas
2. Line-by-line refactoring of your templates → CUE
3. Custom `diff` scripts for your K8s resource types
4. Per-file rollback triggers

Post your templates and I'll generate the migration plan.
