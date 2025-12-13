---
aliases: []
confidence: 
created: 2025-04-08T11:39:32Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:45Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [ff_deploy]
title: FItfile deployment ArgoCD Style
type: 
uid: 
updated: 
version: 
---

Based on my analysis, here's how the components fit together:

1. Current Architecture:
   - The `ffnode` chart appears to be an "App of Apps" pattern implementation for ArgoCD
   - It defines a complete deployment unit that includes multiple components (frontend, fitconnect, workflows-api, etc.)
   - The chart uses ArgoCD Application resources to manage the deployment of various components

2. Deployment Structure:
   - The `hie-prod-34` deployment is a specific instance using the ffnode chart
   - It overrides default values from the ffnode chart with environment-specific configurations
   - The deployment includes components like MongoDB, MinIO, PostgreSQL, and various services

3. Charts Directory Status:
   - The individual charts in the `charts` directory appear to be the component definitions
   - These charts are likely still needed because:
     a. They define the actual Kubernetes resources for each component
     b. The ffnode chart references these components through ArgoCD Applications
     c. The recent modifications to `ffnode/values.yaml` and templates suggest active use

4. Recommendation:
   The charts are still needed because:
   1. They serve as the source of truth for component definitions
   2. The ffnode chart uses them as dependencies to create ArgoCD Applications
   3. The recent activity in the ffnode chart (last modified Apr 07) indicates active use
   4. The hie-prod-34 deployment shows a working pattern of using the ffnode chart with overrides

However, I would suggest some organizational improvements:

1. Documentation:
   - Add clear documentation in the ffnode chart explaining its role as an App of Apps
   - Document the relationship between ffnode and the individual component charts

2. Structure:
   - Consider moving the component charts to a separate repository if they're truly reusable
   - Keep only the ffnode chart and deployment-specific values in this repository
   - Add a clear README explaining the deployment pattern

3. Versioning:
   - Implement proper versioning for both the ffnode chart and component charts
   - Document version compatibility between components

I'll explain the flow of reconciliation from ArgoCD's perspective, starting from this template and going down to the actual MongoDB pods. Let me break this down step by step:

1. Initial Template Processing (Helm Level)
   - This file is a template that generates an ArgoCD `Application` resource
   - The template is processed by Helm when the ffnode chart is installed/upgraded
   - The `{{- if eq .Values.deploy.persistence true }}` condition determines if this Application should be created
   - Various template functions populate values like namespace, release name, and chart version

2. ArgoCD Application Creation
   - The template generates an ArgoCD `Application` resource with:

 ```yaml
 apiVersion: argoproj.io/v1alpha1
 kind: Application
 metadata:
   name: [release-name]-mongodb
   namespace: argocd
```

   - This Application is the "app of apps" entry point for MongoDB
   - It's placed in the `argocd` namespace where ArgoCD manages its applications

3. ArgoCD Application Controller Reconciliation
   - The ArgoCD Application Controller watches for Application resources
   - When it sees this Application, it:
     1. Reads the `source` section to determine what to deploy:

```yaml
source:
  chart: helm/mongodb
  repoURL: "fitfileregistry.azurecr.io"
  targetRevision: "15.6.12"
```

2. Fetches the MongoDB Helm chart from the specified registry
3. Processes the Helm values (merged from multiple sources):

```yaml
values: |
  {{- $values := merge (merge .Values.mongodb (dict "global" .Values.global)) (include "bitnami.metrics" . | fromYaml) -}}
```

4. Kubernetes Resource Generation
   - ArgoCD uses the Helm chart to generate Kubernetes resources
   - The MongoDB chart typically creates:
     - StatefulSet for MongoDB pods
     - Services for network access
     - ConfigMap for configuration
     - PersistentVolumeClaim for data storage
     - Other supporting resources (secrets, etc.)

5. Kubernetes Controller Reconciliation
   - The Kubernetes `StatefulSet` controller sees the new StatefulSet
   - It creates `PersistentVolumeClaim` if needed
   - It creates Pods according to the StatefulSet spec
   - The Pod controller schedules the pods on appropriate nodes

