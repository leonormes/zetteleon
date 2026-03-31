---
created: 2026-03-31T14:50:52+00:00
modified: 2026-03-31T14:59:29+00:00
title: Network Topography & fitConnectHosts
---

## Helm Deployment Analysis: Network Topography & fitConnectHosts

This report maps the current state of our FFNode deployments, identifying critical anti-patterns and performance risks related to tenant resolution and internal networking.

### 1. Network Topography

Based on the `deploy.coordinatingStation` configuration, our environments are categorized into two primary roles:

| Category | Environments | Description |
|:--- |:--- |:--- |
| Coordinating Hubs | `ff-test-b`, `ff-test-c`, `ff-b`, `ff-c` | Set `coordinatingStation: true`. These nodes act as central hubs for federation and coordination. |
| Standalone Nodes | `nwsde-prod-1`, `mcnft-prod-1`, `barts-prod`, `eoe-prod-34`, `nnuh-prod-1`, `cuh-prod-1`, `ff-hyve-1/2` | The majority of deployments. These are local data nodes that may reference external hubs but often operate independently for local tenant context. |

### 2. Anti-Pattern Audit

We scanned all `values.yaml` files for the identified anti-patterns.

#### Key Anti-Patterns Found

- MISSING_SELF_REFERENCE: The node does not list its own `fitConnectCode` in the `fitConnectHosts` array. This triggers external lookups for local data.
- PUBLIC_URL_USED_LOCALLY: The node lists itself but uses a public ingress URL (e.g., `https://nwsde-prod-1.fitfile.net`) instead of an internal service URL.
- MISSING_ALLOWED_ORIGIN: The `ffcloud.appConfig.allowedOrigin` field is blank, potentially causing CORS issues in federated setups.

#### Environment Audit

| Environment | fitConnectCode | Status | Findings |
|:--- |:--- |:--- |:--- |
| nwsde-prod-1 | `North West SDE` | 🔴 CRITICAL | Missing self-reference. Lists `lca-prd-2` and `MCNFT PROD 1` but not itself. |
| mcnft-prod-1 | `MCNFT PROD 1` | 🔴 CRITICAL | Missing self-reference. Lists nothing. |
| barts-prod | `Barts Prod` | 🔴 CRITICAL | Missing self-reference. Lists nothing. |
| ff-hyve-1 | `NHS Provider 1` | 🔴 CRITICAL | Missing self-reference. Lists nothing. |
| ff-hyve-2 | `NHS Provider 2` | 🔴 CRITICAL | Missing self-reference. Lists nothing. |
| eoe-prod-34 | `EOE SDE CODISC` | 🟡 WARNING | Non-Cluster URLs. Lists itself but uses `http://hie-prod-34-ffcloud-service` (no `.svc.cluster.local`). |
| ff-eoe-sde | `NHS SDE` | 🟢 OK-ISH | Lists itself internally, but missing `allowedOrigin`. |
| fitfile (ff-test-a/b/c) | Various | 🟡 WARNING | Highly inconsistent use of internal vs external URLs for cross-references. |

> [!IMPORTANT]
> nwsde-prod-1 is verified to be missing its own local entry, directly causing the `ECONNABORTED` incident by forcing the pod to hairpin through the public internet to reach its own `/tenants` endpoint.

### 3. Cross-Environment Consistency Check

We found significant drift in how services are referenced across different environments:

| Target Node | Reference Patterns Found |
|:--- |:--- |
| FITConnect A | `http://ff-test-a-ffcloud-service`, `https://app.fitfile.net/ffcloud`, `http://ff-a-ffcloud-service/ffcloud` |
| FITConnect B | `http://ff-test-b-fitconnect-ftc.ff-test-b.svc`, `https://ff-test-b.fitfile.net/ffcloud` |
| EOE SDE CODISC| `http://hie-prod-34-fitconnect-ftc`, `http://hie-test-34-fitconnect-ftc` |

