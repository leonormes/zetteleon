---
aliases: []
confidence: 
created: 2025-08-28T11:46:46Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T14:24:10Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [charts, dependency-management, helm, modules, versioning]
title: Create a Central Version Catalog Module
type:
uid: 
updated: 
version:
---

## Option 1: Create a Central Version Catalog Module (Recommended)

This approach involves creating a new, dedicated Terraform module whose only purpose is to define and output the chart versions. This module acts as a "version catalog" that your other configurations can reference.

### How it Works

1. **Create a New Module**: You would create a new, simple module (e.g., in a new Git repo called `terraform-version-catalog`).

- [outputs.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/TFC-Modules/terraform-helm-fitfile-platform/outputs.tf:0:0-0:0): This file defines all the chart versions.

```hcl
output "helm_chart_versions" {
  description = "A map of approved Helm chart versions for platform components."
  value = {
    ingress_nginx      = "4.11.2"
    argocd             = "7.7.5"
    argocd_apps        = "1.4.1"
    vault_operator     = "0.10.0" # <-- Update here
    reflector          = "7.1.288"
    cluster_autoscaler = "9.43.0"
  }
}

output "helm_repository_url" {
  description = "The OCI URL for the Helm chart repository."
  value       = "oci://fitfilepublic.azurecr.io"
}
```

2. **Publish the Module**: Publish this module to your private Terraform Cloud registry.
3. **Consume the Module**: In each of your deployment configurations (both the one on Terraform Cloud and the one on the jumpbox), you would call this new module to get the versions.

```hcl
# In your private_platform_template/main.tf (and other configs)

# 1. Fetch the versions from the central catalog module
module "version_catalog" {
source  = "app.terraform.io/FITFILE-Platforms/version-catalog/helm"
version = "1.0.0" # Version of the catalog itself
}

# 2. Pass the versions to your platform module
module "platform" {
source  = "app.terraform.io/FITFILE-Platforms/fitfile-platform/helm"
version = "2.0.0"

# ... other required parameters

# Pass versions from the catalog
vault_operator_chart_version = module.version_catalog.helm_chart_versions.vault_operator
ingress_nginx_chart_version  = module.version_catalog.helm_chart_versions.ingress_nginx
argocd_chart_version         = module.version_catalog.helm_chart_versions.argocd
# ... and so on for all charts

helm_repository_url = module.version_catalog.helm_repository_url
}
```

### Why This is the Best Approach

- **Single Source of Truth**: You update versions in exactly one place.
- **Versioning**: The catalog module itself is versioned, giving you excellent control over rollouts. You can test a new set of chart versions by just updating the `version` of the `version_catalog` module in a dev environment.
- **Terraform Native**: It uses standard Terraform module composition, which is clean and easy to understand.
  That's an excellent and crucial question. You are correct. Even with the central version catalog module, you would still need to update the module's `version` attribute in each of your deployment configurations to pull in the changes.

However, this is a deliberate and powerful feature, not a drawback. It gives you **controlled rollouts**. You don't want every cluster to update automatically the moment you publish a new version, as that could be risky.

The process gives you a clear, safe, and automatable workflow:

1. **Central Change**: You update a chart version in the `version-catalog` module and publish a new version of it (e.g., from `1.0.0` to `1.1.0`). This is your single point of change.
2. **Controlled Rollout**: You then decide *when* to roll out this new set of versions to each cluster by updating the module version in that cluster's Terraform configuration.

```hcl
# In Dev Cluster's Terraform code
module "version_catalog" {
source  = "app.terraform.io/FITFILE-Platforms/version-catalog/helm"
version = "1.1.0" // Update dev first to test the new versions
}

# In Prod Cluster's Terraform code
module "version_catalog" {
source  = "app.terraform.io/FITFILE-Platforms/version-catalog/helm"
version = "1.0.0" // Production stays on the old, stable version for now
}
```

### How to Automate the "Manual" Update

The key is to automate the process of updating the `version` attribute across all your deployment repositories. The industry-standard solution for this is to use a dependency update bot like **Renovate** or **GitHub's Dependabot**.

Here’s how it works with Renovate:

1. **Configure Renovate**: You add a `renovate.json` configuration file to each of your deployment repositories (the ones on TFC, the one for the jumpbox, etc.).
2. **Detect New Versions**: You configure Renovate to monitor your private Terraform Cloud registry.
3. **Create Pull Requests**: When you publish a new version of your `version-catalog` module (e.g., `v1.1.0`), Renovate will automatically open a pull request in every single consuming repository. The PR will propose changing `version = "1.0.0"` to `version = "1.1.0"`.
4. **Review and Merge**: Your team can then review, approve, and merge these PRs to trigger the `terraform apply` for each environment. You can even configure Renovate to auto-merge for non-production environments.