6. Pod Lifecycle
   - Kubelet on each node creates the containers
   - MongoDB containers start up
   - Readiness probes ensure the MongoDB instance is ready
   - The StatefulSet controller maintains the desired number of replicas

7. Continuous Reconciliation
   - ArgoCD continuously monitors:
     - The desired state (from the Application)
     - The actual state (in the cluster)
   - If drift occurs, ArgoCD can automatically sync the changes
   - The sync wave (`argocd.argoproj.io/sync-wave: "0"`) ensures proper ordering of deployments

8. Health Checking
   - ArgoCD monitors the health of all resources
   - The Application status reflects the overall health
   - The sync policy (`syncPolicy`) determines automatic sync behavior

Here's a visual flow of the reconciliation process:

```sh
Helm Template (mongodb-application.yaml)
           ↓
ArgoCD Application Resource
           ↓
ArgoCD Application Controller
           ↓
MongoDB Helm Chart Processing
           ↓
Kubernetes Resources (StatefulSet, Services, etc.)
           ↓
Kubernetes Controllers (StatefulSet, Pod)
           ↓
MongoDB Pods Running in Cluster
```

The key benefit of this "app of apps" pattern is that it:

1. Centralizes deployment configuration
2. Enables declarative management of all components
3. Provides consistent deployment patterns
4. Allows for automated drift detection and correction
5. Maintains deployment order through sync waves
6. Initial Infrastructure Deployment (First Step)
   - Private VPC is created
   - EKS cluster is deployed in the private VPC
   - Jumpbox is set up in the private VPC for access

7. Platform Deployment (Second Step - From Jumpbox)
   The terraform-helm-fitfile-platform module:
   - Creates necessary namespaces
   - Deploys core components in this order:
     1. Vault Operator (for secrets management)
     2. Reflector (for secret reflection across namespaces)
     3. Ingress Controller (for external access)
     4. ArgoCD (the GitOps platform)
     5. Cluster Autoscaler (for AWS)
8. ArgoCD Deployment and App of Apps Pattern
   The ArgoCD module deploys two key components:

```hcl
# 1. Core ArgoCD installation
resource "helm_release" "argocd" {
 chart      = "helm/argo-cd"
 namespace  = "argocd"
 # ... configuration for ingress, TLS, etc.
}

# 2. App of Apps deployment
resource "helm_release" "argocd-apps" {
 chart      = "helm/argocd-apps"
 name       = "fitfile-project"
 # ... configuration for applications
}
```

4. Connection to ffnode Chart
   - The `argocd-apps` helm release is where your ffnode chart gets deployed
   - It uses the app-values.tftpl template to configure the applications
   - This is where the "app of apps" pattern is implemented:
     1. The ffnode chart is deployed as an ArgoCD Application
     2. This Application then manages other Applications (like MongoDB, etc.)
     3. Each component chart (from your charts directory) is deployed as a separate Application
5. Complete Deployment Flow

```sh
Terraform (from jumpbox)
       ↓
ArgoCD Installation
       ↓
ArgoCD Apps Chart (fitfile-project)
       ↓
ffnode Chart (App of Apps)
       ↓
Component Applications (MongoDB, etc.)
       ↓
Kubernetes Resources
```

6. Security and Access Flow

```sh
Private VPC
       ↓
Jumpbox (SSH access)
       ↓
Terraform execution
       ↓
ArgoCD UI (via Ingress)
       ↓
Kubernetes API
```

This architecture provides several benefits:

1. Security: All deployment happens from within the private VPC
2. GitOps: All changes are tracked in Git and applied through ArgoCD
3. Modularity: Each component is independently versioned and managed
4. Scalability: Easy to add new components or environments
5. Consistency: Same deployment pattern across environments

The charts in your `charts` directory are still needed because:

1. They define the actual Kubernetes resources for each component
2. They're referenced by the ffnode chart's ArgoCD Applications
3. They provide the templating and configuration for each component
4. They maintain version control and consistency across deployments

## Here's how the `helm_release` "argocd-apps" Works

