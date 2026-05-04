## Raw Output / Content

You

I have 2 yaml configuration files. Common.yaml and override.yaml. I need to deep merge then so that override is the final say. What is the easiest way to do this in gitops terraform

---

Claude

Since you're already on Terragrunt, you have a native `deep_merge()`—no external modules needed.

## Terragrunt (simplest, given Your stack)

```hcl
# terragrunt.hcl
locals {
  common   = yamldecode(file("${get_terragrunt_dir()}/common.yaml"))
  override = yamldecode(file("${get_terragrunt_dir()}/override.yaml"))
  config   = deep_merge(local.common, local.override)
}

inputs = {
  config = local.config
}
```

`deep_merge` recursively merges maps—override wins on conflicts at every nesting level. Lists are replaced, not appended (this is almost always what you want in GitOps, but worth knowing).

## Pure Terraform (if You Need it in a module)

Terraform has no native deep merge. The lightest option is the `Invicton-Labs/deepmerge/null` module:

```hcl
module "config" {
  source  = "Invicton-Labs/deepmerge/null"
  version = "0.2.0"

  maps = [
    yamldecode(file("${path.module}/common.yaml")),
    yamldecode(file("${path.module}/override.yaml")),
  ]
}

# Access via: module.config.merged
```

## Why Terragrunt's Approach is Better here

The Terragrunt `deep_merge()` runs at the HCL evaluation layer *before* Terraform even sees the values, so you can use the merged result directly in `inputs` without adding a module dependency. It also means `terraform plan` sees a flat, already-resolved map—easier to debug drift.

Next action: If this is for a specific cluster config (e.g. `mkuh-prd-4`), drop the two YAML filenames and I'll sketch the exact `terragrunt.hcl` locals block for your layout.