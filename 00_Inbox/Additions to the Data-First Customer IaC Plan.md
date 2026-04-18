---
created: 2026-04-11T08:35:48+00:00
modified: 2026-04-11T08:49:05+00:00
title: Additions to the Data-First Customer IaC Plan
---

## 1. Pre-Requisite: Fix Live Bugs _Before_ Module Extraction

The plan jumps straight to Direction A (extract into shared module) but your MKUH Brutal Synthesis from Thursday April 9 (~2:04 PM) identified live correctness risks that must be patched first. Extracting a broken `locals.tf` into a shared module amplifies bugs across all customers:

| Bug                                                                                                                                                             | Impact if Extracted Unpatched                                         |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------- |
| VaultAuth split-brain—Terraform (jumpbox.tftpl) and CUE (render_fitfile.cue) both deploy `VaultAuth/default` with conflicting roles (`deployment_key` vs `vso`) | Every customer inherits the conflict; debugging becomes multi-repo    |
| Node pool scheduling—fallback `agentpool="workflow"` vs actual pool key `"workflows"`                                                                           | Pods fail to schedule on every new customer cluster                   |
| TheHyve bypass—raw `.tftpl` path skipping CUE entirely                                                                                                          | Module consumers inherit a known architectural violation as "blessed" |

Recommendation: Add a Phase 0 to the plan: patch these three before any extraction begins. Your MKUH note already has the fix sequence for each.

---

## 2. Missing Principle: The Post-Handoff Rule

Your MASTER_REMEDIATION_PLAN (from Friday April 10 ~12:43 PM) states an "Architecture Law" that the IDE plan doesn't capture:

> Post-handoff rule: ALL non-sensitive downstream config reads from `terraform output -json infra_facts` ONLY.

This means CUE must never read `customer.yaml` directly—it reads `infra_facts`. Without this as an explicit principle, you risk a split-brain where CUE and Terraform have different views of the same customer config. Add it as Principle 5 alongside the existing four.

---

## 3. Missing Principle: Single-Writer Enforcement

Both the MKUH analysis and the Claude Code audit repeatedly flag resources defined in both Terraform and CUE/Helm (VaultAuth, ArgoCD repo creds, `imagePullSecrets`, namespaces). The IDE plan's catalogs implicitly help, but it should be an explicit architectural rule:

> For every resource type, designate exactly one owner (Terraform or CUE/Helm). Document ownership in `CONTRACTS.md`. Remove the competing implementation.

This is the single highest-leverage governance addition—without it, every new integration risks recreating the VaultAuth split-brain pattern.

---

## 4. The "Three Generations" Sunset Path Is Missing

Your MASTER_REMEDIATION_PLAN explicitly identifies three overlapping deployment models coexisting in the codebase:

1. Gen 1—Manual, TFC-only, Confluence-guided, central-services driven
2. Gen 2—Bootstrap-era (`make bootstrap / make finish-bootstrap`), separate provider files
3. Gen 3—Data-driven: `customer.yaml → Terraform → infra_facts → CUE → values.yaml` (the target)

The IDE plan describes the Gen 3 target beautifully but doesn't address how to deprecate/migrate Gen 1 and Gen 2 artifacts. You need:

- An explicit deprecation schedule for Gen 1/Gen 2 patterns (which files, which repos)
- A migration playbook for existing customers still on Gen 2 (how they adopt the shared module)
- Feature flags or compatibility shims in the shared module if Gen 2 customers can't migrate immediately

---

## 5. `infra_facts` Is Mostly Passthrough—Address This

Your MASTER_REMEDIATION_PLAN audit found that only 1 of 21 fields in `infra_facts` comes from a live provisioned resource (`customer_short_name`). The other 20 are derived/computed from YAML. This raises a fundamental question the IDE plan should address:

- Option A: Accept that `infra_facts` is a "normalized config blob" and treat it as the single contract surface between Terraform and CUE. The shared module's job is to produce a _complete, well-typed_ `infra_facts` from the merge of `customer.yaml` + `common.yaml` + provisioned state.
- Option B: Split `infra_facts` into `infra_state` (live resources: AKS endpoints, Vault paths, DNS zones) and `infra_config` (derived/merged YAML passthrough), so CUE can distinguish "this came from Azure" vs "this came from YAML."

Either way, the shared module needs to make this explicit. The current "21 fields, 1 live" situation means `infra_facts` is doing double duty as config bus and state reporter.