1. Purpose
   - This helm release deploys ArgoCD Applications that define what should be deployed in your cluster
   - It's essentially the "app of apps" pattern implementation
   - It creates a project called "fitfile" and multiple ArgoCD Applications under it

2. Configuration Structure

```hcl
resource "helm_release" "argocd-apps" {
 name       = "fitfile-project"
 chart      = "helm/argocd-apps"
 namespace  = var.app_namespace
 values     = [templatefile("${path.module}/app-values.tftpl", { applications = var.applications })]
}
```

3. Template Processing
   - Uses `app-values.tftpl` as a template
   - The template processes a list of applications defined in the `applications` variable
   - Each application in the list becomes an ArgoCD Application resource

4. Application Definition Structure

```hcl
applications = [
 {
   name = "app-name"
   target_revision = "branch-or-tag"
   chart_path = "charts/ffnode"
   destination = {
     namespace = "target-namespace"
   }
   source = {
     type = "helm"  # or "plugin"
     release_name = "release-name"
     value_files = ["path/to/values.yaml"]
     values = "inline yaml values"
   }
 }
]
```

5. Generated ArgoCD Applications
   For each application in the list, it generates an ArgoCD Application that looks like:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
 name: app-name
 namespace: argocd
spec:
 project: fitfile
 source:
   repoURL: https://gitlab.com/fitfile/deployment.git
   targetRevision: "branch-or-tag"
   path: charts/ffnode
   helm:
     releaseName: release-name
     valueFiles: ["path/to/values.yaml"]
     values: |
       # inline values here
 destination:
   server: https://kubernetes.default.svc
   namespace: target-namespace
 syncPolicy:
   automated:
     prune: true
     selfHeal: true
```

6. Project Configuration
   - Creates a project called "fitfile"
   - Allows access to all namespaces (`namespace: ""`)
   - Whitelists certain cluster resources (ClusterIssuer, PriorityClass)
   - Restricts source repositories to your deployment repo

7. Sync Policy
   - Automated sync is enabled
   - Pruning is enabled (removes resources that are no longer defined)
   - Self-healing is enabled (reverts manual changes)

8. Special Features
   - Supports both Helm and Plugin-based applications
   - Can use value files or inline values
   - Handles Vault integration for plugins
   - Ignores differences in deployment replicas (allows HPA to work)

9. Flow of Operation

```sh
Terraform applies
       ↓
argocd-apps helm release created
       ↓
Template processes applications list
       ↓
ArgoCD Applications created
       ↓
ArgoCD controller sees new Applications
       ↓
Applications sync their resources
       ↓
Kubernetes resources created
```

This setup allows you to:

1. Define all your applications in one place (Terraform)
2. Version control your application definitions
3. Automatically deploy and manage applications
4. Keep your cluster in sync with your Git repository
5. Handle both Helm charts and custom plugins
6. Manage multiple environments with different configurations
7. Root Configuration

```hcl
locals {
 argocd_applications = [{
   name            = "ff-${lower(var.deployment_key)}"  # e.g., "ff-pv-aks-1"
   target_revision = "master"
   source = {
     release_name = lower(var.deployment_key)
     type         = "helm"
     value_files  = [var.deployment_repo_values_file_path]  # e.g., "/ffnodes/fitfile/pv-aks-1/values.yaml"
   }
 }]
}
```

   This defines a single root application that will be deployed by ArgoCD. It's using the ffnode chart we discussed earlier.

2. Platform Module Deployment

```hcl
module "platform" {
 source  = "app.terraform.io/FITFILE-Platforms/fitfile-platform/helm"
 version = "1.0.38"

 argocd_host          = local.argocd_host
 argocd_applications  = local.argocd_applications
 # ... other configuration
}
```

   This module (which we looked at earlier) deploys:

   - ArgoCD itself
   - The root application that manages all other applications

3. Deployment Flow

```sh
Terraform (from jumpbox)
       ↓
Platform Module
       ↓
ArgoCD Installation
       ↓
Root Application (ff-pv-aks-1)
       ↓
ffnode Chart
       ↓
