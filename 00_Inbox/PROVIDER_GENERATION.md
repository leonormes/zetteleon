---
created: 2026-02-23T17:04:39+00:00
modified: 2026-03-14T11:10:52+00:00
title: PROVIDER_GENERATION
---

## Provider Configuration Generation

### Overview

The `providers.tf` file contains the Terraform Cloud backend configuration with the workspace name. Since Terraform doesn't support variable interpolation in the `terraform {}` block, we generate this file from a template.

### How It Works

1. Template: `templates/providers.tftpl` contains the provider configuration with a `${deployment_key}` placeholder
2. Generator: `providers_generator.tf` processes the template and generates the file
3. Output: The generated file is written to `generated/providers.tf`

### Workflow for New Customer Deployments

#### Initial Setup

1. Edit `config/customer.yaml` with customer-specific values
2. Run Terraform to generate the providers file:

   ```bash
   terraform init -backend=false
   terraform apply -target=local_file.providers
   ```

3. Copy the generated file to the root:

   ```bash
   cp generated/providers.tf providers.tf
   ```

4. Now run the full Terraform workflow:

   ```bash
   terraform init
   terraform plan
   terraform apply
   ```

#### Why This Approach?

The Terraform Cloud backend configuration must be present before `terraform init` runs, but it cannot contain variable interpolations. This chicken-and-egg problem is solved by:

1. Using `-backend=false` for the initial run to generate the file
2. Copying the generated file to where Terraform expects it
3. Running normal Terraform operations with the correct workspace name

### Alternative Approaches

If you prefer not to use file generation, you can:

1. Use backend-config flags:

   ```bash
   terraform init -backend-config="workspaces.name=<deployment-key>"
   ```

2. Manual maintenance: Keep `providers.tf` in sync with `deployment_key` manually (not recommended for GitOps)
3. Environment-specific backends: Use separate backend configs per environment (doesn't scale well)

### Files

- `templates/providers.tftpl` - Template with placeholders
- `providers_generator.tf` - Generator logic
- `generated/providers.tf` - Generated output (gitignored)
- `providers.tf` - Active file used by Terraform (should match generated)
- `providers.tf.generated` - Original hardcoded file (kept as reference)

### Important Notes

- The `providers.tf` file in the root should match the workspace name in Terraform Cloud
- For existing deployments: Keep the existing `providers.tf` file. The workspace name is already correct ("lca-prd-2"). The generation workflow is for NEW customers only.
- For new deployments, verify the workspace name matches `deployment_key` from `customer.yaml`
- The generated file should be reviewed before copying to root to ensure correctness
