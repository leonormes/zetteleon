---
captured: "2026-03-07T16:51:32+00:00 2026-03-07T16:51:32+00:00"
created: 2026-03-07T16:51:34+00:00
modified: 2026-03-14T11:10:34+00:00
source: "https://claude.ai/chat/6c20e52e-238d-4623-8c67-3bc23d7aaeb0"
status: "processing"
tags: ["input"]
title: HEAD Terraform failure and vault CLI debugging
type: "head"
---

## Raw Output / Content

why is terraform failing? Give me a set up vault cli commands to investigate

---

Let me read the log first.

---

\# 1. Set your env (adjust if different) export VAULT\_ADDR=" [https://vault-public-vault-8b38a0c2.e3dedc53.z1.hashicorp.cloud:8200](https://vault-public-vault-8b38a0c2.e3dedc53.z1.hashicorp.cloud:8200/) " export VAULT\_NAMESPACE="admin" # 2. List top-level child namespaces under admin # You expect to see "deployments/" here vault namespace list # 3. Check what's inside admin/deployments export VAULT\_NAMESPACE="admin/deployments" vault namespace list # 4. Confirm mkuh-prd-4 does NOT exist (it was destroyed and recreation failed) # This should return an error or empty vault namespace lookup mkuh-prd-4 # 5. Check if the DOUBLED path exists (it shouldn't, but let's rule it out) export VAULT\_NAMESPACE="admin/deployments/deployments" vault namespace list # Expect: error / "no namespace"—confirming the double-prefix is bogus # 6. Reset to the correct parent and check auth mounts export VAULT\_NAMESPACE="admin/deployments" vault auth list # Look for jwt-mkuh-prd-4/—it should be gone since the namespace was deleted # 7. Check what the provider SHOULD be targeting # List secrets engines to confirm the parent namespace is healthy vault secrets list Keys ---- central/ deployments/ fitfile/ Keys ---- acr-test/ barts/ cuh-prod-1/ ff-eoe-sde/ ff-hyve-1/ ff-hyve-2/ ff-wmsde-1/ gh-pt-1/ hie-prod-34/ hie-test-34/ lca-prd-2/ mcnft-prod-1/ nnuh-prod-1/ nwsde-prod-1/ pentest/ prod-1/ pv-aks-1/ sandbox-testing-1/ staging/ testing/ ucl-test-1/ wm-dev-1/ Namespace not found No namespaces found Path Type Accessor Description Version ---- ---- -------- ----------- ------- token/ ns\_token auth\_ns\_token\_f9f9b99d token based credentials n/a Path Type Accessor Description ---- ---- -------- ----------- cubbyhole/ ns\_cubbyhole ns\_cubbyhole\_f6e4b14a per-token private secret storage identity/ ns\_identity ns\_identity\_e8149c43 identity store sys/ ns\_system ns\_system\_f34e3377 system endpoints used for control, policy and debugging

---

This is very revealing. Key findings:

## What the Output Tells Us

1. `mkuh-prd-4` is gone. The destroy succeeded (line 47 of the log) but recreation failed, so you're now in a state where the namespace has been deleted and not replaced. All the secrets, auth backends, and KV mounts that lived inside it are gone too.
2. `admin/deployments/deployments` EXISTS. This is critical—command 5 returned `"No namespaces found"` instead of an error. That means this rogue doubled namespace is a real, empty namespace sitting in Vault. It was probably created by a previous botched run with the same double-prefix bug.
3. `admin/deployments` parent is healthy. The long list of customer namespaces confirms the correct path is fine. `mkuh-prd-4` just needs to be recreated under it.

## Next Investigation Steps

## Then: Find the Terraform Double-prefix

You're looking for something like `namespace = "admin/deployments"` being set at the workspace/variable level, and then the `central_services` module appending `/deployments` again. One of those two needs removing—the fix depends on whether the duplication is in `tfvars` or in the module's provider block.

Immediate action: Run commands 1–2 above to confirm the rogue namespace is empty, then delete it with command 3. After that, the Terraform fix is the real blocker.

---