Component Applications (MongoDB, etc.)
```

4. Values File Path

```hcl
deployment_repo_values_file_path = "/ffnodes/fitfile/pv-aks-1/values.yaml"
```

   This points to the values file that overrides the defaults in the ffnode chart. This is where you define:

   - Which components to deploy
   - Environment-specific configurations
   - Resource requirements
   - etc.

5. Vault Integration

```hcl
app_role_secrets_map = tomap({
 "argocd" = { ... },
 "application" = { ... },
 "spicedb" = { ... },
 "argoWorkflows" = { ... },
 "monitoring" = { ... }
})
```

   This sets up Vault authentication for different components, allowing them to securely access secrets.

6. Complete Deployment Chain

```sh
vars.tfvars (deployment config)
       ↓
main.tf (terraform configuration)
       ↓
platform module
       ↓
ArgoCD installation
       ↓
Root Application (ff-pv-aks-1)
       ↓
ffnode chart with /ffnodes/fitfile/pv-aks-1/values.yaml
       ↓
Component Applications
       ↓
Kubernetes Resources
```

7. Security Flow

```sh
Private VPC
       ↓
Jumpbox
       ↓
Terraform (with AWS EKS authentication)
       ↓
ArgoCD (with Vault authentication)
       ↓
Component Applications
```

This setup provides several benefits:

1. Centralized Configuration: All deployment settings in one place (vars.tfvars)
2. Environment Isolation: Each deployment has its own namespace and configuration
3. Secret Management: Vault integration for secure secret access
4. GitOps: All changes tracked in Git
5. Private Access: Everything deployed from within the private VPC
6. Automated Deployment: ArgoCD handles the actual deployment of components

The key point is that this template only deploys the root application (ff-pv-aks-1). That root application then uses the ffnode chart to deploy all the component applications (MongoDB, etc.) through ArgoCD's app of apps pattern.

Would you like me to elaborate on any specific part of this flow or explain how specific components interact in more detail?

## Here's how Stage 2 Works Using the private_platform_template

1. Template Structure

   ```sh
   private_platform_template/
   ├── main.tf           # Main configuration
   ├── vars.tfvars       # Deployment-specific variables
   ├── vars_setup.sh     # Script to set up variables
   └── default_data_source.json  # Default data source configuration
   ```

2. Deployment Flow

   ```sh
   Stage 1 (Infrastructure)
           ↓
   Jumpbox Access
           ↓
   private_platform_template
           ↓
   Platform Module
           ↓
   ArgoCD Installation
           ↓
   Root Application
           ↓
   Component Applications
   ```

3. Key Components

   a. Vault Integration

```hcl
locals {
 vault_namespace = "deployments/${var.deployment_key}"
 app_role_secrets_map = tomap({
   "argocd" = { ... },
   "application" = { ... },
   "spicedb" = { ... },
   "argoWorkflows" = { ... },
   "monitoring" = { ... }
 })
}
```

   b. ArgoCD Application

```hcl
locals {
 argocd_applications = [{
   name            = "ff-${lower(var.deployment_key)}"
   target_revision = "master"
   source = {
     release_name = lower(var.deployment_key)
     type         = "helm"
     value_files  = [var.deployment_repo_values_file_path]
   }
 }]
}
```

   c. Platform Module

```hcl
module "platform" {
 source  = "app.terraform.io/FITFILE-Platforms/fitfile-platform/helm"
 version = "1.0.29"

 ingress_ip_address         = var.ingress_controller_ip_address
 ingress_load_balancer_type = "internal"
 vault_address             = var.vault_address
 argocd_host              = local.argocd_host
 argocd_applications      = local.argocd_applications
 app_role_secrets_map     = local.app_role_secrets_map
}
```

4. Configuration Flow

```sh
vars.tfvars (deployment config)
       ↓
vars_setup.sh (variable setup)
       ↓
main.tf (terraform configuration)
       ↓
platform module
       ↓
ArgoCD installation
       ↓
