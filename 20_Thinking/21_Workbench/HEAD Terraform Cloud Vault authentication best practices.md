---
captured: "2026-03-07T16:52:17+00:00 2026-03-07T16:52:17+00:00"
created: 2026-03-07T16:52:18+00:00
modified: 2026-03-14T11:10:34+00:00
source: "https://claude.ai/chat/fef056e5-8fa2-4148-b96b-e0e342b20d6a"
status: "processing"
tags: ["input"]
title: HEAD Terraform Cloud Vault authentication best practices
type: "head"
---

## Raw Output / Content

I am using terraform cloud to deploy secrets to my hcp vault. the workspace needs to authenticate with the vault. I have this suggestion but I don't want to keep adding a new token manually. What is the best practice to allow my tfc to manage a name space 1. `VAULT_TOKEN`: Generate a temporary Vault token from your local authenticated CLI that has namespace read privileges and add it to TFC. You can generate one by running: vault token create -ttl=24h Paste the returned `token` value into TFC as an Environment Variable named `VAULT_TOKEN`. (Mark both variables as Sensitive in TFC!)

---

That suggestion is the manual token anti-pattern—it's operationally fragile and a security risk. You'd be chasing expiry every 24 hours (or setting long TTLs, which is worse). Here's what you actually want.

## The Right Answer: TFC Dynamic Provider Credentials (Workload Identity)

The principle: Terraform Cloud generates a unique OIDC JWT for every single run. You configure Vault to trust TFC as an identity provider via a JWT auth method. Each run authenticates itself—no static secrets exist anywhere.

Why this is correct:

- Zero stored credentials. Nothing to rotate, nothing to leak.
- Each run gets a short-lived Vault token scoped to exactly the policy you define.
- It's Vault's own recommended pattern and TFC's native integration—not a workaround.

## How It Works (the chain)

## Micro-Steps to Set It Up

### Step 1—Create the JWT Auth Method in HCP Vault

This tells Vault "I trust tokens signed by Terraform Cloud."

The `oidc_discovery_url` is the key bit—Vault fetches TFC's public signing keys from `https://app.terraform.io/.well-known/openid-configuration` and uses them to verify run JWTs. No shared secret needed.

### Step 2—Create a Vault Policy for what TFC Can Do

Scope this to the namespace/paths your workspace needs. For example, if TFC is managing secrets in a specific namespace:

Tighten this to your actual needs—this is deliberately broad for illustration.

### Step 3—Create the JWT Auth Role Bound to Your Workspace

This is where you lock it down to a specific TFC organisation and workspace:

The `bound_claims.sub` is the security boundary. It ensures only runs from that specific workspace can authenticate. The `sub` claim format is documented by HashiCorp—the `*` on `run_phase` allows both plan and apply phases.

### Step 4—Configure the TFC Workspace Environment Variables

In your TFC workspace, set these as environment variables (not Terraform variables):

| Variable | Value | Sensitive? |
| --- | --- | --- |
| `TFC_VAULT_PROVIDER_AUTH` | `true` | No |
| `TFC_VAULT_ADDR` | `https://your-cluster.vault.hashicorp.cloud:8200` | No |
| `TFC_VAULT_RUN_ROLE` | `tfc-my-workspace` | No |
| `TFC_VAULT_AUTH_PATH` | `jwt-tfc` | No |
| `TFC_VAULT_NAMESPACE` | `admin` (or your HCP root namespace) | No |

No `VAULT_TOKEN` at all. TFC sees these variables, knows to use workload identity, and handles the JWT exchange automatically.

### Step 5—Configure the Vault Provider in Your Terraform Code

That's it. The provider picks up the dynamically-minted token from TFC's environment.

---

## The Chicken-and-Egg Problem

You'll notice Steps 1–3 themselves need a Vault token to create the auth method and role. This is the one place where a manually-created token is acceptable—as a bootstrap action, run once. After that, the JWT auth method handles everything and you never touch a token again.

Your immediate next action: Check whether you already have a `jwt` or `oidc` auth method enabled in your HCP Vault by running `vault auth list` from your CLI. That tells you if someone has already started this, or if you're starting from scratch.

---

