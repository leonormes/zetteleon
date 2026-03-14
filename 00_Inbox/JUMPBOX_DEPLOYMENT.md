---
created: 2026-02-23T17:04:39+00:00
modified: 2026-03-14T11:10:54+00:00
title: JUMPBOX_DEPLOYMENT
---

## Jumpbox Main.tf Configuration

This file should be generated and deployed to the jumpbox VM. The template in `jumpbox_main.tftpl` is already configured for Kubernetes authentication.

### Generate the Configuration

From your local machine in the LCA-DP directory:

```bash
cd /Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/Clusters/nwsde/Production/LCA-DP

# Generate the jumpbox main.tf
terraform output -raw jumpbox_main_content > /tmp/jumpbox_main.tf

# View the generated file
cat /tmp/jumpbox_main.tf
```

### Key Configuration Points

The generated `main.tf` will contain:

#### 1. No AppRole Credentials

```hcl
locals {
  # Empty - using Kubernetes auth
  app_role_secrets_map = {}
}
```

#### 2. Kubernetes VaultAuth

```hcl
resource "kubernetes_manifest" "vault_auth" {
  manifest = {
    apiVersion = "secrets.hashicorp.com/v1beta1"
    kind       = "VaultAuth"
    metadata = {
      name      = "default"
      namespace = "lca-prd-2"
    }
    spec = {
      method = "kubernetes"
      mount  = "lca-prd-2"
      kubernetes = {
        role           = "lca-prd-2"
        serviceAccount = "default"
        audiences      = ["https://kubernetes.default.svc.cluster.local"]
      }
    }
  }
}
```

#### 3. Platform Module (No AppRole Map)

```hcl
module "platform" {
  source  = "app.terraform.io/FITFILE-Platforms/fitfile-platform/helm"
  version = "2.2.15"
  
  # ... other config ...
  
  app_role_secrets_map = {}  # Empty for Kubernetes auth
  use_image_pull_secret = true
}
```

### Deploy to Jumpbox

1. Copy to jumpbox:

   ```bash
   scp /tmp/jumpbox_main.tf user@jumpbox:~/terraform/main.tf
   ```

2. On the jumpbox, apply:

   ```bash
   cd ~/terraform
   
   # Remove old AppRole VaultAuth
   kubectl delete vaultauth default -n argocd
   
   # Apply new configuration
   terraform init
   terraform apply
   ```

3. Verify:

   ```bash
   kubectl describe vaultauth default -n argocd
   kubectl describe vaultdynamicsecret fitfile-image-pull -n argocd  
   kubectl get secret fitfile-image-pull-secret -n argocd
   ```

### What This Creates

- VaultAuth in `argocd` namespace using Kubernetes auth
- Platform module deployment (ArgoCD, Ingress, VSO, Reflector)
- VaultDynamicSecret for image pull secret (created by platform module)
- All secrets accessible via Kubernetes auth (no AppRole credentials needed)