Root Application
```

5. Security Flow

   ```sh
   Private VPC
           ↓
   Jumpbox
           ↓
   Terraform (with AKS credentials)
           ↓
   Vault Authentication
           ↓
   ArgoCD
           ↓
   Applications
   ```

6. Dependencies Chain

   ```sh
   Infrastructure (Stage 1)
           ↓
   AKS Cluster Access
           ↓
   Vault Authentication
           ↓
   ArgoCD Installation
           ↓
   Root Application
           ↓
   Component Applications
   ```

7. Key Features
   - Private Access: All components deployed within private VPC
   - Secret Management: Vault integration for secure secret access
   - GitOps: ArgoCD for declarative deployments
   - Modularity: Platform module for consistent deployments
   - Environment Isolation: Separate namespaces and configurations
   - Automated Deployment: ArgoCD handles component deployment

8. Deployment Process
   1. Clone template to jumpbox
   2. Update vars.tfvars with deployment-specific values
   3. Run vars_setup.sh to prepare environment
   4. Apply Terraform configuration
   5. Platform module deploys ArgoCD
   6. ArgoCD deploys root application
   7. Root application deploys components

This setup provides:

1. Consistent Deployment: Same pattern for all environments
2. Secure Access: Through private VPC and Vault
3. Automated Management: Through ArgoCD
4. Environment Isolation: Through separate configurations
5. Secret Management: Through Vault integration
6. Scalability: Easy to add new environments

Ah, let me trace this through. The key is in how the root ArgoCD application is configured and how it connects to the ffnode chart. Let me show you the flow:

1. Root Application Configuration (from private_platform_template/main.tf):

```hcl
locals {
  argocd_applications = [{
    name            = "ff-${lower(var.deployment_key)}"  # e.g., "ff-pv-aks-1"
    target_revision = "master"
    source = {
      release_name = lower(var.deployment_key)
      type         = "helm"
      value_files  = [var.deployment_repo_values_file_path]  # e.g., "/ffnodes/fitfile/pv-aks-1/values.yaml"
    }
  }]
}
```

2. Values File Path (from vars.tfvars):

```hcl
deployment_repo_values_file_path = "/ffnodes/fitfile/pv-aks-1/values.yaml"
```

3. ffnode Chart (from helm_chart_deployment/charts/ffnode/values.yaml):

```yaml
deploy:
  fitfileCentral: true
  initialiseCluster: true
  certManager: true
  persistence: true
  messageBroker: true
  blobCsiDriver: false
  seedData: false
  workflowsIntegrationTests: false
  monitoring: true
  vault: false
  coordinatingStation: true
  fitconnect: true
  frontend: true
  workflowsApi: true
```

4. Application Templates (from helm_chart_deployment/charts/ffnode/templates/):

```sh
templates/
├── mongodb-application.yaml
├── fitconnect-application.yaml
├── frontend-application.yaml
├── ffcloud-application.yaml
├── workflows-api-application.yaml
└── ... (other component applications)
```

Here's the complete flow:

1. Initial Deployment:

   ```sh
   private_platform_template
           ↓
   Root ArgoCD Application (ff-pv-aks-1)
           ↓
   ffnode Chart
           ↓
   Component Applications
   ```

2. How it Works:
   - The root application points to the ffnode chart
   - The ffnode chart's values.yaml defines which components to deploy
   - The ffnode chart's templates directory contains ArgoCD Application definitions for each component
   - Each component application (like fitconnect, ffcloud) is created based on these templates

3. Example Component Application (from mongodb-application.yaml):

```yaml
{{- if eq .Values.deploy.persistence true }}
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: {{ ternary .Values.mongodb.releaseName (printf "%s-mongodb" .Release.Name) (ne .Values.mongodb.releaseName "") }}
  namespace: argocd
spec:
  destination:
    namespace: {{include "namespace" . }}
    server: https://kubernetes.default.svc
  source:
    chart: helm/mongodb
    repoURL: "fitfileregistry.azurecr.io"
    targetRevision: {{ default "15.6.12" .Values.mongodb.targetRevision }}
    helm:
      releaseName: {{ ternary .Values.mongodb.releaseName (printf "%s-mongodb" .Release.Name) (ne .Values.mongodb.releaseName "") }}
      values: |
        {{- $values := merge (merge .Values.mongodb (dict "global" .Values.global)) (include "bitnami.metrics" . | fromYaml) -}}
        {{- include "renderValuesWithVaultSecretInExtraDeploy" (list . $values) | indent 8 }}
