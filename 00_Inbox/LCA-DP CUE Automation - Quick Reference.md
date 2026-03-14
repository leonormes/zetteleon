---
created: 2026-03-07T13:51:58+00:00
modified: 2026-03-14T09:59:05+00:00
title: LCA-DP CUE Automation - Quick Reference
---

## Daily Workflow

### 1. Make Changes to Customer Config

```bash
vim config/customer.yaml
```

### 2. Apply Terraform Changes

```bash
terraform apply
```

### 3. Regenerate Helm Values (Automated!)

```bash
make generate-values
```

That's it! The script automatically:

- ✅ Extracts `infra_facts` from Terraform
- ✅ Validates the data structure
- ✅ Passes it to CUE
- ✅ Generates `generated/values.yaml`

## Common Commands

| Command | Purpose |
|---------|---------|
| `make help` | Show all available targets |
| `make generate-values` | Generate Helm values from CUE + Terraform |
| `make validate-cue` | Validate CUE config without generating |
| `./generate-values.sh` | Run generation script directly |

## Before/After Comparison

### ❌ Old Manual Way (Error-Prone)

```bash
# Had to manually construct JSON with customer details
cue export ./templates/values.cue \
    -t infra='{"customer_short_name":"lca","deployment_key":"lca-prd-2",...}' \
    --out yaml > generated/values.yaml
```

Problems:

- Manual typing → typos and errors
- Hard to remember all fields
- Not DRY (data duplicated)

### ✅ New Automated Way

```bash
make generate-values
```

Benefits:

- Single command
- No manual input
- Data comes from `customer.yaml` via Terraform
- Type-safe with CUE validation
- Idempotent and reproducible

## Data Flow

```
customer.yaml
    ↓
locals.tf (processes config)
    ↓
values_generator.tf (creates infra_facts output)
    ↓
generate-values.sh (extracts output)
    ↓
templates/values.cue (applies schema + logic)
    ↓
generated/values.yaml (final output)
    ↓
ArgoCD (deploys)
```

## Troubleshooting

### "Could Not Retrieve infra_facts"

```bash
# Refresh Terraform state
terraform refresh
terraform apply
```

### CUE Validation Fails

```bash
# Check Terraform output format
terraform output -json infra_facts | jq

# Validate CUE schema
cue vet templates/values.cue
```

### Want to See what Data is Being Used?

```bash
# View the infrastructure facts
terraform output infra_facts

# Or as JSON
terraform output -json infra_facts | jq
```

## Pro Tips

1. Always validate before generating:

   ```bash
   make validate-cue && make generate-values
   ```

2. Review changes before committing:

   ```bash
   git diff generated/values.yaml
   ```

3. Automation is safe:
   - The script is idempotent (same input = same output)
   - Version controlled (changes are tracked in Git)
   - Reversible (just revert the commit)

## Need Help?

- Check the main [README.md](./README.md) for detailed documentation
- View CUE schema: `cat templates/values.cue`
- View Terraform outputs: `terraform output`
