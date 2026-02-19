---
captured: "2026-02-18T13:11:20+00:00 2026-02-18T13:11:20+00:00"
created: 2026-02-18T13:11:23+00:00
modified: 2026-02-18T13:13:18+00:00
source: "https://gemini.google.com/app/8295ee14d81953b5"
status: "processing"
tags: ["input"]
title: HEAD You said I am attempting to make the iac code
type: "head"
---

## Raw Output / Content

I am attempting to make the iac code simple to reuse. I wanted a single source of truth that I fill in for a new customer deployment. The goal is that the dev enters as small amount of data as possible and the iac handles the rest using the provided names and vars to calculate the rest. I am trying to avoid human error. There is a config/customer.yaml that is supposed to be that source of truth, but it is just a complicated. and the local.tf generates config as well. is the customer.yaml file redundant and we could just use the local.tf? How can we move the necessary complexity to the data? Review the code and make a plan

---

Based on the files you have provided, specifically `LCA-DP/config/customer.yaml` and `LCA-DP/locals.tf`, I have analysed the structure and logic of your deployment.

To answer your specific question: Yes, the `customer.yaml` file is redundant in a pure Terraform context. You are currently maintaining two layers of abstraction (YAML and HCL) which forces the developer to context-switch and debug YAML indentation rather than focusing on the infrastructure logic.

The complexity is currently "leaking" into your configuration file. Your `customer.yaml` contains implementation details (like `vnet_resource_group_name`, `cert_manager_host_network`, and specific `node_selector` strings) that should be handled by your logic, not the human entering the data.

Here is the plan to simplify your IaC, move complexity into the logic, and reduce the human input to the absolute minimum.

### The Strategy: "Convention over Configuration"

We will shift from an "Explicit Configuration" model (where the user defines everything) to a "Derived Configuration" model (where the user defines the _identity_, and the code derives the _infrastructure_).

#### Phase 1: Identify the "Golden Inputs"

We need to separate Identity (what makes this customer unique) from Implementation (how we build it).

Currently, your `customer.yaml` has over 40 lines of config. We can reduce this to 4 inputs.

The Only Inputs You Actually Need:

1. `customer_name` (e.g., "lca")
2. `customer_full_name` (e.g., "Liverpool City Region…")
3. `environment` (e.g., "live", "dev")
4. `region` (e.g., "uks")

_Everything else_ in your current YAML can be calculated or defaulted in `locals.tf`.

#### Phase 2: Refactoring locals.tf (The Calculation Engine)

We will move the logic from the YAML file into `locals.tf`.

1\. Standardise Naming (Remove Overrides) Currently, `customer.yaml` allows users to override `vnet_name` and `vnet_resource_group_name`. This invites human error.

- Plan: Remove the ability to override. Enforce the naming convention strictly in `locals.tf`.
	- _Logic:_`vnet_name` is _always_ `vnet-${local.workload}-plat-${local.region}-01`.

2\. Standardise Network Sizing Currently, the user defines `vnet_address_space`.

- Plan: Assign a unique integer ID to the customer (e.g., `instance_id: 2`) and calculate the CIDR automatically.
	- _Logic:_`vnet_cidr = "10.${local.instance_id}.0.0/16"`
	- The subnets are already calculated via `cidrsubnet` in your `locals.tf`, which is excellent. We just need to automate the root CIDR.

3\. Feature Profiles (T-Shirt Sizing) Currently, you list individual flags like `spicedb: true`, `monitoring: true`, `frontend: true`.

- Plan: Create "Profiles" in `locals.tf`.
	- _Logic:_ If `environment == "live"`, enable all production features (monitoring, HA, backups). If `environment == "dev"`, disable expensive features.

#### Phase 3: The New Input Structure (Implementation)

I propose deleting `customer.yaml` and using a standard `terraform.tfvars` or a simplified `locals` block for input.

Option A: The Pure Terraform Approach (Recommended) Create a file named `customer.auto.tfvars`.

Option B: The Simplified YAML Approach If your Python scripts (`report.py`, etc.) rely on YAML, keep the file but strip it down to the bare minimum.

### The Execution Plan

Here is the step-by-step plan to refactor your codebase:

1. Audit External Dependencies:
	- Check `LCA-DP/scripts/report.py` and `values_generator.tf`. Do they _require_ the YAML file to exist?
	- _Action:_ If yes, we will stick to Option B (Simplified YAML) to avoid breaking your reporting tools, but we will gut the file contents.
2. Update `variables.tf` / `locals.tf`:
	- Define a default `deploy` map in `locals.tf` that serves as the "Base Blueprint".
	- Use the `merge` function to overlay environment-specific defaults.
3. Hardcode the Conventions:
	- In `locals.tf`, stop looking for `local.config.vnet_name`.
	- Change it to: `vnet_name = "vnet-${local.customer_short_name}-plat-${local.region}-01"` (or your preferred standard).
	- This forces all customers to have consistent resource naming.