export VAULT\_NAMESPACE=admin/ ❯ vault auth list Path Type Accessor Description Version ---- ---- -------- ----------- ------- approle/ approle auth\_approle\_f0941c94 n/a n/a jwt-lca-prd-2/ jwt auth\_jwt\_86bd19f9 JWT auth for lca-prd-2 cluster n/a jwt-terraform/ jwt auth\_jwt\_30371417 n/a n/a jwt/ jwt auth\_jwt\_39c1d7b2 n/a n/a kubernetes/ kubernetes auth\_kubernetes\_8c2a4b7a n/a n/a local-dev-auth-mount/ approle auth\_approle\_1b65f67b n/a n/a token/ ns\_token auth\_ns\_token\_8395ce45 token based credentials n/a

---

You've already got `jwt-terraform/` sitting there—that's your TFC auth method. You're past the bootstrap.

Immediate next action: Check what role(s) are configured on it and whether the OIDC discovery URL is pointing at TFC:

Then list existing roles:

If any roles come back, read the one that looks relevant:

Paste what comes back and we'll see if it's already wired up correctly or needs adjusting for your workspace. You might be closer to done than you think.

---

vault read auth/jwt-terraform/config Key Value --- ----- bound\_issuer [https://app.terraform.io](https://app.terraform.io/) default\_role n/a jwks\_ca\_pem n/a jwks\_pairs \[\] jwks\_url n/a jwt\_supported\_algs \[\] jwt\_validation\_pubkeys \[\] namespace\_in\_state true oidc\_client\_id n/a oidc\_discovery\_ca\_pem n/a oidc\_discovery\_url [https://app.terraform.io](https://app.terraform.io/) oidc\_response\_mode n/a oidc\_response\_types \[\] provider\_config map\[\] unsupported\_critical\_cert\_extensions <nil> ~ on ⛵ fitfile-cloud-staging-aks-cluster () on ☁️ Shared Services on 🅰 (eu-west-2) at 16:26:28 ❯ vault list auth/jwt-terraform/role Keys ---- tfc-role ~ on ⛵ fitfile-cloud-staging-aks-cluster () on ☁️ Shared Services on 🅰 (eu-west-2) at 16:26:35 ❯ vault read auth/jwt-terraform/role/tfc-role Key Value --- ----- alias\_metadata map\[\] allowed\_redirect\_uris \[[https://app.terraform.io](https://app.terraform.io/)\] bound\_audiences \[vault.workload.identity\] bound\_claims map\[sub:organization:FITFILE-Platforms:project:\*:workspace:\*:run\_phase:\*\] bound\_claims\_type glob bound\_subject n/a claim\_mappings <nil> clock\_skew\_leeway 0 expiration\_leeway 0 groups\_claim n/a max\_age 0 not\_before\_leeway 0 oidc\_scopes <nil> role\_type jwt token\_bound\_cidrs \[\] token\_explicit\_max\_ttl 0s token\_max\_ttl 0s token\_no\_default\_policy false token\_num\_uses 0 token\_period 0s token\_policies \[hcp-root tfc-policy\] token\_ttl 20m token\_type default user\_claim terraform\_full\_workspace user\_claim\_json\_pointer false verbose\_oidc\_logging true

---

This is already fully wired up and quite permissively scoped. Here's what you've got:

The auth method (`jwt-terraform/`) is correctly pointing at TFC's OIDC discovery URL. That's the trust anchor—Vault fetches TFC's signing keys automatically.

The role (`tfc-role`) is configured with:

- `bound_claims.sub` = `organization:FITFILE-Platforms:project:*:workspace:*:run_phase:*`—this allows any workspace in any project across your FITFILE-Platforms org to authenticate. That's deliberately broad, which is fine if all your TFC workspaces are trusted to have the same Vault access.
- `token_policies` = `hcp-root` and `tfc-policy`—these control what the authenticated run can actually do.
- `token_ttl` = 20 minutes—sensible for a run.
- `bound_audiences` = `vault.workload.identity`—correct for TFC's dynamic credentials.

You're done on the Vault side. The only thing left is the TFC workspace configuration.

Immediate next action: Go to your TFC workspace → Variables and check whether these environment variables already exist:

| Variable | Expected Value |
| --- | --- |
| `TFC_VAULT_PROVIDER_AUTH` | `true` |
| `TFC_VAULT_ADDR` | your HCP Vault cluster URL |
| `TFC_VAULT_RUN_ROLE` | `tfc-role` |
| `TFC_VAULT_AUTH_PATH` | `jwt-terraform` |
| `TFC_VAULT_NAMESPACE` | `admin` |

If those five are set, you can remove any `VAULT_TOKEN` variable entirely—it's redundant and will actually take precedence if present, bypassing the dynamic credential flow.

One thing worth checking: run `vault read sys/policy/tfc-policy` to see what that policy actually grants. The `hcp-root` policy name is a bit eyebrow-raising—if that's literally the root policy, your TFC runs have full admin access to the entire namespace, which works but is broader than you might want long-term.

---

~~vault\_address~~ Overwritten View The vault address accessible to the consuming modules via a terraform variable with the same name

[https://vault-public-vault-8b38a0c2.e3dedc53.z1.hashicorp.cloud:8200/terraformNone](https://vault-public-vault-8b38a0c2.e3dedc53.z1.hashicorp.cloud:8200/terraformNone) TFC\_VAULT\_ADDR The address of the Vault instance manage

[https://vault-public-vault-8b38a0c2.e3dedc53.z1.hashicorp.cloud:8200/envNone](https://vault-public-vault-8b38a0c2.e3dedc53.z1.hashicorp.cloud:8200/envNone) TFC\_VAULT\_NAMESPACE The namespace in Vault where the pre-configured jwt auth method was setup

admin/fitfileenvNone TFC\_VAULT\_PROVIDER\_AUTH Must be present and set to true, or Terraform Cloud will not attempt to authenticate to Vault.

trueenvNone TFC\_VAULT\_RUN\_ROLE The pre configured role setup in Vault to authorize with. This was created within the admin/fitfile namespace

tfc-roleenvNone

---

Two problems jumping out:

1\. `TFC_VAULT_AUTH_PATH` is missing entirely. Without it, TFC defaults to the `jwt` mount path. But your auth method is mounted at `jwt-terraform`. So TFC is trying to authenticate against the wrong mount. Add:

| Variable | Value | Type |
| --- | --- | --- |
| `TFC_VAULT_AUTH_PATH` | `jwt-terraform` | env |

2\. Namespace mismatch—possibly. Your `TFC_VAULT_NAMESPACE` is set to `admin/fitfile`, but when you ran `vault auth list` under `admin/`, the `jwt-terraform/` method was there—in `admin/`, not `admin/fitfile`.

`TFC_VAULT_NAMESPACE` tells TFC which namespace to authenticate _against_. If `jwt-terraform` lives in `admin/` but TFC is pointing at `admin/fitfile`, the auth request will fail because Vault won't find the mount in that child namespace.

Quick check to confirm: Run this to see if there's a separate auth method in the child namespace:

If `jwt-terraform/` doesn't appear there, then you need to decide:

- Option A: Change `TFC_VAULT_NAMESPACE` to `admin` (where the auth method actually lives), and ensure the `tfc-policy` grants access into the `admin/fitfile` namespace path.
- Option B: Create a dedicated JWT auth method inside `admin/fitfile` with a role scoped to that namespace's resources.

Option A is simpler and is the typical pattern—authenticate at the parent, policy grants access to the child.

Immediate next action: Run that `vault auth list` against `admin/fitfile` and paste the result. That tells us which fix you need.

---

VAULT\_NAMESPACE=admin/fitfile vault auth list Path Type Accessor Description Version ---- ---- -------- ----------- ------- jwt/ jwt auth\_jwt\_19768b24 n/a n/a kubernetes/ kubernetes auth\_kubernetes\_29405a4f n/a n/a token/ ns\_token auth\_ns\_token\_32a2f20c token based credentials n/a userpass/ userpass auth\_userpass\_6dba455e n/a n/a

---

Interesting—there _is_ a `jwt/` mount in `admin/fitfile`. And since `TFC_VAULT_AUTH_PATH` is missing, TFC defaults to `jwt`. So it might actually be hitting this mount by accident and working (or failing for a different reason).

But we need to verify this mount is actually configured for TFC. Run:

Then:

If a role exists:

This tells us whether the `jwt/` mount in `admin/fitfile` is wired to TFC's OIDC, or if it's configured for something else entirely (like one of your AKS clusters). That's the fork in the road—either this mount is already your TFC auth and just needs a role tweak, or it belongs to another workload and you need to either create a `jwt-terraform/` mount here or switch `TFC_VAULT_NAMESPACE` to `admin`.

---

VAULT\_NAMESPACE=admin/fitfile vault read auth/jwt/config Key Value --- ----- bound\_issuer [https://app.terraform.io](https://app.terraform.io/) default\_role n/a jwks\_ca\_pem n/a jwks\_pairs <nil> jwks\_url n/a jwt\_supported\_algs \[\] jwt\_validation\_pubkeys \[\] namespace\_in\_state true oidc\_client\_id n/a oidc\_discovery\_ca\_pem n/a oidc\_discovery\_url [https://app.terraform.io](https://app.terraform.io/) oidc\_response\_mode n/a oidc\_response\_types \[\] provider\_config map\[\] unsupported\_critical\_cert\_extensions <nil> ~ on ⛵ fitfile-cloud-staging-aks-cluster () on ☁️ Shared Services on 🅰 (eu-west-2) at 16:29:00 ❯ VAULT\_NAMESPACE=admin/fitfile vault list auth/jwt/role Keys ---- tfc-role ~ on ⛵ fitfile-cloud-staging-aks-cluster () on ☁️ Shared Services on 🅰 (eu-west-2) at 16:29:17 ❯ VAULT\_NAMESPACE=admin/fitfile vault read auth/jwt/role/tfc-role Key Value --- ----- alias\_metadata map\[\] allowed\_redirect\_uris <nil> bound\_audiences \[vault.workload.identity\] bound\_claims map\[sub:organization:FITFILE-Platforms:project:\*:workspace:\*:run\_phase:\*\] bound\_claims\_type glob bound\_subject n/a claim\_mappings <nil> clock\_skew\_leeway 0 expiration\_leeway 0 groups\_claim n/a max\_age 0 not\_before\_leeway 0 oidc\_scopes <nil> policies \[tfc-policy\] role\_type jwt token\_bound\_cidrs \[\] token\_explicit\_max\_ttl 0s token\_max\_ttl 0s token\_no\_default\_policy false token\_num\_uses 0 token\_period 0s token\_policies \[tfc-policy\] token\_ttl 20m token\_type default user\_claim terraform\_full\_workspace user\_claim\_json\_pointer false verbose\_oidc\_logging false

---

This is fully wired up and should already be working. Here's the complete picture:

- `TFC_VAULT_NAMESPACE` = `admin/fitfile` → correct, the `jwt/` mount lives there
- `TFC_VAULT_AUTH_PATH` is absent → TFC defaults to `jwt` → which is exactly where the mount is
- The `tfc-role` in this namespace has the right OIDC discovery, bound audience, and org claim

So the missing `TFC_VAULT_AUTH_PATH` is actually fine here because the mount _is_ at the default `jwt/` path. No change needed.

The only meaningful difference from the parent namespace role: this one grants `tfc-policy` only (no `hcp-root`). That's actually better—tighter scoping.

Quick check: Verify what that policy actually allows:

If that policy has the permissions your workspace needs, then your setup is complete and you should never need to set a `VAULT_TOKEN`. If you currently have a `VAULT_TOKEN` variable in that TFC workspace, remove it—it will override the dynamic credential flow and defeat the whole point.

To confirm end-to-end: Trigger a speculative plan in TFC and look at the logs for a line like `Successfully authenticated to Vault via OIDC`. That's your proof the chain is working.

---

---

Yes, that's likely your actual problem. There are two separate concerns here that are crossing wires:

Authentication (where TFC gets its token): `admin/fitfile`—controlled by `TFC_VAULT_NAMESPACE`

Operations (where the provider tries to do things): `admin`—hardcoded in your provider block

The token TFC receives is minted in `admin/fitfile` with the `tfc-policy` from that namespace. When your provider then tries to operate in `admin` (the parent), that token almost certainly doesn't have permissions up there. Vault tokens are scoped to the namespace they were issued in and below, not above.

You have two options depending on where you actually need to manage resources:

Option A—You're managing resources inside `admin/fitfile`:Strip the provider block back and let TFC's environment variables handle everything:

This means the provider operates in `admin/fitfile`, matching where the token was issued.

Option B—You genuinely need to manage resources in the parent `admin` namespace:Change `TFC_VAULT_NAMESPACE` in TFC to `admin`, so authentication happens against the `jwt-terraform/` mount there (which has the `hcp-root` + `tfc-policy` policies). Then set `TFC_VAULT_AUTH_PATH` to `jwt-terraform` since that's the mount path in `admin`. Your provider block would stay as-is.

Immediate next action: Decide which namespace your Terraform code is actually targeting. Run a quick `grep -r "vault_" *.tf` in the workspace to see what resources you're creating—are they secrets/mounts/policies inside `admin/fitfile`, or in `admin`?
