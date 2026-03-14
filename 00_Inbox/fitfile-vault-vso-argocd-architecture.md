---
created: 2026-03-13T19:00:12+00:00
modified: 2026-03-14T11:10:51+00:00
title: fitfile-vault-vso-argocd-architecture
---

graph TB

    subgraph HCP["HCP Vault Cloud"]

        direction TB

        VaultInstance["vault-public-vault-8b38a0c2\ne3dedc53.z1.hashicorp.cloud:8200"]

        subgraph VaultNS["Vault Namespace: admin/deployments/&lt;cluster&gt;"]
            direction TB
            KV["KV-v2 Engine\nmount: secrets/"]
            AzureEngine["Azure Secrets Engine\nmount: azure/"]
            JWTAuth["JWT Auth\nmount: jwt-&lt;cluster&gt;/"]
            AppRoleAuth["AppRole Auth\nmount: approle/"]
            VaultPolicies["Policies\ndefault · acr-reader · operator"]

            subgraph KVPaths["KV Secret Paths"]
                ArgoKV["secrets/argocd\n─────────────────\ngitlab_deploy_token_username\ngitlab_deploy_token_password\ngitlab_values_access_username\ngitlab_values_access_token\nadmin_password\nserver_secret_key"]
                AppKV["secrets/application\n─────────────────\nmongodb_password\nmongodb_replica_set_key\nauth0_client_id\nauth0_client_secret\npostgresql_password\n..."]
            end
        end
    end

    subgraph TFC["Terraform Cloud"]
        TFVault["Vault Workspace\n─────────────────\n• JWT auth mount\n• Auth roles\n• Policies\n• KV secret seeding"]
        TFCluster["Cluster Workspace\n─────────────────\n• AKS/EKS cluster\n• VSO Helm release\n• kubectl_manifest:\n  VaultAuth per NS"]
    end

    subgraph AKS["AKS Cluster"]
        direction TB

        subgraph VSOSystem["namespace: vault-secrets-operator-system"]
            VSOPod["VSO Controller Manager\nHelm: vault-secrets-operator v0.10.0"]
            VConn["VaultConnection: default\n─────────────────\naddress: HCP Vault URL\nskipTLSVerify: false"]
        end

        subgraph ArgoNS["namespace: argocd"]
            direction TB
            VAuthArgo["VaultAuth: default\n─────────────────\nmethod: jwt\nmount: jwt-&lt;cluster&gt;\nnamespace: admin/deployments/&lt;cluster&gt;\nserviceAccount: default\naudiences: [AKS OIDC issuer]\nvaultConnectionRef:\n  vault-secrets-operator-system/default"]

            subgraph VSSArgo["VaultStaticSecrets"]
                VSSRepo["VaultStaticSecret:\narrowcd-repo-fitfile-deployment-repo\n─────────────────\npath: argocd\ntransformation templates:\n  username ← gitlab_deploy_token_username\n  password ← gitlab_deploy_token_password\n  url ← gitlab.com/fitfile/deployment.git"]
                VSSValues["VaultStaticSecret:\narrowcd-values-repo-creds\n─────────────────\npath: argocd\ntransformation templates:\n  username ← gitlab_values_access_username\n  password ← gitlab_values_access_token\n  url ← gitlab.com/fitfile/customers/.../&lt;cluster&gt;.git"]
                VSSSecret["VaultStaticSecret:\narrowcd-secret\n─────────────────\npath: argocd\ntransformation templates:\n  admin.password\n  server.secretkey"]
            end

            subgraph K8SSecretsArgo["Kubernetes Secrets (created by VSO)"]
                SecRepo["Secret: argocd-repo-fitfile-deployment-repo\nlabel: argocd.argoproj.io/secret-type: repository"]
                SecValues["Secret: argocd-values-repo-creds\nlabel: argocd.argoproj.io/secret-type: repository"]
                SecArgo["Secret: argocd-secret"]
            end

            subgraph ArgoPods["ArgoCD Components"]
                ArgoServer["argocd-server"]
                ArgoRepo["argocd-repo-server"]
                ArgoAppCtrl["argocd-application-controller"]
            end

            RootApp["Application: ff-&lt;cluster&gt;\n(app-of-apps)\n─────────────────\nsource 1: fitfile/deployment.git\n  path: charts/ffnode\n  targetRevision: &lt;cluster&gt;-prod-latest-release\nsource 2: fitfile/customers/.../&lt;cluster&gt;.git\n  ref: values\n  targetRevision: main"]
        end

        subgraph AppNS["namespace: &lt;cluster&gt; (e.g. mkuh-prd-4)"]
            direction TB
            VAuthApp["VaultAuth: default\n(same pattern as argocd VaultAuth)"]

            VSSMongo["VaultStaticSecret: mongodb\n─────────────────\npath: application\ntransformation templates:\n  mongodb-root-password ← mongodb_password\n  mongodb-replica-set-key ← mongodb_replica_set_key\nexcludes: [.*]"]

            VDSPull["VaultDynamicSecret:\nfitfile-image-pull-secret\n─────────────────\nmount: azure\npath: creds/acr-pull\nrenewalPercent: 67\ntransformation → .dockerconfigjson\n  username ← client_id\n  password ← client_secret"]

            SecMongo["Secret: mongodb"]
            SecPull["Secret: fitfile-image-pull-secret\ntype: kubernetes.io/dockerconfigjson"]

            ChildApp["Child Application:\nff-&lt;cluster&gt;-mongodb-b17ef\n(rendered by parent Helm)"]

            AppPods["Application Pods\n(MongoDB, etc.)"]
        end
    end

    subgraph GitLab["GitLab"]
        DeployRepo["fitfile/deployment.git\n─────────────────\nHelm charts\n(charts/ffnode, etc.)"]
        ValuesRepo["fitfile/customers/eoe/&lt;cluster&gt;.git\n─────────────────\ngenerated/values.yaml\n(per-customer config)"]
    end

    %% Terraform provisions
    TFVault -->|"creates auth mounts,\nroles, policies,\nseeds KV secrets"| VaultNS
    TFCluster -->|"creates cluster,\ninstalls VSO Helm,\napplies VaultAuth CRs"| AKS

    %% VSO watches and reconciles
    VSOPod -->|"watches VaultStaticSecret\n& VaultDynamicSecret CRs"| VSSArgo
    VSOPod -->|"watches"| VSSMongo
    VSOPod -->|"watches"| VDSPull

    %% VaultAuth chain
    VAuthArgo -->|"references"| VConn
    VAuthApp -->|"references"| VConn
    VConn -->|"connects to"| VaultInstance

    %% Auth to Vault
    VAuthArgo -->|"JWT auth via\nAKS OIDC issuer"| JWTAuth
    VAuthApp -->|"JWT auth"| JWTAuth
    JWTAuth -->|"grants policies"| VaultPolicies

    %% VSS reads from Vault KV
    VSSRepo -->|"reads"| ArgoKV
    VSSValues -->|"reads"| ArgoKV
    VSSSecret -->|"reads"| ArgoKV
    VSSMongo -->|"reads"| AppKV

    %% VDS reads from Azure engine
    VDSPull -->|"reads"| AzureEngine

    %% VSO creates K8s Secrets
    VSSRepo -->|"creates/updates"| SecRepo
    VSSValues -->|"creates/updates"| SecValues
    VSSSecret -->|"creates/updates"| SecArgo
    VSSMongo -->|"creates/updates"| SecMongo
    VDSPull -->|"creates/updates"| SecPull

    %% ArgoCD uses secrets
    ArgoServer -->|"reads"| SecArgo
    ArgoRepo -->|"reads repo creds"| SecRepo
    ArgoRepo -->|"reads repo creds"| SecValues

    %% ArgoCD fetches from GitLab
    ArgoRepo -->|"git clone\n(deploy token)"| DeployRepo
    ArgoRepo -->|"git clone\n(values access token)"| ValuesRepo

    %% App-of-apps chain
    RootApp -->|"Helm renders\nchild Application CRs"| ChildApp
    ChildApp -->|"syncs → creates"| VSSMongo
    ChildApp -->|"syncs → creates"| VDSPull

    %% Pods consume secrets
    AppPods -->|"mounts"| SecMongo
    AppPods -->|"imagePullSecrets"| SecPull

    %% Styling
    classDef vault fill:#FFD700,stroke:#B8860B,color:#000
    classDef vso fill:#7B68EE,stroke:#483D8B,color:#fff
    classDef k8s fill:#326CE5,stroke:#1a3a7a,color:#fff
    classDef argo fill:#EF7B4D,stroke:#c45a2e,color:#fff
    classDef gitlab fill:#FC6D26,stroke:#c45520,color:#fff
    classDef tf fill:#7B42BC,stroke:#5a2d8a,color:#fff
    classDef secret fill:#2ECC71,stroke:#1a9c54,color:#fff

    class VaultInstance,KV,AzureEngine,JWTAuth,AppRoleAuth,VaultPolicies,ArgoKV,AppKV vault
    class VSOPod,VConn,VAuthArgo,VAuthApp,VSSRepo,VSSValues,VSSSecret,VSSMongo,VDSPull vso
    class SecRepo,SecValues,SecArgo,SecMongo,SecPull secret
    class ArgoServer,ArgoRepo,ArgoAppCtrl,RootApp,ChildApp argo
    class DeployRepo,ValuesRepo gitlab
    class TFVault,TFCluster tf
    class AppPods k8s
