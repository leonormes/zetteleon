---
created: 2026-02-24T16:27:53+00:00
modified: 2026-03-14T11:10:51+00:00
title: lca-prd-2-credential-flow
---

```d2
direction: down

hcp_vault: HCP Vault Cloud {
  style.fill: "#f0f4ff"

  admin: "admin/ namespace" {
    style.fill: "#e8eef8"

    auth: "auth/jwt-lca-prd-2" {
      style.fill: "#fff3cd"
      role: |text
        role: lca-prd-2
        method: jwt
        bound_sa: system:serviceaccount:*:default
      |
    }

    policies: Policies {
      style.fill: "#fff3cd"
      p1: "argocd-secrets-lca-prd-2\n→ deployments/lca-prd-2/secrets/data/* (read, list)"
      p2: "acr-reader\n→ central/azure/creds/acr-pull (read)"
      p3: "gitlab-reader\n→ central/gitlab/data/token (read)"
    }

    central: "central/ namespace" {
      style.fill: "#d4edda"

      azure_mount: "azure/ (dynamic)" {
        style.fill: "#c3e6cb"
        acr_creds: "creds/acr-pull\n→ client_id, client_secret"
      }

      gitlab_mount: "gitlab/ (kv-v2)" {
        style.fill: "#c3e6cb"
        token: "token\n→ value (glpat-...)\n→ scopes: read_api, read_repository\n→ expires: 2027-01-25"
      }
    }

    deployments: "deployments/lca-prd-2/ namespace" {
      style.fill: "#d4edda"

      secrets_mount: "secrets/ (kv-v2)" {
        style.fill: "#c3e6cb"
        argocd_path: "argocd\n→ admin_password\n→ server_secret_key\n→ gitlab_deploy_token_username\n→ gitlab_deploy_token_password"
      }
    }

    auth -> policies: grants
  }
}

k8s: "Kubernetes Cluster (lca-prd-2)" {
  style.fill: "#fff5f5"

  vso: "Vault Secrets Operator\n(ns: vault-secrets-operator-system)" {
    style.fill: "#fde8e8"
  }

  argocd_ns: "argocd namespace" {
    style.fill: "#fde8e8"

    vault_auth: "VaultAuth: default\nmethod: jwt | mount: jwt-lca-prd-2 | ns: admin" {
      style.fill: "#fff3cd"
    }

    vss_group: VaultStaticSecrets {
      style.fill: "#d4edda"

      argocd_secret_crd: "argocd-secret\nmount: secrets | path: argocd\nns: admin/deployments/lca-prd-2" {
        style.fill: "#c3e6cb"
      }

      group_creds_crd: "argocd-group-creds\nmount: gitlab | path: token\nns: admin/central" {
        style.fill: "#c3e6cb"
      }

      repo_deploy_crd: "argocd-repo-fitfile-deployment-repo\nmount: secrets | path: argocd\nns: admin/deployments/lca-prd-2" {
        style.fill: "#c3e6cb"
      }
    }

    vds_group: VaultDynamicSecrets {
      style.fill: "#cce5ff"

      acr_repo_crd: "argocd-repo-creds-acr\nmount: azure | path: creds/acr-pull\nns: admin/central" {
        style.fill: "#b8daff"
      }

      img_pull_crd: "fitfile-image-pull-secret\nmount: azure | path: creds/acr-pull\nns: admin/central" {
        style.fill: "#b8daff"
      }
    }

    secrets_group: "K8s Secrets (produced)" {
      style.fill: "#f8f9fa"

      argocd_secret_k8s: "argocd-secret\nadmin.password | admin.passwordMtime | server.secretkey" {
        style.fill: "#ffffff"
      }

      group_creds_k8s: "argocd-group-creds\nlabel: repo-creds\nurl: https://gitlab.com/fitfile\nusername: oauth2 | password: glpat-..." {
        style.fill: "#ffffff"
        style.stroke: "#28a745"
      }

      repo_deploy_k8s: "argocd-repo-fitfile-deployment-repo\nlabel: repository\nurl: .../fitfile/deployment.git\nusername: argocd-test | password: (deploy token)" {
        style.fill: "#ffffff"
        style.stroke: "#28a745"
      }

      acr_repo_k8s: "argocd-repo-creds-acr\nlabel: repository\nurl: https://fitfileregistry.azurecr.io\nusername: (SP client_id) | password: (SP secret)" {
        style.fill: "#ffffff"
        style.stroke: "#007bff"
      }

      img_pull_k8s: "fitfile-image-pull-secret\ntype: dockerconfigjson\nregistry: fitfileregistry.azurecr.io" {
        style.fill: "#ffffff"
        style.stroke: "#007bff"
      }
    }

    argocd_app: "ArgoCD Application: ff-lca-prd-2" {
      style.fill: "#ffe0b2"

      source1: "Source 1 (charts)\nhttps://gitlab.com/fitfile/deployment.git" {
        style.fill: "#fff3e0"
      }

      source2: "Source 2 (values) — BLOCKED\nhttps://gitlab.com/fitfile/customers/nwsde/lca-infra-prd.git\nToken lacks access to customers/nwsde subgroup" {
        style.fill: "#fff3e0"
        style.stroke: "#dc3545"
        style.stroke-width: 2
      }
    }
  }
}

# --- Auth Flow ---
k8s.vso -> hcp_vault.admin.auth: "JWT (OIDC from AKS)" {
  style.stroke: "#6c757d"
  style.stroke-dash: 3
}

# --- VaultAuth References ---
k8s.argocd_ns.vss_group -> k8s.argocd_ns.vault_auth: "vaultAuthRef: default" {
  style.stroke: "#6c757d"
  style.stroke-dash: 3
}
k8s.argocd_ns.vds_group -> k8s.argocd_ns.vault_auth: "vaultAuthRef: default" {
  style.stroke: "#6c757d"
  style.stroke-dash: 3
}

# --- Vault Reads ---
k8s.argocd_ns.vss_group.argocd_secret_crd -> hcp_vault.admin.deployments.secrets_mount.argocd_path: reads {
  style.stroke: "#28a745"
}
k8s.argocd_ns.vss_group.group_creds_crd -> hcp_vault.admin.central.gitlab_mount.token: reads {
  style.stroke: "#28a745"
}
k8s.argocd_ns.vss_group.repo_deploy_crd -> hcp_vault.admin.deployments.secrets_mount.argocd_path: reads {
  style.stroke: "#28a745"
}
k8s.argocd_ns.vds_group.acr_repo_crd -> hcp_vault.admin.central.azure_mount.acr_creds: generates {
  style.stroke: "#007bff"
}
k8s.argocd_ns.vds_group.img_pull_crd -> hcp_vault.admin.central.azure_mount.acr_creds: generates {
  style.stroke: "#007bff"
}

# --- Secret Production ---
k8s.argocd_ns.vss_group.argocd_secret_crd -> k8s.argocd_ns.secrets_group.argocd_secret_k8s: syncs {
  style.stroke: "#6c757d"
}
k8s.argocd_ns.vss_group.group_creds_crd -> k8s.argocd_ns.secrets_group.group_creds_k8s: syncs {
  style.stroke: "#6c757d"
}
k8s.argocd_ns.vss_group.repo_deploy_crd -> k8s.argocd_ns.secrets_group.repo_deploy_k8s: syncs {
  style.stroke: "#6c757d"
}
k8s.argocd_ns.vds_group.acr_repo_crd -> k8s.argocd_ns.secrets_group.acr_repo_k8s: syncs {
  style.stroke: "#6c757d"
}
k8s.argocd_ns.vds_group.img_pull_crd -> k8s.argocd_ns.secrets_group.img_pull_k8s: syncs {
  style.stroke: "#6c757d"
}

# --- ArgoCD Credential Matching ---
k8s.argocd_ns.argocd_app.source1 -> k8s.argocd_ns.secrets_group.repo_deploy_k8s: "exact match (priority 1) ✅" {
  style.stroke: "#28a745"
  style.stroke-width: 2
}
k8s.argocd_ns.argocd_app.source2 -> k8s.argocd_ns.secrets_group.group_creds_k8s: "prefix match (priority 2) ❌" {
  style.stroke: "#dc3545"
  style.stroke-width: 2
  style.stroke-dash: 5
}
```
