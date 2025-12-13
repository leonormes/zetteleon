---
aliases: []
confidence: 
created: 2025-02-07T12:57:52Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:51Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [workstation]
title: Terraform CLI Wiki
type:
uid: 
updated: 
version:
---

## Renaming Resources

If you have state already managed by TF and you change to resource name TF treats it like a new resource as the path has changed. To avoid this, as it scarely destroys stuff, do some moving. If there is something already there you can rm it from state first. Here is an example

```sh
# First remove the duplicate state entry
terraform state rm 'tfe_workspace.staging_cluster_v2'

# Then move the state from staging-v2 to staging_cluster_v2
terraform state mv 'tfe_workspace.staging-v2' 'tfe_workspace.staging_cluster_v2'
```

## Using OP to Supply the Ssh-key

To reference your SSH public key stored in 1Password from a Terraform script, you can use the 1Password Terraform provider. Here's how you can set it up and retrieve the SSH public key:

### Setup

1. First, ensure you have the 1Password CLI installed on your macbook. The minimum required version is 2.23.0[3].
2. Add the 1Password provider to your Terraform configuration:

```hcl
terraform {
  required_providers {
    onepassword = {
      source  = "1Password/onepassword"
      version = "~> 1.1.4"
    }
  }
}

provider "onepassword" {
  account = "<your_account_id>"
}
```

Replace `<your_account_id>` with your 1Password account ID or sign-in address[3].

### Retrieving the SSH Public Key

To retrieve the SSH public key, use the `onepassword_item` data source:

```hcl
data "onepassword_item" "ssh_key" {
  vault = "<your_vault_id>"
  uuid  = "<your_ssh_key_item_uuid>"
}
```

Replace `<your_vault_id>` with the ID of the vault containing your SSH key, and `<your_ssh_key_item_uuid>` with the UUID of the SSH key item[4][5].

### Using the Public Key

You can now reference the public key in your Terraform resources. For example:

```hcl
resource "some_resource" "example" {
  # ... other configuration ...
  public_key = data.onepassword_item.ssh_key.public_key
}
```

### Important Notes

1. The `onepassword_item` data source will retrieve the entire SSH key item, including both the public and private keys. However, only use the public key in your Terraform configuration to maintain security[4].
2. Ensure you have the necessary permissions to access the vault and the specific item in 1Password.
3. When running Terraform commands, you may need to authenticate with 1Password using biometric unlock or your account password[3].
4. If you're using this in a CI/CD environment, consider using a 1Password service account for authentication instead of your personal account[6].
