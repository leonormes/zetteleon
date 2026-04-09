---
created: 2026-04-09T20:18:26+00:00
modified: 2026-04-09T20:24:44+00:00
title: MASTER_REMEDIATION_PLAN
---

## Master Remediation Plan & Strategic Roadmap

Date: 2026-04-09
Sources consolidated:

- `ff-test-1/docs/PIPELINE_AUDIT.md`—Terraform → CUE → Helm contract findings
- `Network Topography & fitConnectHosts.md`—multi-environment network anti-patterns
- `Single Source of Truth Customer Deployment Plan.md`—strategic architecture direction
- `mkuh-prod-4: Customer Deployment Automation — Phased Improvement Plan`—phased execution model and success criteria

> Stale assumption corrected: The phased improvement plan describes `vault_secret_consumers` as "dead code—defined but never read by `render_fitfile.cue`". This was true at time of writing. It is false as of current code: `vault_secret_dispatch.cue:14` reads `infra.vault_secret_consumers[app]` and `render_fitfile.cue` calls `#vaultSecretsList` at 10 call sites. Phase 5 of that plan is ~70% done mechanically. The remaining work is documentation accuracy and removing the dual-path shell script—not implementing the CUE mechanism. See Part 1 (What Is Already Fixed) and P-3.

This is the single planning document for both immediate fixes and the longer roadmap. `PIPELINE_AUDIT.md` and the network topology doc contain the original detailed evidence; this document is the actionable master list.

---

### Status Key

| Symbol | Meaning |
|:---:|---|
| ✅ | Fixed—verified in current code |
| 🔴 | Open—critical, fix before next deploy |
| 🟠 | Open—high priority |
| 🟡 | Open—medium priority |
| 🟢 | Open—low / architectural |

---

### Part 0—Strategic Context

#### The Core Problem: Three Generations in One Codebase

The system is mid-transition between three overlapping deployment models that are all partially visible:

1. Generation 1—older manual steps, TFC-only, Confluence-guided, central-services driven. Still present in some docs and jumpbox template assumptions.
2. Generation 2—bootstrap-era customer repos with local `make bootstrap` / `make finish-bootstrap`, separate provider files, targeted applies. Mostly right.
3. Generation 3—data-driven pipeline: `customer.yaml` → Terraform → `infra_facts` → CUE → `values.yaml`. The correct target model. Partially implemented.

That's why the docs feel "true but not usable" and why new customer setup still requires 5–7 file changes across multiple languages. The remediation items below are surgical fixes that move the codebase from Gen 1/2 toward a clean Gen 3. The strategic phases in Part 8 describe the full journey.

#### The Two-Mode Model (Target Architecture)

Every customer deployment has two distinct phases, which must be kept separate in tooling and docs:

```md
Mode A — Bootstrap (one-time, local)
  Creates foundational control-plane resources only:
  - GitLab repo + deploy token
  - TFC project/workspace
  - Vault namespace + initial path structure
  make bootstrap → make finish-bootstrap

Mode B — Managed (ongoing, GitOps/TFC)
  Normal steady-state pipeline after bootstrap:
  - Terraform provisions AKS + central services
  - Terraform outputs infra_facts
  - CUE validates schema + renders values
  - ArgoCD/jumpbox bootstraps in-cluster apps
  - Changes via config/customer.yaml → PR → TFC plan → apply
```

Mixing these modes (e.g. running `-target` in steady-state, or manually editing `generated/values.yaml`) is the primary source of operational incidents and drift.

#### Data Ownership Rule (Architecture Law)

Each layer owns one thing. Violations of this rule are the root cause of most drift issues:

| Layer                           | Owns                                                                                                           | Must not own                                                      |
| ------------------------------- | -------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------- |
| `config/customer.yaml`          | Identity, network CIDRs, DNS, cluster sizing, feature enablement overrides, rare secret overrides              | Platform constants, duplicated app logic, Vault paths             |
| `platform-defaults/common.yaml` | Shared defaults: enabled apps, rollout rings, platform policy, Vault mount conventions, standard VSO consumers | Customer-specific data                                            |
| Terraform                   | Infra resources, central services integration, computed `infra_facts`                                          | Hand-maintained app value logic expressible in CUE                |
| CUE                         | Schema/contract for `infra_facts`, validation, mapping, rendering values, conditional logic                    | Customer-specific literals, platform defaults that belong in YAML |
| Helm                        | Chart structure and templating                                                                                 | Business rules better expressed in CUE/values                     |

---

### Part 1—Pipeline Audit: Current Status

#### What Is Already Fixed

These items from the original audit are confirmed resolved by reading the current code:

| Item | Fix Evidence |
|---|---|
| Grafana `if` guard—`vaultSecrets` conditional on `deploy.monitoring` | `render_fitfile.cue:87`—`if facts.deploy.monitoring {` |
| `mongodb_replica_count` promoted to `infra_facts`—CUE reads from facts | `schema_infra.cue:102`, `generators.tf:43`, `render_fitfile.cue:122` |
| `mock_infra.json` vault_secret_consumers populated—full consumer snapshot | `mock_infra.json:135–351` has all apps |
| `vault_secret_dispatch.cue` is live—10 call sites in `render_fitfile.cue` | `render_fitfile.cue:83,115,123,128,133,168,184,226,275,289` |
| `#InfraFacts.fitconnect_hosts` schema—properly typed with all four fields | `schema_infra.cue:44–49` |
| `fitConnectHosts` rendered conditionally—only when list is non-empty | `render_fitfile.cue:194–196` |

---

#### Open Pipeline Issues

##### 🔴 P-1—`generated/values.yaml` Is Stale (identity Mismatch + Phantom resources)

| Dimension | Detail |
|---|---|
| Problem | `generated/values.yaml:1` shows `namespace: mkuh-prd-4`; `config/customer.yaml:13` now says `name: "ffuh"`. ArgoCD reads this file—a push before regeneration deploys MKUH identifiers (wrong namespace, wrong Vault paths, wrong FQDN) for a different customer. |
| Second problem | `generated/values.yaml:5–28` contains two `kind: VaultAuth` CRs that CUE's `render_fitfile.cue` does not emit (comment at line 22–25 confirms ownership moved to jumpbox Terraform). Next ArgoCD sync after regeneration will delete these objects, breaking VSO until jumpbox Terraform is re-applied. |
| Third problem | `generated/values.yaml:65`: `messageBroker: true`—this flag is absent from `schema_infra.cue`'s deploy block. CUE's open struct silently passes it through. Next `make generate-values` will purge it; verify no Helm template guards on `.Values.deploy.messageBroker` remain. |
| Root cause (strategic) | `generated/` files are gitignored per architecture intent, but this file was committed from a previous customer. This is a data ownership violation—`generated/` belongs to the pipeline, not git. The `verify-generated` gate (P-1 fix) prevents this class of mistake. |
| Fix | Run `make generate-values` after `terraform apply` against the correct workspace. Do not push `generated/values.yaml` until regenerated. Add `make verify-generated` CI gate. |
| Files | `generated/values.yaml`, `config/customer.yaml`, `Makefile` |

Proposed `make verify-generated`:

```makefile
verify-generated:
	@EXPECTED=$$(grep '^name:' config/customer.yaml | awk '{print $$2}' | tr -d '"'); \
	ACTUAL=$$(grep '^deploymentKey:' generated/values.yaml | awk '{print $$2}'); \
	if echo "$$ACTUAL" | grep -q "$$EXPECTED"; then \
		echo "✅ deploymentKey matches customer ($$ACTUAL)"; \
	else \
		echo "❌ Stale generated/values.yaml: deploymentKey=$$ACTUAL but customer=$$EXPECTED. Run: make generate-values"; exit 1; \
	fi
```

---

##### 🟠 P-2—`locals.tf:244` `enable_grafana` Fallback is `false`, Platform Default is `true`

| Dimension | Detail |
|---|---|
| Problem | `enable_grafana = try(local.config.services.enable_grafana, false)`—`common.yaml` sets `services.enable_grafana: true`. After the three-tier merge, `local.config.services.enable_grafana` always resolves to the common value, making the `false` fallback unreachable in normal operation. It misleads readers into thinking Grafana defaults off. |
| Fix | Change fallback to `true` to match platform intent. |
| File | `locals.tf:244` |

```diff
-  enable_grafana   = try(local.config.services.enable_grafana, false)
+  enable_grafana   = try(local.config.services.enable_grafana, true)
```

---

##### 🟠 P-3—`PROCESS_AND_PLAN.md §2.2` Incorrectly Labels `vault_secret_consumers` as "dead schema"