Missing Ports: Most external references omit explicit ports (relying on 443). However, if an environment like `lca-prd-2` were moved to a non-standard port, updated values would need to be manually propagated to all referencing nodes—a high-risk manual step.

### 4. Proposed Architectural Improvements

To prevent these issues, we recommend transitioning from manual array management to dynamic host injection.

#### Recommended Pattern: The "Auto-Loopback" Helper

Modify the base Helm chart to automatically prepend the local service URL to the `fitConnectHosts` array during rendering.

```yaml
# Proposed logic in ffcloud deployment template
- name: APPCONFIG_FITCONNECTHOSTS
  value: |
    {{- $hosts := .Values.ffcloud.appConfig.fitConnectHosts | default list -}}
    {{- /* Check if self is already in the list */ -}}
    {{- $hasSelf := false -}}
    {{- range $hosts -}}
      {{- if eq .fitConnectCode ($.Values.global.fitConnectCode | default "") -}}
        {{- $hasSelf = true -}}
      {{- end -}}
    {{- end -}}
    {{- /* Auto-inject local loopback if missing */ -}}
    {{- if not $hasSelf -}}
      {{- $localEntry := dict 
          "fitConnectCode" .Values.global.fitConnectCode 
          "fitConnectUri" (printf "http://%s-fitconnect-ftc.%s.svc.cluster.local/fitconnect" .Release.Name .Release.Namespace)
          "coordinatorUri" (printf "http://%s-ffcloud-service.%s.svc.cluster.local/ffcloud" .Release.Name .Release.Namespace)
          "cryptoUri" "" -}}
      {{- $hosts = prepend $hosts $localEntry -}}
    {{- end -}}
    {{- $hosts | toJson -}}
```

#### Key Rationale

1. Enforced Local-First: Developers only need to define _external_ nodes. The "Self" node is always present and always internal.
2. DNS Resilience: Uses the fully qualified name (`.svc.cluster.local`) which is faster and more reliable than public ingress.
3. DRY Values: Reduces the `values.yaml` size and eliminates the primary source of copy-paste errors.

## `fitConnectHosts` Network Topology & Configuration Audit

### 1. Network Topography

#### Coordinating Hubs

Nodes that own a `fitConnectHosts` config and serve as the federated query entry point:

| Hub            | Namespace      | Public Host                                   | Coordinates                         |
| -------------- | -------------- | --------------------------------------------- | ----------------------------------- |
| `ff-a`         | `ff-a`         | `app.fitfile.net`                             | ff-b, ff-c, barts (prod)            |
| `ff-test-a`    | `ff-test-a`    | `ff-test-a.fitfile.net`                       | ff-test-b, ff-test-c                |
| `hie-prod-34`  | `hie-prod-34`  | `app.eoe-sde-codisc.privatelink.fitfile.net`  | cuh-prod-1, nnuh-prod-1, ff-a, ff-c |
| `nwsde-prod-1` | `nwsde-prod-1` | `nwsde-prod-1.fitfile.net`                    | lca-prd-2 (external), mcnft-prod-1  |
| `ff-eoe-sde`   | `ff-eoe-sde`   | `app.ff-eoe-sde.privatelink.fitfile.net`      | ff-hyve-1, ff-hyve-2                |
| `kch/prod`     | `kch`          | `fitfile.kingsch.nhs.uk`                      | standalone                          |
| `kch/mn4`      | _(sandbox)_    |—| standalone                          |
| `stg/sandbox`  | `stg-sandbox`  | `fitfile.net.stgeorges.nhs.uk`                | standalone                          |
| `hie-test-34`  | `hie-test-34`  | `app.eoe-test-codisc.privatelink.fitfile.net` | standalone (self-only)              |

#### Satellite / Coordinating-Station Nodes

`deploy.coordinatingStation: true`, no `fitConnectHosts`, register upstream:

| Node                        | Upstream Hub                                      |
| --------------------------- | ------------------------------------------------- |
| `ff-b`, `ff-c`              | `ff-a`                                            |
| `ff-test-b`, `ff-test-c`    | `ff-test-a`                                       |
| `ff-hyve-1`, `ff-hyve-2`    | `ff-eoe-sde`                                      |
| `mcnft-prod-1`              | `nwsde-prod-1`                                    |
| `cuh-prod-1`, `nnuh-prod-1` | `hie-prod-34`                                     |
| `barts/prod`                | implicitly `ff-a` (shares spicedb/argo-workflows) |

#### Private-link / Dev Nodes

No federation config: `sandbox-testing-1`, `development`, `testing`, `pv-aks-1`, `wm-dev-1`, `gh-pt-1`, `ff-wmsde-1`, `acr-test`.

---

### 2. Anti-Pattern Audit—Environment by Environment

#### `nwsde/nwsde-prod-1`—THE INCIDENT NODE 🔴

```yaml
fitConnectHosts:
- fitConnectCode: "lca-prd-2"
fitConnectUri: "https://lca-prd-2.fitfile.net/fitconnect"
coordinatorUri: https://lca-prd-2.fitfile.net/ffcloud
- fitConnectCode: "MCNFT PROD 1"
fitConnectUri: "https://mcnft-prod-1.fitfile.net/fitconnect"
coordinatorUri: https://mcnft-prod-1.fitfile.net/ffcloud
```

| Anti-Pattern            | Status                                          |
| ----------------------- | ----------------------------------------------- |
| Missing self-entry      | ❌ CONFIRMED—no entry for `nwsde-prod-1` itself |
| Self uses public URL    | N/A (no self-entry)                             |
| Missing `allowedOrigin` | ✅ present (`".*\\.fitfile.net"`)               |

Root cause of the incident confirmed. The node has no internal self-reference. On startup, tenant resolution queries the first available host, which is `lca-prd-2` over the public internet. That node blocks `/tenants` as internal-only → `403 Forbidden`. The `ECONNABORTED` was likely a timeout on a subsequent retry. Fix: add a self-entry using the internal service URL before the peer entries.

---

#### `fitfile/ff-a`—Production Hub 🟡

```yaml
fitConnectHosts:
- fitConnectCode: FITConnect A # self
fitConnectUri: https://app.fitfile.net/fitconnect # ⚠️ PUBLIC
coordinatorUri: http://ff-a-ffcloud-service/ffcloud # ⚠️ short hostname
- fitConnectCode: FITConnect B
fitConnectUri: https://app2.fitfile.net/fitconnect
coordinatorUri: https://app2.fitfile.net/ffcloud
- fitConnectCode: FITConnect C
fitConnectUri: https://app3.fitfile.net/fitconnect
coordinatorUri: https://app3.fitfile.net/ffcloud
```

| Anti-Pattern                              | Status                                                              |
| ----------------------------------------- | ------------------------------------------------------------------- |
| Missing self-entry                        | ✅ present                                                          |
| Self `fitConnectUri` uses public URL      | ⚠️ YES—routes through Cloudflare/ingress to reach itself            |
| Self `coordinatorUri` uses short hostname | ⚠️ `http://ff-a-ffcloud-service/ffcloud`—no namespace qualifier     |
| Missing `allowedOrigin`                   | ❌ MISSING—CORS risk on production hub                              |
| Peers use public `coordinatorUri`         | ⚠️ ff-b and ff-c route through public ingress for coordinator calls |

The short `http://ff-a-ffcloud-service/ffcloud` works only because the service lives in the same namespace as the pod doing the resolution. It will silently fail if ever called from a cross-namespace context.

---

#### `fitfile/ff-test-a`—Staging Hub 🟡