```

4. Deployment Chain:

```sh
Root Application (ff-pv-aks-1)
           ↓
ffnode Chart
           ↓
Component Applications (created from templates)
           ↓
Individual Component Deployments
```

5. Component Selection:
   - The `deploy` section in ffnode's values.yaml controls which components are deployed
   - Each component has its own ArgoCD Application template
   - The templates are rendered based on the values.yaml configuration
   - Each component application then deploys its specific resources

6. Values Override Flow:

```sh
deployment_repo_values_file_path
           ↓
Environment-specific values.yaml
           ↓
ffnode chart values.yaml (defaults)
           ↓
Component-specific values
           ↓
Final Kubernetes resources
```

So, to answer your specific question:

1. The root app doesn't directly know what to deploy
2. It deploys the ffnode chart
3. The ffnode chart contains templates for all possible components
4. The values.yaml (both default and overridden) determine which components are actually deployed
5. Each component's template creates an ArgoCD Application that then deploys that component

I see that this is a two-stage deployment:

1. Stage 1 (test-sde-v2):
   - Creates the infrastructure (VPC, EKS, etc.)
   - Sets up the jumpbox
   - Configures networking and security

2. Stage 2 (using private_platform_template):
   - This is where the ArgoCD and ffnode chart deployment happens
   - You would:
     1. SSH into the jumpbox
     2. Clone the private_platform_template
3. Update vars.tfvars with:

```hcl
deployment_key = "test-sde-v2"
deployment_repo_values_file_path = "/ffnodes/fitfile/test-sde-v2/values.yaml"
```

4. Run the deployment

The connection to the ffnode chart happens in stage 2 through the private_platform_template, which we saw earlier:

```hcl
locals {
  argocd_applications = [{
    name            = "ff-${lower(var.deployment_key)}"  # becomes "ff-test-sde-v2"
    target_revision = "master"
    source = {
      release_name = lower(var.deployment_key)
      type         = "helm"
      value_files  = [var.deployment_repo_values_file_path]  # points to "/ffnodes/fitfile/test-sde-v2/values.yaml"
    }
  }]
}
```

Would you like me to:

1. Show you how to set up the stage 2 deployment for test-sde-v2?
2. Look at an example values.yaml file from another deployment to see how it configures the components?
3. Explain more about how the two stages work together?

In the private_platform_template, when we see:

```hcl
argocd_applications = [{
  name            = "ff-${lower(var.deployment_key)}"
  target_revision = "master"
  source = {
    release_name = lower(var.deployment_key)
    type         = "helm"
    value_files  = [var.deployment_repo_values_file_path]
  }
}]
```

This is using ArgoCD's Helm integration, but it's missing a crucial piece - the chart source! Let me check the platform module to see where this is configured:

Read file: TFC-Modules/terraform-helm-fitfile-platform/argocd/app-values.tftpl

Now I see the missing piece! In the template, there's a crucial line:

```hcl
path: ${app.chart_path}
```

This is where the chart path is specified. Let me check the variables to see how this is set:

Read file: TFC-Modules/terraform-helm-fitfile-platform/argocd/variables.tf

Now I see it! The chart path is specified in the applications variable with a default value:

```hcl
chart_path = optional(string, "charts/ffnode")
```

So here's how it all works:

1. Chart Location:
   - The ffnode chart is located at `helm_chart_deployment/charts/ffnode/`
   - This is referenced in the Git repository as `charts/ffnode`

2. ArgoCD Application Configuration:

```hcl
applications = [{
 name            = "ff-test-sde-v2"
 target_revision = "master"
 chart_path      = "charts/ffnode"  # This is the default
 source = {
   release_name = "test-sde-v2"
   type         = "helm"
   value_files  = ["/ffnodes/fitfile/test-sde-v2/values.yaml"]
 }
}]
```

3. Helm Chart Resolution:
   - ArgoCD looks for the chart at `charts/ffnode` in the Git repository
   - This resolves to `helm_chart_deployment/charts/ffnode/Chart.yaml`
   - The values file is used to override the default values in the chart

4. Complete Flow:

   ```sh
   Git Repository
           ↓
   charts/ffnode (chart path)
           ↓
   Chart.yaml (chart definition)
           ↓
   values.yaml (default values)
           ↓
   /ffnodes/fitfile/test-sde-v2/values.yaml (overrides)
           ↓
   Final Kubernetes Resources
   ```

So when you see:

```hcl
value_files = [var.deployment_repo_values_file_path]
```

This is just specifying which values file to use to override the defaults in the chart. The chart itself is found at the `chart_path` location in the Git repository.

Would you like me to:

1. Show you how to modify the chart path for a specific deployment?
2. Explain more about how Helm resolves charts and values?
3. Show you how to verify which chart is being used in a deployment?

Let me analyse your implementation of the App of Apps pattern in ArgoCD. Here's what I found:

1. **Root Application (ffnode)**:
   - Your `ffnode` Helm chart acts as the root application that manages multiple child applications
   - The chart uses feature flags in `values.yaml` under the `deploy:` section to control which applications are deployed
   - Common ArgoCD sync policies are defined in `values.yaml` under `argocdApp:` section

2. **Child Applications**:
   Your implementation includes several child applications, each with their own ArgoCD application definition:
   - Infrastructure components:
     - `cert-manager-application.yaml`
     - `blob-csi-driver-application.yaml`
     - `vault-application.yaml`
   - Databases:
     - `mongodb-application.yaml`
     - `postgresql-application.yaml`
     - `minio-application.yaml`
   - Application components:
     - `ffcloud-application.yaml`
     - `fitconnect-application.yaml`
     - `frontend-application.yaml`
     - `workflows-api-application.yaml`
   - Monitoring:
     - `grafana-application.yaml`
     - `prometheus-crds-application.yaml`

3. **Sync Policy Configuration**:
   You have implemented a robust sync policy in `values.yaml`:

   ```yaml
   argocdApp:
     syncPolicy:
       automated:
         prune: true
         selfHeal: true
         allowEmpty: false
       syncOptions:
         - Validate=false
         - CreateNamespace=true
         - PrunePropagationPolicy=foreground
         - PruneLast=true
       retry:
         limit: 5
         backoff:
           duration: 5s
           factor: 2
           maxDuration: 3m
   ```

4. **Best Practices Implemented**:
   - Modular structure with separate application definitions
   - Feature flags for selective deployment
   - Consistent sync policies across applications
   - Namespace management through CreateNamespace option
   - Proper pruning and clean-up configuration
   - Retry mechanisms for failed syncs

5. **Security Considerations**:
   - Integration with Vault for secrets management
   - Image pull secrets configuration
   - OAuth configuration support
   - Certificate management through cert-manager

Recommendations for improvement:

1. **Health Checks**: Consider adding health checks and sync windows to your ArgoCD applications for better control over deployment timing and reliability.
2. **Resource Management**: Some of your applications have resource requests defined, but not all. Consider adding consistent resource requests/limits across all applications.
3. **Progressive Delivery**: You might want to consider implementing progressive delivery patterns using Argo Rollouts for critical services.
4. **Application Dependencies**: While the App of Apps pattern is implemented well, you could make dependencies between applications more explicit using the `dependsOn` field in ArgoCD applications.
5. **Project Segregation**: Currently using the `default` project. Consider creating separate ArgoCD projects for different types of applications (infrastructure, applications, monitoring) for better RBAC control.

Example of how to implement application dependencies:

```yaml
spec:
  dependsOn:
    - name: cert-manager
    - name: postgresql
