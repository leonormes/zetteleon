---
aliases: []
confidence: 
created: 2025-09-04T08:34:27Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T14:24:14Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [topic/technology/kubernetes, troubleshooting]
title: Transpiling K8s Manifests Locally for Testing Cluster
type:
uid: 
updated: 
version:
---

Yes, there are several ways to render all Kubernetes manifests locally. Based on your codebase analysis, here's a comprehensive approach to generate a golden image of your testing cluster configuration:

## **🔧 1. Terraform Helm Charts Rendering**

For the foundational components deployed via Terraform:

```bash
# Navigate to the terraform-helm-fitfile-platform module
cd /Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/TFC-Modules/terraform-helm-fitfile-platform

# Initialize Terraform (if not done)
terraform init

# Generate Terraform plan to see what would be deployed
terraform plan -var-file="testing.tfvars" -out=testing.tfplan

# Use terraform show to extract Helm values
terraform show -json testing.tfplan | jq '.planned_values.root_module.child_modules'

# Alternative: Use helm template directly with extracted values
helm template argocd ./argocd --values argocd-values.yaml --namespace argocd
helm template ingress-nginx ./ingress_nginx --values ingress-values.yaml --namespace ingress-nginx
helm template vault-operator ./vault_operator --values vso-values.yaml --namespace vault-secrets-operator-system
helm template reflector ./reflector --values reflector-values.yaml --namespace reflector
helm template cluster-autoscaler ./cluster_autoscaler --values cluster-autoscaler-values.yaml --namespace kube-system
```

## **🚀 2. ArgoCD Applications Rendering**

### **Method A: Using Existing Template Script (Enhanced)**

Your existing [template.sh](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/helm_chart_deployment/scripts/template.sh:0:0-0:0) script can be enhanced to output manifests:

```bash
#!/usr/bin/env bash
# Enhanced version of scripts/template.sh

DEPLOYMENT="fitfile/testing"
OUTPUT_DIR="./rendered-manifests/testing"
mkdir -p "$OUTPUT_DIR"

BASEDIR=$(dirname $0)
CHARTS_DIR="$BASEDIR/../charts"
FFNODES_DIR="$BASEDIR/../ffnodes"
SELECTED_FFNODE_DIR="$FFNODES_DIR/$DEPLOYMENT"
SELECTED_FFNODE_NAME=$(basename $SELECTED_FFNODE_DIR)

echo "Rendering all manifests for $SELECTED_FFNODE_NAME to $OUTPUT_DIR"

# 1. Render FFNode umbrella chart (generates ArgoCD Applications)
helm template $SELECTED_FFNODE_NAME \
  "$CHARTS_DIR/ffnode" \
  -f "$SELECTED_FFNODE_DIR/values.yaml" \
  --namespace testing \
  > "$OUTPUT_DIR/00-argocd-applications.yaml"

# 2. Render individual service charts
for chart_dir in $CHARTS_DIR/*/; do
  CHART_NAME=$(basename $chart_dir)

  # Skip ffnode (already rendered above)
  [[ "$CHART_NAME" == "ffnode" ]] && continue

  # Find override values
  OVERRIDE_VALUES_DIR=""
  for override_dir in $SELECTED_FFNODE_DIR/values/*/; do
    OVERRIDE_FOLDER_NAME=$(basename $override_dir)
    if [[ "$CHART_NAME" == *"$OVERRIDE_FOLDER_NAME"* ]]; then
      OVERRIDE_VALUES_DIR="$override_dir"
    fi
  done

  # Build values arguments
  OVERRIDES="-f $SELECTED_FFNODE_DIR/values/shared-secrets-values.yaml"
  if [ "$OVERRIDE_VALUES_DIR" != "" ]; then
    for override_file_path in $OVERRIDE_VALUES_DIR/*; do
      OVERRIDES="$OVERRIDES -f $override_file_path"
    done
  fi

  RELEASE_NAME="$SELECTED_FFNODE_NAME-$CHART_NAME"

  echo "Rendering $CHART_NAME..."
  helm template $RELEASE_NAME $chart_dir $OVERRIDES \
    --namespace testing \
    > "$OUTPUT_DIR/$CHART_NAME.yaml" 2>/dev/null || echo "Failed to render $CHART_NAME"
done

echo "All manifests rendered to $OUTPUT_DIR"
```

