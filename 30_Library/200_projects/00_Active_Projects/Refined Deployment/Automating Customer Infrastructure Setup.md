---
aliases: []
confidence: 
created: 2025-09-21T08:46:05Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T14:24:10Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: Automating Customer Infrastructure Setup
type:
uid: 
updated: 
version:
---

## **Overall Goal:**

You are an expert DevOps engineer. Your task is to refactor our existing Terraform codebase in the `central-services/` directory and create a `Makefile` to automate the entire process of onboarding a new customer. The goal is to create a system where a developer can run a single command, like `make apply CUSTOMER_NAME="new-customer-xyz"`, to provision all necessary resources (GitLab repos, TFC workspaces, etc.) for that specific customer without manual intervention.

**Key Constraints:**

- **No Hardcoded Secrets:** All credentials and tokens are managed as secrets within the HCP Terraform Cloud workspace environment. Your code should contain no default passwords, tokens, or secrets.
- **Parameterisation:** All customer-specific resources (project names, repository paths, workspace names) must be generated dynamically based on input variables.
- **Modularity:** The process should be broken down into logical, verifiable steps.

---

## **Phase 1: Parameterise the GitLab Configuration**

**Context:** The Terraform files in `central-services/gitlab/` currently define specific, hardcoded GitLab projects. We need to modify this to create a generic, reusable module that can provision a standard set of repositories for any new customer.

**Your Task:**

1. **Create a `customer_name` Variable:** In `central-services/gitlab/variables.tf`, add a new variable:

   Terraform

```sh
variable "customer_name" {
 type        = string
 description = "The unique identifier for the customer, used to name and tag resources."
}
```

2. **Refactor `gitlab_project` Resources:** Go through `central-services/gitlab/main.tf` and `central-services/gitlab/projects_customers.tf`. Replace all hardcoded `name` and `path` attributes for customer-specific projects with dynamic values derived from `var.customer_name`.
   - **Example (Before):**

     Terraform

     ```sh
     resource "gitlab_project" "uhb_prod" {
       name             = "uhb_wmsde_prod"
       path             = "uhb-wmsde-prod"
       # ...
     }
     ```

   - **Example (After):**

     Terraform

     ```sh
     # This resource will create a production repository for the new customer.
     resource "gitlab_project" "customer_prod" {
       name             = "${var.customer_name}-prod-repo"
       path             = "${var.customer_name}-prod-repo"
       namespace_id     = data.gitlab_group.customer.id
       description      = "Production infrastructure for ${var.customer_name}"
       # ... other settings
     }
     ```

3. **Remove Hardcoded Tokens:** In `central-services/gitlab/variables.tf`, find the `GITLAB_TOKEN` variable and completely remove the `default` value. The variable definition should only be:

   Terraform

   ```sh
   variable "GITLAB_TOKEN" {
     type      = string
     sensitive = true
   }
   ```

**Validation for Phase 1:**

- After your changes, running `terraform plan -var="customer_name=test-customer"` within the `central-services/gitlab/` directory should show a plan to create new GitLab projects named `test-customer-prod-repo` (and others), not the old hardcoded names like `uhb_wmsde_prod`.

---

## **Phase 2: Parameterise the HCP Terraform Cloud Configuration**

**Context:** The files in `central-services/hcp/tfc/` define TFC projects and workspaces. This needs to be adapted to automatically create a dedicated workspace for each new customer's GitLab repository.

**Your Task:**

1. **Add a `customer_name` Variable:** In `central-services/hcp/tfc/variables.tf`, add the same `customer_name` variable as in the GitLab section.
2. **Create a Dynamic Workspace Resource:** Add a new `tfe_workspace` resource in a file like `ws-customer.tf`. This workspace should be configured to connect to the GitLab repository you made dynamic in Phase 1.

   Terraform

   ```sh
   resource "tfe_workspace" "customer_workspace" {
     name         = "${var.customer_name}-prod-workspace"
     organization = data.tfe_organization.org.name
     project_id   = tfe_project.fitfile_production.id // or a relevant project ID
     vcs_repo {
       identifier     = "path/to/${var.customer_name}-prod-repo" // Update with your GitLab group path
       oauth_token_id = var.gitlab_oauth_token_id // Assume this is configured in TFC
     }
   }
   ```