```

## App of Apps Pattern in Argo CD

The App of Apps pattern is a method for managing multiple Argo CD Applications using a single, higher-level Argo CD Application. This pattern is useful for cluster bootstrapping, managing microservices, and other scenarios where you need to manage many related applications.

### Resources Used

- **Argo CD Application:** The primary resource used to define the desired state of a set of Kubernetes resources.
- **Git Repository:** Stores the Kubernetes manifests for the applications.

### Best Practices

- **Repository Structure:** Organize your Git repository in a way that makes sense for your application structure. For example, you might have a directory for each application.
- **Templating:** Use templating tools like Helm or Kustomize to manage the Application definitions.
- **Automation:** Leverage Argo CD's auto-sync and auto-prune features to automate the deployment and cleanup of applications.
- **Access Control:** Secure your "root" Application to prevent unauthorized changes, as this can lead to widespread deployments.

### Example

Let's say you have a root Argo CD Application that manages two child applications: `app1` and `app2`.

YAML

```sh
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: root-app
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/your-org/root-app-config.git
    targetRevision: HEAD
    path: apps
  destination:
    server: https://kubernetes.default.svc
    namespace: argocd
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

The Git repository (`https://github.com/your-org/root-app-config.git`) has the following structure:

```sh
apps/
  app1.yaml
  app2.yaml
```

