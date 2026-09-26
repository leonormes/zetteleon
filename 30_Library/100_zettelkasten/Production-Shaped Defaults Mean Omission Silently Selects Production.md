---
conformant: true
created: 2026-09-23T14:48:58+00:00
created_utc: '2026-09-23T00:00:00Z'
modified: 2026-09-25T16:29:29+00:00
permalink: llmeon/00-inbox/production-shaped-defaults-mean-omission-silently-selects-production
source_title: Multi-customer Deployment Review, and an Assessment of CUE
source_url: N/A — internal engineering assessment
status: seed
tags: [configuration-management, defaults, environment-config]
title: Production-Shaped Defaults Mean Omission Silently Selects Production
type: claim
upstream: '[[CUE-ASSESSMENT]]'
---

## Production-Shaped Defaults Mean Omission Silently Selects Production

A default value shaped for production, with no `env: dev | live` discriminator anywhere in the values contract, means a non-production customer who omits the corresponding override inherits production configuration.

### Scope & Conditions

Applies to any default field where the chart's default value is correct for only a subset of environments and no explicit environment type is validated.

### Evidence

> "`charts/ffnode/values.yaml` defaults `global.oauth.baseURL` to `https://fitfile-prod.eu.auth0.com`. Five nodes inherit it … for anything non-production that inherits it, omitting a line selects production."

### Implications

- The failure mode is invisible at the point of omission—nothing fails, the wrong environment is simply selected.
- Modelling environment as a closed disjunction would make the wrong combination structurally unrepresentable.

### Related

- [[SoT - Pattern - CUE Data Architecture]]—shared mechanism: Pattern 1's `profile: "dev" | "stage" | "prod"` disjunction is exactly the missing discriminator this claim needs.
- [[SoT - Generative Infrastructure Configuration Framework]]—extends: environment identity belongs in the Configuration Kernel, per that SoT's "One Home" hierarchy.
