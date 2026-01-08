---
aliases: []
confidence: ""
created: 2026-01-03T15:22:49+00:00
epistemic: ""
last_reviewed: ""
modified: 2026-01-08T10:50:03+00:00
purpose: ""
review_interval: ""
see_also: []
source_of_truth: []
status: active
tags: []
title: Helm Platform Review Prompt
type: prompt
---

## Role

You are a Principal Infrastructure Engineer and Helm Expert acting as a Code Reviewer.

## The Context: "The Compiler Migration"

We are refactoring our infrastructure from a legacy "Wrapper Chart" (which blindly passed 100s of values to sub-charts) to a new **"Compiler Pattern"**.

**The Goal:**
1. **Input:** A high-level "Intent" (e.g., `class: production-ha`, `features: [fitconnect, hutch]`).
2. **Logic:** A Logic Engine (`_compiler.tpl`) that compiles this intent into rigid, type-safe specifications.
3. **Output:** 100% valid Kubernetes manifests (using standard off-the-shelf Bitnami/Argo charts).

**The Business Requirement:**
We are scaling to many customers. We need to:
- **Prevent Human Error:** Impossible states (e.g., "FitConnect enabled but Postgres disabled") must be unrepresentable.
- **Maintain Flexibility:** We must support bespoke overrides (e.g., "Customer A needs 2 replicas, not 3") without forking the platform.
- **Manage Lifecycle:** We need to upgrade versions (e.g., MongoDB 16 -> 17) centrally, but allow pinning specific customers to old versions if needed.

## The Codebase to Review

### 1. The Data Structure (`values.yaml`)

_Defines the "Classes" (Topology), "Profiles" (Physics), and "Versions" (Lifecycle)._

```yaml
_specs:
  classes:
    local-dev:
      desc: "Ephemeral, laptop-friendly"
      topology: "standalone"
      profile: "micro"
      features: { vault: true, monitoring: false, backups: false }
    production-ha:
      desc: "High Availability, Data Integrity"
      topology: "replicaset"
      profile: "standard"
      features: { vault: true, monitoring: true, backups: true }

  profiles:
    micro:
      infra: 
        requests: { cpu: "10m", memory: "32Mi" }
        limits:   { cpu: "100m", memory: "64Mi" }
      db:    
        requests: { cpu: "100m", memory: "256Mi" }
        limits:   { cpu: "500m", memory: "512Mi" }
    standard:
      infra: 
        requests: { cpu: "100m", memory: "128Mi" }
        limits:   { cpu: "500m", memory: "256Mi" }
      db:    
        requests: { cpu: "500m", memory: "1Gi" }
        limits:   { cpu: "2000m", memory: "4Gi" }

  versions:
    mongodb: "16.5.0"
    postgresql: "12.5.0"
    minio: "12.8.0"
    argoworkflows: "0.45.0"
    spicedb: "1.14.0"
    certmanager: "v1.12.0"
    prometheus: "6.0.0"
    grafana_agent: "1.0.0"
    hutch: "1.2.0"
    pgweb: "HEAD"
````

### 2. The Logic Engine (`_compiler.tpl`)

_Calculates configuration based on Class, Features, and Overrides._

```yaml
{{- define "fitfile.compile.mongodb" -}}
  {{- $class := .Values.global.class | default "local-dev" -}}
  {{- $spec := index .Values._specs.classes $class -}}
  {{- $profile := index .Values._specs.profiles $spec.profile -}}
  
  {{- /* A. Base Config */ -}}
  {{- $mongoConfig := dict -}}
  {{- if eq $spec.topology "replicaset" -}}
    {{- $_ := set $mongoConfig "architecture" "replicaset" -}}
    {{- $_ := set $mongoConfig "replicaCount" 3 -}}
  {{- else -}}
    {{- $_ := set $mongoConfig "architecture" "standalone" -}}
    {{- $_ := set $mongoConfig "replicaCount" 1 -}}
  {{- end -}}
  {{- $_ := set $mongoConfig "resources" $profile.db -}}
  {{- $_ := set $mongoConfig "auth" (dict "existingSecret" "mongodb-creds") -}}

  {{- /* B. Apply Overrides (The Escape Hatch) */ -}}
  {{- $overrides := .Values.overrides.mongodb | default dict -}}
  {{- merge $overrides $mongoConfig | toYaml -}}
{{- end -}}

{{- define "fitfile.compile.observability" -}}
  {{- $class := .Values.global.class -}}
  {{- $spec := index .Values._specs.classes $class -}}
  {{- if $spec.features.monitoring -}}
    {{- $crdConfig := dict "enabled" true -}}
    {{- $agentConfig := dict "cluster" (dict "name" .Values.global.identity.tenant) -}}
    
    {{- /* Merge Overrides Deeply */ -}}
    {{- $overrides := .Values.overrides.observability | default dict -}}
    {{- dict 
        "crds" (merge ($overrides.crds | default dict) $crdConfig)
        "agent" (merge ($overrides.agent | default dict) $agentConfig)
        | toYaml 
    -}}
  {{- end -}}
{{- end -}}
```

### 3. The Adapters (`templates/compiler/*.yaml`)

_The bridge between Logic and Manifests. Note the dynamic versioning._

```yaml
# mongodb.yaml
{{- include "fitfile.compile.mongodb" . | nindent 0 }}
{{- if .Values.features.mongodb }}
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: {{ .Values.global.identity.tenant }}-mongodb
  namespace: argocd
spec:
  project: default
  source:
    chart: mongodb
    repoURL: "oci://registry-1.docker.io/bitnami"
    # DYNAMIC VERSION:
    targetRevision: {{ .Values._specs.versions.mongodb | quote }}
    helm:
      values: |
        {{- include "fitfile.compile.mongodb" . | nindent 8 }}
  destination:
    server: [https://kubernetes.default.svc](https://kubernetes.default.svc)
    namespace: {{ .Values.global.identity.tenant }}
{{- end }}
```

### 4. The Customer Intent (`customer-repo/values.yaml`)

_How we configure a specific customer._

```yaml
fitfile-core:
  global:
    class: "production-ha" # Sets topology=replicaset, profile=standard
    identity:
      tenant: "ff-a"
      domain: "fitfile.net"

  features:
    ffcloud: true
    frontend: true
    fitconnect: true
    hutch: false
    pgweb: true

  # THE ESCAPE HATCH: Custom overrides for this customer ONLY
  overrides:
    mongodb:
      replicaCount: 2 # Override standard (3) to match legacy hardware
      resources:
        requests: { cpu: "300m" } # Downgrade request, keep safety limits
    minio:
      persistence:
        existingClaim: "pvc-ff-a-minio" # Bind to legacy data
```

## Review Objectives

Please review this architecture and code with a focus on:

1. **Flexibility:** Can I easily change a specific resource limit or version for _just one_ customer without branching the main chart?
2. **Safety:** Are the resource limits applied correctly? Does the `merge` logic in `_compiler.tpl` ensure that overrides take precedence over defaults?
3. **Maintainability:** Is the `_specs.yaml` structure scalable as we add more services (e.g. Redis, RabbitMQ)?
4. **Refactoring:** Are there any antipatterns in the Go Templating? Is there a cleaner way to handle the "Dependency Injection" (e.g. passing the Postgres URL to FitConnect)?

Provide a critique and 3 specific refactoring suggestions to improve the pattern.