| Dimension | Detail |
|---|---|
| Problem | `docs/PROCESS_AND_PLAN.md:40–47` says `vault_secret_consumers` is "dead schema / never consumed". This is false: `vault_secret_dispatch.cue:14` reads `infra.vault_secret_consumers[app]`; `render_fitfile.cue` calls `#vaultSecretsList` at 10 call sites. Engineers following this doc will leave the field empty or delete live pipeline code. |
| Root cause (strategic) | Documentation describing Gen 1/2 state coexists with Gen 3 code. This is the "true but not usable" problem from the SSoT review. |
| Fix | Replace §2.2 entirely (see patch in Part 4). |
| File | `docs/PROCESS_AND_PLAN.md` |

---

##### 🟡 P-4—`.gitignore` Typo: `generated/infa.json` alongside Correct `generated/infra.json`

```diff
-generated/infa.json
 generated/infra.json
```

---

##### 🟡 P-5—`#ThehyvePlatformPolicy.registry_host` Default Duplicates `platform_policy.platform.registry_url`

`policy_defaults.cue:61` declares `registry_host: string | *"fitfileregistry.azurecr.io"` which is never read—`render_thehyve.cue:17` already uses `policy.platform.registry_url`. Three independent copies of the same registry URL means a registry migration requires three separate changes.

```diff
# cue/policy_defaults.cue
 #ThehyvePlatformPolicy: {
-	registry_host:    string | *"fitfileregistry.azurecr.io"
 	image_tag:        string | *"0.4.5-test"
```

---

##### 🟡 P-6—`deploy.messageBroker` Not in `#InfraFacts` Schema

`generated/values.yaml:65` has `messageBroker: true` in the deploy block; `schema_infra.cue:15–34` has no `messageBroker` field. CUE's open struct silently passes unknown deploy flags through to Helm. Search `helm_chart_deployment/charts/ffnode` for `messageBroker`; if a template guards on it, add the field to schema; if not, the stale value disappears on next generation.

---

##### 🟢 P-7—`deploy.*` CUE Defaults Create a Second Source of Truth

`schema_infra.cue:16–34` declares deploy flags with CUE defaults (e.g. `certManager: bool | *true`). Real defaults live in `common.yaml standard_deployment` and flow through Terraform. If Terraform ever omits a flag, CUE silently fills its own default rather than surfacing the gap.

Fix (Tier C): Change `bool | *default` → `bool` for all deploy flags. This makes any omission a CUE parse error.

---

### Part 2—Network Topology Audit (`fitConnectHosts`)

#### The Root Cause Pattern

The `ECONNABORTED` incident on `nwsde-prod-1` was caused by a missing self-entry in `fitConnectHosts`. Without a self-entry, the pod selected the first available peer (`lca-prd-2` via the public internet) for its own `/tenants` lookup. That node returns `403 Forbidden` on internal-only endpoints. The timeout cascade produced `ECONNABORTED`.

This is an entire class of bug, not a one-off. Any deployment missing its self-entry silently hairpins through Cloudflare/ingress for data that lives in the same pod's namespace. The long-term fix (Tier B-2) makes this structurally impossible via Helm `_helpers.tpl` auto-injection—no self-entry in `values.yaml` means no self-entry can be wrong or missing.

---

#### Environment-by-Environment Status

##### `nwsde/nwsde-prod-1`—🔴 INCIDENT NODE

| Anti-Pattern | Status |
|---|---|
| Missing self-entry | ❌ CONFIRMED—no entry for `nwsde-prod-1` itself |
| `lca-prd-2` port verified | ❓ UNKNOWN—referenced as `https://lca-prd-2.fitfile.net` (port 443 implied); if it runs on `:11001` this silently times out |
| `allowedOrigin` | ✅ present |

Immediate fix:

```yaml
ffcloud:
  appConfig:
    fitConnectHosts:
    - fitConnectCode: "North West SDE"
      fitConnectUri: "http://nwsde-prod-1-fitconnect-ftc.nwsde-prod-1.svc.cluster.local/fitconnect"
      coordinatorUri: "http://nwsde-prod-1-ffcloud-service.nwsde-prod-1.svc.cluster.local/ffcloud"
      cryptoUri: ""
    - fitConnectCode: "lca-prd-2"
      fitConnectUri: "https://lca-prd-2.fitfile.net/fitconnect"   # TODO: verify port
      coordinatorUri: "https://lca-prd-2.fitfile.net/ffcloud"     # TODO: verify port
      cryptoUri: ""
    - fitConnectCode: "MCNFT PROD 1"
      fitConnectUri: "https://mcnft-prod-1.fitfile.net/fitconnect"
      coordinatorUri: "https://mcnft-prod-1.fitfile.net/ffcloud"
      cryptoUri: ""
```

---

##### `fitfile/ff-a`—🟠 Production Hub

| Anti-Pattern | Status |
|---|---|
| Missing self-entry | ✅ present |
| Self `fitConnectUri` uses public URL | ⚠️ routes through Cloudflare to reach itself |
| Self `coordinatorUri` short hostname | ⚠️ `http://ff-a-ffcloud-service/ffcloud`—no namespace qualifier |
| Missing `allowedOrigin` | ❌ CORS risk on production hub |
| Peers use public `coordinatorUri` | ⚠️ ff-b and ff-c route through public ingress |

---

##### `fitfile/ff-test-a`—🟡 Staging Hub

| Anti-Pattern | Status |
|---|---|
| Missing self-entry | ✅ present |
| Self uses public URL | ✅ `fitConnectUri` is internal |
| Self `coordinatorUri` short hostname | ⚠️ no namespace qualifier |
| Peers use public `coordinatorUri` | ⚠️ ff-test-b and ff-test-c coordinator calls go public |
| ff-test-c `fitConnectUri` has `https://` on svc hostname | ❌ BUG—in-cluster DNS has no TLS cert, must be `http://` |

---

##### `eoe/hie-prod-34`—🟠 EOE SDE Production Hub

| Anti-Pattern | Status |
|---|---|
| Missing self-entry | ✅ present |
| Self uses short hostname | ⚠️ no `.hie-prod-34.svc.cluster.local` suffix |
| Missing `allowedOrigin` | ❌ CORS risk on prod node |
| Asymmetric with `ff-a` | ⚠️ `hie-prod-34` lists `ff-a`; `ff-a` does not list `hie-prod-34`—unidirectional only |

---

##### `eoe/ff-eoe-sde`—🟠 EOE SDE Hub

| Anti-Pattern | Status |
|---|---|
| Missing self-entry | ✅ present |
| Missing `coordinatorUri` on ALL entries | ❌ every entry lacks `coordinatorUri`—coordinator-mediated queries will fail |
| Missing `allowedOrigin` | ❌ |

---

##### `eoe/hie-test-34`—🟡 EOE SDE Test

| Anti-Pattern | Status |
|---|---|
| Self-entry present (standalone) | ✅ |
| Short hostname | ⚠️ |
| Missing `allowedOrigin` | ❌ |

---

##### `kch/prod` & `kch/mn4`—🟡 KCH (old-style chart)

| Anti-Pattern | `kch/prod` | `kch/mn4` |
|---|---|---|
| Self-entry present | ✅ | ✅ |
| `coordinatorUri` missing | ❌ | ❌ |
| Bare service names (intentional—old schema) | ⚠️ | ⚠️ |
| `allowedOrigin` | ❌ MISSING | ✅ |

---

##### `stg/sandbox`—🟡 St George's (old-style chart)

| Anti-Pattern | Status |
|---|---|
| Self-entry present | ✅ |
| `coordinatorUri` missing | ❌ |
| Short hostname | ⚠️ |
| Missing `allowedOrigin` | ❌ |

---

##### `barts/prod`—🟠 Orphaned Node

No `fitConnectHosts` at all. No `coordinatingStation: true`. No entry in `ff-a`'s federation list. Determine: satellite of `ff-a` (set `coordinatingStation: true`) or standalone (add self-entry with internal FQDN).

---

#### Network Findings Summary

| Environment | Missing Self | Self Public URL | Short Hostname | Missing `allowedOrigin` | Missing `coordinatorUri` | Other |
|---|:---:|:---:|:---:|:---:|:---:|---|
| `nwsde-prod-1` | 🔴 | N/A | N/A | ✅ | N/A | lca-prd-2 port unverified |
| `ff-a` | ✅ | ⚠️ fitConnectUri | ⚠️ coordinator | 🔴 | ✅ | peers use public coordinator |
| `ff-test-a` | ✅ | ✅ | ⚠️ coordinator | ✅ | ✅ | ff-test-c has `https://` on svc URL |
| `hie-prod-34` | ✅ | ✅ | ⚠️ | 🔴 | ✅ | asymmetric with ff-a |
| `hie-test-34` | ✅ | ✅ | ⚠️ | 🔴 | ✅ |—|
| `ff-eoe-sde` | ✅ | ✅ | ⚠️ | 🔴 | 🔴 all entries |—|
| `kch/prod` | ✅ | ✅ | ⚠️ intentional | 🔴 | 🔴 | old chart schema |
| `kch/mn4` | ✅ | ✅ | ⚠️ | ✅ | 🔴 | old chart schema |
| `stg/sandbox` | ✅ | ✅ | ⚠️ | 🔴 | 🔴 | old chart schema |
| `barts/prod` | 🟠 no list | N/A | N/A | 🔴 | N/A | orphaned from federation |

