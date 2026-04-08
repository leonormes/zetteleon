---
created: 2026-04-04T10:42:40+00:00
modified: 2026-04-08T18:01:21+00:00
tags: [_VaultSecretsFor, InfraFacts, PlatformPolicy, RenderThehyveValues, ThehyvePlatformPolicy, VSO]
title: mkuh
---

This is a classic case of a solid architectural spine buckling under the weight of operational exceptions and deadline-driven shortcuts. Both analyses are spot on, but when combined, they reveal a clear hierarchy of technical debt. We have live correctness risks (silent Terraform bugs and resource conflicts) mixed with blatant layer violations (TheHyve bypassing the pipeline).

I have analysed and consolidated the feedback into a single, uncompromising, and prioritised refactoring plan.

---

## Brutal Synthesis

The core GitOps intent (`customer.yaml` → `locals.tf` → `infra_facts` → CUE) is healthy, but the execution is sloppy. The platform is currently suffering from a "split brain" where Terraform and Argo CD are fighting over Vault authentication, Terraform variable types are silently swallowing data, and a massive architectural bypass (TheHyve) has been bolted onto the side. We need to fix the live bugs first, then force the rogue components back into the standard data pipeline.

---

## The Consolidated Refactoring Plan

This plan is broken down into three strict phases, ordered by operational risk and architectural integrity.

### Phase 1: Critical State Conflicts & Contract Bugs (Fix Immediately)

These issues are actively causing silent failures or resource fighting.

- 1.1 Resolve the `VaultAuth` Split-Brain: Terraform (`jumpbox.tftpl`) and CUE (`render_fitfile.cue`) are both deploying `VaultAuth/default` into the deployment and `argocd` namespaces, but with conflicting roles (`deployment_key` vs `"vso"`) and audience specs.
    - Action: Choose a single owner. If CUE/Helm owns application secrets, remove the `kubectl_manifest.vault_auth` from `jumpbox.tftpl` for those specific namespaces. Standardise the `role` and `audiences` to whatever Vault's JWT backend is actually expecting.
- 1.2 Patch the `generators/variables.tf` Silent Data Loss: The `platform_vault` variable type definition is missing keys (e.g., `argocd_path`, `argo_workflows`, `monitoring`). Because Terraform strictly checks object types, it silently strips these undeclared attributes, resulting in empty string interpolations in templates.
    - Action: Update the variable type definition to perfectly mirror the `#InfraFacts.platform_vault` schema in CUE. Ensure defaults are mapped securely from `common.yaml`.
- 1.3 Fix the Node Pool Scheduling Bug: The fallback `node_placement` specifies `agentpool = "workflow"`, while the actual AKS node pool key is `workflows`. This guarantees pods will fail to schedule.
    - Action: Standardise the literal label value in `platform-defaults/common.yaml` and reference it consistently.

### Phase 2: Architectural Realignment (TheHyve)

TheHyve currently bypasses CUE completely, relying on raw, hardcoded Terraform templates. This destroys the single source of truth.

- 2.1 Force TheHyve into the CUE Pipeline:
    - Action: Create `cue/render_thehyve.cue`. Move all Vault Secrets Operator (VSO) wiring into `infra.vault_secret_consumers["thehyve"]` using the existing `_VaultSecretsFor` dispatch mechanism.
- 2.2 Extract TheHyve Literals:
    - Action: Rip out the hardcoded `0.4.5-test` image tag, ACR registry URLs, resource limits, and PostgreSQL sizes from the `.tftpl` file. Move these into `policy_defaults.cue` or a dedicated `#ThehyvePlatformPolicy`.
- 2.3 Burn the Bypass:
    - Action: Once CUE is generating the TheHyve configuration, delete `generators/thehyve.tf`, `templates/thehyve_values.yaml.tftpl`, and the `thehyve_values_content` outputs entirely.

### Phase 3: Data-Flow Hygiene & Eviction

`locals.tf` has become a dumping ground for platform constants that belong in `common.yaml`, and `render_fitfile.cue` is littered with hardcoded strings.

- 3.1 Purge `locals.tf` of Platform Constants:
    - Action: Evict all fallbacks to `platform-defaults/common.yaml`. This includes: `s3_export` paths, platform system namespaces (`argo`, `argocd`, `ingress-nginx`), Auth0 pool key mappings, and default Kubernetes/VM sizes. `locals.tf` must only merge data (`try(local.config.X, local.common.X)`), not author it.
- 3.2 Fix the `argocd_applications` Default:
    - Action: Remove `key = "thehyve"` from the default `argocd_applications` list in `locals.tf`. TheHyve is a customer-specific deployment (MKUH), not a platform-wide default. This must be defined in `config/customer.yaml`.
- 3.3 Eliminate Dead Code & Empty Stubs:
    - Action: Delete the commented-out `thehyve_password_config` blocks in `locals.tf`. Furthermore, delete the 14 empty string stubs under `vault_secrets.thehyve.static_data` in `customer.yaml`. If a secret is required, it must be properly seeded via the pipeline; empty stubs add nothing but noise.
- 3.4 Update Mock Data Contracts:
    - Action: Update `cue/mock_infra.json` so it contains the complete `platform_vault` object and representative `vault_secret_consumers`. The mock must be a faithful representation of the contract to ensure `cue vet` is actually validating reality.

---

Phase 1 addresses live infrastructure risks and should be executed immediately. Are you ready for me to outline the specific Terraform code changes required to patch the `variables.tf` contract bug and resolve the `VaultAuth` split-brain?