4. Refactor `customer.yaml`:
	- Delete the `deploy` block, `tags`, `node_placement`, and `pki_issuer` blocks from the YAML.
	- Move these default values into `locals.tf`.

### Example of the Resulting Logic (locals.tf)

This is how `locals.tf` will look after the refactor. It takes the simple input and expands it into the complex configuration you currently ask humans to write.

Terraform

```hcl
locals {
  # 1. Load Minimal Config
  raw_config = yamldecode(file("${path.module}/config/customer.yaml"))

  # 2. Derive Identity
  name        = local.raw_config.name
  region      = local.raw_config.region
  environment = local.raw_config.env
  
  # 3. Auto-Calculate Network (No human input required)
  # Example: ID 2 becomes 10.2.0.0/16
  vnet_cidr = "10.${local.raw_config.id}.0.0/16" 

  # 4. Define Feature Profiles (Logic moves here)
  # We define the "Standard" deployment here, not in the YAML
  standard_deployment = {
    certManager            = true
    monitoring             = true
    ingress_controllers    = true
    # Logic: Only enable HA features in 'live'
    high_availability      = local.environment == "live" ? true : false
  }

  # 5. Generate Tags Automatically
  common_tags = {
    Application = upper("${local.name}-DP")
    ManagedBy   = "Terraform"
    Environment = local.environment
    CostCenter  = local.name
  }
}
```

Would you like me to proceed with generating the code for `locals.tf` and the simplified `customer.yaml` based on this plan?

---

I want a llm prompt with full context for my coding assistant in antigravity (Gemini). It can read and write to the files as well as see the dependencies

---

Here is a comprehensive prompt you can paste directly into your coding assistant. It includes the context of your files, the specific architectural goals, and the "Convention over Configuration" strategy we developed.

---

### Prompt for Coding Assistant

Role: You are a Principal DevOps Engineer and Terraform Expert specializing in Azure and "Convention over Configuration" patterns.

Context: I am refactoring a Terraform project (`LCA-DP`) that deploys a customer environment. Currently, the configuration is brittle and relies on a complex `config/customer.yaml` file where humans manually define implementation details (like VNet names, CIDRs, and specific feature flags).

Goal:We are moving to a "Derived Configuration" model. The human should only provide the "Identity" of the customer, and the Terraform logic (`locals.tf`) should deterministically calculate the "Implementation" details.

The Strategy:

1. Minimize Input: Reduce `customer.yaml` from ~50 lines to ~5 lines (Identity only).
2. Maximize Logic: Move all naming conventions, network calculations, and feature toggles into `locals.tf`.
3. Standardize: Enforce strict naming conventions and network sizing (based on an integer ID) to remove human error.

Current File State:

- `LCA-DP/config/customer.yaml`: Currently contains mixed identity and implementation data.
- `LCA-DP/locals.tf`: Currently just reads the YAML and passes it through.
- `LCA-DP/main.tf`: Consumes these locals.
- `LCA-DP/values_generator.tf`: Exports these locals for external scripts (must remain compatible or be updated).

Task Checklist:

1\. Refactor `LCA-DP/config/customer.yaml` Replace the entire file content with _only_ these fields:

2\. Rewrite `LCA-DP/locals.tf` Update `locals.tf` to implement the following logic based on the _new_ minimal YAML:

- Network Calculation:
	- Derive `vnet_address_space` from the `id`. Formula: `10.{id}.0.0/16`.
	- Keep existing `cidrsubnet` logic for subnets, but ensure they use this new calculated base.
- Naming Conventions (Hardcoded):
	- `vnet_name` MUST be: `vnet-{name}-plat-{region}-01`
	- `resource_group_name` MUST be: `rg-{name}-{region}-{env_prefix}-net` (Note: derive `env_prefix` from `env`. If `live` -> `prd`, if `dev` -> `dev`).
- Feature Profiles (T-Shirt Sizing):
	- Create a `standard_deployment` map in locals.
	- If `env == "live"`, enable production features (monitoring, high\_availability, persistence).
	- If `env == "dev"`, disable expensive features.
	- _Self-Correction:_ Ensure `deploy` object in `locals` matches the structure expected by `main.tf`.

3\. Update `LCA-DP/values_generator.tf`

- Ensure the `infra_facts` output still produces the necessary data for external scripts, even though the source input has changed. Map the new calculated locals to the expected keys.

Constraint Checklist & Confidence Score:

1. Use British English for all comments/docs.
2. Do NOT delete `customer.yaml` (keep the file, just change content).
3. Ensure `vnet_cidr` calculation is robust.
4. Do not hallucinate external modules; strictly use the existing codebase context.

Action:Please analyse the dependencies between `locals.tf` and `main.tf`, then execute the changes described above to `customer.yaml` and `locals.tf`. Show me the diffs before applying if possible.

---

\## SYSTEM ROLE: Principal Site Reliability Engineer (Infrastructure-as-Code Specialist)

You are an expert in GitOps, Declarative Infrastructure, and System Bootstrapping. You specialize in converting manual, error-prone sysadmin tasks into idempotent, data-driven automation. Your primary tools are Terraform/OpenTofu, Helm, and the native APIs of HCP Vault and Grafana.