---

### Part 3—Consolidated Remediation Plan

#### Tier A—Safe, Mechanical (single Commit, < 2h total)

| ID | Action | File(s) |
|---|---|---|
| A-1 | Fix `.gitignore` typo: remove `generated/infa.json` | `.gitignore` |
| A-2 | Fix `enable_grafana` fallback: `false` → `true` | `locals.tf:244` |
| A-3 | Update `PROCESS_AND_PLAN.md §2.2`: `vault_secret_consumers` is active (see Patch 2) | `docs/PROCESS_AND_PLAN.md` |
| A-4 | Update `PROCESS_AND_PLAN.md §2.5`: remove `workspace_vars.tf` / `providers.tf.bkp` stale rows | `docs/PROCESS_AND_PLAN.md` |
| A-5 | Fix `https://` TLS bug on `ff-test-c` peer in `ff-test-a` values | `ff-test-a` Helm values |
| A-6 | Add `allowedOrigin: ".*\\.fitfile.net"` to every node where missing | `ff-a`, `hie-prod-34`, `hie-test-34`, `ff-eoe-sde`, `stg/sandbox`, `kch/prod` |
| A-7 | Add `coordinatorUri` to all entries missing it | `ff-eoe-sde`, `kch/prod`, `kch/mn4`, `stg/sandbox` |
| A-8 | Delete `workspace_vars.tf`—97 lines of entirely commented-out TFC variable management; no active resources | `workspace_vars.tf` |
| A-9 | Delete `providers.tf.bkp`—stale backup of an old providers file; source of confusion during bootstrap | `providers.tf.bkp` |
| A-10 | Split `docs/CODE_REVIEW_AND_DATA_FLOW.md`—extract historical/completed items into a separate `docs/CHANGELOG.md` or archive; leave only current-state in the main file | `docs/CODE_REVIEW_AND_DATA_FLOW.md` |
| A-11 | Remove remaining commented-out dead code blocks (e.g. thehyve secrets block in `locals.tf:462–483`)—archive in commit message if needed | `locals.tf` |

> Before deleting A-8/A-9: run `terraform plan` on the customer workspace to confirm zero unintended changes. Expected: no plan diff (files contain only comments or dead backup content).

---

#### Tier B—Medium Risk, High Value

##### B-1—🔴 CRITICAL: Fix `nwsde-prod-1` Self-entry

Add the self-entry with internal FQDN as the first entry. Verify `lca-prd-2` port. Deploy immediately—this is the confirmed incident root cause. See the patch in Part 2.

##### B-2—Helm `_helpers.tpl` Auto-Loopback for `fitConnectHosts`

Once deployed, a missing-self entry is structurally impossible.

`charts/ffnode/templates/_helpers.tpl`:

```yaml
{{/*
Auto-inject the self (loopback) fitConnectHost entry.
values.yaml declares peers only — self is always computed from Release metadata.
*/}}
{{- define "ffnode.selfFitConnectEntry" -}}
- fitConnectCode: {{ .Values.global.fitConnectCode | quote }}
  fitConnectUri: "http://{{ .Release.Name }}-fitconnect-ftc.{{ .Release.Namespace }}.svc.cluster.local/fitconnect"
  coordinatorUri: "http://{{ .Release.Name }}-ffcloud-service.{{ .Release.Namespace }}.svc.cluster.local/ffcloud"
  cryptoUri: ""
{{- end }}
```

In the template that renders `fitConnectHosts`:

```yaml
fitConnectHosts:
{{- include "ffnode.selfFitConnectEntry" . | nindent 2 }}
{{- if .Values.ffcloud.appConfig.fitConnectHosts }}
{{- toYaml .Values.ffcloud.appConfig.fitConnectHosts | nindent 2 }}
{{- end }}
```

After this, remove self-entries from all `values.yaml` and `customer.yaml` files (peers only).

##### B-3—`values.schema.json` Validation for `fitConnectHosts`

Catches missing `coordinatorUri` at `helm lint` time:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema",
  "properties": {
    "ffcloud": {
      "properties": {
        "appConfig": {
          "properties": {
            "fitConnectHosts": {
              "type": "array",
              "items": {
                "required": ["fitConnectCode", "fitConnectUri", "coordinatorUri"],
                "properties": {
                  "fitConnectCode": {"type": "string", "minLength": 1},
                  "fitConnectUri":  {"type": "string", "minLength": 1},
                  "coordinatorUri": {"type": "string", "minLength": 1},
                  "cryptoUri":      {"type": "string"}
                },
                "additionalProperties": false
              }
            }
          }
        }
      }
    }
  }
}
```

##### B-4—`make verify-generated` CI Gate (see P-1)

Prevents pushing stale generated artifacts from a previous customer. Add to Makefile; run in CI before `git push`.

##### B-5—Remove `#ThehyvePlatformPolicy.registry_host` (see P-5)

Single-line removal; run `make validate-cue-mock` after.

##### B-6—Fix `ff-a` Production Hub Self-Entry

```yaml
# ff-a self-entry — after fix
- fitConnectCode: "FITConnect A"
  fitConnectUri: "http://ff-a-fitconnect-ftc.ff-a.svc.cluster.local/fitconnect"
  coordinatorUri: "http://ff-a-ffcloud-service.ff-a.svc.cluster.local/ffcloud"
  cryptoUri: ""
```

##### B-7—Qualify All Short Hostnames to Full FQDN

Short hostnames work only within the same namespace and fail silently on namespace change. Standard: `http://<release>-<svc>.<namespace>.svc.cluster.local`. Environments: `ff-a` coordinator, `ff-test-a` coordinator, `hie-prod-34`, `hie-test-34`, `ff-eoe-sde`.

##### B-8—Document Asymmetric Federation `hie-prod-34` ↔ `ff-a`

`hie-prod-34` lists `ff-a`; `ff-a` does not list `hie-prod-34`. Decide intentional vs oversight; document in `CONTRACTS.md` either way.

##### B-9—Bootstrap Mode Separation (from SSoT)

The `cloud {}` block comment/uncomment pattern is a recurring source of operator error (verified from `mkuh-prod-2` bootstrap incidents). Separate bootstrap provider config from steady-state:

- `providers_bootstrap.tf`—already exists in `generated/`; formalize this as the canonical bootstrap file
- Steady-state `providers.tf` is untouched during bootstrap
- `make bootstrap` explicitly uses `providers_bootstrap.tf` via `-chdir` or `TF_CLI_ARGS`
- Document this split in `README.md` and the migration playbook

##### B-10—Remove Script Recomputation of Terraform-Derived Values

`scripts/infra-facts-for-cue.sh` currently re-reads `customer.yaml` directly and overrides `cert_manager_extra_args`, `ffcloud_admin_user_id`, and `mongodb_connection_host`. This means `make generate-values` can produce output that diverges from what Terraform actually provisioned. The `mongodb_connection_host` calculation is duplicated between `locals.tf` and the script—two independent implementations of the same formula.

Audit tasks before changing:

- Catalogue every field `infra-facts-for-cue.sh` computes or overrides
- Cross-reference each against `locals.tf` and `generators.tf` to confirm the duplication
- Identify any field that genuinely cannot come from Terraform output (there should be none after `generators.tf` is complete)

Fix: Remove the `customer.yaml` overrides from `infra-facts-for-cue.sh`; trust `terraform output -json infra_facts` exclusively. If TF output is stale, surface it as a clear error (e.g. check `terraform show -json | jq '.values.outputs.infra_facts'` exits 0) rather than silently recomputing. After this change, `make generate-values` and `make validate-cue` are guaranteed to use the same data.

##### B-11—Data-Driven ArgoCD Apps (Eliminate `jumpbox.tftpl` Hardcoding)

`templates/jumpbox.tftpl` is a 474-line template with hardcoded ArgoCD Application blocks for every app (`ff-<key>`, `thehyve-<key>`, `relay-<key>`). Adding a new top-level app requires editing this template, which triggers a full regeneration of `generated/genjump.tf`. This is a Gen 1 pattern that directly contradicts the data-driven architecture.

Current state: `locals.tf:398–417` already assembles `argocd_applications` as a data-driven list (keyed off `deploy.*` flags) and passes it to the generators module. The list exists; the template just doesn't iterate over it cleanly.

Tasks:

- Define a canonical `argocd_application` object shape in `generators/variables.tf` (key, chart_path, values_file_path, destination_namespace)
- Refactor `templates/jumpbox.tftpl` to iterate over the `argocd_applications` list variable instead of hardcoded blocks
- Migrate all existing hardcoded apps to the data structure (ff, thehyve, relay)
- Validate with `terraform plan`—expect template content changes in `genjump.tf` but no infrastructure destruction
- After this: adding a new app is a `locals.tf` one-liner (or a `customer.yaml` entry via `argocd_applications` override) with no template edits

Definition of done: `jumpbox.tftpl` contains zero hardcoded app names. `terraform plan` renders all existing apps correctly.

---

#### Tier C—Architectural (Sprint-Scale)

| ID | Item |
|---|---|
| C-1 | Remove CUE defaults from `deploy.*` flags (`bool \| *default` → `bool`)—surfaces missing Terraform coverage as parse errors instead of silently applying wrong defaults |
| C-2 | Make `deploy.*` flags exhaustive in `schema_infra.cue`—add any missing (e.g. `messageBroker`) or explicitly document which are chart-only |
| C-3 | Add `make verify-generated` as a CI gate running before `git push` |
| C-4 | Document peer URL convention in `CONTRACTS.md` (see Part 7) |
| C-5 | Standardise chart-level `allowedOrigin` default in `charts/ffnode/values.yaml`—omitting it produces `".*\\.fitfile.net"` rather than blank |
| C-6 | `lca-prd-2` port audit—externally managed; verify listening port, update all references if non-443 |
| C-7 | Establish `barts/prod` federation membership—satellite of `ff-a` or standalone |

#### Tier D—Operational Foundations (from SSoT, Sprint-Scale)

These items address the "three generations" mixing problem and are prerequisites for making the system maintainable by a new engineer.

| ID | Item | Deliverable |
|---|---|---|
| D-1 | Freeze canonical onboarding path—declare the bootstrap workflow as the only official new-customer path; mark legacy Confluence steps as reference/deprecated | `README.md` update |
| D-2 | Complete "new customer" playbook §A—8 steps from scaffold to verify (partially in `MIGRATION_PLAYBOOK.md`); must be followable by a new engineer without assistance | `MIGRATION_PLAYBOOK.md` §A |
| D-3 | Write "upgrade existing customer" playbook §B—change platform defaults, regenerate, ring-promote, verify ArgoCD sync | `MIGRATION_PLAYBOOK.md` §B |
| D-4 | Define repo ownership map in `CONTRACTS.md`—one canonical table (see Part 7); mark legacy Confluence steps as reference/deprecated | `docs/CONTRACTS.md` |
| D-5 | Rewrite "add secret" process as a decision tree—platform-default vs customer-override paths; reference `vault_secret_consumers` as the mechanism; reduce to 1–2 file touches | `docs/PROCESS_AND_PLAN.md` or new runbook |
| D-6 | Rewrite "add app" process as a validated step-by-step checklist—cross-check against actual TF + CUE + jumpbox wiring; after B-11 this should be ≤3 file touches | `docs/PROCESS_AND_PLAN.md` or new runbook |
| D-7 | Document "rotate secret" end-to-end—Vault KV update → VSO refresh → rollout restart | New runbook section |
| D-8 | Create `create_customer.sh` scaffold script—inputs: deployment key, short name, full name, hub group, env, region, CIDR, DNS zone; outputs: populated `customer.yaml` + printed next steps | `scripts/create_customer.sh` |
| D-9 | Template/gold master customer repo—parameterised folder that `create_customer.sh` populates | New `customer_template/` directory |
| D-10 | Add `make preflight-check` target—validates tokens, TFC access, Vault reachability before bootstrap starts | `Makefile` |

---

### Part 4—Concrete Patches

#### Patch 1—Housekeeping (Tier A, Single commit)

`.gitignore`:

```diff
-generated/infa.json
 generated/infra.json
```

`locals.tf:244`:

```diff
-  enable_grafana   = try(local.config.services.enable_grafana, false)
+  enable_grafana   = try(local.config.services.enable_grafana, true)
```

---

#### Patch 2—`PROCESS_AND_PLAN.md` Corrections (Tier A, Single commit)

Replace §2.2 entirely:

```markdown
### 2.2 `vault_secret_consumers` is the active VSO dispatch mechanism

`vault_secret_consumers` is fully implemented and active — do not remove it.

- `common.yaml` defines per-app consumer lists (argoWorkflows, mongodb, minio, postgresql,
  fitconnect, ffcloud, frontend, certManager, grafana, spicedb, thehyve, workflowTemplates)
- `locals.tf` merges them (customer non-empty list replaces platform list per app)
- `generators.tf:41` passes the merged map in `infra_facts.vault_secret_consumers`
- `vault_secret_dispatch.cue:14` consumes `infra.vault_secret_consumers[app]` via `#vaultSecretsList`
- `render_fitfile.cue` calls `(#vaultSecretsList & {infra: facts, app: "..."}).out` at 10 call sites

To add or change a VSO secret: update `vault_secret_consumers` in `common.yaml` (platform-wide)
or `config/customer.yaml` (customer-specific override). Do not edit `render_fitfile.cue`.
```

§2.5: Remove rows for `workspace_vars.tf` and `providers.tf.bkp`—both resolved.

---

#### Patch 3—`nwsde-prod-1` Self-entry (Tier B-1, Deploy immediately)

Full patch shown in Part 2 environment section above.

---

#### Patch 4—`ff-a` Production Hub Fixes (Tier B-6 + A-6)

```yaml
ffcloud:
  appConfig:
    allowedOrigin: ".*\\.fitfile.net"
    fitConnectHosts:
    - fitConnectCode: "FITConnect A"
      fitConnectUri: "http://ff-a-fitconnect-ftc.ff-a.svc.cluster.local/fitconnect"
      coordinatorUri: "http://ff-a-ffcloud-service.ff-a.svc.cluster.local/ffcloud"
      cryptoUri: ""
    - fitConnectCode: "FITConnect B"
      fitConnectUri: "https://app2.fitfile.net/fitconnect"
      coordinatorUri: "https://app2.fitfile.net/ffcloud"
      cryptoUri: ""
    - fitConnectCode: "FITConnect C"
      fitConnectUri: "https://app3.fitfile.net/fitconnect"
      coordinatorUri: "https://app3.fitfile.net/ffcloud"
      cryptoUri: ""
```

---

#### Patch 5—`ff-test-a` Staging Hub Fixes (Tier A-5)

```diff
# ff-test-a peer entry for ff-test-c
-fitConnectUri: https://ff-test-c-fitconnect-ftc.ff-test-c.svc/fitconnect
+fitConnectUri: http://ff-test-c-fitconnect-ftc.ff-test-c.svc.cluster.local/fitconnect
```

---

#### Patch 6—`ff-eoe-sde` Missing coordinatorUri (Tier A-7 + A-6)

```yaml
ffcloud:
  appConfig:
    allowedOrigin: ".*\\.fitfile.net"
    fitConnectHosts:
    - fitConnectCode: "NHS SDE"
      fitConnectUri: "http://ff-eoe-sde-fitconnect-ftc.ff-eoe-sde.svc.cluster.local/fitconnect"
      coordinatorUri: "http://ff-eoe-sde-ffcloud-service.ff-eoe-sde.svc.cluster.local/ffcloud"
      cryptoUri: ""
    - fitConnectCode: "NHS Provider 1"
      fitConnectUri: "https://nhs-provider-1.fitfile.net/fitconnect"
      coordinatorUri: "https://nhs-provider-1.fitfile.net/ffcloud"
      cryptoUri: ""
    - fitConnectCode: "NHS Provider 2"
      fitConnectUri: "https://nhs-provider-2.fitfile.net/fitconnect"
      coordinatorUri: "https://nhs-provider-2.fitfile.net/ffcloud"
      cryptoUri: ""
```

---

#### Patch 7—Helm `_helpers.tpl` Auto-loopback (Tier B-2)

Full patch shown in Part 3 B-2. After deployment, remove all self-entries from `values.yaml` files and `customer.yaml`; keep only peer lists. Update `schema_infra.cue`'s `fitconnect_hosts` type comment to say "peers only".

---

#### Patch 8—`#ThehyvePlatformPolicy.registry_host` Removal (Tier B-5)

```diff
# cue/policy_defaults.cue
 #ThehyvePlatformPolicy: {
-	registry_host:    string | *"fitfileregistry.azurecr.io"
 	image_tag:        string | *"0.4.5-test"
```

---

### Part 5—Verification Checklist

#### Step 1—Schema + Mock

```bash
make validate-cue-mock
# Success: exits 0, no CUE type errors

# Verify grafana guarded on deploy.monitoring (confirmed in render_fitfile.cue:87)
cue export ./cue/values.cue ./cue/*.cue \
    -t "infra=$(cat cue/mock_infra.json)" \
    -e values --out yaml | grep "^grafana:" || echo "grafana absent (expected — mock has monitoring:true, should appear)"

# Verify replicaCount flows from mock
cue export ./cue/values.cue ./cue/*.cue \
    -t "infra=$(cat cue/mock_infra.json)" \
    -e values --out yaml | grep replicaCount
# Expected: replicaCount: 1 (matches mock "mongodb_replica_count": 1)

# After Patch 8 (registry_host removal): re-run validate-cue-mock
make validate-cue-mock
# Success: exits 0 — confirms no template read registry_host from #ThehyvePlatformPolicy
```

