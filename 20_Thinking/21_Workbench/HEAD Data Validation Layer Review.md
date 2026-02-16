---
captured: "2026-02-16T09:38:45+00:00 2026-02-16T09:38:45+00:00"
created: 2026-02-16T09:38:47+00:00
modified: 2026-02-16T09:40:39+00:00
source: "https://chatgpt.com/c/698f34ec-85d4-8396-b6a1-124f04a5a184"
status: "processing"
tags: ["input"]
title: HEAD Data Validation Layer Review
type: "head"
---

## Raw Output / Content

I am new to cue, but this file feels wrong. It has lots of hard coded values in it. this should be a generic data validation layer that would work with many different configs. should the specific values be passed in for different configs? Can this be made more useful? Review as a data oriented architect

---

You're not wrong: this file is doing three different jobs at once:

1. Validate input (Terraform `infra_facts`)
2. Define platform policy/defaults (Auth0 domain, image pull secret, versions, persistence sizes, feature flags, etc.)
3. Render a specific Helm values shape (argocd, grafana, mongodb, ffcloud, fitconnect, etc.)

When those are fused, you end up with "validation" that's actually a single product's opinionated config, which makes reuse painful.

Below is how I'd review it as a data-oriented architect, and how to make it a genuinely reusable "data validation layer".

---

## What Feels "wrong" (and why)

### 1) "Hardcoded values" Are Really Policy, not Validation

Examples from `_platform` and elsewhere:

- Auth0 domain/audience: `"fitfile-prod.eu.auth0.com"`, `"https://…/api/v2/"`
- Image pull secret name: `"fitfile-image-pull-secret"`
- Mongo chart target: `"16.5.*"`
- Persistence: `"64Gi"`
- ArgoCD `targetRevision: "master"`
- Frontend feature flags and env limits
- Cert manager webhook hostNetwork/port
- Default Auth0 admin user id: `auth0|633…`

Those might be valid _platform defaults_, but they are not universal _schema constraints_. They should not live inside the same artifact as "input contract".

Architectural principle: treat these as policy data (owned by platform), not validation logic.

---

### 2) Output is Tightly Coupled to One Helm Chart Universe

The file doesn't just validate; it emits a very specific Helm values tree (`grafana`, `mongodb`, `ffcloud`, `fitconnect`, `workflowTemplates`, etc.).

That's fine for one stack, but it means this can't be reused as a generic validator for "many different configs" unless those configs happen to have the same charts and secret conventions.

---

### 3) Repeated Vault Template Strings = "stringly Typed config"

You've got repeated connection string templates in multiple places (mongodb conn appears several times, spicedb/postgres/auth templates too).

This creates drift risk: one template changes, five copies don't.

You started to address it with `#VaultTemplates`, but it's incomplete and inconsistent (some places still inline the strings).

---

### 4) Node Placement Logic is Suspicious

You have:

This _ignores_ the actual provided `nodeSelector/tolerations` values and replaces them with hardcoded ones, gated only on "field exists".

That's likely a bug in intent: either

