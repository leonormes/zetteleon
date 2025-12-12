---
aliases: []
confidence: 
created: 2025-09-04T11:40:12Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T14:24:10Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [automation, config, project/work/deployment, terraform, versioning]
title: Automated Platform Module Version Management
type:
uid: 
updated: 
version:
---

You're absolutely right - Terraform doesn't allow variables in the `version` field of module blocks. Here are several alternative approaches to centralize platform module version management:

## **🎯 Alternative Solutions**

### **1. Terraform Configuration Generation (Recommended)**

Generate Terraform files from templates using the centralized versions:

```bash
#!/bin/bash
# scripts/generate-cluster-configs.sh

# Fetch versions from global-version-manager
PLATFORM_VERSION=$(terraform output -state=global-version-manager.tfstate platform_module_version)

# Generate cluster configs from templates
for cluster_dir in Clusters/FITFILE/*/; do
  envsubst < templates/cluster-main.tf.tpl > "$cluster_dir/main.tf"
done
```

**Template file** (`templates/cluster-main.tf.tpl`):

```hcl
module "platform" {
  source  = "app.terraform.io/FITFILE-Platforms/fitfile-platform/helm"
  version = "${PLATFORM_MODULE_VERSION}"

  # Chart versions from remote state
  ingress_nginx_chart_version = data.terraform_remote_state.versions.outputs.${ENVIRONMENT}_ingress_nginx_chart_version
}
```

### **2. Terragrunt for DRY Configuration**

Use Terragrunt to centralize module versions:

```hcl
# terragrunt.hcl (root)
remote_state {
  backend = "remote"
  config = {
    organization = "FITFILE-Platforms"
    workspaces = {
      name = "global-version-manager"
    }
  }
}

# clusters/production/prod-1/terragrunt.hcl
include "root" {
  path = find_in_parent_folders()
}

terraform {
  source = "../../../modules/cluster"
}

inputs = {
  platform_module_version = dependency.versions.outputs.platform_module_version
  environment = "production"
}
```

### **3. GitLab CI/CD Pipeline Automation**

Automate version updates through CI/CD:

```yaml
# .gitlab-ci.yml
update-platform-versions:
  stage: update-configs
  script:
    - |
      # Get latest platform version
      PLATFORM_VERSION=$(terraform output -json | jq -r '.platform_module_version.value')

      # Update all cluster configs
      find Clusters/ -name "main.tf" -exec sed -i "s/version = \".*\"/version = \"$PLATFORM_VERSION\"/" {} \;

      # Create MR with changes
      git add .
      git commit -m "chore: update platform module to $PLATFORM_VERSION"
      git push origin -o merge_request.create
  only:
    - schedules
```

### **4. Terraform Locals with External Data**

Use external data source to fetch versions:

```hcl
# In each cluster main.tf
data "external" "platform_versions" {
  program = ["bash", "${path.module}/scripts/get-platform-version.sh"]
}

locals {
  platform_version = data.external.platform_versions.result.platform_module_version
}

# Use in module call - but this still won't work for version field!
```

### **5. Makefile-Based Configuration Management**

Use Make to manage configurations:

```makefile
# Makefile
.PHONY: update-versions sync-clusters

PLATFORM_VERSION := $(shell terraform output -raw platform_module_version)

update-versions:
 @echo "Updating platform version to $(PLATFORM_VERSION)"
 @find Clusters/ -name "main.tf" -exec sed -i 's/version = "[^"]*"/version = "$(PLATFORM_VERSION)"/g' {} \;

sync-clusters: update-versions
 @for dir in Clusters/FITFILE/*/; do \
  echo "Syncing $$dir"; \
  cd "$$dir" && terraform plan; \
 done
```

### **6. JSON/YAML Configuration Files (Most Flexible)**

Create a configuration-driven approach:

```yaml
# config/cluster-versions.yaml
environments:
  production:
    platform_module_version: "2.1.4"
    clusters:
      - prod-1-cluster
      - pentest-cluster
  staging:
    platform_module_version: "2.2.7"
    clusters:
      - staging-cluster-2
  testing:
    platform_module_version: "2.2.7"
    clusters:
      - testing-cluster
      - ff-hyve-1
```

```bash
#!/bin/bash
# scripts/sync-cluster-versions.sh

CONFIG_FILE="config/cluster-versions.yaml"

# For each environment
yq eval '.environments | keys | .[]' "$CONFIG_FILE" | while read env; do
  PLATFORM_VERSION=$(yq eval ".environments.$env.platform_module_version" "$CONFIG_FILE")
  CLUSTERS=$(yq eval ".environments.$env.clusters[]" "$CONFIG_FILE")

  echo "Updating $env clusters to platform version $PLATFORM_VERSION"

  echo "$CLUSTERS" | while read cluster; do
    CLUSTER_DIR="Clusters/FITFILE/*/$cluster"
    find . -path "*$CLUSTER_DIR/main.tf" -exec sed -i "s/version = \".*\"/version = \"$PLATFORM_VERSION\"/" {} \;
  done
done
```

## **🏆 Recommended Approach: Hybrid Solution**

Combine multiple approaches for maximum effectiveness:

```bash
#!/bin/bash
# scripts/platform-version-manager.sh

set -e

COMMAND=${1:-"check"}
CONFIG_FILE="config/platform-versions.yaml"

case $COMMAND in
  "check")
    echo "🔍 Checking platform version drift..."
    # Compare current versions with desired versions
    ;;

  "update")
    ENVIRONMENT=${2:-"all"}
    echo "🔄 Updating platform versions for $ENVIRONMENT..."

    # Fetch latest versions from global-version-manager
    terraform -chdir=../central-services/hcp/tfc output -json > /tmp/versions.json

    # Update cluster configs based on environment
    if [[ "$ENVIRONMENT" == "all" ]]; then
      ENVIRONMENTS=("production" "staging" "testing")
    else
      ENVIRONMENTS=("$ENVIRONMENT")
    fi

    for env in "${ENVIRONMENTS[@]}"; do
      PLATFORM_VERSION=$(jq -r ".${env}_platform_module_version.value" /tmp/versions.json)

      echo "  📦 Updating $env clusters to platform version $PLATFORM_VERSION"

      # Find and update cluster configs for this environment
      find "Clusters/FITFILE" -path "*$env*" -name "main.tf" \
        -exec sed -i.bak "s/version = \"[^\"]*\"/version = \"$PLATFORM_VERSION\"/" {} \;
    done
    ;;

  "validate")
    echo "✅ Validating cluster configurations..."
    # Run terraform validate on all clusters
    find Clusters/ -name "main.tf" -execdir terraform validate \;
    ;;

  *)
    echo "Usage: $0 {check|update [environment]|validate}"
    exit 1
    ;;
esac
```

## **🎯 Implementation Recommendation**

Since Terraform doesn't allow variables in the `version` field, I recommend the **JSON/YAML Configuration + Script Automation** approach as it provides the best balance of centralization and maintainability.

### **Implementation Steps:**

**1. Create Configuration File:**

```yaml
# config/platform-versions.yaml
environments:
  production:
    platform_module_version: "2.1.4"
    clusters:
      - prod-1-cluster
      - pentest-cluster
      - pentest-1-cluster
  staging:
    platform_module_version: "2.2.7"
    clusters:
      - staging-cluster-2
  testing:
    platform_module_version: "2.2.7"
    clusters:
      - testing-cluster
      - ff-hyve-1
      - ff-hyve-2
```

**2. Add Version Management Script:**

```bash
#!/bin/bash
# scripts/manage-platform-versions.sh

set -e

sync_versions() {
    local env=$1
    local config_file="config/platform-versions.yaml"

    # Get platform version for environment
    local platform_version=$(yq eval ".environments.$env.platform_module_version" "$config_file")

    # Get clusters for environment
    local clusters=$(yq eval ".environments.$env.clusters[]" "$config_file")

    echo "🔄 Updating $env clusters to platform version $platform_version"

    # Update each cluster's main.tf
    echo "$clusters" | while read cluster; do
        find Clusters/ -path "*$cluster/main.tf" -exec \
            sed -i.bak "s/version = \"[^\"]*\"/version = \"$platform_version\"/" {} \;
        echo "  ✅ Updated $cluster"
    done
}

case ${1:-"help"} in
    "sync")
        if [[ -n $2 ]]; then
            sync_versions "$2"
        else
            for env in production staging testing; do
                sync_versions "$env"
            done
        fi
        ;;
    "check")
        echo "🔍 Current platform module versions:"
        grep -r "version.*=" Clusters/*/main.tf | grep -v terraform_remote_state
        ;;
    *)
        echo "Usage: $0 {sync [environment]|check}"
        ;;
esac
```

**3. Integrate with GitLab CI:**

```yaml
# .gitlab-ci.yml
update-platform-versions:
  stage: deploy
  script:
    - ./scripts/manage-platform-versions.sh sync
    - |
      if git diff --quiet; then
        echo "No version changes needed"
      else
        git add .
        git commit -m "chore: sync platform module versions"
        git push origin HEAD:platform-version-updates -o merge_request.create
      fi
  only:
    - schedules
  when: manual
```

**4. Add to Global Version Manager:**

```hcl
# In fitfile-version-manager/versions.tf
# Add platform module versions alongside chart versions
output "production_platform_module_version" {
  description = "Platform module version for production clusters"
  value       = "2.1.4"
}

output "staging_platform_module_version" {
  description = "Platform module version for staging clusters"
  value       = "2.2.7"
}

output "testing_platform_module_version" {
  description = "Platform module version for testing clusters"
  value       = "2.2.7"
}
```

**5. Enhanced Script with TFC Integration:**

```bash
#!/bin/bash
# scripts/sync-from-tfc.sh

# Fetch versions from Terraform Cloud
terraform -chdir=../central-services/hcp/tfc output -json > /tmp/tfc-versions.json

# Update local config file
yq eval -i "
  .environments.production.platform_module_version = \"$(jq -r '.production_platform_module_version.value' /tmp/tfc-versions.json)\" |
  .environments.staging.platform_module_version = \"$(jq -r '.staging_platform_module_version.value' /tmp/tfc-versions.json)\" |
  .environments.testing.platform_module_version = \"$(jq -r '.testing_platform_module_version.value' /tmp/tfc-versions.json)\"
" config/platform-versions.yaml

# Sync cluster configurations
./scripts/manage-platform-versions.sh sync
```

This approach gives you:

- ✅ **Centralized version management** through TFC + local config
- ✅ **Environment-aware versioning**
- ✅ **Automated synchronization** via scripts
- ✅ **Git-based change tracking**
- ✅ **CI/CD integration** for automated updates
- ✅ **Validation and drift detection**

The key insight is to treat the Terraform `version` field as a generated/managed field rather than trying to make it dynamic at runtime.