---

## 6. `mock_infra.json` Contract Fidelity

The IDE plan mentions CUE validation but doesn't address `mock_infra.json`—which is the thing that makes `cue vet` meaningful in CI. Your MKUH analysis specifically called out:

> _Update `cue/mock_infra.json` so it contains the complete `platform_vault` object and representative `vault_secret_consumers`. The mock must be a faithful representation of the contract._

Add to Direction C: The shared module should generate `mock_infra.json` from a `terraform output -json infra_facts` of a reference environment (e.g., `ff-test-1`), not maintain it by hand. This ensures the mock and reality stay in sync.

---

## 7. TheHyve Has a Specific Remediation Sequence

The IDE plan treats TheHyve as an example under Direction B (catalogs), but your MKUH analysis laid out a precise 3-step sequence that should be a tracked dependency:

1. Create `cue/render_thehyve.cue` using the existing `_VaultSecretsFor` dispatch
2. Extract hardcoded literals (image tag `0.4.5-test`, ACR URLs, resource limits, PG sizes) into `policy_defaults.cue` or a dedicated `#ThehyvePlatformPolicy`
3. Then and only then: delete `generators/thehyve.tf`, `templates/thehyve_values.yaml.tftpl`, and the `thehyve_values_content` outputs

This must complete before `generators/` moves into the shared module (Direction A), otherwise you're shipping a known bypass into the registry.

---

## 8. CI Validation Should Be Mandatory, Not Optional

Direction C says:

> _Optional: validate `customer.yaml` in CI with the same CUE/JSON Schema used by the module_

Given everything you've found this month—silent `try(…)` fallbacks swallowing data, missing fields between layers, aspirational SoT claims—this should be mandatory. The enforcement chain should be:

1. `customer.yaml` validated against a published JSON Schema / CUE definition in the customer repo CI, before `terraform plan`
2. `infra_facts` validated against `#InfraFacts` via `cue vet` after `terraform apply`
3. `generated/values.yaml` diffed against previous before merge

---

## 9. Bootstrap Artifact Cleanup

Your Single Source of Truth plan (April 9 ~5:03 PM) identified that bootstrap and steady-state are "partially intertwined." The IDE plan says bootstrap variables stay as variables—correct—but doesn't address cleaning up bootstrap-only artifacts that persist after Phase A completes:

- Generated provider files from `make bootstrap`
- Targeted apply scripts
- One-time credential seeding code

The shared module should have a `post_bootstrap_cleanup` target or at least document what's safe to delete after the first successful TFC run.

---

## 10. Sequencing Summary

Given all of the above, here's the execution order I'd recommend:

| Step | What                                                                 | Depends On                       |
| ---- | -------------------------------------------------------------------- | -------------------------------- |
| 0    | Patch VaultAuth split-brain, node pool label, TheHyve bypass         | Nothing—do now                   |
| 1    | Enforce single-writer rule + document in CONTRACTS.md                | Step 0                           |
| 2    | Extract merge helpers into shared module (incremental, not big-bang) | Step 1                           |
| 3    | Replace imperative lists with platform catalogs (Direction B)        | Step 2                           |
| 4    | Move generators/ into shared module (Direction A completion)         | Steps 2+3 + TheHyve fully in CUE |
| 5    | Align ArgoCD app-of-apps (Direction D)                               | Step 3                           |
| 6    | Mandatory CI gates (Direction C, non-optional)                       | Steps 2+4                        |
| 7    | Gen 1/Gen 2 deprecation + customer migration                         | Steps 4+6 stable                 |

---

## Bottom Line

The IDE plan is architecturally correct but insufficiently sequenced. It describes the destination without accounting for the landmines your audit already found on the path. The biggest additions are:

1. Fix live bugs before extracting (don't ship known defects into a shared module)
2. Post-handoff rule as a first-class principle (CUE reads `infra_facts`, never `customer.yaml`)
3. Single-writer enforcement (the root cause of the VaultAuth class of bug)
4. Three-generation sunset path (the plan assumes Gen 3 only; reality has Gen 1+2 still in flight)
5. Mandatory, not optional, CI validation (the whole contract story falls apart without enforcement)

The plan's risk callout about big-bang extraction is spot-on—your own MASTER_REMEDIATION_PLAN confirms incremental is the only safe path. Start with Step 0 patches, then extract merge helpers, then catalogs, then generators.
