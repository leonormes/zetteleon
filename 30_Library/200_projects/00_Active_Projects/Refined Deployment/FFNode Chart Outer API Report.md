---
created: 2026-01-28T13:09:57+00:00
modified: 2026-01-28T17:54:39+00:00
title: FFNode Chart Outer API Report
---

## FFNode Outer API Report

This report documents the outer API and configuration options for the `ffnode` umbrella chart, which serves as the deployment unit for FITFILE components.

### Meta & Identity

Core identifiers for the deployment unit.

| Field | Type | Required | Description |
|:--- |:--- |:--- |:--- |
| `deploymentKey` | `string` | Yes | Unique identifier for this deployment (e.g., `ff-prod-1`). Used for hostnames, vault paths, and resource naming. |
| `namespace` | `string` | No | Target K8s namespace. Defaults to `deploymentKey` if unset. |

### Deployment Topology (`deploy`)

Boolean feature flags to enable or disable specific subsystems.

```yaml
deploy:
  # Infrastructure
  initialiseCluster: bool # (Default: true) Installs base cluster resources (ArgoCD Apps)
  certManager: bool       # (Default: true) Installs cert-manager
  persistence: bool       # (Default: true) Installs stateful services (MinIO, Mongo, Postgres)
  monitoring: bool        # (Default: true) Installs Grafana/Prometheus stack
  messageBroker: bool     # (Default: true) Enabled but currently unused in values
  blobCsiDriver: bool     # (Default: false) Azure Blob CSI driver
  mutatingProxyWebhook: bool # (Default: false) Internal proxy webhook

  # Core Services
  coordinatingStation: bool # (Default: true) Deploys 'ffcloud' service
  fitconnect: bool          # (Default: true) Deploys 'fitconnect' service
  frontend: bool            # (Default: true) Deploys 'frontend' UI
  workflowsApi: bool        # (Default: true) Deploys 'workflows-api' service
  spicedb: bool             # (Default: true) Deploys SpiceDB permissions system
  
  # Development / Migration
  seedData: bool        # (Default: false) Runs jobs to seed initial data
  mongodbNext: bool     # (Default: false) Parallel Mongo deployment for migration
  workflowsIntegrationTests: bool # (Default: false) Deploys integration test scaffolding
```

### Global Configuration (`global`)

Shared configuration propagated to all sub-charts.

```typescript
interface GlobalConfig {
  images: Record<string, any>;
  imagePullSecrets: Array<{ name: string }>; // Default: [{name: "fitfile-image-pull-secret"}]
  
  vault: {
    enabled: boolean;       // Default: true
    secretsMount: string;   // Default: "secrets"
    namespace?: string;     // Optional override for Vault namespace
  };

  oauth: {
    baseURL: string;               // Default: "https://fitfile-prod.eu.auth0.com"
    managementApiAudience: string; // Default: ".../api/v2/"
  };

  dbSuffix: string;       // Suffix appended to DB names (e.g. "_test")
  fitConnectCode?: string; // Optional override for the node's unique code
  
  default_output_format: "parquet" | string; // Default: parquet
}
```

### Component Configurations

#### Argo Workflows (`argoWorkflows`)

Configures the workflow orchestration engine.

- `chart.targetRevision`: `0.45.`
- `server`: Configures SSO (Microsoft Entra), Ingress (TLS/SSL Passthrough), and Auth Modes (`sso`, `client`).
- `persistence`: Uses PostgreSQL for workflow archiving (`argoworkflows` DB).

#### Core Business Logic

- `ffcloud`: Coordinating station service. Manages `ffCloudCode` and DB connection logic.
- `fitconnect`: Connectivity service. Handles S3 endpoints and connectivity logic.
- `frontend`: React web UI. Configures API endpoints (`graphqlApiUrl`, `restApiUrl`) and feature flags.

#### Data Stores

- `mongodb`: Bitnami-based replica set deployment (Default: 2 replicas).
- `postgresql`: Primary DB for `ffcloud`, `spicedb`, and `argoworkflows`.
- `minio`: Object storage with pre-provisioned buckets (`output`, `temp`, `uploads`).
- `spicedb`: Fine-grained permissions system using PostgreSQL as a datastore.

### Secret Management (`vaultSecrets`)

A recursive pattern used across almost all components to inject secrets from HashiCorp Vault.

```typescript
interface VaultSecret {
  secretName: string;   // Name of the K8s secret to create
  vaultPath: string;    // Path in Vault
  refreshAfter?: string; // e.g., "5m"
  rolloutRestartTargets?: Array<{ kind: string; name: string }>; 
  
  secretTransformation: {
    excludes: string[];
    templates: Record<string, { text: string }>; // Go templates for formatting
  };
}
```

### Extension Points

- `extraDeploy`: List of raw K8s manifests.
- `extraVaultSecrets`: Additional dynamic/static secrets for VSO.

## FFNode Chart: API Contract & Complexity Analysis

Role: Senior Principal Systems Architect

Subject: Forensic Analysis & API Redesign of `ffnode` Umbrella Chart

Principle: Tesler's Law (Conservation of Complexity)

### 1. Executive Summary

The current `ffnode` chart suffers from "Pass-Through Complexity". Instead of encapsulating the complexity of Kubernetes, Vault, and Service Mesh interactions, it exposes the raw implementation details to the user via `values.yaml`. This violates Tesler's Law by forcing the User to manage complexity that belongs in the System (the Chart).

The `vaultSecrets` configuration is the most critical offender, requiring the user to write Go templates inside YAML strings, effectively leaking the entire abstraction layer.

