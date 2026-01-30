---
created: 2026-01-30T11:00:55+00:00
modified: 2026-01-30T11:45:00+00:00
tags: [architecture, k8s, specification]
title: FFNode Chart Refactoring Spec
---

## FFNode Umbrella Chart: Forensic Analysis & API Specification

#architecture #k8s #specification

Date: 28 January 2026

Author: Senior Principal Systems Architect

Subject: Complexity Abstraction & Outer API Redesign

### 1. The Complexity Heatmap (Forensic Audit)

Our audit of the current deployment values (specifically across `barts`, `eoe`, and `fitfile` namespaces) reveals a critical violation of the "Information Hiding" principle. The abstraction layer of the Helm chart has leaked, forcing consumers to act as chart developers.

#### A. The "Accidental Complexity" of `vaultSecrets`

Diagnosis: Pass-Through Templating.

Currently, the user is required to write Go templates _inside_ YAML strings, which are then processed by Helm to generate _another_ template for the Vault Secrets Operator (VSO). This is "Double-Templating Inception."

Evidence:

In `@ffnodes/eoe/cuh-prod-1/hutch_values.yaml`, we observe:

```yaml
text: '{{`{{get .Secrets "bunny_database_username"}}`}}'
```

Impact:

1. Cognitive Load: The user must understand the VSO templating language (`get.Secrets`) and escape it correctly for Helm (`{{` … `}}`).
2. Brittle Contracts: A typo in the inner string (`"bunny_database_username"`) is not caught until runtime (pod startup failure), as it bypasses Helm's linting.
3. Leaky Abstraction: The user is manually defining the `transformation` block. The chart should _know_ how to transform a database password; the user should only supply the _reference_.

#### B. The Coupling of `rolloutRestartTargets`

Diagnosis: Hard-coded Dependency Injection.

The user is forced to manually bind the lifecycle of a Secret to the lifecycle of a Deployment. This requires the user to predict the exact rendered name of a Kubernetes resource.

Evidence:

In `@ffnodes/eoe/cuh-prod-1/hutch_values.yaml`:

```yaml
rolloutRestartTargets:
  - kind: Deployment
    name: '{{ include "hutch.bunny.fullname" . }}'
```

Impact:

1. Internal Knowledge Required: The user must know that the internal helper template is named `hutch.bunny.fullname`. If the chart developer refactors this helper, every consumer values file breaks.
2. Manual Wiring: In a DDD approach, if a Deployment consumes a Secret, the graph knows this relationship. The restart policy should be implicit in the connection, not explicitly defined by the user.

#### C. The "Boolean Switchboard" (`deploy` flags)

Diagnosis: Imperative Configuration.

The `deploy` section (e.g., `initialiseCluster: false`, `certManager: false`) turns the values file into a procedural script.

Evidence:

In `@ffnodes/barts/prod/values.yaml`:

```yaml
deploy:
  spicedb: false
  initialiseCluster: false
  certManager: false
  monitoring: false
```

Impact:

This forces the user to manually compose a valid platform state. It allows invalid states (e.g., deploying `fitconnect` without `spicedb` in an environment where it is strictly required).

---

### 2. The Formal Data API (The Solution)

We propose a strict TypeScript contract for the new `values.yaml`. This moves complexity from the _user's mind_ into the _chart's schema_.

#### A. Core Interfaces

```ts
// The Root Interface for the FFNode Helm Chart.
// Adheres to "Data Structures over Code".
export interface FFNodeAPI {
// High-level intent. Encapsulates defaults for boolean flags.
// - 'dev': ephemeral, mocks enabled, local storage.
// - 'stage': cloud resources, valid certs, lower resilience.
// - 'prod': HA, vault strictness, PII guards active.
// profile: 'dev' | 'stage' | 'prod';
// The Identity of this deployment within the Global Graph.
  identity: {
    siteCode: string; // e.g., "CUH"
    environment: string; // e.g., "prod-1"
    // The "Single Source of Truth" for DNS and Ingress grouping
    clusterDomain: string; // e.g., "privatelink.fitfile.net"
  };

  // Service Capabilities.
  // Replaces "deploy" booleans with configuration objects.
  // Presence of the object implies "enabled: true".
  capabilities: {
    // Replaces deploy.fitconnect & fitconnect section
    fitConnect?: {
      connectivity: 'island' | 'archipelago' | 'continental';
      // Abstracted secrets - no templating visible to user
      credentials: SecretIntent<FitConnectCredentials>;
    };

    // Replaces deploy.spicedb
    permissions?: {
      engine: 'spicedb';
      topology: 'embedded' | 'external';
      // If external, connection details are required
      connection?: ConnectionString; 
    };

    // Replaces "global.oauth" and "argocd.sso"
    authentication: {
      provider: 'auth0' | 'entra-id';
      tenantUri: string;
      // User defines intent, Chart handles the VSO mapping
      secrets: SecretIntent<AuthCredentials>;
    };
  };

  /
    Data Persistence Topology.
    The user declares what they need, not how it is deployed.
   /
  persistence: {
    databaseStrategy: 'ephemeral' | 'cloud-managed' | 'operator-managed';
    // Replaces mongodb & postgresql sections
    stores: {
      main: DatabaseDefinition;
      events: DatabaseDefinition;
      analytics: DatabaseDefinition;
    };
  };
}
```