\## THE USER CONTEXT

The user is a DevOps Engineer migrating from an "Imperative/Manual" workflow to a "Data-Centric/Declarative" workflow. They are managing a Kubernetes-based cluster environment. They have "Contextual Baggage" from manual configurations in Grafana and HCP Vault and need to eliminate human error through schema-driven generation.

\## PEDAGOGICAL/OPERATIONAL CONSTRAINTS

1\. \*\*Declarative Supremacy\*\*: Every suggestion must be driven by a central configuration file (YAML/JSON). Do not suggest "clicking" or "one-off CLI commands."

2\. \*\*Idempotency Check\*\*: Before providing code, verify if the resource can be re-applied without destroying state.

3\. \*\*Schema Validation\*\*: You must insist on a defined schema for the "input data." If the user provides messy data, your first task is to propose a structured YAML schema that covers Providers, Auth, and Observability.

4\. \*\*Provider Mapping\*\*: Map "Config Keys" directly to "Resource Arguments" (e.g., \`config.vault.seal\_type\` -> \`vault\_generic\_secret\`).

\## IMMEDIATE GOAL

Analyze the user's current 'manual steps' for Grafana and HCP Vault. Design a unified Configuration Manifest schema and the corresponding Terraform/Logic blocks to automate the instantiation of these services based on that manifest.

---

Here is the fully contextualised prompt you requested. You can paste this directly into your coding assistant. It contains the architectural context, the specific file contents, and the transformation logic required.

---

### Prompt for Coding Assistant

Role: You are a Principal DevOps Engineer and Terraform Expert specializing in "Convention over Configuration" refactoring. You are working on the `LCA-DP` project.

Objective:Refactor the Terraform configuration to move from an "Explicit Configuration" model (where humans define every value in YAML) to a "Derived Configuration" model (where humans define Identity, and Terraform calculates Implementation).

Context & Constraints:

1. Source of Truth: The `LCA-DP/config/customer.yaml` file is currently too complex (40+ lines). We must strip it down to 5 specific "Identity" fields.
2. Logic Engine: The `LCA-DP/locals.tf` file must become the calculation engine. It will take the simple Identity fields and derive all naming conventions, network CIDRs, and feature flags.
3. Gold Master Rules:
	- Naming: Resources must follow: `vnet-{short_name}-plat-{region}-01` and `rg-{short_name}-{region}-{env_prefix}-net`.
	- Networking: The VNet CIDR must be calculated mathematically using a customer `id`. Formula: `10.{id}.0.0/16`.
	- British English: Use British English for all comments and documentation.
4. Compatibility: The `LCA-DP/values_generator.tf` file relies on specific locals existing (like `deploy`, `node_placement`). The new `locals.tf` must generate these defaults so the generator doesn't break.

---

### Current File Context

1\. `LCA-DP/config/customer.yaml` (Target for Reduction) _Current State:_ Contains `vnet_address_space`, `deploy` flags, `pki_issuer`, etc._Target State:_ Must ONLY contain:

2\. `LCA-DP/locals.tf` (Target for Expansion) _Current State:_ Reads YAML directly._Target Logic to Implement:_

- `env_prefix`: If `env == "live"` then "prd", else "dev".
- `vnet_cidr`: `10.{id}.0.0/16`.
- `subnets`: Keep existing `cidrsubnet` logic but apply to the new `vnet_cidr`.
- `deploy` (Feature Flags): Create a `standard_deployment` map. If `env == "live"`, enable high availability features (monitoring, persistence).
- `node_placement`: Hardcode standard Azure spot/workflow tolerations here instead of reading from YAML.

---

### Task Checklist

Please execute the following changes:

Step 1: Refactor `LCA-DP/config/customer.yaml`

- Wipe the current content.
- Replace it with the 5 "Identity" fields listed above (Name, Full Name, Env, Region, ID).

Step 2: Rewrite `LCA-DP/locals.tf`

- Imports: Load the new minimal YAML.
- Calculations:
	- Calculate `vnet_address_space` using the `id` from YAML.
	- Calculate `env_prefix` based on `env`.
	- Hardcode the `vnet_name` and `resource_group_name` patterns (do not allow overrides).
- Defaults (The "Hidden" Configuration):
	- Define the `deploy` map with logic: `high_availability = local.environment == "live"`.
	- Define `ffcloud_service_accounts` and `fitconnect_hosts` as empty lists `[]` (default).
	- Define `pki_issuer` with `enabled = false` (default).
	- Define `s3_export` with `enabled = true` (default).
	- Define `node_placement` with the standard Azure workflow tolerations.
- Tagging: Ensure `common_tags` includes `ManagedBy = "Terraform"` and `Environment = local.environment`.

Step 3: Verification

- Ensure that `local.infra_facts` in `values_generator.tf` will still resolve successfully (i.e., ensure all referenced locals exist in your new `locals.tf`).

Output:Please show me the code for the new `customer.yaml` and the completely rewritten `locals.tf`.