```yaml
fitConnectHosts:
- fitConnectCode: FITConnect A # self
fitConnectUri: http://ff-test-a-fitconnect-ftc.ff-test-a.svc/fitconnect # ✅ internal svc (partial FQDN)
coordinatorUri: http://ff-test-a-ffcloud-service/ffcloud # ⚠️ short hostname
- fitConnectCode: FITConnect B
fitConnectUri: http://ff-test-b-fitconnect-ftc.ff-test-b.svc/fitconnect # ✅ internal svc
coordinatorUri: https://ff-test-b.fitfile.net/ffcloud # ⚠️ PUBLIC coordinator
- fitConnectCode: FITConnect C
fitConnectUri: https://ff-test-c-fitconnect-ftc.ff-test-c.svc/fitconnect # ❌ https:// on svc URL — TLS will fail
coordinatorUri: https://ff-test-c.fitfile.net/ffcloud # ⚠️ PUBLIC coordinator
```

| Anti-Pattern                                               | Status                                                             |
| ---------------------------------------------------------- | ------------------------------------------------------------------ |
| Missing self-entry                                         | ✅ present                                                         |
| Self uses public URL                                       | ✅ `fitConnectUri` is internal                                     |
| Self `coordinatorUri` uses short hostname                  | ⚠️ no namespace in coordinator                                     |
| `allowedOrigin`                                            | ✅ present                                                         |
| Peers use public `coordinatorUri`                          | ⚠️ ff-test-b and ff-test-c coordinator calls go public             |
| ff-test-c `fitConnectUri` has `https://` on a svc hostname | ❌ BUG—in-cluster service DNS has no TLS cert, should be `http://` |

The comment in the file explicitly acknowledges the public-vs-internal issue for `fitConnectUri` ("Changing this to avoid the cloudflare max json payload size")—this is a known workaround, but `coordinatorUri` for peers was not fixed at the same time.

---

#### `eoe/hie-prod-34`—EOE SDE Production Hub 🟡

```yaml
fitConnectHosts:
- fitConnectCode: "EOE SDE CODISC" # self
fitConnectUri: http://hie-prod-34-fitconnect-ftc/fitconnect # ⚠️ short hostname
coordinatorUri: http://hie-prod-34-ffcloud-service/ffcloud # ⚠️ short hostname
- fitConnectCode: "CUH PROD 1"
fitConnectUri: "https://cuh-prod-1.fitfile.net/fitconnect"
coordinatorUri: https://cuh-prod-1.fitfile.net/ffcloud
- fitConnectCode: "NNUH PROD 1"
fitConnectUri: "https://nnuh-prod-1.fitfile.net/fitconnect"
coordinatorUri: https://nnuh-prod-1.fitfile.net/ffcloud
- fitConnectCode: "FITConnect A"
fitConnectUri: https://app.fitfile.net/fitconnect
coordinatorUri: https://app.fitfile.net/ffcloud
- fitConnectCode: "FITConnect C"
fitConnectUri: https://app3.fitfile.net/fitconnect
coordinatorUri: https://app3.fitfile.net/ffcloud
```

| Anti-Pattern             | Status                                        |
| ------------------------ | --------------------------------------------- |
| Missing self-entry       | ✅ present                                    |
| Self uses public URL     | ✅ No (uses internal service hostname)        |
| Self uses short hostname | ⚠️ no `.hie-prod-34.svc.cluster.local` suffix |
| Missing `allowedOrigin`  | ❌ MISSING—CORS risk on prod node             |

---

#### `eoe/hie-test-34`—EOE SDE Test (Standalone) 🟡

```yaml
fitConnectHosts:
- fitConnectCode: "EOE SDE CODISC" # self only
fitConnectUri: http://hie-test-34-fitconnect-ftc/fitconnect
coordinatorUri: http://hie-test-34-ffcloud-service/ffcloud
```

| Anti-Pattern             | Status                                   |
| ------------------------ | ---------------------------------------- |
| Missing self-entry       | ✅ has itself (standalone—only one entry) |
| Self uses short hostname | ⚠️ no namespace qualifier                |
| Missing `allowedOrigin`  | ❌ MISSING                                |