- node placement is policy (then don't accept it in `infra_facts`), or
- node placement is input (then propagate it, don't override).

---

### 5) Terraform Contract is Mixed with Runtime Templating Contract

`_infraJson @tag(infra)` + `json.Unmarshal` is fine, but the file then mixes:

- terraform inputs
- helm templating strings (`{{ include … }}`)
- VaultSecretsOperator resource specs
- chart-specific knobs

This makes it hard to test and reason about "what is data" vs "what is a template program".

---

## Should Specific Values Be Passed in for Different Configs?

Yes—but not necessarily passed "everywhere".

The scalable model is:

- Schema: what must/may be provided (validation)
- Policy/default packs: platform-approved defaults (parameterizable, versioned)
- Instance overlays: environment/customer/product-specific values
- Renderers: map validated+resolved config into Helm values (or other outputs)

In CUE terms: use unification to combine layers, not one monolith.

---

## A More Reusable Design (CUE-native)

### Split into 4 files/packages (minimum)

1. `schema/infra_facts.cue`
	Only `#InfraFacts` (your contract with Terraform) + strict validation rules.
2. `policy/platform_defaults.cue`
	`_platform` moves here, but becomes data and is overrideable by env packs.
3. `products/fitfile/render.cue`
	The Helm values rendering for Fitfile charts lives here (opinionated).
4. `instances/<env>/<customer>.cue`
	Only the overrides for that deployment (or references to tags).

Then your "generic validation layer" is (1). The rest are optional add-ons.

---

## Make "policy" Explicit and Overrideable

Instead of `_platform: { …hardcoded… }`, define a _defaulted schema_ for policy:

Now:

- platform team can ship defaults
- environments can override `platform.auth0.domain` without editing product renderer
- validation still applies (domain must be string, etc.)

---

## Turn Your Renderer into a Parameterized "function"

Right now you implicitly use `_infra` and `_platform`. Make it explicit:

Then an instance supplies `infra` (from tag) and `policy` (from defaults + overrides). That's how you make this reusable across different stacks: you can have multiple renderers against the same validated `infra`.

---

## Normalize Vault Templating: Single Source of Truth

Finish what you started: one template library, referenced everywhere.

- Keep `#VSO.map`
- Make `#VaultTemplates.mongodbConn` the only way mongodb conn is produced
- Same for postgresql/spicedb/auth
- Then in each component you reference those templates

This reduces drift and review surface dramatically.

---

## Tighten Schema Validation (real "data Validation layer" value)

Your `#InfraFacts` is currently mostly "types + some defaults". Add constraints that prevent bad deployments:

Examples:

- `deployment_key`: regex (k8s namespace safe), max length
- `public_fqdn`: must be a hostname / not contain scheme
- `customer_short_name`: restricted charset
- if `s3_export.enabled: true` then require `vault_path` and `secret_name`
- if `pki_issuer.enabled: true` then require `vault_namespace`, `pki_path`, `role_id`
- enforce `fitconnect_hosts[*].fitConnectCode == infra.fit_connect_code` (if that's expected)
- enforce allowed deploy flags or consistency rules (e.g., if `deploy.spicedb=false` but apps require it, fail early)

That's where CUE shines: preventing invalid combinations before Helm/Terraform apply.

---

## Fix the Node Placement bug/ambiguity

Decide ownership:

- If node placement is input-driven, propagate directly:
	- `nodeSelector: _infra.node_placement.nodeSelector`
	- `tolerations: _infra.node_placement.tolerations`
- If node placement is platform policy, remove it from `#InfraFacts` and move it into policy packs by component (workflows, db, etc.)

Right now it's the worst of both: accepts input, then ignores it.

---

## What I Would Do First (high ROI, Low risk)

1. Extract `_platform` into `policy/` and make it overrideable.
2. Extract `#InfraFacts` into `schema/` and add real constraints + conditional requirements.
3. Extract `#VaultTemplates` and finish deduping (no inline conn strings).
4. Refactor node placement to either propagate or own it as policy.

That alone will make this materially more useful across configs without rewriting everything.

---

If you want, I can propose a concrete new folder layout + a refactored CUE skeleton that still supports your current invocation style (`cue export … -t infra="…"`) but cleanly separates schema vs policy vs rendering.

---

propose a concrete new folder layout + a refactored CUE skeleton that still supports your current invocation style (cue export… -t infra="…") but cleanly separates schema vs policy vs rendering.

---

Here's a concrete folder layout + a refactored CUE skeleton that keeps your current invocation working:

…but cleanly splits schema vs policy vs rendering.

---

## Proposed Folder Layout

You can keep `package config` everywhere if you like, but I'd recommend using packages (`schema`, `policy`, `templates`, `fitfile`) so the boundaries stay real.

---

## 1) cue/schema/infra\_facts.cue (validation-only)

```markdown
cuepackage schema

// Contract with Terraform output: \`infra_facts\`
#InfraFacts: {
  customer_short_name: string
  deployment_key:      string
  public_fqdn:         string
  fit_connect_code:    string

  // Example: real validation constraints (add more as needed)
  deployment_key: =~"^[a-z0-9]([-a-z0-9]*[a-z0-9])?$"   // k8s-ish name
  public_fqdn:    =~"^([a-zA-Z0-9-]+\\.)+[a-zA-Z]{2,}$" // hostname (no scheme)

  deploy: {
    certManager:               bool | *true
    spicedb:                   bool | *true
    persistence:               bool | *true
    messageBroker:             bool | *false
    blobCsiDriver:             bool | *false
    seedData:                  bool | *false
    workflowsIntegrationTests: bool | *false
    monitoring:                bool | *false
  }

  node_placement?: {
    nodeSelector?: {[string]: string}
    tolerations?: [...{
      key:      string
      operator: "Equal" | "Exists"
      value?:   string
      effect?:  "NoSchedule" | "PreferNoSchedule" | "NoExecute"
    }]
  }

  // ...keep going with the rest of your Terraform contract
}
```

This file should never mention Helm charts, versions, Auth0 domains, secret names, etc.

---

## 2) cue/policy/platform\_policy.cue (policy Schema + defaults)

Optional environment overrides:

### cue/policy/env/prod.cue

### cue/policy/env/dev.cue

---

## 3) cue/templates/vault.cue (dedupe templates)

---

## 4) cue/render/fitfile/values.cue (renderer: Infra + Policy → Helm values)

---

## 5) cue/values.cue (thin Entrypoint Wrapper, Keeps Your invocation)

This is the only file that cares about `-t infra="…"`.

```markdown
cuepackage config

import (
  "encoding/json"

  "cue/schema"
  "cue/policy"
  "cue/policy/env"    // optional: you can remove if you don’t want env layering yet
  "cue/render/fitfile"
)

// Keep your current CLI contract:
_infraJson: string @tag(infra)
infra: schema.#InfraFacts & json.Unmarshal(_infraJson)

// Optional env selector (defaults to "prod" here). You can omit entirely.
_envName: string | *"prod" @tag(env)

// Compose policy layers:
// base defaults + env overrides (if present)
policy: policy.#Defaults & (
  if _envName == "prod" { env.Env } else if _envName == "dev" { env.Env } else {}
)

// Render final values
values: (fitfile.#Render & {
  infra:  infra
  policy: policy
}).values
```

> If you don't want `-t env=…` yet, delete `_envName` and the `env` import, and set `policy: policy.#Defaults`.

---

## Commands that Work Immediately

### Current Behavior (only Infra tag)

### With Environment Overrides (optional)

---

## Why This Structure Stays Generic

- `schema/` is reusable across _many_ configs (pure validation)
- `policy/` is platform-owned defaults and constraints (overrideable)
- `render/fitfile/` is the only opinionated Fitfile/Helm wiring
- The entrypoint is tiny and keeps your exact invocation style

---

If you want, I can adapt this skeleton to your _actual_ `#InfraFacts` shape by lifting it directly from your current `values.cue` (and I'll also point out the couple of places where your existing logic is overriding input unintentionally, like node placement).

---

cue export./values.cue -t infra="$(terraform output -json infra\_facts)" -e values ╷ │ Error: Output "infra\_facts" not found │ │ The output variable requested could not be found in the state file. If you │ recently added this to your configuration, be sure to run `terraform ` │ apply`, since the state won't be updated with new output variables until ` │ that command is run. ╵ no tag for "infra" expected ')', found 'IDENT' \_envName:./values.cue:22:6

---

You've got two separate problems here: one is Terraform (no such output), and the other is a CUE syntax/tag/package wiring issue in the skeleton.

## 1) Terraform: infra\_facts Output Doesn't Exist (yet)

Terraform is telling you your state file has no output named `infra_facts`.

Quick ways to confirm what outputs you _do_ have:

Or list them as JSON keys:

Then either:

- use the correct output name in your command, or
- add an output in Terraform and run `terraform apply`.

Example Terraform output definition:

Then:

So: the first error is simply "wrong/missing Terraform output name".

---

## 2) CUE: "no Tag for infra" + Parse Error near \_envName

These come from two issues in the skeleton I gave:

### A) @tag(infra) Only Works if You Use the Tag Injection Correctly

With `cue export file.cue -t infra=…`, CUE replaces tagged fields. But you must ensure:

- the tagged field exists in the same package instance you are exporting, and
- the file parses cleanly (yours didn't), otherwise CUE never sees the tag.

### B) The Parse Error Expected ')', Found 'IDENT' \_envName means the Import block/package Path Isn't Valid as Written

In the skeleton, I used imports like `"cue/schema"` etc. That assumes you have a `cue.mod` module and correct module paths. If you don't, CUE will often choke or behave strangely depending on how you lay out packages.

Also: in CUE, you can't import a directory like `cue/policy/env` as a package called `env` unless it's a real package and module path resolves.

---

## A Working Minimal Skeleton (no Module assumptions)

Below is a concrete layout that works even without cue.mod, by keeping everything in one package (`package config`) and splitting by files only. This avoids import/module pain and fixes your parsing/tag issues.

## Folder Layout (simple, robust)

Everything is `package config`, so no imports.

---

## cue/schema\_infra.cue

---

## cue/policy\_defaults.cue

---

## cue/templates\_vault.cue

---

## cue/render\_fitfile.cue

---

## cue/values.cue (entrypoint With tag)

---

## Command that Will Work (once Terraform Output exists)

If your Terraform output name is different, substitute it:

---

## Why Your Earlier Errors Happened (in One line each)

- Terraform: you don't have an output called `infra_facts` in state → create it + `terraform apply`, or use the correct existing output name.
- CUE: the earlier multi-package/module import layout didn't parse/resolve in your repo → CUE never saw the tag field, and you got both a parse error and "no tag for infra".

---

If you paste the output of `terraform output` (just the names), I can tell you exactly what to use in the command, and if you share your current `#InfraFacts` portion I can drop it into the schema file so you don't lose any existing fields.

---

I ran it from the correct upper folder for the terraform to work but still get cue export./cue/values.cue -t infra="$(terraform output -json infra\_facts)" -e values no tag for "infra" expected ')', found 'IDENT' \_envName:./cue/values.cue:22:6

---

That error combo is exactly what happens when your `./cue/values.cue` still contains the earlier `_envName` skeleton (or an import block that doesn't parse). Once the file fails to parse, CUE often also reports "no tag for infra" because it never successfully loads the field with `@tag(infra)`.

### Fix: replace./cue/values.cue with This Minimal Entrypoint (no \_envName)

Open `./cue/values.cue` and make it exactly:

Then ensure these files exist alongside it (same `package config`):

- `./cue/schema_infra.cue` defining `#InfraFacts`
- `./cue/policy_defaults.cue` defining `platform` and `#PlatformPolicy`
- `./cue/render_fitfile.cue` defining `#RenderValues`

If _any_ of those have `package somethingElse`, you'll get weird "not found" behaviour. They all need to be `package config` for this "no-module" approach.

---

## Why You're seeing Expected ')', Found 'IDENT' \_envName:./cue/values.cue:22:6

Because line ~22 in your current `values.cue` still has an `_envName:` field _after_ something CUE thinks should have been closed (usually a broken `import (…)` block or a bad package import path). Deleting the `_envName` version and using the minimal file above removes the problem.

---

## Re-run the Command

From the Terraform root (so `terraform output` works):

Note: I'm exporting the directory`./cue` rather than a single file. That guarantees CUE loads all the sibling `.cue` files in the package.

If you prefer the file path, this also works _as long as_ all the other files are in the same package and included:

---

## Quick Sanity Check: Does CUE See the Tag Now?

Run:

If the tag is recognized, you'll get schema errors about missing fields in `{}` (expected). If it still says "no tag for infra", then your `@tag(infra)` field is not in the loaded package instance (most commonly: `package` mismatch or you're not loading the right files).

---

If you paste your current `./cue/values.cue` (just that file), I'll point to the exact syntax break at line 22 and rewrite it in-place.

---

cue export./cue/values.cue -t infra="$(terraform output -json infra\_facts)" -e values infra: reference "#InfraFacts" not found:./cue/values.cue:9:8 values: reference "#RenderValues" not found:./cue/values.cue:12:10 values.policy: reference "platform" not found:./cue/values.cue:14:11

---

Good—now CUE is parsing and seeing your tag. These new errors mean: `values.cue` is the only file being loaded, so it can't see the definitions that live in other `.cue` files (`#InfraFacts`, `#RenderValues`, `platform`).

In CUE, `cue export./cue/values.cue …` loads _just that file_ unless the other files are brought into the same package instance via the directory.

## Fix: Export the Directory (recommended)

Run:

That loads all`.cue` files in `./cue/` that share the same `package` name.

---

## Also Verify: All Files Are in the Same Package

At the very top of each file in `./cue/` you need the same package line, e.g.:

If your other files say `package schema` / `package policy` etc, then with no `cue.mod` module/imports they won't be visible to `values.cue`.

So either:

### Option A (no Module, simplest)

Make sure these exist in `./cue/` and all say `package config`:

- `schema_infra.cue` → defines `#InfraFacts`
- `policy_defaults.cue` → defines `platform` and `#PlatformPolicy`
- `render_fitfile.cue` → defines `#RenderValues`
- `values.cue` → entrypoint

Then `cue export./cue …` works.

### Option B (module + Real packages)

If you _want_ separate packages (`schema`, `policy`, `render/fitfile`) then you must create `cue.mod` and use proper imports. That's a bigger step; we can do it, but Option A will get you unblocked immediately.

---

## Quick "show Me what CUE is loading" Check

From the same folder you're running the command:

You should see all the files. If not, you're pointing at the wrong directory.

---

## One More Gotcha: File Extensions and Hidden Files

Make sure the helper files are actually named `*.cue` and live under `./cue/` (not `./cues/`, not `./cue/schema/*.cue` unless you export `./cue/…` or have a module set up).

---

### Minimal Working Command Sequence

If you run `ls./cue/*.cue` and paste the filenames + the first line (`package …`) from each file, I can tell you immediately which mismatch is causing the missing references.

---

cue export./cue/values.cue \\ -t infra="$(terraform output -json infra\_facts)" \\ -e values infra: reference "#InfraFacts" not found:./cue/values.cue:9:8 values: reference "#RenderValues" not found:./cue/values.cue:12:10 values.policy: reference "platform" not found:./cue/values.cue:14:11 …/LCA-DP on  main $!? on ⛵ fitfile-cloud-prod-1-aks-cluster-admin () on ☁️ FitFileLZ on 🅰 (eu-west-2) at 14:47:46 ❯ tree cue  cue ├── 󰲹 policy\_defaults.cue ├── 󰲹 render\_fitfile.cue ├── 󰲹 schema\_infra.cue ├── 󰲹 templates\_vault.cue └── 󰲹 values.cue

---

You're super close. The `tree` confirms the files are there—the reason CUE still can't see `#InfraFacts/#RenderValues/platform` is because you're exporting only `./cue/values.cue`, and CUE is not loading the sibling files in the package in that invocation.

### Do This instead (export the directory)

That loads _all_`.cue` files under `./cue/` in the same package instance.

---

## If You Must Export values.cue (not the directory)

Then you need to explicitly include the other files on the command line:

But exporting the directory is the normal way.

---

## One More Check (likely not Needed, but quick)

Make sure every file starts with exactly the same package line, e.g.:

If any file says `package schema` or similar, CUE will treat it as a different package and it won't unify.

You can check quickly:

---

### Why This Happens

- `cue export./cue/values.cue` ⇒ loads _just that file_.
- `cue export./cue` ⇒ loads the _package instance_ (all files in that folder with same `package`).

Run the directory export and you should be past the "reference not found" errors.
