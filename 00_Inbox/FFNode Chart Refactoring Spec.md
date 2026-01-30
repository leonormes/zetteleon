---
created: 2026-01-30T11:00:55+00:00
modified: 2026-01-30T11:16:49+00:00
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

```typescript
/
  The Root Interface for the FFNode Helm Chart.
  Adheres to "Data Structures over Code".
 /
export interface FFNodeAPI {
  /
    High-level intent. Encapsulates defaults for boolean flags.
    - 'dev': ephemeral, mocks enabled, local storage.
    - 'stage': cloud resources, valid certs, lower resilience.
    - 'prod': HA, vault strictness, PII guards active.
   /
  profile: 'dev' | 'stage' | 'prod';

  /
    The Identity of this deployment within the Global Graph.
   /
  identity: {
    siteCode: string; // e.g., "CUH"
    environment: string; // e.g., "prod-1"
    // The "Single Source of Truth" for DNS and Ingress grouping
    clusterDomain: string; // e.g., "privatelink.fitfile.net"
  };

  /
    Service Capabilities.
    Replaces "deploy" booleans with configuration objects.
    Presence of the object implies "enabled: true".
   /
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

```typescript
/
  Defines the intent to retrieve sensitive data.
  The Chart Logic generates the VSO manifests based on this schema.
 /
export type SecretIntent<T> = 
  | { source: 'vault'; path: string; keyMap?: Partial<Record<keyof T, string>> }
  | { source: 'k8s-secret'; name: string; keyMap?: Partial<Record<keyof T, string>> }
  | { source: 'literal'; value: T }; // Only allowed if profile === 'dev'

// Contract for Auth Credentials
interface AuthCredentials {
  clientId: string;
  clientSecret: string;
}

// Contract for DB Credentials
interface FitConnectCredentials {
  dbUser: string;
  dbPass: string;
  encryptionKey: string;
}
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

## Report: Legacy "App of Apps" Configuration Analysis & Refactoring Plan

**Date:** 2026-01-30
**Context:** FITFILE Deployment / `charts/ffnode`

### 1. Executive Summary

The current `ffnode` Helm chart functions as a monolithic "God Chart" that orchestrates the entire platform deployment. While functional, it suffers from high cognitive load due to **imperative templating logic** taking precedence over **declarative data**.

Developers currently have to mental-model complex string concatenation, conditional logic scattered across multiple files, and opaque helper functions just to understand what will be deployed.

**Recommendation:** Refactor to a **Data-Oriented Architecture** where `values.yaml` acts as the single source of truth, and a generic rendering engine generates the ArgoCD Application resources.

---

### 2. Current Architecture Analysis (The Pain Points)

#### A. "Toggle Hell" & Scattered Logic

Currently, adding or modifying a service requires touching multiple files:

1. **The Toggle:** `deploy.serviceName` (e.g., `deploy.frontend`) in `values.yaml`.
2. **The Configuration:** A specific section (e.g., `frontend:`) in `values.yaml`.
3. **The Template:** A dedicated file `templates/frontend-application.yaml` wrapping the entire resource in `{{- if eq.Values.deploy.frontend true }}`.

**Impact:** It is difficult to get a "glanceable" view of the system. You cannot iterate over the services; you must manually maintain a template file for each one.

#### B. The "String Block" Anti-Pattern

The `Application` manifests use a text block for Helm values, which forces the usage of the `tpl` function and complex string escaping:

**YAML Snippet**

```yaml
source:
  helm:
    values: |
      {{- $values := merge .Values.frontend (dict "global" .Values.global) -}}
      {{- include "renderValuesWithVaultSecretInExtraDeploy" (list . $values) | indent 8 }}
```

**Impact:**
- **No Type Safety:** YAML errors inside this block (indentation, typos) are treated as strings until ArgoCD tries to render them, leading to "runtime" errors rather than "compile-time" (templating) errors.
- **Opaque Context:** It is unclear what `renderValuesWithVaultSecretInExtraDeploy` actually does without deep-diving into `_helpers.tpl`.

#### C. Parochial Helper Logic

Logic like `renderValuesWithVaultSecretInExtraDeploy` couples the deployment mechanism (ArgoCD) tightly with the implementation details of a specific secret provider (Vault) and a specific injection method (modifying `extraDeploy`).

---

### 3. Proposed Refactor: Data-Oriented & Type-Safe

We will move from **Imperative Templates** (writing a file for each app) to **Declarative Data** (defining a list of apps).

#### A. The New `values.yaml` Structure

Define a standard schema for an "Application".

```yaml
# Global Configuration (Context)
global:
  domain: fitfile.net
  env: prod
  vault:
    enabled: true

# The "App of Apps" Data Structure
applications:
  frontend:
    enabled: true
    source:
      chart: charts/components/frontend
      # OR
      repoURL: https://gitlab.com/fitfile/deployment.git
      targetRevision: HEAD
    
    # Declarative Values (Type-Safe Map, not String)
    values:
      ingress:
        enabled: true
      resources:
        requests:
          cpu: 100m
    
    # Abstracted Dependencies/Infra
    infrastructure:
      vault:
        role: frontend-role
        secrets:
          - key: auth0-client-id
            env: AUTH0_CLIENT_ID
      database:
        type: mongodb
        binding: true # Automatically inject connection strings
```

#### B. The Single Generic Template (`templates/app-generator.yaml`)

Instead of 20+ files, we use one:

```yaml
{{- range $appName, $appConfig := .Values.applications }}
{{- if $appConfig.enabled }}
---
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: {{ $appName }}
  namespace: argocd
spec:
  source:
    path: {{ $appConfig.source.chart }}
    helm:
      # We serialize the values map directly to YAML, avoiding manual string construction
      values: |
        {{- toYaml $appConfig.values | nindent 8 }}
        {{- /* Logic to inject infrastructure config based on $appConfig.infrastructure can go here */ -}}
  destination:
    namespace: {{ $appConfig.destination.namespace | default $.Values.global.defaultNamespace }}
{{- end }}
{{- end }}
```

#### C. Migration Strategy

1. **Create the Schema:** Define the `applications` list structure in a new values file (e.g., `values-v2.yaml`) alongside the old one.
2. **Port One Service:** Take a simple service (e.g., `frontend`) and move its config from the root of `values.yaml` into the `applications` list.
3. **Implement the Generator:** Create the `templates/app-generator.yaml`.
4. **Verify:** Run `helm template` and ensure the output `Application` manifest for `frontend` is identical (or functionally equivalent) to the old one.
5. **Iterate:** Gradually move `ffcloud`, `fitconnect`, etc., into the list.
6. **Cleanup:** Delete the old `templates/frontend-application.yaml` and the legacy values keys.

### 4. Immediate Benefits

1. **DevEx:** A developer adds a new service by adding 10 lines to `values.yaml`, not by creating new files and debugging indentation.
2. **Safety:** The values are treated as data objects. Helm's `toYaml` function handles the formatting guarantees.
3. **Clarity:** The infrastructure requirements (Vault, DBs) are declared explicitly in the data, not buried in helper templates.