---

#### `eoe/ff-eoe-sde`—EOE SDE Hub 🟠

```yaml
fitConnectHosts:
- fitConnectCode: "NHS SDE" # self
fitConnectUri: http://ff-eoe-sde-fitconnect-ftc/fitconnect
cryptoUri: ""
# ❌ NO coordinatorUri for self
- fitConnectCode: "NHS Provider 1"
fitConnectUri: https://nhs-provider-1.fitfile.net/fitconnect
# ❌ NO coordinatorUri for Provider 1 either
- fitConnectCode: "NHS Provider 2"
fitConnectUri: https://nhs-provider-2.fitfile.net/fitconnect
# ❌ NO coordinatorUri for Provider 2 either
```

| Anti-Pattern                            | Status                                                                     |
| --------------------------------------- | -------------------------------------------------------------------------- |
| Missing self-entry                      | ✅ present (`fitConnectUri`)                                                |
| Missing `coordinatorUri` on ALL entries | ❌ ALL entries lack `coordinatorUri`—coordinator-mediated queries will fail |
| Missing `allowedOrigin`                 | ❌ MISSING                                                                  |
This is a significant gap. If `coordinatorUri` is required for tenant resolution or orchestration, every federated call from this node is misconfigured.

---

#### `kch/prod` & `kch/mn4`—KCH (old-style Separate chart) 🟡

```yaml
# kch/prod
fitConnectHosts:
- fitConnectCode: KCH Prod
fitConnectUri: http://fitconnect-service # ⚠️ bare service name, no release prefix, no namespace
cryptoUri: http://crypto-service
# kch/mn4
fitConnectHosts:
- fitConnectCode: KCH Sandbox
fitConnectUri: http://fitconnect-service
cryptoUri: http://crypto-service
allowedOrigin: ".*\\.fitfile.net" # ✅ present
```

| Anti-Pattern                                              | kch/prod                                 | kch/mn4 |
| --------------------------------------------------------- | ---------------------------------------- | ------- |
| Self-entry present                                        | ✅                                        | ✅       |
| `coordinatorUri` missing                                  | ❌                                        | ❌       |
| Uses bare service names (no release prefix, no namespace) | ⚠️ (likely intentional—old chart schema) | ⚠️      |
| `allowedOrigin`                                           | ❌ MISSING                                | ✅       |

---

#### `stg/sandbox`—St George's (old-style chart) 🟡

```yaml
fitConnectHosts:
- fitConnectCode: STG Sandbox
fitConnectUri: http://stg-sandbox-fitconnect-ftc # ⚠️ short hostname, no namespace
cryptoUri: http://crypto-service
```

| Anti-Pattern             | Status    |
| ------------------------ | --------- |
| Self-entry present       | ✅         |
| `coordinatorUri` missing | ❌         |
| Short hostname           | ⚠️        |
| `allowedOrigin`          | ❌ MISSING |

---

#### `barts/prod`—Standalone Node 🟠

No `fitConnectHosts` configured at all, despite being a fully deployed production node (`ffCloudCode: FFCloud_Barts_Prod`, with `machineToUserConfig`). It shares `argo-workflows.fitfile.net` and `ac.fitfile.net` with `ff-a`, suggesting it is treated as a satellite—but there is no `coordinatingStation: true` flag, no `coordinator.namespace`, and no entry in `ff-a`'s `fitConnectHosts` for Barts. Barts appears to be orphaned from the federation.

---

### 3. Cross-Environment Consistency Check

#### `lca-prd-2` Port Alignment

`lca-prd-2` is referenced only in `nwsde-prod-1` using `https://lca-prd-2.fitfile.net/fitconnect` (port 443 implied). If `lca-prd-2` is running on `:11001`, every URL referencing it is wrong and would silently time out or refuse. There is no `lca-prd-2` values file in this repo—it is externally managed—but the port must be verified and corrected:

