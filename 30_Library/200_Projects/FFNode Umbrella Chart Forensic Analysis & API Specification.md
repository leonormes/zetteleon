---
aliases: []
created: 2026-01-29T07:28:40+00:00
id: FFNode Umbrella Chart Forensic Analysis & API Specification
modified: 2026-06-11T15:13:07+00:00
project_category: refined_deployment
project_name: Refined Deployment
project_status: active
tags:
  - architecture
  - cuelang
  - ff_deploy
  - k8s
  - specification
title: FFNode Umbrella Chart Forensic Analysis & API Specification
type:
---

## 1. The Complexity Heatmap (Forensic Audit)

> Note: The diagnosis remains unchanged from the original forensic audit. The primary issues identified—Pass-Through Templating, Hard-coded Dependencies, and Imperative Boolean Flags—are the drivers for this CUE-based refactor.\_

- [ ] Incoporate cue into the secrets managements [due:: 2026-02-11] ^2026-02-11T08-03-31 {{operonId:: o3vzhjr}} {{status:: Project.Brainstorming}} {{priority:: C}} {{prodosProject:: Refined Deployment}} {{datetimeCreated:: 2026-06-11T16:12:37}} {{datetimeModified:: 2026-06-11T16:36:14}}
    - [📱 View in Todoist app](todoist://task?id=10006842860) (Created: 📝 2026-02-11T08:03)

### A. The "Accidental Complexity" of `vaultSecrets`

Diagnosis: Pass-Through Templating ("Double-Templating Inception").

Impact: Cognitive load, brittle contracts, and abstraction leaks where consumers act as chart developers.

### B. The Coupling of `rolloutRestartTargets`

Diagnosis: Hard-coded Dependency Injection.

Impact: Requires internal knowledge of helper templates (`hutch.bunny.fullname`); creates manual wiring for lifecycle dependencies.

### C. The "Boolean Switchboard" (`deploy` flags)

Diagnosis: Imperative Configuration.

Impact: Allows invalid platform states (e.g., enabling dependent services without their prerequisites).

---

## 2. The Formal Data API (The Solution)

We propose a strict CUE Schema for the new `values.yaml`. This moves complexity from the _user's mind_ into the _compiler's unification logic_.

### A. Core Schema Definitions

```cue
package ffnode

// The Root Definition for the FFNode Helm Chart.
// Adheres to "Configuration as Data" with strict typing.
#FFNodeAPI: {
    // High-level intent.
    // - 'dev': ephemeral, mocks enabled, local storage.
    // - 'stage': cloud resources, valid certs, lower resilience.
    // - 'prod': HA, vault strictness, PII guards active.
    profile: "dev" | "stage" | "prod" @tag(profile)

    // The Identity of this deployment within the Global Graph.
    identity: {
        siteCode:      string // e.g., "CUH"
        environment:   string // e.g., "prod-1"
        // The "Single Source of Truth" for DNS and Ingress grouping
        clusterDomain: string // e.g., "privatelink.fitfile.net"
    }

    // Service Capabilities.
    // Replaces "deploy" booleans with structural configuration.
    // Presence of the struct implies enabled status.
    capabilities: {
        // Replaces deploy.fitconnect & fitconnect section
        fitConnect?: {
            connectivity: "island" | "archipelago" | "continental"
            // Abstracted secrets - no templating visible to user
            credentials: #SecretIntent
        }

        // Replaces deploy.spicedb
        permissions?: {
            engine: "spicedb"
            topology: "embedded" | "external"
            // If external, connection details are enforced via constraints (see Sec 3)
            connection?: string
        }

        // Replaces "global.oauth" and "argocd.sso"
        authentication: {
            provider:  "auth0" | "entra-id"
            tenantUri: string
            // User defines intent, Chart handles the VSO mapping
            secrets: #SecretIntent
        }
    }

    // Data Persistence Topology.
    // The user declares requirements, not deployment mechanics.
    persistence: {
        databaseStrategy: "ephemeral" | "cloud-managed" | "operator-managed"
        backups:          bool | true // Default true, constrained below

        // Replaces mongodb & postgresql sections
        stores: {
            main:      #DatabaseDefinition
            events:    #DatabaseDefinition
            analytics: #DatabaseDefinition
        }
    }
}
```

### B. The Secret Intent Definition

This is the key to removing VSO (Vault Secrets Operator) complexity. CUE's Disjunctions allow us to define mutually exclusive schemas for retrieving sensitive data.

> Architectural Note: This maps directly to the "Unidirectional State Synchronizer" pattern. CUE validates that the provided fields match exactly one of the allowed `source` types.

| SecretIntent Source       | Generated VSO CRD           | Purpose                                       |
| ------------------------- | --------------------------- | --------------------------------------------- |
| `source: "vault"`         | `VaultStaticSecret`         | Mirrors a KV JSON path from Vault.            |
| `source: "vault-dynamic"` | `VaultDynamicSecret`        | Manages leases/TTL for ephemeral credentials. |
| `source: "k8s-secret"`    | `ExternalSecret` (Optional) | References existing opaque secrets.           |

```cue
// Defines the intent to retrieve sensitive data.
// The Chart Logic generates the VSO manifests based on this schema.
#SecretIntent: {
    source: "vault"
    path:   string
    keyMap?: { [string]: string }
} | {
    source: "k8s-secret"
    name:   string
    keyMap?: { [string]: string }
} | {
    source: "literal"
    // Only allowed if profile === 'dev' (Enforced in Section 3)
    value:  { … }
}
```

---

## 3. The Validation Logic (The Guardrails)

In CUE, validation is not a separate step; it is intrinsic to the schema. We enforce invariants using Unification Constraints. If a user's config violates these rules, the CUE evaluation fails immediately, preventing invalid Helm generation.

### Invariant A: Production Security Enforcement

_If the profile is Production, external Secrets Management is mandatory._

```cue
// Inside #FFNodeAPI definition
if profile == "prod" {
    capabilities: authentication: secrets: source: "vault"
}
```

### Invariant B: Persistence Strategy Consistency

_If using ephemeral databases, backups must be disabled._

```cue
// Inside #FFNodeAPI definition
if persistence.databaseStrategy == "ephemeral" {
    persistence: backups: false
}
```

### Invariant C: Topology Integrity

_If SpicedB is external, the connection string is required._

```cue
// Inside #FFNodeAPI definition
if capabilities.permissions.topology == "external" {
    capabilities: permissions: connection: !=_|_ // Must be defined (not bottom)
}
```

### Invariant D: Dev-Only Literals

_Literal secrets are strictly forbidden outside of development profiles._

```cue
// Inside #FFNodeAPI definition
if profile != "dev" {
    // Iterate over all capabilities to ban literal secrets
    capabilities: [Name=_]: {
        credentials?: source: !="literal"
        secrets?:     source: !="literal"
    }
}
```

---

## 4. Architectural Precedents & Cross-Project Validation

> LTM Insight: This refactor aligns with the "Generative Engine" pattern from the LCA-DP project, but leverages CUE's hermeticity for safer configuration management.

### A. The "Generative Engine" Precedent (LCA-DP)

We are replicating the successful Configuration-Driven Architecture used in the `LCA-DP` project.

| Component    | LCA-DP Role                      | FFNode (Proposed) Role                   |
| ------------ | -------------------------------- | ---------------------------------------- |
| Input Schema | `customer.yaml` (Central Config) | `values.cue` (Unified Config)            |
| Engine       | `locals.tf` (Ingestion Logic)    | `output_tool.cue` (CUE to YAML export)   |
| Output       | `generated/values.yaml`          | `Application` & `VaultStaticSecret` CRDs |
| State Store  | Terraform State                  | ArgoCD (GitOps State)                    |

### B. The Rendering Logic (App of Apps Pattern)

The CUE configuration will export standard Kubernetes manifests. The transition relies on CUE's ability to marshal data into YAML streams.

1. Traversal: CUE comprehensions iterate over the `capabilities` struct.
2. Source Detection: Pattern matching on the `source` field determines if we generate a `VaultStaticSecret` or an `ExternalSecret`.
3. Value Serialization: `cue export` outputs the final `values.yaml` or fully rendered manifests, guaranteeing that the output is valid against the schema before it ever reaches the cluster.

### C. Alignment with Secret Management SoT

By enforcing the `#SecretIntent` disjunction, we mathematically prove that a configuration cannot exist where a user requests a Vault secret but fails to provide a `path`. The "Leaky Abstraction" is sealed by the CUE compiler.