#### Step 2—Terraform Validate

```bash
terraform init && terraform validate
# Success: "The configuration is valid."
# After Patch 1 (enable_grafana): plan should show no unexpected changes
```

#### Step 3—Terraform Plan

```bash
terraform plan -out=plan.tfplan
# Success: no unexpected resource changes
# Verify: enable_grafana fallback change has no plan impact (value already true via merge)
```

#### Step 4—Full Pipeline Regeneration

```bash
make generate-values
git diff generated/values.yaml
# Success markers:
# - deploymentKey: ffuh-prd-1  (NOT mkuh-prd-4)
# - No messageBroker in deploy block
# - No VaultAuth CRs in extraDeploy
# - All vaultSecrets blocks populated (not [])
# - grafana: key present (deploy.monitoring: true for live env)
# - mongodb.replicaCount: 1

make verify-generated   # after adding to Makefile
# Success: "✅ deploymentKey matches customer (ffuh-prd-1)"
```

#### Step 5—CUE Vet against Real Output

```bash
INFRA_JSON=$(terraform output -json infra_facts | jq -c '.value // .')
cue vet -c ./cue/*.cue -t "infra=$INFRA_JSON"
# Success: exits 0, no output
# "field not allowed" → new TF field not in schema_infra.cue → update schema
# "missing required field" → generators.tf omits a required field → update generators
# "type mismatch" → TF type doesn't match CUE declaration → fix one side
```

#### Step 6—Helm Dry-run

```bash
cd helm_chart_deployment
helm template ffnode charts/ffnode \
    -f ../ff-test-1/generated/values.yaml \
    --namespace ffuh-prd-1 --dry-run 2>&1 | head -60
# Success: YAML output, no errors
# After B-2 (auto-loopback): fitConnectHosts in output must include self-entry with .svc.cluster.local URL
# "nil pointer" → a values key expected by template absent from generated/values.yaml
```

#### Step 7—Network Topology Fix Verification

```bash
# After deploying nwsde-prod-1 fix (Patch 3):
kubectl logs -n nwsde-prod-1 -l app=ffcloud-service --since=5m \
    | grep -i "tenant\|ECONNABORTED\|403"
# Success: no ECONNABORTED; /tenants resolves 200 from local service

# After auto-loopback (B-2):
helm template ffnode charts/ffnode -f <env>/values.yaml --namespace <env> \
    | grep -A5 "fitConnectHosts" | head -20
# Success: first entry is self with .svc.cluster.local URL
```

---

### Part 6—Execution Order

#### Immediate (this week—incident prevention)

| # | Item(s) | Risk | Notes |
|---|---|---|---|
| 1 | Patch 3—`nwsde-prod-1` self-entry | DEPLOY NOW | Active incident class |
| 2 | Patch 1 + A-8 + A-9 (housekeeping: gitignore, enable_grafana, delete dead files) | None | `terraform plan` first to confirm zero diff |
| 3 | Patch 2 + A-10 + A-11 (doc corrections + CODE_REVIEW split + dead code removal) | None | Single commit |

#### Sprint 1—Network Fixes + Contract Guards

| # | Item(s) | Risk | Notes |
|---|---|---|---|
| 4 | Patch 4—`ff-a` allowedOrigin + internal self URLs | Low | Production hub |
| 5 | Patch 5—`ff-test-a` `https://` bug | Low | Test env |
| 6 | Patch 6—`ff-eoe-sde` coordinatorUri | Low | Prevents federated query failure |
| 7 | A-6 + A-7—allowedOrigin + coordinatorUri on all remaining nodes | Low | Batch remaining env fixes |
| 8 | B-4—`make verify-generated` in Makefile | None | Guardrail before next push |
| 9 | Patch 8—`#ThehyvePlatformPolicy.registry_host` removal | Low | Run `validate-cue-mock` after |

#### Sprint 2—Structural Fixes (recommended Order: Phase 1 → Phase 4 → Phase 3 → Phase 2)

The phased improvement plan recommends this ordering for structural work because Phase 4 (data-driven jumpbox) unblocks Phase 3 (accurate "add app" docs) which in turn makes Phase 2 (dual truth removal) lower risk:

| # | Item(s) | Risk | Notes |
|---|---|---|---|
| 10 | B-2 + B-3—Auto-loopback `_helpers.tpl` + `values.schema.json` | Medium | Remove all self-entries from values files in same PR |
| 11 | B-11—Data-driven jumpbox apps (Phase 4) | Medium | Zero hardcoded app names in `jumpbox.tftpl`; validate with `terraform plan` |
| 12 | D-5 + D-6—"Add secret" and "add app" decision-tree runbooks (Phase 3) | None | Write after B-11 so app checklist reflects the simplified file-touch count |
| 13 | B-10—Remove script recomputation from `infra-facts-for-cue.sh` (Phase 2) | Medium | Audit field-by-field first; requires TF output to be current |
| 14 | B-9—Bootstrap mode separation (provider file formalization) | Low | Docs + Makefile only |
| 15 | D-2 + D-3—Complete migration playbook §A and §B | None | Documentation sprint |
| 16 | D-4 + D-7—Repo ownership map in CONTRACTS.md + "rotate secret" runbook | None |—|

#### Sprint 3—Architectural Hardening

| # | Item(s) | Risk | Notes |
|---|---|---|---|
| 17 | C-1—Remove CUE deploy flag defaults | Medium | All deploy flags must be present in TF output first |
| 18 | C-5—Chart-level `allowedOrigin` default in `ffnode/values.yaml` | Low |—|
| 19 | D-8 + D-9—Scaffold script + template repo | Medium | New tooling |
| 20 | D-10—`make preflight-check` target | Low |—|
| 21 | C-6 + C-7—`lca-prd-2` port audit + `barts/prod` federation decision | Low | Requires external coordination |

---

### Part 7—Repo & Data Ownership Map

This table is the definitive answer to "who owns what". Add to `docs/CONTRACTS.md`.

#### Repo Ownership

| Repo / Area | Owns | Must not own |
|---|---|---|
| Customer repo (`ff-test-1/` etc.) | Customer-specific data, orchestration entrypoint, generated artifacts | Platform constants, duplicated app logic |
| `platform-defaults` (common.yaml) | Shared defaults: rollout rings, platform policy, Vault conventions, standard VSO consumer catalog | Customer-specific overrides |
| `terraform-fitfile-central-services-consumer` | GitLab/TFC/Vault/Auth0/Grafana integration layer | Customer business config |
| Infra module repo(s) | AKS/VNet/private infra provisioning | App deployment values |
| CUE layer (`cue/`) | Contract + mapping from `infra_facts` + policy to Helm values | Customer literals duplicated from YAML |
| Helm chart repo | Chart structure and templates | Business rules better expressed in CUE |
| Legacy `central-services` | Reference / migration only | New-customer primary flow |

#### `fitConnectHosts` URL Convention

Add to `docs/CONTRACTS.md` under a dedicated section:

| Peer type | `fitConnectUri` | `coordinatorUri` |
|---|---|---|
| Self (same pod's namespace) | Do not set in `values.yaml`—managed by Helm `_helpers.tpl` auto-loopback after B-2 | Same |
| Same cluster, different namespace | `http://<release>-fitconnect-ftc.<namespace>.svc.cluster.local/fitconnect` | `http://<release>-ffcloud-service.<namespace>.svc.cluster.local/ffcloud` |
| Cross-cluster (external node) | `https://<env>.fitfile.net/fitconnect` | `https://<env>.fitfile.net/ffcloud` |
| Custom port (e.g. `lca-prd-2`) | `https://<env>.fitfile.net:<port>/fitconnect` | `https://<env>.fitfile.net:<port>/ffcloud` |
| Never | `http://` on a public hostname | `https://` on a `.svc` hostname (no TLS cert in-cluster) |

---

### Part 8—Strategic Phased Roadmap

The six phases below map directly to the phased improvement plan and encompass all Tier items from Part 3. Each has a clear "definition of done". They encompass all Tier items from Part 3. The recommended execution order within Phases B–E is: Phase B (dead code) → Phase D (data-driven apps) → Phase C (docs/recipes) → Phase E (dual-truth removal). This ordering is intentional: cleaning the codebase first makes Phase D lower-risk; completing Phase D makes the "add app" docs in Phase C accurate; accurate docs make Phase E (removing the shell script dual-path) lower-risk.

---

#### Phase A—Make it Operable Now (Tiers A + B-1 through B-4, This sprint)

Goal: Stop the immediate incident risk and eliminate the most dangerous drift.

1. Deploy `nwsde-prod-1` self-entry fix (Patch 3)—eliminates the active ECONNABORTED class
2. Run all Tier A housekeeping items in one commit (A-1 through A-11)
3. Fix all `allowedOrigin` and `coordinatorUri` gaps across environments (A-5 through A-7)
4. Add `make verify-generated` gate (B-4)
5. Auto-loopback `_helpers.tpl` + `values.schema.json` (B-2, B-3)

Definition of done: No environment has a missing self-entry or missing `coordinatorUri`. `make verify-generated` passes. `terraform plan` shows zero unintended changes after dead file removal.

---

#### Phase B—Clean Dead Code (Tier A-8 through A-11, Sprint 1)

Goal: Remove noise so the codebase reflects current reality. A developer reading the repo should see only live code.

1. Delete `workspace_vars.tf` and `providers.tf.bkp` (A-8, A-9)
2. Split `CODE_REVIEW_AND_DATA_FLOW.md`—history into archive, current state only in main file (A-10)
3. Remove commented-out dead code blocks (A-11)
4. Run `terraform plan` after each removal to confirm zero diff

Definition of done: `terraform plan` shows zero unintended changes. No `.bkp` files, no dead code blocks, no document that mixes completed history with current state.

---

#### Phase C—Write the Recipes (Tier D-2 through D-7, Sprint 2—after Phase D)

Goal: Replace ambiguous prose with actionable, deterministic runbooks. A developer unfamiliar with the repo can add an app or secret by following the documented checklist alone.

1. Rewrite "add secret" process as a decision tree—platform-default vs customer-override; reference `vault_secret_consumers` as the mechanism (D-5)
2. Rewrite "add app" checklist—cross-checked against actual TF + CUE + jumpbox wiring; after B-11 this is ≤3 file touches (D-6)
3. Document "rotate secret" end-to-end (D-7)
4. Complete migration playbook §A (new customer) and §B (upgrade) (D-2, D-3)
5. Repo ownership map in `CONTRACTS.md` (D-4)

Definition of done: A new engineer can add an app, add a secret, rotate a secret, or onboard a customer by following the docs alone without asking for help. The `thehyve` app either follows the standard CUE path or has an explicitly documented exception with justification.

---

#### Phase D—Data-Driven ArgoCD Apps (B-11, Sprint 2—before Phase C)

Goal: Adding a new app never requires editing a 474-line template.

1. Define canonical `argocd_application` object shape in `generators/variables.tf`
2. Refactor `jumpbox.tftpl` to iterate over the data-driven list from `locals.tf:398–417`
3. Migrate all hardcoded apps (ff, thehyve, relay) to the data structure
4. Validate with `terraform plan`; update "add app" checklist (Phase C) to reflect the simplified flow

Definition of done: `jumpbox.tftpl` contains zero hardcoded app names. Adding a new app is a `locals.tf` one-liner (or a `customer.yaml` entry). `terraform plan` renders all existing apps correctly.

---

#### Phase E—Eliminate the Dual Truth Path (B-10, Sprint 2—after Phase C)

Goal: Single source for infrastructure facts—Terraform only, no shell script duplication.

Note on Phase 5 from the phased plan: The `vault_secret_consumers` mechanism described in Phase 5 is already implemented (10 call sites in `render_fitfile.cue`; see "What Is Already Fixed" in Part 1). The remaining work in this phase is: (a) removing the shell script recomputation, and (b) ensuring the docs accurately describe the existing flow so engineers use `common.yaml` rather than editing `render_fitfile.cue` directly.

1. Audit `infra-facts-for-cue.sh` field-by-field against `locals.tf`/`generators.tf`
2. Remove `customer.yaml` overrides from the script; trust `terraform output -json infra_facts` exclusively
3. Update `PROCESS_AND_PLAN.md` to reflect the single data path
4. Run `make validate-cue` to confirm end-to-end correctness

Definition of done: No infrastructure fact is computed in both `locals.tf` and a shell script. CUE rendering sources all infra data from Terraform outputs. `make validate-cue` passes.

---

#### Phase F—Make it Elegant (Tier C + D-8/9/10, Future sprints)

Goal: "New customer = copy template, edit data, bootstrap." Adding a shared app or secret is a `platform-defaults` change only—no customer repo edits.

1. Scaffold script `create_customer.sh` (D-8)
2. Gold master template customer repo (D-9)
3. `make preflight-check` target (D-10)
4. Remove CUE deploy flag defaults → `bool` (C-1, requires all deploy flags in TF first)
5. Thin customer repo—shared logic in platform/module repos; customer repo is mostly data

Definition of done: A new customer can be scaffolded in under 10 minutes. A new shared app requires only `platform-defaults` + chart changes—zero customer repo edits.

---

### Part 9—Recommended Required Deliverables

These are the artefacts that will make this system clear for the next engineer. Status tracks what exists vs what is needed.

| # | Deliverable | Status | Owner |
|---|---|---|---|
| 1 | `README.md`—quick start, bootstrap vs managed mode, exact commands | Exists (needs bootstrap/managed separation highlighted) | D-1 |
| 2 | `docs/CONTRACTS.md`—TF → CUE → Helm interface, ownership, URL convention, merge semantics | Exists (needs URL convention + ownership table added) | D-4 |
| 3 | `docs/MIGRATION_PLAYBOOK.md`—onboard new customer §A + upgrade existing §B | Exists (§A partial; §B missing) | D-2/D-3 |
| 4 | `docs/PROCESS_AND_PLAN.md`—current reality, honest gaps, phased cleanup | Exists (§2.2 stale—fix in Patch 2; §2.5 stale—fix in A-4) | A-3/A-4 |
| 5 | "Add secret" decision tree runbook—platform-default vs customer-override paths | Missing | D-5 |
| 6 | "Add app" step-by-step checklist—validated against actual TF + CUE + jumpbox wiring | Missing (exists but unvalidated) | D-6 |
| 7 | "Rotate secret" end-to-end runbook | Missing | D-7 |
| 8 | `scripts/create_customer.sh`—scaffold new customer folder from inputs | Missing | D-8 |
| 9 | `Makefile`—`preflight-check`, `bootstrap`, `finish-bootstrap`, `validate-cue`, `generate-values`, `verify-generated` | Exists (missing `preflight-check` and `verify-generated`) | B-4/D-10 |

---

### Part 10—Success Criteria

Adapted from the phased improvement plan. These are the measurable outcomes that define "done" for the overall programme.

| Metric | Current State | Target State | Phase |
|---|---|---|---|
| Files touched to add a new app | 5–7 | 1–2 | Phase D + C |
| Files touched to add a new secret | 2–4 (mechanism exists; docs wrong) | 1–2 | Phase C + E |
| Files touched to add a new customer | ~10 (manual) | 1 YAML + 3 commands | Phase F |
| Dead code / stale files in repo | Multiple (`workspace_vars.tf`, `.bkp`, dead code blocks) | Zero | Phase B |
| Duplicate truth paths | Shell script + Terraform | Terraform only | Phase E |
| Hardcoded apps in `jumpbox.tftpl` | All (ff, thehyve, relay) | Zero (data-driven) | Phase D |
| Process documentation | Mixed/stale (§2.2 wrong, §2.5 wrong, CODE_REVIEW conflated) | Decision-tree runbooks, current-state only | Phases B + C |
| Environments with missing `allowedOrigin` | 6 | 0 | Phase A |
| Environments with missing self-entry | 1 (nwsde-prod-1) | 0 | Phase A—IMMEDIATE |
| Bootstrap mode separated from steady-state | No (`cloud {}` manual toggle) | Yes (explicit provider files, separate targets) | Phase A/E |
| `make generate-values` determinism | Non-deterministic (script overrides TF output) | Fully deterministic (TF output only) | Phase E |
| `cue vet` catches contract violations | Partially (open struct silently passes unknown fields) | Fully (required `bool` deploy flags) | Phase F |

### Terraform State as Source of Truth

Date: 2026-04-09

Context: Strategic analysis of which Terraform-managed resources currently flow into CUE/Helm, which don't, and what the target architecture looks like.

---

#### The Idea

`customer.yaml` helps create resources via Terraform. Terraform Cloud holds authoritative state for every provisioned resource. That state—not a re-read of `customer.yaml`, not a shell script formula—should be the single input to CUE, which then renders Helm values.

The current system is 90% there. The gaps are specific and fixable.

---

#### What Terraform Actually Manages

##### Bucket 1—Infrastructure (`module.private-infrastructure`)

| Resource | TF creates | Where the value goes today |
|---|---|---|
| AKS cluster | Host, CA cert, client cert/key | → `main.tf` → `central_services` (provider auth). Not in `infra_facts` |
| OIDC issuer URL | `data.azurerm_kubernetes_cluster.oidc_issuer_url` | → `generators.tf` → jumpbox template (VaultAuth JWT). Not in `infra_facts` |
| Private DNS zone | `azurerm_private_dns_zone` | DNS resource only—FQDN is _derived_ from `customer.yaml`, not read back from Azure |
| Ingress A record | `azurerm_private_dns_a_record.ingress` | → `generators.tf` → jumpbox template. Not in `infra_facts` |
| VNet / subnets / NAT / Bastion | Various Azure resources | Internal to infra module. Not surfaced anywhere downstream |

##### Bucket 2—Central Services (`module.central_services`)

| Resource | TF creates | Where the value goes today |
|---|---|---|
| Auth0 application | `client_id`, `client_secret`, `api_identifier` | → Vault KV (`application.pool_keys.auth0.*`) → VSO → K8s secret. `auth0_client_id` is a root output but not in `infra_facts` |
| GitLab project | Project URL, SSH URL, deploy token | `values_repo_url` → `infra_facts.values_repo_url` ✅. SSH/HTTPS URLs are root outputs but not in `infra_facts` |
| Vault namespace + mounts | JWT auth mount path, KV paths | Used internally by jumpbox. Not in `infra_facts` |
| TFC workspace | Workspace ID/URL | Used internally. Not surfaced |
| Grafana resources | Stack details | Used internally. Not surfaced |
| Auth0 M2M client credentials | Via `vault_secrets.application.pool_keys` | → Vault → VSO → `auth.json` template → app secrets. Correctly bypasses `infra_facts` |

##### Bucket 3—What `infra_facts` Actually Contains

Of everything Terraform produces, `infra_facts` is assembled almost entirely from derived config (`locals.tf` expressions over `customer.yaml` + `common.yaml`), not from live resource attributes:

| `infra_facts` field | Source | Live resource? |
|---|---|:---:|
| `deployment_key`, `public_fqdn`, `argocd_fqdn` | Derived from `customer.yaml` name/env/id/dns | ❌ |
| `values_repo_url` | `module.central_services.values_repo_url` | ✅ |
| `fit_connect_code` | `= local.deployment_key` (customer.yaml derived) | ❌ |
| `deploy.*` flags | `common.yaml` standard_deployment + customer.yaml overrides | ❌ |
| `platform_policy`, `platform_vault` | `common.yaml` (static config, not live resources) | ❌ |
| `node_placement`, `s3_export`, `pki_issuer` | `customer.yaml` / `common.yaml` | ❌ |
| `mongodb_connection_host` | Formula computed from `deployment_key` + chart version hash | ❌ |
| `vault_secret_consumers` | `common.yaml` catalog | ❌ |

`values_repo_url` is the only field in `infra_facts` sourced from a live provisioned resource. Every other field is derived from config at plan time.

---

#### The Two Gaps

##### Gap A—TF Computes Values that Bypass `infra_facts` Entirely

These values exist in TF state after every apply but never reach CUE:

| Value | Currently reaches | Consequence of absence from `infra_facts` |
|---|---|---|
| `oidc_issuer_url` | Jumpbox template only | CUE/Helm can't use the actual cluster OIDC URL for VaultAuth or workload identity config |
| `ingress_ip` | Jumpbox template only | Helm re-derives from CIDR formula; actual provisioned IP not confirmed |
| `auth0_client_id` / `auth0_api_identifier` | Root outputs + Vault KV | Available but CUE can't use them for non-VSO config (display labels, ArgoCD annotations) |
| `gitlab_project_url` / `gitlab_project_ssh_url` | Root outputs only | Not available to CUE for anything that references the project |

Note: Auth0 credentials intentionally stay out of `infra_facts`—they are sensitive and already flow correctly via Vault → VSO → K8s secrets. That path is correct for credentials. What belongs in `infra_facts` is structural output: URLs, IPs, identifiers used for non-secret configuration.

##### Gap B—The Shell Script Re-derives what TF State Already Knows

`scripts/infra-facts-for-cue.sh` re-reads `customer.yaml` directly and overrides three fields that are already computed by Terraform and present in `terraform output -json infra_facts`:

| Field overridden by script | Already in `infra_facts` via | Why this is wrong |
|---|---|---|
| `cert_manager_extra_args` | `generators.tf:35` | Overrides TF output with a re-read of customer.yaml |
| `ffcloud_admin_user_id` | `generators.tf:29` | Same |
| `mongodb_connection_host` | `generators.tf:43` | Duplicates the formula already in `locals.tf:495–511` |

The script was written to solve stale-state ("TF output may lag"). The correct solution is to surface staleness as an error, not bypass TF state entirely. This is the dual truth path (B-10 in the remediation plan).

---

#### What `customer.yaml` Should Actually Contain

After this vision is fully realised, `customer.yaml` contains only genuine human decisions—things that cannot be computed from anything Terraform provisions:

```yaml
# Identity — what a human assigns; not derivable
name: "ffuh"
full_name: "FITFILE University Hospital"
env: "live"
region: "uks"
id: 1
hub_group: "fitfile"

# Physical network — must be a human decision; cannot be computed post-hoc
network:
  vnet_address_space: "10.104.189.128/26"

# Feature choices — intentional overrides of platform defaults
standard_deployment:
  live:
    thehyve: true

# Cluster sizing — hardware choices
cluster:
  node_pools:
    workflows:
      vm_size: "Standard_D2s_v5"
      min_count: 0
      max_count: 3
```

Everything else derives automatically:

| Value | Derived by |
|---|---|
| `deployment_key` | `${name}-${env_prefix}-${id}` in `locals.tf` |
| `public_fqdn` | `${deployment_key}.${dns.zone}` |
| `argocd_fqdn` | `argocd.${public_fqdn}` |
| `auth0_config` (callbacks, origins) | Computed from `public_fqdn` in `locals.tf` |
| `values_repo_url` | `module.central_services.values_repo_url` (live resource) |
| `ingress_ip` | `cidrhost(system_subnet, 10)` or actual Azure LB IP |
| `oidc_issuer_url` | `data.azurerm_kubernetes_cluster.oidc_issuer_url` (live resource) |
| Auth0 credentials | Vault → VSO (never in `infra_facts`) |
| Platform policy, vault paths, VSO consumers | `common.yaml` via platform-defaults module |

---

#### The Fix: Expand `infra_facts` with Live Resource Outputs

The two live resource values that are already passed to the generators module but not included in `infra_facts` should be added. Both are in `generators/variables.tf` already—they just don't flow through.

`generators.tf`—add to the `infra_facts` map:

```hcl
infra_facts = {
  # ... all existing fields ...

  # Live resource outputs — already passed to generators module, not yet in infra_facts
  oidc_issuer_url = var.oidc_issuer_url   # data.azurerm_kubernetes_cluster.this.oidc_issuer_url
  ingress_ip      = var.ingress_ip        # cidrhost(subnets.system, 10) or actual Azure IP
}
```

`cue/schema_infra.cue`—add to `#InfraFacts`:

```cue
oidc_issuer_url: string | *""
ingress_ip:      string | *""
```

`cue/mock_infra.json`—add representative values:

```json
"oidc_issuer_url": "https://oidc.prod.aks.azure.com/00000000-0000-0000-0000-000000000000/",
"ingress_ip": "10.104.189.138"
```

---

#### The Fix: Remove Shell Script Re-derivation (B-10)

```diff
# scripts/infra-facts-for-cue.sh
-# Override cert_manager_extra_args from customer.yaml
-CERT_MANAGER_ARGS=$(yq '.cert_manager_extra_args // []' config/customer.yaml)
-INFRA_JSON=$(echo "$INFRA_JSON" | jq --argjson v "$CERT_MANAGER_ARGS" '.cert_manager_extra_args = $v')
-
-# Override ffcloud_admin_user_id from customer.yaml
-ADMIN_USER=$(yq '.ffcloud_admin_user_id // ""' config/customer.yaml)
-INFRA_JSON=$(echo "$INFRA_JSON" | jq --arg v "$ADMIN_USER" '.ffcloud_admin_user_id = $v')
-
-# Recompute mongodb_connection_host
-...formula...
+# Trust terraform output entirely. If output is stale, fail explicitly.
 terraform output -json infra_facts | jq -c '.value // .'
```

After this change, `make generate-values` is deterministic: the same TF state always produces the same `values.yaml`.

---

#### Flow After Both Fixes

```
customer.yaml
  (minimal: name, CIDR, env, feature flags)
      ↓
Terraform apply
  module.private-infrastructure  → AKS, VNet, DNS, ingress IP
  module.central_services        → Auth0, GitLab, Vault, TFC
  locals.tf                      → derived names, FQDNs, policy merges
      ↓
terraform output -json infra_facts
  (authoritative: all computed + provisioned values in one JSON blob)
      ↓  no script overrides
CUE (#InfraFacts validation + #RenderValues rendering)
      ↓
generated/values.yaml  →  ArgoCD  →  Helm  →  AKS
```

Auth0 credentials flow on a separate, correct path:

```
Terraform → central_services → Vault KV
                                    ↓
                               VSO VaultStaticSecret
                                    ↓
                               K8s Secret → app reads auth.json
```

This path is correct and should not change. Credentials are not in `infra_facts` by design.

---

#### Summary

| Question | Answer |
|---|---|
| Is the idea sound? | Yes—TF state is already the right boundary; the plumbing is mostly there |
| How many live resource outputs reach `infra_facts` today? | One (`values_repo_url`) |
| What's stranded in TF state but not reaching CUE? | `oidc_issuer_url`, `ingress_ip`, `gitlab_project_url` |
| Should Auth0 credentials be in `infra_facts`? | No—they're sensitive and flow correctly via Vault → VSO |
| What's the primary anti-pattern to fix? | Shell script re-reading `customer.yaml` to override what TF already computed |
| What should `customer.yaml` contain? | Only genuine human decisions: name, CIDR, env, feature flag overrides |
| What makes `make generate-values` non-deterministic today? | The shell script overrides TF output with locally re-derived values |

I hear you—the big idea is clean and powerful:

> `customer.yaml` → Terraform → TFC State → Interrogate State → Populate Downstream Config (CUE → Helm)

Instead of recomputing infrastructure facts in shell scripts or duplicating values, you let Terraform Cloud be the single authority for all resource-derived configuration. Let me map out the Terraform-managed resources I can identify across your module ecosystem.

---

#### Terraform Module Inventory (TFC Registry)

From your [GitKraken workspace](https://gitkraken.com) views and TFC registry, here are the modules under `FITFILE-Platforms` that create stateful resources:

##### 1. Auth0 Resources

| Module | What It Creates | Key State Outputs |
|--------|----------------|-------------------|
| `terraform-auth0-tenant` | Auth0 tenant configuration | Tenant domain, issuer URL |
| `terraform-fitfile-auth0-consumer` | Auth0 applications/clients per customer | Client IDs, client secrets, API audience URIs, callback URLs, connections |

This is your prime example—Auth0 config created here gets passed downstream into both infrastructure (Vault secrets for apps to consume) and Helm (values for app configuration). The TFC state already holds the client IDs, secrets, and domains.

##### 2. Azure Private Infrastructure

| Module | What It Creates | Key State Outputs |
|--------|----------------|-------------------|
| `terraform-azure-private-infrastructure` | AKS cluster, VNet/subnets, load balancer, jumpbox VM, NSGs | `aks_cluster_outbound_ip_address`, cluster endpoint, subnet IDs, resource group name, jumpbox IP, kubeconfig data |

From the [Confluence Node Installation](https://fitfile.atlassian.net/wiki/spaces/FITFILE/pages/1861779457/Node+Installation+-+Infrastructure?atl_f=PAGETREE) page, we can see the output is already partially defined:

```terraform
output "aks_cluster_outbound_ip_address" {
  value = module.private-infrastructure.load_balancer_outbound_ip
}
```

##### 3. Platform Helm Components

| Module | What It Creates | Key State Outputs |
|--------|----------------|-------------------|
| `terraform-helm-fitfile-platform` | Helm releases: ArgoCD, ingress-nginx, cluster-autoscaler, reflector, vault-operator | Ingress controller IP, ArgoCD server URL, release metadata |

From the `terraform init` output (~February 10), the sub-modules are:

- `platform.argocd`
- `platform.cluster_autoscaler`
- `platform.ingress_controller` (ingress_nginx)
- `platform.reflector`
- `platform.vault_operator`

##### 4. ArgoCD & Deployment

| Module | What It Creates | Key State Outputs |
|--------|----------------|-------------------|
| `terraform-argo-argocd` | ArgoCD projects, applications, repository credentials | App names, project names, sync status |
| `terraform-fitfile-unified-deployment` | Orchestrates full customer deployment | Aggregated outputs from sub-modules |

##### 5. Central Services & Supporting

| Module | What It Creates | Key State Outputs |
|--------|----------------|-------------------|
| `terraform-fitfile-central-services-connector` | Connections to shared/central services | Service endpoints, connection strings |
| `terraform-azure-aks-backup` | AKS backup configuration | Backup vault ID, policy details |
| `terraform-azure-aks-automation` | AKS automation runbooks | Automation account details |
| `vault` (module) | Vault policies, auth methods, secret engines | Mount paths, policy names, auth method accessors |

##### 6. Defaults & Versioning

| Module | What It Creates | Key State Outputs |
|--------|----------------|-------------------|
| `terraform-fitfile-platform-defaults` | Platform-wide default values (v1.0.0) | Default config values keyed to `customer.yaml` structure |
| `fitfile-version-manager` | Version pinning/management | Current version pins |

The `platform-defaults` module is especially relevant—from the [TFC Registry](https://vault-public-vault-8b38a0c2.e3dedc53.z1.hashicorp.cloud:8200/ui/vault/secrets/secrets/kv/argocd/details?namespace=admin%2Fdeployments%2Flca-prd-2&version=32) (~March 2), it's described as:

> _"Platform-wide default configuration values, keyed identically to customer.yaml structure."_

This is already designed to be the defaults layer that `customer.yaml` overrides.

---

#### The Data Flow You're Describing

```
┌──────────────┐
│ customer.yaml│  (customer-specific overrides)
└──────┬───────┘
       │
       ▼
┌──────────────────────────────────────────────────┐
│              Terraform Modules                    │
│                                                   │
│  Auth0 Tenant ──► Auth0 Consumer                 │
│  Azure Private Infra ──► Platform Helm           │
│  Central Services Connector                       │
│  ArgoCD ──► Unified Deployment                   │
│  Vault config                                     │
└──────────────────┬───────────────────────────────┘
                   │
                   ▼
          ┌────────────────┐
          │   TFC State    │  (single source of truth for ALL computed values)
          │   per workspace│
          └────────┬───────┘
                   │
                   │  terraform output -json / TFC API / tfe_outputs data source
                   ▼
          ┌────────────────┐
          │  CUE Rendering │  (merges defaults + customer.yaml + TFC state)
          └────────┬───────┘
                   │
                   ▼
          ┌────────────────┐
          │  values.yaml   │  → Helm / ArgoCD
          └────────────────┘
```

---

#### Key Terraform State Interrogation Points

The resources that generate the most downstream configuration are:

##### Auth0 (highest value—your Cited example)

```
TFC State holds:
  → auth0_client.*.client_id        → feeds into Helm values + Vault secrets
  → auth0_client.*.client_secret    → feeds into Vault secret store
  → auth0_tenant.*.domain           → feeds into app config (issuer URLs)
  → auth0_resource_server.*.identifier → feeds into API audience config
```

##### Infrastructure

```
TFC State holds:
  → azurerm_kubernetes_cluster.*.kube_config        → cluster access
  → azurerm_public_ip.*.ip_address                  → ingress/outbound IPs
  → azurerm_subnet.*.id                             → network config
  → azurerm_resource_group.*.name                   → resource scoping
```

##### Platform

```
TFC State holds:
  → helm_release.ingress_nginx.* → ingress controller IP
  → helm_release.argocd.*        → ArgoCD endpoint
  → kubernetes_namespace.*       → namespace inventory
```

---

#### What This Eliminates

This is exactly the Phase 2 from the plan we built, but you're rightly saying it's actually the foundational architectural principle, not just a cleanup phase:

| Current Problem | How TFC State Solves It |
|----------------|------------------------|
| `infra-facts-for-cue.sh` recomputes infra values | Replaced by `terraform output -json` from TFC |
| `locals.tf` and shell script both derive same values | Single derivation in Terraform, consumed from state |
| Auth0 client IDs manually wired into multiple places | Pulled once from TFC state, flowed through CUE |
| Jumpbox template hardcodes app names | App list driven from `customer.yaml`, endpoints from state |
| Adding a secret requires 5-7 file touches | `customer.yaml` declares intent, TFC state provides computed values |

---

#### Implementation Mechanism

For cross-workspace state consumption, you have a few options in TFC:

1. `tfe_outputs` data source—one workspace reads another workspace's outputs directly
2. `terraform_remote_state`—similar but older pattern
3. TFC API (`/api/v2/workspaces/:id/current-state-version`)—for external consumers (scripts, CI/CD)
4. Run triggers—downstream workspaces auto-run when upstream state changes

Given your architecture, the most natural pattern is probably `tfe_outputs` for Terraform-to-Terraform chaining (Auth0 → Infrastructure → Platform), and the TFC API for CUE rendering (external to Terraform).

---

Want me to map the specific output contracts each module would need to expose to make this state-interrogation pattern work end-to-end? That would essentially define the "API surface" of each TFC workspace that downstream consumers depend on.