export VAULT\_NAMESPACE="admin/deployments" vault namespace lookup deployments Namespace not found …/mkuh-prod-4 on  main on ⛵ fitfile-cloud-staging-aks-cluster () on ☁ subcr-sde-prd on 🅰 (eu-west-2) at 13:21:22 ❯ …/mkuh-prod-4 on  main on ⛵ fitfile-cloud-staging-aks-cluster () on ☁ subcr-sde-prd on 🅰 (eu-west-2) at 13:21:22 ❯ export VAULT\_NAMESPACE="admin/deployments/deployments" vault auth list vault secrets list Error listing enabled authentications: Error making API request. Namespace: admin/deployments/deployments/ URL: GET [https://vault-public-vault-8b38a0c2.e3dedc53.z1.hashicorp.cloud:8200/v1/sys/auth](https://vault-public-vault-8b38a0c2.e3dedc53.z1.hashicorp.cloud:8200/v1/sys/auth) Code: 404. Errors: \* no handler for route "deployments/sys/auth". route entry not found. Error listing secrets engines: Error making API request. Namespace: admin/deployments/deployments/ URL: GET [https://vault-public-vault-8b38a0c2.e3dedc53.z1.hashicorp.cloud:8200/v1/sys/mounts](https://vault-public-vault-8b38a0c2.e3dedc53.z1.hashicorp.cloud:8200/v1/sys/mounts) Code: 404. Errors: \* no handler for route "deployments/sys/mounts". route entry not found. …/mkuh-prod-4 on  main on ⛵ fitfile-cloud-staging-aks-cluster () on ☁ subcr-sde-prd on 🅰 (eu-west-2) at 13:21:33 ❯ vault namespace list | grep deployments No namespaces found

---

Good news—the rogue namespace doesn't actually exist. The `404` on auth/secrets list and `Namespace not found` on lookup both confirm that. The earlier "No namespaces found" from command 5 was just the CLI's way of saying "I can't find anything here"—misleading wording, but it's a clean `404`, not an empty namespace.

So the picture is simple:

- `admin/deployments/deployments`—doesn't exist, never did. It's purely a bogus path being constructed by the Terraform provider config.
- `admin/deployments/mkuh-prd-4`—was destroyed by the replace operation and never recreated because the create targeted the wrong (doubled) namespace.

The entire problem is in Terraform. Nothing to clean up in Vault itself.

## Find the Double-prefix Source

You're looking for two things that each add `deployments`:

- Source A: The root provider or workspace variable sets `namespace = "admin/deployments"`
- Source B: The `central_services` module appends `/deployments` again (e.g. `namespace = "${var.vault_namespace}/deployments"`)

One of those needs to change. Paste whatever the greps return and I'll pinpoint the exact line.

---

Found it. Two separate namespace construction patterns that conflict:

## The Double-prefix Source

| Location | What it does | Resulting namespace |
| --- | --- | --- |
| `main.tf:3` | Provider `vault.deployments` sets `namespace = "admin/deployments"` | `admin/deployments` |
| `central_services` module (internal) | Module receives that provider, then internally prepends `deployments/` when creating the namespace resource | `admin/deployments/deployments` ← boom |

Meanwhile, your root-level `vault_k8s_auth.tf` does it correctly—it uses the default Vault provider (presumably `namespace = "admin"`) and manually builds the full relative path: `namespace = "deployments/${local.deployment_key}"`.

## Confirm the Theory

You're looking for something like `namespace = "deployments"` or `namespace = "deployments/${var.deployment_key}"` on the `vault_namespace.customer_ns` resource inside the module. That's the second `deployments` segment.

## The Fix (once confirmed)

Option A—Change the root provider (most likely correct):

This aligns `vault.deployments` with the module's expectation that it will handle the `deployments/` prefix internally. Your `vault_k8s_auth.tf` resources already work this way against the default provider.

Option B—If the module does NOT add `deployments/` internally, then the module has a bug and needs patching at source.

Immediate next action: Run that `grep` against `.terraform/modules/central_services/` and paste the output. That tells us definitively whether Option A is the fix, or whether the module itself needs a version bump.

---

grep -rn 'namespace'.terraform/modules/central\_services/ --include="\*.tf".terraform/modules/central\_services/outputs.tf:25:output "vault\_namespace\_path" {.terraform/modules/central\_services/outputs.tf:26: value = var.enable\_vault? vault\_namespace.customer\_ns\[0\].path\_fq: null.terraform/modules/central\_services/main.tf:7: namespace\_id = data.gitlab\_group.hub\[0\].id.terraform/modules/central\_services/main.tf:43: identifier = gitlab\_project.customer\_repo\[0\].path\_with\_namespace.terraform/modules/central\_services/main.tf:137:# Creates a dedicated namespace for the customer under 'deployments'.terraform/modules/central\_services/main.tf:140:resource "vault\_namespace" "customer\_ns" {.terraform/modules/central\_services/main.tf:142: path = lookup(var.names, "vault\_namespace", var.deployment\_key).terraform/modules/central\_services/main.tf:143: namespace = var.vault\_parent\_namespace.terraform/modules/central\_services/main.tf:149: namespace = vault\_namespace.customer\_ns\[0\].path\_fq.terraform/modules/central\_services/main.tf:162: namespace = vault\_namespace.customer\_ns\[0\].path\_fq.terraform/modules/central\_services/main.tf:175: namespace = vault\_namespace.customer\_ns\[0\].path\_fq.terraform/modules/central\_services/main.tf:182:# Allow access to shared ACR secret in central namespace.terraform/modules/central\_services/main.tf:222: namespace = vault\_namespace.customer\_ns\[0\].path\_fq.terraform/modules/central\_services/main.tf:230: namespace = vault\_namespace.customer\_ns\[0\].path\_fq.terraform/modules/central\_services/main.tf:239: namespace = vault\_namespace.customer\_ns\[0\].path\_fq.terraform/modules/central\_services/main.tf:248: namespace = vault\_namespace.customer\_ns\[0\].path\_fq.terraform/modules/central\_services/main.tf:258: namespace = vault\_namespace.customer\_ns\[0\].path\_fq.terraform/modules/central\_services/main.tf:279: namespace = vault\_namespace.customer\_ns\[0\].path\_fq.terraform/modules/central\_services/variables.tf:294:variable "vault\_parent\_namespace" {.terraform/modules/central\_services/variables.tf:295: description = "The parent namespace for the customer namespace. Defaults to 'deployments'."

---

That's the full picture. Here's the exact chain:

## The Double-prefix Traced End-to-end

| Layer | Value | Cumulative path |
| --- | --- | --- |
| Provider `vault.deployments` (`main.tf:3`) | `namespace = "admin/deployments"` | `admin/deployments` |
| Module variable `vault_parent_namespace` (default, not overridden) | `"deployments"` | `admin/deployments` + `deployments` |
| Resource `vault_namespace.customer_ns[0]` (line 142) | `path = "mkuh-prd-4"` | `admin/deployments/deployments/mkuh-prd-4` |

The module is designed to be used with a provider pointing at `admin`, and it handles the `deployments/` prefix itself via `vault_parent_namespace`. But you're passing it `vault.deployments` which already includes that segment.

## The Fix

Smallest, safest change—override the variable in your module call:

This tells the module "don't add any parent prefix—the provider is already scoped correctly." The namespace resource then creates `mkuh-prd-4` directly under the provider's `admin/deployments`.

Don't change the provider to `namespace = "admin"`—that would break any other resources in this workspace that rely on `vault.deployments` being scoped to `admin/deployments`.

## Before You Push

If `central_services` is the only consumer, the one-line addition is the complete fix. The Grafana `accessPolicyId` error is separate and unrelated—tackle that after this lands.

---

Close—the module validates that `vault_parent_namespace` can't be empty. So an empty string override won't work. The fix needs to be one level up.

## The Real Fix

The module is designed to receive a provider at `admin` and it adds `deployments/` itself via the default `vault_parent_namespace = "deployments"`. You're passing it a provider that's already scoped to `admin/deployments`, which doubles it.

Change the provider passed to the module:

This gives the module a provider at `admin`, the module's default `vault_parent_namespace = "deployments"` kicks in, and the namespace is created at `admin/deployments/mkuh-prd-4`. Correct.

Before you push, verify: what namespace does your default `vault` provider use?

You're looking for the default (un-aliased) provider block. It should have `namespace = "admin"`. If so, the one-line change above is the complete fix.

Also worth checking: are any other resources in this workspace using `vault.deployments` directly (not via the module)?

If anything else references `vault.deployments`, those are fine—the provider itself is correct for resources that don't add their own `deployments/` prefix. It's only the module that conflicts because it adds the prefix internally.

---

grep -B1 -A5 'provider "vault"' main.tf providers.tf | head -30 main.tf:provider "vault" { main.tfalias = "deployments" main.tfnamespace = "admin/deployments" main.tf-} main.tfmain.tf-module "central\_services" { -- providers.tfproviders.tf:provider "vault" { providers.tf-} providers.tfproviders.tf-provider "grafana" { providers.tfcloud\_access\_policy\_token = var.grafana\_cloud\_access\_policy\_token providers.tf-} …/mkuh-prod-4 on  main on ⛵ fitfile-cloud-staging-aks-cluster () on ☁ subcr-sde-prd on 🅰 (eu-west-2) at 14:17:49 ❯ grep -rn 'vault\\.deployments' \*.tf | grep -v 'module.\*central\_services' main.tf:15: vault = vault.deployments

---

That `main.tf:15` hit is the module block—the `grep -v` just didn't match because "module" and "central\_services" aren't on the same line. So `vault.deployments` has exactly one consumer: the `central_services` module.

## Confirmed Fix

The default `vault` provider in `providers.tf` has no explicit namespace, meaning it uses the `VAULT_NAMESPACE` env var—which will be `admin` in your TFC workspace. Your `vault_k8s_auth.tf` resources already work against this default provider with `namespace = "deployments/${local.deployment_key}"`, confirming it resolves to `admin`.

One-line change in `main.tf`:

The module's default `vault_parent_namespace = "deployments"` then builds the correct full path: `admin` (from provider) + `deployments` (from module default) + `mkuh-prd-4` (from `deployment_key`) = `admin/deployments/mkuh-prd-4`.

After this lands cleanly, you can also delete the entire `vault.deployments` provider alias block—nothing else uses it:

Immediate next action: Make the one-line provider swap, push, and let the plan run. The Grafana `accessPolicyId` error will likely still appear—that's a separate issue to tackle once the Vault resources are clean.

---

I see—you applied both changes, but you only needed the provider swap. The `vault_parent_namespace = ""` override on line 30 was my earlier suggestion that we already proved doesn't work (the module validates against empty strings).

With `vault = vault` (the default provider at `admin`), the module's built-in default of `vault_parent_namespace = "deployments"` is now exactly what you want. The path will be: `admin` (provider) + `deployments` (module default) + `mkuh-prd-4` (deployment\_key) = correct.

## Fix

Remove line 30 from `main.tf`:

That's it. Let the default do its job. Push and re-plan.

---

got passed the plan stage but then failed in apply

---

Big progress—the namespace fix worked. The module resources all created successfully (namespace, KV mount, approle, JWT auth backend + role). The remaining failures are now root-level resources, not module ones.

## What's failing now

The two `vault_policy` resources in `vault_k8s_auth.tf` (lines 44 and 56):

These resources set `namespace = "deployments/${local.deployment_key}"` using string interpolation. Terraform sees no dependency on the namespace resource—so it runs them in parallel with (or even before) the module finishes creating the namespace.

The module's own resources work because they reference `vault_namespace.customer_ns[0].path_fq`, which creates an implicit dependency graph edge. Your root resources bypass that entirely.

## The Fix

You need a dependency on the namespace. The cleanest option is to use the module's output:

This does two things: uses the authoritative path from the module output and creates the implicit dependency so Terraform waits for the namespace to exist.

Before pushing, confirm the output value will be correct:

You saw earlier it's `vault_namespace.customer_ns[0].path_fq`. On HCP Vault, `path_fq` returns the fully-qualified path (e.g. `admin/deployments/mkuh-prd-4`). If the default provider already sets `admin` via env var, you may get a double `admin`. So check what format the root resources expect—they currently use `"deployments/${local.deployment_key}"` (relative, no `admin/` prefix).

If `path_fq` returns the full path including `admin/`, you'll need to strip it:

Immediate next action: Run that `grep` on the outputs, then check what `path_fq` actually returns by querying Vault:

The namespace should exist now (the module created it successfully this run). The lookup will confirm the exact path format.

---

the next error

---

All Vault resources are now clean. The namespace, policies, JWT auth, KV secrets—everything created or updated successfully. The only remaining failure is the Grafana issue, which has been tagging along since the very first run.

## Remaining Error: Grafana accessPolicyId

The module is trying to create an access policy token, but the access policy itself doesn't exist (or isn't being passed). Check what the module expects:

The `accessPolicyId` error means either the `grafana_cloud_access_policy` resource failed to create in a previous run (so the token has no parent to reference), or the `access_policy_id` attribute is being computed from a resource that's not in state. The greps above will tell us which.

---

\# 1. See how the module constructs the token resource grep -B5 -A15 'grafana\_cloud\_access\_policy\_token' \\.terraform/modules/central\_services/main.tf # 2. Check if there's a corresponding access\_policy resource grep -n 'grafana\_cloud\_access\_policy' \\.terraform/modules/central\_services/main.tf # 3. Check what your grafana\_config local passes in grep -A10 'grafana\_config' locals.tf } # Grafana Cloud—Per-deployment access policy token # Replaces the manual step of adding to central-services/grafana/locals.tf resource "grafana\_cloud\_access\_policy\_token" "deployment" { count = var.enable\_grafana && var.grafana\_config!= null &&!var.is\_bootstrap? 1: 0 region = var.grafana\_config.region access\_policy\_id = var.grafana\_config.access\_policy\_id name = var.deployment\_key display\_name = "Kubernetes ${var.deployment\_key} token" } 300:resource "grafana\_cloud\_access\_policy\_token" "deployment" { grafana\_config = try(local.config.grafana\_config, null) # Dynamic Configuration Overrides hub\_group = try(local.config.hub\_group, local.workload) tfc\_project\_name = try(local.config.tfc\_project\_name, title(local.workload)) cert\_manager\_host\_network = try(local.config.cert\_manager\_host\_network, false) pki\_issuer = try(local.config.pki\_issuer, { enabled = false }) # Central Services / Names dns\_zone = try(local.config.dns\_zone, "privatelink.fitfile.net")

---

Clear. The module expects `grafana_config.access_policy_id` to be a valid Grafana Cloud access policy ID. It's being pulled from `local.config.grafana_config` (your `customer.yaml` or equivalent).

## The Problem

The `grafana_cloud_access_policy_token` resource needs a pre-existing access policy to attach the token to. The `access_policy_id` field is being passed as empty/null, so the Grafana API rejects it with `409 - Field is required`.

## Investigate

You're looking for whether this module also creates the `grafana_cloud_access_policy` resource itself, or whether it expects one to already exist and the ID passed in via config. Given it's reading from `var.grafana_config.access_policy_id`, the policy is managed externally—likely in your central-services Terraform workspace.

## Most Likely Fix

Your `customer.yaml` (or wherever `grafana_config` is defined) needs the `access_policy_id` field populated. Something like:

To find the ID:

Or check the central-services Terraform state for the existing access policy resource output. This is a config data gap, not a Terraform bug—once the ID is in your config, this will resolve. Completely separate from the Vault namespace chain you just fixed.

---

72ce4489-8442-47ad-b130-2aa7a3ecf3ba # 1. What does your config file actually have for grafana? grep -A10 'grafana' config/customer.yaml # 2. Check if there's an access policy already created in Grafana Cloud # (this would be in your central-services stack, not this workspace) grep -rn 'grafana\_cloud\_access\_policy' \\.terraform/modules/central\_services/main.tf | grep -v token # access\_policy\_id: from central-services grafana module (shared prod access policy) # URLs and user IDs: shared across all prod deployments (stack-level) grafana\_config: access\_policy\_id: "" # PASTE from central-services/grafana: grafana\_cloud\_access\_policy.prod\_deployment\_policy.policy\_id region: "prod-gb-south-0" prometheus\_host: " [https://prometheus-prod-05-gb-south-0.grafana.net](https://prometheus-prod-05-gb-south-0.grafana.net/) " prometheus\_user: "807866" loki\_host: " [https://logs-prod-008.grafana.net](https://logs-prod-008.grafana.net/) " loki\_user: "402902" tempo\_host: " [https://tempo-prod-06-prod-gb-south-0.grafana.net:443](https://tempo-prod-06-prod-gb-south-0.grafana.net/) " tempo\_user: "399415"

---

There it is—`access_policy_id: ""` with a helpful comment telling you exactly where to get it.

You've already got the ID: `72ce4489-8442-47ad-b130-2aa7a3ecf3ba`

## Fix

Commit, push, and this should be a fully clean apply. All three original errors are now resolved:

1. Vault double namespace—fixed by swapping `vault.deployments` → `vault` provider
2. Vault policy race condition—fixed by using `module.central_services.vault_namespace_path` dependency
3. Grafana access policy ID—fixed by populating the config value

---

the problem now is those vars are already in the ws. How do I import them all

---

Good news—Grafana is now clean too. The only failures are the 6 `tfe_variable` resources that already exist in the workspace but aren't in Terraform state.

## Get the Variable IDs

You need the TFE variable IDs to import. The format is `<org>/<workspace>/<variable_id>`:

## Then Generate the Import Blocks

Once you have the output (e.g. `ARM_CLIENT_ID var-abc123`), add import blocks to your config:

Or if you'd rather do it as a one-liner script after running step 2:

Immediate next action: Run command 1 and 2 to get the variable IDs, then add the import blocks and push. After a successful apply, you can remove the import blocks—they're one-shot.
