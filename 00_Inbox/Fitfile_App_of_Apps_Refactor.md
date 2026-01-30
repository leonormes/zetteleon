---
created: 2026-01-30T11:00:55+00:00
modified: 2026-01-30T11:01:47+00:00
title: Fitfile_App_of_Apps_Refactor
---

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