#### B. The Secret Intent Interface

This is the key to removing VSO complexity. The user declares _where_ the secret comes from, not _how_ to process it.

> **Architectural Note:** This maps directly to the "Unidirectional State Synchronizer" pattern defined in the `SoT - Vault KV Data Structure`. The chart acts as the translation layer between Intent and CRD.

| SecretIntent Source | Generated VSO CRD | Purpose |
| :--- | :--- | :--- |
| `source: 'vault'` | `VaultStaticSecret` | Mirrors a KV JSON path from Vault to a K8s Secret. |
| `source: 'vault-dynamic'` | `VaultDynamicSecret` | Manages leases/TTL for ephemeral credentials (e.g., DB users). |
| `source: 'k8s-secret'` | `ExternalSecret` (Optional) | references existing opaque secrets (e.g., from SealedSecrets). |

```ts
/
  Defines the intent to retrieve sensitive data.
  The Chart Logic generates the VSO manifests based on this schema.
 /
export type SecretIntent<T> =
  | { source: 'vault'; path: string; keyMap?: Partial<Record<keyof T, string>> }
  | { source: 'k8s-secret'; name: string; keyMap?: Partial<Record<keyof T, string>> }
  | { source: 'literal'; value: T }; // Only allowed if profile === 'dev'
```

---

### 3. The Validation Logic (The Guardrails)

We enforce invariants using JSON Schema logic (pseudocode) to prevent "Configuration Drift" and invalid states.

#### Invariant A: Production Security Enforcment

_If the profile is Production, external Secrets Management is mandatory._

```json
{
  "if": {
    "properties": { "profile": { "const": "prod" } }
  },
  "then": {
    "properties": {
      "capabilities": {
        "properties": {
          "authentication": {
            "properties": {
              "secrets": {
                "properties": {
                  "source": { "const": "vault" } 
                }
              }
            }
          }
        }
      }
    }
  },
  "errorMessage": "Production profiles MUST use Vault for authentication secrets."
}
```

#### Invariant B: Persistence Strategy Consistency

_If using ephemeral databases, backups must be disabled (or flagged)._

```json
{
  "if": {
    "properties": {
      "persistence": {
        "properties": { "databaseStrategy": { "const": "ephemeral" } }
      }
    }
  },
  "then": {
    "properties": {
      "persistence": {
        "properties": {
          "backups": { "const": false }
        }
      }
    }
  },
  "errorMessage": "Ephemeral storage strategies cannot support backup configurations."
}
```

#### Invariant C: Topology Integrity

_If SpicedB is external, the connection string is required._

```json
{
  "if": {
    "properties": {
      "capabilities": {
        "properties": {
          "permissions": {
            "properties": { "topology": { "const": "external" } }
          }
        }
      }
    }
  },
  "then": {
    "properties": {
      "capabilities": {
        "properties": {
          "permissions": {
            "required": ["connection"]
          }
        }
      }
    }
  }
}
```

---

### 4. Architectural Precedents & Cross-Project Validation

> **LTM Insight:** This refactor aligns with the "Generative Engine" pattern from the LCA-DP project and the "App of Apps" rendering logic defined in our System Prompts.

#### A. The "Generative Engine" Precedent (LCA-DP)
We are replicating the successful **Configuration-Driven Architecture** used in the `LCA-DP` project.

| Component | LCA-DP Role | FFNode (Proposed) Role |
| :--- | :--- | :--- |
| **Input Schema** | `customer.yaml` (Central Config) | `values.yaml` (Typed Interface) |
| **Engine** | `locals.tf` (Ingestion Logic) | `_helpers.tpl` & `app-generator.yaml` |
| **Output** | `generated/values.yaml` | `Application` & `VaultStaticSecret` CRDs |
| **State Store** | Terraform State | ArgoCD (GitOps State) |

#### B. The Rendering Logic (App of Apps Pattern)
Based on the `@10_System/prompts/App of Apps Prompt.md`, the `templates/app-generator.yaml` must implement the following recursive rendering logic:

1.  **Traversal:** Iterate over the `applications` map in `values.yaml`.
2.  **Source Detection:** Dynamically determine if the child is a Helm Chart (`source.chart`) or a Git Repo (`source.repoURL`).
3.  **Value Serialization:** Use the `toYaml` function to serialize the `values` map into a string block for the child Application, effectively passing the configuration context down the tree.
4.  **Overlay Merging:** (Future) Support `kustomize` overlays for environment-specific patches.

#### C. Alignment with Secret Management SoT
This specification explicitly resolves the "Leaky Abstraction" identified in the **FITFILE Secret Management Architecture**. By enforcing the `SecretIntent` interface, we remove the need for developers to interact with the raw VSO templating language, effectively "codifying" the security policy into the chart itself.