### **Method B: ArgoCD CLI Rendering**

Use ArgoCD CLI to render applications as ArgoCD would:

```bash
# Install ArgoCD CLI
curl -sSL -o argocd-linux-amd64 https://github.com/argoproj/argo-cd/releases/latest/download/argocd-linux-amd64
sudo install -m 555 argocd-linux-amd64 /usr/local/bin/argocd

# Login to ArgoCD (if accessible)
argocd login testing-argocd.fitfile.net

# Render specific application
argocd app manifests testing-fitconnect --source live > fitconnect-manifests.yaml
argocd app manifests testing-ffcloud-service --source live > ffcloud-manifests.yaml
argocd app manifests testing-mongodb --source live > mongodb-manifests.yaml

# Or get all apps for the testing environment
argocd app list -o name | grep testing | xargs -I {} argocd app manifests {} > {}-manifests.yaml
```

### **Method C: Direct Helm Template with ArgoCD Values**

Extract values from ArgoCD Applications and render directly:

```bash
# Extract MongoDB configuration from ArgoCD Application
yq eval '.spec.source.helm.values' charts/ffnode/templates/mongodb-application.yaml > mongodb-extracted-values.yaml

# Render with extracted values
helm template testing-mongodb \
  oci://fitfileregistry.azurecr.io/helm/mongodb \
  --version "16.5.*" \
  -f mongodb-extracted-values.yaml \
  --namespace testing \
  > mongodb-rendered.yaml
```

## **🛠️ 3. Complete Golden Image Generation Script**

Create a comprehensive script to render everything:

```bash
#!/usr/bin/env bash
# generate-golden-image.sh

set -e

ENVIRONMENT="fitfile/testing"
OUTPUT_DIR="./golden-image-testing"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
VERSIONED_OUTPUT_DIR="${OUTPUT_DIR}-${TIMESTAMP}"

mkdir -p "$VERSIONED_OUTPUT_DIR"/{terraform,argocd,individual-charts}

echo "🚀 Generating Golden Image for Testing Environment"
echo "📁 Output Directory: $VERSIONED_OUTPUT_DIR"

# 1. Terraform Helm Charts
echo "🔧 Rendering Terraform Helm Charts..."
cd TFC-Modules/terraform-helm-fitfile-platform

# Extract and render each module
terraform init -backend=false
terraform plan -var-file="../../testing.tfvars" -out=testing.tfplan 2>/dev/null || echo "⚠️  Terraform plan failed, using defaults"

# Render foundational charts
helm template argocd ./argocd \
  --set server.ingress.hosts[0]="testing-argocd.fitfile.net" \
  --namespace argocd \
  > "$VERSIONED_OUTPUT_DIR/terraform/01-argocd.yaml"

helm template ingress-nginx ./ingress_nginx \
  --namespace ingress-nginx \
  > "$VERSIONED_OUTPUT_DIR/terraform/02-ingress-nginx.yaml"

helm template vault-operator ./vault_operator \
  --namespace vault-secrets-operator-system \
  > "$VERSIONED_OUTPUT_DIR/terraform/03-vault-operator.yaml"

helm template reflector ./reflector \
  --namespace reflector \
  > "$VERSIONED_OUTPUT_DIR/terraform/04-reflector.yaml"

cd ../../helm_chart_deployment

# 2. ArgoCD Applications (App of Apps)
echo "🎯 Rendering ArgoCD Applications..."
helm template testing charts/ffnode \
  -f "ffnodes/$ENVIRONMENT/values.yaml" \
  --namespace testing \
  > "$VERSIONED_OUTPUT_DIR/argocd/00-applications.yaml"

# 3. Individual Service Charts
echo "📦 Rendering Individual Service Charts..."

# Get all charts that would be deployed
CHARTS=(
  "fitconnect"
  "ffcloud-service"
  "frontend"
  "databases"
  "spicedb"
  "workflows-api"
)

for CHART in "${CHARTS[@]}"; do
  if [ -d "charts/$CHART" ]; then
    echo "  📋 Rendering $CHART..."

    # Build values files arguments
    VALUES_ARGS="-f ffnodes/$ENVIRONMENT/values.yaml"

    # Add chart-specific values if they exist
    if [ -d "ffnodes/$ENVIRONMENT/values/$CHART" ]; then
      for values_file in ffnodes/$ENVIRONMENT/values/$CHART/*.yaml; do
        [ -f "$values_file" ] && VALUES_ARGS="$VALUES_ARGS -f $values_file"
      done
    fi

    helm template "testing-$CHART" "charts/$CHART" \
      $VALUES_ARGS \
      --namespace testing \
      > "$VERSIONED_OUTPUT_DIR/individual-charts/$CHART.yaml" 2>/dev/null || echo "    ❌ Failed to render $CHART"
  fi
done

# 4. Workflow Templates
echo "🔄 Rendering Workflow Templates..."
helm template testing-workflows workflows/src \
  -f "ffnodes/$ENVIRONMENT/values.yaml" \
  --namespace testing \
  > "$VERSIONED_OUTPUT_DIR/individual-charts/workflow-templates.yaml"

# 5. Integration Test Templates (if enabled)
if grep -q "workflowsIntegrationTests: true" "ffnodes/$ENVIRONMENT/values.yaml"; then
  echo "🧪 Rendering Integration Test Templates..."
  helm template testing-integration-tests workflows/integration-tests \
    -f "ffnodes/$ENVIRONMENT/values.yaml" \
    --namespace testing \
    > "$VERSIONED_OUTPUT_DIR/individual-charts/integration-tests.yaml"
fi

# 6. Generate summary
echo "📊 Generating Summary..."
cat > "$VERSIONED_OUTPUT_DIR/README.md" << EOF
# Golden Image - Testing Environment

Generated: $(date)
Environment: $ENVIRONMENT

## Structure

- \`terraform/\` - Foundational components deployed via Terraform
- \`argocd/\` - ArgoCD Applications (App of Apps pattern)
- \`individual-charts/\` - Individual service manifests

## Files

### Terraform Components
$(ls -la $VERSIONED_OUTPUT_DIR/terraform/ | tail -n +2 | awk '{print "- " $9 " (" $5 " bytes)"}')

### ArgoCD Applications
$(ls -la $VERSIONED_OUTPUT_DIR/argocd/ | tail -n +2 | awk '{print "- " $9 " (" $5 " bytes)"}')

### Individual Charts
$(ls -la $VERSIONED_OUTPUT_DIR/individual-charts/ | tail -n +2 | awk '{print "- " $9 " (" $5 " bytes)"}')

## Usage

Compare against future renders:
\`\`\`bash
diff -r $VERSIONED_OUTPUT_DIR new-render-directory
\`\`\`
EOF

echo "✅ Golden Image Generated Successfully!"
echo "📁 Location: $VERSIONED_OUTPUT_DIR"
echo "📄 Summary: $VERSIONED_OUTPUT_DIR/README.md"

# Create symlink to latest
ln -sfn "$VERSIONED_OUTPUT_DIR" "$OUTPUT_DIR-latest"
echo "🔗 Latest symlink: $OUTPUT_DIR-latest"
```

## **📋 4. Usage Instructions**

```bash
# Make the script executable
chmod +x generate-golden-image.sh

# Generate golden image for testing
./generate-golden-image.sh

# After refactoring, generate new render
./generate-golden-image.sh

# Compare the two
diff -r golden-image-testing-20250904-083000 golden-image-testing-20250904-090000

# Or use more sophisticated diff tools
code --diff golden-image-testing-20250904-083000 golden-image-testing-20250904-090000
```

## **🎯 5. ArgoCD-Specific Rendering**

For the most accurate ArgoCD rendering, you can also use:

```bash
# If you have access to the ArgoCD server
argocd app diff testing-fitconnect --local-path charts/fitconnect

# Or use the ArgoCD repo-server directly
docker run --rm -v $(pwd):/workspace \
  argoproj/argocd:latest \
  argocd-repo-server --help
```

This approach gives you a complete golden image of your testing cluster configuration that you can use for comparison during refactoring. The versioned output directories allow you to track changes over time and ensure your refactoring doesn't introduce unintended modifications.