```yaml
# If lca-prd-2 runs on :11001, this must be:
fitConnectUri: "https://lca-prd-2.fitfile.net:11001/fitconnect"
coordinatorUri: "https://lca-prd-2.fitfile.net:11001/ffcloud"
```

#### Asymmetric Federation: `hie-prod-34` ↔ `ff-a`

`hie-prod-34` lists `ff-a` and `ff-c` in its federation config, but `ff-a`'s own `fitConnectHosts` does not include `hie-prod-34`. The topology is unidirectional: `hie-prod-34` can initiate calls to `ff-a`, but `ff-a` cannot initiate calls back to `hie-prod-34`. Whether intentional, this should be documented.

#### `https://` On a Cluster-internal Svc URL in `ff-test-a`

`ff-test-c` peer entry in `ff-test-a`:

```yaml
fitConnectUri: https://ff-test-c-fitconnect-ftc.ff-test-c.svc/fitconnect # ❌
```

In-cluster service DNS does not have TLS certificates. This should be `http://`.

---

### 4. Findings Summary

| Environment    | Missing Self | Self Uses Public URL |  Short Hostname  | Missing `allowedOrigin` | Missing `coordinatorUri` | Other                               |
| -------------- | :----------: | :------------------: | :--------------: | :---------------------: | :----------------------: | ----------------------------------- |
| `nwsde-prod-1` |      🔴      |         N/A          |       N/A        |            ✅            |           N/A            | lca-prd-2 port unverified           |
| `ff-a`         |      ✅       |   ⚠️ fitConnectUri   |  ⚠️ coordinator  |           🔴            |            ✅             | peers use public coordinator        |
| `ff-test-a`    |      ✅       |          ✅           |  ⚠️ coordinator  |            ✅            |            ✅             | ff-test-c has `https://` on svc URL |
| `hie-prod-34`  |      ✅       |          ✅           |        ⚠️        |           🔴            |            ✅             | asymmetric with ff-a                |
| `hie-test-34`  |      ✅       |          ✅           |        ⚠️        |           🔴            |            ✅             | —                                   |
| `ff-eoe-sde`   |      ✅       |          ✅           |        ⚠️        |           🔴            |      🔴 all entries      | —                                   |
| `kch/prod`     |      ✅       |          ✅           | ⚠️ (intentional) |           🔴            |            🔴            | old chart schema                    |
| `kch/mn4`      |      ✅       |          ✅           |        ⚠️        |            ✅            |            🔴            | old chart schema                    |
| `stg/sandbox`  |      ✅       |          ✅           |        ⚠️        |           🔴            |            🔴            | old chart schema                    |
| `barts/prod`   |  🟠 no list  |         N/A          |       N/A        |           🔴            |           N/A            | orphaned from federation            |

---

### 5. Architectural Recommendations

#### Rec 1: Auto-inject the Self-entry in the Helm Chart (eliminates the Entire Incident class)

The self-entry should never be in `values.yaml`. Move it into `_helpers.tpl` so the chart computes and prepends it automatically from `{{.Release.Name }}` and `{{.Release.Namespace }}`:

```yaml
{{/* _helpers.tpl */}}
{{- define "ffnode.selfFitConnectEntry" -}}
- fitConnectCode: {{ .Values.global.fitConnectCode | quote }}
fitConnectUri: http://{{ .Release.Name }}-fitconnect-ftc.{{ .Release.Namespace }}.svc.cluster.local/fitconnect
coordinatorUri: http://{{ .Release.Name }}-ffcloud-service.{{ .Release.Namespace }}.svc.cluster.local/ffcloud
cryptoUri: ""
{{- end }}
```

In the template that renders the app config:

```yaml
fitConnectHosts:
{{- include "ffnode.selfFitConnectEntry" . | nindent 2 }}
{{- toYaml .Values.ffcloud.appConfig.fitConnectHosts | nindent 2 }}
```

Values files then only declare _peers_:

```yaml
# nwsde-prod-1/values.yaml — AFTER fix
ffcloud:
appConfig:
fitConnectHosts: # PEERS ONLY — self is injected by the chart
- fitConnectCode: "lca-prd-2"
fitConnectUri: "https://lca-prd-2.fitfile.net:11001/fitconnect"
coordinatorUri: "https://lca-prd-2.fitfile.net:11001/ffcloud"
cryptoUri: ""
- fitConnectCode: "MCNFT PROD 1"
fitConnectUri: "https://mcnft-prod-1.fitfile.net/fitconnect"
coordinatorUri: "https://mcnft-prod-1.fitfile.net/ffcloud"
cryptoUri: ""
```

This makes a "missing self-entry" literally impossible to commit.

#### Rec 2: Set `allowedOrigin` as a Chart-level Default

Add it to the chart's base `values.yaml` so omitting it in environment values still produces a safe output:

```yaml
# charts/components/ffnode/values.yaml (chart defaults)
ffcloud:
appConfig:
allowedOrigin: ".*\\.fitfile.net"
```

Environments that need a stricter pattern override it; environments that forget it get the standard wildcard.

#### Rec 3: Standardise URL Scheme for Peers

Adopt a two-tier convention and document it explicitly:

| Peer type                         | `fitConnectUri`                                                            | `coordinatorUri`                                                         |
| --------------------------------- | -------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| Same cluster, different namespace | `http://<release>-fitconnect-ftc.<namespace>.svc.cluster.local/fitconnect` | `http://<release>-ffcloud-service.<namespace>.svc.cluster.local/ffcloud` |
| Cross-cluster (external node)     | `https://<env>.fitfile.net/fitconnect`                                     | `https://<env>.fitfile.net/ffcloud`                                      |
| Custom port (e.g. lca-prd-2)      | `https://<env>.fitfile.net:<port>/fitconnect`                              | `https://<env>.fitfile.net:<port>/ffcloud`                               |
Enforce this with a Helm schema validation (`values.schema.json`) that rejects entries where `fitConnectUri` contains a public hostname for a same-cluster peer, or where `coordinatorUri` is missing entirely.

#### Rec 4: Add `values.schema.json` Validation

```json
{
"properties": {
"ffcloud": {
"properties": {
"appConfig": {
"properties": {
"fitConnectHosts": {
"type": "array",
"items": {
"required": [
"fitConnectCode",
"fitConnectUri",
"coordinatorUri"
],
"properties": {
"coordinatorUri": {
"type": "string",
"minLength": 1
}
}
}
}
}
}
}
}
}
}
```

This would have caught the `ff-eoe-sde` and `kch` entries missing `coordinatorUri` at `helm lint` time.

#### Rec 5: Immediate Remediation Priority

| Priority        | Action                                                            | Environments                                                                 |
| --------------- | ----------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| 🔴 Critical     | Add self-entry with internal FQDN. Verify `lca-prd-2` port.       | `nwsde-prod-1`                                                               |
| 🟠 High         | Add `allowedOrigin`                                               | `ff-a`, `hie-prod-34`, `ff-eoe-sde`, `stg/sandbox`, `kch/prod`, `barts/prod` |
| 🟡 Medium       | Add missing `coordinatorUri` entries                              | `ff-eoe-sde`, `kch/prod`, `kch/mn4`, `stg/sandbox`                           |
| 🟡 Medium       | Fix `https://` on svc URL                                         | `ff-test-a` (ff-test-c peer entry)                                           |
| 🟡 Medium       | Clarify federation membership                                     | `barts/prod`                                                                 |
| 🟢 Low          | Qualify all short hostnames with `.<namespace>.svc.cluster.local` | `ff-a`, `hie-prod-34`, `hie-test-34`, `ff-eoe-sde`                           |
| 🟢 Architecture | Implement Rec 1—move self-entry into `_helpers.tpl`               | All ffnode charts                                                            |
