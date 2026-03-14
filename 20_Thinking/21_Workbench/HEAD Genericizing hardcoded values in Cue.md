---
captured: "2026-03-07T16:54:58+00:00 2026-03-07T16:54:58+00:00"
created: 2026-03-07T16:54:59+00:00
modified: 2026-03-14T11:10:39+00:00
source: "https://claude.ai/chat/93f1bb81-3ab2-45d8-bab7-236bf3563b4f"
status: "processing"
tags: ["input"]
title: HEAD Genericizing hardcoded values in Cue
type: "head"
---

## Raw Output / Content

I am new to cue, but this file feels wrong. It has lots of hard coded values in it. this should be a generic data validation layer that would work with many different configs. should the specific values be passed in for different configs? Can this be made more useful? Review as a data oriented architect

---

Right, Leon. Your instinct is spot on—this file is doing too many jobs at once, and the "generic validation layer" you're sensing it _should_ be is buried under a lot of concrete, deployment-specific configuration. Let me give you the full architectural teardown.

---

## Diagnosis: Three Concerns Masquerading as One File

This file conflates three fundamentally different responsibilities:

1. Schema / Contract—`#InfraFacts` defines the shape of input from Terraform. This is genuinely reusable. ✅
2. Reusable Patterns—`#VSO.map` and the vault secret structure are patterns that _should_ be shared. Partially done. ⚠️
3. Concrete Deployment Config—Hardcoded Auth0 domains, feature flags, probe timings, path patterns, a literal user ID. This is the bit that kills reusability. ❌

The result: you cannot hand this file to a second customer or a second environment without editing it. That's the smell you're picking up on.

---

## The Seven Specific Problems

### 1\. Copy-Pasted Vault Secret Templates (The Biggest Win to Fix)

The MongoDB connection string template appears four times verbatim (fitconnect, ffcloud, frontend, workflowTemplates):

Same for `postgresql.json`, `spicedb.json`, `auth.json`, and the S3 key templates. This is a maintenance trap—one typo in one copy and you've got a deployment divergence that's incredibly hard to diagnose.

What CUE gives you here: Define these as `#VaultTemplate` definitions, just like you did with `#VSO.map`, but for the compound patterns:

Each component then _selects_ which templates it needs rather than redefining them.

### 2\. Environment-Specific Values Hardcoded as "Platform Defaults"

`_platform` is a good instinct—you've started centralising. But the values inside it are concrete, not parameterised:

- `"fitfile-prod.eu.auth0.com"`—This is literally the _prod_ domain. What about staging? Dev? A customer with their own IdP?
- `"64Gi"` persistence—Fine for one cluster size, not for all.
- `"16.5.*"` mongo version—Pins you to a specific chart version.

These should be inputs (either via `#InfraFacts` or a separate `#PlatformConfig` schema), not constants.

### 3\. A Hardcoded User ID on Line 302

This is a specific Auth0 user identifier baked into the config. It will be wrong for every other customer. This _must_ come from the input data.

### 4\. The workflowsApi Node Placement Logic is Broken

Lines 346-359 check whether `_infra.node_placement.nodeSelector` exists… then ignore the actual value and hardcode `agentpool: "workflows"`:

Same for tolerations—it checks for existence then hardcodes `dedicated=workflows`. The input data is being used as a boolean flag, not as actual configuration. Either pass through the real values or make the intent explicit with a dedicated boolean.

### 5\. Feature Flags Are Static Constants

Every flag is `"true"`. If they're always on, why are they flags? If they vary per customer/environment, they need to be inputs. Right now they're noise that obscures the actual configuration surface.

### 6\. No Environment Concept

There's no `env: "prod" | "staging" | "dev"` dimension anywhere. The file _is_ the prod config, implicitly. This means:

- You can't use CUE's constraint system to enforce "staging must not have monitoring pointed at prod Grafana"
- You can't derive sensible defaults per environment (smaller persistence in dev, different Auth0 tenant, etc.)

### 7\. The TLS/Ingress Pattern is Duplicated Three Times

fitconnect, ffcloud, and frontend all repeat this pattern with minor variations:

cue

```
tls: spec: [{
    hosts: [_infra.public_fqdn]
    secretName: "fitfile-\(_infra.customer_short_name)-tls"
}]
ingress: hosts: [{
    hostname: _infra.public_fqdn
    path:     "/some-path"
    pathType: "Prefix"
}]
\`\`\`

The only thing that changes is \`path\` and \`pathType\`. This is a candidate for a \`#IngressSpec\` definition that takes the path as a parameter.

---

## The Target Architecture

Conceptually, you want to split this into three layers:
\`\`\`
┌─────────────────────────────────────┐
│  Layer 1: SCHEMAS & CONSTRAINTS     │  ← Reusable across ALL customers
│  #InfraFacts, #VaultSecret,         │     "What shape must data have?"
│  #IngressSpec, #VaultTemplates      │
├─────────────────────────────────────┤
│  Layer 2: COMPOSITION LOGIC         │  ← Reusable across ALL customers
│  "Given inputs X, produce Helm      │     "How do inputs become outputs?"
│  values Y using patterns Z"         │
├─────────────────────────────────────┤
│  Layer 3: CONCRETE VALUES           │  ← Per-customer / per-environment
│  Auth0 domains, feature flags,      │     "What are the actual values?"
│  admin user IDs, persistence sizes  │
└─────────────────────────────────────┘
```

Right now, all three layers are in one file. Layers 1 and 2 are your "generic data validation layer." Layer 3 is what gets passed in per deployment.

In CUE terms, this means:

- `schema.cue`—All `#Definition` types. The contract. No concrete values.
- `patterns.cue`—`#VSO.map`, `#VaultTemplates`, `#IngressSpec`. Reusable structural patterns.
- `compose.cue`—The logic that takes `#InfraFacts` + `#PlatformConfig` and produces the Helm values structure. References patterns, never hardcodes.
- `customer_acme_prod.cue` (or injected JSON)—The actual concrete values for a specific deployment.

---

## Concrete Next Action

Don't try to refactor this all at once—that's a recipe for paralysis given the file's complexity.

First micro-step: Extract the duplicated vault secret templates into named definitions. This is the highest-value, lowest-risk change because it's purely mechanical and immediately reduces your maintenance surface.

Open the file and add this block right after `#VSO` (line 126):

Then replace each copy-pasted instance with a reference like `mongodb: #VaultTemplates.mongodbConn`. Run `cue vet` after each replacement to confirm nothing broke. One component at a time.

That single change eliminates ~24 duplicated template strings and gives you a foundation to build the rest of the separation on. Want me to produce the refactored file with that first pass applied?