3. **Review Existing Workspaces:** Examine files like `ws-ff-prod.tf` and `ws-uhb-prod.tf`. Consolidate these into a single generic customer workspace resource as described above.

**Validation for Phase 2:**

- Running `terraform plan -var="customer_name=test-customer"` in the `central-services/hcp/tfc/` directory should show a plan to create a new TFC workspace named `test-customer-prod-workspace`.

---

## **Phase 3: Create the Orchestration `Makefile`**

**Context:** Now that the Terraform code is parameterised, we need a single, simple interface to execute it. A `Makefile` in the root `central-services/` directory is perfect for this.

Your Task:

Create a new file named Makefile in the central-services/ directory with the following content. This file will orchestrate the terraform commands across all the different service directories.

Makefile

```sh
# Makefile for automating the onboarding of a new FITFILE customer.

# --- Variables ---
# This is the main input. Pass it on the command line.
# Example: make plan CUSTOMER_NAME="new-customer-xyz"
CUSTOMER_NAME ?= "default-customer"

# Check if CUSTOMER_NAME is set to a non-default value for apply/destroy
ifeq ($(CUSTOMER_NAME), "default-customer")
  APPLY_GUARD = @echo "ERROR: You must provide a CUSTOMER_NAME for 'apply' and 'destroy'. Ex: make apply CUSTOMER_NAME=my-new-customer"; exit 1
else
  APPLY_GUARD = @echo "Proceeding with customer: $(CUSTOMER_NAME)"
endif

# --- Terraform Command ---
# Define Terraform variables to be passed to each command.
TF_VARS = -var="customer_name=$(CUSTOMER_NAME)"

.PHONY: all plan apply destroy clean

# --- Main Targets ---
all: apply

## plan: Generates an execution plan for all services for the specified customer.
plan: plan-gitlab plan-tfc

## apply: Creates all resources for the specified customer.
apply: $(APPLY_GUARD) apply-gitlab apply-tfc

## destroy: Destroys all resources for the specified customer.
destroy: $(APPLY_GUARD) destroy-gitlab destroy-tfc

# --- Service-Specific Targets ---

# GitLab
plan-gitlab:
 @echo "==> Planning GitLab resources for $(CUSTOMER_NAME)..."
 cd gitlab && terraform init && terraform plan $(TF_VARS)

apply-gitlab:
 @echo "==> Applying GitLab resources for $(CUSTOMER_NAME)..."
 cd gitlab && terraform init && terraform apply -auto-approve $(TF_VARS)

destroy-gitlab:
 @echo "==> Destroying GitLab resources for $(CUSTOMER_NAME)..."
 cd gitlab && terraform destroy -auto-approve $(TF_VARS)

# Terraform Cloud
plan-tfc:
 @echo "==> Planning TFC resources for $(CUSTOMER_NAME)..."
 cd hcp/tfc && terraform init && terraform plan $(TF_VARS)

apply-tfc:
 @echo "==> Applying TFC resources for $(CUSTOMER_NAME)..."
 cd hcp/tfc && terraform init && terraform apply -auto-approve $(TF_VARS)

destroy-tfc:
 @echo "==> Destroying TFC resources for $(CUSTOMER_NAME)..."
 cd hcp/tfc && terraform destroy -auto-approve $(TF_VARS)

# --- Utility Targets ---
## clean: Removes terraform state files and caches.
clean:
 @echo "Cleaning up Terraform files..."
 find . -type d -name ".terraform" -exec rm -rf {} +
 find . -type f -name ".terraform.lock.hcl" -delete
```

**Validation for Phase 3:**

- From the `central-services/` directory, run `make plan CUSTOMER_NAME="final-test"`. The command should execute successfully, initialising and planning both the `gitlab` and `hcp/tfc` modules and showing the resources to be created for the "final-test" customer.
- Run `make apply` without a customer name. It should fail with the error message defined in `APPLY_GUARD`.