### 2. The "Interface vs. Implementation" Audit

#### 🔴 High Complexity (Infrastructure & Secrets)

   The "Templating in YAML" Anti-Pattern:

Observation: Users define `vaultSecrets` with `text: '{{"{{`…`}}"}}'`.

Verdict: This is fragile and hostile. The user must know the internal secret keys (e.g., `postgresql_password`) and the Vault VSO syntax.

Ownership: Currently User. Must move to Chart.

Manual Dependency Management:

Observation: Users must manually specify `rolloutRestartTargets`.

Verdict: The chart knows that `ffcloud` depends on the `ffcloud-secrets`. The user should not have to manually link the Deployment to the Secret rotation.

Ownership: Currently User. Must move to Chart.

#### 🟠 Medium Complexity (Connectivity)

Implicit "Magic Strings":

Observation: Hostnames are derived via conventions (e.g., `{{ .Release.Name }}-postgresql`).

Verdict: If a user supplies an external Postgres, they have to override deep values or risk the chart assuming a local one exists.

Ownership: Shared/Ambiguous. Must move to Explicit Data Model.

#### 🟡 Low Complexity (Deployment Flags)

The "Boolean Swamp":

Observation: `deploy.persistence`, `deploy.monitoring`, etc.

Verdict: Boolean flags are insufficient for architectural decisions. `persistence: true` doesn't differentiate between "local-path ephemeral" and "managed disk with snapshots".

### 3. The "Data-Driven" API Contract

We propose replacing the current implementation-heavy `values.yaml` with a strict Intent-Based Data Model.

#### A. Topology Profiles (Replacing Booleans)

Instead of 20 boolean flags, use a Profile to assert architectural constraints.

```typescript
// Proposed Types
type DeploymentProfile = 'local-dev' | 'staging' | 'prod-ha' | 'edge-airgapped';

interface ArchitectureSpec {
  profile: DeploymentProfile;
  
  // Overrides allowed by the profile
  storageClass?: string; // specific to the environment
  highAvailability: boolean; // Enforced true by 'prod-ha'
}
```

#### B. Canonical Secret Registry (Replacing `vaultSecrets`)

The chart defines the Schema of secrets it needs. The user only defines the Source.

Current (Bad):

```yaml
vaultSecrets:
  - secretName: "mongodb"
    templates:
       password: '{{"{{`{{get .Secrets \"mongodb_password\"}}`}}"}}'
```

Proposed (Good):

```yaml
# User Input
secrets:
  source: "vault"
  rootPath: "secret/data/deployments/ff-prod-1"
  # Optional: Map keys if they differ from convention
  mapping:
    dbPassword: "mongo_root_pass_v2" 

# Chart Logic (Hidden from User)
# The chart knows that 'mongodb' needs a password. 
# It looks up 'rootPath/dbPassword' automatically.
```

#### C. The Unified Graph (Global Configuration)

Move all "Glue" to the Global scope. Components only configure their "Internals".

```typescript
interface GlobalGraph {
  identity: {
    tenantId: string;
    environment: string;
  };
  
  // The 'Truth' of the network
  ingress: {
    domain: string; // e.g. "fitfile.net"
    tlsIssuer: string;
  };

  // The 'Truth' of the data layer
  datastore: {
    engine: 'embedded-mongo' | 'external-atlas';
    connection?: string; // Required if external
  };
}
```

### 4. Formal API Spec (TypeScript Definition)

This is the contract for the new `values.yaml`.

```typescript
interface FFNodeValues {
  // 1. Meta-Architecture
  profile: 'dev' | 'prod';
  
  // 2. Identity & Access
  tenant: {
    key: string; // e.g., "barts"
    displayName: string;
  };
  
  // 3. Secret Strategy
  secrets: {
    provider: 'vault' | 'k8s-native';
    config: {
      vaultAddress?: string;
      vaultMount?: string;
    };
  };

  // 4. Service Graph (The Glue)
  services: {
    database: DatabaseService;
    objectStorage: StorageService;
    auth: AuthService;
  };

  // 5. Component Specifics (The Internals)
  // Only expose what CANNOT be derived from the Global Graph
  components: {
    ffcloud: {
      resources: ResourceRequirements;
      logLevel: 'debug' | 'info';
    };
    frontend: {
      features: Record<string, boolean>;
    };
  };
}

interface DatabaseService {
  type: 'managed' | 'external';
  // If managed, the chart spins up Mongo/Postgres pods.
  // If external, validation requires connection strings.
}
```

### 5. Validation Logic (Pre-flight Checks)

We must implement `schema.json` to enforce this contract before Helm even runs.

Rule 1: External Data requires Connection Details

```json
{
  "if": { "properties": { "services": { "properties": { "database": { "const": "external" } } } } },
  "then": { "required": ["externalConnectionUri"] }
}
```

Rule 2: Prod Profile requires Vault

```json
{
  "if": { "properties": { "profile": { "const": "prod-ha" } } },
  "then": { 
    "properties": { 
      "secrets": { "properties": { "provider": { "const": "vault" } } } 
    } 
  }
}
```

### 6. Implementation Plan

1. Create `_secrets.tpl`: A library helper that takes a standard secret key (e.g., `DB_PASSWORD`) and generates the Vault Secret CRD automatically, hiding the template syntax from the user.
2. Refactor `global`: Deprecate component-level `host` overrides. Centralize in `global.topology`.
3. JSON Schema: Generate a `values.schema.json` that enforces the "Profile" constraints.