Each file defines a child application:

```yaml
# apps/app1.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: app1
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/your-org/app1-config.git
    targetRevision: HEAD
    path: k8s
  destination:
    server: https://kubernetes.default.svc
    namespace: app1-ns
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

**Links:**
- [Ingress Configuration - Argo CD - Declarative GitOps CD for Kubernetes](<200_projects/SDLC/Ingress Configuration - Argo CD - Declarative GitOps CD for Kubernetes.md>)
- [k8s curriculum](<200_projects/k8s/k8s curriculum.md>)

```yaml
# apps/app2.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: app2
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/your-org/app2-config.git
    targetRevision: HEAD
    path: k8s
  destination:
    server: https://kubernetes.default.svc
    namespace: app2-ns
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

**Links:**
- [Ingress Configuration - Argo CD - Declarative GitOps CD for Kubernetes](<200_projects/SDLC/Ingress Configuration - Argo CD - Declarative GitOps CD for Kubernetes.md>)
- [k8s curriculum](<200_projects/k8s/k8s curriculum.md>)

In this example, changes to the `root-app` will trigger the creation/update of `app1` and `app2`.

### Glossary

- **App of Apps Pattern:** An Argo CD pattern where one Argo CD Application manages other Argo CD Applications.
- **Root Application:** The top-level Argo CD Application that manages other "child" Applications.
- **Child Application:** An Argo CD Application managed by a "root" Application.

To add a dependency annotation to an Argo CD Application manifest, you simply add an entry to the `metadata.annotations` section of the Application resource.

Here's the basic structure:

YAML

```sh
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: my-app
  namespace: argocd
  annotations:
    argocd.argoproj.io/depends-on: <dependency-name>
spec:
  # ... your Application spec ...
```

**Explanation:**

- `argoproj.io/depends-on`: This is the annotation key that Argo CD uses to identify application dependencies.
- `<dependency-name>`: Replace this with the name of the Application that your current Application depends on.

**Example:**

Let's say you have two Argo CD Applications: `order-service` and `database-service`. The `order-service` Application depends on the `database-service` being deployed first. You would add the dependency annotation to the `order-service` Application:

YAML

```sh
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: order-service
  namespace: argocd
  annotations:
    argocd.argoproj.io/depends-on: database-service
spec:
  # ... spec for order-service ...
```

**Important Considerations:**

- **Namespace:** Ensure both the dependent and the dependency Applications are in the same namespace. Cross-namespace dependencies are not supported.
- **Circular Dependencies:** Avoid creating circular dependencies (e.g., app A depends on app B, and app B depends on app A), as this can lead to indefinite waiting.
- **Application Names:** The value of the annotation should exactly match the `metadata.name` of the Application you're depending on.
- **Argo CD Version:** The `depends-on` feature was introduced in Argo CD v2.0.0. Make sure your Argo CD version supports this feature.

By using this annotation, you can control the order in which Argo CD synchronizes your Applications, ensuring that dependencies are deployed before their dependents.