This workflow gives you the best of both worlds:

- **Centralization**: You change the version number in only one place (the catalog module).
- **Automation**: The process of propagating that change is handled automatically by a bot.
- **Control**: You retain full control over *when* each environment gets updated by managing the pull requests.

You've perfectly described a classic infrastructure management challenge. The goal is to bridge the gap between your automated Terraform Cloud (TFC) workflows and the manual, air-gapped workflows on your jumpboxes.

The solution has two parts:

1. **Centralize the Version**: Create a single source of truth for the module version.
2. **Centralize the Execution**: Trigger the `terraform apply` on all jumpboxes from one place, without manual SSH.

I recommend using a combination of **Terraform Remote State** for centralization and **Ansible** for remote execution. This is a robust, industry-standard pattern.

### The Solution: Terraform Remote State + Ansible

Here’s the step-by-step plan:

#### Step 1: Create a Central Version Manager in TFC

First, we'll create a dedicated TFC workspace to act as the single source of truth for your module versions.

1. **Create a new Git repository** (e.g., `fitfile-version-manager`).
2. **Add a `versions.tf` file** to this new repository:

```hcl
# versions.tf

terraform {
cloud {
organization = "FITFILE-Platforms"
workspaces {
  name = "global-version-manager"
}
}
}

# Define the version you want all deployments to use.
# To update all clusters, you only change this value and apply.
output "platform_module_version" {
description = "The version of the fitfile-platform module to be used by all deployments."
value       = "2.0.0" # <-- SINGLE SOURCE OF TRUTH
}
```

3. **Create a new TFC workspace** named `global-version-manager` linked to this repository. Run `terraform apply` once to initialize the state.

#### Step 2: Update Your Deployments to Read from Central State

Now, modify the Terraform code used by **both TFC and the jumpboxes** to read the version from this new central state.

- In your `private_platform_template` and other deployment configurations, add this data source:

```hcl
# Add this to your main.tf or a new data.tf file

data "terraform_remote_state" "versions" {
backend = "remote"

config = {
organization = "FITFILE-Platforms"
workspaces = {
  name = "global-version-manager"
}
}
}

# Update your module block to use the version from the data source
module "platform" {
source  = "app.terraform.io/FITFILE-Platforms/fitfile-platform/helm"
# The version is now read dynamically from your central manager
version = data.terraform_remote_state.versions.outputs.platform_module_version

# ... other variables
}
```

With this change, any `terraform plan` or `apply` will automatically use the version defined in the `global-version-manager` workspace.

#### Step 3: Use Ansible to Automate Jumpbox Execution

This is the key to eliminating manual SSH. We'll use Ansible to run `terraform apply` on all jumpboxes in parallel.

1. **Set up a Control Node**: Designate a machine (your local laptop, a CI runner, or a "master" jumpbox) where you will install Ansible.
2. **Create an Ansible Inventory File** (`inventory.ini`): This file lists all your jumpbox hostnames.

```ini
# inventory.ini

[jumpboxes]
jumpbox-prod-1.fitfile.net
jumpbox-prod-2.fitfile.net
jumpbox-staging-1.fitfile.net
```

3. **Create an Ansible Playbook** (`run_terraform.yml`): This playbook defines the tasks to run on each jumpbox.

```yaml
# run_terraform.yml

- name: Update Terraform Deployments on Jumpboxes
hosts: jumpboxes
become: no # Assumes you run as a user with correct permissions

tasks:
- name: Change to the Terraform directory
  ansible.builtin.command:
    chdir: /path/to/your/terraform/code # e.g., /srv/terraform/private_platform_template
    cmd: git pull # Ensure the code is up-to-date

- name: Run Terraform Apply
  ansible.builtin.command:
    chdir: /path/to/your/terraform/code
    # The -auto-approve flag is crucial for automation
    cmd: terraform apply -auto-approve -var-file=vars.tfvars
  register: tf_apply

- name: Show Terraform output
  ansible.builtin.debug:
    var: tf_apply.stdout_lines
```

### The New Workflow

Now, when you want to update all your clusters to a new version:

1. **Update the Source of Truth**: Go to your `fitfile-version-manager` Git repo, change the `platform_module_version` output in `versions.tf` to `"2.1.0"`, and push. TFC will automatically apply this change in the `global-version-manager` workspace.
2. **Trigger the Rollout**: From your Ansible control node, run a single command:

```bash
ansible-playbook -i inventory.ini run_terraform.yml
```

Ansible will securely connect to every jumpbox listed in your inventory and run the `git pull` and `terraform apply` commands for you. Because the Terraform code now reads its version from the remote state, it will automatically pick up the new version (`2.1.0`) and upgrade the deployment.

This approach gives you exactly what you asked for: a central place to manage the version and a single command to update all your manual deployments.
